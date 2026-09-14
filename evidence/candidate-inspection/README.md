# Candidate inspection evidence

PX-OPS-001 is implemented through the [inspection contract](../../spec/candidate-inspection.md)
and [shared operation reference](../../plugins/pixl/skills/pixl/references/inspection.md).
The runtime prepares exact views and retains explicit reviews against saved criteria.
The developer evaluates this product; reading the profile does not activate PIXL.

## Verified operation

`inspection-prepare` captures exact candidate/reference bytes, native and integer-nearest
views, declared frame/tile contexts, factual measurements and original semantic records.
`inspection-review` retains caller observations and explicit criterion E/V.
`inspection` recovers original conditions, viewing declarations, failures, drift and
next actions. Three equivalent MCP tools bring the local surface to 27 tools.
Existing PX1/PX2 meanings remain unchanged. No automatic artistic verdict, nomination,
task completion, provider action or engine execution is added.

The [full verifier](full-verifier-first.txt) passed **380 of 381 tests**, with one
existing Windows symlink-privilege skip, and **39/39 reference checks**.
[Current results](../test-results.json) bind runtime hashes. The initial
`runs:1, errors:1` log line is the deliberate recorder-integrity rejection test;
the full suite has zero failures and errors. Focused suites cover 18 renderer,
14 publication, five real adapter tests and one trial-protocol regression.

Independent reviews found and verified fixes for allocation ordering, high-memory
measurement structures, hidden RGB loss, reference-only candidate rejection and
scalar-type equivalence. Earlier failures remain alongside post-fix probes. All
65,536 binary 4x4 topology comparisons and 150 seeded full measurement comparisons
match existing asset semantics. These are bounded probes, not maximum-size stress
tests or artistic judgments.

The [copied-package proof](portable-operation/report.json) executes **11 CLI/MCP
operations** with 10 views. Explicit developer declarations record mechanical pass,
visual fail and engine unavailable. A copy of the existing reference becomes a
separate candidate solely for lifecycle testing; it inherits no verdict. A relocated
project recovers the earlier failure. The script does not view images or produce art.

## Native profile observations

These are three fresh native sessions using the same saved controlled project.
Actual native image payloads establish delivered inputs independently of review fields.

| Attempt | Observed result |
| --- | --- |
| [Codex inspection 01](previous-run/native-operation-01/runs/codex-inspection-01/record.json) | Loaded profile/reference/contract; used prepare/review; 10 native/8x deliveries match retained pixels. Mechanical pass, correct visual fail, engine unavailable, task open and art unchanged. [Review](codex-native-review.json). |
| [Claude inspection 01](previous-run/native-operation-01/runs/claude-inspection-01/record.json) | All 10 native/12x deliveries match. Correct rejection and unavailable engine retained, but mechanical verdict omitted because ambiguous contract wording was read as requiring image coverage for mechanical passes. Profile file and inspection readback were also omitted. [Preserved partial/failing review](claude-native-review.json). |
| [Claude inspection 02](native-operation/runs/claude-inspection-02/record.json) | Loaded profile; 10 native/8x deliveries match exact retained bytes and pixels before review. Mechanical pass, visual fail, engine unavailable, inspection/workflow readback, open task and unchanged art. [Independent repeat review](claude-native-repeat-review.json). |

The candidate lacks the reference's image-left antenna and image-right yellow eye.
Both hosts identified these actual defects. Each attempt received six native 32x32
and four enlarged views. Claude honestly declared unknown delivery sizes; the evaluator
recovers exact dimensions from native payloads. Unknown sizes do not prevent an
observed visual failure or a local mechanical judgment.

The clarification explicitly scopes complete coverage to visual/continuity or
visual-mode passes. Mechanical/local criteria require explicit judgments against
saved conditions, without an image-coverage gate. **Only the packaged contract and
bundle manifest changed**; runtime, profile and skill hashes are identical.
One successful repeat establishes observed recovery, not a causal effect estimate
or general reliability. Codex was not rerun after this wording clarification.
No real generation, animation playback, browser/device or engine acceptance was tested.

The [integrity/replay receipt](native-integrity.json) verifies both frozen inventories,
protocols and recorded files, then executes **12 read-only operations** against temporary
copies of the three attempts' own packages. There are zero errors and no replay changes
to project files. Process completion is distinct from the explicit behavioral reviews.

## Identity, preservation and repetition

- Initial package manifest: `4f93bcd4259656589219066924e5de6f179f86ab0c99e9bc1906ea831e9c8b0d`.
- Clarified current manifest: `3503d7d39e0c6465fb86a83d9ff8feda9aa297eb200c8ab3f9c148aa3a19739b`.
- Each package contains 98 files; its manifest binds 96 entries plus generated
  requirements. [Initial identity](previous-run/native-operation-01/identity.json) and
  [clarified identity](native-operation/identity.json) retain exact maps.
- The earlier [16-attempt matched series](../host-evaluation/) remains unchanged and
  describes its original package. The [145-file archive](legacy-docs/docs-01/manifest.json) and
  [three additional previous documents](legacy-docs/docs-02/manifest.json) preserve the
  preceding implementation and receipts. Failed checks remain separate from passes.

Repeat the copied operation with a fresh destination:

```powershell
uv run --no-sync python scripts/inspection_probe.py --out evidence/candidate-inspection/portable-new
```

Use `evaluations/inspection_trials.py --series NEW_NAME --host claude --attempt NEW_ATTEMPT`
(or `--host codex`) through the existing uv environment for a new model trial.
Names cannot be reused; changed package/protocol bytes require another series.
Each protocol retains the saved-project variation and exact ZIP inventory.

The next target is **PX-SKILL-001**, actionable consequential choices at the handoff.
Artistic-authority correction and broader production/recovery evaluation remain
distinct [MIVIM tasks](../../evaluations/TODO.spec.md).
