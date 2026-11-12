"""Author the adoption decision D with its proof receipt E and the destination choices.
Usage: python -I author_decision.py ROOT KIT_RUNTIME OUT_WIRE
Computes exact record hashes with the bundled runtime (read-only import); no provider action."""
import json, hashlib, sys
from datetime import datetime, UTC
from pathlib import Path
root, runtime, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(runtime))
from pixl import codec, graph, store
from pixl.codec import Ref, Symbol, Record
doc = store.load(root / ".pixl/assets/robot.directions")
G = "r.acf329804ba043b7."
now = datetime.now(UTC).isoformat(timespec="seconds")
def rev(path):
    j = json.loads((root / path).read_text(encoding="utf-8")); return {"path": path, "sha256": hashlib.sha256((root/path).read_bytes()).hexdigest(), "review": j.get("review"), "state_hash": j.get("state_hash")}
proof = {
  "version": 1, "kind": "method proof for decision adopt_rotation", "written_at": now,
  "method": "Reference-conditioned PixelLab V3 rotation of the exact approved south frame (create_object_pro_flash, first_frame_url = uploaded source bytes, n_directions 8, view side, palette = source colours) to obtain east/north/west; exact byte reuse for south; deterministic local mirror of the accepted east when the provider's west lacks the front edge.",
  "executed_on": {"job": G + "request", "object_id": "2a3cb51a-6cf7-485d-8441-3c3db762cc9d", "background_job_id": "ea834364-0f7d-42eb-876b-bb26e21e1269", "generations_consumed": 1, "source_sha256": "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7"},
  "outcome": {
    "east": {"candidate": "candidate.east.raw", "sha256": "71b35089965b6457f505d569f4fc89fbcc2521bf188aa43f836dc207c3771fb4", "provenance": "generated", "verdicts": "10/10 pass", "review": rev("work/native-production/reviews/review-east-raw-01.result.json")},
    "north": {"candidate": "candidate.north.raw", "sha256": "db516f78a836f89b618ba00cfac0d2373f260ae3923b6198f17c62ab957ba3f5", "provenance": "generated", "verdicts": "10/10 pass", "review": rev("work/native-production/reviews/review-north-raw-01.result.json")},
    "west_raw": {"candidate": "candidate.west.raw", "sha256": "8209e5f6bc71d22eb76a6aa98b8bf08ffcfea46aafaf0bd056e649d64980f84c", "provenance": "generated, rejected", "verdicts": "identity fail, direction fail, 8 pass", "review": rev("work/native-production/reviews/review-west-raw-01.result.json")},
    "west_edited": {"candidate": "candidate.west.edited", "sha256": "ec96bf6379daf161ce8643894b72c50b4bb543e105f336cbc58f27293df655a0", "provenance": "edited (mirror of candidate.east.raw)", "verdicts": "10/10 pass", "review": rev("work/native-production/reviews/review-west-edited-01.result.json")},
    "south": {"candidate": "candidate.south", "sha256": "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7", "provenance": "reused source bytes", "verdicts": "2/2 pass", "review": rev("work/native-production/reviews/review-south-01.result.json")}},
  "conclusion": "The method produced identity-preserving east and north views at 1 generation; west needed a deterministic mirror of the accepted east. Adopted for this family with that limitation recorded; the raw west is retained as rejected. This proof is the specialist's retained summary of actual reviewed results, not provider attestation.",
  "limitations": ["One sample on one 32x32 symmetric sprite; not a general claim about the tool.", "The provider's west required a local edit; a different seed or Pro rotate could be tried at extra cost if an unedited west is ever required."]}
pf = root / "work/native-production/decision/method-proof.json"
pf.write_text(json.dumps(proof, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
pdg = hashlib.sha256(pf.read_bytes()).hexdigest()
S = lambda n: Ref(G + f"source.{n}")
new = [
 Record("destination.paths", "I", {"pr": Ref("project"), "wh": Ref("actor"), "ky": "destination.paths", "st": Symbol("confirmed"),
   "vl": {"south": "assets/robot/south.png", "east": "assets/robot/east.png", "north": "assets/robot/north.png", "west": "assets/robot/west.png"},
   "so": [S(6), S(8)], "wy": "src/robot.ts robotSprites maps each Facing to these exact files; BRIEF.md requires separate PNGs under assets/robot/."}),
 Record("destination.sampling", "I", {"pr": Ref("project"), "wh": Ref("actor"), "ky": "destination.sampling", "st": Symbol("confirmed"),
   "vl": {"sampling": "nearest", "cell": [32, 32]}, "so": [S(6)], "wy": "src/robot.ts cell = {width 32, height 32, sampling nearest}."}),
 Record("adopt_rotation", "D", {"wh": Ref("actor"),
   "wt": "Adopt for the robot.directions family: exact byte reuse of the approved south; reference-conditioned PixelLab V3 object rotation (create_object_pro_flash with the uploaded source as first frame, n_directions 8, view side, source palette) for east and north; and a deterministic horizontal mirror of the accepted east for west, because the provider's west omitted the front edge.",
   "wr": [Ref("candidate.south"), Ref("candidate.east.raw"), Ref("candidate.north.raw"), Ref("candidate.west.edited"), Ref(G+"contract.east"), Ref(G+"contract.north"), Ref(G+"contract.west")],
   "wy": "The reviewed representative sample (job " + G + "request, object 2a3cb51a-6cf7-485d-8441-3c3db762cc9d, 1 generation) passed every saved criterion for east, north and the edited west, and the raw west failed direction/identity; the mirror is geometrically exact for this left-right-symmetric design. Scoped to this family; not a general method claim.",
   "rs": [S(8), S(6), S(7), S(3), Ref("source.comparison")], "pc": [Ref("proof.adopt_rotation")]}),
]
for r in new: doc.records[r.id] = r
proj = doc.records["project"]; proj.fields["in"] = proj.fields["in"] + [Ref("destination.paths"), Ref("destination.sampling")]
scope = graph.proof_scope(doc, ["adopt_rotation"])
bs = [{"rf": Ref(i), "dg": codec.record_hash(doc.records[i])} for i in sorted(scope)]
doc.records["proof.adopt_rotation"] = Record("proof.adopt_rotation", "E", {"nm": "Retained sample result summary proving the adopted rotation method for this family", "ur": pf.relative_to(root).as_posix(), "dg": pdg, "rs": Symbol("pass"), "md": Symbol("local"), "at": now, "bs": bs})
doc.revision += 1
out.write_bytes(codec.encode(doc))
print("scope size", len(scope), "revision", doc.revision, "proof file sha", pdg)
print(sorted(scope))
