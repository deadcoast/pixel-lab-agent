"""Build work/continuation/PHASE2-CALLER.json for CONTINUATION-ASSIGNMENT.md phase 2 (native same-child reconciliation).

Reads SPECIALIST-ROUND2.json and the caller-authored phase2-assessment-input.json, hashes inputs/outputs, re-hashes the
whole tree against the phase-1 baseline (nothing outside work/continuation may change) and the phase-2 baseline of
work/continuation (no phase-1 output may change), and records the native continuation evidence and dispositions.
Usage: python -I work/continuation/build_phase2.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
CONT = "work/continuation"
OUT = f"{CONT}/PHASE2-CALLER.json"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


inp = load(f"{CONT}/phase2-assessment-input.json")
phase1 = load(f"{CONT}/PHASE1-CALLER.json")
review = load(f"{CONT}/CALLER-REVIEW-01.json")
round1 = load(f"{CONT}/SPECIALIST-ROUND1.json")
round2 = load(f"{CONT}/SPECIALIST-ROUND2.json")

# identities expected from phase 1
expected = {
    f"{CONT}/CALLER-REVIEW-01.json": phase1["caller_review"]["sha256"],
    f"{CONT}/SPECIALIST-ROUND1.json": phase1["specialist_round1"]["sha256"],
    "work/focused-successor/specialist-proposal.json": review["identities"]["proposal"]["sha256"],
    ".pixl/assets/queue.ready/state.px": review["identities"]["state"]["sha256"],
}
for path, digest in expected.items():
    if sha(path) != digest:
        sys.exit(f"input identity changed: {path}")

# preservation: outside work/continuation against the phase-1 baseline; inside against the phase-2 baseline (phase-1 files)
baseline = load(f"{CONT}/baseline-hashes.json")["files"]
current = {}
for base, dirs, names in os.walk(ROOT):
    rel_base = os.path.relpath(base, ROOT).replace(os.sep, "/")
    dirs[:] = [d for d in dirs if d != "__pycache__" and not (rel_base == "work" and d == "continuation")]
    for name in names:
        rel = os.path.relpath(os.path.join(base, name), ROOT).replace(os.sep, "/")
        current[rel] = sha(os.path.join(base, name))
outside = {
    "changed": [r for r, d in baseline.items() if r in current and current[r] != d],
    "missing": [r for r in baseline if r not in current],
    "added": [r for r in current if r not in baseline],
}
p2base = load(f"{CONT}/phase2-baseline-continuation-hashes.json")["files"]
inside_changed = [r for r, d in p2base.items() if not os.path.exists(r) or sha(r) != d]
preservation = {
    "outside_work_continuation": {"baseline": f"{CONT}/baseline-hashes.json", "files": len(baseline), **outside, "unchanged": not any(outside.values())},
    "phase1_files_under_work_continuation": {"baseline": f"{CONT}/phase2-baseline-continuation-hashes.json", "files": len(p2base), "changed_or_missing": inside_changed, "unchanged": not inside_changed},
}
if any(outside.values()) or inside_changed:
    print(json.dumps(preservation, indent=1))
    sys.exit("preservation violated; refusing to report")

new_files = {}
for base, _, names in os.walk(CONT):
    for name in sorted(names):
        rel = os.path.join(base, name).replace(os.sep, "/")
        if rel not in p2base and rel != OUT:
            new_files[rel] = sha(rel)

phase = {
    "version": 1,
    "kind": "phase2-caller-result",
    "assignment": {"path": "CONTINUATION-ASSIGNMENT.md", "sha256": sha("CONTINUATION-ASSIGNMENT.md"), "phase": 2},
    "native_child": inp["native_child"],
    "native_continuation_established": inp["native_continuation_established"],
    "inputs": {path: digest for path, digest in expected.items()} | {f"{CONT}/PHASE1-CALLER.json": sha(f"{CONT}/PHASE1-CALLER.json")},
    "outputs": {"specialist_round2": {"path": f"{CONT}/SPECIALIST-ROUND2.json", "sha256": sha(f"{CONT}/SPECIALIST-ROUND2.json")}, "new_files_this_phase": new_files},
    "specialist_round2_summary": inp["specialist_round2_summary"],
    "caller_checks_on_round2": inp["caller_checks_on_round2"],
    "findings": inp["findings"],
    "remaining_disagreements": inp["remaining_disagreements"],
    "remaining_decisions": inp["remaining_decisions"],
    "preservation": preservation,
    "not_done_by_design": [
        "no production adoption, renderer execution, new art acceptance, state commit, PLAR write, job action, inspection packet or PixelLab call",
        "original proposal, 20 Q records, state.px revision 88, assets, historical results and every phase-1 output unchanged",
        "M1 mapping alternative and broader host reliability remain open",
    ],
    "next_action": inp["next_action"],
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    json.dump(phase, handle, indent=1, ensure_ascii=False)
    handle.write("\n")
print(json.dumps({"out": OUT, "sha256": sha(OUT), "new_files": len(new_files), "preservation_ok": True}))
