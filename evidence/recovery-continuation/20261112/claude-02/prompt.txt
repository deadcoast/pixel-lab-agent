Explicit CF-08 controlled native recovery evaluation, not a new art assignment.
Consumer root: C:/Users/ryanf/AppData/Local/Temp/pixl readiness claude clean 7x5frzoi/consumer. Kit: C:/Users/ryanf/AppData/Local/Temp/pixl readiness claude clean 7x5frzoi/consumer/installed pixl.
Selected Python: C:/github/pixel-lab-agent/build/readiness-setup-01/runtime/Scripts/python.exe. Read RECOVERY-ASSIGNMENT.md and the assigned phase file.
The actual named pixl:pixl specialist is required.
The local PIXL server and originating pixellab-recovery-test fixture are separate.
Only that controlled fixture is configured; no real provider or paid work is assigned.
Work only inside this consumer. Do not inspect evaluator backing files outside it,
credentials, host settings or memory; do not install packages or modify the kit.
Keep provider_simulated=true. Human acceptance and artistic/engine acceptance are
separate and unperformed; do not let a generic human-approval gate halt recovery.

# Assigned recovery phase 2

Cold-read the previous partial handoff and actual saved jobs/state.
Keep unresolved-job unknown. The old download URL belonged to an ended connection;
re-query the SAME saved provider/job ID for this connection's fresh result URL.
Download the complete returned PNG to work/provider-recovery/phase-2/retrieved.png. Verify actual byte length,
SHA-256 and PNG decoding against the originating response. Do not copy reference
pixels as recovered output. Preserve phase1's partial bytes and error untouched.
Import through public job-import using job=recoverable-job, output=recovered-avatar, candidate=recovered-avatar-candidate.
Retain the import evidence you supplied in work/provider-recovery/phase-2/import-evidence.json and full return
in work/provider-recovery/phase-2/import-result.json. Obtain its actual retained candidate path/hash from
current public state/job reports; no acceptance is granted by import. Return that
file to the caller. Caller independently reads/hashes the actual candidate, opens
it with an available image tool, checks src/avatar.ts, and copies exact bytes to
assets/robot.png. Return status='recovered' with visual/engine acceptance unperformed.

Both participants must read the full current public jobs report, saved as
work/provider-recovery/phase-2/jobs-before.json by the specialist and work/provider-recovery/phase-2/jobs-after.json after its work.
The caller independently retrieves its own current report as work/provider-recovery/phase-2/caller-jobs.json.
The specialist writes work/provider-recovery/phase-2/SPECIALIST-RESULT.json; caller writes
work/provider-recovery/phase-2/CALLER-RESULT.json after actual child completion and independent consumption.
Each report includes phase, status, provider_simulated=true, job, remote_id,
unresolved_job, unresolved_state, candidate (null or {id,output,path,sha256}),
state ({path,sha256,canonical_hash,revision}), evidence_refs (actual path/sha256),
limitations and next_action. The caller also includes native_child and a file
reference to specialist_result. File paths are consumer-relative; hashes are actual
SHA-256. Preserve supplied schema/value meanings. Do not claim live PixelLab,
new artistic quality, target-engine or human acceptance. M1/M2 and broader M3/M4
remain open. Return useful exact files and recovery status, not just a plan.
