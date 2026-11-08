"""Caller helper (second save): restore queue.ready `existing` to its requirement-time bytes.

The runtime's requirements identity (_requirements) excludes only status/next/evidence/production,
so the first delivery save's edit to `existing` changed requirements_hash 244f4591... -> 8c1a69e2...
and made the completed generation's selection read as 'changed'. Nothing the generation was reviewed
against changed. This save restores the prior `existing` entry exactly, records the delivered file
under `evidence` (excluded from the hash) and amends `next`. No other row or field changes.

Run from the consumer root:
  python -I work/queue.ready/caller/plar-update-delivery2.py work/queue.ready/caller/plar-update-delivery2.json
"""
import hashlib
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
doc = json.loads(Path("plar.txt").read_text(encoding="utf-8"))
prior = json.loads(Path(".pixl/plar-history/32e1590fc1220abe61d23f0193a739e52644bcab093c2bf98b13c368adab5e85.json").read_text(encoding="utf-8"))
before = json.loads(json.dumps(doc))
row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
prior_row = next(a for a in prior["assets"] if a["id"] == "queue.ready")


def sha(rel):
    return hashlib.sha256(Path(rel).read_bytes()).hexdigest()


CAND = sha("assets/ready-confirmed.png")
assert CAND == "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"

row["existing"] = json.loads(json.dumps(prior_row["existing"]))
row["evidence"].append({
    "path": "assets/ready-confirmed.png",
    "note": (
        f"Delivered file at the PLAR destination: exact bytes of nominated candidate r.028f320bf7292612.candidate.ready "
        f"(sha256 {CAND}, 210 bytes, 16x16 RGBA, 1 frame), byte-identical to the retained PX2 artifact and to the "
        "controlled-create-0002 download (evaluator fixture from pixellab-test, provider_simulated=true). The `existing` "
        "entry above is deliberately left at its requirement-time text because the runtime includes `existing` in "
        "requirements_hash; the file's presence is reported by the reader, not by that prose."
    ),
})
row["next"] = (
    "Delivered: r.028f320bf7292612.task is done (store revision 17, hash fc545519...), candidate "
    "r.028f320bf7292612.candidate.ready passed all eight rev3 criteria (review r.028f320bf7292612.review1) and its "
    "exact bytes are at assets/ready-confirmed.png (see evidence); node verify-integration.mjs confirmed statusCell and "
    "compactStatus resolve succeeded -> Ready -> this path with frames 1 and a 16x16 PNG header. The image is an "
    "evaluator fixture from the controlled pixellab-test connection (controlled-create-0002), not upstream PixelLab art. "
    "Requirements are unchanged since the reviewed contract (requirements_hash 244f4591...); the `existing` entry keeps "
    "its requirement-time wording so that identity is preserved. Remaining: (1) record the Ready representative-sample "
    "style decision and source-bind the approved reference before expanding queue.working, queue.retry and "
    "queue.paused; (2) exercise statusCell/compactStatus in an actual renderer when one exists (none supplied; "
    "unverified); (3) run the family distinction reviews (Working not success; Retry and Paused distinguishable without "
    "colour) once those assets exist. Do not reuse controlled-create-0002 on a real PixelLab service; any further Ready "
    "generation needs a new, separately authorized request. Earlier tasks 'task' and r.f9e2fa53f4fcac2a.task remain "
    "open history with plar_selection blockers."
)

# Guards: only queue.ready existing/evidence/next changed; existing now equals the prior version exactly.
for a_old, a_new in zip(before["assets"], doc["assets"]):
    if a_old["id"] != "queue.ready":
        assert a_old == a_new, a_old["id"]
    else:
        for k in a_old:
            if k not in ("existing", "next", "evidence"):
                assert a_old[k] == a_new[k], k
for k in before:
    if k != "assets":
        assert before[k] == doc[k], k
assert row["existing"] == prior_row["existing"]
req_keys = [k for k in prior_row if k not in ("status", "next", "evidence", "production")]
assert all(prior_row[k] == row[k] for k in req_keys), "requirement-identity fields differ from the reviewed version"
out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, hashlib.sha256(out.read_bytes()).hexdigest())
