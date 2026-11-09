"""Check literal mapping and native role evidence; do not grade meaning by count."""

import hashlib
import json
from pathlib import Path


def main():
    attempt = Path(__file__).resolve().parent / "native/claude-01"
    project = attempt / "project"
    work = project / "work/choice-comparison"

    def read(path):
        return json.loads(path.read_bytes())

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    mapping = read(work / "specialist/criterion-mapping.json")
    before = read(work / "03-request-review-full-before-authoring-01.json")
    after = read(work / "04-request-review-full-after-provenance-correction.json")
    checks = []

    def require(name, condition, detail=None):
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    for side, rows, report, count in [
        ("before", [r["old"] for r in mapping["pairs"]], before, 20),
        ("after", [q for r in mapping["pairs"] for q in r["new"] + r["split_diagnostics"]], after, 23),
    ]:
        expected = {r["id"]: r for r in report["criteria"]}
        require(side + " exact IDs hashes literals modes domains sources", len(rows) == count
                and {r["id"] for r in rows} == set(expected)
                and all(all(r[k] == expected[r["id"]][k] for k in
                            ["record_sha256", "check", "domain", "mode", "sources"]) for r in rows))
    independent = read(work / "caller/independent-comparison.json")
    require("caller independently covers all successor criteria", len(independent["criteria"]) == 23
            and {r["after"]["id"] for r in independent["criteria"]} == {r["id"] for r in after["criteria"]})
    events = [json.loads(line) for line in (attempt / "stdout.jsonl").read_text(encoding="utf-8").splitlines()]
    invocations = [c for e in events if e.get("type") == "assistant"
                   for c in e.get("message", {}).get("content", [])
                   if c.get("type") == "tool_use" and c.get("name") == "Agent"
                   and c.get("input", {}).get("subagent_type") == "pixl"]
    require("native registered pixl agent invoked", bool(invocations), [c["id"] for c in invocations])
    result = read(work / "specialist/SPECIALIST-RESULT.json")
    bad = [r["path"] for r in result["artifacts"] if sha(project / r["path"]) != r["sha256"]]
    require("specialist return artifact hashes unchanged", not bad, bad)
    bad = []
    for name, expected in result["inputs_verified"]["exports"].items():
        if sha(work / name) != expected:
            bad.append(name)
    for name, expected in result["inputs_verified"]["sources"].items():
        if sha(project / name) != expected:
            bad.append(name)
    require("specialist verified exports and sources match", not bad, bad)
    output = {"status": "pass" if all(c["pass"] for c in checks) else "fail", "checks": checks,
              "checker_sha256": sha(Path(__file__)),
              "limits": "Identity, literal coverage and native invocation only. Does not mechanically establish semantic correctness or new artistic acceptance."}
    (attempt / "independent-mapping-checks.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "checks": len(checks),
                      "failed": [c for c in checks if not c["pass"]]}, indent=2))


if __name__ == "__main__":
    main()
