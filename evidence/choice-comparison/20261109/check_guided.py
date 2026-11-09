"""Check the retained guided Codex artifacts without changing the trial's files."""

import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def main():
    attempt = Path(__file__).resolve().parent / "native/codex-guided-01"
    identity = read(attempt / "identity.json")
    project = Path(identity["project"])
    work = project / "work/choice-comparison"
    checks = []

    def require(name, condition, detail=None):
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    changed = [p for p, h in identity["inputs"].items()
               if not (project / p).is_file() or sha(project / p) != h]
    require("all files present at guided start preserved", not changed, changed)
    require("guided process completed", read(attempt / "record.json")["returncode"] == 0)
    result = read(work / "CALLER-RESULT-guided.json")
    require("guided result explicitly scoped", result["status"] == "complete_guided_comparison"
            and not result["evaluation"]["fresh_unassisted_pass"]
            and not result["evaluation"]["named_role_qualification"])
    mapping = read(work / "guided/specialist-mapping.json")
    before, after = [read(work / name) for name in ["before-full.json", "after-full.json"]]
    old = [r["original"] for r in mapping["mapping"]]
    new = [q for r in mapping["mapping"] for q in r["successors"]]
    require("20 original literal records exactly preserved", len(old) == 20
            and sorted(old, key=lambda r: r["id"]) == sorted(before["criteria"], key=lambda r: r["id"]))
    require("23 successor literal records exactly preserved", len(new) == 23
            and sorted(new, key=lambda r: r["id"]) == sorted(after["criteria"], key=lambda r: r["id"]))
    actual = {r["id"]: r for r in after["criteria"]}
    reviews = mapping["successor_criterion_reviews"]
    require("every successor has a literal specialist review", len(reviews) == 23
            and {r["criterion"] for r in reviews} == set(actual)
            and all(r["check"] == actual[r["criterion"]]["check"]
                    and r["record_sha256"] == actual[r["criterion"]]["record_sha256"] for r in reviews))
    coverage = read(work / "guided/caller-comparison-coverage.json")["comparison_coverage"]
    require("public caller coverage complete without machine semantic verdict", coverage["complete"]
            and coverage["semantic_verdict"] == "not_assessed")
    failed_refs = []
    refs = []

    def walk(value):
        if isinstance(value, dict):
            if "path" in value and "sha256" in value:
                path = project / value["path"]
                refs.append(value["path"])
                if not path.is_file() or sha(path) != value["sha256"]:
                    failed_refs.append(value["path"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(result)
    followup = read(work / "guided/specialist-followup.json")
    walk(followup)
    require("caller and addendum linked artifact hashes valid", not failed_refs,
            {"references_checked": len(refs), "failed": failed_refs})
    citation_errors = []
    for row in followup["citation_corrections"]:
        source = row["evidence"]
        first, last = source["lines"]
        text = "\n".join((project / source["path"]).read_text(encoding="utf-8").splitlines()[first - 1:last])
        if text != source["text"]:
            citation_errors.append(row["id"])
    require("corrected cited line excerpts match actual sources", not citation_errors, citation_errors)
    original = {r["id"]: r for r in before["criteria"]}
    require("static scope addendum uses exact old and current checks", len(followup["static_scope_corrections"]) == 4
            and all(r["before"]["check"] == original[r["before"]["id"]]["check"]
                    and r["after"]["check"] == actual[r["after"]["id"]]["check"]
                    for r in followup["static_scope_corrections"]))
    parent = next(attempt.glob("native-01a1c160-*.jsonl"))
    child = next(attempt.glob("native-01a1c166-*.jsonl"))
    calls = [d["payload"] for line in parent.read_text(encoding="utf-8").splitlines()
             if (d := json.loads(line)).get("type") == "response_item"
             and d.get("payload", {}).get("type") == "function_call"]
    require("native parent delegated and followed up", any(c.get("namespace") == "collaboration"
            and c.get("name") == "spawn_agent" for c in calls)
            and any(c.get("namespace") == "collaboration" and c.get("name") == "followup_task" for c in calls))
    require("native child reads current shared profile and skill", any(
            d.get("type") == "response_item" and d.get("payload", {}).get("name") == "exec"
            and "Get-Content .agents/skills/export-kit/skills/pixl/SKILL.md" in d["payload"].get("input", "")
            and "Get-Content .agents/skills/export-kit/resources/agent/PROFILE.md" in d["payload"].get("input", "")
            for line in child.read_text(encoding="utf-8").splitlines() if (d := json.loads(line))))
    output = {"status": "pass" if all(c["pass"] for c in checks) else "fail", "checks": checks,
              "checker_sha256": sha(Path(__file__)), "project": str(project),
              "limits": "Mechanical retention, mapping, citations and native trace checks. Semantic conclusions require the separate maintainer review. Child inherited full context; guided result is not a blind, unassisted or named-role pass.",
              "artifacts": {str(p.relative_to(project)): sha(p) for p in work.rglob("*") if p.is_file()}}
    (attempt / "independent-checks.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "checks": len(checks),
                      "failed": [c for c in checks if not c["pass"]]}, indent=2))


if __name__ == "__main__":
    main()
