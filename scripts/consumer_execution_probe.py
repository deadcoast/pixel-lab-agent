"""Exercise installed profile retention without requiring optional browser access."""

import hashlib
import json


def run_consumer_execution_probe(cli, root):
    from tests.test_consumer_execution import execution_fixture

    root.mkdir()
    state, config = execution_fixture(root)
    before = state.read_bytes()
    config_path = root / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    exported = cli(["consumer-execute", str(state), "package", str(config_path),
                    "--out", "work/execution", "--root", str(root),
                    "--node", str(root / "missing-node.exe"),
                    "--result-path", "work/export.json"], expected_returncode=1)
    raw = (root / exported["result_path"]).read_bytes()
    result = json.loads(raw)
    sources = json.loads((root / "work/execution/renderer-sources.json").read_bytes())
    if not (exported["result_saved"] and exported["status"] == "unavailable"
            and hashlib.sha256(raw).hexdigest() == exported["result_sha256"]
            and result["error"]["code"] == "consumer_capability"
            and result["status"] == "unavailable" and state.read_bytes() == before
            and len(sources) == 6 and not result["renderer_executed"]
            and not result["automatic_acceptance"] and not result["state_changed"]):
        raise RuntimeError("Installed execution capability receipt or state boundary differs")
    for row in sources:
        if hashlib.sha256((root / row["copy"]).read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError("Installed execution profile copy differs")
    return {"status": "pass", "checks": ["installed public execution command",
            "six shipped profile files retained with exact hashes", "unavailable capability and nonzero exit",
            "exact result export", "unchanged state and no acceptance"],
            "scope": "Installed profile and failure-retention proof; no browser or artistic acceptance"}
