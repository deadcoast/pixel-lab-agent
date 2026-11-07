# Approved sample through family delivery

Use this operation when extending a reviewed representative sample into related assets, comparing their continuity, retaining a delivery package, or resuming an existing family. It governs PIXL production. A developer maintaining these instructions remains in the development role.

## Start with the actual saved family

Read the [PX2 specification](../../../resources/spec/PIXL-2.md) and [registry](../../../runtime/pixl/registry-v2.json), including their family extension. Discover the installed runner's help or MCP schemas before using the operations below. Existing PX1 and older PX2 projects retain their declared semantics; do not manufacture a migration by relabeling their headers.

Gather the brief and sources, target use, actual sample bytes and verdicts, confirmed style choices, applicable adoption decisions and proofs, member inventory, destination choices, and authorized provider scope. Read `workflow STATE --root ROOT`, `family STATE [OUTPUT] --root ROOT`, and `jobs STATE --root ROOT` before extending or retrying existing work. `family` verifies retained files and reports current selection, requirements, pending jobs and historical snapshot drift. It changes no state.

Open the exact nominated sample X and its retained observations. Confirm its sample task is done and that its passing verdicts answer the family-relevant question. A replaced or rejected candidate cannot serve as the approved baseline merely because its old PNG remains. A sample that demonstrated a front idle pose does not establish all-direction walk contacts or diagonal tile seams; use the [sample operation](intake-sample.md) to exercise that uncertainty before scaling it.

## Save the members and collective requirements first

Use the normal decode/edit/encode/validate/expected-hash commit sequence. Record only fields defined in the current specification. Before files exist, save F plans rather than invented X identities.

1. Each production F names the exact sample candidate through `bs`. Its producer T lists that X in `ip` and the sample T directly in `dp`. Retain the applicable contract, confirmed choices, adoption D and executed proof; the baseline link does not replace those requirements.
2. Make a delivery T and a report-kind F. Set this F's `bs` to the same sample, `mb` to the distinct ordered member F IDs, and `ds` to the same project's destination I choices. The sample output itself may be a member. Other members must be production outputs with the same baseline. List every producer as a direct prerequisite of the delivery T and the baseline X as its input. A family cannot contain itself or another family delivery.
3. Define member Q criteria and separate collective Q criteria before results. The family needs a continuity criterion with an observable condition and appropriate evidence mode. State the actual comparison: for example, consistent equipment placement across the requested directions, grounded feet across the cycle, or matching shared boundaries across the required tile transitions. Add engine criteria when required by this destination; a target name alone does not create an engine verdict.
4. Save destination choices with their sources, owner and rationale: target project and version, intended paths/names, slicing or tile mapping, pivots, timing, sampling, scale, alpha or atlas rules as applicable. Missing choices remain unresolved; observed/proposed values remain distinct from confirmation. Such choices block delivery activation/completion, while useful member files can still be retained.

Commit this plan before collecting verdicts. Keep the project's actual dimensions, style and acceptance conditions; example values are not defaults. `ready` and `workflow` apply activation blockers. Retaining a package has narrower prerequisites and does not grant production adoption or delivery acceptance.

## Produce members, compare them, and preserve rejection

Run the [provider recovery operation](provider-recovery.md) for each required real generation attempt. It saves the exact request before dispatch and imports actual downloaded bytes as an unaccepted candidate. Read the family report as well as jobs: a member or baseline attempt may be outside the delivery task's forward context packet. For `prepared`, `unknown`, `submitted` or `running` work, resolve the reported action before another attempt or snapshot. An unknown attempt requires the saved request/history and actual provider reconciliation; missing service access leaves that attempt unknown. Do not invent a job ID or infer that a request was never received.

Evaluate each member against its own requirements and approved baseline. Keep mechanical measurements, visual observations, temporal or neighborhood comparisons, and engine results separate. A contact sheet is useful comparison evidence, but the actual task determines the required additional inspection:

| Family | Inspection to perform and retain |
| --- | --- |
| Static sprites or variants | Compare actual members and baseline at native scale and enlarged scale; inspect silhouette, volume, equipment landmarks, palette/ramp use, lighting and edge treatment against this project's contract. |
| Animation or directions | Play the actual sequence at its intended timing, including loop boundaries and required direction changes. Inspect contact poses and individual frames for anchor drift, sliding, volume changes and direction mapping. Save which files/frames, playback timing, context and observed defect or pass condition support the verdict. |
| Tiles or transitions | Assemble repeated neighborhoods using the actual members, including the edges, corners, diagonals and material transitions this game requires. Inspect seams, repeat visibility and projection in those arrangements. Retain the arrangement/mapping and images or observations identifying the compared files. |

A dimension or palette check cannot supply these visual judgments. If playback, neighborhood assembly or visual access is unavailable, retain that precise boundary and leave its criterion unavailable/unperformed. Do not write a passing visual receipt for an unseen artifact. When an inspection fails, retain X/E/V and its actual defect, create a revised X at a new path, inspect the revision, and nominate it only with its own current evidence. A successful generation request does not answer the member's acceptance criteria.

## Retain and review the exact delivery

When the baseline is still eligible and every planned member has a nominee on a done task, inspect the family report for pending jobs and blockers. The delivery task must be open or active for retention. Invoke:

```text
family-snapshot STORE OUTPUT CANDIDATE --expect HASH --root ROOT
family STATE OUTPUT --root ROOT
```

MCP equivalents are `pixl_family_snapshot` with `store`, `output_id`, `candidate_id`, `expect`, and `pixl_family` with `path` and optional `output`. The server supplies the project root. Reload and reconcile after a stale-hash error; do not overwrite state or repeat remote generation.

Snapshot retains actual member copies and a canonical manifest under the store's content-addressed `deliveries/` directory, then publishes a new manifest X with its exact constituent references. Its `accepted: false` means retention created no nomination, verdict or task completion. `remote_executed: false` describes this local operation. Read the resulting manifest and report, verify member order and copied-file identities, and use the copied files for collective review and destination testing. A successful copy does not demonstrate continuity.

Nominate the intended manifest candidate through the normal saved-state operation. Evaluate each collective Q against this exact manifest, baseline, copied members, destination choices and current plan. Retain actual observation files, then bind E/V to the full candidate/criterion semantic scope. Save a continuity failure independently from per-member passes. Revise the implicated member and repeat its checks, then take a new snapshot; preserve the rejected family candidate and observations.

Published manifest candidates and their constituent X identities are immutable. Member selection, baseline, membership or destination changes leave old packages intact. Reopen affected completed work and supersede stale verdicts/receipts, save the changed plan, and evaluate a new snapshot. The report identifies drift; recomputing an old receipt hash cannot make a historical package current.

## Destination boundary and cold handoff

Use the target engine and the retained files to exercise the applicable import behavior: frame slicing and order, pivots/contact alignment, timing and loop transitions, direction mapping, texture sampling/display scale, alpha/atlas edges, tile neighbor mapping, or required material/lighting behavior. Record the actual engine/project version, files tested, settings and observed outcome. Metadata inspection alone does not establish engine acceptance.

If the engine or target project is unavailable, still deliver links to the retained manifest and useful files. Record an unavailable V with `ev=[]` and the precise missing capability; keep delivery unfinished. Leave the concrete next action, such as importing the named copied sheet into the specified target scene, applying the saved slice/pivot/timing settings, and playing the listed loop and direction transitions. State that destination acceptance is unverified. Do not turn missing engine access into a visual rejection or a fabricated live receipt.

Commit a handoff containing the state path and observed revision/hash, family output and manifest candidate, package and copied-file locations, baseline and selected member IDs, relevant failed/unavailable verdicts, pending job IDs and last observed states, and the next task with its required context and action. An N record can point to the retained records/tasks; retain the human-readable instructions in project evidence as needed.

A cold session starts with `family`, `workflow` and `jobs` against that root, then retrieves focused `context` and opens the cited artifacts and observations. Reconcile unknown jobs first, review reported plan/selection drift before new evaluation, and execute only the outstanding check or revision. Mark the delivery T done only after every declared criterion on its current nominee passes and prerequisites are done. Finish with the useful files, actual verification, unresolved limits and actionable handoff, without claiming art quality or engine readiness from local fixtures.
