# PIXL host evaluations

Current maintainer operations: [native trial recording and continuation](NATIVE-CONTINUATION.md)
retains actual host/session/child identities and separates native continuation from
artifact recovery. [Claude continuation](../evidence/native-continuation/README.md)
and [named Codex role qualification](../evidence/named-codex-role/README.md) retain
their separate native routes, original failures and exact scope. The product
[TODO](../TODO.md) carries the next work; M1 remains open.

**Historical controlled milestone, 2026-11-05:** [PX-EVAL-004](delegated-asset-request.spec.md)
tests the official PixelLab integration through a delegated generation request in
each host. Exercise request construction, job handling, retrieval, inspection and
parent consumption; mock only the external provider boundary. Tests must not
submit real generation jobs or consume PixelLab credits. The adapter, offline tests
and native trial runner are implemented; [recorded outcomes](../evidence/delegated-asset-request/README.md)
retain failures and per-host acceptance limits. Earlier packages, attempts and verdicts stay unchanged.

The newer [candidate-inspection milestone](../evidence/candidate-inspection/README.md)
adds three native attempts in separate frozen series. Codex used the new operation
with verified native/enlarged viewing and retained all three outcome categories.
Claude's first attempt exposed ambiguous contract wording and left the mechanical
criterion unperformed. A contract-only clarification and fresh repeat retained
mechanical pass, correct visual rejection and engine unavailable. The original
failure remains preserved; one repeat does not establish general reliability.
These results do not change the earlier matched comparison below.

These trials evaluate the profile as a product. The developer/evaluator does not
adopt PIXL. [The original scenario catalog](profile-scenarios.json) supplies the
criteria; [the design](../docs/superpowers/specs/2026-09-11-host-evaluation-design.md)
defines the evidence boundaries. The evaluator-only image oracle is never copied
into a trial project or included in its prompt.

The [compiled report](../evidence/host-evaluation/report.json) covers **16 native
attempts** against one frozen package. Codex completed eight model sessions. Claude
completed four; three reached the 600-second limit after substantive work, and the
original authentication failure remains preserved. Both hosts have observable behavior
on five matched catalog cases, with a visual repeat and their own cold intake continuation.
The [criterion review](../evidence/host-evaluation/criterion-review.json) grades actual
observations, including interrupted outputs. Six catalog cases remain unexecuted.
The review retains **33 pass, 2 fail and 9 unverified** catalog verdicts, plus **8 pass**
on supplementary cold checks. Repeats and the preserved auth failure are included;
these counts are not a normalized success rate or independent statistical samples.
[Next work](TODO.spec.md) covers actionable handoffs and unsupported artistic
requirements. Candidate inspection is now implemented and separately evaluated.

The comparison shows several useful operations and a concrete failure. Both hosts kept
the maintainer role and rejected the candidate's missing antenna and eye despite passing
mechanical checks. Codex preserved the requested partial-alpha/selective-AA aesthetic;
Claude's retained style plan substituted zero contour AA and a supposedly approved palette.
The cold Claude session finished the interrupted intake study and asked for consequential
choices, but repeated an unsupported outline/canvas threshold. Valid saved state does not
establish sound artistic judgment.

Only maintainer routing and visual rejection have completed fresh turns in both hosts.
The interrupted Claude intake, missing-provider and style trials still support specific
observations; they do not count as completed turns. No provider generation or destination
acceptance was exercised. Model configuration, tool permissions, recording formats and
overlapping launch schedules differ, so timings and scores do not establish host superiority
or a causal benefit from PIXL. There is no profile-disabled control arm.

## What a result means

| Layer | Required observation | Does not establish |
| --- | --- | --- |
| Host loading | Native discovery, actual package path, local MCP connection | Successful model inference or instruction following |
| Profile behavior | Actual model/tool transcript and criterion review | General reliability, host superiority or production-quality art |
| Local artifact outcome | Retained files, actual pixel measurements/inspection, valid state | PixelLab execution or target-engine acceptance |
| Production outcome | Authorized provider observations and actual visual/destination review | Inferred success from fixtures or metadata |

`host_completed_ungraded` means the native host reported a completed turn. It is
never a passing behavioral score. Claude can emit a result with `subtype: success`
and `is_error: true` after authentication fails; the recorder treats that as a
host error. Init metadata identifies a selected model, not an inference response.

## Running and replaying

Use the existing uv environment from the repository root:

```powershell
uv run --no-sync python evaluations/host_trials.py
uv run --no-sync python evaluations/host_trials.py --host codex --case mechanical-pass-visual-rejection --attempt codex-visual-new --model gpt-6-astra --sandbox danger-full-access --retain-host-session
uv run --no-sync python evaluations/host_trials.py --host claude --case missing-provider --attempt claude-missing-new
uv run --no-sync python evaluations/host_trials.py --host codex --case incomplete-intake --attempt codex-cold-new --model gpt-6-astra --sandbox danger-full-access --retain-host-session --cold-from codex-intake-01
uv run --no-sync python evaluations/check_host_evidence.py
uv run --no-sync python -m unittest tests.test_host_evidence tests.test_host_report -v
```

After new attempts, update the independent criterion review before recompiling
`evaluations/write_host_report.py`; it refuses unreviewed attempts. The compiler
checks observed criterion text and retained identities rather than grading answers.
It derives observed inference, completed turns, usage and matched prompt/image identities
from each host's records. Invalid model-authored state is reportable as a failed outcome;
corrupted or unreviewed evidence prevents compilation. Replay discovers retained store
heads in the directories each host actually chose.

Attempt names cannot be reused. The series refuses a changed source package;
start a separately reviewed series for a changed profile. Every attempt archives
the executed runner version. The first command freezes the bundle and creates
deterministic test images, not production art. The cold command verifies the
predecessor and carries forward only its saved files; a new model session receives
no previous conversation. It is an intake continuation, not the unexecuted
contract-change or uncertain-submission scenario.

The Windows `workspace-write` trial rejected shell reads and image viewing while
local MCP continued to work. Later trials use the same file-access permission
available to this development workspace. Their temporary directories separate
inputs/outputs; they are **not an operating-system security sandbox**. The runner
does not change global configuration or copy credentials. A requested model is
recorded separately from model identity found in host events.

Codex 0.154.0 discovers the unchanged nested packaged skill as `pixl:pixl` under
`.agents/skills/pixl-kit/skills/pixl/SKILL.md`. Session overrides disable unrelated
home skills, plugins, hooks, memories and remote MCP configuration. This exercises
native repository skill discovery of package contents, not marketplace installation.
The installed schema was checked directly: it does not expose the extra-root
field described in [the current app-server documentation](https://learn.chatgpt.com/docs/app-server#skills).
The retained native discovery probe is the authority for this installed version.

Claude uses `--plugin-dir` with the same package and `--strict-mcp-config` with the
local server. The first native init exposed PIXL's skill, agent and all 24 local
MCP tools, then OAuth failed before model inference. After authentication was restored,
assistant messages identify `claude-opus-5`; init metadata separately selects
`claude-opus-5[1m]`. Codex requested/selected `gpt-6-astra` with xhigh reasoning, without
an independent assistant-message model label. Other built-in Claude skills also appear
in its init inventory; the host environments are not identical.
Session loading, structured output and authentication commands are documented in
[Claude's CLI reference](https://code.claude.com/docs/en/cli-reference).

Codex's normal exec JSON stream omits some code-mode tool observations, including
successful image-view results. For inspection trials, `--retain-host-session`
retains this trial's own native journal, including image inputs returned to the
model. Earlier ephemeral attempts retain their stream and files but cannot gain
viewer evidence retrospectively. The evidence review must state that limitation.
Claude's native stream retains image payloads from Read calls; the review matches their
decoded pixels to actual inputs and inspection artifacts. Enlarged viewing alone does
not establish that the model also inspected native-scale readability.

The complete baseline package, prompts, inputs, executed runner versions, raw
streams, output files and review records live under
[`evidence/host-evaluation`](../evidence/host-evaluation/). The original runtime,
provider and family receipts are preserved separately. Deterministic replay checks
the retained state through a fresh copy of that package and never starts a model.
The [earlier Codex baseline report and checks](../evidence/host-evaluation/previous-run/host-evaluation-01/codex-baseline/manifest.json)
remain archived, and every earlier raw attempt and criterion verdict is unchanged.
