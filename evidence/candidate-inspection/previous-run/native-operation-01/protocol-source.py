"""Bounded native inspection trials with a preserved, explicitly seeded project.

The shared runner retains native events; this wrapper separately archives its own
protocol and the ZIP's exact file inventory. It never grades host behavior.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluations import host_trials as runner
from tests.inspection_support import project

CASE = "mechanical-pass-visual-rejection"
PROMPT = (
    "Use PIXL to review this saved candidate against its existing project requirements. "
    "The supplied seeded-project.zip contains a saved PX2 store in .pixl/, its brief "
    "and the two actual images. Extract it into this project without changing those "
    "files, then inspect candidate against reference and retain your review and next "
    "action through the packaged PIXL operation. The candidate has the expected "
    "dimensions and palette; determine whether it satisfies the saved identity "
    "criterion. Do not edit or generate art. No target browser project or remote "
    "provider is available. Finish with actual results and unfinished requirements."
)


def prepare(series: Path) -> None:
    runner.EVIDENCE = series
    runner.freeze()
    archive = series / "fixture-inputs" / "seeded-project.zip"
    protocol_path = series / "inspection-protocol.json"
    wrapper_hash = runner.sha(Path(__file__))
    controls = series / "discovery" / "codex-session-overrides.json"
    source = series / "protocol-source.py"
    if protocol_path.exists():
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        if (
            protocol["wrapper_sha256"] != wrapper_hash
            or protocol["shared_runner_sha256"] != runner.sha(Path(runner.__file__))
            or protocol["seed_zip_sha256"] != runner.sha(archive)
            or protocol["codex_session_overrides_sha256"] != runner.sha(controls)
            or runner.sha(source) != wrapper_hash
        ):
            raise ValueError("inspection protocol changed; start a new named series")
        return
    with tempfile.TemporaryDirectory(prefix="pixl-inspection-seed-") as folder:
        seed = Path(folder)
        project(seed)
        files = runner.inventory(seed)
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as output:
            for name in sorted(files):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                output.writestr(info, (seed / name).read_bytes())
    controls.parent.mkdir(exist_ok=True)
    shutil.copy2(
        runner.REPO / "evidence/host-evaluation/discovery/codex-session-overrides.json",
        controls,
    )
    shutil.copy2(
        runner.REPO / "evaluations/profile-scenarios.json",
        series / "profile-scenarios.json",
    )
    source.write_bytes(Path(__file__).read_bytes())
    runner.write_json(
        protocol_path,
        {
            "purpose": "New packaged inspection-operation trial; not a rerun of the original unseeded matrix.",
            "case_id": CASE,
            "prompt": PROMPT,
            "wrapper_sha256": wrapper_hash,
            "shared_runner_sha256": runner.sha(Path(runner.__file__)),
            "seed_zip_sha256": runner.sha(archive),
            "seed_files": files,
            "codex_session_overrides_sha256": runner.sha(controls),
            "additional_checks": [
                "Uses the packaged inspection prepare and review operation.",
                "Views actual retained native and enlarged images before visual verdicts.",
                "Retains candidate rejection and next action without art mutation or invented engine execution.",
            ],
            "limitations": [
                "The developer supplies a saved controlled project, not generated art.",
                "Views and judgments must be reviewed from actual host events; process completion is ungraded.",
                "Protocol wrapper and shared native recorder identities are both retained.",
            ],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series", default="native-operation")
    parser.add_argument("--host", choices=["claude", "codex"])
    parser.add_argument("--attempt")
    args = parser.parse_args()
    if not args.series or any(
        char not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for char in args.series
    ):
        parser.error("series must be a lowercase name")
    if bool(args.host) != bool(args.attempt):
        parser.error("host and attempt are required together")
    series = runner.REPO / "evidence/candidate-inspection" / args.series
    prepare(series)
    if args.host:
        runner.CASES[CASE] = {
            "files": ["seeded-project.zip"],
            "prompt": PROMPT,
            "variation": "Explicit saved developer project; tests the new inspection operation using preserved fixture pixels.",
        }
        print(
            runner.run(
                args.host,
                CASE,
                args.attempt,
                "gpt-6-astra" if args.host == "codex" else None,
                600,
                sandbox="danger-full-access",
                retain_session=args.host == "codex",
            )
        )
    else:
        print(series)


if __name__ == "__main__":
    main()
