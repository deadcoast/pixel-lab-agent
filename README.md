# PIXL

PIXL is a proprietary agent-operated project language and pixel-art production kit for Claude and Codex. It combines a versioned UDL, an executable state/evidence runtime, source-grounded pixel-art knowledge, a current PixelLab capability inventory, and a shared expert agent profile.

The UDL is designed for agent operation. Human readability is not a wire-design criterion. Host Markdown, JSON and TOML exist at the Claude/Codex/MCP boundary; the operational project language is `.px`.

## Use it

Python 3.11 or newer:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e .
.venv/Scripts/python.exe scripts/verify.py
.venv/Scripts/python.exe -m pixl validate examples/atelier/project.px --root .
.venv/Scripts/python.exe -m pixl context examples/atelier/project.px produce
```

On POSIX, use `.venv/bin/python`. Invoke `$pixl` in Codex from this repository, or `/pixl` in Claude. Claude also supports `claude --agent pixl`. The complete portable plugin is [`plugins/pixl`](plugins/pixl); [`AGENT-KIT.md`](docs/AGENT-KIT.md) gives exact discovery, relocation and MCP setup instructions. No global configuration has been changed.

## What is implemented

- **PIXL/1:** 13 typed record kinds for actors, projects, sources, runtime dependencies, visual contracts, knowledge, decisions, tasks, assets, evidence, remote jobs and handoff context. Deterministic grammar, canonical hashes, closed schemas, dependency ordering and complete context selection.
- **State runtime:** revision-checked commits, local writer exclusion, immutable snapshots, immutable proof receipts with explicit supersession, source/artifact drift checks and mandatory reopening of affected completed tasks.
- **Pixel-art knowledge:** 43 scoped methods with 93 exact local source ranges, research decisions, concrete POC recipes, and 24 executable reference checks spanning 28 methods. Coverage and unexecuted project-specific recipes are explicit in [`methods/method-proof-coverage.json`](methods/method-proof-coverage.json).
- **PixelLab preparation:** 100 documented MCP tools and 454 parameters, a dated official documentation snapshot, exact caller-supplied schema validation, cross-field rules, deterministic intent identity and observation-based job journaling.
- **Agent kit:** one shared PIXL expert profile, Claude/Codex adapters, a portable runtime, and 14 local MCP tools. The actual authenticated PixelLab connection remains with the host harness.

## Source and evidence

| Artifact | Purpose |
|---|---|
| [PIXL specification](spec/PIXL-1.md) and [registry](pixl/registry.json) | Complete implemented syntax, types, semantics and boundaries |
| [Design and implementation decisions](docs/IMPLEMENTATION.md) | WHO / WHAT / WHERE / WHY, research, alternatives and proof obligations |
| [PIXL profile](agent/PROFILE.md) | Forward-facing expert behavior and production loop |
| [Pixel-art research](docs/research/pixel-art-knowledge.md) | Curated methods, source corrections and artistic scope |
| [PixelLab research](docs/research/pixellab-platform.md) | Tool capabilities, API distinctions and execution constraints |
| [Verification](docs/VERIFICATION.md) | Reproduction commands, failed attempts, final evidence and limitations |
| [Test results](evidence/test-results.json) | Actual suite counts, runtime hashes and source preservation |
| [Representation benchmark](evidence/representation-benchmark.json) | Equal-semantics byte/token measurements and bootstrap cost |

The original five source files are preserved. The catalog indexes them without executing embedded examples and records duplicate research by content hash. Local reference fixtures are labeled as fixtures; they are not PixelLab-generated assets.

Live PixelLab generation, target-engine import and controlled multi-model performance trials were not run. The kit implements the local mechanisms and teaches the agent how to gather those project-specific proofs. A smaller serialization and passing mechanical checks do not establish better reasoning or better art.
