"""Compile reviewed observations, preserving the boundary between evidence layers."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime

from host_trials import EVIDENCE, REPO, freeze, sha, verify_run, write_json


def main() -> None:
    identity = freeze()
    review = json.loads((EVIDENCE / "criterion-review.json").read_text(encoding="utf-8"))
    integrity = json.loads((EVIDENCE / "integrity.json").read_text(encoding="utf-8"))
    if integrity["error_count"]:
        raise ValueError("evidence replay has failures")
    reviewed_attempts = {entry["attempt"] for entry in review["runs"] + review["supplementary_continuations"]}
    if reviewed_attempts != {entry["attempt"] for entry in integrity["runs"]}:
        raise ValueError("attempts remain unreviewed or unreplayed")
    catalog = json.loads((EVIDENCE / "profile-scenarios.json").read_text(encoding="utf-8"))
    criteria = {case["id"]: case["criteria"] for case in catalog["cases"]}
    counts: Counter[str] = Counter()
    for entry in review["runs"]:
        if [c["criterion"] for c in entry["criteria"]] != criteria[entry["case_id"]]:
            raise ValueError("review omitted or changed an original criterion")
        counts.update(c["verdict"] for c in entry["criteria"])
        for name, expected in entry["reviewed_evidence_hashes"].items():
            if sha(EVIDENCE / "runs" / entry["attempt"] / name) != expected:
                raise ValueError("reviewed trial changed")
    for entry in review["supplementary_continuations"]:
        for name, expected in entry["reviewed_evidence_hashes"].items():
            if sha(EVIDENCE / "runs" / entry["attempt"] / name) != expected:
                raise ValueError("reviewed continuation changed")
    if dict(counts) != review["summary"]["original_criterion_verdicts"]:
        raise ValueError("criterion totals differ")
    attempts = []
    for replay in integrity["runs"]:
        trial = EVIDENCE / "runs" / replay["attempt"]
        if verify_run(trial) or sha(trial / "record.json") != replay["record_sha256"]:
            raise ValueError("replayed trial changed")
        record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
        events = []
        for line in (trial / "stdout.jsonl").read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        usage = next((e["usage"] for e in reversed(events) if e.get("type") == "turn.completed"), None)
        attempts.append({
            "attempt": replay["attempt"], "case_id": record["case_id"],
            "phase": record.get("phase", "fresh"), "host": record["host_and_version"],
            "requested_model": record["requested_model"],
            "host_reported_model": record.get("host_reported_model") or record.get("observed_model"),
            "model_identity_limit": "CLI request/host configuration is not an independent API model attestation; Claude's failed attempt only has init metadata.",
            "execution_status": record["execution_status"], "elapsed_seconds": record["elapsed_seconds"],
            "native_journal_retained": record.get("native_journal_found", False),
            "artifact_count": len(record["artifacts"]), "record_sha256": replay["record_sha256"],
            "codex_reported_usage": usage,
            "package_mutated": record["package_mutated"],
            "deterministic_state_replays": len(replay["state_replay"]),
        })
    visual_a = EVIDENCE / "runs" / "codex-visual-01"
    visual_b = EVIDENCE / "runs" / "codex-visual-02"
    repeated = sha(visual_a / "prompt.txt") == sha(visual_b / "prompt.txt") and all(
        sha(visual_a / "input-project" / name) == sha(visual_b / "input-project" / name)
        for name in ("reference.png", "candidate.png")
    )
    if not repeated:
        raise ValueError("visual repeat does not share exact prompt/input images")
    evidence_names = ["identity.json", "profile-scenarios.json", "fixture-oracle.json", "criterion-review.json",
                      "integrity.json", "recorder-review.json", "harness-tests.txt", "quality-checks.txt", "claude-auth-recheck.json"]
    report = {
        "version": 1, "observed_at": datetime.now(UTC).isoformat(),
        "status": "local_evaluation_complete_cross_host_behavior_blocked",
        "source_revision": identity["source_revision"], "source_tree_dirty": True,
        "bundle_manifest_sha256": identity["bundle_manifest_sha256"],
        "profile_hash": identity["profile_hash"], "skill_hashes": identity["skill_hashes"],
        "runtime_hashes": identity["runtime_hashes"],
        "coverage": review["summary"], "attempts": attempts,
        "separate_outcome_layers": {
            "host_discovery": {"codex": "native packaged-skill discovery verified", "claude": "native plugin, skill, agent and 24 local tools loaded"},
            "profile_behavior": {"codex": "seven completed model sessions; criterion-specific passes and unverified components retained", "claude": "unverified: expired OAuth prevented inference"},
            "controlled_artifact_outcomes": {"visual_defect_rejection": "both repeats rejected the missing antenna and eye", "repeat_prompt_and_input_bytes_equal": repeated, "native_viewer_evidence": "second visual trial only", "cold_intake": "all 39 predecessor artifact hashes unchanged"},
            "production_outcomes": {"live_pixellab": "not_exercised", "new_production_art": "not_created", "engine_acceptance": "not_exercised", "animation_or_tile_continuity": "not_exercised"},
        },
        "next_tasks": "evaluations/TODO.spec.md",
        "limitations": review["global_limitations"] + [
            "Temporary project separation is not an OS sandbox; the selected file-access setting is retained in each launch.",
            "No profile-disabled control arm: these observations do not measure the causal improvement contributed by PIXL.",
            "Most cases have one trial, and only the visual case was repeated; no general reliability or host-ranking claim is supported.",
            "The original runtime suite and POC receipts were preserved, not rerun by this evaluation.",
        ],
        "evidence_hashes": {name: sha(EVIDENCE / name) for name in evidence_names},
        "tooling_hashes": {name: sha(REPO / name) for name in (
            "evaluations/host_trials.py", "evaluations/check_host_evidence.py", "evaluations/write_host_report.py", "tests/test_host_evidence.py")},
    }
    write_json(EVIDENCE / "report.json", report)
    print(json.dumps({"attempts": len(attempts), "original_criteria": dict(counts), "status": report["status"]}))


if __name__ == "__main__":
    main()
