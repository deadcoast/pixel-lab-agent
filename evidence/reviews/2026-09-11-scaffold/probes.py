"""Reproduce the scaffold review using local fixtures in temporary directories.

Run with the project Python. Writes no project state; emits observations to stdout.
This is review evidence, not a production acceptance test or provider simulation.
"""

import hashlib
import json
import sys
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pixl.catalog import build
from pixl.codec import PixlError, Record, Ref, Symbol, record_hash
from pixl.graph import proof_scope, validate
from pixl.store import commit, initialize
from tests.support import sample


def rebind_decision(doc):
    doc.records["proof"].fields["bs"] = [
        {"rf": Ref(id_), "dg": record_hash(doc.records[id_])}
        for id_ in sorted(proof_scope(doc, ["decision"]))
    ]


def run():
    results = {
        "observed_at": datetime.now(UTC).isoformat(),
        "baseline_commit": "52f86dd",
        "scope": "Current unchanged runtime; documentation and role-boundary edits may be present.",
        "runtime_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((ROOT / "pixl").iterdir())
            if path.suffix in (".py", ".json")
        },
    }
    with TemporaryDirectory(prefix="pixl scaffold review ") as tmp:
        root = Path(tmp)
        doc = sample(root)
        doc.records["task"].fields["st"] = Symbol("active")
        initial = initialize(root / ".pixl", doc, root)
        candidate = deepcopy(doc)
        candidate.revision = 1
        candidate.records["task"].fields.update(
            st=Symbol("done"), ev=[Ref("proof")]
        )
        result = commit(root / ".pixl", candidate, initial["hash"], root)
        results["local_only_completion"] = {
            "committed_revision": result["revision"],
            "task_state": candidate.records["task"].fields["st"].value,
            "receipt_modes": [candidate.records["proof"].fields["md"].value],
            "visual_receipts": 0,
            "engine_receipts": 0,
            "limitation": "A report fixture legitimately completes with local evidence; the schema has no task-specific acceptance obligations. No art was accepted.",
        }
        planned = deepcopy(doc)
        planned.records["asset"].fields.update(
            ur="future-sprite.png", dg="0" * 64
        )
        rebind_decision(planned)
        try:
            validate(planned, root)
            results["planned_output_validation"] = {"accepted": True}
        except PixlError as error:
            results["planned_output_validation"] = {
                "accepted": False, "code": error.code, "detail": str(error)
            }
        succeeded = deepcopy(doc)
        succeeded.records["job"] = Record(
            "job", "J", {
                "tk": Ref("task"), "tl": "fixture-tool", "ah": "a" * 64,
                "si": Symbol("succeeded"), "ri": "synthetic-review-id",
                "ev": [Ref("proof")],
            }
        )
        validate(succeeded, root)
        results["job_summary_without_journal"] = {
            "accepted": True,
            "receipt_bound_records": [
                row["rf"].id for row in succeeded.records["proof"].fields["bs"]
            ],
            "job_bound": False,
            "remote_executed": False,
        }
        no_proof = deepcopy(doc)
        no_proof.records["decision"].fields["pc"] = []
        rebind_decision(no_proof)
        try:
            validate(no_proof, root)
            results["unproven_decision"] = {"accepted": True}
        except PixlError as error:
            results["unproven_decision"] = {
                "accepted": False, "code": error.code, "detail": str(error)
            }
    results["default_catalog"] = {
        "paths": [row["path"] for row in build(ROOT)["documents"]],
        "note": "AGENTS.md was added by this review; before edits only NOTICE.md and README.md were indexed.",
    }
    results["current_supplied_sources"] = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "lines": len(path.read_text(encoding="utf-8-sig").splitlines()),
        }
        for path in sorted((ROOT / "training/original-docs").glob("*.md"))
    ]
    results["limitations"] = [
        "Synthetic local fixtures only; no production assets or remote IDs.",
        "No PixelLab execution, engine import, or model performance claims.",
        "Each observation demonstrates only its named runtime path.",
    ]
    return results


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
