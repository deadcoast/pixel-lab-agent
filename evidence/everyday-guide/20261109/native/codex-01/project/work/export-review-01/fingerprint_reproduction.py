"""Reproduce review_scope_sha256 with the installed kit's definition
(runtime/pixl/production_review.py: scope without sources[].absolute_path and with request reduced to
id/intent_sha256/request; platform._sha = sha256 of json.dumps(sort_keys, separators=(',',':'), ensure_ascii=False)).
Applies it to both the fresh raw report and the prior raw report to show whether the fingerprint difference
is explained by the definition alone. Run: python -I work/export-review-01/fingerprint_reproduction.py
"""
import hashlib
import io
import json
from pathlib import Path


def sha_json(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    ).hexdigest()


def scope_of(report):
    return {
        "plan": report["plan"],
        "baseline": report["baseline"],
        "criteria": report["criteria"],
        "sources": report["sources"],
        "controls": report["controls"],
        "decisions": report["decisions"],
        "selections": report["selections"],
        "request": report["request"],
    }


def current_definition(report):
    scope = scope_of(report)
    request = scope["request"]
    return sha_json(
        {
            **scope,
            "sources": [{k: v for k, v in s.items() if k != "absolute_path"} for s in scope["sources"]],
            "request": {k: request[k] for k in ("id", "intent_sha256", "request")} if request else None,
        }
    )


def full_scope_variant(report):
    # candidate earlier definition: whole scope including absolute paths and lifecycle fields
    return sha_json(scope_of(report))


def no_abs_full_request_variant(report):
    scope = scope_of(report)
    return sha_json({**scope, "sources": [{k: v for k, v in s.items() if k != "absolute_path"} for s in scope["sources"]]})


def abs_reduced_request_variant(report):
    scope = scope_of(report)
    request = scope["request"]
    return sha_json({**scope, "request": {k: request[k] for k in ("id", "intent_sha256", "request")} if request else None})


fresh = json.loads(Path("work/export-review-01/request-review-raw.txt").read_bytes().decode("utf-8"))
prior = json.loads(Path("work/criteria-review-01/request-review-raw.txt").read_bytes().decode("utf-8"))
result = {
    "definition_source": ".agents/skills/pixl-kit/runtime/pixl/production_review.py (scope_hash) and platform.py (_sha/_json_bytes)",
    "fresh_report_review_scope_sha256": fresh["review_scope_sha256"],
    "prior_report_review_scope_sha256": prior["review_scope_sha256"],
    "current_definition_on_fresh_report": current_definition(fresh),
    "current_definition_on_prior_report": current_definition(prior),
    "variants_on_prior_report": {
        "full_scope_with_absolute_paths_and_lifecycle": full_scope_variant(prior),
        "no_absolute_paths_full_request": no_abs_full_request_variant(prior),
        "absolute_paths_reduced_request": abs_reduced_request_variant(prior),
    },
    "variants_on_fresh_report": {
        "full_scope_with_absolute_paths_and_lifecycle": full_scope_variant(fresh),
        "no_absolute_paths_full_request": no_abs_full_request_variant(fresh),
        "absolute_paths_reduced_request": abs_reduced_request_variant(fresh),
    },
}
result["current_definition_reproduces_fresh_value"] = result["current_definition_on_fresh_report"] == fresh["review_scope_sha256"]
result["prior_report_under_current_definition_equals_fresh_value"] = result["current_definition_on_prior_report"] == fresh["review_scope_sha256"]
result["prior_value_reproduced_by_variant"] = [
    name for name, value in result["variants_on_prior_report"].items() if value == prior["review_scope_sha256"]
]
result["lifecycle_fields_in_request"] = {
    "fresh": {k: fresh["request"][k] for k in ("state", "remote_id", "blockers", "next_action")},
    "prior": {k: prior["request"][k] for k in ("state", "remote_id", "blockers", "next_action")},
    "identical": {k: fresh["request"][k] for k in ("state", "remote_id", "blockers", "next_action")}
    == {k: prior["request"][k] for k in ("state", "remote_id", "blockers", "next_action")},
}
json.dump(result, io.open("work/export-review-01/fingerprint-reproduction.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(result, indent=1))
