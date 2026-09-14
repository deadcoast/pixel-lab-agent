"""Independent operation review probes; no provider/model calls or generated bundles."""

import copy
import hashlib
import json
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from pixl import codec, inspection, store
from pixl.codec import PixlError
from tests.inspection_support import options, project

results = []
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    project(root)
    folder = root / ".pixl"
    prepared = inspection.prepare(
        folder, codec.digest(store.load(folder)), "candidate", "packet", options(), root
    )
    observation = {
        "reviewer": "actor",
        "observed_at": datetime.now(UTC).isoformat(),
        "observations": [
            {
                "view": prepared["views"][0]["id"],
                "delivered_size": None,
                "note": "Controlled review declaration.",
            }
        ],
        "verdicts": [
            {
                "criterion": "q.visual",
                "status": "fail",
                "reason": "Missing feature.",
                "supersedes": None,
            }
        ],
        "next_action": "Retain separate revision.",
        "limitations": ["No real host viewing."],
    }
    for name, mutate in [
        (
            "future observation",
            lambda x: x.update(
                observed_at=(datetime.now(UTC) + timedelta(days=1)).isoformat()
            ),
        ),
        (
            "before preparation",
            lambda x: x.update(observed_at="2020-01-01T00:00:00+00:00"),
        ),
        ("naive observation", lambda x: x.update(observed_at="2026-09-11T22:00:00")),
        ("unobserved visual failure", lambda x: x.update(observations=[])),
        (
            "engine pass",
            lambda x: x["verdicts"][0].update(criterion="q.engine", status="pass"),
        ),
        (
            "false supersession",
            lambda x: x["verdicts"][0].update(supersedes="not.current"),
        ),
    ]:
        declared = copy.deepcopy(observation)
        mutate(declared)
        before = codec.digest(store.load(folder))
        try:
            inspection.review(folder, before, "packet", "rejected", declared, root)
        except PixlError as error:
            assert before == codec.digest(store.load(folder))
            results.append(
                {
                    "probe": name,
                    "result": "rejected without state change",
                    "error": error.code,
                }
            )
        else:
            raise AssertionError(name)
    inspection.review(
        folder, codec.digest(store.load(folder)), "packet", "review", observation, root
    )
    doc = store.load(folder)
    before = codec.digest(doc)
    original = doc.records["q.visual"].fields["ck"]
    doc.records["q.visual"].fields["ck"] = "Amended visual condition."
    for record in doc.records.values():
        if record.kind in ("E", "V"):
            record.fields["ob"] = True
    doc.revision += 1
    store.commit(folder, doc, before, root)
    reported = inspection.report(store.load(folder), root, "packet")["packets"][0]
    assert "q.visual" in reported["binding_drift"]
    assert (
        next(q for q in reported["criteria"] if q["id"] == "q.visual")["check"]
        == original
    )
    assert len(reported["reviews"]) == 1
    assert reported["reviews"][0]["observation"]["verdicts"][0]["status"] == "fail"
    results.append(
        {
            "probe": "amendment after retained failure",
            "result": "original check and failed review preserved; drift explicit",
        }
    )
print(
    json.dumps(
        {
            "source_sha256": hashlib.sha256(
                Path("pixl/inspection.py").read_bytes()
            ).hexdigest(),
            "results": results,
        },
        indent=2,
    )
)
