"""Bounded, deterministic raster views for retained candidate inspection.

This module renders bytes only.  It does not publish records, assign IDs, accept
art, or claim visual or engine verification.  Callers publish the returned files.

Resource limits are fixed here so requests fail before publication: 64 MiB per
encoded input, 256 MiB across inputs, 16,384 pixels on either decoded axis,
16,777,216 pixels per decoded frame, 1,024 frames per input, 67,108,864 decoded
pixels in aggregate, 128 contexts, 1,024 declared frame rectangles, 4,096 tile
placements, 65,536 exact visible RGBA colors per measured frame, 4,096 rendered
views, 2,048 pixels on either delivered view axis, 64 MiB per encoded view,
512 MiB across all returned files, and 134,217,728 rendered pixels in aggregate.
A derived context is also limited to the decoded frame bounds (axis and pixel
limits).  Large views are completely tiled into logical-pixel crops before
integer-nearest enlargement.
"""

from __future__ import annotations

import copy
import hashlib
import io
import re
from dataclasses import dataclass
from typing import Any, cast

from PIL import Image, ImageColor, UnidentifiedImageError

from .codec import PixlError

MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_SOURCE_BYTES = 256 * 1024 * 1024
MAX_SOURCE_SIDE = 16_384
MAX_FRAME_PIXELS = 16_777_216
MAX_SOURCE_FRAMES = 1_024
MAX_DECODED_PIXELS = 67_108_864
MAX_MEASURED_COLORS = 65_536
MAX_CONTEXTS = 128
MAX_CONTEXT_RECTS = 1_024
MAX_TILE_PLACEMENTS = 4_096
MAX_VIEWS = 4_096
MAX_VIEW_SIDE = 2_048
MAX_VIEW_BYTES = 64 * 1024 * 1024
MAX_TOTAL_OUTPUT_BYTES = 512 * 1024 * 1024
MAX_RENDERED_PIXELS = 134_217_728

_CONTRACT_KEYS = {"px", "pl", "al"}
_OPTION_REQUIRED = {"references", "scale", "backgrounds"}
_OPTION_OPTIONAL = {"max_side", "contexts"}
_FRAME_CONTEXT_KEYS = {
    "name",
    "kind",
    "source",
    "source_frame",
    "rects",
    "durations_ms",
    "pivots",
}
_TILE_CONTEXT_KEYS = {
    "name",
    "kind",
    "source",
    "source_frame",
    "tile_size",
    "grid",
}
_HEX_COLOR = re.compile(r"#[0-9a-fA-F]{6}")
_FORMAT_SUFFIXES = {
    "BMP": ".bmp",
    "GIF": ".gif",
    "JPEG": ".jpg",
    "PNG": ".png",
    "TIFF": ".tif",
    "WEBP": ".webp",
}


@dataclass
class _Decoded:
    frames: list[Image.Image]
    durations: list[Any]
    suffix: str


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise PixlError(code, detail)


def _integer(value: Any) -> bool:
    return type(value) is int


def _pair(value: Any, *, positive: bool = False) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(_integer(item) for item in value)
        and (not positive or all(item > 0 for item in value))
    )


def _validate_contract(
    contract: Any,
) -> tuple[int, int, set[tuple[int, int, int, int]], str]:
    _require(
        isinstance(contract, dict) and set(contract) == _CONTRACT_KEYS,
        "inspection_contract",
        "expected exactly px, pl and al",
    )
    dimensions = contract["px"]
    _require(
        _pair(dimensions, positive=True),
        "inspection_contract",
        "px must be [positive integer width, positive integer height]",
    )
    palette = contract["pl"]
    _require(
        isinstance(palette, list) and all(isinstance(color, str) for color in palette),
        "inspection_contract",
        "pl must be a JSON list of colors",
    )
    try:
        allowed = cast(
            set[tuple[int, int, int, int]],
            {ImageColor.getcolor(color, "RGBA") for color in palette},
        )
    except (TypeError, ValueError) as error:
        raise PixlError(
            "inspection_contract", "pl contains an invalid color"
        ) from error
    alpha = contract["al"]
    _require(
        alpha in ("binary", "full"),
        "inspection_contract",
        "al must be binary or full",
    )
    return int(dimensions[0]), int(dimensions[1]), allowed, str(alpha)


def _validate_options(options: Any, candidate_id: str) -> dict[str, Any]:
    _require(isinstance(options, dict), "inspection_options", "expected JSON object")
    keys = set(options)
    _require(
        _OPTION_REQUIRED <= keys <= _OPTION_REQUIRED | _OPTION_OPTIONAL,
        "inspection_options",
        "expected references, scale, backgrounds and optional max_side, contexts",
    )
    references = options["references"]
    _require(
        isinstance(references, list)
        and all(isinstance(source, str) and source for source in references),
        "inspection_options",
        "references must be a list of source IDs",
    )
    _require(
        len(references) == len(set(references)) and candidate_id not in references,
        "inspection_options",
        "references must be distinct and exclude the candidate",
    )
    scale = options["scale"]
    _require(
        _integer(scale) and 2 <= scale <= 16,
        "inspection_options",
        "scale must be an integer from 2 through 16",
    )
    backgrounds = options["backgrounds"]
    _require(
        isinstance(backgrounds, list)
        and bool(backgrounds)
        and all(
            isinstance(background, str)
            and (background == "checkerboard" or _HEX_COLOR.fullmatch(background))
            for background in backgrounds
        ),
        "inspection_options",
        "backgrounds must be nonempty #RRGGBB or checkerboard values",
    )
    canonical_backgrounds = [
        background.lower() if background != "checkerboard" else background
        for background in backgrounds
    ]
    _require(
        len(canonical_backgrounds) == len(set(canonical_backgrounds)),
        "inspection_options",
        "backgrounds must be distinct",
    )
    max_side = options.get("max_side", 1024)
    _require(
        _integer(max_side) and 64 <= max_side <= MAX_VIEW_SIDE,
        "inspection_options",
        "max_side must be an integer from 64 through 2048",
    )
    contexts = options.get("contexts", [])
    _require(
        isinstance(contexts, list) and len(contexts) <= MAX_CONTEXTS,
        "inspection_options",
        f"contexts must be a list of at most {MAX_CONTEXTS} entries",
    )
    return {
        "references": list(references),
        "scale": scale,
        "backgrounds": canonical_backgrounds,
        "max_side": max_side,
        "contexts": copy.deepcopy(contexts),
    }


def _decode(data: bytes, source: str, pixel_budget: int) -> _Decoded:
    try:
        with Image.open(io.BytesIO(data)) as image:
            frame_count = getattr(image, "n_frames", 1)
            _require(
                _integer(frame_count) and 0 < frame_count <= MAX_SOURCE_FRAMES,
                "inspection_limit",
                f"{source}: maximum {MAX_SOURCE_FRAMES} decoded frames",
            )
            frames: list[Image.Image] = []
            durations: list[Any] = []
            decoded_pixels = 0
            for index in range(frame_count):
                image.seek(index)
                width, height = image.size
                _require(
                    0 < width <= MAX_SOURCE_SIDE and 0 < height <= MAX_SOURCE_SIDE,
                    "inspection_limit",
                    f"{source}: maximum {MAX_SOURCE_SIDE} pixels on a decoded axis",
                )
                _require(
                    width * height <= MAX_FRAME_PIXELS,
                    "inspection_limit",
                    f"{source}: maximum {MAX_FRAME_PIXELS} pixels per decoded frame",
                )
                _require(
                    decoded_pixels + width * height <= pixel_budget,
                    "inspection_limit",
                    f"maximum {MAX_DECODED_PIXELS} aggregate decoded pixels",
                )
                frames.append(image.convert("RGBA"))
                durations.append(image.info.get("duration"))
                decoded_pixels += width * height
            suffix = _FORMAT_SUFFIXES.get(image.format or "", ".bin")
    except PixlError:
        raise
    except (
        EOFError,
        OSError,
        ValueError,
        UnidentifiedImageError,
        Image.DecompressionBombError,
    ) as error:
        raise PixlError(
            "inspection_image", f"{source}: {type(error).__name__}"
        ) from error
    return _Decoded(frames, durations, suffix)


def _measurement(
    data: bytes,
    decoded: _Decoded,
    width: int | None,
    height: int | None,
    allowed: set[tuple[int, int, int, int]],
    alpha: str,
) -> dict[str, Any]:
    failures: set[str] = set()
    measured_frames = []
    allowed_packed = {
        (red << 24) | (green << 16) | (blue << 8) | alpha_value
        for red, green, blue, alpha_value in allowed
    }
    for index, frame in enumerate(decoded.frames):
        alpha_band = frame.getchannel("A")
        alpha_bytes = alpha_band.tobytes()
        histogram = alpha_band.histogram()
        visible_pixels = sum(histogram[1:])
        fractional = sum(histogram[1:255])
        raw = frame.tobytes()
        colors: set[int] = set()
        for pixel_index, alpha_value in enumerate(alpha_bytes):
            if alpha_value == 0:
                continue
            offset = pixel_index * 4
            colors.add(
                (raw[offset] << 24)
                | (raw[offset + 1] << 16)
                | (raw[offset + 2] << 8)
                | raw[offset + 3]
            )
            _require(
                len(colors) <= MAX_MEASURED_COLORS,
                "inspection_limit",
                f"maximum {MAX_MEASURED_COLORS} exact visible colors per frame",
            )
        bad_colors = sorted(
            color for color in colors if allowed_packed and color not in allowed_packed
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
        measured_frames.append(
            {
                "index": index,
                "width": frame.width,
                "height": frame.height,
                "duration_ms": decoded.durations[index],
                "visible_pixels": visible_pixels,
                "visible_colors": len(colors),
                "fractional_alpha_pixels": fractional,
                "outside_palette": [f"#{color:08x}" for color in bad_colors[:64]],
                "outside_palette_count": len(bad_colors),
                "opaque_components": _components(alpha_bytes, frame.width),
                "visible_bbox": list(bbox) if bbox else None,
            }
        )
    return {
        "pass": not failures,
        "sha256": hashlib.sha256(data).hexdigest(),
        "frame_count": len(decoded.frames),
        "frames": measured_frames,
        "failures": sorted(failures),
        "visual_quality_verified": False,
        "engine_import_verified": False,
        "measurement_notes": (
            "Components use 4-connectivity and nonzero alpha; fragmentation is a "
            "measurement, not automatic aesthetic failure."
        ),
    }


def _find(parent: dict[int, int], label: int) -> int:
    root = label
    while parent[root] != root:
        root = parent[root]
    while parent[label] != label:
        following = parent[label]
        parent[label] = root
        label = following
    return root


def _union(parent: dict[int, int], first: int, second: int) -> int:
    first_root, second_root = _find(parent, first), _find(parent, second)
    root = min(first_root, second_root)
    parent[first_root] = root
    parent[second_root] = root
    return root


def _components(alpha: bytes, width: int) -> int:
    """Count four-connected nonzero-alpha regions with O(width) labels."""
    previous = [0] * width
    next_label = 1
    completed = 0
    for row_start in range(0, len(alpha), width):
        parent = {label: label for label in previous if label}
        current = [0] * width

        for x, alpha_value in enumerate(alpha[row_start : row_start + width]):
            if alpha_value == 0:
                continue
            left = current[x - 1] if x else 0
            above = previous[x]
            if left and above:
                current[x] = _union(parent, left, above)
            elif left or above:
                current[x] = _find(parent, left or above)
            else:
                current[x] = next_label
                parent[next_label] = next_label
                next_label += 1
        prior_roots = {_find(parent, label) for label in previous if label}
        current = [_find(parent, label) if label else 0 for label in current]
        current_roots = {label for label in current if label}
        completed += len(prior_roots - current_roots)
        previous = current
    return completed + len({label for label in previous if label})


def _png(image: Image.Image) -> bytes:
    stream = io.BytesIO()
    image.save(stream, format="PNG", compress_level=9)
    return stream.getvalue()


def _background(
    size: tuple[int, int], value: str, origin: tuple[int, int]
) -> Image.Image:
    if value != "checkerboard":
        return Image.new("RGBA", size, ImageColor.getcolor(value, "RGBA"))
    image = Image.new("RGBA", size)
    pixels = image.load()
    if pixels is None:
        raise PixlError("inspection_image", "could not allocate background")
    ox, oy = origin
    for y in range(size[1]):
        for x in range(size[0]):
            shade = 192 if ((x + ox) // 8 + (y + oy) // 8) % 2 == 0 else 128
            pixels[x, y] = (shade, shade, shade, 255)
    return image


class _Renderer:
    def __init__(self, files: dict[str, bytes], max_side: int):
        self.files = files
        self.max_side = max_side
        self.views: list[dict[str, Any]] = []
        self.rendered_pixels = 0
        self.output_bytes = sum(len(data) for data in files.values())

    def emit(
        self,
        logical: Image.Image,
        *,
        source: str,
        frame: int,
        context: str | None,
        background: str | None,
        scale: int,
        origin: tuple[int, int] = (0, 0),
    ) -> None:
        crop_side = self.max_side // scale
        _require(
            crop_side > 0,
            "inspection_limit",
            "scale leaves no logical pixels within max_side",
        )
        for y in range(0, logical.height, crop_side):
            for x in range(0, logical.width, crop_side):
                width = min(crop_side, logical.width - x)
                height = min(crop_side, logical.height - y)
                _require(
                    len(self.views) < MAX_VIEWS,
                    "inspection_limit",
                    f"maximum {MAX_VIEWS} rendered views",
                )
                crop = logical.crop((x, y, x + width, y + height))
                crop_origin = (origin[0] + x, origin[1] + y)
                if background is not None:
                    crop = Image.alpha_composite(
                        _background(crop.size, background, crop_origin), crop
                    )
                if scale != 1:
                    crop = crop.resize(
                        (crop.width * scale, crop.height * scale),
                        Image.Resampling.NEAREST,
                    )
                pixels = crop.width * crop.height
                _require(
                    self.rendered_pixels + pixels <= MAX_RENDERED_PIXELS,
                    "inspection_limit",
                    f"maximum {MAX_RENDERED_PIXELS} rendered pixels",
                )
                data = _png(crop)
                _require(
                    len(data) <= MAX_VIEW_BYTES
                    and self.output_bytes + len(data) <= MAX_TOTAL_OUTPUT_BYTES,
                    "inspection_limit",
                    "encoded view or aggregate returned files exceed documented limits",
                )
                path = f"views/{len(self.views):04d}.png"
                self.files[path] = data
                self.views.append(
                    {
                        "path": path,
                        "source": source,
                        "frame": frame,
                        "context": context,
                        "scale": scale,
                        "background": background,
                        "crop": [crop_origin[0], crop_origin[1], width, height],
                        "width": crop.width,
                        "height": crop.height,
                        "sha256": hashlib.sha256(data).hexdigest(),
                    }
                )
                self.rendered_pixels += pixels
                self.output_bytes += len(data)


def _emit_variants(
    renderer: _Renderer,
    image: Image.Image,
    source: str,
    frame: int,
    context: str | None,
    options: dict[str, Any],
    origin: tuple[int, int] = (0, 0),
) -> None:
    renderer.emit(
        image,
        source=source,
        frame=frame,
        context=context,
        background=None,
        scale=1,
        origin=origin,
    )
    for background in options["backgrounds"]:
        for scale in (1, options["scale"]):
            renderer.emit(
                image,
                source=source,
                frame=frame,
                context=context,
                background=background,
                scale=scale,
                origin=origin,
            )


def _validate_source_frame(context: dict[str, Any], decoded: _Decoded) -> int:
    source_frame = context.get("source_frame")
    if not _integer(source_frame):
        raise PixlError(
            "inspection_context",
            "source_frame must select an existing decoded frame",
        )
    source_frame = cast(int, source_frame)
    _require(
        0 <= source_frame < len(decoded.frames),
        "inspection_context",
        "source_frame must select an existing decoded frame",
    )
    return source_frame


def _frame_strip(
    frames: list[Image.Image], pivots: list[Any]
) -> tuple[Image.Image, str]:
    if all(pivot is not None for pivot in pivots):
        left = max(pivot[0] for pivot in pivots)
        right = max(
            frame.width - pivot[0] for frame, pivot in zip(frames, pivots, strict=True)
        )
        top = max(pivot[1] for pivot in pivots)
        bottom = max(
            frame.height - pivot[1] for frame, pivot in zip(frames, pivots, strict=True)
        )
        cell_width, cell_height = left + right, top + bottom
        size = (cell_width * len(frames), cell_height)
        _validate_context_size(size, "frame comparison")
        strip = Image.new("RGBA", size)
        for index, (frame, pivot) in enumerate(zip(frames, pivots, strict=True)):
            strip.paste(
                frame,
                (index * cell_width + left - pivot[0], top - pivot[1]),
            )
        return strip, "common_pivot"
    size = (sum(frame.width for frame in frames), max(frame.height for frame in frames))
    _validate_context_size(size, "frame comparison")
    strip = Image.new("RGBA", size)
    offset = 0
    for frame in frames:
        strip.paste(frame, (offset, 0))
        offset += frame.width
    return strip, "top_left"


def _validate_context_size(size: tuple[int, int], label: str) -> None:
    width, height = size
    _require(
        width <= MAX_SOURCE_SIDE
        and height <= MAX_SOURCE_SIDE
        and width * height <= MAX_FRAME_PIXELS,
        "inspection_limit",
        f"{label} context exceeds decoded frame bounds",
    )


def _render_frame_context(
    renderer: _Renderer,
    context: dict[str, Any],
    decoded: _Decoded,
    options: dict[str, Any],
) -> dict[str, Any]:
    _require(
        set(context) == _FRAME_CONTEXT_KEYS,
        "inspection_context",
        "frames context has unknown or missing fields",
    )
    source_frame = _validate_source_frame(context, decoded)
    source_image = decoded.frames[source_frame]
    rects = context["rects"]
    durations = context["durations_ms"]
    pivots = context["pivots"]
    _require(
        isinstance(rects, list) and 0 < len(rects) <= MAX_CONTEXT_RECTS,
        "inspection_context",
        f"rects must contain 1 through {MAX_CONTEXT_RECTS} entries",
    )
    _require(
        isinstance(durations, list)
        and isinstance(pivots, list)
        and len(durations) == len(rects) == len(pivots),
        "inspection_context",
        "rects, durations_ms and pivots must have equal lengths",
    )
    frames = []
    for index, rect in enumerate(rects):
        _require(
            isinstance(rect, list)
            and len(rect) == 4
            and all(_integer(value) for value in rect),
            "inspection_context",
            "each rect must be [x, y, positive width, positive height]",
        )
        x, y, width, height = rect
        _require(
            x >= 0
            and y >= 0
            and width > 0
            and height > 0
            and x + width <= source_image.width
            and y + height <= source_image.height,
            "inspection_context",
            "frame rect lies outside the selected decoded frame",
        )
        duration = durations[index]
        _require(
            duration is None or (_integer(duration) and duration > 0),
            "inspection_context",
            "durations_ms entries must be positive integers or null",
        )
        pivot = pivots[index]
        _require(
            pivot is None
            or (_pair(pivot) and 0 <= pivot[0] < width and 0 <= pivot[1] < height),
            "inspection_context",
            "pivots entries must be local integer coordinates or null",
        )
        frame = source_image.crop((x, y, x + width, y + height))
        frames.append(frame)
        _emit_variants(
            renderer,
            frame,
            context["source"],
            source_frame,
            f"{context['name']}:frame:{index}",
            options,
            (x, y),
        )
    strip, alignment = _frame_strip(frames, pivots)
    _emit_variants(
        renderer,
        strip,
        context["source"],
        source_frame,
        f"{context['name']}:comparison",
        options,
    )
    return {
        "name": context["name"],
        "kind": "frames",
        "source": context["source"],
        "source_frame": source_frame,
        "rects": copy.deepcopy(rects),
        "durations_ms": copy.deepcopy(durations),
        "pivots": copy.deepcopy(pivots),
        "alignment": alignment,
    }


def _edge_differences(first: Image.Image, second: Image.Image, orientation: str) -> int:
    if orientation == "horizontal":
        return sum(
            first.getpixel((first.width - 1, y)) != second.getpixel((0, y))
            for y in range(first.height)
        )
    return sum(
        first.getpixel((x, first.height - 1)) != second.getpixel((x, 0))
        for x in range(first.width)
    )


def _render_tile_context(
    renderer: _Renderer,
    context: dict[str, Any],
    decoded: _Decoded,
    options: dict[str, Any],
) -> dict[str, Any]:
    _require(
        set(context) == _TILE_CONTEXT_KEYS,
        "inspection_context",
        "tiles context has unknown or missing fields",
    )
    source_frame = _validate_source_frame(context, decoded)
    source_image = decoded.frames[source_frame]
    tile_size = context["tile_size"]
    _require(
        _pair(tile_size, positive=True),
        "inspection_context",
        "tile_size must be [positive integer width, positive integer height]",
    )
    tile_width, tile_height = tile_size
    _require(
        source_image.width % tile_width == 0 and source_image.height % tile_height == 0,
        "inspection_context",
        "tile_size must divide the selected decoded frame exactly",
    )
    grid = context["grid"]
    _require(
        isinstance(grid, list)
        and bool(grid)
        and all(isinstance(row, list) and bool(row) for row in grid),
        "inspection_context",
        "grid must be a nonempty rectangular list",
    )
    columns = len(grid[0])
    _require(
        all(len(row) == columns for row in grid)
        and len(grid) * columns <= MAX_TILE_PLACEMENTS,
        "inspection_context",
        f"grid must be rectangular with at most {MAX_TILE_PLACEMENTS} placements",
    )
    sheet_columns = source_image.width // tile_width
    tile_count = sheet_columns * (source_image.height // tile_height)
    _require(
        all(
            _integer(index) and 0 <= index < tile_count for row in grid for index in row
        ),
        "inspection_context",
        "grid contains an invalid zero-based row-major tile index",
    )
    width, height = columns * tile_width, len(grid) * tile_height
    _validate_context_size((width, height), "tile neighborhood")

    def tile(index: int) -> Image.Image:
        x = (index % sheet_columns) * tile_width
        y = (index // sheet_columns) * tile_height
        return source_image.crop((x, y, x + tile_width, y + tile_height))

    neighborhood = Image.new("RGBA", (width, height))
    for row_index, row in enumerate(grid):
        for column_index, index in enumerate(row):
            neighborhood.paste(
                tile(index), (column_index * tile_width, row_index * tile_height)
            )
    adjacent = []
    for row_index, row in enumerate(grid):
        for column_index in range(columns - 1):
            first, second = row[column_index], row[column_index + 1]
            adjacent.append(
                {
                    "orientation": "horizontal",
                    "at": [row_index, column_index],
                    "first": first,
                    "second": second,
                    "differing_pixels": _edge_differences(
                        tile(first), tile(second), "horizontal"
                    ),
                }
            )
    for row_index in range(len(grid) - 1):
        for column_index in range(columns):
            first, second = (
                grid[row_index][column_index],
                grid[row_index + 1][column_index],
            )
            adjacent.append(
                {
                    "orientation": "vertical",
                    "at": [row_index, column_index],
                    "first": first,
                    "second": second,
                    "differing_pixels": _edge_differences(
                        tile(first), tile(second), "vertical"
                    ),
                }
            )
    _emit_variants(
        renderer,
        neighborhood,
        context["source"],
        source_frame,
        f"{context['name']}:neighborhood",
        options,
    )
    return {
        "name": context["name"],
        "kind": "tiles",
        "source": context["source"],
        "source_frame": source_frame,
        "tile_size": copy.deepcopy(tile_size),
        "grid": copy.deepcopy(grid),
        "adjacent_edges": adjacent,
    }


def _render_context(
    renderer: _Renderer,
    context: Any,
    decoded: dict[str, _Decoded],
    selected: set[str],
    options: dict[str, Any],
) -> dict[str, Any]:
    _require(
        isinstance(context, dict), "inspection_context", "context must be an object"
    )
    name, kind, source = context.get("name"), context.get("kind"), context.get("source")
    _require(
        isinstance(name, str) and bool(name),
        "inspection_context",
        "context name must be a nonempty string",
    )
    _require(
        kind in ("frames", "tiles") and isinstance(source, str) and source in selected,
        "inspection_context",
        "context kind or selected source is invalid",
    )
    if kind == "frames":
        return _render_frame_context(
            renderer, context, decoded[cast(str, source)], options
        )
    return _render_tile_context(renderer, context, decoded[cast(str, source)], options)


def render(
    snapshots: dict[str, bytes],
    candidate_id: str,
    contract: dict[str, Any],
    options: dict[str, Any],
) -> dict[str, Any]:
    """Return retained input/view bytes and factual metadata without publication."""
    _require(
        isinstance(candidate_id, str) and bool(candidate_id),
        "inspection_sources",
        "candidate_id must be a nonempty string",
    )
    width, height, allowed, alpha = _validate_contract(contract)
    canonical = _validate_options(options, candidate_id)
    source_order = [candidate_id, *canonical["references"]]
    _require(
        isinstance(snapshots, dict)
        and set(snapshots) == set(source_order)
        and all(type(data) is bytes for data in snapshots.values()),
        "inspection_sources",
        "snapshots must contain exactly the candidate and explicit references as bytes",
    )
    total_source_bytes = sum(len(snapshots[source]) for source in source_order)
    _require(
        all(0 < len(snapshots[source]) <= MAX_SOURCE_BYTES for source in source_order)
        and total_source_bytes <= MAX_TOTAL_SOURCE_BYTES,
        "inspection_limit",
        "encoded inputs exceed per-source or aggregate byte limits",
    )

    decoded: dict[str, _Decoded] = {}
    decoded_pixels = 0
    for source in source_order:
        value = _decode(snapshots[source], source, MAX_DECODED_PIXELS - decoded_pixels)
        decoded_pixels += sum(frame.width * frame.height for frame in value.frames)
        _require(
            decoded_pixels <= MAX_DECODED_PIXELS,
            "inspection_limit",
            f"maximum {MAX_DECODED_PIXELS} aggregate decoded pixels",
        )
        decoded[source] = value

    files: dict[str, bytes] = {}
    inputs = []
    measurements = {}
    for index, source in enumerate(source_order):
        data = snapshots[source]
        path = f"inputs/{index:04d}{decoded[source].suffix}"
        files[path] = data
        digest = hashlib.sha256(data).hexdigest()
        inputs.append({"source": source, "path": path, "sha256": digest})
        if source == candidate_id:
            measurements[source] = _measurement(
                data, decoded[source], width, height, allowed, alpha
            )
        else:
            measurements[source] = _measurement(
                data, decoded[source], None, None, set(), "full"
            )

    renderer = _Renderer(files, canonical["max_side"])
    for source in source_order:
        for frame_index, frame in enumerate(decoded[source].frames):
            _emit_variants(renderer, frame, source, frame_index, None, canonical)

    names: set[str] = set()
    observations = []
    selected = set(source_order)
    for context in canonical["contexts"]:
        _require(
            isinstance(context, dict)
            and isinstance(context.get("name"), str)
            and context["name"] not in names,
            "inspection_context",
            "context names must be distinct",
        )
        names.add(context["name"])
        observations.append(
            _render_context(renderer, context, decoded, selected, canonical)
        )

    return {
        "files": files,
        "views": renderer.views,
        "measurements": measurements,
        "inputs": inputs,
        "options": canonical,
        "context_observations": observations,
    }
