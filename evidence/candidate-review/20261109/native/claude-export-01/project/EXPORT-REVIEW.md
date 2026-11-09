# Verify the exact report export and retain the completed caller review

The preceding native caller completed its 20-criterion comparison and obtained
specialist r2 corrections; CRITERIA-RESULT.json records that outcome. This task is
the exact export/continuity check, not another drafting or production assignment.

Use the current installed kit's request-review guidance. Call pixl_request_review
with packet .pixl/assets/queue.ready/state.px, plan authoring-01.plan and job
authoring-01.working.join-01. Save its raw result as exact bytes under a NEW work
directory; if the host spills the result, copy that file as bytes. Parse generated
JSON explicitly as UTF-8 and compare any formatted copy to its raw parsed value.

The earlier work/criteria-review-01/request-review-raw.txt is intact UTF-8. The
earlier formatted request-review.json was decoded with the Windows default and
altered non-ASCII characters in request.request.discovery.evidence.declaration_text.
Retain both files and describe the observed difference rather than repairing them.
Compare the fresh parsed report against that exact earlier RAW report. The kit now
excludes job lifecycle observations from review_scope_sha256 so progress alone
does not invalidate unchanged semantic review; current state/blockers remain shown.
Verify which fields actually differ and that the criteria, source excerpts,
controls, decisions, selections and executable request are unchanged. Do not assume
that the expected fingerprint difference is the only difference.

If the actual semantic evidence is unchanged, retain a NEW caller comparison:
preserve all 20 criterion_comparisons and their specialist-r2 dispositions verbatim,
update the report path/hash and review_scope_sha256 to the exact current report,
and record explicit continuity provenance to the prior caller comparison. Read the
previous comparison and its four discrepancy resolutions; preserve their scope.
If evidence changed, compare the actual change rather than inheriting agreement.
Call pixl_request_review with comparison=the new caller file and retain its result.
Structural coverage is not a semantic verdict. The old normal-motion contract
still needs its documented corrections before future adoption; the changed
reduced-motion requirements and prepared blocked intent remain unresolved.

Return EXPORT-RESULT.json with exact paths/hashes, observed differences, coverage,
unchanged historical-file verification and concrete continuation. Do not change
state, PLAR, old reports/proposals, assets or the frozen kit. Do not dispatch,
prepare, render, generate or invent an operation that rebinds an immutable job.
The existing specialist review is complete; no fresh delegation is needed for
this caller's byte/identity continuity check.
