# Candidate and family review authoring, version 1

This adapter publishes explicit specialist judgments through existing PX2 X/E/V
records and task completion. It adds no UDL fields or automatic artistic judgment.
It supports saved raster candidates and saved family manifest candidates equally.
The existing inspection-packet operation and its view-coverage rules are unchanged.
Use that operation for prepared-packet viewing; use this operation for actual
project observations such as recorded playback, collective views and renderer reports.

## Read the exact review target

`review-context STATE CANDIDATE --root ROOT` / `pixl_review_context` returns current
canonical `state_hash`, semantic `binding_hash`, candidate file SHA-256, owning
task/output, literal criteria and their current verdict IDs, nomination and task
status. Family context also identifies the immutable manifest and retained members;
its `snapshot_acceptance` describes creation, while `current_acceptance` describes
the current criteria and task. Neither is an inferred aesthetic judgment.

## Publish one explicit review

`candidate-review STORE CANDIDATE REVIEW_ID REVIEW_JSON --expect STATE_HASH --root ROOT`
and `pixl_candidate_review` use the same closed JSON observation:

```json
{
  "version": 1,
  "binding_hash": "FROM_REVIEW_CONTEXT",
  "reviewer": "EXISTING_ACTOR_ID",
  "observed_at": "2026-11-09T16:00:00+00:00",
  "observations": [
    {"path":"work/playback.png","sha256":"ACTUAL_FILE_HASH","mode":"visual","note":"What the reviewer actually saw, including scale and sequence scope."},
    {"path":"work/render.json","sha256":"ACTUAL_FILE_HASH","mode":"live","note":"What the actual destination execution established."}
  ],
  "verdicts": [
    {"criterion":"CURRENT_Q_ID","status":"pass","reason":"Judgment against the literal check.","supersedes":null,"observations":[0]}
  ],
  "action": "record",
  "next_action": "Review the remaining destination criterion.",
  "limitations": []
}
```

`observed_at` is a caller-declared timezone-aware observation time no later than
recording; it is not generated viewing history. Each performed verdict references
one or more distinct observations of its required evidence mode (`local`, `visual`
or `live`). Unavailable verdicts have no observation indices and create no E.
Each supplied criterion must belong to this output. `supersedes` names its exact
current V or is null when none exists. Omitted criteria retain their current state.
Reasons, observations, next action and limitations remain specialist-authored.
An evidence file or schema alone cannot establish that the observation occurred.

`action` is explicit: `record` retains judgments; `nominate` also selects this
candidate for its output, preserving other output selections; `complete` also
performs the existing task-completion checks/transitions. Completion needs every
output nominated and every required criterion passing, current allocation,
activation prerequisites and resolved pending jobs. A failed/unavailable review
is retained with record/nominate; asking to complete it fails before publication.
Already-done work must be explicitly reopened before a new review.

The current canonical state hash protects publication. The semantic binding hash
protects the candidate, output/criteria and their complete semantic dependencies
even if a caller refreshes the state hash after a contract change. File SHA-256
values protect the observations. The adapter derives E scope, IDs and record
bindings; callers do not construct records or calculate a canonical state digest.

## Retention, retries and limits

Files are captured and copied under `STORE/reviews/<report-sha256>/`; the canonical
report contains the request, original paths, retained identities and source state.
Auxiliary X records bind retained files, and E binds the report plus candidate/Q
semantic scope. Report/file IDs are derived from REVIEW_ID. No supplied source
or previous evidence is overwritten. Maximum 64 observations, 64 MiB per file,
256 MiB aggregate and 1,024 declared verdicts; reports retain the codec size limit.

The operation holds the store lock, checks the complete review/nomination/completion
sequence before publishing, then saves ordinary revisions. An interruption may
leave immutable unreferenced files or a retained review before completion. Reload
the current state hash and repeat the **same REVIEW_ID and observation** to finish;
existing review/verdict IDs are reused. Changed payloads, stale bindings or
superseded reviews cannot be replayed as new acceptance. A retry never submits a
provider job. Changing the review requires a new ID and explicit supersession.

Results expose `state_hash` (canonical state), `review_sha256` (report file), current
criteria/nomination/task status and publication steps. Immutable snapshot creation
status stays separate from current acceptance. The report does not attest reviewer
identity, actual viewing or renderer honesty; retained host/runner evidence supplies
those observations. Generic source amendment and historical supersession retain
their existing PX2 semantics.

## Save results directly

Use CLI `--result-path work/review-result.json` or MCP `result_path` to save the
complete result without transcribing JSON, Windows paths or hashes. The option is
available for context, request-review, review-context, candidate-review, family,
family-snapshot and PLAR handoff. The path is relative to the explicit consumer
root and must be fresh; an existing destination is rejected before the operation.
The response contains `result_saved`, the path, file SHA-256, byte count and key
status fields. Read the saved file for complete criteria and publication details.
CLI full wire context remains PX text; other listed exports contain JSON.

If writing fails after an operation publishes, the response has
`result_saved:false` and includes the actual `operation_result` (and `wire_result`
for wire context). CLI returns a nonzero exit code. Reconcile that result with
current state before retrying; a failed file export does not undo publication.
Use a fresh path and the operation's existing retry rules. Default output without
this option is unchanged; exports do not alter the saved-state format.
