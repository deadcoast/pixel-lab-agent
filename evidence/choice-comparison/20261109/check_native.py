"""Independent retention/export checks; semantic review remains a separate judgment."""

import hashlib
import json
import sys
from pathlib import Path

from evaluations.host_trials import write_json
from pixl import codec, graph, store


def check(attempt):
    project = attempt / "project"
    identity = json.loads((attempt / "identity.json").read_bytes())
    checks = []

    def require(name, value, detail=None):
        checks.append({"name": name, "pass": bool(value), "detail": detail})

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    current = store.load(project / ".pixl/assets/queue.ready")
    graph.validate(current, project)
    require("accepted state unchanged and valid", codec.digest(current) == identity["baseline_state_hash"])
    changed = [p for p, h in identity["inputs"].items() if not (project / p).is_file() or sha(project / p) != h]
    require("all prior consumer and evidence files unchanged", not changed, changed)
    kit = project / ".agents/skills/export-kit"
    require("frozen current kit unchanged", all((kit / p).is_file() and sha(kit / p) == h for p, h in identity["package_files"].items()))
    record = json.loads((attempt / "record.json").read_bytes())
    require("native process completed", record["returncode"] == 0)
    work = project / "work/choice-comparison"
    payloads = {}
    malformed = []
    for file in work.rglob("*.json"):
        try:
            payloads[file.relative_to(project).as_posix()] = json.loads(file.read_bytes())
        except (ValueError, UnicodeError) as error:
            malformed.append({"path": file.relative_to(project).as_posix(), "error": str(error)})
    require("caller return retained", "work/choice-comparison/CALLER-RESULT.json" in payloads)
    expected = json.loads((attempt / "expected-context.json").read_bytes())
    contexts = [p for p, value in payloads.items() if value == expected]
    require("exact focused context exported", bool(contexts), contexts)
    expected_changes = json.loads((attempt / "expected-changes.json").read_bytes())
    comparisons = [p for p, value in payloads.items() if value == expected_changes]
    require("exact compact changes exported", bool(comparisons), comparisons)
    full = {side: [(p, value) for p, value in payloads.items() if isinstance(value, dict)
                   and value.get("kind") == "production_plan_review"
                   and value.get("plan", {}).get("id") == expected_changes[side]["plan"]["id"]]
            for side in ["before", "after"]}
    for side, count in [("before", 20), ("after", 23)]:
        require("exact full " + side + " criteria retrieved", bool(full[side]) and any(
            value["review_scope_sha256"] == expected_changes[side]["review_scope_sha256"]
            and [{"id": q["id"], "record_sha256": q["record_sha256"]} for q in value["criteria"]] == expected_changes["criterion_index"][side]
            and len(value["criteria"]) == count for _, value in full[side]), [p for p, _ in full[side]])
    require("compact view leaves semantic consistency unassessed", expected_changes["consistent"] is None)
    require("original unavailable verdict still visible", any(r["status"] == "unavailable"
            for r in expected_changes["review_attention"]["after"]["failures_obsolete_or_stale"]))
    require("current accepted output needs no transferred predecessor acceptance", all(
        not r["requires_review"] and r["task_status"] == "done" for r in expected_changes["review_attention"]["after"]["outputs"]))
    result = {"status": "pass" if all(r["pass"] for r in checks) else "fail", "checks": checks,
              "malformed_new_json": malformed, "export_paths": {"context": contexts, "changes": comparisons},
              "checker_sha256": sha(Path(__file__)),
              "limits": "Artifact identity and preservation checks only. Native delegation, actual retrieval and semantic interpretation need trace/review assessment; malformed scratch is retained separately."}
    write_json(attempt / "independent-checks.json", result)
    return {"status": result["status"], "checks": len(checks), "failed": [r for r in checks if not r["pass"]], "malformed": malformed}


if __name__ == "__main__":
    print(json.dumps(check(Path(sys.argv[1]).resolve()), indent=2))
