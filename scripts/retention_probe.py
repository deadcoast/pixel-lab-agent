"""Exercise project source retention through an isolated installed CLI."""

import hashlib
import json
from pathlib import Path


def run_retention_probe(cli, root):
    root = Path(root)
    kit = root / "kit"
    source = kit / "resources/method.txt"
    source.parent.mkdir(parents=True)
    original = b"Original library source for the isolated installation check.\n"
    source.write_bytes(original)
    source_hash = hashlib.sha256(original).hexdigest()
    (kit / "bundle-manifest.json").write_text(
        json.dumps(
            {"files": [{"path": "resources/method.txt", "sha256": source_hash}]}
        ),
        "utf-8",
    )
    folder = root / ".pixl"
    created = cli(
        [
            "intake",
            str(folder),
            "--root",
            str(root),
            "--brief",
            "Synthetic source-retention check.",
        ]
    )
    state = folder / "state.px"
    document = cli(["decode", str(state)])
    document["revision"] += 1
    document["records"].append(
        {
            "id": "source.original",
            "kind": "S",
            "fields": {
                "ur": "kit/resources/method.txt",
                "dg": source_hash,
                "ln": [1, 1],
                "at": "2026-11-07",
                "au": {"$symbol": "study"},
            },
        }
    )
    candidate = root / "source-plan.json"
    candidate.write_text(json.dumps(document), "utf-8")
    published = cli(
        [
            "commit",
            str(folder),
            str(candidate),
            "--json",
            "--expect",
            created["hash"],
            "--root",
            str(root),
        ]
    )
    before = state.read_bytes()
    retained = cli(
        [
            "retain-library",
            str(folder),
            "kit",
            "--expect",
            published["hash"],
            "--root",
            str(root),
        ]
    )
    source.write_bytes(
        b"Updated library source; old proof is not proof of these bytes.\n"
    )
    report = cli(["workflow", str(state), "--root", str(root)])
    snippet = cli(
        [
            "source",
            "kit/resources/method.txt",
            "--expect",
            source_hash,
            "--start",
            "1",
            "--end",
            "1",
            "--root",
            str(root),
        ]
    )
    if (
        retained["state_changed"]
        or state.read_bytes() != before
        or report["hash"] != published["hash"]
        or report["retained_sources"][0]["expected_sha256"] != source_hash
        or snippet["text"] != original.decode()
        or not snippet["retained_revision"]
    ):
        raise RuntimeError(
            "installed source retention failed to preserve the exact declared revision"
        )
    return {
        "status": "pass",
        "state_unchanged": True,
        "original_source_sha256": source_hash,
        "scope": "Isolated installed CLI; synthetic library-source replacement and cold workflow/source retrieval.",
    }
