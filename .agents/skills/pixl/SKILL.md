---
name: pixl
description: Use PIXL for pixel-art production, PixelLab asset workflows, style contracts, visual and import validation, or structured PIXL UDL state in this repository.
---

Read and follow the canonical [PIXL skill](../../../plugins/pixl/skills/pixl/SKILL.md) and [profile](../../../agent/PROFILE.md). Resolve those paths from this file's directory; the repository root is three levels above it.

This is the repository discovery wrapper. In this source checkout, use `spec/PIXL-1.md`, `pixl/registry.json`, `knowledge/`, and `examples/` as the current sources. Use `python -m pixl --help` from the repository after local package setup, or the bundled runner after `python scripts/build_plugin.py`. Keep generated project artifacts in the selected project directory.

The local runtime validates and manages production state. Remote PixelLab tools require their own authenticated harness connection. Discover actual schemas and returned IDs; preparation and journal state do not establish remote execution.
