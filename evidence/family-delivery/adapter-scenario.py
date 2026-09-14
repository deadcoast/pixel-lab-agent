"""Retain two scripted local workflow scenarios; never execute a remote service.

Run once from the source checkout with the selected project interpreter. Existing
output is deliberately refused to preserve every prior run's bytes.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY))

from tests.test_family_operations import FamilyOperationTests  # noqa: E402


class RecordedFamilyOperations(FamilyOperationTests):
    def setUp(self):
        self.root = self.scenario_root
        self.root.mkdir()
        self.folder = self.root / ".pixl"

    def cli(self, *args, expected_code=0):
        result = super().cli(*args, expected_code=expected_code)
        self.events.append({
            "surface": "cli", "arguments": list(map(str, args)),
            "expected_exit": expected_code, "result": result,
        })
        return result

    def rpc(self, method, params=None):
        result = super().rpc(method, params)
        self.events.append({
            "surface": "mcp", "method": method, "params": params, "result": result,
        })
        return result


def main():
    destination = Path(__file__).with_name("adapter-scenario")
    destination.mkdir()
    instructions = destination / "instructions"
    instructions.mkdir()
    sources = [
        "agent/PROFILE.md", "plugins/pixl/skills/pixl/SKILL.md",
        "plugins/pixl/skills/pixl/references/family-delivery.md",
        "plugins/pixl/skills/pixl/references/provider-recovery.md",
        "plugins/pixl/skills/pixl/references/intake-sample.md",
        "plugins/pixl/skills/pixl/references/runtime.md",
    ]
    report = {
        "purpose": "Scripted local family operation walkthrough inspected against authored instructions",
        "limits": [
            "No independent profile-compliance trial or controlled before/after benchmark",
            "All provider observations and passing fixture verdicts are explicitly synthetic",
            "No real provider call, actual art-quality verdict, animation playback, tile assembly or target-engine execution",
        ],
        "sources": [], "scenarios": [],
    }
    for source in sources:
        path = REPOSITORY / source
        copied = instructions / path.name
        shutil.copyfile(path, copied)
        report["sources"].append({
            "source": source, "retained": copied.relative_to(destination).as_posix(),
            "sha256": hashlib.sha256(copied.read_bytes()).hexdigest(),
        })
    scenarios = [
        ("unknown-member", "test_cold_unknown_member_job_blocks_snapshot_without_repeating_dispatch"),
        ("unavailable-engine", "test_mcp_snapshot_and_cold_report_preserve_unavailable_engine_boundary"),
    ]
    try:
        for name, method in scenarios:
            entry = {"name": name, "method": method, "events": [], "passed": False}
            report["scenarios"].append(entry)
            scenario = RecordedFamilyOperations(method)
            scenario.scenario_root = destination / name
            scenario.events = entry["events"]
            scenario.setUp()
            getattr(scenario, method)()
            entry["passed"] = True
        (destination / "handoff.md").write_text(
            "# Retained fictional scenario handoff\n\n"
            "This is a developer walkthrough, not production art or remote execution. "
            "Passing visual/live fixture receipts exercise recording rules only.\n\n"
            "- `unknown-member/.pixl/state.px`: member.job remains unknown after its one local "
            "dispatch claim. Both family snapshot routes refused new retention. Start with family, "
            "workflow and jobs using unknown-member as root; read the saved request and reconcile "
            "that attempt before another dispatch or snapshot. No real provider exists for this fixture.\n"
            "- `unavailable-engine/.pixl/state.px`: package is nominated and retained files are "
            "under its X path in .pixl/deliveries. The target check is unavailable, and the attempted "
            "done transition was refused. Start with family, workflow and jobs using unavailable-engine "
            "as root, open the manifest/copied PNGs, and inspect engine.unavailable. Its concrete next "
            "action is to import these files into the named target project and execute the saved "
            "import checks before accepting delivery. The named engine/project is fictional; no real "
            "engine acceptance can be performed or claimed from these files.\n",
            encoding="utf-8",
        )
    finally:
        (destination / "record.json").write_text(
            json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({"report": str(destination / "record.json"), "scenarios_passed": len(scenarios)}))


if __name__ == "__main__":
    main()
