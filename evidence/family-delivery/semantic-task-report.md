# Family semantic task evidence

Developer mechanics only. Retained synthetic local/visual/live receipts do not
establish real art quality, production-profile compliance or engine acceptance.

## Initial attempt, preserved

Command: `.venv/Scripts/python.exe -m unittest tests.test_families.FamilySchemaTests -v`

Exit 1; 2 tests, 2 failures. Missing API failed as intended:
`AssertionError: unexpectedly None : Family planning API is missing`.
The published-plan test first exposed a fixture error:
`transition: task: open -> done`. Corrected the fixture to publish active then
done states for both sample and member; production transition rules unchanged.

## Confirmed missing semantics

Reran the same command after correcting the fixture. Exit 1; 2 tests, 2 failures:
missing `pixl.families` and `unknown_field: member.output.bs`. The latter occurred
while publishing the member plan after a saved and accepted sample.

## Review regressions, preserved

Independent root review identified two missing structural checks: a family
candidate without xs bypassed delivery validation, and a family report plan with
ct could require an impossible raster contract on the helper's manifest X.

Command: `.venv/Scripts/python.exe -m unittest tests.test_families.FamilyTests.test_family_candidate_cannot_bypass_snapshot_checks_by_omitting_constituents tests.test_families.FamilyTests.test_family_manifest_plan_cannot_adopt_a_raster_contract -v`

Exit 1; 2 tests, 2 failures. Both failed with `AssertionError: PixlError not raised`.
Added mandatory xs for candidates of family outputs and rejected ct on a family
report plan. Legacy non-family report semantics remain unchanged.

## Implemented unit and fixture contract

Changed source/test files:

- `pixl/families.py`: pure structural validation, baseline/destination blockers,
  sorted semantic planning bindings, current selection, snapshot readiness and
  detailed baseline/member/destination/criterion/job observations.
- `pixl/registry-v2.json`: registry 2.2.0; optional F.bs/F.mb/F.ds and X.xs.
- `pixl/lifecycle.py`: add pure family blockers to activation checks.
- `tests/family_support.py`: real store publications with saved plans preceding
  synthetic verdicts; active state precedes done state.
- `tests/test_families.py`: 23 tests covering new semantics and legacy behavior.

The only additional changed file from this task is this evidence report. The
parent owns graph/store integration and delivery.py; no bundle was rebuilt and
no commit was made by this task.

`family(root, folder=None)` returns the final persisted Document at revision 6.
Default folder: `root / '.pixl'`. Explicit folders are passed to the real store.

| Role | Task | Output | Candidate |
| --- | --- | --- | --- |
| accepted synthetic sample | task | output | sample |
| accepted synthetic member | member.task | member.output | member |
| open delivery plan | delivery.task | delivery.output | none |

Destination choice `destination` starts confirmed with value
`Synthetic fixture engine`. Delivery criteria are `q.continuity` (visual mode)
and `q.delivery.engine` (live mode). Members are `[output, member.output]`;
snapshot constituents therefore project `[sample, sample, member]`.

Pure `plan` returns exactly `{output, task, baseline, members, destinations,
bindings}`. Bindings are a dict of record ID to record hash in sorted insertion
order. `describe` returns `{output, task, state, baseline, destinations, members,
candidate, requirements, candidates, blockers, snapshot_blockers, pending_jobs}`.
Baseline includes candidate/output/task/eligible/reasons/requirements; each member
includes output/task/state/candidate/accepted/reasons/requirements/candidates.
Pending jobs are `{id, task, state}`. Destination and requirement rows reuse the
existing lifecycle report shape. No report function recursively validates.

## Final unit verification

Command: `.venv/Scripts/python.exe -m unittest tests.test_families -v`

Exit 0; 23 tests passed in 5.062 seconds after the review corrections.

Command: `.venv/Scripts/python.exe -m unittest tests.test_families tests.test_lifecycle_validation tests.test_lifecycle_store tests.test_versions tests.test_graph tests.test_store -v`

Exit 0; 104 tests ran in 7.477 seconds: 103 passed, one pre-existing Windows
symlink-privilege skip. All family tests passed. Earlier 102-test run before the
two review regressions passed with the same one skip.

Command: `.venv/Scripts/python.exe -m ruff check pixl/families.py pixl/lifecycle.py tests/family_support.py tests/test_families.py`

Exit 0: `All checks passed!`.

Command: `.venv/Scripts/python.exe -m mypy pixl/families.py tests/family_support.py tests/test_families.py`

Exit 0: `Success: no issues found in 3 source files`. Mypy also emitted the
existing dependency note at pixl/job_history.py:86 that untyped bodies are not
checked by default; this is not a strict whole-program type proof.

Command: `git diff --check -- pixl/families.py pixl/registry-v2.json pixl/lifecycle.py tests/family_support.py tests/test_families.py`

Exit 0. These files include untracked source from the ongoing repository work;
the diff check alone does not inspect untracked files. Ruff examined their bytes.

## Independent delivery review observations

Reviewed parent-owned delivery.py and graph/store integration without editing
them. Temporary Python probes used the real saved fixture and retained snapshot
bytes. A publication interception retained the helper's candidate before the
probe called real store.commit; it did not fabricate manifest contents.

- Verified possible generic-publication gap: adding open->active delivery task
  activation to the captured snapshot candidate still published successfully.
  Parent notified to resolve against the single-candidate retention contract.
- Verified historical membership changes reject a new current pass verdict
  against an older snapshot in rooted and unrooted validation.
- Verified root-sensitive limitation: with membership unchanged, saving a changed
  continuity criterion then adding a freshly bound current verdict in memory
  passed unrooted validation but rooted validation rejected `family_stale`.
  Rooted writes/reports remain protected; unrooted checks cannot read frozen plans.
- Flagged an unexecuted code-inspection concern: manifest path resolution before
  lexical-path comparison may permit an inside-root redirect during read-only
  validation. Publication's storage check is stricter. Parent notified; Windows
  symlink privilege is unavailable in this run.

The first combined review probe incorrectly attempted active->open; the store
correctly rejected `transition: delivery.task: active -> open`. Corrected the
probe without changing production rules, then obtained the results above.

## Limits

This task exercised language discovery/schema and local recorded lifecycle
mechanics, including actual local publication and receipt bytes. It did not
operate PIXL as the art-production profile, run a real provider or engine,
evaluate production art, or establish repeated cross-host instruction following.
Parent-owned adapter, integration, packaging and final review results are separate.

## Final scoped delivery re-review

Re-read the parent's corrected `pixl/delivery.py`, graph/store hooks and
`spec/family-delivery.md`. No delivery or other source files were edited during
this review.

The generic-publication finding is resolved: a new snapshot publication now
requires the added-record set to be exactly that candidate ID and every existing
record to remain equal to the saved state. The real generic-commit regression
rejects simultaneous task activation with `delivery_publication` and preserves
state bytes. Existing snapshot history remains amendable through separate
intentional planning revisions.

The redirected-manifest finding is resolved: rooted manifest validation compares
the confined resolved path against its lexical path below the resolved project
root before reading the manifest. The actual Windows junction regression passed;
it redirected an already retained manifest directory inside the temporary project
and the read-only report rejected it with `delivery_storage`. This junction check
does not depend on the unavailable symbolic-link privilege cited in the earlier
legacy-store test skip.

The unrooted limitation is now explicit in `spec/family-delivery.md`: unrooted
checks cannot read frozen bindings or copied bytes and do not establish package
validity. The reviewed family report requires a root, store publication validates
the candidate with the explicit/default project root, and delivery transitions
read frozen manifests. Thus the previously observed rooted/unrooted distinction
is an accurately documented boundary, with rooted report/publication protection.

Command: `.venv/Scripts/python.exe -m unittest tests.test_delivery tests.test_families.FamilyTests.test_family_candidate_cannot_bypass_snapshot_checks_by_omitting_constituents tests.test_families.FamilyTests.test_family_manifest_plan_cannot_adopt_a_raster_contract -v`

Exit 0; all 23 tests passed in 8.915 seconds, with no skips. This includes 21
delivery checks covering the two repaired paths, generic storage/saved-plan
checks, unchanged historical snapshots after membership edits, source/copy
identity, published X immutability, stale writes, pending work, unavailable
engine verdicts, and PX1 rejection, plus the two family structural regressions.

Final scoped result: **no open findings in the reviewed local family/delivery
semantics and publication scope**. This result does not establish real art,
provider, engine, cross-host behavior or the parent's subsequent bundle/wheel
validation. The earlier failed probes and findings above remain retained.
