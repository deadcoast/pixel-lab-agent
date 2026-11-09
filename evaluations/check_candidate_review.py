"""Independent local outcome/retention checks after a native review trial."""

import argparse
import json
from pathlib import Path

from evaluations.host_trials import sha, write_json
from pixl import candidate_review, codec, graph, store


def check(attempt):
    attempt = Path(attempt).resolve()
    project = attempt / "project"
    folder = project / ".pixl/assets/queue.ready"
    identity = json.loads((attempt / "identity.json").read_text(encoding="utf-8"))
    current = store.load(folder)
    graph.validate(current, project)
    before = codec.parse((folder / "history" / (identity["baseline_state_hash"] + ".px")).read_bytes())
    checks = []

    def require(name, condition, detail=None):
        checks.append({"name": name, "pass": bool(condition), **({"detail": detail} if detail is not None else {})})

    result_paths = [p.relative_to(project).as_posix() for p in
                    [project / "REVIEW-RESULT.json", project / "work/native-review/REVIEW-RESULT.json"] if p.is_file()]
    require("native result retained", bool(result_paths), result_paths)
    allowed = ".pixl/assets/queue.ready/state.px"
    changed = [name for name, digest in identity["inputs"].items()
               if name != allowed and (not (project / name).is_file() or sha(project / name) != digest)]
    require("original consumer files and prior evidence unchanged", not changed, changed)
    kit = project / ".agents/skills/review-kit"
    require("frozen native kit unchanged", all((kit / p).is_file() and sha(kit / p) == h for p, h in identity["package_files"].items()))
    removed = sorted(set(before.records) - set(current.records))
    require("all old records retained", not removed, removed)
    unexpected = []
    for key, old in before.records.items():
        new = current.records.get(key)
        if old == new:
            continue
        if key in {"provenance-correction.working.task", "provenance-correction.delivery.task"}:
            continue
        if (old.kind == "V" and new is not None and new.fields.get("ob") is True
                and {k: v for k, v in old.fields.items() if k != "ob"} == {k: v for k, v in new.fields.items() if k != "ob"}):
            continue
        unexpected.append(key)
    require("only intended lifecycle and supersession edits to old records", not unexpected, unexpected)
    require("no provider attempts added", {r.id for r in before.records.values() if r.kind == "J"} ==
            {r.id for r in current.records.values() if r.kind == "J"})
    working = candidate_review.context(current, project, "provenance-correction.working.candidate")
    require("Working complete and nominated with eight passing criteria", working["nominated"] and
            working["current_acceptance"]["task_complete"] and len(working["criteria"]) == 8 and
            all(q["status"] == "pass" for q in working["criteria"]))
    require("prior unavailable verdict preserved and superseded", current.records["provenance.working.motion.unavailable"].fields.get("ob") is True)
    task = current.records["provenance-correction.delivery.task"]
    require("family complete with one nominee", task.fields["st"].value == "done" and len(task.fields["ca"]) == 1)
    family = None
    if task.fields["ca"]:
        family = candidate_review.context(current, project, task.fields["ca"][0].id)
        require("three collective criteria pass", len(family["criteria"]) == 3 and all(q["status"] == "pass" for q in family["criteria"]))
        require("immutable creation remains unaccepted alongside current acceptance",
                not family["snapshot_acceptance"]["accepted"] and family["current_acceptance"]["task_complete"])
        require("four exact retained family member files", len(family["members"]) == 4 and
                all(sha(project / row["retained_path"]) == row["sha256"] for row in family["members"]))
    reports = [r for r in current.records.values() if r.kind == "X" and r.fields.get("mt", {}).get("candidate_review") == 1]
    require("ordinary review reports retained", len(reports) == 2, [r.id for r in reports])
    new_verdicts = [r.id for r in current.records.values() if r.kind == "V" and r.id not in before.records]
    require("exactly four new verdicts without replay duplication", len(new_verdicts) == 4, new_verdicts)
    replays = []
    for path in (project / "work/native-review").glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (ValueError, UnicodeError):
            continue
        if isinstance(data, dict) and data.get("reused_review") is True and data.get("publications") == []:
            replays.append(path.relative_to(project).as_posix())
    require("identical retry returned no new publications", bool(replays), replays)
    result = {"status": "pass" if all(row["pass"] for row in checks) else "fail", "checks": checks,
              "state_hash": codec.digest(current), "state_revision": current.revision,
              "working": working, "family": family,
              "scope": "Independent local identity, lifecycle, history and retention checks. Native viewing/renderer traces and semantic judgments require separate review."}
    write_json(attempt / "independent-checks.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("attempt", type=Path)
    args = parser.parse_args()
    result = check(args.attempt)
    print(json.dumps({"status": result["status"], "checks": len(result["checks"]),
                      "failures": [x for x in result["checks"] if not x["pass"]]}, indent=2))
    raise SystemExit(result["status"] != "pass")
