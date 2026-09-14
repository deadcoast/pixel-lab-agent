"""Check an RGBA sprite against the project's translucent-treatment contract.

The contract is the machine-readable half of the style rules derived from
translucent-reference.png: which RGB values are allowed, which of them may
carry fractional alpha, and which alpha levels exist. Everything this script
reports is a measurement. Silhouette quality, glow believability and engine
behaviour are not checked here.

Usage:
    python tools/alpha_treatment_check.py CONTRACT.json IMAGE.png [IMAGE.png ...]

Exit code 0 when every image satisfies the contract, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from PIL import Image


def parse_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    if len(text) != 6:
        raise ValueError(f"expected #rrggbb, got {value!r}")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def neighbors(x: int, y: int):
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


def check(contract: dict, path: Path) -> dict:
    image = Image.open(path).convert("RGBA")
    width, height = image.size
    pixels = image.load()

    roles = contract["roles"]
    rgb_role = {}
    translucent_rgb = set()
    for name, spec in roles.items():
        for entry in spec["rgb"]:
            rgb_role[parse_rgb(entry)] = name
        if spec.get("translucent"):
            translucent_rgb.update(parse_rgb(entry) for entry in spec["rgb"])
    allowed_alpha = set(contract["alpha_levels"])

    failures: list[str] = []
    alpha_hist: Counter[int] = Counter()
    role_hist: Counter[str] = Counter()
    fringe: list[tuple[int, int]] = []
    opaque: set[tuple[int, int]] = set()
    visible: set[tuple[int, int]] = set()

    expected = tuple(contract.get("size", (width, height)))
    if (width, height) != expected:
        failures.append(f"size {width}x{height} != contract {expected[0]}x{expected[1]}")

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            alpha_hist[a] += 1
            if a == 0:
                if contract.get("clear_rgb_must_be_zero", True) and (r, g, b) != (0, 0, 0):
                    failures.append(f"({x},{y}) transparent pixel carries RGB {(r, g, b)}")
                continue
            visible.add((x, y))
            if a not in allowed_alpha:
                failures.append(f"({x},{y}) alpha {a} outside declared levels {sorted(allowed_alpha)}")
            role = rgb_role.get((r, g, b))
            if role is None:
                failures.append(f"({x},{y}) RGB #{r:02x}{g:02x}{b:02x} outside contract palette")
                continue
            role_hist[role] += 1
            if a == 255:
                opaque.add((x, y))
            else:
                fringe.append((x, y))
                if (r, g, b) not in translucent_rgb:
                    failures.append(
                        f"({x},{y}) role '{role}' carries fractional alpha {a}; "
                        "only translucent roles may"
                    )

    # The opaque body must read as one shape, and every partial pixel must touch it.
    if opaque:
        stack = [next(iter(opaque))]
        seen = {stack[0]}
        while stack:
            cx, cy = stack.pop()
            for nx, ny in neighbors(cx, cy):
                if (nx, ny) in opaque and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        if contract.get("single_opaque_body", True) and len(seen) != len(opaque):
            failures.append(
                f"opaque body splits into more than one 4-connected component "
                f"({len(seen)} of {len(opaque)} reachable)"
            )
    if contract.get("fringe_touches_body", True):
        for x, y in fringe:
            if not any((nx, ny) in opaque for nx, ny in neighbors(x, y)):
                failures.append(f"({x},{y}) partial-alpha pixel is not adjacent to the opaque body")

    fraction = len(fringe) / len(visible) if visible else 0.0
    limit = contract.get("max_fractional_share")
    if limit is not None and fraction > limit:
        failures.append(f"fractional-alpha share {fraction:.3f} exceeds limit {limit}")

    return {
        "path": str(path),
        "pass": not failures,
        "size": [width, height],
        "visible_pixels": len(visible),
        "opaque_pixels": len(opaque),
        "fractional_pixels": len(fringe),
        "fractional_share": round(fraction, 4),
        "alpha_histogram": {str(k): v for k, v in sorted(alpha_hist.items())},
        "role_pixels": dict(sorted(role_hist.items())),
        "failures": failures,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    contract = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    results = [check(contract, Path(p)) for p in argv[2:]]
    report = {
        "contract": argv[1],
        "contract_name": contract.get("name"),
        "pass": all(r["pass"] for r in results),
        "results": results,
        "notes": "Mechanical contract measurement only; no visual or engine judgement.",
    }
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
