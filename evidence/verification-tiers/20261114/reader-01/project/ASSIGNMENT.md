# Choose verification from the public entrypoint

1. **inspect** — Find the current verification guide from the public README. Execute its appropriate read-only command to inspect existing evidence without rebuilding it; retain exact stdout/stderr and actual child exit code under work/. Explain what the result means, including current versus historical applicability. Return inspection metadata as specified below.

2. **focused** — A developer changes consumer-index metadata behavior. Which exact documented focused command is useful, what does it write, and what can a passing result establish? Explain why running all unittest discovery is a different side-effect choice. Do not execute either test route in this reader assignment.

3. **rebuild** — Explain the full verifier's order, changed outputs, archive coverage and failure behavior. Is appending --help a safe way to inspect its options? What important effects and locations remain outside its archive? Do not run rebuilders or their --help variants.

4. **tiers** — Distinguish local implementation/distribution checks, native run completion, grading retained work, useful asset/consumer outcomes and human acceptance. Which native preparation/run routes may contact a model or the official provider, and what does an old grade or current integrity result fail to establish? Do not run a native or provider assignment.

Return NAVIGATION-RESULT.json with version:1, status:'complete' or 'incomplete',
entrypoint, a route array naming the repository-relative documents followed, and
inspection:{command:[strings], exit_code:integer, stdout_path:'work/relative-file', stderr_path:'work/relative-file'}. These paths are relative to your scratch root. Include
answers (one per question). Each answer has id, conclusion, evidence (an array of
{path,sha256} references to exact local files), limits (strings), and prior_failures
(exact file references where applicable). Quote only small relevant facts; do not
copy large receipts. Cite exact receipt paths and hashes rather than relying only
on an index summary. If a fact cannot be found, state that gap; do not infer a pass.
At the end, report any confusing navigation, contradictory current-facing wording,
or missing route in navigation_observations (strings). No post-launch help will be
provided. Do not write the evaluator's grade or alter any original artifact.
