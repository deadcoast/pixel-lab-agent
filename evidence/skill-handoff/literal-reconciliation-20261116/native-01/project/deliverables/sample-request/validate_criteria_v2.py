"""Validate sample-criteria.json against the kit's asset-plan.schema.json. READ-ONLY by default.

Successor of validate_criteria.py (retained unchanged as the script that produced
criteria-schema-validation.json, sha256 93643a34...). The v1 script wrote that retained
artifact unconditionally on every run, so reproducing the validation as its docstring
instructed overwrote a file whose hash is quoted in bound artifacts (caller finding 1,
2026-11-15e). This version never writes unless an explicit --out path is given, and
refuses to write over an existing file. Reviewers reproducing the validation must use
this script, not v1.

Passing means structural validity against the schema plus file-local line-bound sanity.
It is not a semantic review, not acceptance and not provider-schema validity.

Usage (consumer root, selected interpreter, isolated mode):
  python -I deliverables/sample-request/validate_criteria_v2.py                # print only
  python -I deliverables/sample-request/validate_criteria_v2.py --out NEW.json # also save
  python -I deliverables/sample-request/validate_criteria_v2.py --criteria PATH --schema PATH
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import UTC, datetime

from jsonschema import Draft202012Validator

DEFAULT_SCHEMA = "pixl-kit/runtime/pixl/asset-plan.schema.json"
DEFAULT_CRITERIA = "deliverables/sample-request/sample-criteria.json"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def report(schema_path, criteria_path):
    schema = json.load(open(schema_path, encoding="utf-8"))
    plan = json.load(open(criteria_path, encoding="utf-8-sig"))
    validator = Draft202012Validator(schema)
    errors = [
        {"path": "/" + "/".join(str(p) for p in e.absolute_path), "message": e.message}
        for e in sorted(validator.iter_errors(plan), key=lambda e: list(e.absolute_path))
    ]
    bounds = []
    for output in plan.get("outputs", []):
        for criterion in output.get("criteria", []):
            for source in criterion.get("sources", []):
                if "lines" in source:
                    with open(source["path"], "rb") as handle:
                        total = handle.read().count(b"\n")
                    first, last = source["lines"]
                    bounds.append({
                        "criterion": criterion["id"], "path": source["path"],
                        "lines": source["lines"], "file_lines": total,
                        "in_bounds": 1 <= first <= last <= total,
                    })
    return {
        "validated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "validator": "jsonschema.Draft202012Validator",
        "script": "deliverables/sample-request/validate_criteria_v2.py",
        "schema": {"path": schema_path, "sha256": sha(schema_path)},
        "criteria": {"path": criteria_path, "sha256": sha(criteria_path)},
        "schema_valid": not errors,
        "errors": errors,
        "line_bounds": bounds,
        "all_line_bounds_inside_files": all(b["in_bounds"] for b in bounds),
        "meaning": "Structural validity against asset-plan.schema.json and file-local bound "
                   "sanity only. Not a semantic review, not acceptance, not provider-schema "
                   "validity. This run wrote nothing unless --out named a fresh path.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--criteria", default=DEFAULT_CRITERIA)
    parser.add_argument("--out", help="save the report to this NEW path (refuses to overwrite)")
    args = parser.parse_args()
    if args.out and os.path.exists(args.out):
        print(json.dumps({"error": f"refusing to overwrite existing file: {args.out}"}))
        return 2
    result = report(args.schema, args.criteria)
    text = json.dumps(result, indent=1)
    print(text)
    if args.out:
        with open(args.out, "x", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
    return 0 if result["schema_valid"] and result["all_line_bounds_inside_files"] else 1


if __name__ == "__main__":
    sys.exit(main())
