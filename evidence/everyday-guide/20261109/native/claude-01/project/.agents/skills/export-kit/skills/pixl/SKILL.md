---
name: pixl
description: Use when delegating or producing PixelLab visual assets, including UI, sprites, animation, tiles, fonts, style consistency, inspection and project integration. Developing the PIXL profile, skills, language, runtime, or plugin is a maintainer task and does not activate this profile.
---

For an assigned pixel-art production task, adopt the [PIXL profile](../../resources/agent/PROFILE.md). If the task is to develop or review PIXL itself, retain the development role and treat this skill and the profile as artifacts under review. Merely reading their instructions does not change the reader's role. Resolve every relative path here from this skill directory, not the user's current working directory. The plugin root is two directories above this file's directory. Read only resources needed for the current operation.

Start with [everyday asset production](references/everyday.md): assignment → selected
asset → official request → candidate/family review → delivery and continuation.
It uses public operations and links detailed procedures at the step that needs them.
Use [hash identities and paths](references/identities-and-paths.md) when choosing a
publication guard, following a source locator, exporting a result or relocating a
consumer. Preserve the current assignment's queue path and production generation.

For work assigned by another agent, use the [delegation contract](references/delegation.md) to carry project context and return consumable results. At contract handoff, use [request and criteria review](references/request-review.md): return the exact artifacts for the caller to compare with its original assignment before adoption. For tool choice and reference conditioning, use [PixelLab operations](references/pixellab-operations.md). Start from the official [platform docs](https://www.pixellab.ai/docs) and [MCP tool overview](https://api.pixellab.ai/mcp/docs); then inspect the relevant connected tool declaration.

For a retained production result, the delegation contract uses `pixl_plar_handoff` to save exact continuation data alongside your expert findings. Return its path/hash so another agent can resume without a manually rewritten job summary.

The [state-authority reference](references/state-authority.md) preserves the detailed production-state rules. Load it when authoring or resuming state. PIXL's custom UDL holds agent production state. This Markdown file and the plugin manifests are harness adapters. Read the specification and registry for the state's actual format before authoring it: [PX1 specification](../../resources/spec/PIXL-1.md) / [registry](../../runtime/pixl/registry.json), or [PX2 specification](../../resources/spec/PIXL-2.md) / [registry](../../runtime/pixl/registry-v2.json). New intake/sample operations use PX2; existing PX1 state keeps its original meaning. Locate relevant material in `../../resources/knowledge/`; examples under `../../resources/examples/` illustrate syntax, not an automatically approved project style.

For repository-wide asset requirements, load [PLAR](../plar/SKILL.md), then select an asset from the consumer project's `plar.txt`. For an existing asset request, use its focused row or supplied brief directly. A selected PLAR asset's first concrete candidate can use [PLAR preparation](../plar/references/prepare.md) to save the reviewed plan and durable request without handwriting PX2 records. PLAR owns the requirements queue; PX2 owns the retained production attempt and acceptance evidence. Keep actual source requirements stable when the queue status changes.

Production uses the official paid PixelLab API, preferring the authenticated MCP tool surface. The optional HTTP adapter is a separate explicitly selected route for the operation it supports. Preserve existing user authorization and scope. Discover the actual operation and schema before translating the selected asset contract.

Use the [production workflow](references/production.md) for asset work and the [runtime boundary](references/runtime.md) for state operations or MCP wiring. Preserve the user's source aesthetics, research consequential method choices, and prove uncertain methods on a representative sample before generating a batch.

When imported library sources must survive kit updates, use [source retention and recovery](references/library-retention.md). Read reported retained-source identities during resumption; old proof remains scoped to its original bytes.

Use the [source-grounded knowledge operation](references/knowledge.md) to answer a production question from the actual supplied sources. It defines source discovery, method selection, exact text retrieval, applicability assessment, and the stopping condition before project-specific adoption.

Use the [intake and representative-sample operation](references/intake-sample.md) to retain unknown/proposed/confirmed choices, plan outputs before files exist, and record mechanical, visual, continuity or engine acceptance separately. Before deriving style criteria, checker rules or provider instructions, apply its [authority check](references/intake-sample.md#keep-authority-through-derived-rules). Save applicable criteria before evaluation and preserve failed or unavailable checks through resumption. For a cold resume without an accepted representative sample, read this reference and follow its handoff guidance before the final response.

Keep requirement authority through each translation: explicit user/project constraints, observations and proposals remain distinct in the provider request and review criteria. Read [the artistic-authority checks](references/artistic-authority.md) when deriving aesthetic restrictions or auditing a contradictory approach; the retained examples are conditional guidance.

Use the [candidate inspection operation](references/inspection.md) to prepare saved candidate/reference views, inspect them through the host, and retain explicit reviews against their original criteria. Record actual viewing limits and next actions; mechanical measurements do not supply artistic acceptance.

Use the [provider submission and recovery operation](references/provider-recovery.md) to save an exact request against its task and output plans, claim dispatch before a host call, reconcile unknown outcomes and import returned candidates. Read both workflow and job status before starting another request.

Use the [family and delivery operation](references/family-delivery.md) when extending an approved sample, comparing related assets, retaining a delivery package or resuming family production. Save exact baseline, members, destination choices and collective criteria first. Inspect actual animation playback or tile neighborhoods when applicable, retain failed revisions, and distinguish copied files from accepted delivery. Start cold sessions with family, workflow and job reports.

The compiled operational knowledge is [library.px](../../resources/knowledge/library.px). Retrieve one method with `context <resolved library.px> k.<method-id> --root <resolved resources directory>`. This returns the method's prerequisites, procedure, checks, failure conditions, exact source locators and current bounded POC receipt. Applicability atoms map losslessly to source meanings in [applicability.json](../../resources/knowledge/applicability.json). Read receipt limitations before adopting a method for a different production contract.

The bundled runner is `../../scripts/pixl.py`; the runtime is `../../runtime/`. Resolve the runner to an absolute path and run it with the selected Python environment: `python "<resolved runner>" --help`. It requires Python 3.11+, Pillow 10+, and jsonschema 4.18+; install the bundled `../../requirements.txt` into the selected environment. It loads the bundled package regardless of the project working directory. Keep mutable state and outputs in the user's project. In a source checkout, `python -m pixl` is also available after local package setup.

Before a remote action, discover the actual PixelLab tools and their schemas in the harness. The durable `job-prepare` and `job-dispatch` operations save intent and a single dispatch claim; the host performs the actual call. The original `prepare` and `job` commands remain stateless compatibility helpers. The local PIXL state server does not submit or poll PixelLab. The optional separate HTTP bridge does execute its documented official API operation; the host's PixelLab MCP connection exposes its own current tool surface. Use only actual remote observations to establish a real identifier and status. If tools or credentials are unavailable, complete local planning and checks and name the precise missing capability.

Validate mechanical constraints, inspect images visually, and verify required engine import behavior before accepting an asset. Report what was checked and what remains uncertain. Retain evidence and use the expected current state hash when committing UDL updates. `pixl_commit` accepts a JSON `document` directly or a `candidate` wire-file path; both use the same validation. Do not claim live generation or model-performance improvements from fixtures or local validation.
