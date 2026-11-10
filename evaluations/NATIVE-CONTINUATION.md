# Continuing a native trial

This is maintainer evaluation infrastructure. PIXL's production profile, skills,
official PixelLab tools and project state remain the production workflow. A host
session is useful working context; the retained assignment, files and judgments
are the durable basis for recovery.

Use one consumer directory across continuation rounds and a fresh attempt directory
for each invocation. Do not copy the entire preceding trial tree into every round.
Reference the original input archive and frozen kit identities; retain new outputs,
native logs and exact transcript snapshots with each result.

## Three different outcomes

| Mode | Meaning | Required evidence |
| --- | --- | --- |
| New session | New caller with an explicit assignment | Actual session ID, loaded configuration and caller result |
| Native continuation | Original caller session sends an existing child its follow-up | Same observed parent session, actual host follow-up to the original child, subsequent work/result from that child, preserved project authority |
| Artifact-based restart | New caller/child recovers saved work | Exact predecessor identities, original files/failed grade retained, explicit new native identity and scoped continuation outcome |

An exit code or a resumable transcript does not establish behavioral success.
`continuation.json` always leaves `behavioral_verdict` ungraded. Review the native
trace and returned files separately. A successfully delivered follow-up alone
does not prove that the child completed the requested work.

For Codex, the recorder retains observed thread identities, actual role/path
metadata, tool declarations, loaded-instruction matches and collaboration call
locations from the native journals. Requested roles and inherited context remain
distinct from the child's own loaded role and work. A generic child remains
generic even if its task name includes PIXL. The [named-role evaluation](../evidence/named-codex-role/README.md)
passes one explicit registered-role assignment and completed same-child follow-up
within a parent process, while retaining earlier failed/partial attempts. The Claude resume helper
does not implement or qualify Codex continuation across separate processes.

The installed isolated Codex launcher needs an explicit invocation-scoped
`agents.pixl.config_file` setting to expose the role selector; merely copying
`.codex/agents/pixl.toml` did not do so in the retained attempts. See the
[consumer setup](../docs/AGENT-KIT.md#plar-and-current-host-delegation). Preserve the
actual role file, wrappers and package in `configuration_files` so later input
checks can detect drift. No user-global registration is required by this route.

The dedicated case reuses the accepted everyday-guide consumer, restores its
ignored production state from the retained baseline archive, and copies the
unchanged repository role plus a frozen portable kit. Prepare a fresh attempt:

```powershell
.venv/Scripts/python.exe -m evaluations.named_codex_role_case evidence/my-trial/codex-01 --consumer build/my-trial-consumer --prepare-only
```

Omitting `--prepare-only` also starts the native Codex caller and retains its
outputs and changed-file archive, including new immutable handoffs under `.pixl`.
The assigned operation reuses accepted work; it makes no new provider request or
art/renderer acceptance. The independent grader uses actual journal roles,
instruction loading, completed follow-up work and returned public-operation
artifacts. A configuration probe or a report-shaped JSON file is insufficient.

## Run and inspect

The existing scenario prepares `launch.json`, `prompt.txt` and `identity.json`.
Its `cwd` names the consumer; it need not be `attempt/project`. Set `artifact_roots`
to the specific new output directories/files so interrupted snapshots retain useful
file identities without repeatedly hashing an entire historical fixture.

```powershell
.venv/Scripts/python.exe -m evaluations.native_trial_records run evidence/my-trial/round1
```

The runner writes raw stdout/stderr and atomically refreshes `continuation.json`
during execution. It records parent/child identities, relevant Agent/SendMessage
calls with raw stream line locations, interruption reason, actual transcript
availability, configuration hashes and observed artifact hashes. Finished attempts
also retain transcript snapshots and the existing `record.json` inventory.
An optional `--timeout SECONDS` preserves an interrupted result. Windows tree-stop
failure falls back to the owned process handle and explicitly records that child
tree termination was not confirmed. The default has no imposed trial deadline.

For an old attempt, derive a separate record without rewriting its original receipt:

```powershell
.venv/Scripts/python.exe -m evaluations.native_trial_records inspect evidence/old-trial --out evidence/new-review/old-trial-continuation.json
```

Historical inspection identifies a usage interruption even when the old host calls
its result subtype `success`. Keep the original execution status and failed/partial
grade. Malformed or unfinished stream tails remain counted, not invented into events.

## Resume the actual parent and child

Claude trials prepared by the common harness now enable session persistence and
assign a session UUID. The subprocess disables automatic memory and removes an
inherited `CLAUDE_CODE_SKIP_PROMPT_HISTORY` override when persistence is enabled;
user-wide settings are unchanged. Old launches with `--no-session-persistence`
remain historical and are not silently rewritten.

Write the precise follow-up into a UTF-8 file. Obtain the child ID from the actual
completed attempt, then prepare a fresh invocation:

```powershell
.venv/Scripts/python.exe -m evaluations.native_trial_records resume evidence/my-trial/round1 evidence/my-trial/round2 --child ACTUAL_CHILD_ID --prompt followup.md
.venv/Scripts/python.exe -m evaluations.native_trial_records run evidence/my-trial/round2
```

Preparation verifies the previous input/configuration identities and the original
parent and child transcripts. It keeps the consumer directory, agent definition,
MCP configuration and package, replaces session-creation flags with the exact
`--resume` parent ID, and records the expected child. Execution checks these inputs
again. A missing transcript or changed configuration returns a concrete error
before launching; it does not reinterpret a fresh child as continuation.

The caller asks the native `SendMessage` tool to continue that child and waits for
its result. Native tool calls and forwarded child messages determine what actually
happened. Retained transcript snapshots are evidence; copying one into a different
machine does not automatically restore native host sessions there. If native
history is unavailable, explicitly start artifact recovery from the saved files.

Official sources checked 2026-11-09: [Claude CLI persistence/resume](https://code.claude.com/docs/en/cli-reference),
[subagent continuation](https://code.claude.com/docs/en/sub-agents#resume-subagents),
and [parent session plus child ID](https://code.claude.com/docs/en/agent-sdk/subagents#resume-subagents).
Installed behavior and this repository's [actual results](../evidence/native-continuation/README.md)
are graded separately from those API descriptions. Continue work through
[TODO](../TODO.md) and [SHELVED](../SHELVED.md); M1 remains open.
