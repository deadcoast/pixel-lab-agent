"""Validate sample-criteria.json against the kit's asset-plan.schema.json and retain the result.

Read-only apart from writing criteria-schema-validation.json beside the criteria file.
Uses the same Draft 2020-12 validator class the runtime uses (request_review.py line 107,
plar_prepare.py SCHEMA). Passing here means structural validity only; it is not a review,
not acceptance and not provider schema validity.

Usage (consumer root, selected interpreter):
  python -I deliverables/sample-request/validate_criteria.py
"""
import hashlib
import json
from datetime import UTC, datetime

from jsonschema import Draft202012Validator

SCHEMA = "pixl-kit/runtime/pixl/asset-plan.schema.json"
CRITERIA = "deliverables/sample-request/sample-criteria.json"
OUT = "deliverables/sample-request/criteria-schema-validation.json"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def main():
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    plan = json.load(open(CRITERIA, encoding="utf-8-sig"))
    validator = Draft202012Validator(schema)
    errors = [
        {"path": "/" + "/".join(str(p) for p in e.absolute_path), "message": e.message}
        for e in sorted(validator.iter_errors(plan), key=lambda e: list(e.absolute_path))
    ]
    # line-bound sanity: every cited `lines` range lies inside the cited file
    bounds = []
    for output in plan["outputs"]:
        for criterion in output["criteria"]:
            for source in criterion["sources"]:
                if "lines" in source:
                    with open(source["path"], "rb") as handle:
                        total = handle.read().count(b"\n")
                    first, last = source["lines"]
                    bounds.append({
                        "criterion": criterion["id"], "path": source["path"],
                        "lines": source["lines"], "file_lines": total,
                        "in_bounds": 1 <= first <= last <= total,
                    })
    report = {
        "validated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "validator": "jsonschema.Draft202012Validator",
        "schema": {"path": SCHEMA, "sha256": sha(SCHEMA)},
        "criteria": {"path": CRITERIA, "sha256": sha(CRITERIA)},
        "schema_valid": not errors,
        "errors": errors,
        "line_bounds": bounds,
        "all_line_bounds_inside_files": all(b["in_bounds"] for b in bounds),
        "meaning": "Structural validity against asset-plan.schema.json and file-local bound sanity only. Not a semantic review, not acceptance, not provider-schema validity.",
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=1)
        handle.write("\n")
    print(json.dumps(report, indent=1))
    return 0 if report["schema_valid"] and report["all_line_bounds_inside_files"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
