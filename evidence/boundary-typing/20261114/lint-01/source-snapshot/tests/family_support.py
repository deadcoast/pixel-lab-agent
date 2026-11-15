"""Published synthetic family fixtures; no real art or engine acceptance."""

from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from pixl import codec, graph, store
from pixl.codec import Record, Ref, Symbol
from tests.lifecycle_support import add_candidate, add_verdict, sample


def family(root, folder=None):
    """Save sample/member plans before verdicts; return the open delivery plan.

    The default store is ``root / '.pixl'``. Stable IDs are sample task/output
    ``task``/``output`` with X ``sample``; member task/output/X are
    ``member.task``/``member.output``/``member``; the delivery task/output are
    ``delivery.task``/``delivery.output``. ``destination`` starts confirmed.
    All local, visual and live receipts explicitly identify synthetic data.
    """
    root = Path(root)
    folder = root / ".pixl" if folder is None else Path(folder)
    doc = sample(root)
    doc.records["choice"].fields.update(st=Symbol("confirmed"), so=[Ref("source")])
    store.initialize(folder, doc, root)

    def publish(candidate):
        current = store.load(folder)
        candidate.revision = current.revision + 1
        store.commit(folder, candidate, codec.digest(current), root)
        return store.load(folder)

    add_candidate(doc, root, "sample")
    for domain in ("mechanical", "visual", "engine"):
        add_verdict(doc, root, "sample", "q." + domain, "pass", "sample.v." + domain)
    doc.records["task"].fields["st"] = Symbol("active")
    doc = publish(doc)
    doc.records["task"].fields["st"] = Symbol("done")
    doc = publish(doc)

    doc.records["method"] = Record("method", "K", {
        "nm": "Synthetic family method", "ap": [Symbol("fixture")],
        "op": ["Exercise recorded family semantics"], "ck": ["Retain fixture evidence"],
        "so": [Ref("source")], "pc": [Ref("adoption.e")],
    })
    doc.records["decision"] = Record("decision", "D", {
        "wh": Ref("actor"), "wt": "Adopt the synthetic fixture method",
        "wr": [Ref("method")], "wy": "Exercise local planning mechanics only",
        "rs": [Ref("source")], "pc": [Ref("adoption.e")],
    })
    path = root / "adoption.json"
    path.write_text('{"purpose":"Synthetic developer adoption proof; no art claim"}\n', encoding="utf-8")
    doc.records["adoption.e"] = Record("adoption.e", "E", {
        "nm": "Synthetic adoption proof", "ur": path.name,
        "dg": sha256(path.read_bytes()).hexdigest(), "rs": Symbol("pass"),
        "md": Symbol("local"), "at": "2026-09-11", "bs": [
            {"rf": Ref(id_), "dg": codec.record_hash(doc.records[id_])}
            for id_ in sorted(graph.proof_scope(doc, ["decision"]))
        ],
    })
    doc.records["member.task"] = Record("member.task", "T", {
        "nm": "Produce synthetic family member", "ow": Ref("actor"),
        "pr": Ref("project"), "dp": [Ref("task")], "dc": [Ref("decision")],
        "kn": [Ref("method")], "st": Symbol("open"), "ph": Symbol("production"),
        "ip": [Ref("sample")], "op": [Ref("member.output")], "ca": [], "vr": [],
    })
    doc.records["q.member.continuity"] = Record("q.member.continuity", "Q", {
        "nm": "Synthetic member continuity", "dm": Symbol("continuity"),
        "md": Symbol("visual"), "ck": "Compare fixture member against the retained fixture sample",
        "wh": Ref("actor"), "so": [Ref("source")],
    })
    doc.records["member.output"] = Record("member.output", "F", {
        "tk": Ref("member.task"), "nm": "Synthetic family member", "kd": Symbol("sprite"),
        "ct": Ref("contract"), "rq": [Ref("q.mechanical"), Ref("q.member.continuity")],
        "bs": Ref("sample"),
    })
    doc = publish(doc)

    # Use the real raster fixture writer without changing the completed sample.
    temporary = deepcopy(doc)
    add_candidate(temporary, root, "member")
    member = temporary.records["member"]
    member.fields["of"] = Ref("member.output")
    doc.records["member"] = member
    doc.records["member.task"].fields["ca"] = [Ref("member")]
    for criterion in ("q.mechanical", "q.member.continuity"):
        add_verdict(doc, root, "member", criterion, "pass", "member.v." + criterion)
    doc.records["member.task"].fields["st"] = Symbol("active")
    doc = publish(doc)
    doc.records["member.task"].fields["st"] = Symbol("done")
    doc = publish(doc)

    doc.records["destination"] = Record("destination", "I", {
        "pr": Ref("project"), "wh": Ref("user"), "ky": "delivery_target",
        "st": Symbol("confirmed"), "vl": "Synthetic fixture engine",
        "so": [Ref("source")], "wy": "Fixture target only; no real engine executed",
    })
    doc.records["project"].fields["in"].append(Ref("destination"))
    for id_, domain, mode, check in [
        ("q.continuity", "continuity", "visual", "Review selected fixtures together against the exact baseline"),
        ("q.delivery.engine", "engine", "live", "Retain fixture destination import execution evidence"),
    ]:
        doc.records[id_] = Record(id_, "Q", {
            "nm": check, "dm": Symbol(domain), "md": Symbol(mode), "ck": check,
            "wh": Ref("actor"), "so": [Ref("source")],
        })
    doc.records["delivery.task"] = Record("delivery.task", "T", {
        "nm": "Deliver synthetic family", "ow": Ref("actor"), "pr": Ref("project"),
        "dp": [Ref("task"), Ref("member.task")], "dc": [Ref("decision")],
        "kn": [Ref("method")], "st": Symbol("open"), "ph": Symbol("delivery"),
        "ip": [Ref("sample"), Ref("member")], "op": [Ref("delivery.output")],
        "ca": [], "vr": [],
    })
    doc.records["delivery.output"] = Record("delivery.output", "F", {
        "tk": Ref("delivery.task"), "nm": "Synthetic family delivery", "kd": Symbol("report"),
        "rq": [Ref("q.continuity"), Ref("q.delivery.engine")], "bs": Ref("sample"),
        "mb": [Ref("output"), Ref("member.output")], "ds": [Ref("destination")],
    })
    return publish(doc)
