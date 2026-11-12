# NF-08 — Visible asset lineage

Cycle: **IDENTIFY-2026-11-09-01**. Updated: **2026-11-11**. Status: **bounded complete; both native outcomes, final full verification, actual consumer regression and final-kit identity/compatibility pass**.

This bounded M3 increment makes the provenance of each delivered family member visible through existing job/artifact identities. It must distinguish generated seeds, provider edits, deterministic construction and reused assets without introducing another production ledger. The [finding](../../docs/IDENTIFIED.md#new-features-and-additions), [PLAN](../../PLAN.md#m3--source-allocation-through-useful-consumer-production), [ordered backlog](../../SHELVED.md#m3--source-allocation-through-useful-consumer-production) and [TODO](../../TODO.md) retain the active cycle and broader acceptance requirements.

## Retained authority and required distinctions

The [real queue-family production](../pixellab-family-production/README.md) is the source for these historical relationships. Its requests, provider identities, imported bytes, failed candidates and judgments remain evidence of that operation. The [origin identities](../pixellab-family-production/20261108/project/work/live-family/origin.json), [family snapshot](../pixellab-family-production/20261108/project/work/live-family/family-snapshot.json), [construction record](../pixellab-family-production/20261108/project/work/live-family/working-animation-motion-01-construction.json) and [integration checks](../pixellab-family-production/20261108/project/work/live-family/integration.json) retain the narrower identity and transformation boundaries.

| Delivered member | Existing lineage that the view must preserve |
| --- | --- |
| Working | A generated seed was reviewed and deterministically rotated through the official PixelLab workbench into the delivered four-frame strip. The final motion is specialist-constructed from that seed. The rejected animation-model output and subsequent background-repair attempt remain separate historical candidates. |
| Retry | The accepted static arrow came from the retained real generation. Its relationship to the delivered artifact must remain inspectable. |
| Paused | The transparent generation failed; an opaque generation retained the bars and a deterministic provider cutout removed the observed background. The delivered cutout retains the recorded generation/edit source chain; failed predecessors remain separate historical evidence, not inferred parent edges. |
| Ready | The reused controlled-fixture sample retains its prior provenance. Its old provider identifier and changed-contract diagnostic do not establish real generation for this continuation. |

The [original consumer handoff](../pixellab-family-production/20261108/project/CURRENT-HANDOFF.md) and prior [integration-change](../integration-change/README.md) and [consumer-execution](../consumer-execution/README.md) results remain separately scoped. Existing review, delivery and destination evidence does not become fresh acceptance merely because its lineage is displayed. Start remains the consumer's original SVG and is not relabelled as generated family output.

## Implemented read-only projection

The [runtime projection](../../pixl/asset_lineage.py) derives a bounded `lineage` view from existing artifact and durable-job identities. Rooted family reports expose it beside current members and historical snapshot files; `review-context` exposes candidate and delivered-member lineage; PLAR delivery reads and fresh handoffs expose nominated candidates and family-snapshot members. The [public contract](../../spec/family-delivery.md#visible-asset-lineage) and [common skill reference](../../plugins/pixl/skills/pixl/references/family-delivery.md#visible-asset-lineage) explain the same distinctions.

- `artifact.jobs` identifies direct importing jobs. Supporting `jobs` retain saved request intent, imported-artifact events, observations and exact journal locators.
- `source_requests` follows explicit provider-scoped request references. Missing, ambiguous and unresolved upload relationships remain explicit; a matched request reference is not proof that every imported pixel came from its named source.
- `same_bytes` records byte equivalence without selecting a source, parent or direction of reuse. `workflow_inputs` records task context without inferring pixel ancestry.
- Explicit simulation evidence remains visible, and `remote_verified` remains false: local file/journal consistency does not authenticate remote execution. Operation labels describe saved intent, not successful artistic outcomes.
- Limits and `truncated` disclose bounded expansion. Exact journal paths/JSON pointers preserve access to omitted evidence; existing caller `delivery_ref`/`resume_ref` locators retain larger reports.

The bounded view does not promise to expose every failed animation or transparent-Paused attempt as a parent edge. Those attempts remain separate retained historical evidence; absent relationships are not invented.

The projection adds no production ledger, state record, manifest/schema mutation, provider action, review or acceptance. Historical snapshots and handoffs retain their original bytes; a fresh read obtains the new view. Working's quarter-turn construction semantics remain in the separate historical construction report rather than an invented runtime ancestry edge.

## Local and distribution verification

The [final full verifier](../verification-runs/20261112T042106.397108Z/result.json) passes **973 tests plus one existing Windows symlink-privilege skip (974 run)**, **39 reference checks** and fresh wheel/copied-plugin probes. The [final verification summary](20261111/verification-final.json) binds that result, native grades and the frozen grader. Relative to TM-07's 920-test baseline, **54 tests** were added: 13 core lineage, six public-surface, five renderer-bridge and 30 case/grader tests. The final verifier includes the hardened grader and same-child continuation checks; local/source/distribution, native interpretation and actual consumer execution retain separate proof scopes.

The final bundle manifest SHA-256 is `a7e1f20eb46f69db2698310fc37175ad8605ef1d4530055f8c6784f6afd1931c`, with 198 manifest files and 200 complete-kit files. [Final-kit identity/compatibility](20261111/final-kit-compatibility-02.json) passes **7/7 checks** against the exact 200-file native archive. Runtime, profile, shared skills, contracts and renderer sources are byte-identical; only four generated reference files and the manifest differ. This is an identity/compatibility proof, not another native or rendered trial.

The [first compatibility audit](20261111/final-kit-compatibility.json) remains failed. Its wrapper used `measurements.json` instead of `measurement.json` and supplied a relative path to a verifier that requires an absolute root. Correcting the wrapper produced the separate passing receipt without changing product or package bytes.

The [pre-native full verifier](../verification-runs/20261112T034536.024204Z/result.json) passes **957 tests plus one Windows symlink-privilege skip (958 run)**, **39 reference checks** and fresh wheel/copied-plugin installation probes. The [verification summary](20261111/verification.json) binds the result and frozen grader source. The increase from TM-07's 920-test baseline is **38 tests**: 13 core lineage, six public-surface, 14 case/grader and five renderer-bridge regressions. That earlier result and its 38-test increase remain historical; the final 974-test run above adds the hardened grader cases. Native outcomes remain separate.

The native-frozen bundle manifest SHA-256 is `fa3ed36c63223c4307e03b5b7a9d821ee9f1b8ad4ecf48730f5ba2da7d7b7dfd`, with 198 manifest files and 200 complete-kit files. Both native trials and the mechanical consumer regression use this kit. The [200-file kit archive](20261111/native-kit-fa3ed36c.zip) and [snapshot identities](20261111/native-kit-snapshot.json) preserve its exact bytes before the final grader-only verification refresh.

The [first full-verifier failure](../verification-runs/20261112T033740.173952Z/result.json) remains: **949 passed, one failure, two errors and one skip (953 run)**. It exposed a compatibility defect in the renderer bridges: derived `lineage` in review-member rows was compared as though it were part of the immutable family manifest. Both the legacy PLAR and reusable queue-motion bridges now exclude only the explicit presentation fields `lineage` and `retained_path`; they still compare every immutable field and reject unknown extras. Five added regressions cover the correction; the focused bridge group passed 34 tests before the successful full rerun. State and manifest contracts did not change.

The earlier [preflight wrapper failure](20261111/preflight-family-01-error.json) attempted to parse empty successful `encode` output as JSON. The corrected wrapper's [13 public-family checks](20261111/preflight-family-02.json) pass without a product-source change; the failed attempt remains. Earlier implementation checks included 65 affected tests after correcting a stale caller-result assertion to resolve `delivery_ref`, plus [43 consumer-execution/destination regressions](20261111/consumer-regression.txt). These focused counts overlap the broader suite and are not additional independent totals.

The [actual public `consumer-execute` regression](20261111/consumer-regression/receipt.json) passes **9/9 checks** with the exact native-frozen kit. It consumes four enriched lineage members, executes the real isolated renderer, checks exact files/import and owned-process cleanup, and preserves all initial inputs without state writes or acceptance. Its [result](20261111/consumer-regression/result.json), [renderer checks](20261111/consumer-regression/check.json), [import result](20261111/consumer-regression/import-result.json), [review context](20261111/consumer-regression/review-context.json) and [observation bundle](20261111/consumer-regression/observations.zip) are retained. This is a mechanical operation regression, not a native model, visual-quality or acceptance result.

## Retained queue inspection and native continuation

A development read of the retained queue state checked these distinctions:

| Member/context | Observed projection and limit |
| --- | --- |
| Ready | A direct retained import exposes explicit controlled-fixture simulation evidence (`simulated: true`); its request/tool/provider ID does not convert it into authenticated real generation. |
| Working | The direct deterministic motion-edit request records 196 pixel patches and an explicit request reference to the earlier 193-pixel background repair. The generated seed is visible as workflow context, with unresolved upload evidence retained. The separate construction report supplies the quarter-turn meaning. |
| Paused | The 196-pixel cutout request resolves its explicit source reference to the opaque generation; the failed transparent attempt remains historical evidence. |
| Retry | The direct retained import exposes its generation request and observations. |
| Retained artistic-revision successors | Three successor members (Working, Retry and Paused) expose equal-byte candidates; Ready retains the same candidate. The equivalences create no new direct importing job and prove no directed reuse relationship. |

## Native caller outcomes

[Codex passes 42/42 independent checks](20261111/codex-01/grade-04.json) in its original process with the same named child. [Claude passes 45/45](20261111/claude-01/grade-02.json) using its original evidence plus a verified same-parent/same-child continuation. Both load the shared profile/skill and lineage reference, read the original and reused families through public surfaces, distinguish direct imports/request references/context/equivalence and Ready's controlled fixture, retrieve separate construction evidence, and deliver specialist/caller reports without new provider work or acceptance.

Codex's [first 35/42 grade](20261111/codex-01/grade-01.json) remains. Its failed checks reflected proof-adapter gaps: six actual public CLI reads ran through one exact inline fixture loop, and a complete earlier source read preceded a later distinct failed read. Narrow AST/dataflow and full-byte source-read checks now recognize those recorded operations with negative tests. The original evidence is regraded; no native rerun is substituted, and raw command/tool errors remain retained.

Claude's [first 0/1 grade](20261111/claude-01/grade-01.json) remains an incomplete outcome: its parent exited zero after saying it was waiting, the host stopped the background child, and comparison/specialist/caller report files were absent. The [continuation](20261111/claude-01-resume-01/continuation.json) resumes the same parent and child; native SendMessage acknowledgement, task-start and completion notifications bind the continued work. The continued child transcript retains the original transcript as an exact byte prefix, and all 14 original report-file hashes remain preserved. No replacement child is used. TaskOutput remained unavailable despite the launch tool list; that error is retained with the successful SendMessage route.

Four earlier Claude PLAR calls included unsupported `result_path` arguments and correctly failed input-schema validation. Actual public CLI fallback succeeded; these are caller argument errors, not server response-size failures. Source-kit files, production history and every initial inventoried byte remain unchanged. The existing baseline policy excludes generated interpreter caches: 22 new `__pycache__/*.pyc` files are disclosed separately rather than claimed absent. [Preservation](20261111/claude-01-resume-01/preservation.json) and the final grade retain those scope boundaries.

The [frozen grader-04 provenance](20261111/grader-source-04-provenance.json) binds both final grades, case/test source snapshots and **30 passing focused case/grader tests**. Its grader SHA-256 is `9461fe0c21c87ed3d896837f7abdff98834c799b5c0a2561d4929ec40b99ea01`. The final full verifier and separate seven-check identity/compatibility proof now pass after these grader-only changes. The earlier full result and native-frozen kit remain unchanged. No new provider call, art production, visual acceptance or broad host reliability is claimed.

## Required A–E review

**A — How can this improve?** Make delivered-member origins directly inspectable from existing identities so a caller can follow the seed, edit, construction or reuse chain without reconstructing it from prose. The shared public projection now exposes those existing identities with explicit unknowns and bounded exact-detail access; local preservation, public surfaces, distribution, actual consumer execution and both native caller outcomes now pass within their scopes. The final full verification and separate kit-identity proof also pass.

**B — Host compatibility?** Preserve the shared runtime/skill boundary and existing Claude/Codex consumer routes. Shared family/review/PLAR surfaces, the existing compact-result locator route and common guidance are implemented. The full suite, fresh wheel/copied-plugin probes and actual public consumer regression pass. NF-08 now passes Codex 42/42 and Claude 45/45 with the frozen native kit. Claude required explicit same-parent/same-child recovery after the host stopped its background child; the retained failure limits broader reliability claims. The final full verification and separate kit-identity proof also pass.

**C — Contextual and artistic quality?** The retained queue projection distinguishes deterministic Working edit intent and explicit Ready simulation evidence; the separate construction report retains the specialist's correction of failed generated motion. Provenance can explain an artistic decision but cannot establish current acceptance or consistent quality by itself. No new art or visual judgment is claimed.

**D — Can another project use and resume it?** The implemented report derives from existing production records and exact artifact identities available to the consuming project, with explicit unresolved references, equivalence and workflow-context limits. The existing isolated consumer passes the nine-check native-kit mechanical regression with enriched lineage and unchanged inputs. Both native callers interpret the retained lineage, and Claude continues the same parent/child with exact predecessor evidence preserved. Arbitrary-project coverage and broader long-gap reliability remain open.

**E — Where are responsibilities represented?** The profile retains artistic judgment; the common skills explain how to read and use provenance; runtime/MCP derive and expose existing relationships; official PixelLab remains responsible for actual generation/editing. This evidence report records development verification and does not replace consumer production state.

## Continuation

NF-08 is complete as this bounded lineage slice. Next, pull **CF-10** useful complete native production from [SHELVED](../../SHELVED.md#m3--source-allocation-through-useful-consumer-production). **M1/M2 and broader M3 remain open**, along with broader generated quality, host reliability and the unrelated incomplete Claude QOL-10 caller-result continuation. Continue the current PLAN rather than starting another IDENTIFY audit.
