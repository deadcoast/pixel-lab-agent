"""Build work/continuation/PHASE1-CALLER.json for CONTINUATION-ASSIGNMENT.md phase 1.

Reads the retained outputs (SPECIALIST-ROUND1.json, CALLER-REVIEW-01.json), hashes them, re-hashes every retained
file against work/continuation/baseline-hashes.json to prove nothing outside work/continuation changed, and records
the native child ID, the caller's independent assessment of the specialist and the exact follow-up for that child.
Usage: python -I work/continuation/build_phase1.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
OUT = "work/continuation/PHASE1-CALLER.json"
CONT = "work/continuation"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


ASSESSMENT_PATH = os.path.join(CONT, "phase1-assessment-input.json")
assessment = load(ASSESSMENT_PATH)  # caller-authored: child id, specialist assessment, follow-up
review = load(os.path.join(CONT, "CALLER-REVIEW-01.json"))
round1 = load(os.path.join(CONT, "SPECIALIST-ROUND1.json"))

# preservation: every file hashed at phase start must be unchanged; new files appear only under work/continuation
baseline = load(os.path.join(CONT, "baseline-hashes.json"))["files"]
changed, missing, added = [], [], []
current = {}
for base, dirs, names in os.walk(ROOT):
    rel_base = os.path.relpath(base, ROOT).replace(os.sep, "/")
    dirs[:] = [d for d in dirs if d != "__pycache__" and not (rel_base == "work" and d == "continuation")]
    for name in names:
        rel = os.path.relpath(os.path.join(base, name), ROOT).replace(os.sep, "/")
        current[rel] = sha(os.path.join(base, name))
for rel, digest in baseline.items():
    if rel not in current:
        missing.append(rel)
    elif current[rel] != digest:
        changed.append(rel)
for rel in current:
    if rel not in baseline:
        added.append(rel)
preservation = {
    "baseline": {"path": os.path.join(CONT, "baseline-hashes.json").replace(os.sep, "/"), "sha256": sha(os.path.join(CONT, "baseline-hashes.json")), "files": len(baseline)},
    "unchanged": not changed and not missing and not added,
    "changed": changed, "missing": missing, "added_outside_work_continuation": added,
    "note": "baseline hashed at phase start (before any child or caller write); excludes work/continuation and __pycache__",
}
if changed or missing or added:
    print(json.dumps(preservation, indent=1))
    sys.exit("retained files changed; refusing to report preservation")

outputs = {}
for name in sorted(os.listdir(CONT)):
    path = os.path.join(CONT, name)
    if os.path.isdir(path):
        for base, _, names in os.walk(path):
            for inner in sorted(names):
                p = os.path.join(base, inner)
                outputs[os.path.relpath(p, ROOT).replace(os.sep, "/")] = sha(p)
    elif name != "PHASE1-CALLER.json":
        outputs[os.path.relpath(path, ROOT).replace(os.sep, "/")] = sha(path)

phase = {
    "version": 1,
    "kind": "phase1-caller-result",
    "assignment": {"path": "CONTINUATION-ASSIGNMENT.md", "sha256": sha("CONTINUATION-ASSIGNMENT.md"), "phase": 1, "status": "phase 1 complete: specialist round 1 retained, independent caller review retained; reconciliation deferred to the next invocation by design"},
    "restart": "artifact-based restart of the interrupted focused-authoring comparison (the earlier child, launched with persistence disabled, is not resumed). Its grade and files under work/focused-successor are unchanged.",
    "native_child": assessment["native_child"],
    "specialist_round1": {"path": f"{CONT}/SPECIALIST-ROUND1.json", "sha256": sha(f"{CONT}/SPECIALIST-ROUND1.json"), "kind": round1.get("kind"), "defects": len(round1.get("defects", [])), "status": round1.get("status") or round1.get("assessment", {}).get("status")},
    "caller_review": {"path": f"{CONT}/CALLER-REVIEW-01.json", "sha256": sha(f"{CONT}/CALLER-REVIEW-01.json"), "verdict": review["verdict"]},
    "identities": review["identities"],
    "outputs": outputs,
    "independent_assessment_of_specialist": assessment["independent_assessment_of_specialist"],
    "follow_up_for_same_child": assessment["follow_up_for_same_child"],
    "preservation": preservation,
    "tools_with_side_effects": "none beyond creating files under work/continuation; MCP calls were read-only (pixl_validate, pixl_request_review with result_path under work/continuation, pixl_plar_read); no PixelLab call, no commit, no job or PLAR write; global settings and memory untouched",
    "open": [
        "Reconciliation of CALLER-REVIEW-01.json by the same native child (next invocation).",
        "Production/rendering remain separate: no successor capture, check.py run, plan authoring, job resolution or acceptance was performed.",
        "Owner decision on frozen-spinner semantics (P1) versus a new static glyph (P2).",
        "M1 mapping alternative and broader host reliability remain open; same-child continuation is not claimed as tested until the next invocation actually resumes it.",
    ],
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    json.dump(phase, handle, indent=1, ensure_ascii=False)
    handle.write("\n")
print(json.dumps({"out": OUT, "sha256": sha(OUT), "outputs": len(outputs), "preservation_unchanged": preservation["unchanged"]}))
