"""Phase-2 retrieval of the originating fixture resource.

Retries retrieval (never submission) of the fresh download URL until the complete
expected byte count arrives, preserving every partial attempt under a distinct
name and retaining exact curl stdout/stderr/exit codes with host-clock timestamps.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

root = sys.argv[1]
url = sys.argv[2]
expected_bytes = int(sys.argv[3])
expected_sha = sys.argv[4]
max_attempts = int(sys.argv[5])

phase = os.path.join(root, "work", "provider-recovery", "phase-2")
target = os.path.join(phase, "retrieved.png")
log_path = os.path.join(phase, "download-log.json")
curl = shutil.which("curl.exe") or shutil.which("curl")


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


version = subprocess.run([curl, "--version"], capture_output=True, text=True)
attempts = []
complete = False
for n in range(1, max_attempts + 1):
    tmp = os.path.join(phase, f"retrieved.attempt{n}.download")
    cmd = [curl, "--fail", "--show-error", "--silent", "--output", tmp, url]
    started = now()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    finished = now()
    size = os.path.getsize(tmp) if os.path.exists(tmp) else None
    digest = sha256(tmp) if size else None
    ok = proc.returncode == 0 and size == expected_bytes and digest == expected_sha
    rec = {
        "attempt": n,
        "command": cmd,
        "started_at": started,
        "finished_at": finished,
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "bytes": size,
        "sha256": digest,
        "complete": ok,
    }
    if ok:
        os.replace(tmp, target)
        rec["retained_as"] = "work/provider-recovery/phase-2/retrieved.png"
        complete = True
    elif size:
        part = os.path.join(phase, f"retrieved.attempt{n}.part")
        os.replace(tmp, part)
        rec["retained_as"] = f"work/provider-recovery/phase-2/retrieved.attempt{n}.part"
    else:
        if os.path.exists(tmp):
            os.remove(tmp)
        rec["retained_as"] = None
    attempts.append(rec)
    if ok:
        break

log = {
    "phase": 2,
    "provider_simulated": True,
    "job": "recoverable-job",
    "remote_id": "controlled-recovery-0001",
    "output": "recovered-avatar",
    "url": url,
    "url_source": "work/provider-recovery/phase-2/provider-get-image.json images[0].download_url (fresh loopback URL from this connection's get_image re-query of the same job ID)",
    "tool": curl,
    "tool_version": version.stdout.splitlines()[0] if version.stdout else version.stderr,
    "timestamp_source": "host clock via selected Python datetime.now(timezone.utc) immediately before and after each curl invocation",
    "expected": {"bytes": expected_bytes, "sha256": expected_sha, "width": 32, "height": 32, "format": "png"},
    "attempts": attempts,
    "complete": complete,
    "retained_path": "work/provider-recovery/phase-2/retrieved.png" if complete else None,
    "written_at": now(),
}
with open(log_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(log, f, indent=2)
    f.write("\n")
print(json.dumps({"complete": complete, "attempts": len(attempts), "last": attempts[-1]}, indent=2))
