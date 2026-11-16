# Native Claude model selection and retained continuation

<a id="claude-model-continuation"></a> **Native execution restored; handoff qualification still fails.** The same caller and specialist completed their retained task using the configured Opus model and existing Max login. Literal answer-effect and optional-background errors remain adopted in the returned handoff. [Exact result](RESULT.json).

The isolated evaluation omitted the user's model selection. It passed
`--setting-sources ""` without `--model`; the retained caller and child used
`claude-fable-5-1`. The user's existing settings selected `claude-opus-5-5`
before the failed run. Native authentication was already `claude.ai`,
`firstParty`, subscription `max`.

The earlier `model_requires_usage_credits` / `extra_usage_out_of_credits`
failure did **not** establish exhaustion of the user's included Max access.
Asking the user to restore usage access was an unsupported diagnosis. Original
[failed evidence](../literal-reconciliation-20261116/README.md) remains intact.

The preparation APIs now accept an explicit `--model` for a fresh caller or
same-session continuation. This correction belongs to the maintainer's isolated
evaluation launcher. Normal PIXL use inherits the existing native host.

This continuation keeps caller `0f688277-0e32-45d2-9ee8-8d47724b0865`,
specialist `a94b4dc767b65b243`, the same external consumer and frozen kit.
Its invocation selects the user's Opus model and effort explicitly; scoped
settings also select that model for subagents. Authentication and global
settings remain unchanged. No new owner answers or evaluator feedback are
supplied. The [preparer](prepare.py.txt) retains the prior input state before
execution. Native response models and completed results must be observed;
requested configuration alone is not completion evidence.

The native continuation finished with exit 0. Both the original caller and child
returned actual responses on `claude-opus-5-5`; the CLI's rate events reported
`isUsingOverage: false`. This observes included access during this run, not an
account billing audit. The child completed its correction handback and the
caller saved [its final result](native-01/project/CALLER-RESULT-LITERAL-RECONCILIATION-02.json)
with SHA-256 `28c2976f3fcc9036ba60cdb3feed4a9b9a98b5920d4bd6e28937b7e45209e0a6`.
All 167 entry files remain unchanged; 17 new files bring the retained output to
184. The current state remains revision 16 and the frozen kit remains unchanged.

**Behavioral qualification still fails.** Independent review finds that the
adopted specialist return still promises production-gate clearance from an
insufficient set of answers. Another current field still treats backgrounds as
required for visual review despite the source's permitted fallback. Complete
literal coverage did not detect or resolve these meaning errors. The failed
[semantic review](semantic-review.json) records 26 passing criteria, seven
failures and one inherited/preserved result across the unchanged 34 criteria.
Its [41 reference bindings](semantic-verification.json) verify separately.
These results remain separate from successful native execution, preserved
identities and file-integrity checks.

The [focused verification record](focused-verification.json) reports 37 passing
tests and scoped Ruff. A test-only lint error was corrected and that changed
test was rerun; raw output is retained only in the development conversation.
The full verifier was not rerun, and its earlier receipt does not cover the
changed evaluation/test sources. The original preflight's vacuous inherited-
criteria check is retained and explicitly replaced for that purpose by the
[seven-check addendum](preflight-addendum.json). Mechanical observations and
any checker limitations are retained separately in [mechanical.json](mechanical.json).
That first mechanical check is 29/32 partial: its parser did not recognize the
host's system-attachment delivery format, and its return-file rule was too
narrow. The preserved [delivery addendum](mechanical-delivery-addendum.json)
verifies the exact child text in the attachment, its inclusion in the next
actual model request and the final caller response. Seven additive checks
reconcile all 32 mechanical checks; this is composed evidence, not a clean
rerun of the first checker. The separate [access observations](mechanical-access.json)
retain the native authentication and no-overage events.

## Product usability finding

The shipped cold-handoff guide currently requires manual review rows for every
JSON leaf, including metadata and empty containers. The default everyday guide
also starts with an existing queue fixture instead of a direct asset brief.
These are concrete sources of extra work in production instructions, separate
from the isolated launch defect. Existing CF-02 / PX-SKILL-001 work should reduce
that burden and measure useful asset delivery. Exhaustive coverage diagnostics
and passing harness checks do not demonstrate that PIXL helps produce better
art or saves caller effort. This continuation preserves its frozen guide so
later simplification can be assessed separately.

Human acceptance remains separate. M1/M2 and broader M3/M4/M5 remain open.

The [read-only integrity check](integrity.json) covers 29 claims and 127
receipts. It reports one current claim, 11 historical claims and 17 needing
review; exit 1 preserves source/release applicability gaps. All 141 snapshotted
declared receipt and changed maintained files retained their bytes and times.
An incidental whole-repository snapshot was stopped after revealing 93,349
files; its [incomplete check](integrity-snapshot-interruption.json) receives no
verification credit. The scoped check above is the completed result.
The [final maintenance check](final-check.json) verifies changed-file credential
shapes, maintained-source whitespace, 1,220 local documentation links and all
29 registered claim lines. These checks establish no additional behavioral or
artistic result.

Official references: [Claude model selection](https://code.claude.com/docs/en/model-config)
and [subagent model selection](https://code.claude.com/docs/en/sub-agents).
