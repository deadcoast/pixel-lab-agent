# PIXL

PIXL is a pixel-art production agent profile and skill system for Claude and Codex. This repository develops that profile, its operational skills, and the tools and knowledge that support its work. The intended outcome is coherent UI and game assets produced through the official PixelLab platform from project-specific references, inspected, integrated, and preserved with enough context for another agent or session to continue.

**Overall request remains open.** The [overall plan and TODO](TODO.md) is the current development work list: ordered remaining outcomes, evidence, completion criteria and next action. Completed increments below do not mean the specialist ecosystem is finished.

**Current stage: scoped production demonstrated; broader reliability remains in development.** Allocation, first-request preparation, connected authoring, durable provider recovery, inspection and family delivery are implemented. [Official PixelLab production](evidence/pixellab-family-production/README.md) records actual generated assets and repairs; [successor acceptance](evidence/successor-acceptance/README.md) records motion/family review in both existing consumers. [Named Codex qualification](evidence/named-codex-role/README.md) passes one explicitly registered role and same-child recovery/handoff. The [artistic-revision task](evidence/artistic-revision/README.md) now completes the original Claude corrected29 successor with fresh acceptance of existing artwork; all task-outcome checks pass, while an outer recorder failure keeps the overall trial partial. These scoped results retain caller corrections and failed evidence. [Useful native production](evidence/native-production/README.md) now reaches actual caller consumption in both hosts: Codex passes 35/35 checks and Claude 40/40 after two guided same-parent/same-child recoveries, including a family-directory runtime correction. Exact tested kits and original failures remain retained. Automatic discovery, broader host reliability, independent artistic consistency and other asset/engine classes remain open. The [last complete verifier](evidence/test-results.json) establishes its recorded implementation checks, not general production readiness. [PLAN](PLAN.md), [SHELVED](SHELVED.md) and [TODO](TODO.md) carry the remaining work.

**Consumer setup:** the read-only readiness report distinguishes installed files, supplied host observations and provider visibility. [Fresh installation and native results](evidence/readiness/README.md) qualify copied-kit, wheel and locked source local use, Codex's explicit portable role, and Claude's authenticated plugin route, including omitted-role/plugin cases in both hosts. Earlier authentication blocks and grader corrections remain preserved; these scoped local outcomes do not establish provider access or broader reliability. Follow the [consumer-first setup guide](docs/AGENT-KIT.md#set-up-a-consumer-project) and [declared install/update support matrix](docs/INSTALL-SUPPORT.md) for qualified runtime routes, relocation and cold recovery limits.

**Caller handoff:** the opt-in [compact caller result](evidence/caller-result/README.md) keeps full observations and exact continuation behind verified locators, with structured local recovery. Codex completes the scoped operation at 28/28 independent checks. The original Claude attempt retains its incomplete HTTP-429/timeout result. A later guided continuation completes the same retained caller assignment at 31/31 checks plus a separate 22/22 review; its frozen-kit scope and broader reliability limits remain explicit.

**Candidate/family review:** [review-context and candidate-review](spec/candidate-review.md) expose literal criteria and exact bindings, retain explicit observations, and connect nomination/completion with recoverable retries. The specialist still supplies actual visual and destination judgments. Prepared inspection packets retain their existing view-coverage rules.

**Isolated consumer execution:** [`consumer-execute`](spec/consumer-execution.md) runs the shipped queue-motion profile, checks actual frame/wrap and reduced-motion-switch observations, and retains exact delivered-file evidence. It leaves production state and acceptance unchanged. [TM-07 results and limits](evidence/consumer-execution/README.md) track the scoped qualification; M1/M2 and broader M3 remain open.

**Historical HTTP integration milestone complete for the controlled test.** Claude and Codex each delegated to PIXL, submitted through the official HTTP adapter, retrieved and inspected the fixture, and saved an independent parent review. See the [recorded outcomes](evidence/delegated-asset-request/README.md) and [milestone contract](evaluations/delegated-asset-request.spec.md). Provider transport was simulated; these results establish the delivery workflow, not newly generated artwork or target-engine quality.

**Project asset requirements:** use `$plar` in Codex or `/plar` in Claude to create or update the consumer project's `plar.txt`, then hand a selected asset to PIXL for paid official PixelLab production. The selected-asset path now uses `pixl_plar_prepare` / `plar prepare` to turn reviewed arguments and candidate criteria into the durable first request; [workflow and actual results](evidence/plar-allocation/README.md). Read the [critical review and A–E answers](docs/PLAR-REVIEW.md), [PLAR skill](plugins/pixl/skills/plar/SKILL.md) and [worked consumer project](examples/plar-project/README.md).

**Request and criteria handoff:** the specialist returns the exact proposed request, reference inputs and acceptance criteria; the calling agent compares them with the original sources and retains its own review before adoption. [Earlier native results](evidence/request-review/README.md) retain controlled delivery and original failures. [Targeted handoff repairs](evidence/handoff-repair/README.md), [criteria comparison](evidence/criteria-handoff/README.md) and [focused successor authoring](evidence/focused-authoring/README.md) record later corrections and remaining interrupted/native-route gaps. [The operation](plugins/pixl/skills/pixl/references/request-review.md) keeps contract agreement, delivered-file review and actual provider quality distinct.

**Delegate visual work:** give PIXL the consumer root, a selected asset or direct brief, reference roles, and the existing decisions and authorization. The specialist chooses the PixelLab operation and returns files, findings and resumable context. Start with the [agent-to-agent contract](plugins/pixl/skills/pixl/references/delegation.md), [official-operation guide](plugins/pixl/skills/pixl/references/pixellab-operations.md), [connection templates](docs/AGENT-KIT.md#connect-official-pixellab), and [reference-aware example](examples/delegation/README.md). The [development review](docs/AGENT-HANDOFF-REVIEW.md) answers the required A–E questions.

For repository development, follow [AGENTS.md](AGENTS.md). Reading or editing PIXL's profile does not activate it. Invoke the production profile when the task is to perform pixel-art work.

The UDL is designed for agent operation. Human readability is not a wire-design criterion. Host Markdown, JSON and TOML exist at the Claude/Codex/MCP boundary; the operational project language is `.px`.

## Use it

Use the [capability/outcome matrix](docs/CAPABILITY-OUTCOMES.md) to choose a useful route, see what actually worked in each host and consumer, and identify the next unqualified condition. Human acceptance is recorded separately from development qualification.

For an asset assignment, start with the [everyday production guide](plugins/pixl/skills/pixl/references/everyday.md):
select the actual queue/asset, prepare or resume the official request, review the
candidate and family, and return usable files with a saved continuation.

1. Load the complete PIXL kit in the consumer project through the [host setup](docs/AGENT-KIT.md#set-up-a-consumer-project).
   The profile and skills make PIXL the visual specialist; a Python installation
   alone does not register the host's agent or skills.
2. Keep the host's official PixelLab connection available for production. The
   local CLI/MCP supports requirements, state, inspection and handoff; it does not
   replace the official provider. Inspect the actual connected tool declarations.
3. Give PIXL the consumer root, selected asset or brief, reference roles and
   existing choices/authorization. The caller receives actual files, findings
   and a precise continuation.

The complete portable kit is [`plugins/pixl`](plugins/pixl). Its consumer runtime
needs Python 3.11+, Pillow and jsonschema, without maintainer tooling. Follow the
[copied-kit instructions](docs/AGENT-KIT.md#set-up-a-consumer-project) for a selected
environment and host entrypoint. A wheel is an alternative local-runtime
distribution; it does not install skills or register a named specialist.

When setup is uncertain, use the [read-only readiness report](plugins/pixl/skills/pixl/references/readiness.md):

```text
python ABSOLUTE_KIT/scripts/pixl.py readiness --root CONSUMER --host codex --installation ABSOLUTE_KIT
```

Use the selected interpreter and quote paths containing spaces. The report
separates installed files, caller-supplied host observations and tool visibility;
it performs no authentication or generation probe. The [hash and path reference](plugins/pixl/skills/pixl/references/identities-and-paths.md)
explains the distinct installation, consumer and store roots during production.

## Maintain this repository

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

The default development sync keeps lint, type-checking, build and benchmark tools
in the dev group. `uv sync --locked --no-dev` is a runtime-only source-checkout
route; it needs this repository and lockfile. It is not required for a consumer
using a complete copied kit. Tokenizer benchmarking remains in the optional
`benchmark` extra as well as the maintainer environment.

For a read-only check of current package inputs and retained capability claims, run
`.venv/Scripts/python.exe -B scripts/check_integrity.py`. The
[integrity guide](docs/EVIDENCE-INTEGRITY.md) explains historical results, stale
current applicability and exact recovery actions. The command prints a report
without rebuilding packages or evidence.

The verifier archives previous generated evidence, regenerates local fixtures and the plugin, discovers the entire test suite, and builds/installs a wheel through its source distribution. Each attempt has its own directory under `evidence/verification-runs/`; a failed stage leaves a current failure report and identifies unperformed stages. See [verification scope](docs/VERIFICATION.md) for separate lint/type checks and evidence limits.

The checked-in source adapters expose `$pixl` in Codex and `/pixl` in Claude;
Claude also supports `claude --agent pixl` from this checkout. Consumer/plugin
entrypoints have their own paths and names in [AGENT-KIT.md](docs/AGENT-KIT.md).
No global configuration is changed by the kit.

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
