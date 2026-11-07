---
name: pixl
description: Use when producing, inspecting, or integrating pixel-art assets, or maintaining an art project's PIXL production state. Repository development, architecture review, and authoring PIXL profiles, skills, or runtime code are maintainer tasks and do not activate this profile.
---

For a production task, read and follow the canonical [PIXL skill](../../../plugins/pixl/skills/pixl/SKILL.md) and [profile](../../PROFILE.md). When developing or reviewing PIXL itself, retain the development role and inspect those files as project artifacts. Reading this wrapper or encountering `.px` does not itself activate PIXL. Resolve those paths from this file's directory; the repository root is three levels above it.

This is the repository discovery wrapper. In this source checkout, use `spec/PIXL-1.md`, `pixl/registry.json`, `knowledge/`, and `examples/` as the current sources. Use `python -m pixl --help` from the repository after local package setup, or the bundled runner after `python scripts/build_plugin.py`. Keep generated project artifacts in the selected project directory.

The local runtime validates and manages production state. Remote PixelLab tools require their own authenticated harness connection. Discover actual schemas and returned IDs; preparation and journal state do not establish remote execution.
