# Exact retained Claude seed

[RESULT.json](RESULT.json) passes nine preservation and compatibility checks. The
[seed](seed/) contains the exact 36 files from the interrupted revised-routing
Claude project. No source, state, report, choice, authorization or receipt was
rewritten. Its unusual store path remains `state.px/state.px`. Original unsupported
outline/canvas generalizations remain in the retained reports for later behavioral
review; validation does not endorse them.

Use [seed-manifest.json](seed-manifest.json), a relative-path-to-SHA256 mapping, to
prepare the cold trial. [seed.zip](seed.zip) and
[original-project.zip](original-project.zip) are identical complete snapshots,
SHA256 `3b00025b5d4ac60ae34d932a90c36541db79c2a43ae00d79b79d801cd710530c`.
The parent archive and old/current kit identities are recorded in RESULT.json.
The expanded original archive was not modified. Scratch copies under `work/`
are ignored; the retained archives, scripts, command records and outputs provide
the reproducible inputs and results.

The old project already validates with the current frozen kit. Its five S records
reference project-owned brief/research/observation files and the two supplied
images. It imports no kit library source records, so `retain-library` is neither
needed nor applicable. This differs from the historical common Codex cold seed,
which imported kit resources. No source-retention directory was added here.

The preparation preserves three evaluator findings:

1. [Original commands](commands.json) show successful validation with both the old
   installed kit and the current installed kit, using the current frozen runtime.
   The initial script incorrectly expected source drift; its
   [failed expectation](attempt-01-assumption-failure.json) remains recorded.
2. [The explicit retain-library attempt](continuation-commands.json) correctly
   returned `library_sources` because this project imports no kit resources. It
   did not alter the project state or add source snapshots.
3. [The first portable commands](final-commands.json) passed validation/workflow
   but correctly refused authoring context focused on a project record. The
   [corrected portable commands](final-v2-commands.json) pass validation, workflow,
   task-focused authoring context (`t_sample`) and decoding. Original failed
   output and the script that made that call remain available.

This is local evaluator preparation and compatibility evidence, not native
behavior. The original Claude run used `--no-session-persistence`; using this
seed starts an artifact-based cold context, not the original native session.
No provider or model call, full verifier, new art verdict, engine acceptance or
human acceptance was performed by this preflight.
