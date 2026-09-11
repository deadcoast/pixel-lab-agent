from hashlib import sha256
from pathlib import Path

from pixl.codec import Document, Record, Ref, Symbol, record_hash
from pixl.graph import proof_scope


def sample(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "source.txt").write_text("source intent\n", encoding="utf-8", newline="\n")
    (root / "asset.txt").write_text("asset content\n", encoding="utf-8")
    (root / "proof.txt").write_text("local check result\n", encoding="utf-8")
    def hash_file(name):
        return sha256((root / name).read_bytes()).hexdigest()
    def r(id_, kind, **kw):
        return Record(id_, kind, kw)
    records = [r("actor", "A", nm="PIXL", rl=Symbol("agent")),
               r("source", "S", ur="source.txt", dg=hash_file("source.txt"), ln=[1, 1], at="2026-09-10", au=Symbol("local")),
               r("style", "C", nm="fixture", px=[16, 16], pl=[], vw=Symbol("side"), sa=Symbol("nearest"), al=Symbol("binary"), li="fixture"),
               r("project", "P", nm="fixture", ow=Ref("actor"), ct=Ref("style"), sc=[Ref("source")]),
               r("asset", "X", nm="fixture", ur="asset.txt", dg=hash_file("asset.txt"), ct=Ref("style"), kd=Symbol("report")),
               r("proof", "E", nm="check", ur="proof.txt", dg=hash_file("proof.txt"), rs=Symbol("pass"), md=Symbol("local"), at="2026-09-10", bs=[]),
               r("decision", "D", wh=Ref("actor"), wt="fixture decision", wr=[Ref("asset")], wy="source-directed fixture", rs=[Ref("source")], pc=[Ref("proof")]),
               r("task", "T", nm="produce asset", ow=Ref("actor"), pr=Ref("project"), dp=[], dc=[Ref("decision")], kn=[], io=[Ref("asset")], st=Symbol("open"), ev=[])]
    doc = Document(0, {r.id: r for r in records})
    doc.records["proof"].fields["bs"] = [{"rf": Ref(id_), "dg": record_hash(doc.records[id_])} for id_ in sorted(proof_scope(doc, ["decision"]))]
    return doc
