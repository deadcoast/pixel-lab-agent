"""Deterministic, offline proofs of bounded pixel-art mechanics.

These are executable reference fixtures, not tests of an external image service
or promises that a game engine implements the same systems. Each observation is
compared with hand-derived fixture expectations or an explicit invariant. No
network, renderer, account or external source code is involved.

At import, the executing module code is compared with a fresh compilation of
the captured source, including nested code and constants, before binding its
hash. This CPython guard rejects stale timestamp caches. The source hash is
checked again at run entry and after fixtures, before publishing a receipt.
These checks do not attest a hostile loader/interpreter, dependencies, in-memory
patches, or transient source edits restored between checks.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from hashlib import sha256
from itertools import pairwise
from pathlib import Path
from typing import cast

from PIL import Image
from PIL import __version__ as pillow_version

_IMPORTED_SOURCE_PATH = Path(__file__).resolve()
_IMPORTED_SOURCE_BYTES = _IMPORTED_SOURCE_PATH.read_bytes()
# CPython code equality compares nested code constants recursively. Comparing
# only co_code misses changed function bodies and constants. Compile without
# executing or inheriting flags; match this process's -O/-OO optimization.
_EXECUTING_MODULE_CODE = sys._getframe().f_code
_SOURCE_MODULE_CODE = compile(
    _IMPORTED_SOURCE_BYTES,
    _EXECUTING_MODULE_CODE.co_filename,
    "exec",
    dont_inherit=True,
    optimize=sys.flags.optimize,
)
if _EXECUTING_MODULE_CODE != _SOURCE_MODULE_CODE:
    raise RuntimeError(
        "runner_source_mismatch: executing runner code does not match its source; refresh the runner bytecode cache and reload the module"
    )
_IMPORTED_SOURCE_SHA256 = sha256(_IMPORTED_SOURCE_BYTES).hexdigest()
del _IMPORTED_SOURCE_BYTES, _EXECUTING_MODULE_CODE, _SOURCE_MODULE_CODE


def _assert_runner_source_unchanged() -> None:
    try:
        current = sha256(_IMPORTED_SOURCE_PATH.read_bytes()).hexdigest()
    except OSError as error:
        raise RuntimeError(
            "runner_source_changed: imported runner source is unavailable; restore it and reload the module"
        ) from error
    if current != _IMPORTED_SOURCE_SHA256:
        raise RuntimeError(
            "runner_source_changed: runner source changed after import; reload the module before running proofs"
        )


_BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
_PALETTE = (
    (16, 24, 32, 255),
    (64, 96, 80, 255),
    (144, 176, 112, 255),
    (224, 216, 144, 255),
)


def _dither_mask(threshold: int) -> list[list[bool]]:
    return [[rank < threshold for rank in row] for row in _BAYER]


def _components(points: set[tuple[int, int]], diagonal: bool = False) -> list[set]:
    pending = set(points)
    components = []
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    while pending:
        seed = min(pending)
        pending.remove(seed)
        found, queue = {seed}, [seed]
        while queue:
            x, y = queue.pop()
            for dx, dy in steps:
                neighbor = (x + dx, y + dy)
                if neighbor in pending:
                    pending.remove(neighbor)
                    found.add(neighbor)
                    queue.append(neighbor)
        components.append(found)
    return components


def _palette_violations(image: Image.Image) -> list[list[int]]:
    return [
        [x, y]
        for y in range(image.height)
        for x in range(image.width)
        if image.getpixel((x, y)) not in _PALETTE
    ]


def _band(intensity: float, count: int = 4) -> int:
    if not math.isfinite(intensity) or count < 2:
        raise ValueError("Light intensity must be finite and band count at least two")
    return math.floor(min(1.0, max(0.0, intensity)) * (count - 1) + 0.5)


def _corner_match(left: int, right: int, axis: str) -> bool:
    # Bit assignment is TL=1, TR=2, BR=4, BL=8, unlike an edge-mask set.
    if axis == "horizontal":
        return bool(left & 2) == bool(right & 1) and bool(left & 4) == bool(right & 8)
    return bool(left & 8) == bool(right & 1) and bool(left & 4) == bool(right & 2)


def _at_time(frames: list[tuple[str, int]], time_ms: int) -> str:
    if not frames or any(duration <= 0 for _, duration in frames):
        raise ValueError("Animation requires frames with positive durations")
    local = time_ms % sum(duration for _, duration in frames)
    for name, duration in frames:
        if local < duration:
            return name
        local -= duration
    raise AssertionError("Unreachable timeline state")


def _place(
    point: Sequence[float], translation: tuple[float, float], degrees: float
) -> list[float]:
    angle = math.radians(degrees)
    x, y = point
    return [
        round(x * math.cos(angle) - y * math.sin(angle) + translation[0], 9),
        round(x * math.sin(angle) + y * math.cos(angle) + translation[1], 9),
    ]


def _normalize(vector) -> tuple[float, ...]:
    length = math.sqrt(sum(value * value for value in vector))
    if not length or not math.isfinite(length):
        raise ValueError("Normal vector must have finite nonzero length")
    return tuple(value / length for value in vector)


def _sand(seed: int) -> tuple[list, list]:
    # Persistent particle IDs make duplicate movement observable. This bounded
    # model has powder, a floor and one-cell moves, not general fluid chemistry.
    grid = {(3, 1): 1, (3, 2): 2, (4, 1): 3}
    states = [dict(grid)]
    move_logs = []
    for tick in range(20):
        updated = set()
        moves = []
        for y in range(6, -1, -1):
            for x in range(8) if tick % 2 == 0 else range(7, -1, -1):
                particle = grid.get((x, y))
                if particle is None or particle in updated:
                    continue
                updated.add(particle)
                direction = (
                    1
                    if (seed ^ (x * 73856093) ^ (y * 19349663) ^ (tick * 83492791)) & 1
                    else -1
                )
                for nx, ny in (
                    (x, y + 1),
                    (x + direction, y + 1),
                    (x - direction, y + 1),
                ):
                    if 0 <= nx < 8 and ny < 7 and (nx, ny) not in grid:
                        del grid[(x, y)]
                        grid[(nx, ny)] = particle
                        moves.append((particle, x, y, nx, ny))
                        break
        states.append(dict(grid))
        move_logs.append(moves)
    return states, move_logs


def _wake_chunks(old: tuple[int, int], new: tuple[int, int]) -> set[int]:
    """One-cell influence halo in the two horizontal chunks of the fixture."""
    return {
        x // 8
        for point in (old, new)
        for x in range(point[0] - 1, point[0] + 2)
        if 0 <= x < 16
    }


def _region_world(dirty: bool) -> dict:
    static = {(x, 7) for x in range(16)} | {(6, 2), (7, 2)}
    position = (7, 1)
    active = {0}
    states: list[tuple[int, int]] = [position]
    wakes, visits = [], 0
    for _ in range(8):
        next_active = set()
        updated = False
        for y in range(7, -1, -1):
            for x in range(16):
                if dirty and x // 8 not in active:
                    continue
                visits += 1
                if (x, y) != position or updated:
                    continue
                updated = True
                for destination in ((x, y + 1), (x + 1, y + 1), (x - 1, y + 1)):
                    nx, ny = destination
                    if 0 <= nx < 16 and 0 <= ny < 8 and destination not in static:
                        old = position
                        position = destination
                        next_active.update(_wake_chunks(old, position))
                        break
        active = next_active
        states.append(position)
        wakes.append(sorted(active))
    return {"positions": states, "wakes": wakes, "visits": visits}


def _border_mismatches(image: Image.Image) -> list[list]:
    mismatches = [
        ["horizontal", y]
        for y in range(image.height)
        if image.getpixel((0, y)) != image.getpixel((image.width - 1, y))
    ]
    for x in range(image.width):
        if image.getpixel((x, 0)) != image.getpixel((x, image.height - 1)):
            mismatches.append(["vertical", x])
    return mismatches


def _key_landmarks(points: set[tuple[int, int]]) -> dict:
    background = {(x, y) for y in range(16) for x in range(16)} - points
    holes = [
        part
        for part in _components(background)
        if not any(x in (0, 15) or y in (0, 15) for x, y in part)
    ]
    tooth_region = {(x, y) for x, y in points if 9 <= x <= 14 and 8 <= y <= 10}
    return {
        "hole": any((4, 6) in hole for hole in holes),
        "shaft": all((x, y) in points for x in range(7, 14) for y in (6, 7)),
        "teeth": len(_components(tooth_region)),
    }


def run_all(output_dir: Path | str) -> dict:
    """Run reference fixtures, write PNG evidence and poc-report.json, return it.

    Filesystem errors propagate rather than claiming a report was saved. An
    individual fixture's exception is recorded as a failed check and does not
    suppress subsequent checks. Re-running the same implementation produces the
    same report; wall-clock timestamps are deliberately not simulated evidence.
    """
    _assert_runner_source_unchanged()
    from .service import resource_root

    resources = resource_root()
    knowledge_bytes = (resources / "knowledge" / "pixel-art.json").read_bytes()
    knowledge_hash = sha256(knowledge_bytes).hexdigest()
    source_paths = {
        source["path"]
        for method in json.loads(knowledge_bytes)["methods"]
        for source in method["sources"]
    }
    source_hashes = {
        path: sha256((resources / path).read_bytes()).hexdigest()
        for path in sorted(source_paths)
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    checks = []
    artifacts = []

    def save_image(name: str, image: Image.Image) -> None:
        path = output / name
        image.save(path, format="PNG")
        artifacts.append(
            {
                "path": name,
                "sha256": sha256(path.read_bytes()).hexdigest(),
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
            }
        )

    def check(
        identifier: str,
        method_ids: list[str],
        expected: dict,
        operation: Callable[[], dict],
        limitations: str,
        accepts: Callable[[dict], bool] | None = None,
    ) -> None:
        try:
            observed = operation()
            json.dumps(observed, allow_nan=False)
            passed = accepts(observed) if accepts else observed == expected
        except Exception as error:  # noqa: BLE001 - Retain fixture exceptions as failed proof observations.
            observed = {"error": f"{type(error).__name__}: {error}"}
            passed = False
        checks.append(
            {
                "id": identifier,
                "method_ids": method_ids,
                "status": "pass" if passed else "fail",
                "observed": observed,
                "expected": expected,
                "limitations": limitations,
            }
        )

    def dither_coverage():
        masks = [_dither_mask(value) for value in (4, 8, 12)]
        image = Image.new("RGBA", (12, 4))
        for index, mask in enumerate(masks):
            for y, row in enumerate(mask):
                for x, occupied in enumerate(row):
                    image.putpixel(
                        (index * 4 + x, y),
                        (255, 255, 255, 255) if occupied else (0, 0, 0, 255),
                    )
        save_image("dither-coverage.png", image)
        return {"counts": [sum(sum(row) for row in mask) for mask in masks]}

    check(
        "dither-coverage-4x4",
        ["dither-coverage"],
        {"counts": [4, 8, 12]},
        dither_coverage,
        "Counts only this specified 4x4 ordered pattern; does not establish texture quality.",
    )

    def dither_phase():
        start = _dither_mask(8)
        frames = [
            [[start[y][(x - phase) % 4] for x in range(4)] for y in range(4)]
            for phase in range(5)
        ]
        return {
            "counts": [sum(sum(row) for row in frame) for frame in frames],
            "returns_to_start": frames[0] == frames[-1],
        }

    check(
        "dither-phase-cycle",
        ["dither-phase-motion"],
        {"counts": [8, 8, 8, 8, 8], "returns_to_start": True},
        dither_phase,
        "Proves coverage and periodicity, not comfort, directional readability or absence of visual flicker.",
    )

    def palette_membership():
        image = Image.new("RGBA", (4, 4))
        image.putdata([_PALETTE[index % 4] for index in range(16)])
        valid = _palette_violations(image)
        image.putpixel((2, 1), (64, 96, 81, 255))
        return {
            "valid_violations": valid,
            "mutant_violations": _palette_violations(image),
        }

    check(
        "palette-membership",
        ["palette-contract"],
        {"valid_violations": [], "mutant_violations": [[2, 1]]},
        palette_membership,
        "Exact RGBA membership for an opaque fixture; no claim about palette taste or perceptual distance.",
    )

    def palette_bands():
        bands = [_band(value) for value in (-1, 0, 0.2, 0.5, 0.8, 1, 2)]
        rejected = False
        try:
            _band(float("nan"))
        except ValueError:
            rejected = True
        return {
            "indices": bands,
            "output_colors": [list(_PALETTE[index]) for index in bands],
            "rejects_nan": rejected,
        }

    check(
        "palette-band-bounds",
        ["palette-lighting", "material-ramps"],
        {
            "indices": [0, 0, 1, 2, 2, 3, 3],
            "output_colors": [
                [16, 24, 32, 255],
                [16, 24, 32, 255],
                [64, 96, 80, 255],
                [144, 176, 112, 255],
                [144, 176, 112, 255],
                [224, 216, 144, 255],
                [224, 216, 144, 255],
            ],
            "rejects_nan": True,
        },
        palette_bands,
        "Tests an explicit four-band ramp lookup, not an engine shader, color-management path or temporal lighting quality.",
    )

    def corner_pairs():
        # These literal allowed-neighbor tables are the independent oracle,
        # enumerated from a paper drawing of TL/TR/BR/BL corner labels.
        right_oracle = [
            (0, 2, 4, 6),
            (0, 2, 4, 6),
            (1, 3, 5, 7),
            (1, 3, 5, 7),
            (8, 10, 12, 14),
            (8, 10, 12, 14),
            (9, 11, 13, 15),
            (9, 11, 13, 15),
            (0, 2, 4, 6),
            (0, 2, 4, 6),
            (1, 3, 5, 7),
            (1, 3, 5, 7),
            (8, 10, 12, 14),
            (8, 10, 12, 14),
            (9, 11, 13, 15),
            (9, 11, 13, 15),
        ]
        below_oracle = [
            (0, 4, 8, 12),
            (0, 4, 8, 12),
            (0, 4, 8, 12),
            (0, 4, 8, 12),
            (2, 6, 10, 14),
            (2, 6, 10, 14),
            (2, 6, 10, 14),
            (2, 6, 10, 14),
            (1, 5, 9, 13),
            (1, 5, 9, 13),
            (1, 5, 9, 13),
            (1, 5, 9, 13),
            (3, 7, 11, 15),
            (3, 7, 11, 15),
            (3, 7, 11, 15),
            (3, 7, 11, 15),
        ]
        totals, mismatches = [], []
        for axis, oracle in (("horizontal", right_oracle), ("vertical", below_oracle)):
            total = 0
            for a in range(16):
                for b in range(16):
                    actual = _corner_match(a, b, axis)
                    total += actual
                    if actual != (b in oracle[a]):
                        mismatches.append([axis, a, b])
            totals.append(total)
        return {
            "pairs_per_axis": 256,
            "compatible_per_axis": totals,
            "oracle_mismatches": mismatches,
            "right_of_2": [b for b in range(16) if _corner_match(2, b, "horizontal")],
            "below_8": [b for b in range(16) if _corner_match(8, b, "vertical")],
        }

    check(
        "corner-topology-pairs",
        ["terrain-topology"],
        {
            "pairs_per_axis": 256,
            "compatible_per_axis": [64, 64],
            "oracle_mismatches": [],
            "right_of_2": [1, 3, 5, 7],
            "below_8": [1, 5, 9, 13],
        },
        corner_pairs,
        "Checks binary corner-label compatibility, not visual seams, 47-tile blob completeness or provider tile ordering.",
    )

    def crop_anchor():
        image = Image.new("RGBA", (16, 16))
        for y in range(7, 12):
            for x in range(6, 10):
                image.putpixel((x, y), _PALETTE[2])
        bounds = image.getchannel("A").getbbox()
        if bounds is None:
            raise ValueError("Crop fixture has no visible pixels")
        cropped = image.crop(bounds)
        anchor = (8, 11)
        local = [anchor[0] - bounds[0], anchor[1] - bounds[1]]
        restored = Image.new("RGBA", image.size)
        restored.paste(cropped, bounds[:2])
        save_image("crop-restored.png", restored)
        return {
            "crop_size": list(cropped.size),
            "trim_offset": list(bounds[:2]),
            "local_anchor": local,
            "restored_anchor": [local[0] + bounds[0], local[1] + bounds[1]],
            "pixels_equal": restored.tobytes() == image.tobytes(),
        }

    check(
        "crop-anchor-roundtrip",
        ["crop-and-anchor"],
        {
            "crop_size": [4, 5],
            "trim_offset": [6, 7],
            "local_anchor": [2, 4],
            "restored_anchor": [8, 11],
            "pixels_equal": True,
        },
        crop_anchor,
        "Tests transparent-padding trimming, not automatic segmentation of a painted background.",
    )

    def integer_upscale():
        colors = [
            (255, 0, 0, 255),
            (0, 255, 0, 255),
            (0, 0, 255, 255),
            (255, 255, 0, 255),
        ]
        image = Image.new("RGBA", (2, 2))
        image.putdata(colors)
        scaled = image.resize((6, 6), Image.Resampling.NEAREST)
        uniform = []
        for index, (ox, oy) in enumerate(((0, 0), (3, 0), (0, 3), (3, 3))):
            uniform.append(
                all(
                    scaled.getpixel((ox + x, oy + y)) == colors[index]
                    for y in range(3)
                    for x in range(3)
                )
            )
        save_image("integer-upscale.png", scaled)
        return {
            "size": list(scaled.size),
            "uniform_blocks": uniform,
            "color_count": len(
                {scaled.getpixel((x, y)) for y in range(6) for x in range(6)}
            ),
        }

    check(
        "integer-nearest-upscale",
        ["integer-presentation"],
        {"size": [6, 6], "uniform_blocks": [True, True, True, True], "color_count": 4},
        integer_upscale,
        "Pillow output-pixel proof only; browser zoom, device pixel ratio, camera transforms and engine sampling remain untested.",
    )

    check(
        "frame-boundaries",
        ["frame-timing"],
        {"frames": ["A", "A", "B", "B", "C", "C", "A"]},
        lambda: {
            "frames": [
                _at_time([("A", 80), ("B", 40), ("C", 120)], t)
                for t in (0, 79, 80, 119, 120, 239, 240)
            ]
        },
        "Tests looping frame selection with half-open intervals, not audiovisual synchronization or action-event dispatch.",
    )

    def edge_centroids():
        frames = [(1, 0), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0, 1)]
        return {
            "masses": [sum(frame) for frame in frames],
            "centroids": [
                sum(x * value for x, value in enumerate(frame)) / sum(frame)
                for frame in frames
            ],
        }

    check(
        "edge-coverage-centroid",
        ["edge-color-migration"],
        {"masses": [1, 1, 1, 1, 1], "centroids": [0, 0.25, 0.5, 0.75, 1]},
        edge_centroids,
        "Coverage centroid is a numerical motion cue, not proof that a viewer perceives an equally spaced movement.",
    )

    def handoff():
        frames = [".##..", ".###.", "..##."]
        points = [{(x, 0) for x, c in enumerate(frame) if c == "#"} for frame in frames]
        return {
            "areas": [len(p) for p in points],
            "centroids": [sum(x for x, y in p) / len(p) for p in points],
            "components": [len(_components(p)) for p in points],
        }

    check(
        "cluster-handoff-centroid",
        ["cluster-handoff"],
        {"areas": [2, 3, 2], "centroids": [1.5, 2, 2.5], "components": [1, 1, 1]},
        handoff,
        "The temporary three-cell area is an explicit fixture allowance; rigid-feature volume and animation quality need review.",
    )

    def shading_drift():
        first = Image.new("RGBA", (8, 8))
        for y in range(1, 7):
            for x in range(1, 7):
                first.putpixel((x, y), _PALETTE[1])
        first.putpixel((2, 3), _PALETTE[3])
        first.putpixel((3, 3), _PALETTE[3])
        second = first.copy()
        second.putpixel((2, 3), _PALETTE[1])
        second.putpixel((4, 3), _PALETTE[3])
        pixels = [
            [im.getpixel((x, y)) for y in range(8) for x in range(8)]
            for im in (first, second)
        ]
        return {
            "changed_pixels": sum(a != b for a, b in zip(*pixels)),
            "same_silhouette": first.getchannel("A").tobytes()
            == second.getchannel("A").tobytes(),
            "highlight_areas": [
                sum(pixel == _PALETTE[3] for pixel in frame) for frame in pixels
            ],
        }

    check(
        "shading-drift-mask",
        ["shading-drift", "animation-anchors"],
        {"changed_pixels": 2, "same_silhouette": True, "highlight_areas": [2, 2]},
        shading_drift,
        "Proves mask preservation in this idle fixture, not a convincing breathing action or general world-space foot planting.",
    )

    def coverage_candidate():
        source = Image.new("L", (5, 5))
        source.putpixel((2, 2), 255)
        high = source.resize((20, 20), Image.Resampling.NEAREST)
        shifted = Image.new("L", (20, 20))
        shifted.paste(high, (1, 0))
        coverage = []
        for y in range(5):
            for x in range(5):
                # This image is created in L mode, so each pixel is an integer byte.
                value = (
                    sum(
                        cast(int, shifted.getpixel((x * 4 + dx, y * 4 + dy))) / 255
                        for dy in range(4)
                        for dx in range(4)
                    )
                    / 16
                )
                if value:
                    coverage.append([x, y, value])
        return {
            "nonzero_coverage": coverage,
            "total_coverage": sum(p[2] for p in coverage),
        }

    check(
        "supersampled-coverage",
        ["coverage-candidates"],
        {"nonzero_coverage": [[2, 2, 0.75], [3, 2, 0.25]], "total_coverage": 1},
        coverage_candidate,
        "Tests offline coverage construction; palette cleanup and artistic acceptance remain separate.",
    )

    def rig_pivots():
        parent = (10, 20)
        socket = _place((12, 7), parent, 90)
        a = _place((2, 3), (10, 4), 0)
        b = _place((5, 1), (7, 6), 0)
        bad = _place((5, 1), (8, 6), 0)
        world = [_place(point, parent, 90) for point in (a, b)]
        bad_world = _place(bad, parent, 90)
        return {
            "socket_world": socket,
            "attachment_world_pivots": world,
            "mutant_error": round(math.dist(socket, bad_world), 9),
        }

    check(
        "rig-pivot-hierarchy",
        ["rig-sockets", "rig-cutout"],
        {
            "socket_world": [3, 32],
            "attachment_world_pivots": [[3, 32], [3, 32]],
            "mutant_error": 1,
        },
        rig_pivots,
        "A two-level rigid coordinate proof; attachment artwork, inverse kinematics and a game-engine rig are not evaluated.",
    )

    def snap_state():
        position = 0.0
        rendered = []
        for _ in range(8):
            position += 0.25
            rendered.append(math.floor(position + 0.5))
        return {"rendered": rendered, "continuous_end": position}

    check(
        "final-snap-state",
        ["continuous-state-final-snap"],
        {"rendered": [0, 1, 1, 1, 1, 2, 2, 2], "continuous_end": 2},
        snap_state,
        "Uses nonnegative round-half-up positions; camera transforms, negative tie behavior and independent bone seams need separate fixtures.",
    )

    def quarter_turns():
        original = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)}
        current = set(original)
        first_rows = None
        for index in range(4):
            current = {(2 - y, x) for x, y in current}
            if index == 0:
                first_rows = [
                    "".join("1" if (x, y) in current else "0" for x in range(3))
                    for y in range(3)
                ]
        return {
            "first_rotation_rows": first_rows,
            "four_turns_restore": current == original,
        }

    check(
        "quarter-turn-topology",
        ["rotation-policy"],
        {"first_rotation_rows": ["111", "100", "100"], "four_turns_restore": True},
        quarter_turns,
        "Exact square-grid quarter turns only; arbitrary rotation, resampling and baked light direction remain unproven.",
    )

    def normal_orientation():
        normals = [
            _normalize(v) for v in ((1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1))
        ]
        responses = [
            [
                round(max(0, sum(a * b for a, b in zip(n, light))), 9)
                for light in normals
            ]
            for n in normals
        ]
        errors = []
        for normal in normals + [(0, 0, 1)]:
            encoded = [math.floor((value + 1) * 0.5 * 255 + 0.5) for value in normal]
            decoded = _normalize([2 * value / 255 - 1 for value in encoded])
            dot = min(1, max(-1, sum(a * b for a, b in zip(normal, decoded))))
            errors.append(math.degrees(math.acos(dot)))
        return {
            "responses": responses,
            "maximum_8bit_angular_error_deg": round(max(errors), 9),
        }

    check(
        "normal-orientation",
        ["normal-direction"],
        {
            "responses": [
                [1, 0, 0.5, 0.5],
                [0, 1, 0.5, 0.5],
                [0.5, 0.5, 1, 0],
                [0.5, 0.5, 0, 1],
            ],
            "maximum_8bit_angular_error_deg": "< 1 degree",
        },
        normal_orientation,
        "Tests the declared x-right/y-up numeric convention and 8-bit quantization; no engine import or shader normal convention is certified.",
        lambda o: (
            o["responses"]
            == [[1, 0, 0.5, 0.5], [0, 1, 0.5, 0.5], [0.5, 0.5, 1, 0], [0.5, 0.5, 0, 1]]
            and 0 <= o["maximum_8bit_angular_error_deg"] < 1
        ),
    )

    def visibility():
        def visible(segment):
            # General segment intersection for this noncollinear 2D fixture.
            def orient(a, b, c):
                return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

            light, receiver = (0, 0), (4, 0)
            a, b = segment
            crosses = (
                orient(light, receiver, a) * orient(light, receiver, b) < 0
                and orient(a, b, light) * orient(a, b, receiver) < 0
            )
            return int(not crosses)

        return {
            "visibility": [visible(((2, -1), (2, 1))), visible(((5, -1), (5, 1)))],
            "normal_term": [1, 1],
        }

    check(
        "shadow-occlusion",
        ["shadow-visibility"],
        {"visibility": [0, 1], "normal_term": [1, 1]},
        visibility,
        "A noncollinear segment-visibility fixture; soft shadows, polygon degeneracy and renderer shadow casting are not implemented.",
    )

    def authored_shading():
        diffuse = (0.2, 0.5, 0.8)
        neutral = [
            [round(d * (1 + 0 * (light - 0.5)), 9) for d in diffuse]
            for light in (0, 0.5, 1)
        ]
        low = [round(d * (1 + 0.2 * (0 - 0.5)), 9) for d in diffuse]
        high = [round(d * (1 + 0.2 * (1 - 0.5)), 9) for d in diffuse]
        return {
            "zero_strength": neutral,
            "low_modulation": low,
            "high_modulation": high,
        }

    check(
        "authored-shade-baseline",
        ["preserve-authored-shading"],
        {
            "zero_strength": [[0.2, 0.5, 0.8], [0.2, 0.5, 0.8], [0.2, 0.5, 0.8]],
            "low_modulation": [0.18, 0.45, 0.72],
            "high_modulation": [0.22, 0.55, 0.88],
        },
        authored_shading,
        "Illustrative linear scalar modulation only; preventing artistic double shading still needs rendered comparisons.",
    )

    check(
        "material-channel-isolation",
        ["material-channel-budget"],
        {"outputs": [0.2, 0.6, 0.1, 0.5]},
        lambda: {
            "outputs": [
                round(0.5 * (0.2 + mask * 0.8) + emission, 9)
                for emission in (0.1, 0)
                for mask in (0, 1)
            ]
        },
        "The formula is a reference fixture, not a platform material implementation or a validated 2.5D height pipeline.",
    )

    def cluster_connectivity():
        points = {(1, 1), (1, 2), (2, 1), (2, 2), (5, 1), (6, 2), (1, 6)}
        return {
            "four_neighbor_sizes": sorted(map(len, _components(points))),
            "eight_neighbor_sizes": sorted(map(len, _components(points, True))),
        }

    check(
        "cluster-connectivity",
        ["semantic-clusters"],
        {"four_neighbor_sizes": [1, 1, 1, 4], "eight_neighbor_sizes": [1, 2, 4]},
        cluster_connectivity,
        "Connectivity does not establish semantic importance; no singleton is automatically removed.",
    )

    def cell_simulation():
        states, moves = _sand(1729)
        replay, replay_moves = _sand(1729)
        max_moves = max(
            (
                max(Counter(move[0] for move in tick).values(), default=0)
                for tick in moves
            ),
            default=0,
        )
        bounded = all(
            max(abs(nx - x), abs(ny - y)) <= 1
            for tick in moves
            for _, x, y, nx, ny in tick
        )
        counts = [len(state) for state in states]
        identities = all(set(state.values()) == {1, 2, 3} for state in states)
        return {
            "first_tick": sorted(
                [particle, x, y] for (x, y), particle in states[1].items()
            ),
            "particle_counts": counts,
            "maximum_moves_per_id_per_tick": max_moves,
            "same_seed_same_states": states == replay and moves == replay_moves,
            "displacement_bound_holds": bounded,
            "identities_preserved": identities,
        }

    check(
        "cell-conservation-determinism",
        ["deterministic-cell-update", "cell-materials"],
        {
            "first_tick": [[1, 3, 2], [2, 3, 3], [3, 4, 2]],
            "particle_counts": [3] * 21,
            "maximum_moves_per_id_per_tick": 1,
            "same_seed_same_states": True,
            "displacement_bound_holds": True,
            "identities_preserved": True,
        },
        cell_simulation,
        "Three powder entities, one floor, one-cell movement and 20 serial ticks. Does not establish full fluid behavior, cross-chunk concurrency or Noita equivalence.",
    )

    def destruction():
        points = {(x, y) for y in range(3) for x in (0, 1, 2, 4, 5, 6)} | {(3, 1)}
        before = _components(points)
        points.remove((3, 1))
        after = _components(points)
        union = set().union(*after)
        overlap = sum(map(len, after)) - len(union)
        return {
            "before_sizes": sorted(map(len, before)),
            "after_sizes": sorted(map(len, after)),
            "union_size": len(union),
            "overlap_size": overlap,
        }

    check(
        "destruction-components",
        ["destruction-topology"],
        {
            "before_sizes": [19],
            "after_sizes": [9, 9],
            "union_size": 18,
            "overlap_size": 0,
        },
        destruction,
        "Proves occupancy partition after one bridge removal. Contours, simplification, mass properties and rigid-body solver integration are not implemented.",
    )

    def phased_regions():
        boxes = [(-1, -1, 9, 9), (7, -1, 17, 9), (15, -1, 25, 9)]
        conflicts = []
        for i in range(3):
            for j in range(i + 1, 3):
                a, b = boxes[i], boxes[j]
                if max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(
                    a[3], b[3]
                ):
                    conflicts.append([i, j])
        return {"conflicting_pairs": conflicts}

    check(
        "phase-write-domains",
        ["phased-write-ownership"],
        {"conflicting_pairs": [[0, 1], [1, 2]]},
        phased_regions,
        "Proves three declared half-open rectangle intersections, not that an actual simulation respects those write bounds.",
    )

    def sheet_roundtrip():
        sheet = Image.new("RGBA", (9, 9))
        frames = [Image.new("RGBA", (3, 3), color) for color in _PALETTE]
        origins = [(1, 1), (5, 1), (1, 5), (5, 5)]
        for frame, origin in zip(frames, origins):
            sheet.paste(frame, origin)
        extracted = [sheet.crop((x, y, x + 3, y + 3)) for x, y in origins]
        bad = sheet.crop((4, 1, 7, 4))
        return {
            "roundtrip_matches": [
                a.tobytes() == b.tobytes() for a, b in zip(frames, extracted)
            ],
            "wrong_spacing_detected": bad.tobytes() != frames[1].tobytes(),
        }

    check(
        "sheet-offset-spacing",
        ["sheet-metadata"],
        {"roundtrip_matches": [True, True, True, True], "wrong_spacing_detected": True},
        sheet_roundtrip,
        "Fixed-grid RGBA extraction only; packed-atlas rotations and importer metadata need project-specific validation.",
    )

    def representation_domains():
        def owners(behavior):
            result = []
            for trait, owner in (
                ("independent_matter", "cell"),
                ("rigid_motion", "attachment"),
                ("pose_topology", "frame"),
                ("fractional_feature", "cluster"),
                ("surface_direction", "surface-channel"),
                ("blocks_light", "occlusion"),
            ):
                if behavior.get(trait, False):
                    result.append(owner)
            return result

        fixtures = [
            {"independent_matter": True},
            {"rigid_motion": True},
            {"pose_topology": True},
            {"fractional_feature": True},
            {"surface_direction": True},
            {"blocks_light": True},
        ]
        return {
            "owners": [owners(fixture) for fixture in fixtures],
            "normal_and_shadow": owners(
                {"surface_direction": True, "blocks_light": True}
            ),
            "normal_alone_satisfies_shadow": "occlusion"
            in owners({"surface_direction": True}),
        }

    check(
        "representation-domain-classification",
        ["representation-owner"],
        {
            "owners": [
                ["cell"],
                ["attachment"],
                ["frame"],
                ["cluster"],
                ["surface-channel"],
                ["occlusion"],
            ],
            "normal_and_shadow": ["surface-channel", "occlusion"],
            "normal_alone_satisfies_shadow": False,
        },
        representation_domains,
        "Checks explicit behavior-tag classification and independent ownership domains; it does not evaluate an LLM interpreting an ambiguous brief.",
    )

    def key_silhouette():
        ring = {
            (x, y)
            for y in range(4, 9)
            for x in range(2, 7)
            if x in (2, 6) or y in (4, 8)
        }
        shaft = {(x, y) for x in range(6, 14) for y in (6, 7)}
        teeth = {(x, y) for x in (10, 13) for y in range(8, 11)}
        positive = ring | shaft | teeth
        negative = (
            positive
            | {(x, y) for y in range(5, 8) for x in range(3, 6)}
            | {(x, y) for x in (11, 12) for y in range(8, 11)}
        )
        images = []
        for name, points in (("positive", positive), ("negative", negative)):
            image = Image.new("RGBA", (16, 16))
            for point in points:
                image.putpixel(point, (230, 180, 70, 255))
            save_image(f"key-{name}.png", image)
            images.append(image)
        sheet = Image.new("RGBA", (288, 176), (55, 57, 62, 255))
        for row, image in enumerate(images):
            for column in range(4):
                background = Image.new(
                    "RGBA",
                    (16, 16),
                    (20, 23, 30, 255) if column in (0, 1) else (235, 235, 225, 255),
                )
                if column == 3:
                    for y in range(16):
                        for x in range(16):
                            background.putpixel(
                                (x, y),
                                (115, 125, 130, 255)
                                if (x // 2 + y // 2) % 2
                                else (180, 170, 155, 255),
                            )
                foreground = image.copy()
                if column == 0:
                    for y in range(16):
                        for x in range(16):
                            if cast(tuple[int, int, int, int], foreground.getpixel((x, y)))[3]:
                                foreground.putpixel((x, y), (255, 255, 255, 255))
                composed = Image.alpha_composite(background, foreground)
                sheet.paste(composed, (column * 72 + 4, row * 88 + 4))
                sheet.paste(
                    composed.resize((64, 64), Image.Resampling.NEAREST),
                    (column * 72 + 4, row * 88 + 24),
                )
        save_image("key-contact-sheet.png", sheet)
        return {
            "positive": _key_landmarks(positive),
            "negative": _key_landmarks(negative),
        }

    check(
        "key-silhouette-landmarks",
        ["silhouette-readability"],
        {
            "positive": {"hole": True, "shaft": True, "teeth": 2},
            "negative": {"hole": False, "shaft": True, "teeth": 1},
        },
        key_silhouette,
        "Checks specified geometric landmarks and generates native/4x views. Visual recognition, background readability and final artistic acceptance require inspection; no such judgment is inferred from the counts.",
    )

    def edge_rhythm():
        def deviations(points):
            ordered = sorted(points, key=lambda p: p[1])
            return [
                list(b)
                for a, b in pairwise(ordered)
                if (b[0] - a[0], b[1] - a[1]) != (1, 1)
            ]

        baseline = {(i, i) for i in range(8)}
        detour = baseline - {(4, 4)} | {(5, 4)}
        reported = deviations(detour)
        intentional = {(5, 4), (5, 5)}
        return {
            "baseline_deviations": deviations(baseline),
            "detour_deviations": reported,
            "accidental_correction_candidates": [p for p in reported],
            "intentional_correction_candidates": [
                p for p in reported if tuple(p) not in intentional
            ],
        }

    check(
        "edge-rhythm-detour",
        ["edge-rhythm"],
        {
            "baseline_deviations": [],
            "detour_deviations": [[5, 4], [5, 5]],
            "accidental_correction_candidates": [[5, 4], [5, 5]],
            "intentional_correction_candidates": [],
        },
        edge_rhythm,
        "Tests an explicitly declared unit-step diagonal. Real curved or organic contours are not required to follow this pattern, and the fixture never auto-smooths artwork.",
    )

    def selective_aa():
        source = Image.new("RGBA", (5, 5), _PALETTE[0])
        for i in range(5):
            source.putpixel((i, i), _PALETTE[3])
        allowed = {(1, 0), (2, 1)}
        valid = source.copy()
        for point in allowed:
            valid.putpixel(point, _PALETTE[1])
        mutant = valid.copy()
        mutant.putpixel((2, 2), _PALETTE[1])

        def changes(image):
            return [
                (x, y)
                for y in range(5)
                for x in range(5)
                if image.getpixel((x, y)) != source.getpixel((x, y))
            ]

        return {
            "valid_changes": [list(p) for p in changes(valid)],
            "valid_forbidden_changes": [
                list(p) for p in changes(valid) if p not in allowed
            ],
            "mutant_forbidden_changes": [
                list(p) for p in changes(mutant) if p not in allowed
            ],
            "palette_violations": _palette_violations(valid),
        }

    check(
        "selective-aa-boundary",
        ["selective-edge-aa"],
        {
            "valid_changes": [[1, 0], [2, 1]],
            "valid_forbidden_changes": [],
            "mutant_forbidden_changes": [[2, 2]],
            "palette_violations": [],
        },
        selective_aa,
        "Proves edit locality and approved colors, not perceptual antialiasing quality or suitability against arbitrary backgrounds.",
    )

    def tile_repeat():
        tile = Image.new("RGBA", (8, 8), _PALETTE[0])
        for y in range(1, 7):
            for x in range(1, 7):
                tile.putpixel((x, y), _PALETTE[1])
        for y in (3, 4):
            for x in (3, 4):
                tile.putpixel((x, y), _PALETTE[2])
        neighborhood = Image.new("RGBA", (24, 24))
        for y in range(3):
            for x in range(3):
                neighborhood.paste(tile, (x * 8, y * 8))
        save_image("tile-repeat-neighborhood.png", neighborhood)
        mutant = tile.copy()
        mutant.putpixel((7, 3), _PALETTE[3])
        return {
            "original_mismatches": _border_mismatches(tile),
            "mutant_mismatches": _border_mismatches(mutant),
            "neighborhood_size": list(neighborhood.size),
        }

    check(
        "tile-repeat-neighborhood",
        ["tile-repeat"],
        {
            "original_mismatches": [],
            "mutant_mismatches": [["horizontal", 3]],
            "neighborhood_size": [24, 24],
        },
        tile_repeat,
        "Validates the fixture's exact-border contract and creates a 3x3 image. Matching bytes do not establish invisible repetition or universally seamless texture design.",
    )

    def tile_variants():
        variants = []
        for index in range(3):
            image = Image.new("RGBA", (8, 8), _PALETTE[0])
            for y in (3, 4):
                for x in (index + 1, index + 2):
                    image.putpixel((x, y), _PALETTE[index + 1])
            variants.append(image)

        def select(seed):
            # Tiny, fully enumerable LCG: reproducibility fixture only, not a
            # recommended production noise generator or distribution claim.
            state = seed
            selected = []
            for _ in range(64):
                state = (5 * state + 1) % 16
                selected.append(state % 3)
            return selected

        sequence = select(1)
        literal_cycle = [0, 0, 0, 1, 2, 2, 2, 0, 2, 1, 1, 2, 1, 0, 0, 1]
        mutant = variants[0].copy()
        mutant.putpixel((7, 3), _PALETTE[3])
        return {
            "first_cycle": sequence[:16],
            "selection_count": len(sequence),
            "four_literal_cycles": sequence == literal_cycle * 4,
            "repeatable": sequence == select(1),
            "valid_variant_mismatches": [
                len(_border_mismatches(tile)) for tile in variants
            ],
            "mutant_mismatch_count": len(_border_mismatches(mutant)),
        }

    check(
        "seeded-tile-variants",
        ["tile-variants"],
        {
            "first_cycle": [0, 0, 0, 1, 2, 2, 2, 0, 2, 1, 1, 2, 1, 0, 0, 1],
            "selection_count": 64,
            "four_literal_cycles": True,
            "repeatable": True,
            "valid_variant_mismatches": [0, 0, 0],
            "mutant_mismatch_count": 1,
        },
        tile_variants,
        "Tests seeded selection and fixed borders with an intentionally tiny period-16 PRNG; no production randomness, visual-variety or directional-lighting claim.",
    )

    def provenance_manifest():
        entries: list[dict[str, str | None]] = [
            {
                "id": "folder-original",
                "origin": "original",
                "creator": "PIXL fixture",
                "reuse_basis": "original-authorship",
            },
            {
                "id": "npc-reference",
                "origin": "external",
                "creator": "Dusan Cezek",
                "source": "PIXEL-ART-ASSETS.md:971",
                "reuse_basis": None,
            },
        ]
        originals = [
            item["id"]
            for item in entries
            if item["origin"] == "original" and item.get("creator")
        ]
        unresolved = [
            item["id"]
            for item in entries
            if item["origin"] == "external" and not item.get("reuse_basis")
        ]
        return {
            "declared_original_assets": originals,
            "unresolved_reuse_assets": unresolved,
            "release_manifest_complete": not unresolved,
        }

    check(
        "provenance-manifest",
        ["asset-provenance"],
        {
            "declared_original_assets": ["folder-original"],
            "unresolved_reuse_assets": ["npc-reference"],
            "release_manifest_complete": False,
        },
        provenance_manifest,
        "A metadata completeness check only. It neither verifies a creator claim nor determines copyright, licensing or legal permission; no referenced external asset is copied or redistributed.",
    )

    def alpha_contract():
        foreground, background, alpha = (255, 0, 0), (0, 0, 255), 0.5
        premultiplied = [channel * alpha for channel in foreground]
        return {
            "straight_result": [
                f * alpha + b * (1 - alpha) for f, b in zip(foreground, background)
            ],
            "premultiplied_result": [
                f + b * (1 - alpha) for f, b in zip(premultiplied, background)
            ],
            "double_multiplied_mutant": [
                f * alpha + b * (1 - alpha) for f, b in zip(premultiplied, background)
            ],
            "binary_alpha_violations": [
                i for i, value in enumerate([0, 255, 127]) if value not in (0, 255)
            ],
        }

    check(
        "alpha-compositing-contract",
        ["alpha-contract"],
        {
            "straight_result": [127.5, 0, 127.5],
            "premultiplied_result": [127.5, 0, 127.5],
            "double_multiplied_mutant": [63.75, 0, 127.5],
            "binary_alpha_violations": [2],
        },
        alpha_contract,
        "Linear numeric compositing and alpha-policy fixture only; no display transfer function, GPU blend state or importer is evaluated.",
    )

    def composed_channels():
        tread, recoil, armor = [], [], []
        recoil_curve = [0, -2, -1, 0]
        damage = "normal"
        for tick in range(8):
            tread.append(tick % 4)
            elapsed = tick - 3
            recoil.append(
                recoil_curve[elapsed] if 0 <= elapsed < len(recoil_curve) else 0
            )
            if tick == 5:
                damage = "damaged"
            armor.append(damage)
        return {"tread_indices": tread, "recoil_offsets": recoil, "armor_states": armor}

    check(
        "independent-animation-channels",
        ["composed-animation"],
        {
            "tread_indices": [0, 1, 2, 3, 0, 1, 2, 3],
            "recoil_offsets": [0, 0, 0, 0, -2, -1, 0, 0],
            "armor_states": [
                "normal",
                "normal",
                "normal",
                "normal",
                "normal",
                "damaged",
                "damaged",
                "damaged",
            ],
        },
        composed_channels,
        "Tests three explicitly owned channels and event times; contacts, transform blending and target-engine animation composition remain separate.",
    )

    check(
        "atlas-raw-storage-budget",
        ["atlas-reuse-budget"],
        {"baked_rgba8_bytes": 60000000, "modular_rgba8_bytes": 2621440},
        lambda: {
            "baked_rgba8_bytes": 60 * 500 * 500 * 4,
            "modular_rgba8_bytes": 20 * 64 * 64 * 8 * 4,
        },
        "Uncompressed RGBA8 arithmetic only, excluding padding, compression, mipmaps and metadata. Does not measure GPU resident memory, draw calls, frame time or target-device performance.",
    )

    def companion_alignment():
        diffuse = Image.new("RGBA", (8, 8), _PALETTE[0])
        diffuse.putpixel((2, 5), _PALETTE[3])
        normal = Image.new("RGB", (8, 8), (128, 128, 255))
        normal.putpixel((2, 5), (218, 128, 218))
        shifted = Image.new("RGB", (8, 8), (128, 128, 255))
        shifted.putpixel((3, 5), (218, 128, 218))

        def feature(image, color):
            return {
                (x, y)
                for y in range(8)
                for x in range(8)
                if image.getpixel((x, y)) == color
            }

        diffuse_feature = feature(diffuse, _PALETTE[3])
        return {
            "matching_dimensions": diffuse.size == normal.size,
            "aligned_feature_mismatches": [
                list(p)
                for p in sorted(diffuse_feature ^ feature(normal, (218, 128, 218)))
            ],
            "mutant_dimensions_match": diffuse.size == shifted.size,
            "mutant_feature_mismatches": [
                list(p)
                for p in sorted(diffuse_feature ^ feature(shifted, (218, 128, 218)))
            ],
        }

    check(
        "companion-pixel-alignment",
        ["companion-alignment"],
        {
            "matching_dimensions": True,
            "aligned_feature_mismatches": [],
            "mutant_dimensions_match": True,
            "mutant_feature_mismatches": [[2, 5], [3, 5]],
        },
        companion_alignment,
        "Tests calibration-feature correspondence despite equal dimensions. UV remapping, atlas padding and an engine import path are not evaluated.",
    )

    def dirty_region_parity():
        full, dirty = _region_world(False), _region_world(True)
        return {
            "positions": [list(p) for p in dirty["positions"]],
            "states_match_each_tick": full["positions"] == dirty["positions"],
            "first_wakeup_chunks": dirty["wakes"][0],
            "final_active_chunks": dirty["wakes"][-1],
            "full_cell_visits": full["visits"],
            "dirty_cell_visits": dirty["visits"],
        }

    check(
        "dirty-region-boundary-parity",
        ["dirty-region-wakeup"],
        {
            "positions": [
                [7, 1],
                [8, 2],
                [8, 3],
                [8, 4],
                [8, 5],
                [8, 6],
                [8, 6],
                [8, 6],
                [8, 6],
            ],
            "states_match_each_tick": True,
            "first_wakeup_chunks": [0, 1],
            "final_active_chunks": [],
            "full_cell_visits": 1024,
            "dirty_cell_visits": 704,
        },
        dirty_region_parity,
        "One particle crossing two 8x8 chunks with a one-cell halo and eight serial ticks. Cell-visit reduction is not measured speedup; thermal influence, arbitrary write radii and parallel simulation need separate checks.",
    )

    def reaction_table():
        known = {"water", "steam"}
        rule = {
            "reactant": "water",
            "output": "steam",
            "threshold": 100,
            "probability": 1.0,
        }

        def apply(temperature, reaction):
            if not 0 <= reaction["probability"] <= 1:
                raise ValueError("Probability outside [0,1]")
            if reaction["reactant"] not in known or reaction["output"] not in known:
                raise ValueError("Unknown material")
            return (
                reaction["output"]
                if temperature >= reaction["threshold"] and reaction["probability"] == 1
                else reaction["reactant"]
            )

        outputs = [apply(temperature, rule) for temperature in (99, 100, 101)]
        rejected = []
        for changes in ({"probability": 1.2}, {"output": "unknown"}):
            try:
                apply(101, {**rule, **changes})
                rejected.append(False)
            except ValueError:
                rejected.append(True)
        return {
            "outputs": outputs,
            "occupied_cells": len(outputs),
            "invalid_probability_rejected": rejected[0],
            "unknown_material_rejected": rejected[1],
        }

    check(
        "reaction-threshold-table",
        ["reaction-tables"],
        {
            "outputs": ["water", "steam", "steam"],
            "occupied_cells": 3,
            "invalid_probability_rejected": True,
            "unknown_material_rejected": True,
        },
        reaction_table,
        "Deterministic probability-one replacement and schema guards only; intermediate stochastic probabilities, multi-reactant conflicts and physical thermodynamics are not simulated.",
    )

    def pipeline_dependencies():
        dependencies = [
            ("animation", "snap"),
            ("snap", "light"),
            ("light", "upscale"),
            ("cells", "components"),
            ("components", "physics"),
        ]

        def violations(order):
            position = {stage: index for index, stage in enumerate(order)}
            if len(position) != len(order) or any(
                a not in position or b not in position for a, b in dependencies
            ):
                raise ValueError("Missing or duplicate pipeline stage")
            return [f"{a}->{b}" for a, b in dependencies if position[a] >= position[b]]

        valid = [
            "cells",
            "components",
            "physics",
            "animation",
            "snap",
            "light",
            "upscale",
        ]
        mutant = [
            "cells",
            "components",
            "physics",
            "animation",
            "snap",
            "upscale",
            "light",
        ]
        return {
            "valid_violations": violations(valid),
            "mutant_violations": violations(mutant),
        }

    check(
        "pipeline-dependency-order",
        ["pipeline-order"],
        {"valid_violations": [], "mutant_violations": ["light->upscale"]},
        pipeline_dependencies,
        "Checks an explicit reference dependency graph. It does not establish that any stage actually executed in an external engine or that its data ownership is race-free.",
    )

    def input_pixel_ui():
        idle = {
            (x, y)
            for y in range(1, 7)
            for x in range(1, 7)
            if x in (1, 6) or y in (1, 6)
        }
        pressed = {(x, y + 1) for x, y in idle}
        disabled = {(i, i) for i in range(8)} | {(7 - i, i) for i in range(8)}
        masks = {"idle": idle, "pressed": pressed, "disabled": disabled}
        sheet = Image.new("RGBA", (24, 8))
        for index, name in enumerate(("idle", "pressed", "disabled")):
            for x, y in masks[name]:
                sheet.putpixel(
                    (index * 8 + x, y),
                    _PALETTE[3] if name != "disabled" else _PALETTE[1],
                )
        save_image("pixel-ui-states.png", sheet)
        enabled, held = False, False
        states = []
        for event in ("enabled", "down", "up", "disabled", "down"):
            if event == "enabled":
                enabled = True
            elif event == "disabled":
                enabled, held = False, False
            elif event == "down" and enabled:
                held = True
            elif event == "up":
                held = False
            states.append("disabled" if not enabled else "pressed" if held else "idle")
        return {
            "states": states,
            "distinct_state_masks": len({frozenset(mask) for mask in masks.values()}),
        }

    check(
        "input-driven-pixel-ui",
        ["state-driven-pixel-ui"],
        {
            "states": ["idle", "pressed", "idle", "disabled", "disabled"],
            "distinct_state_masks": 3,
        },
        input_pixel_ui,
        "Tests supplied input-state transitions and distinct original masks. Does not inspect accessibility, overall UI aesthetics, input hardware or an application event loop.",
    )

    _assert_runner_source_unchanged()
    report = {
        "version": 1,
        "observed_at": datetime.now(UTC).isoformat(),
        "status": "pass"
        if all(item["status"] == "pass" for item in checks)
        else "fail",
        "scope": "offline_reference_fixtures",
        "implementation_sha256": _IMPORTED_SOURCE_SHA256,
        "knowledge_sha256": knowledge_hash,
        "source_sha256": source_hashes,
        "pillow_version": pillow_version,
        "checks": checks,
        "artifacts": artifacts,
        "limitations": [
            "No live PixelLab calls were made.",
            "A passing reference fixture is not a provider capability, engine integration or visual-quality certification.",
            "Every current knowledge method has a bounded reference check; project-specific, provider and visual-quality acceptance remain separate.",
        ],
    }
    (output / "poc-report.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return report
