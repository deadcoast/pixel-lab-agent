"""Exercise installed/copy review authoring with synthetic observations."""

import hashlib
import json
from datetime import UTC, datetime

from pixl import codec, store


def run_candidate_review_probe(cli, root):
    from tests.family_support import family

    root.mkdir()
    folder = root / ".pixl"
    family(root, folder)
    snapshot = cli(["family-snapshot", str(folder), "delivery.output", "review.package",
                    "--expect", codec.digest(store.load(folder)), "--root", str(root)])
    ctx = cli(["review-context", str(folder / "state.px"), "review.package", "--root", str(root)])
    evidence = root / "synthetic-observations.txt"
    evidence.write_text("Synthetic distribution probe; not a real visual or engine observation.\n", encoding="utf-8")
    observation = {
        "version": 1, "binding_hash": ctx["binding_hash"], "reviewer": "actor",
        "observed_at": datetime.now(UTC).isoformat(),
        "observations": [{"path": evidence.name, "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
                          "mode": mode, "note": "Synthetic distribution fixture"} for mode in ["local", "visual", "live"]],
        "verdicts": [{"criterion": q["id"], "status": "pass", "reason": "Synthetic distribution check",
                      "supersedes": q["verdict"], "observations": [["local", "visual", "live"].index(q["mode"])]}
                     for q in ctx["criteria"]],
        "action": "complete", "next_action": "Inspect the retained distribution result", "limitations": ["Synthetic fixture"],
    }
    request = root / "review.json"
    request.write_text(json.dumps(observation), encoding="utf-8")
    args = ["candidate-review", str(folder), "review.package", "distribution.review", str(request), "--root", str(root)]
    result = cli(args + ["--expect", snapshot["hash"]])
    repeated = cli(args + ["--expect", result["state_hash"]])
    exported = cli(args + ["--expect", result["state_hash"], "--result-path", "work/review-result.json"])
    saved_bytes = (root / exported["result_path"]).read_bytes()
    saved = json.loads(saved_bytes)
    if not (result["current_acceptance"]["task_complete"] and result["nominated"]
            and not result["snapshot_acceptance"]["accepted"] and repeated["reused_review"]
            and not repeated["publications"] and repeated["state_hash"] == result["state_hash"]):
        raise RuntimeError("Installed candidate/family review failed completion or replay checks")
    if not (exported["result_saved"] and saved == repeated
            and hashlib.sha256(saved_bytes).hexdigest() == exported["result_sha256"]):
        raise RuntimeError("Installed review result export lost exact JSON or identity")
    return {"status": "pass", "checks": ["family review retention", "explicit nomination/completion",
            "immutable creation versus current acceptance", "identical retry without duplicate publication",
            "exact result file export and digest"],
            "scope": "Synthetic distribution operation, not native/artistic acceptance"}
