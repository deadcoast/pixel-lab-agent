"""Measured image properties. Artistic quality remains a separate inspection."""

from collections import Counter
from pathlib import Path
import hashlib
from io import BytesIO

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


def inspect(path, width=None, height=None, palette=None, alpha="binary"):
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
    frames, failures = [], set()
    try:
        with Path(path).open("rb") as stream:
            snapshot = stream.read(MAX_IMAGE_BYTES + 1)
        if len(snapshot) > MAX_IMAGE_BYTES:
            raise PixlError("image_limit", "maximum 256 MiB encoded image")
        snapshot_hash = hashlib.sha256(snapshot).hexdigest()
        with Image.open(BytesIO(snapshot)) as image:
            if getattr(image, "n_frames", 1) > 1024:
                raise PixlError("image_limit", "maximum 16M pixels/frame and 1024 frames")
            total_pixels = 0
            for i in range(getattr(image, "n_frames", 1)):
                image.seek(i)
                count = image.width * image.height
                total_pixels += count
                if count > MAX_FRAME_PIXELS or total_pixels > MAX_TOTAL_PIXELS:
                    raise PixlError("image_limit", "maximum 16M pixels/frame and 64M actual pixels total")
                frame = image.convert("RGBA")
                pixels = list(frame.get_flattened_data()) if hasattr(frame, "get_flattened_data") else list(frame.getdata())
                colors = Counter(p for p in pixels if p[3])
                points = {(index % frame.width, index // frame.width) for index, p in enumerate(pixels) if p[3]}
                bad_colors = sorted(color for color in colors if allowed and color not in allowed)
                fractional = sum(1 for p in pixels if 0 < p[3] < 255)
                if (width is not None and frame.width != width) or (height is not None and frame.height != height):
                    failures.add("dimensions")
                if bad_colors:
                    failures.add("palette")
                if alpha == "binary" and fractional:
                    failures.add("alpha")
                frames.append({"index": i, "width": frame.width, "height": frame.height,
                               "duration_ms": image.info.get("duration"), "visible_pixels": len(points),
                               "visible_colors": len(colors), "fractional_alpha_pixels": fractional,
                               "outside_palette": ["#" + "".join(f"{v:02x}" for v in c) for c in bad_colors[:64]],
                               "outside_palette_count": len(bad_colors), "opaque_components": components(points),
                               "visible_bbox": list(frame.getbbox()) if frame.getbbox() else None})
    except PixlError:
        raise
    except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as error:
        raise PixlError("image_read", f"{Path(path).name}: {type(error).__name__}") from error
    return {"pass": not failures, "sha256": snapshot_hash, "frame_count": len(frames),
            "frames": frames, "failures": sorted(failures), "visual_quality_verified": False,
            "engine_import_verified": False,
            "measurement_notes": "Components use 4-connectivity and nonzero alpha; fragmentation is a measurement, not automatic aesthetic failure."}
