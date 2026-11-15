"""Opt-in official PixelLab bridge. The normal pixl.py MCP server remains local."""

import os
import runpy
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "runtime"))
os.environ["PIXL_PLUGIN_ROOT"] = str(root)
runpy.run_module("pixl.pixellab_mcp", run_name="__main__", alter_sys=True)
