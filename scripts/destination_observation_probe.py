"""Exercise structured observation retention in installed distributions."""

import hashlib
import json
import zipfile


def run_destination_observation_probe(cli, root):
    from tests.test_destination_observation import observation_fixture

    root.mkdir()
    observation_fixture(root)
    state = str(root / ".pixl/state.px")
    before = cli(["validate", state, "--root", str(root)])
    exported = cli(["destination-import", state, "package", "capture/observation.json",
                    "--out", "work/destination", "--root", str(root),
                    "--result-path", "work/destination.json"])
    raw = (root / exported["result_path"]).read_bytes()
    result = json.loads(raw)
    bundle = (root / result["bundle"]["path"]).read_bytes()
    after = cli(["validate", state, "--root", str(root)])
    if not (exported["result_saved"] and hashlib.sha256(raw).hexdigest() == exported["result_sha256"]
            and hashlib.sha256(bundle).hexdigest() == result["bundle"]["sha256"]
            and before["hash"] == after["hash"] and result["files_verified"]
            and not any(result[k] for k in ("renderer_executed", "automatic_acceptance", "state_changed"))):
        raise RuntimeError("Installed destination import lost byte binding or acceptance boundary")
    with zipfile.ZipFile(root / result["bundle"]["path"]) as archive:
        index = json.loads(archive.read("index.json"))
        for row in index["files"]:
            if hashlib.sha256(archive.read(row["archive_path"])).hexdigest() != row["sha256"]:
                raise RuntimeError("Installed destination bundle lost a transitive observation")
    return {"status": "pass", "checks": ["structured report validation", "exact bundle and JSON export",
            "complete transitive observation retention", "unchanged state and no automatic acceptance"],
            "scope": "Synthetic distribution observation, not renderer execution or visual acceptance"}
