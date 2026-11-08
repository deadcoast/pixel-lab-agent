"""Repeat archived artistic-authority cases against a fresh, frozen current kit."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from evaluations import host_trials as runner

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / "evidence/artistic-authority/archives"


def prepare(series: str) -> Path:
    if Path(series).name != series or series in (".", ".."):
        raise ValueError("series must be one new directory name")
    runner.EVIDENCE = ROOT / "evidence/artistic-authority" / series
    original = json.loads((ARCHIVES / "reread-extended.manifest.json").read_text())
    archive = ARCHIVES / original["archive"]
    if runner.sha(archive) != original["sha256"]:
        raise ValueError("historical archive changed")
    with zipfile.ZipFile(archive) as zf:
        def read(name: str) -> bytes:
            path = "reread-extended/" + name
            value = zf.read(path)
            if hashlib.sha256(value).hexdigest() != original["files"][path]:
                raise ValueError("historical input changed: " + name)
            return value

        prior = json.loads(read("protocol.json"))
        runner.CASES.update(prior["cases"])
        existing = runner.EVIDENCE / "protocol.json"
        if existing.exists():
            saved = json.loads(existing.read_text())
            if saved["wrapper_sha256"] != runner.sha(Path(__file__)):
                raise ValueError("wrapper changed; use a new series")
            if saved["recorder_sha256"] != runner.sha(Path(runner.__file__)):
                raise ValueError("recorder changed; use a new series")
            runner.freeze()
            if saved["fixtures"] != runner.inventory(runner.EVIDENCE / "fixture-inputs"):
                raise ValueError("frozen fixture changed")
            return runner.EVIDENCE
        identity = runner.freeze()
        for name in prior["fixtures"]:
            (runner.EVIDENCE / "fixture-inputs" / name).write_bytes(read("fixture-inputs/" + name))
        controls = runner.EVIDENCE / "discovery/codex-session-overrides.json"
        controls.parent.mkdir(parents=True, exist_ok=True)
        controls.write_bytes(read("discovery/codex-session-overrides.json"))
        shutil.copyfile(Path(__file__), runner.EVIDENCE / "trial-runner.py.txt")
        runner.write_json(existing, {
            "task": "PX-SKILL-002", "cases": prior["cases"], "criteria": prior["criteria"],
            "fixtures": runner.inventory(runner.EVIDENCE / "fixture-inputs"),
            "wrapper_sha256": runner.sha(Path(__file__)),
            "recorder_sha256": runner.sha(Path(runner.__file__)),
            "controls_sha256": runner.sha(controls),
            "package_manifest_sha256": identity["bundle_manifest_sha256"],
            "historical_archive_sha256": original["sha256"],
            "timeout_seconds": None, "requested_model": None,
            "differences": ["Current packaged profile and skills.", "Current host defaults for model and reasoning.",
                            "Supervised runs without the old 600-second ceiling.",
                            "Provider-key environment variables excluded.",
                            "Codex workspace actions use native --approve-for-me automatic review; no elevation or automatic tool approval override."],
            "grading": "Independent reading of complete saved approach, final response and actual tool results. Process completion is ungraded.",
        })
    return runner.EVIDENCE


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series", required=True)
    parser.add_argument("--host", choices=("claude", "codex"))
    parser.add_argument("--case", choices=("selective-style", "small-separated"))
    parser.add_argument("--attempt")
    args = parser.parse_args()
    if bool(args.host) != bool(args.case) or bool(args.host) != bool(args.attempt):
        parser.error("host, case and attempt must be supplied together")
    if args.attempt and (Path(args.attempt).name != args.attempt or args.attempt in (".", "..")):
        parser.error("attempt must be one fresh directory name")
    parent = ROOT / "build/authority-projects"
    parent.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(parent)
    folder = prepare(args.series)
    if args.host:
        print(runner.run(args.host, args.case, args.attempt, None, None,
                         sandbox="workspace-write", retain_session=args.host == "codex"))
    else:
        print(folder)


if __name__ == "__main__":
    main()
