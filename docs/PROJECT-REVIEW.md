# PIXL scaffold review and development direction

**Next milestone selected, 2026-11-05:** test a delegated generation request in
Claude and Codex through the official PixelLab integration. Exercise the production
request, job, retrieval, inspection and delivery workflow with only external calls
mocked; tests must not submit real generation jobs or consume credits.
[PX-EVAL-004](../evaluations/delegated-asset-request.spec.md) defines acceptance
and the mechanism assessment. The adapter and offline tests are implemented;
[native trial evidence](../evidence/delegated-asset-request/README.md) records outcomes
and interface friction separately from live provider execution. Preserve
existing work; the dated review below remains historical context.

Reviewed 2026-09-11 from commit `52f86dd`. This is a development review of the initial scaffold. It describes observed mechanisms and the work needed to support the intended agent; it does not certify a production system. The user's current direction is authoritative: this project concerns agent profiles and skills, with PIXL as the pixel-art production profile. The developer reviewing it does not adopt that profile.

**Current development update, 2026-09-11:** source-grounded research, intake/sample acceptance, durable provider recovery, local family delivery and [candidate inspection](../spec/candidate-inspection.md) are implemented. Inspection retains exact native/enlarged views, original semantic conditions and explicit reviews through existing PX2 X/E/V; it introduces no new UDL version or automatic artistic judgment. The current verifier passed 380 tests, one Windows privilege skip and 39 reference checks. The [inspection evidence](../evidence/candidate-inspection/README.md) separates runtime/copy proofs from new native profile trials. The earlier [five-case matched evaluation](../evaluations/README.md) stays frozen with its original package, failures and viewing limits. Remaining pressure cases, real generation and destination acceptance remain open; [MIVIM tasks](../evaluations/TODO.spec.md) retain that work.

The first [source-reproduction milestone](superpowers/plans/2026-09-11-source-provenance.md) established all five supplied-file identities and migrated 93 citations without changing the methods' other fields. Its earlier 140-pass/one-skip evidence is [archived](../evidence/intake-sample/previous-run/manifest.json). Findings below retain the initial scaffold review and are not a description of every current implementation.

## Product and intended operation

The central product is the agent's ability to carry out a coherent production assignment. A profile supplies its role, domain judgment, responsibilities, authority boundaries, and communication. Skills supply reusable procedures for particular operations. Knowledge supplies source-grounded techniques and their conditions. Tools supply deterministic operations and access to external services. Durable state preserves what the agent knows, has decided, has attempted, and still needs to resolve.

PIXL's specialist knowledge includes pixel craft, characters, animation, tiles, modular rigs, sub-pixel effects, simulation, rendering, and engine integration. These domains have different operations and acceptance criteria. Their examples are teaching and test material, not a request to build every illustrated game system into this repository.

The [profile](../.agents/PROFILE.md) describes the intended end operation:

1. Inspect the user's brief, references, existing assets, target, and constraints.
2. Establish a source-specific contract while retaining unresolved choices.
3. Choose methods and dependencies; exercise consequential uncertainties on a representative sample.
4. Discover and use actual tools under the established authorization and budget.
5. Preserve submissions, uncertain outcomes, returned identities, and observations.
6. Retrieve and inspect candidates mechanically, visually, and in their intended context.
7. Revise or accept each candidate against the applicable requirements.
8. Scale the accepted approach to the asset family, validate delivery, and preserve enough state to resume safely.

The useful output is an asset family with coherent identity, appropriate motion or adjacency, usable integration, and inspectable production history. A valid `.px` document, a tool catalog, or a successful generation request is an intermediate result.

## Architectural responsibilities

These are conceptual responsibilities, not a proposal to create six new frameworks. Keep them identifiable in the implementation; extract shared machinery when real operations establish what should be shared.

| Responsibility | Current location | Required role in the finished operation |
| --- | --- | --- |
| Development authority | User direction; now [AGENTS.md](../AGENTS.md) | Develop and evaluate the product without accidentally adopting its specialist prompt |
| PIXL profile | [agent/PROFILE.md](../.agents/PROFILE.md) | Consistent domain judgment, responsibility, communication, and task scope across hosts |
| Operational skills | [common skill](../plugins/pixl/skills/pixl/SKILL.md) and its two references | Defined entry conditions, required context, procedure, outputs, failure/recovery behavior, and completion criteria per operation |
| Domain knowledge | [supplied sources](pixel-art-training), [curation](../knowledge/pixel-art.json), compiled library | Retrieve relevant techniques with applicability and source limits; distinguish reference demonstrations from project-specific proof |
| State and evidence | [specification](../spec/PIXL-1.md), [registry](../pixl/registry.json), Python runtime | Represent uncertainty, dependencies, decisions, artifacts, observations, acceptance, change impact, and resumption without inventing facts |
| Harness and tool adapters | `.agents/`, `.claude/`, `plugins/pixl/`, local MCP and PixelLab preparation | Load the intended role, expose real capabilities, translate contracts deliberately, and preserve host/service boundaries |

The custom UDL remains an intentional part of this design. Its existing syntax is a versioned contract, not a constraint on what the final agent ought to be able to do. Extend it explicitly when an operating requirement demands it. Do not silently redefine PIXL/1 symbols or hide every missing concept in free text.

Profile prose is not a trained model. The `training/` folder currently supplies reference material; no training or controlled behavior-improvement pipeline was found. Domain breadth in a profile does not establish expertise on real tasks.

## Observed baseline

The checkout was clean before review. The selected environment ran:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -t . -v
```

Result: **123 tests run, 77 passed, 45 errors, one skipped**, exit 1. The skip was the existing Windows symlink-privilege case. The 45 errors comprised six knowledge-compilation tests, three packaging tests, and 36 POC tests. The retained [test log](../evidence/reviews/2026-09-11-scaffold/unittest.txt) records the individual failures. No test assertions failed; execution errors prevented those checks from reaching their assertions.

The existing [test-results.json](../evidence/test-results.json) reports an earlier 122-pass/one-skip run. It is historical evidence, not the current result. [Review probes](../evidence/reviews/2026-09-11-scaffold/probes.json) and their [reproduction script](../evidence/reviews/2026-09-11-scaffold/probes.py) record the additional local boundary checks. These use synthetic local records and never contact PixelLab.

Useful starting mechanisms exist: deterministic parsing, typed references, dependency closure, checked publication, evidence freshness, source slicing, local image measurements, provider argument checking, and observation journals. Their narrow guarantees should survive development. The missing work is how these mechanisms support the agent's complete operation.

## Findings and consequences

### R1. Production activation and development lacked an explicit boundary

The initial repository wrappers said to read and follow the profile, and the common skill said to adopt it unconditionally. The Claude definitions began directly with “You are PIXL.” They described production triggers but did not address development of PIXL itself. See the entrypoints listed in the architecture table; their pre-review forms are in `52f86dd`.

That makes review of the product's instructions ambiguous at the exact point the developer needs to inspect them. This is an instruction-design gap, not a claim that every model would misroute it. This pass adds a maintainer contract and explicit maintenance exclusions/production activation conditions to the three skills and two agent entrypoints. The canonical production profile remains the specialist's behavioral source.

### R2. Source relocation broke the current knowledge and packaging path

[catalog.py](../pixl/catalog.py) lines 11–18, [verify.py](../scripts/verify.py) lines 25–42, [build_plugin.py](../scripts/build_plugin.py) lines 41–48, [setup.py](../setup.py) lines 33–42, and [MANIFEST.in](../MANIFEST.in) line 8 still refer to old root filenames. Curated method sources also retain those locations. The actual files are under `training/original-docs/`.

This is more than a rename. The current deep-research document has 1,713 lines and the methods document 1,703; the bundled predecessors each had 1,647. Their current hashes differ from the historical identical hashes still described in research documentation. The training, assets, and links documents retain their old bytes under their new locations/names. Source ranges and duplicate claims must be reviewed against the current revisions.

The default catalog silently indexed only `NOTICE.md` and `README.md` in the original reviewed tree. POC and bundle operations fail when they try to read the missing originals. Merely copying obsolete bundled files back to the root or replacing hashes would hide the migration problem.

Required correction: establish one explicit source inventory, map the current files and reviewed ranges, preserve historical provenance, update all consumers and packaging routes, execute new proofs, then compile and validate the new bundle. Preserve the failed baseline separately.

### R3. Intake and planning do not have sufficient states

[store.empty_project](../pixl/store.py) lines 73–79 creates a 32×32 side-view, nearest-sampled, binary-alpha contract. Only its name and lighting prose say these values are unconfirmed. The [C schema](../pixl/registry.json) requires concrete values and has no representation for unresolved/observed/proposed/confirmed choices. The A role enum also has only agent/tool/system, although ownership can originate with the user.

D always requires proof and T always requires a decision. X always requires a content hash and a path that must exist during rooted validation/commit. The probe confirms that a future output cannot be represented as X before its file exists. T also combines input and output references in `io`.

An agent can work around this using text, a report artifact, or omitted outputs, but the model then has to invent conventions for basic production planning. The scaffold's example starts with an already-existing swatch and proof, so it does not exercise the empty-project-to-first-output problem.

Required design: distinguish intake facts and proposals, planned deliverables, materialized candidates, and adopted decisions. Support research/proof tasks before adoption. Separate inputs from expected outputs. Preserve the existing requirement that an adopted technical choice has applicable evidence, rather than demanding that all planning pretend to be completed research.

### R4. Completion cannot express the required acceptance

The profile's steps 8–9 require visual and destination checks where applicable. [graph.validate](../pixl/graph.py) lines 277–312 accepts done tasks when prerequisites are done and passing receipts bind the listed artifacts. It does not evaluate an explicit set of required mechanical, visual, continuity, or import criteria. Receipt mode describes how evidence was obtained; it does not specify what acceptance obligation it satisfies.

The probe successfully committed a local report task as done using one local receipt. That is legitimate for such a task, and illustrates why a global “require visual evidence for every task” rule would also be wrong. The missing concept is task-specific acceptance. Similarly, a shipped library POC has source/hash freshness but no machine-checked applicability to a new project's contract.

Required design: declare applicable acceptance requirements before evaluating candidates; bind each verdict to the candidate and contract revision; keep failed, unperformed, and unavailable checks distinct. A mechanically valid asset can remain visually rejected. A delivered candidate can retain an unresolved engine requirement. Passing a reference fixture must not automatically satisfy a production asset's obligations.

### R5. Remote intent, project state, and observation history are disconnected

[platform.prepare](../pixl/platform.py) lines 668–721 validates supplied arguments and schema, then returns an in-memory intent. [service.call](../pixl/service.py) lines 224–239 passes no project, task, contract, or store identity into that operation. [platform.job_update](../pixl/platform.py) returns an observation journal for the caller to persist. There is no supplied transaction that stores the journal and consistently projects it into a J record.

The UDL J check in [graph.py](../pixl/graph.py) lines 313–317 requires a remote ID for accepted states and some evidence for success. The probe accepts a succeeded synthetic J pointing to a receipt about other records, without a journal or binding to the job intent. The stateless journal has stronger history checks, but these are not enforced when J is written directly through the store.

Preparation also looks up the cached capability before validating the supplied schema and applies hard-coded rules afterward. Consequently, newly exposed tools or changed provider constraints can conflict with the stated live-schema precedence. This is a local implementation observation; no current provider inventory was fetched for this review.

Required design: persist intent before submission; connect task, contract, request, schema, journal, candidate, and receipts; reconcile uncertain submissions after restart without recreating paid work. Keep authentication and actual remote calls in the host. Resolve conflicts between dated semantic rules and observed capability explicitly, without bypassing validation or claiming the cache is live.

### R6. The skills describe a loop but do not yet define its operating contracts

The shared profile, common skill, and production reference repeat useful principles. The skill currently has one broad entrypoint and two references. It does not yet provide sufficiently concrete inputs, state changes, recovery instructions, and worked examples for intake, contract resolution, representative production, rejection/revision, family expansion, import, and cold resumption.

The end operation should determine the next skill boundaries. Each operation needs a trigger, required context, outputs, allowable side effects, failure behavior, and an observable stopping condition. Split content when that reduces irrelevant context or clarifies ownership; additional skill files alone are not progress.

### R7. Verification is concentrated on mechanisms rather than agent outcomes

The Python suite exercises language/runtime behavior, fixture calculations, packaging, and local MCP. Existing harness evidence establishes discovery and local calls, with limitations stated in [AGENT-KIT.md](AGENT-KIT.md). It does not establish reliable brief interpretation, method selection, artistic critique, useful revision, or autonomous recovery across Claude and Codex.

Required evaluation: exercise realistic briefs and pressure cases with retained prompt/profile/skill versions, actual tool observations, artifact identities, transcripts, and rubric results. Measure instruction following, grounded decisions, unresolved constraints, avoided duplicate submissions, visual findings, and resumption quality separately from syntax and token counts. New [profile scenarios](../evaluations/profile-scenarios.json) specify initial cases; their expected outcomes are not execution evidence.

### R8. Installation and packaging should serve the profile's operation

[pyproject.toml](../pyproject.toml) lines 10–20 lists type-checkers, linters, build tooling, and token measurement among mandatory runtime dependencies. [build_plugin.py](../scripts/build_plugin.py) copies that whole list into plugin requirements. Its manifest inventories copied runtime/resources, but not the active skill, agent definitions, launcher, or plugin manifests that also influence agent behavior.

Required correction: separate runtime needs from development/benchmark tooling and record the complete evaluated instruction/runtime bundle identity. Retain relocation checks. Tie evaluation results to the profile and skill revisions actually loaded, as well as the Python code. A `1.0.0` package label remains separate from product maturity.

## Development sequence and acceptance

The recommended direction is to mature the profile and skills through one complete representative operation, extending the runtime where that operation exposes missing semantics. A prompt-only rewrite would leave known state gaps; building a generic multi-profile platform first would expand architecture before its reusable contracts are proven.

| Order | Outcome | Work and acceptance |
| --- | --- | --- |
| 0 — this pass | Maintainers can identify the product, role, gaps, and next operation | Add the maintenance boundary, preserve the failing baseline and probes, record this review, and define initial behavioral scenarios. Runtime gaps remain open. |
| 1 | The current sources can be researched and reproduced | Repair the source inventory/range migration; fresh knowledge compilation, POCs, unit suite, plugin relocation, and wheel checks pass with explicit skips. No obsolete source substitution or historical receipt rewriting. |
| 2 | PIXL can take an empty project to a reviewable production plan | Specify one intake/style/sample skill operation; add versioned semantics for unresolved choices, ownership, planned outputs, adoption, and required acceptance. A missing output is valid planning state; an unresolved consequential contract blocks dependent generation with a precise reason. |
| 3 | One representative sample can be produced, rejected/revised, and resumed | Connect persistent intent and journal handling to task/contract state; use available real tools; inspect the retrieved candidate; retain rejection and accepted revision evidence. Restart after submission and after rejection without losing identity or duplicating work. |
| 4 | The approved sample can support a coherent asset family and usable delivery | Extend domain-specific skills for animation or tiles as the chosen task requires; verify family consistency, continuity, and required target import. Preserve explicit unavailable checks and change impact. |
| 5 | The same profile can demonstrate reliable behavior across hosts | Evaluate the exact packaged instructions in both harnesses, then compare repeated task outcomes and cold resumes. Extract shared profile/skill machinery from demonstrated needs; add more profiles only when their requirements are known. |

The first complete operation should use one representative asset from an explicitly supplied brief, with a stated delivery target and review criteria. Art dimensions, aesthetic, budget, target engine, and provider are inputs to that operation, not choices for this repository review to invent. A deterministic local fixture can develop and test the mechanics; it cannot substitute for the later real-art outcome.

## Scope of this review

This pass read the profile, skills and adapters, specification/registry, state and graph implementation, service and CLI boundaries, PixelLab preparation/journal logic, asset inspection, source/knowledge and packaging paths, tests, current research summaries, and representative supplied-source sections. It did not audit every embedded asset/demo in the large archive, refresh external service documentation, generate art, import into an engine, or run a controlled multi-model study.

The role-boundary edits are a concrete first correction. The roadmap describes outstanding development, not completed features or new normative UDL semantics. Passing checks for these edits must not be reported as repairing the 45 pre-existing test errors.

## Checks on this pass

- All three edited skill files passed the installed Codex skill validator. Claude's native validator accepted the portable plugin, repository agent directory, and repository skill directory: three checks passed.
- Relative file links in eight edited documentation/instruction files resolved, and the eleven evaluation scenarios parsed with unique IDs and required case fields. These are static checks, retained in [instruction-checks.json](../evidence/reviews/2026-09-11-scaffold/instruction-checks.json).
- A separate evaluator simulated four routing requests after the edits: two maintenance requests retained the development role; two asset/project requests selected PIXL. [routing-simulation.json](../evidence/reviews/2026-09-11-scaffold/routing-simulation.json) records the proposed responses, actions, and limitations. This was not a before/after model trial or execution of the full production scenarios.
- The local probe script passed Ruff, and `git diff --check` found no whitespace errors. The first YAML dependency probe failed in the project environment; the skill validator subsequently passed using an isolated `uv run --no-project --with pyyaml` environment.
- Running `scripts/verify.py` independently confirmed an immediate `FileNotFoundError` for the obsolete root `links.md`, before it could regenerate evidence. The original runtime, source documents, UDL semantics, generated bundle resources, and old proof receipts were not modified by this pass.
