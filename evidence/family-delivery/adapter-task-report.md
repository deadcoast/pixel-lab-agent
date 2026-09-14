# Family adapter and skill development record

This record concerns repository development. No production profile activation, real PixelLab call, artistic acceptance or target-engine execution occurred here. Existing user authorization covered this work; no remote action is part of either new operation.

## Initial observed failures

Command, using the selected project environment:

```powershell
.venv/Scripts/python.exe -m unittest tests.test_family_operations -v
```

The first run contained four tests and failed all four assertions. The CLI rejected `family` and `family-snapshot` as unknown commands. MCP discovery omitted both family tools and their mutability metadata. The confinement call returned `unknown_tool` before the intended project-path boundary could be exercised. The complete output is retained in [adapters-initial-red.txt](adapters-initial-red.txt); these are missing-interface failures, not successful confinement checks.

## Implementation and authored workflow

Added CLI `family STATE [OUTPUT] --root ROOT` and `family-snapshot STORE OUTPUT CANDIDATE --expect HASH [--root ROOT]`. Added service `family_report(path, root, output_id=None)` and MCP `pixl_family {path, output?}` / `pixl_family_snapshot {store, output_id, candidate_id, expect}`. MCP reports the snapshot as a local mutation and the report as read-only. Neither tool advertises open-world effects. Snapshot `accepted: false` remains a successful local operation, with acceptance evaluated separately.

Added the common family reference and routed the profile, main skill, production, intake/sample and runtime references to it. Its planned operation covers exact sample/member/destination binding, previously saved criteria, actual animation playback or tile neighborhood review, revision after independent continuity rejection, unknown job reconciliation, exact retained member copies, and concrete unavailable-engine handoff.

Before editing, the original profile and affected skill/reference bytes were retained in [adapter-skill-before](adapter-skill-before/identities.json), with SHA256 identities. Reading those instructions identified the missing family operation, but was not a behavioral baseline trial. Authoring used the writing-skills guidance; this milestone does not claim a controlled before/after agent benchmark. Discovery/format, bounded scenario behavior and actual task outcome evidence are reported separately below.

## Intermediate validation

`.venv/Scripts/python.exe -m pixl --help` listed both new CLI commands after routing implementation. Ruff lint passed for the three runtime adapter files and new operation tests. `ruff format --check` identified formatting in the newly added CLI/test sections; that finding was a formatting check, not a runtime failure. API-dependent execution was deferred while the delivery module and family fixture were being implemented by the coordinating agents.

## Final verification and limits

After the dependent modules arrived, the original four interface checks passed in [adapters-routing-green.txt](adapters-routing-green.txt). The expanded nine-test subprocess suite passed in [adapters-integration-green.txt](adapters-integration-green.txt). It verifies real retained member copies, no automatic nomination/verdict/completion, successful CLI exit despite `accepted: false`, explicit project root, MCP mutability/schema/confinement, cold unknown-member recovery and snapshot blocking, unavailable-engine completion rejection, stale publication and actual copied-file corruption.

Two unsuccessful integration attempts remain retained. [Attempt 1](adapters-integration-attempt1.txt) hit the existing open-to-done transition guard before the intended acceptance assertion. [Attempt 2](adapters-integration-attempt2.txt) reached completion validation, where the still-unperformed continuity criterion preceded the unavailable engine check. The fixture was corrected to activate the task and record an explicitly synthetic continuity pass so the final test isolates the unavailable engine guard. No production behavior was changed to satisfy either incorrect fixture expectation; the final rejection identifies `q.delivery.engine is unavailable`.

Existing MCP, provider-job and intake operation tests also passed: 16 tests in [adapters-regression-green.txt](adapters-regression-green.txt), run with `.venv/Scripts/python.exe -m unittest tests.test_mcp tests.test_job_operations tests.test_intake_operations -v`. Ruff lint and format checks pass for the three adapter runtime files and family tests. A static reference check resolved all 38 local links in the common skill and its references, with no missing targets. These checks establish discovery/format and implemented local behavior, not profile compliance or artistic outcomes.

A source-adapter scripted walkthrough was executed using `.venv/Scripts/python.exe evidence/family-delivery/adapter-scenario.py`. Its two retained cases are [record.json](adapter-scenario/record.json), [handoff](adapter-scenario/handoff.md), copied instruction bytes and full project histories. It passed the unknown-member and unavailable-engine paths already covered by the adapter tests. The command completed just before the coordinator's request to defer the separate plugin evaluation. It is preserved as local adapter evidence only: no retrospective baseline, isolated-plugin verification, independent profile-compliance claim, actual art inspection or engine execution is inferred from it.

After the coordinator supplied the final bundle identity, `.venv/Scripts/python.exe evidence/family-delivery/plugin-scenario.py` passed on its first execution. The separate [plugin record](plugin-scenario/record.json) retains 49 process invocations (43 CLI, six MCP), their actual command lines/stdin/stdout/stderr, and a separate runtime-origin check. Every runtime invocation used the relocated copied plugin with `-I -S` and explicit dependency site-packages only. All 90 bundle entries matched both copied bytes and the final source bytes. The script, isolated bootstrap, fixture builder, instructions and runtime identities are retained, and the executed script/runner hashes were independently rechecked after completion.

The scenario starts with explicitly synthetic saved sample/member acceptance, retains an unknown local dispatch claim across restarted reports, and preserves the expected blocked snapshot error. An explicitly fictional failed observation settles that simulated request. The existing accepted member is restored without a new provider call. The first two-member package is retained before a saved membership amendment, and its manifest plus both copied member files remain byte-identical afterward. The old package is reported stale; the new package contains the selected single member. The final revision is 17 with delivery open, collective continuity **unperformed**, destination engine **unavailable**, and no pending job. An N record and [concrete handoff](plugin-scenario/handoff.md) identify the state, current package, useful copied file and outstanding review/import work. The scenario uses static sprite fixtures; animation playback and tile-neighborhood behavior were not exercised.

Identities:

- Final bundle manifest: `2c21250554a42804453ed3ea58810b08fd19b6b1fa08b5f0f3b886e14c3837d1`.
- Plugin scenario record: `03a728a2df24f507cff3d44387de5392d1cd258540e33ab1ba5c5273ce7d5604`.
- Final scenario state: `761f30dd16354831e9c99fa20c942bbb9f49642e820e41125e6051bc1f93a2db`.

This is a bounded scripted operation walkthrough inspected against the authored instructions, not an independent model-following evaluation or a controlled before/after benchmark. Actual useful outcomes are retained fixture files, immutable snapshot history and a resumable local boundary. No real PixelLab, production art-quality acceptance or target-engine execution is established. No bundle generation, installation, packaging change or commit was performed by this adapter task.
