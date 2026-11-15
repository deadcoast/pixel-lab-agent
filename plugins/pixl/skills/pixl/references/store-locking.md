# Resolve a local writer lock

Use this reference when a local operation returns `store_locked`. The operation
has not acquired the exclusive writer lock. Preserve the error and inspect the
reported `lock.path`; do not repeatedly retry a write or remove the file merely
because it is old. Reads needed to understand the published state can continue.

## Understand the observation

The diagnostic uses category `unfinished_work` and recovery action
`inspect_lock_owner`. Its `lock` object names the exact path, `metadata_status`
and `owner_state: "unverified"`. When readable, `owner` contains a recorded `pid`
and may contain `host` and `acquired_at`. Older PID-only records remain readable.
Empty, malformed, oversized, unreadable, changing or non-regular records remain
locks; unavailable metadata does not make them safe to remove.

These are recorded values, not a liveness check. `acquired_at` is the lock's
acquisition time, not a process start time. A PID may have been reused or belong
to another host. An old timestamp, missing PID or matching process name alone
does not establish that the writer has ended. The runtime does not reclaim a
lock from those observations or automatically retry the refused operation.

On Windows, inspect the reported location without changing it. Replace the path
and PID below with the actual diagnostic values; process information is useful
only on the recorded host and with the owning session's context.

```powershell
$lockPath = 'C:/path/to/consumer/.pixl/production/.lock'
Get-Item -LiteralPath $lockPath -Force |
    Select-Object FullName, Length, LastWriteTimeUtc, Attributes
Get-Process -Id 12345 |
    Select-Object Id, ProcessName, Path, StartTime
```

A missing process result is not a complete ownership proof. Use the host's
actual session/process record to identify the writer and confirm its completion
or termination. Do not terminate an unrelated process merely because its PID
matches the lock. If ownership remains unresolved, retain the lock and report
that condition while continuing useful reads or unrelated work.

## Recover a confirmed interrupted writer

1. Pause all writers that could use this project, including agent sessions and
   background work. Confirm the original writer has ended and no other writer
   can enter during recovery. If it is still running, let it finish or reconcile
   that owned session first. Removing or moving a live lock lets another writer
   enter; the original writer's cleanup can then remove the successor's lock.
2. Preserve the diagnostic, owning-session evidence and the exact leftover lock
   bytes in a fresh recovery location. Record the affected consumer and published
   state/PLAR identities. Recheck the reported path; if the file disappeared or
   changed while investigating, inspect the new situation rather than moving it.
3. Only after quiescence is established, deliberately move the confirmed leftover
   regular file to that fresh location. This is an explicit filesystem recovery,
   not a PIXL unlock command. Do not apply it to a directory, symlink or an
   unreadable/changing record whose identity you cannot preserve.
4. Read the actual current production and reconcile the interrupted operation.
   `state.px` is the store publication authority. A valid newer state may already
   have been committed; retained history can also contain an unreferenced
   snapshot. Do not roll back the head or republish an old candidate to recreate
   the pre-interruption state. Retry only the remaining local intent with its
   freshly inspected expected hash and unchanged requirement authority.

For step 3 on Windows, after those conditions are satisfied, choose a new
directory inside the affected consumer. Its creation must succeed without
`-Force`; an existing location is not reused.

```powershell
$recoveryDir = 'C:/path/to/consumer/recovery/lock-01'
New-Item -ItemType Directory -Path $recoveryDir -ErrorAction Stop | Out-Null
Move-Item -LiteralPath $lockPath -Destination (Join-Path $recoveryDir 'lock.record') -ErrorAction Stop
```

Keep project writers paused through the move and subsequent reconciliation.
This procedure depends on quiescent writers; it is not atomic compare-and-unlink
protection against an external process changing the filesystem.

## Resume the right operation

The same helper protects stores, PLAR publication and handoff publication.
Use the operation that failed to choose the reads; not every lock folder
contains `state.px`.

| Refused work | Read before continuing |
| --- | --- |
| Store, review or task-completion publication | Validate the actual store's `state.px`; read its current hash, workflow and retained jobs. For interrupted completion, an already published active/done state changes what remains. |
| PLAR publication or preparation links | Read the actual `plar.txt`, selected asset and linked production. A store publication and PLAR update can have different completion states. |
| Handoff publication | Read the selected production and retained handoff/export files. Preserve an existing result and choose a fresh result path where required. |

Use the configured CLI or local MCP reads from the
[state-authority reference](state-authority.md). A changed local hash does not
resolve an unknown remote job. Follow [provider recovery](provider-recovery.md)
for that same retained attempt; never submit another provider request merely to
repair a local lock or missing publication.
