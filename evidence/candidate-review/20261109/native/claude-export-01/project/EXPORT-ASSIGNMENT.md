# Verify exact result files through the final public interface

You are a native caller verifying a completed review's result handoff. This is a
bounded serialization/retry follow-up, not another art review or generation job.
The earlier native trial remains unchanged outside this isolated copy. Read the
current kit's resources/spec/candidate-review.md, especially Save results directly.

Use the actual local MCP/CLI, not imports of implementation internals or handwritten
copies of tool results. All result paths must be fresh under work/export-review.

1. Use pixl_review_context with result_path, or review-context --result-path, for
   native-review.family.candidate, state .pixl/assets/queue.ready/state.px. Read/parse the exact exported JSON.
2. Use pixl_family / family with result_path to export the current family report.
   Keep creation acceptance distinct from current acceptance.
3. Replay the exact saved request work/export-review/identical-review.json using
   candidate-review / pixl_candidate_review, candidate native-review.family.candidate, review ID
   native-review.family.collective, store .pixl/assets/queue.ready, the current state_hash and a fresh result_path.
   Do not change the request. This must reuse the review with zero publications.
4. Independently check all exported JSON files parse, their bytes/SHA-256 match
   the returned summaries, state remains 23718b6d027836af49f3548fcb38979bd4afca032e8113d7a9222c7c570c8c49, and acceptance
   remains complete. Retain the compact summaries from actual tool/CLI output.
   Use native execution to parse/hash files; do not transcribe complete JSON.
5. Write work/export-review/EXPORT-RESULT.json with actual calls, summary/file
   locators, verified identities, retry/publication result and any error. For
   Claude, preserve the prior malformed 04-family-snapshot-result.json and the
   caller-corrected copy. Link current exported family/context files as usable
   current results; do not rewrite or relabel the old creation receipt.

This verifies the final package's output path and a historical review's retry.
It does not establish broader art quality, named-role selection or new rendering.
