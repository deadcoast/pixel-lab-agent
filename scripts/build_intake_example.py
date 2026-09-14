"""Build an explicitly unfinished PX2 intake example; no art or proof is invented."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pixl import graph, store
from pixl.codec import Record, Ref, Symbol, encode


def build():
    folder = ROOT / "examples/intake"
    folder.mkdir(parents=True, exist_ok=True)
    brief = (
        "Syntax fixture, not an approved production brief.\n"
        "Plan one representative item before its family. Canvas remains undecided.\n"
        "Two supplied directions disagree: continuous dark outlines versus selective edges.\n"
        "Native readability and eventual target-engine import are required; the engine is unavailable.\n"
    )
    source_path = folder / "brief.txt"
    source_path.write_text(brief, encoding="utf-8", newline="\n")
    doc = store.intake_project(
        "Incomplete item-family intake", "A deliberately unfinished planning example"
    )

    def add(id_, kind, fields):
        doc.records[id_] = Record(id_, kind, fields)
        return Ref(id_)

    source = add(
        "brief",
        "S",
        {
            "ur": "examples/intake/brief.txt",
            "dg": graph.file_hash(source_path),
            "ln": [1, 4],
            "at": "2026-09-11",
            "au": Symbol("local"),
        },
    )
    doc.records["project"].fields["sc"] = [source]
    choices = []
    for id_, key, state, value, why in (
        ("canvas", "px", "unresolved", None, "The final canvas has not been chosen."),
        (
            "edges",
            "edge_treatment",
            "conflict",
            ["continuous dark outline", "selective edges"],
            "Resolve the competing source directions.",
        ),
    ):
        choices.append(
            add(
                id_,
                "I",
                {
                    "pr": Ref("project"),
                    "wh": Ref("user"),
                    "ky": key,
                    "st": Symbol(state),
                    "vl": value,
                    "so": [source],
                    "wy": why,
                },
            )
        )
    doc.records["project"].fields["in"] = choices
    criteria = []
    for id_, domain, mode, check in (
        (
            "size",
            "mechanical",
            "local",
            "The actual file matches the chosen canvas and required alpha policy.",
        ),
        (
            "readability",
            "visual",
            "visual",
            "The item retains its required identity at native size on the intended backgrounds.",
        ),
        (
            "import",
            "engine",
            "live",
            "The destination engine displays the intended sampling, scale and transparency.",
        ),
    ):
        criteria.append(
            add(
                id_,
                "Q",
                {
                    "nm": id_,
                    "dm": Symbol(domain),
                    "md": Symbol(mode),
                    "ck": check,
                    "wh": Ref("user"),
                    "so": [source],
                },
            )
        )
    output = add(
        "sample",
        "F",
        {
            "tk": Ref("make_sample"),
            "nm": "Representative item",
            "kd": Symbol("sprite"),
            "rq": criteria,
        },
    )
    add(
        "make_sample",
        "T",
        {
            "nm": "Prove the representative item before family production",
            "ow": Ref("actor"),
            "pr": Ref("project"),
            "dp": [],
            "dc": [],
            "kn": [],
            "st": Symbol("open"),
            "ph": Symbol("sample"),
            "ip": [],
            "op": [output],
            "ca": [],
            "vr": [],
        },
    )
    graph.validate(doc, ROOT)
    (folder / "project.px").write_bytes(encode(doc))
    return {"format": 2, "records": len(doc.records), "ready": graph.ready(doc)}


if __name__ == "__main__":
    print(build())
