"""Reproducible local example. All artwork is a measurement fixture, not PixelLab output."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image

from pixl.assets import inspect
from pixl.codec import Document, Record, Ref, Symbol, encode, record_hash
from pixl.graph import file_hash, validate, proof_scope


def build():
    folder = ROOT / "examples" / "atelier"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "palette-fixture.png"
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    colors = [(32, 40, 64, 255), (72, 104, 128, 255), (136, 184, 168, 255)]
    for y in range(4, 12):
        for x in range(3, 13):
            image.putpixel((x, y), colors[(x - 3) // 4])
    image.save(path)
    result = inspect(path, 16, 16, ["#202840", "#486880", "#88b8a8"])
    (folder / "measurement.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    def rel(p):
        return p.relative_to(ROOT).as_posix()
    records = []
    def add(id_, kind, **fields):
        record = Record(id_, kind, fields)
        records.append(record)
        return record
    add("actor", "A", nm="PIXL", rl=Symbol("agent"))
    source = ROOT / "docs/research/pixel-art-knowledge.md"
    add("research", "S", ur=rel(source), dg=file_hash(source), ln=[1, len(source.read_text(encoding="utf-8").splitlines())], at="2026-09-10", au=Symbol("local"))
    tool_source = ROOT / "docs/research/snapshots/pixellab-mcp.txt"
    add("platform", "S", ur=rel(tool_source), dg=file_hash(tool_source), ln=[], at="2026-09-10", au=Symbol("official"))
    contract = add("style", "C", nm="local-palette-fixture", px=[16, 16], pl=["#202840", "#486880", "#88b8a8"],
                   vw=Symbol("side"), sa=Symbol("nearest"), al=Symbol("binary"),
                   li="Measurement fixture only; palette and grid are not a universal art rule.")
    add("runtime", "R", nm="PixelLab MCP", ur="https://api.pixellab.ai/mcp", vr="live-schema-required", so=[Ref("platform")])
    add("project", "P", nm="PIXL atelier proof", ow=Ref("actor"), ct=Ref("style"), sc=[Ref("research"), Ref("platform")], rt=[Ref("runtime")])
    asset = add("swatch", "X", nm="local measurement fixture", ur=rel(path), dg=file_hash(path), ct=Ref("style"), kd=Symbol("sprite"),
                mt={"origin": Symbol("local_fixture"), "anchor_px": [8, 12], "frame_ms": 100}, tg=["fixture", "palette-contract"])
    proof = add("proof", "E", nm="PNG measurements only", ur=rel(folder / "measurement.json"), dg=file_hash(folder / "measurement.json"),
                rs=Symbol("pass" if result["pass"] else "fail"), md=Symbol("local"), at="2026-09-10",
                bs=[{"rf": Ref(r.id), "dg": record_hash(r)} for r in (asset, contract)])
    add("method", "K", nm="palette-contract", ap=[Symbol("sprite")],
        op=["Inspect actual RGBA pixels against the project palette and alpha policy."],
        ck=["16x16; three allowed visible RGB colors; binary alpha."], so=[Ref("research")], pc=[Ref("proof")])
    add("decision", "D", wh=Ref("actor"), wt="Bind measurable image properties to a visual contract before scaling production.",
        wr=[Ref("swatch")], wy="Establish reproducible mechanical evidence; reserve visual and engine acceptance for separate receipts.",
        rs=[Ref("research")], pc=[Ref("proof")])
    add("measure", "T", nm="Prove palette/grid checker", ow=Ref("actor"), pr=Ref("project"), dp=[], dc=[Ref("decision")],
        kn=[Ref("method")], io=[Ref("swatch")], st=Symbol("done"), ev=[Ref("proof")])
    add("produce", "T", nm="Prepare a source-grounded PixelLab sample after live tool discovery", ow=Ref("actor"), pr=Ref("project"),
        dp=[Ref("measure")], dc=[Ref("decision")], kn=[Ref("method")], io=[Ref("swatch")], st=Symbol("open"), ev=[])
    add("resume", "N", wh=Ref("actor"), fo=[Ref("produce")], nx=[Ref("produce")], bl=[], rv=0)
    doc = Document(0, {r.id: r for r in records})
    proof.fields["bs"] = [{"rf": Ref(id_), "dg": record_hash(doc.records[id_])} for id_ in sorted(proof_scope(doc, ["decision", "method"]))]
    validate(doc, ROOT)
    (folder / "project.px").write_bytes(encode(doc))
    return {"path": rel(folder / "project.px"), "records": len(records), "remote_executed": False}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
