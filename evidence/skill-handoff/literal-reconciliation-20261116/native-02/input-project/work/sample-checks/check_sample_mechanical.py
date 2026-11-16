"""Local mechanical check harness for the two local-mode sample criteria (2026-11-15d).

Checks ONE PNG against the literal text of q_sample_canvas and q_sample_palette as saved in
revision 9 of state.px/state.px (record hashes below). It measures; it does not judge art,
does not create X/E/V records, and its output is tooling output, not acceptance evidence.
A candidate still needs the visual criteria (q_sample_outline, q_sample_readability,
q_style_match) reviewed through pixl_inspection_prepare / pixl_inspection_review.

The pass/fail reading follows the saved wording exactly:
  q_sample_canvas  : width == 32 and height == 32, and zero pixels with 0 < alpha < 255.
  q_sample_palette : every pixel with alpha > 0 has RGB in {#56B5BC, #F4DDA2, #25354A}.
Frame count is reported as an additional measurement only; the saved criteria do not
mention it, so it does not enter either pass/fail reading.

Usage (from the consumer root, selected interpreter, isolated mode):
  python -I work/sample-checks/check_sample_mechanical.py PATH.png [--out RESULT.json]

Exit status: 0 when both checks pass, 1 when either fails, 2 when the file cannot be read.
Only Pillow is required. "Visible pixel" means alpha > 0 after conversion to RGBA.
"""
import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime

from PIL import Image

CONTRACT = {
    "record": "c_sample",
    "record_sha256": "b7f77964257f1bfdbf54ef0dcadc76117e0a3437f40daae1268210ae07147737",
    "state_hash": "fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1",
    "px": [32, 32],
    "pl": ["#56B5BC", "#F4DDA2", "#25354A"],
    "al": "binary",
}

CRITERIA = {
    "q_sample_canvas": {
        "record_sha256": "09be7cbaef447bdfe54a2d77c09693000209cd3fa4c5954a067d471e91eaabd8",
        "domain": "mechanical",
        "mode": "local",
        "check": (
            "The candidate file is exactly 32 x 32 pixels, the canvas of the sample contract "
            "c_sample, and contains zero fractional-alpha pixels under that contract's binary "
            "alpha. Scope: the representative sample only; the canvas is a sample-scoped "
            "controlled-evaluation confirmation and the alpha policy an observation from the "
            "references, neither a confirmed project policy."
        ),
    },
    "q_sample_palette": {
        "record_sha256": "0563ebde9637408c1d14d43d1a2c2aa65abdb3110fa4ed0200373f70b6a40589",
        "domain": "mechanical",
        "mode": "local",
        "check": (
            "Every visible pixel of the candidate is one of the three colours of the sample "
            "contract c_sample palette, #56B5BC, #F4DDA2 and #25354A, with no colours outside "
            "it. Scope: the representative sample only; these are the colours measured in the "
            "references, all three admitted by the sample-scoped outlined-treatment "
            "confirmation, and exclusivity is a sample working rule that a later role accent "
            "may reopen; this is not a confirmed project palette."
        ),
    },
}


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def measure(path):
    with open(path, "rb") as handle:
        data = handle.read()
    image = Image.open(path)
    frames = getattr(image, "n_frames", 1)
    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = rgba.load()
    fractional = 0
    visible = 0
    colours = {}
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            visible += 1
            if a != 255:
                fractional += 1
            colours[(r, g, b)] = colours.get((r, g, b), 0) + 1
    return {
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "format": image.format,
        "source_mode": image.mode,
        "frame_count": frames,
        "width": width,
        "height": height,
        "visible_pixels": visible,
        "fractional_alpha_pixels": fractional,
        "visible_colours": sorted(
            ("#%02X%02X%02X" % rgb, count) for rgb, count in colours.items()
        ),
    }


def evaluate(m):
    palette = {hex_rgb(c) for c in CONTRACT["pl"]}
    outside = [
        {"colour": colour, "pixels": count}
        for colour, count in m["visible_colours"]
        if hex_rgb(colour) not in palette
    ]
    size_ok = [m["width"], m["height"]] == CONTRACT["px"]
    alpha_ok = m["fractional_alpha_pixels"] == 0
    canvas_pass = size_ok and alpha_ok
    palette_pass = not outside
    return {
        "q_sample_canvas": {
            **CRITERIA["q_sample_canvas"],
            "result": "pass" if canvas_pass else "fail",
            "measurements": {
                "size": [m["width"], m["height"]],
                "size_expected": CONTRACT["px"],
                "size_matches": size_ok,
                "fractional_alpha_pixels": m["fractional_alpha_pixels"],
            },
        },
        "q_sample_palette": {
            **CRITERIA["q_sample_palette"],
            "result": "pass" if palette_pass else "fail",
            "measurements": {
                "palette_expected": CONTRACT["pl"],
                "visible_colours": m["visible_colours"],
                "outside_palette": outside,
                "outside_palette_pixels": sum(o["pixels"] for o in outside),
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("png")
    parser.add_argument("--out", help="write the JSON result to this path as well")
    args = parser.parse_args()
    try:
        m = measure(args.png)
    except Exception as error:  # unreadable file is a tooling failure, not a verdict
        report = {"path": args.png, "error": f"{type(error).__name__}: {error}"}
        print(json.dumps(report, indent=1))
        return 2
    results = evaluate(m)
    report = {
        "harness": "work/sample-checks/check_sample_mechanical.py",
        "measured_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "status_meaning": (
            "Measurement only. 'pass'/'fail' here is the harness's reading of the literal "
            "mechanical condition; it is not a V verdict, not E evidence and not acceptance. "
            "Visual criteria are outside this harness."
        ),
        "contract": CONTRACT,
        "file": m,
        "criteria": results,
        "additional_measurements_not_in_any_saved_criterion": {
            "frame_count": m["frame_count"],
            "note": "f_sample plans a single static sprite; a multi-frame file would be a "
                    "cardinality question for import, not a q_sample_canvas failure.",
        },
        "all_local_checks_pass": all(r["result"] == "pass" for r in results.values()),
    }
    text = json.dumps(report, indent=1)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
    return 0 if report["all_local_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
