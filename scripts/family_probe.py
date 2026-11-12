"""Public isolated family operations from a retained synthetic input checkpoint.

Only host fixture data is loaded here. No source runtime or test helpers are
imported into this module or into the caller's relocated runtime process.
"""

import base64
import json
from hashlib import sha256
from pathlib import Path


def run_family_probe(invoke, project):
    project = Path(project) / "family-fixture"
    project.mkdir()
    fixture = (
        Path(__file__).resolve().parents[1]
        / "evidence/family-delivery/portable-fixture.json"
    )
    checkpoint = json.loads(fixture.read_text(encoding="utf-8"))
    checks = []

    def require(condition, message):
        if not condition:
            raise RuntimeError("family distribution probe: " + message)

    for item in checkpoint["files"]:
        raw = base64.b64decode(item["content_base64"], validate=True)
        require(
            sha256(raw).hexdigest() == item["sha256"] and len(raw) == item["bytes"],
            "input checkpoint integrity",
        )
        path = (project / item["path"]).resolve()
        require(
            path.is_relative_to(project.resolve()), "input checkpoint path confinement"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    root = str(project)
    folder = str(project / ".pixl")
    state = str(project / ".pixl/state.px")

    def cli(label, *arguments):
        result = invoke(list(arguments))
        checks.append({"command": arguments[0], "check": label, "status": "pass"})
        return result

    def fields(document, id_):
        return next(row["fields"] for row in document["records"] if row["id"] == id_)

    def publish(document, expected, label):
        document["revision"] += 1
        path = project / (label + ".json")
        path.write_text(json.dumps(document), encoding="utf-8")
        encoded = project / (label + ".px")
        cli(label + " encode", "encode", str(path), "--out", str(encoded))
        return cli(
            label + " publish",
            "commit",
            folder,
            str(encoded),
            "--expect",
            expected,
            "--root",
            root,
        )

    before = cli(
        "inspect the supplied synthetic accepted-member plan",
        "family",
        state,
        "delivery.output",
        "--root",
        root,
    )
    require(
        before["files_verified"] and before["families"][0]["snapshot_blockers"] == [],
        "fixture not ready for local snapshot",
    )
    saved = cli(
        "snapshot actual selected bytes without approval",
        "family-snapshot",
        folder,
        "delivery.output",
        "portable.package",
        "--expect",
        before["hash"],
        "--root",
        root,
    )
    require(
        saved["accepted"] is False and saved["remote_executed"] is False,
        "snapshot invented acceptance",
    )
    document = cli("read retained candidate", "decode", state)
    task = fields(document, "delivery.task")
    require(
        task["ca"] == task["vr"] == [] and task["st"] == {"$symbol": "open"},
        "snapshot changed task acceptance",
    )
    artifact = fields(document, "portable.package")
    manifest_path = project / artifact["ur"]
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    require(
        sha256(manifest_bytes).hexdigest() == artifact["dg"], "manifest hash differs"
    )
    for item in manifest["files"]:
        copied = manifest_path.parent / item["path"]
        require(
            copied.read_bytes() == (project / item["source_path"]).read_bytes(),
            "delivered member bytes differ",
        )
    cold = cli(
        "cold report retains unperformed collective checks",
        "family",
        state,
        "--root",
        root,
    )
    require(
        cold["hash"] == saved["hash"]
        and cold["families"][0]["snapshots"][0]["stale"] == [],
        "cold snapshot differs",
    )
    require(
        {r["status"] for r in cold["families"][0]["requirements"]} == {"unperformed"},
        "collective check fabricated",
    )

    lineage_members = cold["families"][0]["snapshots"][0]["files"]
    require(
        all(row["lineage"]["candidate"] == row["candidate"] for row in lineage_members)
        and all(row["lineage"]["candidate"] == row["candidate"]
                for row in cold["families"][0]["members"]),
        "lineage lost exact current or retained candidate identity",
    )
    require(manifest_path.read_bytes() == manifest_bytes, "lineage rewrote manifest")
    checks.append({"command": "family", "check": "derived member lineage preserves exact identities and manifest bytes", "status": "pass"})

    task["ca"] = [{"$ref": "portable.package"}]
    task["vr"] = [{"$ref": "portable.engine"}]
    document["records"].append(
        {
            "id": "portable.engine",
            "kind": "V",
            "fields": {
                "tk": {"$ref": "delivery.task"},
                "rq": {"$ref": "q.delivery.engine"},
                "xr": {"$ref": "portable.package"},
                "st": {"$symbol": "unavailable"},
                "wh": {"$ref": "user"},
                "at": "2026-09-11",
                "wy": "Distribution fixture has no engine project; real import remains unperformed.",
                "ev": [],
            },
        }
    )
    unavailable = publish(document, saved["hash"], "unavailable-engine")
    boundary = cli(
        "cold report keeps engine unavailable and delivery open",
        "family",
        state,
        "--root",
        root,
    )
    row = boundary["families"][0]
    require(
        row["state"] == "open"
        and any(
            r["id"] == "q.delivery.engine" and r["status"] == "unavailable"
            for r in row["requirements"]
        ),
        "unavailable boundary lost",
    )

    fields(document, "delivery.output")["mb"] = [{"$ref": "output"}]
    amended = publish(document, unavailable["hash"], "amended-membership")
    changed = cli(
        "membership amendment preserves old package and reports drift",
        "family",
        state,
        "--root",
        root,
    )
    require(
        changed["families"][0]["snapshots"][0]["stale"],
        "old membership falsely current",
    )
    require(
        manifest_path.read_bytes() == manifest_bytes, "historical manifest rewritten"
    )
    revised = cli(
        "retain a new snapshot against the saved amended plan",
        "family-snapshot",
        folder,
        "delivery.output",
        "portable.revised",
        "--expect",
        amended["hash"],
        "--root",
        root,
    )
    final = cli(
        "cold report retains both exact packages", "family", state, "--root", root
    )
    rows = {r["candidate"]: r for r in final["families"][0]["snapshots"]}
    require(
        len(rows) == 2
        and len(rows["portable.package"]["files"]) == 2
        and len(rows["portable.revised"]["files"]) == 1,
        "frozen member inventories lost",
    )
    require(
        rows["portable.package"]["files"] == lineage_members,
        "current membership changed historical member lineage",
    )
    require(
        rows["portable.revised"]["stale"] == [] and final["hash"] == revised["hash"],
        "new snapshot not current",
    )
    return {
        "status": "pass",
        "checks": checks,
        "remote_executed": False,
        "fixture_sha256": sha256(fixture.read_bytes()).hexdigest(),
        "scope": "Public isolated CLI from a retained synthetic preaccepted checkpoint; actual member copies, unavailable engine and amended membership; no real art/engine outcome.",
    }
