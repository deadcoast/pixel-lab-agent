"""Independent public-result and preservation checks for the guide consumers."""

import hashlib
import json
import sys
from pathlib import Path

from pixl import codec, graph, service, store


def check(attempt):
    project = attempt / "project"
    identity = json.loads((attempt / "identity.json").read_bytes())
    checks = []

    def require(name, condition, detail=None):
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    state = ".pixl/assets/queue.ready/state.px"
    doc = store.load(project / Path(state).parent)
    graph.validate(doc, project)
    require("canonical state valid and unchanged", codec.digest(doc) == identity["baseline_state_hash"])
    changed = [p for p, h in identity["inputs"].items() if not (project / p).is_file() or sha(project / p) != h]
    require("all original consumer files preserved", not changed, changed)
    kit = project / ".agents/skills/export-kit"
    changed = [p for p, h in identity["package_files"].items() if not (kit / p).is_file() or sha(kit / p) != h]
    require("frozen current package preserved", not changed, changed)
    record = json.loads((attempt / "record.json").read_bytes())
    require("native host completed", record["returncode"] == 0)
    work = project / "work/everyday-guide"
    payloads, malformed = {}, []
    for path in work.rglob("*.json"):
        try:
            payloads[path.relative_to(project).as_posix()] = json.loads(path.read_bytes())
        except (ValueError, UnicodeError) as error:
            malformed.append({"path": path.relative_to(project).as_posix(), "error": str(error)})
    require("caller result retained", "work/everyday-guide/CALLER-RESULT.json" in payloads)
    context = service.call("pixl_context", {"path": state, "focus": "provenance-correction.plan", "view": "authoring"}, project)
    matches = [p for p, v in payloads.items() if v == context]
    require("exact current authoring context exported", bool(matches), matches)
    review = service.call("pixl_review_context", {"path": state, "candidate_id": identity["candidate"]}, project)
    matches = [p for p, v in payloads.items() if v == review]
    require("exact current family review context exported", bool(matches), matches)
    require("snapshot creation separate from current acceptance", review["snapshot_acceptance"]["accepted"] is False
            and review["current_acceptance"]["all_required_pass"] and review["current_acceptance"]["task_complete"])
    replays = [p for p, v in payloads.items() if isinstance(v, dict) and v.get("review") == identity["review"]
               and v.get("reused_review") is True and v.get("publications") == []
               and v.get("state_hash") == identity["baseline_state_hash"] and v.get("remote_executed") is False]
    require("identical review replay returns zero publications", bool(replays), replays)
    selected = service.call("pixl_plar_read", {"path": "authoring-plar.txt", "asset_id": "queue.working"}, project)
    handoffs = []
    for path in (project / ".pixl/handoffs").glob("*.json"):
        relative = path.relative_to(project).as_posix()
        if relative in identity["inputs"]:
            continue
        data = json.loads(path.read_bytes())
        if (path.stem == sha(path) and data.get("asset_id") == "queue.working"
                and data.get("requirements_hash") == selected["requirements_hash"]
                and data.get("selection", {}).get("path") == "authoring-plar.txt"
                and data["selection"]["hash"] == selected["hash"]
                and data.get("resume") == selected["production"]["continuation"]):
            handoffs.append(relative)
    require("handoff binds exact current successor requirements and continuation", bool(handoffs), handoffs)

    objects = []

    def walk(value):
        if isinstance(value, dict):
            objects.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for value in payloads.values():
        walk(value)
    exports = [v for v in objects if v.get("result_saved") is True and "result_sha256" in v]
    bad_exports = [v["result_path"] for v in exports if not (project / v["result_path"]).is_file()
                   or sha(project / v["result_path"]) != v["result_sha256"]]
    require("retained export summaries match actual bytes", bool(exports) and not bad_exports,
            {"summaries": len(exports), "bad": bad_exports})
    exact_sources = []
    for value in objects:
        if not {"text", "sha256", "start", "end", "bytes"} <= value.keys():
            continue
        paths = [p for p, h in identity["inputs"].items() if h == value["sha256"]]
        for p in paths:
            try:
                lines = (project / p).read_bytes().decode("utf-8-sig").splitlines(keepends=True)
            except UnicodeError:
                continue
            if "".join(lines[value["start"] - 1:value["end"]]) == value["text"]:
                exact_sources.append({"path": p, "start": value["start"], "end": value["end"]})
    require("source excerpt matches unchanged source file bytes", bool(exact_sources), exact_sources)
    result = {"status": "pass" if all(c["pass"] for c in checks) else "fail", "checks": checks,
              "malformed_new_json": malformed, "checker_sha256": sha(Path(__file__)),
              "limits": "Mechanical artifact identity/preservation and public operation outcomes. Native role, actual guide use and quality of caller interpretation require trace review; accepted art predates this trial."}
    (attempt / "independent-checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return {"status": result["status"], "checks": len(checks), "failed": [r for r in checks if not r["pass"]], "malformed": malformed}


if __name__ == "__main__":
    print(json.dumps(check(Path(sys.argv[1]).resolve()), indent=2))
