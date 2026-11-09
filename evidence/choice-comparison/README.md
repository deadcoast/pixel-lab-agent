# Focused caller choices and concise successor comparison

This M1 slice implements **SC-04** and **QOL-08** using the retained queue consumers.
It extends existing context and request-review interfaces with no new MCP tool,
saved-state field, automatic approval or production-state mutation.

## Implementation

Authoring context follows declared semantic links through output contracts,
family destinations, current inputs/nominees and decisions. Transitive choice
and source dependencies remain present. Project ownership no longer expands every
`P.in` value. Other intake choices remain discoverable through an ID/key/status
index with complete-context retrieval. Unlinked does not mean irrelevant.

`request-review --view changes --plan NEW --against-plan OLD` compares explicit
retained plans. It reports changed criterion fields, source/contract/choice and
allocation identities, retained choices, current review needs and historical
failed, unavailable, obsolete or stale evidence. Clauses align only by exact
stage/local criterion IDs, without inferred equivalence or direct succession.
Every old/new criterion ID/hash remains indexed; literal text stays in the exact
full reports reached through `before.retrieve` and `after.retrieve`. Changed
current declarations never stand in for unavailable historical choice fields.

The default full request-review response and its review identity are unchanged.
The new comparison hash identifies its current structural report, including
state/observations. Both views use existing direct result-file export. See the
[contract](../../spec/production-plan.md) and [caller workflow](../../plugins/pixl/skills/pixl/references/request-review.md).

## Verification

The [focused run](20261109/verification/focused-tests.txt) passes 24 tests. Nine
new regressions cover unlinked intake payloads, transitive caller authority and
destinations, exact criterion mapping/retrieval, renamed clauses, source drift,
missing historical declarations, failures/stale receipts, missing proof, invalid
options, snapshot tampering, CLI/MCP export parity and relocation. Early synthetic
fixture construction missed refreshed adoption bindings; the fixture was corrected
to include its added authority. No production receipt was amended for a test.
Ruff and configured Mypy pass; untyped-body coverage remains limited.

The [first full run](../verification-runs/20261109T173426.892348Z/result.json)
passed 590 tests plus one Windows privilege skip and 39 reference checks, then
failed distribution: the new probe supplied an absolute request-review packet
where that existing operation requires a consumer-relative path. The probe was
corrected; root confinement was preserved. This failed attempt remains retained.

The [final full run](../verification-runs/20261109T173837.626745Z/result.json)
passes **590 tests plus one Windows symlink-privilege skip**, 39 reference checks,
and fresh installed-wheel/copied-plugin probes including the new view and export.
[Package checks](20261109/verification/package-checks.json) verify all 170 bundle
entries and zero drift in tested source inputs. Frozen native kits match the final
runtime, contract and skill; four generated reference/proof resources differ after
the verifier rebuild, and those identities are explicitly retained.

[Measured on the same consumer](20261109/verification/context-measurement.json),
authoring context decreases from 108,596 to 94,054 UTF-8 JSON bytes, selecting four
choices and 24 source entries instead of six choices and 40 source entries. Two
unexpanded choices remain retrievable. The [observed Claude exports](20261109/verification/observed-export-sizes.json)
contain a 75,798-byte structural change view versus 219,204 bytes across the two
full reports. These are fixture measurements, not general performance claims;
direct file export remains appropriate for reading selected fields.

The [native adapter](../../evaluations/choice_comparison_case.py) copies each
completed review consumer and freezes the kit beside its historical versions.
It compares the original 20 criteria with the accepted 23-criterion successor,
requiring native specialist delegation and independent caller interpretation.
Both hosts completed exact semantic comparisons, with different assistance scopes.
The [result ledger](20261109/RESULT.json) links the retained attempts and the
independent checks. Host versions were Claude Code 2.1.318 and Codex CLI 0.167.0.

### Claude — completed with retained caller corrections

Claude invoked the registered `pixl` Agent in the background and completed its own
comparison before reading the specialist's result. The specialist returned all
20 original and 23 successor criteria with literal checks and record identities.
The caller independently verified those exports, source interpretations and image
measurements. [Twelve retention/export checks](20261109/native/claude-01/independent-checks.json)
and [six mapping/invocation checks](20261109/native/claude-01/independent-mapping-checks.json)
pass. All original consumer files, accepted state and frozen kit remain unchanged.

The specialist caught a wrong motion-verdict ID in the caller's brief and clarified
that earlier re-scoped transparency verdicts reused observations. The caller
accepted both corrections and retained them in its [comparison record](20261109/native/claude-01/project/work/choice-comparison/caller/specialist-check-and-corrections.json).
It also disclosed an early scratch extraction's mis-sliced stage/local labels;
the corrected extraction was used, while the first command/output remains in the
native transcript. This run received no maintainer restart or semantic repair.
The [caller result](20261109/native/claude-01/project/work/choice-comparison/CALLER-RESULT.json)
is a completed comparison, not a new acceptance or a repair of the older interrupted
Claude scenario.

### Codex — initial partial, then guided completion

Codex's first run retained correct exports and all 20/23 identities, passing
[12 independent artifact checks](20261109/native/codex-01/independent-checks.json),
but introduced an unnecessary named-role prerequisite and did not delegate.
Its [original partial result](20261109/native/codex-01/project/work/choice-comparison/CALLER-RESULT.json)
remains intact. A separately recorded guided continuation explicitly permits the
already-supported generic native child loading the shared profile/skill; its
semantic result is graded separately. The same caller resumed and invoked
`/root/guided_pixl_review`, which opened the current shared profile, skill, exact
exports and sources. It inherited caller context: separate agent judgment is
demonstrated, not a blind review or named-role qualification. The inherited optional
consumer role adapter still points to an older review assignment; it was not used
by this generic route and must be refreshed before the named-role M2 trial.

The specialist delivered the complete 20-to-23 mapping. The caller caught three
imprecise source ranges and examples that needed separate static Retry/Paused
scope. A native follow-up to the same child produced a [separate addendum](20261109/native/codex-01/project/work/choice-comparison/guided/specialist-followup.json),
preserving the first result. [Twelve guided checks](20261109/native/codex-guided-01/independent-checks.json)
verify prior-file preservation, exact literal mapping, public caller coverage,
artifact hashes, corrected source excerpts and native delegation/follow-up.
The guided runner executes in the original consumer; its generic `record.json`
artifact inventory is empty because it expects a nested copy. The independent
report explicitly inventories the actual project and verifies its saved baseline.
The [guided caller result](20261109/native/codex-01/project/work/choice-comparison/CALLER-RESULT-guided.json)
is complete within that scope. Artifact checks and guided success do not turn the
original partial behavior into an unassisted pass.

### Semantic assessment and limits

Maintainer review of both mappings and caller findings agrees on the five required
distinctions: non-rejecting alpha diagnostics versus visual exterior judgment;
canvas geometry versus invented in-cell margins; nominal 100 ms cadence versus
scoped perceived pacing; qualitative family coherence versus identical weight;
and shared normal/reduced/live-switch consumer obligations. Exact full clauses
remain the authority for the comparison; ID alignment proves neither semantic
equivalence nor direct plan succession. Static descriptors do not advance frames
even though the renderer's shared scheduler can remain active.

Both hosts retrieved indexed intake rather than treating it as irrelevant or newly
confirmed. Both kept prior acceptance separate from historical unavailable
observations. These trials created no production verdict, new provider result or
renderer acceptance. Broad source ranges remain a saved locator limitation, to
improve in future authoring without rewriting historical bindings.

## Required A–E review

**A — Improvement.** Select relevant declared authority and present structural
changes/review needs before full evidence. Remaining M1 work is consistent hash
and root vocabulary plus the everyday operation guide. Native findings add precise
source-locator examples and retained correction handling to that guidance.

**B — Host compatibility.** Existing CLI/MCP surfaces and direct exports retain
their defaults. Actual installed-host behavior is graded separately from schema
checks. Claude completed registered-agent comparison; Codex completed only after
a guided generic-child clarification. Named Codex role selection, the historical
Claude continuation issue and the older interrupted comparison remain separate M2
work. The generic Codex follow-up demonstrated here does not qualify those routes.

**C — Contextual/artistic quality.** Choice status, actor, sources and rationale
survive selection. PIXL's host model compares literal obligations using its
pixel-art expertise; the runtime cannot decide aesthetic consistency. Input and
reference authority still needs interpretation in its actual role. Both current
comparisons preserved the five authority distinctions above; caught citation and
caller-reference errors remain visible. This is bounded evidence, not general
artistic quality or new temporal acceptance.

**D — Consumer operation.** Both views resolve against the supplied project root
and expose public retrieval/export locators. Existing accepted consumers provide
the task context; they require no new repository or asset brief from the user.

**E — Responsibilities.** The profile supplies expertise and authority discipline;
the skill explains caller review; the host supplies reasoning/delegation and
observation; the runtime selects/checks exact records. Official PixelLab remains
the production provider. These views replace neither art review nor acceptance.

## Continuation

Record actual outcomes in [TODO](../../TODO.md) and [SHELVED](../../SHELVED.md).
SC-04/QOL-08 are implemented with the recorded native scopes. Next take QOL-03 hash
labels, QOL-04 root/locator examples and QOL-01 everyday guidance from SHELVED.
M1 remains active until its remaining exits are satisfied; broader artistic quality
and host reliability remain open. Continue the active [PLAN](../../PLAN.md).
