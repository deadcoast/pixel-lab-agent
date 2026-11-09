"""Run the PIXL package bundled inside this plugin, independent of the caller's cwd."""

import os
import runpy
import sys
from pathlib import Path


def main() -> None:
    plugin_root = Path(__file__).resolve().parents[1]
    runtime = plugin_root / "runtime"
    if not (runtime / "pixl" / "__main__.py").is_file():
        print(
            "PIXL bundled runtime is missing. Build the plugin with "
            "python scripts/build_plugin.py from the source repository.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if sys.version_info < (3, 11):  # noqa: UP036 - Copied launcher must reject old Python before importing the runtime.
        print("PIXL requires Python 3.11 or newer.", file=sys.stderr)
        raise SystemExit(2)
    sys.path.insert(0, str(runtime))
    os.environ["PIXL_PLUGIN_ROOT"] = str(plugin_root)
    runpy.run_module("pixl", run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    main()
