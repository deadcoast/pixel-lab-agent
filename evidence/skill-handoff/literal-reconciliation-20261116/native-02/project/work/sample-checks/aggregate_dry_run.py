"""Aggregate the harness dry-run outputs into work/sample-checks/dry-run.json (2026-11-15d).

Reads the five run-*.json files written by check_sample_mechanical.py --out and checks that
the harness discriminated as intended. Tooling output only: no X/E/V, no verdict.

Usage (consumer root, selected interpreter):  python -I work/sample-checks/aggregate_dry_run.py
"""
import json

RUNS = {
    "reference.png": ("run-reference.json", "pass", "pass"),
    "reference-b.png": ("run-reference-b.json", "pass", "pass"),
    "work/sample-checks/fixture-33x33.png": ("run-fixture-33x33.json", "fail", "pass"),
    "work/sample-checks/fixture-offpalette.png": ("run-fixture-offpalette.json", "pass", "fail"),
    "work/sample-checks/fixture-fractional-alpha.png": ("run-fixture-fractional-alpha.json", "fail", "pass"),
}
DIR = "work/sample-checks/"


def main():
    runs, ok = {}, True
    for target, (name, want_canvas, want_palette) in RUNS.items():
        d = json.load(open(DIR + name, encoding="utf-8"))
        canvas = d["criteria"]["q_sample_canvas"]["result"]
        palette = d["criteria"]["q_sample_palette"]["result"]
        matched = canvas == want_canvas and palette == want_palette
        ok = ok and matched and d["file"]["path"] == target
        runs[DIR + name] = {
            "file": d["file"]["path"], "sha256": d["file"]["sha256"],
            "size": [d["file"]["width"], d["file"]["height"]],
            "fractional_alpha_pixels": d["file"]["fractional_alpha_pixels"],
            "visible_colours": d["file"]["visible_colours"],
            "q_sample_canvas": canvas, "q_sample_palette": palette,
            "expected": {"q_sample_canvas": want_canvas, "q_sample_palette": want_palette},
            "matched_expectation": matched,
            "outside_palette": d["criteria"]["q_sample_palette"]["measurements"]["outside_palette"],
        }
    agg = {
        "purpose": (
            "Dry run of work/sample-checks/check_sample_mechanical.py proving it discriminates. "
            "Tooling output only: no X/E/V records, no verdict, no acceptance. The references are "
            "not candidates; they are run to show the expected pass path. The fixtures are "
            "synthetic files derived from reference.png with exactly one condition broken each."
        ),
        "harness": DIR + "check_sample_mechanical.py",
        "runs": runs,
        "discriminates_as_expected": ok,
    }
    with open(DIR + "dry-run.json", "w", encoding="utf-8", newline="\n") as handle:
        json.dump(agg, handle, indent=1)
        handle.write("\n")
    print(json.dumps(agg, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
