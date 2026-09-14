"""Saved developer project using the preserved defective-sprite evaluation fixture."""

from pathlib import Path

from pixl import graph, store
from pixl.codec import Record, Ref, Symbol
from tests.lifecycle_support import sample

FIXTURES = (
    Path(__file__).resolve().parents[1] / "evidence/host-evaluation/fixture-inputs"
)


def project(root):
    root = Path(root)
    doc = sample(root)
    brief = (
        "Controlled developer fixture, not commissioned art. Review the supplied 32x32 "
        "candidate against reference.png: preserve both antennae and both yellow eyes; "
        "use its three declared colors and binary alpha. Required browser import has "
        "no target project in this fixture and remains unavailable. Preserve the rejected "
        "candidate and identify a separate revision; do not create or edit art.\n"
    )
    (root / "source.txt").write_text(brief, encoding="utf-8")
    doc.records["source"].fields["dg"] = graph.file_hash(root / "source.txt")
    doc.records["project"].fields["br"] = brief.strip()
    doc.records["choice"].fields.update(
        wh=Ref("user"),
        st=Symbol("confirmed"),
        vl=[32, 32],
        so=[Ref("source")],
        wy="Explicit dimensions of this controlled fixture.",
    )
    doc.records["contract"].fields.update(
        px=[32, 32],
        pl=["#25354A", "#56B5BC", "#F4DDA2"],
        li="Flat colors specified for this fixture only.",
    )
    doc.records["q.mechanical"].fields["ck"] = (
        "32x32, only the declared palette, binary alpha."
    )
    doc.records["q.visual"].fields["ck"] = (
        "Preserve both antennae and both yellow eyes relative to reference.png."
    )
    doc.records["q.engine"].fields["ck"] = (
        "Verify import and nearest sampling in the target browser project."
    )
    for name, kind in (("candidate", "sprite"), ("reference", "reference")):
        filename = name + ".png"
        (root / filename).write_bytes((FIXTURES / filename).read_bytes())
        fields = {
            "nm": "Supplied developer " + name,
            "ur": filename,
            "dg": graph.file_hash(root / filename),
            "kd": Symbol(kind),
        }
        if name == "candidate":
            fields.update(ct=Ref("contract"), of=Ref("output"))
        doc.records[name] = Record(name, "X", fields)
    doc.records["task"].fields.update(ip=[Ref("reference")], ca=[Ref("candidate")])
    store.initialize(root / ".pixl", doc, root)
    return doc


def options():
    return {
        "references": ["reference"],
        "scale": 8,
        "backgrounds": ["#ffffff", "#202838"],
        "max_side": 1024,
        "contexts": [],
    }
