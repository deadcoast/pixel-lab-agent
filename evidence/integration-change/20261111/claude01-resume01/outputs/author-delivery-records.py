"""Author the confirmed destination choice, adoption decision and its proof receipt on top of the decoded
revision-9 state, binding the receipt to the exact canonical record hashes of the decision's semantic closure.
Also author the stages:[] delivery plan JSON. Local file authoring only; publication happens through the public commit."""
import datetime
import hashlib
import json
import sys

sys.path.insert(0, "installed pixl/runtime")
from pixl import codec, graph, service  # noqa: E402

W = "work/integration-change/"
G = "r.5b1bc38638b68ed8."
doc = json.load(open(W + "state-decoded-rev9.json", encoding="utf-8"))
by_id = {r["id"]: r for r in doc["records"]}
by_dg = {r["fields"]["dg"]: r["id"] for r in doc["records"] if r["kind"] == "S" and r["id"].startswith(G)}
S_AMEND = by_dg["5b78962f0d2b7d38c9848479fc44e11bb9abf703c3653ed785f4e0a4b95a9a4b"]
S_TIMING = by_dg["c42dd78d4e25d2ef946b38c290db4197f05250a2680fa2d77101dba8fe7bb3fc"]
S_WRAPPER = by_dg["8058e2bca9cab1d0daaf0dd453ec288595357e54aed55aaa1d64da42677eca96"]
S_VIEW = by_dg["4d6ee92e40374d4dd4c6a49a3a20a6caf34e7f2d61a32a230c8ecf54691b5c49"]
S_BRIEF = by_dg["aebe00949f3a9510a44f6f554b8fc97e53476d7658a4bb29419db85b417f02ab"]
S_RENDERER = by_dg["f4ad98c3e1ac61715f904c362f805b3a98e9f532be27d4dfaf5dd1b6060a8f0e"]
S_READY = by_dg["fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"]
ref = lambda i: {"$ref": i}
sym = lambda s: {"$symbol": s}
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

DEST = G + "destination.working"
DEC = G + "decision.reuse150"
PROOF = G + "proof.reuse150"
PROOF_FILE = W + "renderer-check-sample.json"
proof_dg = hashlib.sha256(open(PROOF_FILE, "rb").read()).hexdigest()

destination = {"id": DEST, "kind": "I", "fields": {
    "pr": ref("project"), "wh": ref("actor"), "ky": "destination.working.150", "st": sym("confirmed"),
    "vl": {"path": "assets/working.png", "consumers": ["statusCell", "compactStatus"], "module": "src/queue-view-integration.ts",
           "timing_module": "src/working-timing.ts", "frames": 4, "frame_ms": 150, "cycle_ms": 600, "layout": "horizontal",
           "cell": [16, 16], "scale": 3, "sampling": "nearest", "background": "#172336", "renderer": "renderer-integration"},
    "so": [ref(S_AMEND), ref(S_TIMING), ref(S_WRAPPER), ref(S_VIEW)],
    "wy": "Confirmed destination: the existing path used by statusVisuals.running for both statusCell and compactStatus, with display.frameMs supplied by src/working-timing.ts (150) through the stable wrapper, as instructed by the retained WORKING-TIMING-AMENDMENT.md; no path move or new art."}}
decision = {"id": DEC, "kind": "D", "fields": {
    "wh": ref("actor"),
    "wt": "Adopt the exact retained assets/working.png bytes (candidate " + G + "candidate.working.retained, sha256 cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc) as the delivered Working member at the amended 150 ms per-frame timing (600 ms cycle); no new generation or provider execution.",
    "wr": [ref(DEST), ref(G + "output.working")],
    "wy": "The amendment supersedes only timing and authorizes no new art; the freshly reviewed sample passed its canvas, activity and live integration criteria at 150 ms in both consumers, so reusing the exact bytes satisfies the revised contract without a paid request.",
    "rs": [ref(S_AMEND), ref(S_TIMING), ref(S_WRAPPER), ref(S_BRIEF)],
    "pc": [ref(PROOF)]}}
proof = {"id": PROOF, "kind": "E", "fields": {
    "nm": "Executed proof: renderer-integration/check.py pass over the real browser capture of both consumers at 150 ms (capture-sample)",
    "ur": PROOF_FILE, "dg": proof_dg, "rs": sym("pass"), "md": sym("live"), "at": now, "bs": []}}
doc["records"].extend([destination, decision, proof])
by_id["project"]["fields"]["in"].append(ref(DEST))
doc["revision"] = 10

parsed = codec.Document(doc["revision"], format=doc.get("format", 1))
for row in doc["records"]:
    parsed.records[row["id"]] = codec.Record(row["id"], row["kind"], service.from_data(row["fields"]))
scope = sorted(graph.proof_scope(parsed, [DEC]))
proof["fields"]["bs"] = [{"rf": ref(i), "dg": codec.record_hash(parsed.records[i])} for i in scope]
text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
open(W + "decision-commit-document.json", "w", encoding="utf-8", newline="\n").write(text)

SRC = [S_AMEND, S_TIMING, S_WRAPPER, S_VIEW, S_BRIEF, S_RENDERER, S_READY]
plan = {
    "version": 1, "id": "delivery-150", "project": "project", "actor": "actor",
    "baseline": G + "candidate.working.retained",
    "decisions": [DEC], "knowledge": [], "stages": [],
    "delivery": {
        "name": "Deliver the exact retained Working sheet at 150 ms to both queue consumers",
        "members": [G + "output.working"],
        "destinations": [DEST],
        "criteria": [
            {"id": "bytes", "domain": "mechanical", "mode": "local",
             "check": "The package member copied for " + G + "output.working is byte-identical to the served destination assets/working.png (sha256 cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc) and to the fixture exact_art hash; all four other original art files remain unchanged.",
             "sources": [S_AMEND, S_VIEW]},
            {"id": "continuity", "domain": "continuity", "mode": "visual",
             "check": "In the actual destination screenshot and the 1x/3x consumer cells, the delivered Working sheet keeps the reviewed cool-blue stepped-cluster treatment of the adopted Ready baseline, stays distinguishable from Ready, Retry and Paused without relying on colour alone, and its four frames read as one coherent rotating activity sequence rather than a success or terminal pose.",
             "sources": [S_BRIEF, S_READY, S_VIEW]},
            {"id": "destination", "domain": "engine", "mode": "live",
             "check": "A fresh renderer-integration browser capture shows both statusCell and compactStatus painting the served assets/working.png with nearest filtering and transparent compositing on #172336, looping frames 0-3 at display.frameMs 150 (600 ms cycle, wrap observed at least twice) at the consumer 3x scale, with 1x/3x stills verified by check.py; 1x live playback remains unperformed and is not claimed.",
             "sources": [S_AMEND, S_TIMING, S_WRAPPER, S_RENDERER]},
        ],
    },
}
ptext = json.dumps(plan, indent=2, ensure_ascii=False) + "\n"
open(W + "production-plan-150.json", "w", encoding="utf-8", newline="\n").write(ptext)
print(json.dumps({"scope": scope, "proof_file_sha256": proof_dg, "sources": {"amend": S_AMEND, "timing": S_TIMING, "wrapper": S_WRAPPER, "view": S_VIEW, "brief": S_BRIEF, "renderer": S_RENDERER, "ready": S_READY},
                  "commit_doc_sha256": hashlib.sha256(text.encode()).hexdigest(), "plan_sha256": hashlib.sha256(ptext.encode()).hexdigest()}, indent=1))
