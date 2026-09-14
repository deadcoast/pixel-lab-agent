"""Local developer fixtures for PX2 mechanics; no art/service acceptance claims."""

import json
from hashlib import sha256
from pathlib import Path

from PIL import Image
from PIL.PngImagePlugin import PngInfo

from pixl.codec import Document, Record, Ref, Symbol, record_hash
from pixl.graph import proof_scope


def sample(root):
    """Return an open sample plan with one proposed choice and three criteria."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    source = root / "source.txt"
    source.write_text("Developer fixture brief; no production art requested.\n", encoding="utf-8")
    records = [
        Record("actor", "A", {"nm": "PIXL fixture", "rl": Symbol("agent")}),
        Record("user", "A", {"nm": "Fixture requester", "rl": Symbol("user")}),
        Record("source", "S", {
            "ur": "source.txt", "dg": sha256(source.read_bytes()).hexdigest(),
            "ln": [1, 1], "at": "2026-09-11", "au": Symbol("local"),
        }),
        Record("project", "P", {
            "nm": "Lifecycle developer fixture", "ow": Ref("actor"),
            "sc": [Ref("source")], "in": [Ref("choice")],
        }),
        Record("choice", "I", {
            "pr": Ref("project"), "wh": Ref("actor"), "ky": "px",
            "st": Symbol("proposed"), "vl": [2, 2], "so": [],
            "wy": "Use a tiny raster solely to exercise local state mechanics.",
        }),
        Record("contract", "C", {
            "nm": "Developer fixture", "px": [2, 2], "pl": [],
            "vw": Symbol("side"), "sa": Symbol("nearest"),
            "al": Symbol("binary"), "li": "Synthetic fixture; no aesthetic claim.",
            "ch": [Ref("choice")],
        }),
        Record("task", "T", {
            "nm": "Evaluate a representative fixture", "ow": Ref("actor"),
            "pr": Ref("project"), "dp": [], "dc": [], "kn": [],
            "st": Symbol("open"), "ph": Symbol("sample"), "ip": [],
            "op": [Ref("output")], "ca": [], "vr": [],
        }),
        Record("output", "F", {
            "tk": Ref("task"), "nm": "Planned fixture", "kd": Symbol("sprite"),
            "ct": Ref("contract"),
            "rq": [Ref("q.mechanical"), Ref("q.visual"), Ref("q.engine")],
        }),
    ]
    for id_, domain, mode, check in [
        ("q.mechanical", "mechanical", "local", "Raster dimensions are 2 by 2."),
        ("q.visual", "visual", "visual", "Reviewer evaluates the fixture appearance."),
        ("q.engine", "engine", "live", "Caller retains target-engine execution evidence."),
    ]:
        records.append(Record(id_, "Q", {
            "nm": check, "dm": Symbol(domain), "md": Symbol(mode),
            "ck": check, "wh": Ref("actor"), "so": [Ref("source")],
        }))
    return Document(0, {record.id: record for record in records}, format=2)


def add_candidate(doc, root, id_):
    """Create and nominate a local test raster, retaining previous candidates."""
    root = Path(root)
    path = root / f"{id_}.png"
    metadata = PngInfo()
    metadata.add_text("purpose", "PIXL developer test fixture; not production art")
    Image.new("RGBA", (2, 2), (255, 0, 255, 255)).save(path, pnginfo=metadata)
    doc.records[id_] = Record(id_, "X", {
        "nm": f"Developer fixture {id_}", "ur": path.name,
        "dg": sha256(path.read_bytes()).hexdigest(), "ct": Ref("contract"),
        "kd": Symbol("sprite"), "of": Ref("output"),
    })
    reference = Ref(id_)
    doc.records["task"].fields["ca"] = [reference]
    return reference


def add_verdict(doc, root, candidate_id, criterion_id, status, id_):
    """Record a caller-supplied test verdict with real local receipt bytes."""
    candidate = doc.records[candidate_id]
    output = doc.records[candidate.fields["of"].id]
    task_id = output.fields["tk"].id
    evidence = []
    if status != "unavailable":
        evidence_id = id_ + ".e"
        path = Path(root) / f"{evidence_id}.json"
        path.write_text(json.dumps({
            "purpose": "Synthetic developer lifecycle fixture, not real art acceptance",
            "candidate": candidate_id, "criterion": criterion_id, "status": status,
        }, sort_keys=True) + "\n", encoding="utf-8")
        doc.records[evidence_id] = Record(evidence_id, "E", {
            "nm": "Retained developer fixture observation", "ur": path.name,
            "dg": sha256(path.read_bytes()).hexdigest(), "rs": Symbol(status),
            "md": doc.records[criterion_id].fields["md"], "at": "2026-09-11",
            "bs": [
                {"rf": Ref(target), "dg": record_hash(doc.records[target])}
                for target in sorted(proof_scope(doc, [candidate_id, criterion_id]))
            ],
        })
        evidence = [Ref(evidence_id)]
    doc.records[id_] = Record(id_, "V", {
        "tk": Ref(task_id), "rq": Ref(criterion_id), "xr": Ref(candidate_id),
        "st": Symbol(status), "wh": Ref("actor"),
        "wy": "Synthetic developer fixture outcome; no real provider or engine run.",
        "at": "2026-09-11", "ev": evidence,
    })
    reference = Ref(id_)
    doc.records[task_id].fields["vr"].append(reference)
    return reference
