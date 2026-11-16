"""Run the copied kit's read-only handoff coverage utility."""

import runpy
import sys
from pathlib import Path


def main():
    # -I ignores PYTHONDONTWRITEBYTECODE. Protect the read-only kit even when
    # callers omit -B; direct execution does not cache this launcher itself.
    sys.dont_write_bytecode = True
    runtime = Path(__file__).resolve().parents[1] / "runtime"
    if sys.version_info < (3, 11):  # noqa: UP036 - Copied launchers must reject old Python before runtime imports.
        print("PIXL requires Python 3.11 or newer.", file=sys.stderr)
        raise SystemExit(2)
    if not (runtime / "pixl/handoff_review.py").is_file():
        print("PIXL handoff review runtime is missing. Copy or reinstall the complete kit.", file=sys.stderr)
        raise SystemExit(2)
    sys.path.insert(0, str(runtime))
    runpy.run_module("pixl.handoff_review", run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    main()
