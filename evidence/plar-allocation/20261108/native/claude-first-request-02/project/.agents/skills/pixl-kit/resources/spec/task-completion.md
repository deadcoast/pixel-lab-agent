# Reviewed task completion

`task-complete STORE TASK CANDIDATE... --expect HASH --root ROOT` and
`pixl_task_complete({store,expect,task_id,candidates})` nominate explicit existing
candidates and complete their PX2 task. This is a local publication operation;
it creates no criteria, decisions, evidence, verdicts, asset files or provider calls.
It adds no UDL fields and preserves the existing registry/lifecycle semantics.

Every planned output needs exactly one supplied candidate owned by that output.
Every saved required criterion must already have a current passing verdict for
that candidate. Missing, failed, unavailable or stale acceptance cannot complete.
All normal prerequisite, choice, adoption, baseline and file-binding checks apply.
Prepared/unknown/submitted/running jobs on this task must be reconciled first.
Dropped tasks and changes to already-completed selections require explicit reopening.

The expected hash is checked under the store lock. The complete transition sequence
is validated before publication. An open or blocked task publishes the ordinary
active revision and then the done revision, retaining both snapshots; an active
task needs one revision. The operation holds the writer lock throughout. Validation
failure leaves state unchanged. Storage interruption between publications can leave
a valid active state; read workflow/current hash and resume without repeating any
provider request. Hard process termination may leave the existing store lock; follow the normal stale-lock owner check before recovery. This is not a multi-file all-or-nothing transaction.

An already-done task with the same selection and expected hash returns
`already_complete:true` without another revision. Results include state/hash/revision,
selected candidate IDs, task ID, publication history and explicit
`acceptance_created:false` / `remote_executed:false`. Files still need the caller's
assigned destination integration and actual review; this operation only publishes
completion supported by the existing saved acceptance plan.
