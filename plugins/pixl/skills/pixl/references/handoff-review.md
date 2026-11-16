# Review the literal handoff

Use this operation when returning authored questions, answer effects or a next
operation in a saved JSON result. It exposes every value in the selected parts
of that result and binds the review to the exact files. It does not decide whether
a source supports a claim. Continue authorized independent work while reviewing.

## Establish the current instructions

Read the primary brief, adopted decisions, applicable literal criteria and actual
operation prerequisites. Keep the [current-effect worksheet](intake-sample.md#write-the-current-effect-before-the-return)
in the new continuation note. Its current operation/condition section must carry
all instructions governing the next operation, including remaining dependencies
and permitted alternatives. Previous operational notes are history/evidence, not
parallel current instructions, even when linked by section name. Cite unchanged
source evidence and useful facts without copying the whole project history.
A new note cannot supersede owner requirements or source criteria: correct the
agent's interpretation and explicitly identify which prior instructions it replaces.

Save the new caller result from that fresh review. Select the **whole question
collection and whole next-operation subtree**, not just fields already considered
correct. Include additional scopes for other authored operational claims elsewhere
in the result. Preserve runtime-derived continuation unchanged; review the authored
explanation beside it. Use the actual field names in your file.

## Inventory the saved result

From the consumer root, using the assigned Python interpreter and installed kit:

```powershell
python -B -I pixl-kit/scripts/check_handoff.py caller-result.json --root . --scope /remaining_questions --scope /next_action --out handoff-inventory-01.json
```

Repeat `--scope` for disjoint JSON-pointer subtrees. The inventory lists every
scalar and empty-container leaf with its pointer and actual value, independent of
any review rows. It also supplies the result's byte hash. Inventory status is
`inventory`, not a pass. A missing or overlapping scope must be corrected explicitly;
do not narrow the scope to hide an unreviewed claim.

`-B` avoids creating Python import caches in the read-only kit; `-I` isolates the
interpreter from ambient Python configuration. Use these flags for this helper and
other Python reads of an assigned read-only kit. No global settings need changing.
The helper reads only by default. `--out` exclusively creates one fresh confined
report; its parent directory must already exist. It never overwrites the result,
review, source or prior report. An installed wheel can use
`python -B -I -m pixl.handoff_review` with the same arguments.

## Review every listed value against its meaning

Create a version-1 review file after independently interpreting each source. The
inventory is the worklist, not the expected answer: do not populate `expected` by
blindly copying the saved values. Write what the source-grounded review actually
supports, including qualifiers, alternatives and dependencies still remaining.
Then reconcile the result with those findings under the assignment's authority,
preserving old versions. Bind the review to the final result's actual hash.

The review has these fields (the sample row below is a shape illustration, not a
complete review or a project answer):

```json
{
  "version": 1,
  "result": {"path": "caller-result.json", "sha256": "ACTUAL_RESULT_SHA256"},
  "scopes": ["/remaining_questions", "/next_action"],
  "claims": [
    {
      "pointer": "/remaining_questions/0/unlocks",
      "expected": "The exact effect supported by this project's sources",
      "basis": "source_comparison",
      "finding": "Independent interpretation, applicable scope and disposition",
      "sources": [{"path": "source.md", "sha256": "ACTUAL_SOURCE_SHA256", "lines": [10, 12]}]
    }
  ],
  "carriers": [
    {"path": "continuation.md", "sha256": "ACTUAL_NOTE_SHA256", "lines": [20, 25], "text": "Exact current operational excerpt, including its line endings"}
  ]
}
```

Supply one row for **every inventory leaf**, including IDs, booleans and empty
containers. For an identifier or other non-operational metadata, use
`basis: "metadata"`, a finding explaining that classification, and `sources: []`.
Metadata coverage is reported separately and is not source-grounded review. Do
not classify required/optional flags, answer effects or blocker claims as metadata.
A source-comparison row needs actual source file hashes and inclusive line ranges;
read what those lines say, not only whether the ranges exist.

List exact excerpts covering **all current operational instructions** in the new
note as `carriers`, with its actual hash, inclusive line range and exact text.
Include any other current authored prose that the handoff tells its caller to act
on. Omitted notes or excerpts are outside the check: the helper cannot discover
what an unlisted paragraph would require. Source criteria retain their own authority
regardless of which excerpts are selected.

Each cited source or carrier excerpt must fit **16,384 UTF-8 bytes**. If its
citation reports `needs_narrower_range`, split the section into consecutive,
explicit line ranges with exact text, without dropping current instructions.
JSON inputs are limited to 16 MiB and source files to 64 MiB. Preserve limit
refusals; these read limits do not judge meaning or justify omitting a claim.

## Check coverage, then finish the semantic review

```powershell
python -B -I pixl-kit/scripts/check_handoff.py caller-result.json --root . --scope /remaining_questions --scope /next_action --review handoff-review-01.json --out handoff-check-01.json
```

The check compares the independent inventory with review rows, expected values,
result/source identities and carrier excerpts. Resolve missing or extra rows,
value differences and stale identities explicitly; use fresh output names and
retain failures. It cannot determine whether a finding is sound or metadata is
correctly classified. `coverage_complete` means the declared coverage and bindings
match; `semantic_verdict` remains `not_assessed`. It is not a production-readiness,
artistic-acceptance or instruction-following verdict.

After the check, reopen the actual saved fields and complete current instruction
section. Independently compare each effect and required/optional condition with
the primary sources and remaining prerequisites. If a valid alternative exists,
keep it available; if an answer leaves a prerequisite unmet, retain that limit in
the effect. Reconcile the final response with those same current instructions.
Matching text or a complete coverage report cannot waive a contradictory source.

The review and check bind the result's hash. Keep their hashes out of that result's
own file-reference map to avoid a circular identity; return their paths/hashes
alongside the final result. Any later result or carrier change requires a fresh
review binding and check. Preserve prior results and reports without relabeling
which version they reviewed.
