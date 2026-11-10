# NF-03 readiness and QOL-06 consumer setup

This is a bounded implementation and native setup evaluation in active cycle
`IDENTIFY-2026-11-09-01`, linked to M2, PX-EVAL-005 and PX-PKG-001. M1/M2 and the
overall specialist ecosystem remain open. No artwork, provider submission or
target-engine acceptance is assigned here.

## Implemented operation

[`readiness` / `pixl_readiness`](../../plugins/pixl/skills/pixl/references/readiness.md)
reports the consumer root, inspected installation, dependency imports, static
adapter files and explicitly caller-supplied host observations. It separates the
executing interpreter/module from the installation being inspected. Relative
installation paths use the consumer root; absolute paths may select another
installation. Manifest checks compare listed payload bytes with the exact manifest
snapshot read, without claiming publisher authenticity.

The standard-library bootstrap can report missing dependencies before the
ordinary CLI or local MCP can load. Exit 0 means local prerequisites are satisfied;
exit 1 means incomplete setup and exit 2 invalid input. The existing `ready`
operation still reports production-state readiness. The new operation does not
launch a specialist, inspect credentials or global settings, probe authentication,
submit provider work, or publish project state.

Host observations use a closed envelope of names, a numeric version and an
observation time. They remain supplied assertions. An absent item in a partial
inventory stays unobserved; absence in a supplied complete inventory applies only
to that capture. Authentication and instruction loading stay unverified by the
report even when tools or a role are reported available. Actual native traces
and successful tool calls provide their own evidence below.

Consumer setup now leads with a complete kit, host profile/skill loading and the
parent's official PixelLab connection. Maintainer sync, rebuild and verification
remain separate in [README](../../README.md) and [AGENT-KIT](../../docs/AGENT-KIT.md).
A wheel installs local runtime/profile resources, not native skills or roles.
The portable Codex template is resolved into the consumer and registered for one
invocation; Claude uses its actual plugin role. No global configuration is edited.

## Verification and native results

The [current result and identity index](20261110/RESULT.json) adds authenticated
Claude outcomes to the retained Codex qualification. The [initial index](20261109/RESULT.json)
remains unchanged, including its authentication blocks. These records separate
local setup, native loading, instruction following and useful source/library retrieval.
The [full verifier](../verification-runs/20261110T035753.519588Z/result.json) passes
**716 tests with one Windows symlink-privilege skip**, 39 reference checks,
benchmark and fresh installed-wheel/copied-plugin checks. This is the suite's
total, not a count of newly added tests. [Focused lint/default Mypy](20261109/verification/local-final-01.json)
and [18 supplemental scenario/grader tests plus Ruff/Mypy](20261109/supplemental-verification-01/result.json)
pass. Default Mypy does not fully check untyped bodies. The supplemental grader
and its tests changed after the full verifier; runtime and bundle bytes did not.

The [fresh installation proof](20261109/setup/attempt-01/RESULT.json) records
17 commands. Copied-kit `pip install -r`, installed-wheel `pip install` with the
actual console entrypoint, and source `uv sync --locked --no-dev` all pass exact
source/readiness checks. The bare environment first returns structured incomplete
readiness with exit 1. No maintainer packages are installed. Consumer/package files
and all 299 captured inputs in the source fixture remain unchanged by those checks.
The original maintainer environment was not an installation target. Exact
[wheel/sdist copies](20261109/setup/retained-distribution-01/IDENTITY.json) are
retained. A [repeat-attempt rejection](20261109/setup/existing-output-rejection-01.json)
preserves all 75 existing receipt files. These are Windows/Python 3.14.3 results;
other OS/Python combinations remain unqualified.

| Native case | Observed result | Independent grade |
| --- | --- | --- |
| Codex 0.167.0, clean | Resolved portable template registered; actual `pixl` child completed; exact source/library/readiness results consumed | [19/19 pass](20261109/native/codex-clean-01/independent-grade-02.json) |
| Codex 0.167.0, role loading omitted | Exact role not observable/selectable; no generic replacement; all three local operations completed | [16/16 pass](20261109/native/codex-missing-registration-01/independent-grade-02.json) |
| Claude 2.1.318, clean, authenticated follow-up | Actual `pixl:pixl` child loads the profile/skill and returns exact source/library/readiness results | [18/18 pass](20261110/native/claude-clean-01/independent-grade-03.json) |
| Claude 2.1.318, plugin loading omitted, authenticated follow-up | Exact role/skill probes fail in this invocation; no generic replacement; all three local operations completed | [16/16 pass](20261110/native/claude-missing-registration-01/independent-grade-02.json) |

Both authenticated Claude processes exit 0. The clean case records registered
child `a30b1c71a0d89f028`; the incomplete case has no child. These fresh attempts
follow the retained [clean](20261109/native/claude-clean-01/independent-grade-02.json)
and [omitted-plugin](20261109/native/claude-missing-registration-01/independent-grade-02.json)
authentication blocks. Those original attempts still have zero model tokens and
no child or caller result; their three passing checks cover preparation and
preservation only. No PixelLab authentication conclusion follows from either the
old host-login failure or the new successful local work.

The authenticated clean case initially scored 16/18 because the grader did not
recognize the actual numbered/tabbed `Read` result or the host's skill-body
injection, which omits YAML frontmatter. The [correction](20261110/grader-correction-01/result.json)
binds successful calls, results and injected source to the selected child; it
does not accept assistant quotations as loading evidence. Its 22 focused tests
include four new negative regressions; Ruff and focused Mypy pass. The original
grade, exact before/after sources and initial Mypy configuration/baseline issues
remain retained. Final grade 03 reads the unchanged native attempt; no relaunch
or rewritten native result supplies the passing observation. A later
[format identity check](../caller-result/20261110/format-verification-01/result.json)
restores the grader/test sources' original LF endings and re-executes their affected
grades with unchanged results; the original source snapshots remain retained.

The Codex child's native journal binds its actual `/root/readiness_specialist`
identity to the parent spawn and `pixl` role. Its injected instructions match the
resolved template after CRLF-to-LF normalization only; successful child commands
read the complete current skill/profile. The compact recorder's Codex call/child
summary omits this collaboration surface, so the independent grader uses the
retained native journals. The original recorder summary is unchanged.

Both Codex callers correctly retained full successful MCP envelopes. The first
grader assumed inner data and scored 15/19 and 12/16; those are evaluator defects,
not native task failures. [Original grader](20261109/grader-versions/grade-readiness-initial.py.txt),
[pre-envelope adapter version](20261109/grader-versions/grade-readiness-before-envelope-adapter.py.txt),
and both grade-01 receipts remain preserved. The corrected, regression-tested
grader produces additive grade-02 receipts without relaunching or editing native
results. Its controls reject parent-only reads, wrong child identities, generic
substitution and unsupported catalog claims.

Native cases use independent consumers outside repository ancestry, a complete
relocated kit and the fresh runtime. Each host has a clean role-loading case and
a case that omits that route while keeping local MCP configured. All use the
same frozen manifest `7bd1646fc6dba68180fee13ea58bfe56cd317ccf493cac1e40bc57d964536786`
(177 payload entries plus generated requirements). The official server is
deliberately absent from these evaluation invocations; this says nothing about
other user sessions, account authentication or service availability.

## Review questions A–E

**A — Improvement:** setup now has one small diagnostic report and concrete
consumer routes. It identifies useful next actions without turning a setup check
into another production approval gate. Compact caller results and scoped recovery are now the active
M2 usability work, with qualification tracked separately in [their evidence](../caller-result/README.md).

**B — Claude/Codex compatibility:** static files, role declarations, actual
invocation and loaded instructions are different observations. The fresh trials
qualify the installed host versions and explicit routes only. Automatic discovery,
other versions and broader reliability remain open.

**C — Contextual and artistic quality:** exact source/hash and library retrieval
test whether the specialist can obtain consumer context. They do not establish
reference fidelity, artistic judgment, generated quality or engine acceptance.

**D — Another repository:** the consumer root and installation are explicit;
fresh environments and relocated kits test the documented routes without changing
the maintainer environment. Missing local dependencies and missing role loading
are diagnosed separately from provider observations.

**E — Responsibility:** the profile supplies specialist behavior; skills explain
the workflow; local CLI/MCP reports local facts; the native host supplies actual
role/tool observations; official PixelLab performs separately authorized provider
work. A cached capability catalog is documentation, not live provider discovery.

## Continuation

Keep the [active plan](../../PLAN.md) and [M2 backlog](../../SHELVED.md#m2--dependable-native-agent-to-agent-operation).
The two fresh authenticated Claude cases complete this bounded setup qualification
alongside the retained Codex results; earlier expired-login receipts remain
historical. Continue the active QOL-10 compact caller result and continuation
qualification, with SC-08 error categories informed by observed recovery cases.
Broader production, repeated host reliability and M1/M2 exits remain open.
