"""Extract exact literal criteria and source evidence from the two saved full
request-review reports and the compact changes report.

Reads only saved result files under work/choice-comparison; writes
07-criterion-literal-diff.json. No state change, no provider action.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "work" / "choice-comparison"


def load(name: str) -> dict:
    return json.loads((WORK / name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key_of(cid: str, plan_id: str) -> str:
    # plan ID "<prefix>.plan"; criterion "<prefix>.<stage>.q.<local>" -> "<stage>/<local>"
    prefix = plan_id[: -len(".plan")] if plan_id.endswith(".plan") else plan_id
    assert cid.startswith(prefix + "."), (cid, plan_id)
    rest = cid[len(prefix) + 1 :]
    stage, _, local = rest.partition(".q.")
    return f"{stage}/{local}"


def main() -> int:
    before = load("03-request-review-full-before-authoring-01.json")
    after = load("04-request-review-full-after-provenance-correction.json")
    changes = load("02-request-review-changes.json")

    b_plan = before["plan"]["id"]
    a_plan = after["plan"]["id"]

    b_by_key = {key_of(c["id"], b_plan): c for c in before["criteria"]}
    a_by_key = {key_of(c["id"], a_plan): c for c in after["criteria"]}

    index_before = {r["id"]: r["record_sha256"] for r in changes["criterion_index"]["before"]}
    index_after = {r["id"]: r["record_sha256"] for r in changes["criterion_index"]["after"]}

    compact_fields = {c["key"]: c.get("fields") for c in changes["changes"]["criteria"]["changed"]}
    compact_added = {c["key"] for c in changes["changes"]["criteria"]["added"]}

    rows = []
    for key in sorted(set(b_by_key) | set(a_by_key)):
        b = b_by_key.get(key)
        a = a_by_key.get(key)
        row = {"key": key, "compact_changed_fields": compact_fields.get(key), "compact_added": key in compact_added}
        if b:
            row["before"] = {
                "id": b["id"],
                "record_sha256": b["record_sha256"],
                "index_sha256_matches": index_before.get(b["id"]) == b["record_sha256"],
                "record_status": b.get("record_status"),
                "domain": b["domain"],
                "mode": b["mode"],
                "sources": b["sources"],
                "authority": b.get("authority"),
                "check": b["check"],
            }
        if a:
            row["after"] = {
                "id": a["id"],
                "record_sha256": a["record_sha256"],
                "index_sha256_matches": index_after.get(a["id"]) == a["record_sha256"],
                "record_status": a.get("record_status"),
                "domain": a["domain"],
                "mode": a["mode"],
                "sources": a["sources"],
                "authority": a.get("authority"),
                "check": a["check"],
            }
        if b and a:
            row["alignment"] = "same_stage_and_local_id"
            row["check_text_identical"] = b["check"] == a["check"]
            row["domain_mode_identical"] = (b["domain"], b["mode"]) == (a["domain"], a["mode"])
            row["sources_identical"] = b["sources"] == a["sources"]
        elif a:
            row["alignment"] = "added_in_after_only"
        else:
            row["alignment"] = "removed_in_before_only"
        rows.append(row)

    def source_rows(report: dict) -> list[dict]:
        out = []
        for s in report["sources"]:
            out.append(
                {
                    "id": s["id"],
                    "path": s["path"],
                    "sha256": s["sha256"],
                    "observed_sha256": s.get("observed_sha256"),
                    "status": s.get("status"),
                    "source_class": s.get("source_class"),
                    "locator": s.get("locator"),
                    "scope": s.get("scope"),
                    "line_count": s.get("line_count"),
                    "excerpts": s.get("excerpts"),
                }
            )
        return out

    result = {
        "version": 1,
        "kind": "caller_literal_extraction",
        "note": "Programmatic extraction of exact literal checks from saved full reports. "
        "Alignment is by exact stage/local ID only; it is not semantic equivalence.",
        "inputs": {
            "changes": {"path": "work/choice-comparison/02-request-review-changes.json", "sha256": sha(WORK / "02-request-review-changes.json")},
            "before_full": {"path": "work/choice-comparison/03-request-review-full-before-authoring-01.json", "sha256": sha(WORK / "03-request-review-full-before-authoring-01.json")},
            "after_full": {"path": "work/choice-comparison/04-request-review-full-after-provenance-correction.json", "sha256": sha(WORK / "04-request-review-full-after-provenance-correction.json")},
        },
        "plans": {
            "before": before["plan"],
            "after": after["plan"],
            "before_review_scope_sha256": before["review_scope_sha256"],
            "after_review_scope_sha256": after["review_scope_sha256"],
            "changes_before_scope_matches": before["review_scope_sha256"] == changes["before"]["review_scope_sha256"],
            "changes_after_scope_matches": after["review_scope_sha256"] == changes["after"]["review_scope_sha256"],
        },
        "counts": {
            "before_criteria": len(before["criteria"]),
            "after_criteria": len(after["criteria"]),
            "before_index": len(index_before),
            "after_index": len(index_after),
            "all_before_ids_in_full_report": set(index_before) == {c["id"] for c in before["criteria"]},
            "all_after_ids_in_full_report": set(index_after) == {c["id"] for c in after["criteria"]},
            "aligned_pairs": sum(1 for r in rows if r["alignment"] == "same_stage_and_local_id"),
            "added": sum(1 for r in rows if r["alignment"] == "added_in_after_only"),
            "removed": sum(1 for r in rows if r["alignment"] == "removed_in_before_only"),
            "aligned_with_identical_check_text": sum(1 for r in rows if r.get("check_text_identical")),
        },
        "criteria": rows,
        "sources": {"before": source_rows(before), "after": source_rows(after)},
        "controls": {"before": before["controls"], "after": after["controls"]},
        "selections": {"before": before["selections"], "after": after["selections"]},
        "diagnostics": {"before": before["diagnostics"], "after": after["diagnostics"], "changes": changes["diagnostics"]},
        "review_attention_after_failures": changes["review_attention"]["after"]["failures_obsolete_or_stale"],
    }
    out = WORK / "07-criterion-literal-diff.json"
    out.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"path": str(out.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(out), "counts": result["counts"], "plans": result["plans"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
