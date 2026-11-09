# Continue the retained review with the corrected renderer
The original capture helper could observe the page before Chromium applied its
final screenshot viewport. Preserve that helper, its captures, failed checks and
the family/style findings in FAMILY-RESULT.json. A separate renderer-recheck/
version now sets device metrics before navigation and captures report/layout/image
in one isolated CDP page. This is a maintainer tool correction, not a new art request
or an automatic acceptance result. Verify the actual new output yourself.

Run node renderer-recheck/capture.mjs --out work/NEW_CAPTURE_DIRECTORY and the
selected Python with renderer-recheck/check.py --project . --capture DIRECTORY.
Open the actual screenshot and relevant native/enlarged views; compare both real
source consumers, current asset paths, source/image hashes and observed placement.
Retain an independent caller comparison. Do not alter the renderer to pass checks,
overwrite earlier results or re-create a family plan that is already retained.
Keep the existing style decision unless actual evidence requires a scoped revision.

If the new evidence resolves available-member destination checks, record that
precise outcome through the existing workflow and update PLAR evidence/next work.
It cannot pass a collective criterion requiring the still-absent members, their
animation, non-color distinction or full family continuity. Preserve meaningful
requirement changes and production-selection diagnostics; do not rebind old jobs
or transfer old verdicts to a different contract. Return a fresh exact handoff and
the actual next useful production action. This continuation is explicitly guided
by a renderer repair; do not relabel the original trial as an unassisted pass.
