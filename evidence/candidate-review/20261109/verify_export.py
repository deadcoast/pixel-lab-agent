"""Check native export artifacts independently; does not publish state."""

import hashlib
import json
import sys
from pathlib import Path

from evaluations.host_trials import inventory, write_json
from pixl import candidate_review, codec, graph, store


def check(attempt):
    project = attempt / "project"
    identity = json.loads((attempt / "identity.json").read_bytes())
    current = store.load(project / ".pixl/assets/queue.ready")
    graph.validate(current, project)
    checks = []

    def require(name, condition, detail=None):
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    require("canonical state unchanged", codec.digest(current) == identity["baseline_state_hash"])
    changed = [p for p, digest in identity["inputs"].items()
               if not (project / p).is_file() or sha(project / p) != digest]
    require("all pre-existing input files unchanged", not changed, changed)
    kit = project / ".agents/skills/export-kit"
    require("final frozen kit unchanged", all((kit / p).is_file() and sha(kit / p) == h
                                             for p, h in identity["package_files"].items()))
    predecessor = Path(identity["predecessor"]) / "project"
    require("historical kits unchanged", all(inventory(project / ".agents/skills" / name, ("__pycache__",)) ==
                                            inventory(predecessor / ".agents/skills" / name, ("__pycache__",))
                                            for name in ["pixl-kit", "review-kit"]))
    summaries = {}

    def visit(value):
        if isinstance(value, dict):
            if value.get("result_saved") is True and "result_path" in value:
                summaries[value["result_path"]] = value
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, str) and value.strip().startswith(("{", "[")):
            try:
                visit(json.loads(value))
            except ValueError:
                pass

    for path in (project / "work/export-review").rglob("*"):
        if path.is_file() and path.suffix in {".json", ".txt"}:
            try:
                visit(json.loads(path.read_bytes()))
            except ValueError:
                pass
    for line in (attempt / "stdout.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            visit(json.loads(line))
        except ValueError:
            pass
    exported = {}
    for relative, summary in summaries.items():
        path = graph.confined(project, relative)
        data = path.read_bytes()
        exported[relative] = json.loads(data)
        require("exact JSON file identity: " + relative, sha(path) == summary["result_sha256"]
                and len(data) == summary["result_bytes"] and summary["media_type"] == "application/json")
    expected = candidate_review.context(current, project, identity["candidate"])
    require("current review context exported exactly", any(value == expected for value in exported.values()))
    require("large family report exported", any("families" in value and summaries[path]["result_bytes"] > 32767
                                               for path, value in exported.items()))
    replays = [value for value in exported.values() if value.get("review") == identity["review"]]
    require("identical accepted review exported without publication", bool(replays) and all(
        value.get("reused_review") is True and value.get("publications") == []
        and value["state_hash"] == identity["baseline_state_hash"] for value in replays))
    require("native final result retained", (project / "work/export-review/EXPORT-RESULT.json").is_file())
    result = {"status": "pass" if all(c["pass"] for c in checks) else "fail", "checks": checks,
              "export_summaries": summaries, "state_hash": codec.digest(current),
              "checker_sha256": sha(Path(__file__)),
              "scope": "Native public output files and unchanged accepted state; no new art or renderer qualification."}
    write_json(attempt / "independent-export-checks.json", result)
    return {"host": attempt.name, "status": result["status"], "checks": len(checks),
            "failures": [c for c in checks if not c["pass"]]}


if __name__ == "__main__":
    print(json.dumps(check(Path(sys.argv[1]).resolve()), indent=2))
