Explicit CF-08 controlled native recovery evaluation, not a new art assignment.
Consumer root: C:/Users/ryanf/AppData/Local/Temp/pixl readiness codex clean g4uab3xx/consumer. Kit: C:/Users/ryanf/AppData/Local/Temp/pixl readiness codex clean g4uab3xx/consumer/installed pixl.
Selected Python: C:/github/pixel-lab-agent/build/readiness-setup-01/runtime/Scripts/python.exe. Read RECOVERY-ASSIGNMENT.md and the assigned phase file.
The actual named pixl specialist is required.
The local PIXL server and originating pixellab-recovery-test fixture are separate.
Only that controlled fixture is configured; no real provider or paid work is assigned.
Work only inside this consumer. Do not inspect evaluator backing files outside it,
credentials, host settings or memory; do not install packages or modify the kit.
Keep provider_simulated=true. Human acceptance and artistic/engine acceptance are
separate and unperformed; do not let a generic human-approval gate halt recovery.

# Assigned recovery phase 3

Cold-read prior handoffs and current public state/jobs. Obtain the existing
recovered-avatar-candidate path/hash and actual assets/robot.png. Do not observe, import, prepare,
dispatch, poll or mutate production state in this read-only round. Keep unresolved-job
unknown and recover its exact next action. Caller independently reads/hashes the
actual retained candidate and delivered file, opens the returned PNG, verifies the
consumer path and consumes the result. Return status='recovered' with the SAME
candidate/job/remote identity and explicit next inspection/unresolved-job action.
No new provider call or file copy is needed. Write new reports only under work/provider-recovery/phase-3.

Both participants must read the full current public jobs report, saved as
work/provider-recovery/phase-3/jobs-before.json by the specialist and work/provider-recovery/phase-3/jobs-after.json after its work.
The caller independently retrieves its own current report as work/provider-recovery/phase-3/caller-jobs.json.
The specialist writes work/provider-recovery/phase-3/SPECIALIST-RESULT.json; caller writes
work/provider-recovery/phase-3/CALLER-RESULT.json after actual child completion and independent consumption.
Each report includes phase, status, provider_simulated=true, job, remote_id,
unresolved_job, unresolved_state, candidate (null or {id,output,path,sha256}),
state ({path,sha256,canonical_hash,revision}), evidence_refs (actual path/sha256),
limitations and next_action. The caller also includes native_child and a file
reference to specialist_result. File paths are consumer-relative; hashes are actual
SHA-256. Preserve supplied schema/value meanings. Do not claim live PixelLab,
new artistic quality, target-engine or human acceptance. M1/M2 and broader M3/M4
remain open. Return useful exact files and recovery status, not just a plan.
