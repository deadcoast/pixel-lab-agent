"""Copy the host-spilled coverage result as exact bytes, write a UTF-8 formatted copy, verify parse equality
and summarize comparison_coverage. Run: python -I work/export-review-01/coverage_retain.py SPILLED_PATH"""
import hashlib
import io
import json
import sys
from pathlib import Path

src = Path(sys.argv[1])
b = src.read_bytes()
raw = Path("work/export-review-01/request-review-coverage-raw.txt")
raw.write_bytes(b)
cov = json.loads(b.decode("utf-8"))
fmt = Path("work/export-review-01/request-review-coverage.json")
fmt.write_bytes((json.dumps(cov, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
re = json.loads(fmt.read_bytes().decode("utf-8"))
fresh = json.loads(Path("work/export-review-01/request-review-raw.txt").read_bytes().decode("utf-8"))
same_except_cov = {k: v for k, v in cov.items() if k != "comparison_coverage"} == {
    k: v for k, v in fresh.items() if k != "comparison_coverage"
}
out = {
    "raw": {
        "path": "work/export-review-01/request-review-coverage-raw.txt",
        "sha256": hashlib.sha256(b).hexdigest(),
        "bytes": len(b),
        "spilled_source": str(src),
    },
    "formatted": {
        "path": "work/export-review-01/request-review-coverage.json",
        "sha256": hashlib.sha256(fmt.read_bytes()).hexdigest(),
        "bytes": fmt.stat().st_size,
        "parsed_equal_to_raw": re == cov,
    },
    "comparison_coverage": cov["comparison_coverage"],
    "caller_comparison": cov["caller_comparison"],
    "consistent": cov["consistent"],
    "review_scope_sha256": cov["review_scope_sha256"],
    "identical_to_fresh_report_except_comparison_coverage": same_except_cov,
    "diagnostics": cov["diagnostics"],
    "request_state": cov["request"]["state"],
    "blockers": cov["request"]["blockers"],
}
json.dump(out, io.open("work/export-review-01/coverage-summary.json", "w", encoding="utf-8"), indent=1, ensure_ascii=True)
print(json.dumps(out, indent=1, ensure_ascii=True))
