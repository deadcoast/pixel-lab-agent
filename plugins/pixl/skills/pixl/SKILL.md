---
name: pixl
description: Plan, produce, inspect, and integrate pixel-art assets with PixelLab and validated PIXL production state. Use for coherent sprite families, animation, tiles, style contracts, or PIXL UDL work.
---

Adopt the [PIXL profile](../../resources/agent/PROFILE.md). Resolve every relative path here from this skill directory, not the user's current working directory. The plugin root is two directories above this file's directory. Read only resources needed for the current operation.

PIXL's custom UDL holds agent production state. This Markdown file and the plugin manifests are harness adapters. Read the [versioned UDL specification](../../resources/spec/PIXL-1.md) and [registry](../../runtime/pixl/registry.json) before authoring state. Locate relevant material in `../../resources/knowledge/`; examples under `../../resources/examples/` illustrate syntax, not an automatically approved project style.

Use the [production workflow](references/production.md) for asset work and the [runtime boundary](references/runtime.md) for state operations or MCP wiring. Preserve the user's source aesthetics, research consequential method choices, and prove uncertain methods on a representative sample before generating a batch.

The compiled operational knowledge is [library.px](../../resources/knowledge/library.px). Retrieve one method with `context <resolved library.px> k.<method-id> --root <resolved resources directory>`. This returns the method's prerequisites, procedure, checks, failure conditions, exact source locators and current bounded POC receipt. Applicability atoms map losslessly to source meanings in [applicability.json](../../resources/knowledge/applicability.json). Read receipt limitations before adopting a method for a different production contract.

The bundled runner is `../../scripts/pixl.py`; the runtime is `../../runtime/`. Resolve the runner to an absolute path and run it with the selected Python environment: `python "<resolved runner>" --help`. It requires Python 3.11+, Pillow 10+, and jsonschema 4.18+; install the bundled `../../requirements.txt` into the selected environment. It loads the bundled package regardless of the project working directory. Keep mutable state and outputs in the user's project. In a source checkout, `python -m pixl` is also available after local package setup.

Before a remote action, discover the actual PixelLab tools and their schemas in the harness. PIXL's local `prepare` operation records intent, and its job operation records journal state. Neither submits, polls, authenticates to, or generates with PixelLab. Use only the actual remote tool response to establish a real job identifier and status. If tools or credentials are unavailable, complete local planning and checks and name the precise missing capability.

Validate mechanical constraints, inspect images visually, and verify required engine import behavior before accepting an asset. Report what was checked and what remains uncertain. Retain evidence and use the expected current state hash when committing UDL updates. Do not claim live generation or model-performance improvements from fixtures or local validation.
