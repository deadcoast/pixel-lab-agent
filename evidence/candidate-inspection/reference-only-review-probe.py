import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from pixl import codec, inspection, store
from tests.inspection_support import options, project

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    project(root)
    folder = root / ".pixl"
    p = inspection.prepare(
        folder, codec.digest(store.load(folder)), "candidate", "packet", options(), root
    )
    v = next(v for v in p["views"] if v["source"] == "reference")
    o = {
        "reviewer": "actor",
        "observed_at": datetime.now(UTC).isoformat(),
        "observations": [
            {"view": v["id"], "delivered_size": None, "note": "Viewed reference only."}
        ],
        "verdicts": [
            {
                "criterion": "q.visual",
                "status": "fail",
                "reason": "Candidate missing antenna.",
                "supersedes": None,
            }
        ],
        "next_action": "Revise candidate.",
        "limitations": [],
    }
    result = inspection.review(
        folder, codec.digest(store.load(folder)), "packet", "review", o, root
    )
    print(
        json.dumps(
            {
                "observed_source": v["source"],
                "candidate": "candidate",
                "published": result,
            },
            indent=2,
        )
    )
