# PIXL

PIXL is a pixel-art production agent profile and skill system for Claude and Codex. This repository develops that profile, its operational skills, and the tools and knowledge that support its work. The intended outcome is coherent game assets produced from project-specific references, inspected, integrated, and preserved with enough context for another session to continue.

**Current stage: developing beyond the initial scaffold.** Source-grounded research, intake/sample acceptance, durable provider recovery and family delivery are implemented locally. PX2 connects approved baselines, planned members, collective criteria and destination choices to exact retained packages. Existing PX1 and legacy PX2 semantics are preserved. The last runtime milestone passed 324 tests with one Windows privilege skip. [Native host evaluation](evaluations/README.md) now observes both Claude and Codex on five matched cases, including repeated rejection of a defective sample. Interrupted trials, viewing gaps and unsupported contract choices remain visible in the evidence. Real provider/art/engine outcomes and six further scenarios remain open. Read the [project review](docs/PROJECT-REVIEW.md) and [MIVIM task specifications](evaluations/TODO.spec.md) for the next work.

For repository development, follow [AGENTS.md](AGENTS.md). Reading or editing PIXL's profile does not activate it. Invoke the production profile when the task is to perform pixel-art work.

The UDL is designed for agent operation. Human readability is not a wire-design criterion. Host Markdown, JSON and TOML exist at the Claude/Codex/MCP boundary; the operational project language is `.px`.

## Use it

Python 3.11 or newer:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e .
.venv/Scripts/python.exe scripts/verify.py
.venv/Scripts/python.exe -m pixl sources --root .
.venv/Scripts/python.exe -m pixl workflow examples/intake/project.px --root .
.venv/Scripts/python.exe -m pixl validate examples/atelier/project.px --root .
.venv/Scripts/python.exe -m pixl context examples/atelier/project.px produce
```

On POSIX, use `.venv/bin/python`. Invoke `$pixl` in Codex from this repository, or `/pixl` in Claude. Claude also supports `claude --agent pixl`. The complete portable plugin is [`plugins/pixl`](plugins/pixl); [`AGENT-KIT.md`](docs/AGENT-KIT.md) gives exact discovery, relocation and MCP setup instructions. No global configuration has been changed.

## Scaffold mechanisms

- **PIXL/1:** 13 typed record kinds for actors, projects, sources, runtime dependencies, visual contracts, knowledge, decisions, tasks, assets, evidence, remote jobs and handoff context. Deterministic grammar, canonical hashes, closed schemas, dependency ordering and complete context selection.
- **PIXL/2 lifecycle:** explicit choices, planned outputs, criteria and immutable verdicts. Start with `intake`, save the acceptance plan before evaluation, and use `workflow` to distinguish unperformed, failed, unavailable and passing checks. A sample can investigate a proposal; production adoption has stronger gates. The [operational skill](plugins/pixl/skills/pixl/references/intake-sample.md) covers the complete local sequence.
- **Family delivery:** exact approved sample dependencies, ordered member plans, collective continuity and destination criteria, immutable copied files and historical snapshot drift. The [family skill](plugins/pixl/skills/pixl/references/family-delivery.md) connects actual comparison and revision to `family` / `family-snapshot`; retaining a package creates no acceptance.
- **State runtime:** revision-checked commits, local writer exclusion, immutable snapshots, immutable proof receipts with explicit supersession, source/artifact drift checks and mandatory reopening of affected completed tasks.
- **Pixel-art knowledge:** 43 curated methods with 93 reviewed current source locators and 39 freshly executed reference checks. The compiled [PIXL library](knowledge/library.px) contains prerequisites, procedures, checks, pitfalls, sources and bound proof receipts. The [knowledge operation](plugins/pixl/skills/pixl/references/knowledge.md) takes a production question through source discovery, exact retrieval, applicability assessment and a specific next proof. [Coverage](methods/method-proof-coverage.json) states each reference proof's limits.
- **PixelLab preparation:** 100 documented MCP tools and 454 parameters, a dated official documentation snapshot, exact caller-supplied schema validation, cross-field rules, deterministic intent identity and observation-based job journaling.
- **Agent kit:** one shared PIXL expert profile, Claude/Codex adapters, a portable runtime, and 24 local MCP tools. The actual authenticated PixelLab connection remains with the host harness.

## Source and evidence

| Artifact | Purpose |
|---|---|
| [PX1 specification](spec/PIXL-1.md) / [registry](pixl/registry.json), [PX2 specification](spec/PIXL-2.md) / [registry](pixl/registry-v2.json) | Versioned syntax, types, semantics and boundaries |
| [Design and implementation decisions](docs/IMPLEMENTATION.md) | WHO / WHAT / WHERE / WHY, research, alternatives and proof obligations |
| [PIXL profile](agent/PROFILE.md) | Forward-facing expert behavior and production loop |
| [Pixel-art research](docs/research/pixel-art-knowledge.md) | Curated methods, source corrections and artistic scope |
| [PixelLab research](docs/research/pixellab-platform.md) | Tool capabilities, API distinctions and execution constraints |
| [Verification](docs/VERIFICATION.md) | Reproduction commands, failed attempts, final evidence and limitations |
| [Test results](evidence/test-results.json) | Actual suite counts, runtime hashes and source preservation |
| [Representation benchmark](evidence/representation-benchmark.json) | Equal-semantics byte/token measurements and bootstrap cost |

The supplied source corpus is under [training/original-docs](training/original-docs), identified by [source-inventory.json](training/source-inventory.json). All five files retain their supplied bytes. The [citation migration](knowledge/source-migration.json) records old/current identities and reviewed line correspondence; [archived evidence](evidence/source-migration/previous/manifest.json) preserves the earlier source layout and receipts. Current receipts were regenerated by executing against the current sources. Local reference fixtures are labeled as fixtures; they are not PixelLab-generated assets.

Live PixelLab generation, target-engine import and controlled multi-model performance trials were not run. The kit implements the local mechanisms and teaches the agent how to gather those project-specific proofs. A smaller serialization and passing mechanical checks do not establish better reasoning or better art.
