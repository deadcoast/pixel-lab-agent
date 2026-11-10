# PIXL

PIXL is a pixel-art production agent profile and skill system for Claude and Codex. This repository develops that profile, its operational skills, and the tools and knowledge that support its work. The intended outcome is coherent UI and game assets produced through the official PixelLab platform from project-specific references, inspected, integrated, and preserved with enough context for another agent or session to continue.

**Overall request remains open.** The [overall plan and TODO](TODO.md) is the current development work list: ordered remaining outcomes, evidence, completion criteria and next action. Completed increments below do not mean the specialist ecosystem is finished.

**Current stage: scoped production demonstrated; broader reliability remains in development.** Allocation, first-request preparation, connected authoring, durable provider recovery, inspection and family delivery are implemented. [Official PixelLab production](evidence/pixellab-family-production/README.md) records actual generated assets and repairs; [successor acceptance](evidence/successor-acceptance/README.md) records motion/family review and execution in both existing consumers. Those results are scoped and include maintainer intervention. [Named Codex qualification](evidence/named-codex-role/README.md) now passes one explicitly registered role and same-child recovery/handoff; automatic discovery and broader host reliability remain open. Independent artistic consistency and other asset/engine classes also remain open. The [last complete verifier](evidence/test-results.json) establishes its recorded implementation checks, not general production readiness. [PLAN](PLAN.md), [SHELVED](SHELVED.md) and [TODO](TODO.md) carry the remaining work.

**Candidate/family review:** [review-context and candidate-review](spec/candidate-review.md) expose literal criteria and exact bindings, retain explicit observations, and connect nomination/completion with recoverable retries. The specialist still supplies actual visual and destination judgments. Prepared inspection packets retain their existing view-coverage rules.

**Historical HTTP integration milestone complete for the controlled test.** Claude and Codex each delegated to PIXL, submitted through the official HTTP adapter, retrieved and inspected the fixture, and saved an independent parent review. See the [recorded outcomes](evidence/delegated-asset-request/README.md) and [milestone contract](evaluations/delegated-asset-request.spec.md). Provider transport was simulated; these results establish the delivery workflow, not newly generated artwork or target-engine quality.

**Project asset requirements:** use `$plar` in Codex or `/plar` in Claude to create or update the consumer project's `plar.txt`, then hand a selected asset to PIXL for paid official PixelLab production. The selected-asset path now uses `pixl_plar_prepare` / `plar prepare` to turn reviewed arguments and candidate criteria into the durable first request; [workflow and actual results](evidence/plar-allocation/README.md). Read the [critical review and A–E answers](docs/PLAR-REVIEW.md), [PLAR skill](plugins/pixl/skills/plar/SKILL.md) and [worked consumer project](examples/plar-project/README.md).

**Request and criteria handoff:** the specialist returns the exact proposed request, reference inputs and acceptance criteria; the calling agent compares them with the original sources and retains its own review before adoption. [Earlier native results](evidence/request-review/README.md) retain controlled delivery and original failures. [Targeted handoff repairs](evidence/handoff-repair/README.md), [criteria comparison](evidence/criteria-handoff/README.md) and [focused successor authoring](evidence/focused-authoring/README.md) record later corrections and remaining interrupted/native-route gaps. [The operation](plugins/pixl/skills/pixl/references/request-review.md) keeps contract agreement, delivered-file review and actual provider quality distinct.

**Delegate visual work:** give PIXL the consumer root, a selected asset or direct brief, reference roles, and the existing decisions and authorization. The specialist chooses the PixelLab operation and returns files, findings and resumable context. Start with the [agent-to-agent contract](plugins/pixl/skills/pixl/references/delegation.md), [official-operation guide](plugins/pixl/skills/pixl/references/pixellab-operations.md), [connection templates](docs/AGENT-KIT.md#connect-official-pixellab), and [reference-aware example](examples/delegation/README.md). The [development review](docs/AGENT-HANDOFF-REVIEW.md) answers the required A–E questions.

For repository development, follow [AGENTS.md](AGENTS.md). Reading or editing PIXL's profile does not activate it. Invoke the production profile when the task is to perform pixel-art work.

The UDL is designed for agent operation. Human readability is not a wire-design criterion. Host Markdown, JSON and TOML exist at the Claude/Codex/MCP boundary; the operational project language is `.px`.

## Use it

For an asset assignment, start with the [everyday production guide](plugins/pixl/skills/pixl/references/everyday.md):
select the actual queue/asset, prepare or resume the official request, review the
candidate and family, and return usable files with a saved continuation. The
[hash and path reference](plugins/pixl/skills/pixl/references/identities-and-paths.md)
explains the public result labels and examples for another consumer root. The
commands below are repository development/setup checks, not the asset workflow.

The project is uv managed. Keep the existing `.venv`; the current development environment uses Python 3.14.3 (the package declares Python 3.11 or newer):

```powershell
uv sync --locked
uv build
uv run --no-sync python scripts/verify.py
uv run --no-sync python -m pixl sources --root .
uv run --no-sync python -m pixl workflow examples/intake/project.px --root .
uv run --no-sync python -m pixl validate examples/atelier/project.px --root .
uv run --no-sync python -m pixl context examples/atelier/project.px produce
```

Runtime installation requires Pillow and jsonschema. The default development sync keeps lint, type-checking, build and benchmark tools in the dev group. For a consumer environment use `uv sync --locked --no-dev` or install the wheel normally; tokenizer benchmarking is also available through the `benchmark` extra.

The verifier archives previous generated evidence, regenerates local fixtures and the plugin, discovers the entire test suite, and builds/installs a wheel through its source distribution. Each attempt has its own directory under `evidence/verification-runs/`; a failed stage leaves a current failure report and identifies unperformed stages. See [verification scope](docs/VERIFICATION.md) for separate lint/type checks and evidence limits.

Invoke `$pixl` in Codex from this repository, or `/pixl` in Claude. Claude also supports `claude --agent pixl`. The complete portable plugin is [`plugins/pixl`](plugins/pixl); [`AGENT-KIT.md`](docs/AGENT-KIT.md) gives exact discovery, relocation and MCP setup instructions. No global configuration has been changed.

## Scaffold mechanisms

- **PIXL/1:** 13 typed record kinds for actors, projects, sources, runtime dependencies, visual contracts, knowledge, decisions, tasks, assets, evidence, remote jobs and handoff context. Deterministic grammar, canonical hashes, closed schemas, dependency ordering and complete context selection.
- **PIXL/2 lifecycle:** explicit choices, planned outputs, criteria and immutable verdicts. Start with `intake`, save the acceptance plan before evaluation, and use `workflow` to distinguish unperformed, failed, unavailable and passing checks. A sample can investigate a proposal; production adoption has stronger gates. The [operational skill](plugins/pixl/skills/pixl/references/intake-sample.md) covers the complete local sequence.
- **Family delivery:** exact approved sample dependencies, ordered member plans, collective continuity and destination criteria, immutable copied files and historical snapshot drift. The [family skill](plugins/pixl/skills/pixl/references/family-delivery.md) connects actual comparison and revision to `family` / `family-snapshot`; retaining a package creates no acceptance.
- **Candidate inspection:** exact native/nearest views, explicit frame/tile context, source-bound measurements and retained reviewer declarations. The [inspection skill](plugins/pixl/skills/pixl/references/inspection.md) uses `inspection-prepare`, host viewing and `inspection-review`; `inspection` recovers original conditions, failures and viewing limits. The runtime supplies no automatic artistic verdict.
- **State runtime:** revision-checked commits, local writer exclusion, immutable snapshots, immutable proof receipts with explicit supersession, source/artifact drift checks and mandatory reopening of affected completed tasks.
- **Pixel-art knowledge:** 43 curated methods with 93 reviewed current source locators and 39 freshly executed reference checks. The compiled [PIXL library](knowledge/library.px) contains prerequisites, procedures, checks, pitfalls, sources and bound proof receipts. The [knowledge operation](plugins/pixl/skills/pixl/references/knowledge.md) takes a production question through source discovery, exact retrieval, applicability assessment and a specific next proof. [Coverage](methods/method-proof-coverage.json) states each reference proof's limits.
- **PixelLab preparation:** a historical snapshot of 100 documented MCP tools and 454 parameters, dated official documentation, exact caller-supplied schema validation, cross-field rules, deterministic intent identity and observation-based job journaling.
- **Optional PixelLab HTTP adapter:** one official async image endpoint, exact retained OpenAPI schema, durable submission/polling and PNG import. A separate opt-in MCP bridge exposes it; tests replace its HTTP transport and block sockets.
- **Agent kit:** one shared PIXL expert profile, Claude/Codex adapters, a portable runtime, and the [declared local MCP tools](pixl/mcp.py). The actual authenticated PixelLab connection remains with the host harness.

## Source and evidence

| Artifact | Purpose |
|---|---|
| [PX1 specification](spec/PIXL-1.md) / [registry](pixl/registry.json), [PX2 specification](spec/PIXL-2.md) / [registry](pixl/registry-v2.json) | Versioned syntax, types, semantics and boundaries |
| [Design and implementation decisions](docs/IMPLEMENTATION.md) | WHO / WHAT / WHERE / WHY, research, alternatives and proof obligations |
| [PIXL profile](.agents/PROFILE.md) | Forward-facing expert behavior and production loop |
| [Pixel-art research](docs/research/pixel-art-knowledge.md) | Curated methods, source corrections and artistic scope |
| [PixelLab research](docs/research/pixellab-platform.md) | Tool capabilities, API distinctions and execution constraints |
| [Verification](docs/VERIFICATION.md) | Reproduction commands, failed attempts, final evidence and limitations |
| [Test results](evidence/test-results.json) | Actual suite counts, runtime hashes and source preservation |
| [Representation benchmark](evidence/representation-benchmark.json) | Equal-semantics byte/token measurements and bootstrap cost |

The supplied source corpus is under [training/original-docs](training/original-docs), identified by [source-inventory.json](training/source-inventory.json). All five files retain their supplied bytes. The [citation migration](knowledge/source-migration.json) records old/current identities and reviewed line correspondence; [archived evidence](evidence/source-migration/previous-run/manifest.json) preserves the earlier source layout and receipts. Current receipts were regenerated by executing against the current sources. Local reference fixtures are labeled as fixtures; they are not PixelLab-generated assets.

Live PixelLab generation and scoped destination execution are recorded in the production/acceptance links above. Earlier local fixtures and model-comparison trials retain their original narrower scopes. A smaller serialization, passing mechanical checks or one accepted family does not establish better reasoning, general artistic quality or broad host reliability.
