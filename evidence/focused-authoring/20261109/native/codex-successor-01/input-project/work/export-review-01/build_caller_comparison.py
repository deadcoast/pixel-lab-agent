"""Retain a NEW caller comparison that carries the prior 20 criterion_comparisons verbatim,
rebinds the report identity/fingerprint to the exact current report, and records continuity provenance.
Run from the consumer project root with: python -I work/export-review-01/build_caller_comparison.py
"""
import hashlib
import io
import json
from pathlib import Path

prior_path = Path("work/criteria-review-01/caller-comparison.json")
prior_b = prior_path.read_bytes()
prior = json.loads(prior_b.decode("utf-8"))
new_raw = Path("work/export-review-01/request-review-raw.txt").read_bytes()
new_fmt = Path("work/export-review-01/request-review.json").read_bytes()
report = json.loads(new_raw.decode("utf-8"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


assert prior["review_scope_sha256"] == "aa2c114f0d722d6b8678adce97e1adaae7093d47d5acedd2a818f349dcfb72f0"
assert len(prior["criterion_comparisons"]) == 20
rows = prior["criterion_comparisons"]
assert [r["criterion"] for r in rows] == report["criterion_ids"]
assert all(
    r["record_sha256"] == c["record_sha256"] == c["current_record_sha256"]
    for r, c in zip(rows, report["criteria"])
)

out = dict(prior)  # shallow copy preserves key order
out["assignment"] = {
    "path": "EXPORT-REVIEW.md",
    "sha256": sha(Path("EXPORT-REVIEW.md").read_bytes()),
    "prior_assignment": prior["assignment"],
}
out["reviewer_role"] = (
    prior["reviewer_role"]
    + "; this file is the export/continuity retention by the native caller under EXPORT-REVIEW.md: "
    "the 20 criterion_comparisons, the four discrepancy resolutions, the reduced-motion disposition and "
    "the verdict are carried verbatim from the prior caller comparison, not re-authored"
)
out["reviewed_report"] = {
    "tool": "pixl_request_review(packet='.pixl/assets/queue.ready/state.px', plan='authoring-01.plan', job='authoring-01.working.join-01')",
    "path": "work/export-review-01/request-review.json",
    "sha256": sha(new_fmt),
    "raw_path": "work/export-review-01/request-review-raw.txt",
    "raw_sha256": sha(new_raw),
    "raw_origin": "host-spilled tool result copied as exact bytes; formatted copy parsed as UTF-8 and verified equal to the raw parsed value",
    "state": report["state"],
    "plan": report["plan"],
    "job": report["request"]["id"],
    "job_state": report["request"]["state"],
    "remote_id": report["request"]["remote_id"],
    "intent_sha256": report["request"]["intent_sha256"],
    "request_sha256": report["request"]["request"]["request_sha256"],
    "blockers": report["request"]["blockers"],
    "next_action": report["request"]["next_action"],
}
out["review_scope_sha256"] = report["review_scope_sha256"]
out["continuity_provenance"] = {
    "prior_caller_comparison": {
        "path": "work/criteria-review-01/caller-comparison.json",
        "sha256": sha(prior_b),
        "review_scope_sha256": prior["review_scope_sha256"],
        "unchanged": True,
    },
    "prior_report": {
        "path": "work/criteria-review-01/request-review.json",
        "sha256": sha(Path("work/criteria-review-01/request-review.json").read_bytes()),
        "raw_path": "work/criteria-review-01/request-review-raw.txt",
        "raw_sha256": sha(Path("work/criteria-review-01/request-review-raw.txt").read_bytes()),
    },
    "carried_verbatim": [
        "criterion_comparisons (20 rows)",
        "discrepancies_with_specialist (D1-D4)",
        "reduced_motion_disposition",
        "verdict",
        "specialist_artifacts",
        "sources_read_independently",
        "caller_measurements",
    ],
    "changed_fields": [
        "assignment",
        "reviewer_role (appended sentence)",
        "reviewed_report",
        "review_scope_sha256",
        "continuity_provenance (new)",
        "next_action",
    ],
    "fields_that_differ_between_prior_raw_report_and_current_raw_report": [
        "review_scope_sha256 (aa2c114f... -> 004c98f1...)",
        "sources[0..6].absolute_path (consumer root moved from native/claude-01/project to native/claude-export-01/project)",
    ],
    "fields_verified_identical": [
        "plan",
        "baseline",
        "criteria (20 rows: id, check, domain, mode, sources, stage, output, record_sha256, record_status current, current_record_sha256)",
        "sources excluding absolute_path (id, path, sha256, observed_sha256, record_sha256, status resolved, excerpts, locator, scope, source_class, line_count)",
        "controls (4)",
        "decisions (2)",
        "selections (3, including the changed queue.working selection)",
        "request (id, state prepared, remote_id null, intent_sha256, request incl. arguments/schema/discovery/declaration_text/request_sha256, blockers, next_action)",
        "state (path, sha256, revision 88)",
        "diagnostics (queue.working changed_selection)",
    ],
    "fingerprint_difference_basis": "installed kit excludes absolute source locations and job lifecycle observations from review_scope_sha256 (runtime/pixl/production_review.py); the job carries no lifecycle observations in either report, so the differing value reflects the kit fingerprint definition and the moved absolute paths, not a semantic change; see work/export-review-01/fingerprint-reproduction.json",
    "semantic_evidence_changed": False,
    "reason_rows_not_reauthored": "EXPORT-REVIEW.md: retain the completed comparison without re-authoring it when the actual semantic evidence is unchanged; the caller verified the evidence field by field (work/export-review-01/record-continuity.json, raw-vs-prior-raw-diff.json)",
}
out["next_action"] = (
    "Retain this file, check structural coverage with pixl_request_review(comparison='work/export-review-01/caller-comparison.json'), "
    "then return EXPORT-RESULT.json. No production, dispatch, preparation, revision of the plan or request, or acceptance is assigned. "
    "The old normal-motion contract still needs the r2 corrections before future adoption; the changed reduced-motion requirement "
    "and the prepared blocked intent remain unresolved."
)
dst = Path("work/export-review-01/caller-comparison.json")
dst.write_bytes((json.dumps(out, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
back = json.loads(dst.read_bytes().decode("utf-8"))


def canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


checks = {
    "criterion_comparisons_verbatim": canon(back["criterion_comparisons"]) == canon(prior["criterion_comparisons"]),
    "discrepancies_verbatim": canon(back["discrepancies_with_specialist"]) == canon(prior["discrepancies_with_specialist"]),
    "reduced_motion_verbatim": canon(back["reduced_motion_disposition"]) == canon(prior["reduced_motion_disposition"]),
    "verdict_verbatim": canon(back["verdict"]) == canon(prior["verdict"]),
    "specialist_artifacts_verbatim": canon(back["specialist_artifacts"]) == canon(prior["specialist_artifacts"]),
    "sources_read_verbatim": canon(back["sources_read_independently"]) == canon(prior["sources_read_independently"]),
    "measurements_verbatim": canon(back["caller_measurements"]) == canon(prior["caller_measurements"]),
    "review_scope_sha256": back["review_scope_sha256"],
    "prior_file_unchanged": sha(prior_path.read_bytes()) == sha(prior_b),
    "new_file_sha256": sha(dst.read_bytes()),
    "new_file_bytes": dst.stat().st_size,
    "row_count": len(back["criterion_comparisons"]),
}
json.dump(checks, io.open("work/export-review-01/caller-comparison-build-check.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(checks, indent=1))
