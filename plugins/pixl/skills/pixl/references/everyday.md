# Everyday asset production

Use this path for an assigned asset or family. PIXL supplies visual expertise through
the host model; the caller supplies the assignment and project authority. The local
runtime preserves requirements, attempts and reviews. Official PixelLab tools do
the generation. Start at the project's current step, keeping its existing choices,
authorization and unfinished attempts.

## 1. Locate the assignment and select its asset

Read the caller's brief, actual consumers/backend states and available reference
images. Use [PLAR](../../plar/SKILL.md) to allocate missing/reusable assets when that
inventory is needed. If a queue already exists, use the path the caller selected:
different queue files can retain different generations of the same asset.

This running example is the existing queue successor: `authoring-plar.txt`, asset
`queue.working`. Its older `plar.txt` remains historical production context. In
another project substitute its actual queue and asset; these names and its 16px
cells are not universal requirements.

From the consumer directory, select its Python and the complete installed plugin:

```powershell
$Project = (Resolve-Path ".").Path
$Python = "C:/path/to/selected/python.exe"
$Runner = "C:/path/to/installed/pixl/scripts/pixl.py"
function pixl { & $Python $Runner @args }
$Queue = "authoring-plar.txt"
$Asset = "queue.working"
$Selected = pixl plar read --path $Queue --asset $Asset --root $Project | ConvertFrom-Json
```

Set the two executable paths to the installation in use. Neither is relative to
the production store. For local MCP, the server's configured root is `$Project`;
the corresponding read is `pixl_plar_read` with
`{"path":"authoring-plar.txt","asset_id":"queue.working"}`.
See [identities and paths](identities-and-paths.md) for exact root and hash rules.

## 2. Resume the actual production step

Read selected requirements, source changes, reference roles, unresolved questions
and `production.continuation`. If there is no production link, continue at step 3.
Otherwise derive the store from that continuation, not from the asset's name:

```powershell
$Store = $Selected.production.continuation.store
$StoreFolder = Join-Path $Project $Store
$State = "$Store/state.px"
$StateFile = Join-Path $Project $State
pixl workflow $StateFile --root $Project
pixl jobs $StateFile --root $Project
```

Follow current pending/unknown job observations before another submission. A
delivered continuation means consume the accepted result unless a new requirement
actually calls for revision. A new requirement must have an explicit successor;
old acceptance does not close it. Existing unsupported or unavailable observations
remain visible. Use the [provider recovery procedure](provider-recovery.md) for
uncertain submission or retrieval, and [source retention](library-retention.md)
when a package update exposes missing old source bytes.

## 3. Make the first request or extend the family

For one selected asset, [PLAR preparation](../../plar/references/prepare.md) takes
ordinary JSON: sourced candidate controls, exact review criteria and a provider
request. The caller compares the literal packet against the original brief,
references and code through [request-review](request-review.md). Keep measured
facts, caller decisions and expert design proposals distinct. Carry useful pixel
art judgment into prompts and criteria without turning sample recipes into owner
requirements.

For an adopted baseline and related stages, use the [connected plan contract](../../../resources/spec/production-plan.md):
`production-plan` saves the reviewed stages and `stage-prepare` binds the exact
accepted upstream inputs to a request. These public operations construct the
records. For a delivery composed of accepted existing outputs, a plan with
`stages: []` binds those outputs without creating a generation stage. Reuse
accepted existing art when it satisfies the assigned successor;
do not mislabel reused bytes as generated under that successor.

For this retained successor, orientation is:

```powershell
pixl context $StateFile provenance-correction.plan --view authoring --root $Project --result-path work/current-authoring.json
pixl request-review $State --plan provenance-correction.plan --against-plan authoring-01.plan --view changes --root $Project --result-path work/current-changes.json
```

Use fresh output names. Follow indexed intake when applicable and both full-report
retrievals for literal comparison; the concise view cannot decide consistency.
For another project use plan IDs from its saved context. This explicit pair need
not be directly consecutive.

## 4. Generate through official PixelLab

Use the current [official platform docs](https://www.pixellab.ai/docs),
[MCP tool overview](https://api.pixellab.ai/mcp/docs), and the actual connected
declaration for the operation. Match reference roles to supported image inputs or
handles; a local filename in prose does not supply its pixels. The host makes the
paid official call under the assignment's established scope and authorization.
See [operation selection](pixellab-operations.md) for capability-specific choices.

The local sequence is `job-prepare` (or the preparation from step 3), then
`job-dispatch`. Dispatch returns the exact call for the host and claims this attempt.
Use the observed provider result with `job-observe`; use the provider's actual
status/retrieval tool until the result is available. Download actual returned bytes
and use `job-import` for the saved output. Refresh the canonical state hash before
each publication. The [provider procedure](provider-recovery.md) defines arguments
and unknown-outcome recovery; a local claim or elapsed time is not remote success.

## 5. Review the candidate and complete its task

Read `review-context` / `pixl_review_context` for the exact candidate, current
criteria, binding hash and canonical state hash. Inspect the real file at native
and appropriate enlarged scales, measure its applicable constraints, and exercise
its actual consumer. Animation needs temporal viewing; tiles need neighborhoods.
Keep those observations separate from the mechanical measurements.

Use [candidate-review](../../../resources/spec/candidate-review.md) with an ordinary
observation JSON: reviewer, actual observation time, evidence files, explicit
criterion judgments and `action` (`record`, `nominate` or `complete`). It derives
evidence bindings and preserves failures and superseded verdicts. Supply the
context's `binding_hash` inside the observation and its current `state_hash` as
`expect`. Missing viewing produces an unavailable judgment, not a pass. Prepared
inspection packets retain their [own view-coverage workflow](inspection.md).

After an interrupted review, reload current state and repeat the same review ID
and observation to finish recovery. Changing the observation requires a new review
ID and explicit supersession. An already accepted review can be retried without
new publication; this does not establish a new observation.

## 6. Review the family, integrate and return usable files

Use `family` for exact baseline/member/destination context. `family-snapshot`
retains the selected package as a candidate; its creation-time `accepted:false`
does not describe later acceptance. Review its actual collective appearance and
destination through the same `review-context` and `candidate-review` operations.
Nominate/complete only after the applicable criteria pass. Follow
[family delivery](family-delivery.md) for member selection and integration.

Reread the selected queue before returning. Save the expert summary, useful file
locators, provenance, findings, limits and caller actions through `plar handoff` /
`pixl_plar_handoff`. Choose CLI `--view caller` or MCP `view: "caller"` for the
[compact caller result](../../../resources/spec/caller-result.md); omitting it
keeps the existing receipt. Put the bounded ordinary summary in `details.caller`,
and retain the full observations in other details fields and referenced reports. Its two inputs come from the same fresh focused PLAR read:
`requirements_hash` and `production.continuation.state_hash` for `expect`.
The queue's top-level `hash` is only for queue saves. Return the caller view with
its exact handoff locator, actual deliverables and remaining decisions. Assignment
status and integration findings remain your claims; current production facts and
the immediate next action come from the runtime. Detailed checks remain exactly
retrievable, and a referenced resume must be read in full before acting.
The next agent rereads current state rather than blindly executing an old snapshot.

The stop condition is the assignment's useful delivered outcome or a precise
remaining dependency with preserved work. A valid request, journal or package
alone does not establish visual quality or destination acceptance.
