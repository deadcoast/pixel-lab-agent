"""Revision 2: update only hash-excluded fields (next, evidence) of the queue.ready PLAR row and save via the bundled CLI.

CAS: expect = the plar.txt hash verified by the caller (0ede0be8...). Re-reads and aborts if the bytes moved.
Appends evidence for the four revision-2 files and re-points `next` at the revision-2 packet.
No other field of any row changes; requirements_hash 806a1f2d... must remain unchanged (checked afterwards by plar read).
"""
import copy
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(r"C:\github\pixel-lab-agent\evidence\handoff-repair\20261108\native\claude-03\project")
RUNNER = ROOT / ".agents" / "skills" / "pixl-kit" / "scripts" / "pixl.py"
REV2 = ROOT / "work" / "queue.ready-handoff" / "revision-2"
EXPECT = "0ede0be80131e8c4b071fe06fb4318d69148a4f80282d3b95c49f9f3e377df20"

FILES = {
    "packet": REV2 / "request-review.json",
    "plan": REV2 / "candidate-plan.json",
    "changes": REV2 / "candidate-plan-changes.json",
    "report": REV2 / "request-review-report.json",
}
H = {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in FILES.items()}
for k, v in H.items():
    print(k, v)

raw = (ROOT / "plar.txt").read_bytes()
old_hash = hashlib.sha256(raw).hexdigest()
print("old plar hash", old_hash)
assert old_hash == EXPECT, "plar.txt changed since reading; aborting"

doc = json.loads(raw.decode("utf-8"))
row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
before = copy.deepcopy(row)
others_before = copy.deepcopy([a for a in doc["assets"] if a["id"] != "queue.ready"])

row["next"] = (
    "reassess_handoff (revision 2): the caller independently compared the revision-1 corrected packet "
    "(work/queue.ready-handoff/request-review.json, sha256 14eb7e3eb53a78e4393425fcd800b5355935adb1c5880e06ee2d1978befc47e9) "
    "with the sources and returned two findings; PIXL resolved both in the revision-2 packet "
    f"work/queue.ready-handoff/revision-2/request-review.json (sha256 {H['packet']}): the OWNER.md locator "
    "'lines 8-9' is corrected to 'lines 8-10' (the cited clause 'art acceptance remain future work' is on line 10) and the "
    "ready-meaning basis now states explicitly that '(one arm clearly shorter than the other)' is the specialist's reading "
    "of the owner's 'asymmetrical arms', that an equal-arm V with unequal stroke weight is not a check mark, and that no arm "
    "ratio is imposed. Revision 1 is superseded for that locator fix and basis clarification but retained byte-for-byte; "
    "zero evidence diagnostics on revision 2. The historical contract, verdicts and PX2 state (revision 14, "
    "7a97831f618ffe1c761c0f839525bf4d763eacb56c7fb05b26f15f9ad3da1a81) are unchanged and the bounded Ready fixture "
    "delivery remains complete. Next: the caller inspects the revision-2 packet and records its review at "
    "work/queue.ready-handoff/caller-review.json; the owner/caller records the style-baseline decision (BRIEF.md line 5) "
    "and source-binds the approved Ready bytes before Working/Retry/Paused expansion; supply a graphical renderer to verify "
    "full/compact display and alpha compositing. No new request assigned; preserve pixellab-test fixture provenance and all old history."
)

new_evidence = [
    ("work/queue.ready-handoff/revision-2/request-review.json",
     f"Revision-2 corrected proposal packet (sha256 {H['packet']}); supersedes revision 1 (14eb7e3e...) for the OWNER.md "
     "locator fix (lines 8-9 -> 8-10) and the ready-meaning basis clarification requested by the caller's independent comparison; "
     "request still bound to the historical provider-arguments.json / connection.json; no new request, no re-verdict."),
    ("work/queue.ready-handoff/revision-2/candidate-plan.json",
     f"Revision-2 corrected criteria proposal (sha256 {H['plan']}); identical to revision 1 (a22f704d...) except the ready-meaning "
     "basis, which now attributes '(one arm clearly shorter than the other)' to the specialist's reading of 'asymmetrical arms' "
     "and states that no arm ratio is imposed; schema-valid; no verdicts recorded against it."),
    ("work/queue.ready-handoff/revision-2/candidate-plan-changes.json",
     f"Revision-2 change log (sha256 {H['changes']}); revision-1 per-criterion comparisons retained plus a revision_2 section for the "
     "basis clarification and the packet locator fix."),
    ("work/queue.ready-handoff/revision-2/request-review-report.json",
     f"pixl request-review evidence report on the revision-2 packet: zero diagnostics, 44 resolved excerpts, OWNER.md excerpt at "
     f"lines 8-10, production revision 14 hash 7a97831f... selection_current true (sha256 {H['report']})."),
]
for path, note in new_evidence:
    row["evidence"].append({"path": path, "note": note})

changed = [k for k in row if row[k] != before.get(k)]
print("changed keys", changed)
assert set(changed) <= {"next", "evidence"}, "only next/evidence may change"
assert others_before == [a for a in doc["assets"] if a["id"] != "queue.ready"], "other rows must not change"
assert len(row["evidence"]) == len(before["evidence"]) + 4

doc_path = REV2 / "plar-document.json"
doc_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

result = subprocess.run(
    [sys.executable, "-I", str(RUNNER), "plar", "save", str(doc_path), "--root", str(ROOT), "--expect", EXPECT],
    capture_output=True, text=True,
)
print("SAVE rc", result.returncode)
print(result.stdout[:4000])
print("STDERR", result.stderr[:2000])
print("new plar hash", hashlib.sha256((ROOT / "plar.txt").read_bytes()).hexdigest())
print("document hash", hashlib.sha256(doc_path.read_bytes()).hexdigest())
