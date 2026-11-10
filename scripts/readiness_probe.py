"""Check installed readiness and actual local source retrieval, without provider work."""

import hashlib
import json


def run_readiness_probe(cli, consumer, expected_kind, installation=None):
    consumer.mkdir(exist_ok=False)
    source = consumer / "BRIEF.md"
    source.write_text("Readiness fixture: preserve this source and report its exact bytes.\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    observations = consumer / "observations.json"
    observations.write_text(json.dumps({
        "host": "codex", "observed_at": "2026-11-10T00:00:00Z",
        "local_tools": {"names": [], "complete_inventory": False},
        "official_tools": {"names": [], "complete_inventory": True},
    }), encoding="utf-8")
    before = {path.name: path.read_bytes() for path in consumer.iterdir()}
    args = ["readiness", "--root", str(consumer), "--host", "codex", "--observations", "observations.json"]
    if installation:
        args += ["--installation", str(installation)]
    report = cli(args)
    assert report["installation"]["kind"] == expected_kind
    assert report["local_operations"]["runtime_requirements"] == "satisfied"
    assert report["specialist"]["named_role"] == "not_observed"
    assert report["official_pixellab"]["visibility"]["status"] == "not_listed"
    assert report["official_pixellab"]["authentication"] == "not_verified"
    # An actual read establishes more than a listed operation or installed file.
    retrieved = cli(["source", "BRIEF.md", "--root", str(consumer), "--expect", digest, "--start", "1", "--end", "1"])
    assert retrieved["sha256"] == digest
    assert {path.name: path.read_bytes() for path in consumer.iterdir()} == before
    return {"status": "pass", "installation_kind": expected_kind, "report": report,
            "source_sha256": digest, "consumer_files_unchanged": True,
            "scope": "Installed local execution and read-only report; supplied empty inventory is a fixture, not live provider discovery."}
