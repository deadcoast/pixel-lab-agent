"""Update only hash-excluded fields (next, evidence) of the queue.ready PLAR row and save via the bundled CLI."""
import copy
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(r"C:\github\pixel-lab-agent\evidence\handoff-repair\20261108\native\claude-03\project")
RUNNER = ROOT / ".agents" / "skills" / "pixl-kit" / "scripts" / "pixl.py"
EXPECT = "1794e17cdc7b3c0dac61f4c6aa1c711091a4f66468d4dff39b6795b4a5542606"

raw = (ROOT / "plar.txt").read_bytes()
old_hash = hashlib.sha256(raw).hexdigest()
print("old plar hash", old_hash)
assert old_hash == EXPECT, "plar.txt changed since reading; aborting"

doc = json.loads(raw.decode("utf-8"))
row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
before = copy.deepcopy(row)

row["next"] = (
    "reassess_handoff: PIXL reassessment (work/queue.ready-handoff/) corrected the citation bounds, "
    "connection binding and extent wording of the delivery contract in a new proposal packet "
    "(sha256 14eb7e3eb53a78e4393425fcd800b5355935adb1c5880e06ee2d1978befc47e9) with zero evidence "
    "diagnostics; the historical contract, verdicts and PX2 state (revision 14, "
    "7a97831f618ffe1c761c0f839525bf4d763eacb56c7fb05b26f15f9ad3da1a81) are unchanged and the bounded "
    "Ready fixture delivery remains complete. Next: the caller independently compares the corrected "
    "packet with the sources; the owner/caller records the style-baseline decision (BRIEF.md line 5) "
    "and source-binds the approved Ready bytes before Working/Retry/Paused expansion; supply a graphical "
    "renderer to verify full/compact display and alpha compositing. No new request assigned; preserve "
    "pixellab-test fixture provenance and all old history."
)

new_evidence = [
    ("work/queue.ready-handoff/request-review.json",
     "Reassessment-stage corrected proposal packet (sha256 14eb7e3eb53a78e4393425fcd800b5355935adb1c5880e06ee2d1978befc47e9): "
     "file-local citation bounds, request.provider/connection bound to work/queue.ready-revision/connection.json, "
     "historical_contract block. Does not replace the delivery contract or re-verdict ready.retained; no new request."),
    ("work/queue.ready-handoff/candidate-plan.json",
     "Corrected criteria proposal (sha256 a22f704dfd4432f2750cfacb7a37efda98925d1da40830981cb07da3a88baa3f); six historical "
     "criterion IDs retained; cool-blue dominance demoted to a specialist choice; no verdicts recorded against it."),
    ("work/queue.ready-handoff/candidate-plan-changes.json",
     "Explicit old-to-new criterion change log with source obligation, literal additions, discriminating alternative and "
     "disposition (sha256 a4629aa44561944a1e929232b4ea8b564f1ffacd7e6b931eb1cd422bf5ece40c)."),
    ("work/queue.ready-handoff/request-review-report.json",
     "pixl_request_review evidence report on the corrected packet: zero diagnostics, 44 resolved excerpts, production "
     "revision 14 hash 7a97831f... selection_current true (sha256 b762493f42fd14b122739f4ce584ef1582d06eda26bbaef023abdba2c765a341)."),
    ("work/queue.ready-handoff/specialist-assessment.json",
     "PIXL pixel-art assessment of the delivered fixture: measured pixel map, arm asymmetry, edge rhythm, 3x integer "
     "presentation, contrast diagnostic, viewed native/1x/3x views, family-extension guidance as proposals "
     "(sha256 9ed5ee872d6c493c67fea746f1345618b7b2fad48429e87ecd0bf62b8f3b892b). Not acceptance evidence."),
    ("work/queue.ready-handoff/integration-recheck.json",
     "Re-executed node verify-integration.mjs assets/ready-confirmed.png in this consumer: exit 0, same result object as "
     "the delivery-stage integration.json; not a renderer (sha256 fe5de0a3a1e00437581e4d94ee180e14aefd4706a4d06ac520823e3b750c44ed)."),
]
for path, note in new_evidence:
    row["evidence"].append({"path": path, "note": note})

changed = [k for k in row if row[k] != before.get(k)]
print("changed keys", changed)
assert set(changed) <= {"next", "evidence"}, "only next/evidence may change"

doc_path = ROOT / "work" / "queue.ready-handoff" / "plar-document.json"
doc_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

result = subprocess.run(
    [sys.executable, "-I", str(RUNNER), "plar", "save", str(doc_path), "--root", str(ROOT), "--expect", EXPECT],
    capture_output=True, text=True,
)
print("SAVE rc", result.returncode)
print(result.stdout[:4000])
print("STDERR", result.stderr[:2000])
print("new plar hash", hashlib.sha256((ROOT / "plar.txt").read_bytes()).hexdigest())
