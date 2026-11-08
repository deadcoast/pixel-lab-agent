"""Measured image properties. Artistic quality remains a separate inspection."""

import hashlib
import heapq
from collections import Counter
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageColor, UnidentifiedImageError

from .codec import PixlError

MAX_FRAME_PIXELS = 16_777_216
MAX_TOTAL_PIXELS = 67_108_864
MAX_IMAGE_BYTES = 256 * 1024 * 1024


def components(points):
    points = set(points)
    count = 0
    while points:
        count += 1
        pending = [points.pop()]
        while pending:
            x, y = pending.pop()
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in points:
                    points.remove(neighbor)
                    pending.append(neighbor)
    return count


def color_regions(pixels, width, color):
    """Exact RGBA components; bounded, deterministic top-left box reporting."""
    points = {
        (i % width, i // width) for i, pixel in enumerate(pixels) if pixel == color
    }
    pixel_count, count = len(points), 0
    boxes: list[tuple[int, int, int, int]] = []
    while points:
        count += 1
        x, y = points.pop()
        left = right = x
        top = bottom = y
        pending = [(x, y)]
        while pending:
            x, y = pending.pop()
            left, top = min(left, x), min(top, y)
            right, bottom = max(right, x), max(bottom, y)
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in points:
                    points.remove(neighbor)
                    pending.append(neighbor)
        # A max heap retains the first 128 boxes in top/left order.
        key = (-top, -left, -(bottom + 1), -(right + 1))
        heapq.heappush(boxes, key)
        if len(boxes) > 128:
            heapq.heappop(boxes)
    ordered = sorted(tuple(-v for v in box) for box in boxes)
    return {
        "color": "#" + "".join(f"{v:02x}" for v in color),
        "pixels": pixel_count,
        "component_count": count,
        "boxes": [[left, top, right, bottom] for top, left, bottom, right in ordered],
        "boxes_truncated": count > len(boxes),
        "coordinates": "zero-based [left, top, right, bottom]; right/bottom exclusive; 4-connected",
    }


def inspect(path, width=None, height=None, palette=None, alpha="binary", regions=None):
    if alpha not in ("binary", "full"):
        raise PixlError("alpha_policy", alpha)
    for value in (width, height):
        if value is not None and (type(value) is not int or value <= 0):
            raise PixlError("dimensions", "expected positive pixel dimensions")
    allowed = set()
    try:
        for color in palette or []:
            allowed.add(ImageColor.getcolor(color, "RGBA"))
    except (ValueError, TypeError) as error:
        raise PixlError("palette", "invalid color") from error
    selected = []
    if regions is not None:
        if not isinstance(regions, list) or not 1 <= len(regions) <= 16:
            raise PixlError("regions", "select 1..16 exact RGBA colors")
        try:
            selected = list(
                dict.fromkeys(ImageColor.getcolor(c, "RGBA") for c in regions)
            )
        except (ValueError, TypeError, AttributeError) as error:
            raise PixlError("regions", "invalid color") from error
    frames, failures = [], set()
    try:
        with Path(path).open("rb") as stream:
            snapshot = stream.read(MAX_IMAGE_BYTES + 1)
        if len(snapshot) > MAX_IMAGE_BYTES:
            raise PixlError("image_limit", "maximum 256 MiB encoded image")
        snapshot_hash = hashlib.sha256(snapshot).hexdigest()
        with Image.open(BytesIO(snapshot)) as image:
            if getattr(image, "n_frames", 1) > 1024:
                raise PixlError(
                    "image_limit", "maximum 16M pixels/frame and 1024 frames"
                )
            total_pixels = 0
            for i in range(getattr(image, "n_frames", 1)):
                image.seek(i)
                count = image.width * image.height
                total_pixels += count
                if count > MAX_FRAME_PIXELS or total_pixels > MAX_TOTAL_PIXELS:
                    raise PixlError(
                        "image_limit",
                        "maximum 16M pixels/frame and 64M actual pixels total",
                    )
                frame = image.convert("RGBA")
                # RGBA band bytes guarantee integer channels without mode-dependent pixel types.
                pixels = list(
                    zip(*(band.tobytes() for band in frame.split()), strict=True)
                )
                colors = Counter(
                    pixel for pixel in pixels if len(pixel) > 3 and pixel[3]
                )
                points = {
                    (index % frame.width, index // frame.width)
                    for index, pixel in enumerate(pixels)
                    if len(pixel) > 3 and pixel[3]
                }
                bad_colors = sorted(
                    color for color in colors if allowed and color not in allowed
                )
                fractional = sum(
                    bool(0 < pixel[3] < 255) for pixel in pixels if len(pixel) > 3
                )
                if (width is not None and frame.width != width) or (
                    height is not None and frame.height != height
                ):
                    failures.add("dimensions")
                if bad_colors:
                    failures.add("palette")
                if alpha == "binary" and fractional:
                    failures.add("alpha")
                bbox = frame.getbbox()
                frames.append(
                    {
                        "index": i,
                        "width": frame.width,
                        "height": frame.height,
                        "duration_ms": image.info.get("duration"),
                        "visible_pixels": len(points),
                        "visible_colors": len(colors),
                        "fractional_alpha_pixels": fractional,
                        "outside_palette": [
                            "#" + "".join(f"{v:02x}" for v in c)
                            for c in bad_colors[:64]
                        ],
                        "outside_palette_count": len(bad_colors),
                        "opaque_components": components(points),
                        "visible_bbox": list(bbox) if bbox else None,
                    }
                )
                if selected:
                    frames[-1]["color_regions"] = [
                        color_regions(pixels, frame.width, color) for color in selected
                    ]
    except PixlError:
        raise
    except (
        OSError,
        ValueError,
        UnidentifiedImageError,
        Image.DecompressionBombError,
    ) as error:
        raise PixlError(
            "image_read", f"{Path(path).name}: {type(error).__name__}"
        ) from error
    return {
        "pass": not failures,
        "sha256": snapshot_hash,
        "frame_count": len(frames),
        "frames": frames,
        "failures": sorted(failures),
        "visual_quality_verified": False,
        "engine_import_verified": False,
        "measurement_notes": "Components use 4-connectivity and nonzero alpha; fragmentation is a measurement, not automatic aesthetic failure.",
    }
