"""Additive recovery after the recorder exited while its native caller continued.

Run only after observing the original process absent and a complete native stream.
This does not launch, resume, edit or rerun the consumer, and cannot recover an OS
exit code. The original progress files and recorder source remain unchanged.
"""
import json
import types
from pathlib import Path

from evaluations.artistic_revision_case import retain_outputs
from evaluations.host_trials import inventory, sha, write_json
from evaluations.request_review_trials import retain_journals

attempt = Path(__file__).resolve().parent.parent
recovery = Path(__file__).resolve().parent
original_source = attempt / "native_trial_records.py.txt"
original = types.ModuleType("frozen_recording_recovery")
original.__file__ = str(original_source)
exec(compile(original_source.read_bytes(), str(original_source), "exec"), original.__dict__)
launch = json.loads((attempt / "launch.json").read_bytes())
events = [json.loads(line) for line in (attempt / "stdout.jsonl").read_text(encoding="utf-8").splitlines()]
if events[-1].get("type") != "turn.completed":
    raise ValueError("Native stream has no final turn.completed observation")
if (attempt / "record.json").exists() or (recovery / "continuation.json").exists():
    raise ValueError("Recovery already retained; do not replace evidence")
preserved = {name: sha(attempt / name) for name in ("continuation.json", "continuation.json.tmp", "native_trial_records.py.txt")}
retain_journals(attempt, events)
journal = original.AttemptRecord(attempt, launch, {})
journal.data["started_at"] = json.loads((attempt / "continuation.json").read_bytes())["started_at"]
journal.data["recording_recovery"] = {
    "method": "Additive parsing of completed original stream and retained native journals; no process restart",
    "original_recorder_failed": True,
    "native_os_exit_code": "unknown; not inferred from turn.completed",
    "native_pid_observed_running_after_recorder_exit": 68652,
    "native_process_observed_absent_before_recovery": True,
    "preserved_originals": preserved,
}
continuation = journal.snapshot("finished", returncode=None, interruption="recording_error", output=recovery / "continuation.json")
retain_outputs(attempt)
write_json(attempt / "record.json", {
    "host": launch["host"], "case": launch["case"], "returncode": None,
    "execution_status": "native_turn_completed_after_recorder_failure",
    "behavioral_verdict": "ungraded", "elapsed_seconds": None,
    "continuation": {"path": "recording-recovery/continuation.json", "sha256": sha(recovery / "continuation.json"),
                     "interruption_reason": "recording_error"},
    "artifacts": inventory(Path(launch["cwd"]), ("__pycache__",)),
    "recorded_files": inventory(attempt, ("record.json",)),
    "recovery": {"script_sha256": sha(Path(__file__)), "frozen_recorder_sha256": sha(original_source),
                 "no_relaunch": True, "original_progress_preserved": preserved},
})
assert all(sha(attempt / name) == digest for name, digest in preserved.items())
print(json.dumps({"status": "retained_after_recording_failure", "session_id": continuation["session_id"],
                  "children": [row["id"] for row in continuation["children"]], "returncode": None}))
