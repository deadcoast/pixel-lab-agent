# Exact request and criterion review evidence

`request-review PACKET --root ROOT [--asset ID] [--plar PATH]` and
`pixl_request_review({packet, asset_id?, path?})` expose the same read-only report.
They resolve the existing version-1 request-review packet and candidate-plan JSON.
They do not write a caller review, classify semantic consistency, or authorize a
provider call. The [skill procedure](../plugins/pixl/skills/pixl/references/request-review.md)
assigns the actual comparison to the calling agent.

The report verifies request/criteria byte hashes and returns their exact arguments,
criterion checks, stated bases/authority/scopes, candidate controls and packet choices.
All packet source identities are checked, including references not cited by criteria.
An optional request.connection path/hash binds the exact connection artifact, and
request.provider binds its provider name. Reports verify the artifact identity; new
preparation requires the supplied connection to equal the reviewed one. Existing
packets without these optional assertions keep their previous preparation contract.
Criterion source references produce file-local excerpts or explicit diagnostics for
changed, unavailable, binary, invalid, unresolved or excessively broad locations.
`consistent` remains null and `caller_comparison` remains unperformed. A valid source
range does not show that the requirement entails the authored rejection condition.

Candidate criteria may add `authority` (requirement, proposal, observation, unknown).
A text source pointer may add `lines: [first,last]`, with one-based inclusive integer
bounds, alongside its existing path/locator. Explicit bounds are validated before new
preparation. These optional additions preserve earlier plans and immutable history;
older closed-schema writers do not support authoring the additional fields.

Legacy prose using `line N` or `lines N-M` receives range diagnostics. Other locator
forms remain explicitly unresolved; they are not silently interpreted as verified.
Binary references require actual host inspection. Each source excerpt is bounded;
overlarge ranges return a request to narrow them rather than truncated evidence.
Report reads and preparation honor the same confined consumer paths.

Supplying an asset ID also compares the packet's selected requirements identity and
includes current production. The focused production `continuation` contains the exact
state hash, current task, provider/remote job identities with original discovery,
immediate action, prerequisites before another request, and outcome-dependent next
steps. Pending jobs require their original connection's observation/reconciliation.
Succeeded results lead to retrieval/import or candidate review before a correction
is proposed; actual unavailability can be recorded. A done task leads to delivery
review. Missing or stale selection remains explicit.

These are derived workflow instructions, not additional automatic approval rules.
The existing `new_request_allowed` field remains the local selection/pending advisory;
it does not mean the result was reviewed or another request is needed. Carry the
continuation into the caller result and reread after observations/state changes.
The report neither transfers a simulated job to a live service nor treats source-path
integration as renderer or artistic acceptance.
