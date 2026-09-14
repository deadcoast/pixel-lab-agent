"""Compile reviewed observations without promoting host receipts to behavior passes."""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import UTC, datetime
from itertools import combinations
from pathlib import Path
from typing import Any

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluations.host_trials import (
    EVIDENCE,
    REPO,
    freeze,
    sha,
    verify_run,
    write_json,
)

Row = dict[str, Any]
VERDICTS = {"pass", "fail", "unverified", "not_applicable"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def events_at(path: Path) -> list[Row]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def check_bindings(trial: Path, bindings: Row) -> None:
    for name, expected in bindings.items():
        path = (trial / name).resolve()
        if not path.is_relative_to(trial.resolve()) or not path.is_file() or sha(path) != expected:
            raise ValueError(f"reviewed trial changed: {trial.name}/{name}")


def option(command: list[str], name: str) -> str | None:
    if name in command and command.index(name) + 1 < len(command):
        return command[command.index(name) + 1]
    return None


def positive_usage(usage: Any) -> bool:
    return isinstance(usage, dict) and any(
        isinstance(usage.get(key), (int, float)) and usage[key] > 0
        for key in ("output_tokens", "reasoning_output_tokens")
    )


def codex_activity(events: list[Row]) -> bool:
    for event in events:
        item = event.get("item")
        if event.get("type") not in ("item.started", "item.completed") or not isinstance(item, dict):
            continue
        if item.get("type") in ("agent_message", "reasoning") and item.get("text"):
            return True
        if item.get("type") in ("command_execution", "mcp_tool_call", "file_change", "web_search", "image_generation"):
            return True
    return False


def describe_attempt(trial: Path, replay: Row, reviewed: Row, supplementary: bool) -> Row:
    record = load(trial / "record.json")
    events = events_at(trial / "stdout.jsonl")
    inits = [event for event in events if event.get("type") == "system" and event.get("subtype") == "init"]
    assistant_models = list(dict.fromkeys(
        message["model"] for event in events
        if event.get("type") == "assistant" and not event.get("isApiErrorMessage")
        and isinstance(message := event.get("message"), dict)
        and isinstance(message.get("model"), str) and message["model"] not in ("", "<synthetic>")
    ))
    codex_usage = [event["usage"] for event in events if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict)]
    claude_results = [event for event in events if event.get("type") == "result"]
    claude_result = claude_results[-1] if claude_results else {}
    inference = bool(assistant_models) or codex_activity(events) or any(positive_usage(usage) for usage in codex_usage) or any(
        positive_usage(event.get("usage")) for event in claude_results
    )
    command = record.get("command", [])
    configuration = {
        "host_and_version": record["host_and_version"],
        "requested_model": record.get("requested_model"),
        "reasoning_effort": option(command, "--effort") or next((value.split("=", 1)[1].strip('"') for value in reversed(command) if value.startswith("model_reasoning_effort=")), None),
        "host_reported_model": record.get("host_reported_model") or next((event.get("model") for event in reversed(inits) if event.get("model")), None),
        "shell_sandbox": record.get("shell_sandbox") or option(command, "--sandbox"),
        "permission_mode": option(command, "--permission-mode"),
        "allowed_tools": option(command, "--allowedTools"), "tools": option(command, "--tools"),
        "packaged_skill_loading": "native_plugin_directory" if "--plugin-dir" in command else "project_skill_discovery",
        "ephemeral": "--ephemeral" in command or "--no-session-persistence" in command,
        "native_journal_requested": record.get("retain_native_session", False),
        "output_protocol": option(command, "--output-format") or ("codex_jsonl" if "--json" in command else None),
    }
    input_images = {name: value for name, value in load(trial / "inputs.json").items() if Path(name).suffix.lower() in IMAGE_SUFFIXES}
    check_bindings(trial / "input-project", input_images)
    completed = record["execution_status"] == "host_completed_ungraded"
    row: Row = {
        "attempt": trial.name, "case_id": record["case_id"], "phase": record.get("phase", "fresh"),
        "supplementary": supplementary, "host": record["host_and_version"], "host_id": record["host"],
        "requested_model": record.get("requested_model"),
        "host_reported_model": configuration["host_reported_model"],
        "observed_model": assistant_models[-1] if assistant_models else None,
        "observed_assistant_models": assistant_models,
        "legacy_recorded_observed_model": record.get("observed_model"),
        "model_identity_limit": "Requested and host-selected models are configuration; assistant message model fields are reported identities, not independent model attestation.",
        "execution_status": record["execution_status"], "inference_observed": inference,
        "completed_host_session": completed, "completed_inference_session": completed and inference,
        "elapsed_seconds": record.get("elapsed_seconds"), "configuration": configuration,
        "native_journal_retained": record.get("native_journal_found", False),
        "artifact_count": len(record["artifacts"]), "record_sha256": replay["record_sha256"],
        "bundle_manifest_sha256": record["bundle_manifest_sha256"],
        "prompt_sha256": sha(trial / "prompt.txt"), "input_image_hashes": input_images,
        "codex_reported_usage": codex_usage[-1] if codex_usage else None,
        "claude_reported_usage": claude_result.get("usage"),
        "claude_assistant_usage_events": [
            {"model": message.get("model"), "usage": message["usage"]}
            for event in events if event.get("type") == "assistant"
            and isinstance(message := event.get("message"), dict) and isinstance(message.get("usage"), dict)
        ],
        "claude_result_metrics": {key: claude_result[key] for key in (
            "modelUsage", "total_cost_usd", "duration_api_ms", "duration_ms", "num_turns", "is_error", "terminal_reason",
        ) if key in claude_result},
        "package_mutated": record.get("package_mutated", False),
        "deterministic_state_replays": len(replay.get("state_replay", [])),
        "state_validation_failures": sum(bool(item.get("returncode")) for item in replay.get("state_replay", [])),
        "state_paths": replay.get("state_paths", []),
        "state_validation_errors": replay.get("state_validation_errors", []),
        "reviewed_host_observations": reviewed.get("host_layer", {}),
        "reviewed_production_observations": reviewed.get("production_layer", {}),
        "native_initialization": [{key: event[key] for key in ("plugins", "skills", "mcp_servers", "tools") if key in event} for event in inits],
        "criterion_verdicts": dict(Counter(item["verdict"] for item in reviewed.get("criteria", []))),
        "supplementary_check_verdicts": dict(Counter(item["verdict"] for item in reviewed.get("checks", []))),
    }
    if not inference and any(
        row[field].get(verdict, 0)
        for field in ("criterion_verdicts", "supplementary_check_verdicts")
        for verdict in ("pass", "fail")
    ):
        raise ValueError(f"behavior verdict lacks observed inference: {trial.name}")
    return row


def compare(left: Row, right: Row) -> Row:
    prompt_equal = left["prompt_sha256"] == right["prompt_sha256"]
    images_equal = left["input_image_hashes"] == right["input_image_hashes"]
    differences = []
    if not prompt_equal:
        differences.append("prompt_bytes_differ")
    if not images_equal:
        differences.append("input_image_bytes_differ")
    if left["host_id"] != right["host_id"]:
        differences.append("host_protocol_differs")
    config_changes = {key: {"left": value, "right": right["configuration"].get(key)}
                      for key, value in left["configuration"].items() if value != right["configuration"].get(key)}
    if any(key in config_changes for key in ("requested_model", "host_reported_model", "reasoning_effort")):
        differences.append("model_configuration_differs")
    if any(key in config_changes for key in ("shell_sandbox", "permission_mode", "allowed_tools", "tools")):
        differences.append("access_configuration_differs")
    if any(key in config_changes for key in ("ephemeral", "native_journal_requested", "packaged_skill_loading", "output_protocol")):
        differences.append("recording_or_loading_protocol_differs")
    unchanged_profile = left["bundle_manifest_sha256"] == right["bundle_manifest_sha256"] and not (left["package_mutated"] or right["package_mutated"])
    if not unchanged_profile:
        differences.append("profile_identity_differs_or_mutated")
    completed = left["completed_inference_session"] and right["completed_inference_session"]
    observed = left["inference_observed"] and right["inference_observed"]
    if not completed:
        differences.append("incomplete_host_turn_pair")
    if not observed:
        differences.append("inference_not_observed_for_both")
    return {
        "case_id": left["case_id"], "left": left["attempt"], "right": right["attempt"],
        "left_host": left["host_id"], "right_host": right["host_id"],
        "prompt_bytes_equal": prompt_equal, "input_image_bytes_equal": images_equal,
        "input_image_counts": {"left": len(left["input_image_hashes"]), "right": len(right["input_image_hashes"])},
        "same_unchanged_profile": unchanged_profile, "both_completed_inference": completed,
        "both_observed_inference": observed,
        "configuration_differences": config_changes, "differences": differences,
        "criterion_verdicts": {"left": left["criterion_verdicts"], "right": right["criterion_verdicts"]},
    }


def build_report(evidence: Path, identity: Row) -> Row:
    review = load(evidence / "criterion-review.json")
    integrity = load(evidence / "integrity.json")
    evidence_errors = integrity.get("evidence_error_count", integrity.get("error_count", 0))
    if evidence_errors or any(row.get("errors") for row in integrity["runs"]):
        raise ValueError("corrupted evidence prevents report compilation")
    original = review["runs"]
    supplementary = review["supplementary_continuations"]
    entries = original + supplementary
    reviewed = {entry["attempt"]: entry for entry in entries}
    replayed = {entry["attempt"]: entry for entry in integrity["runs"]}
    if len(reviewed) != len(entries) or len(replayed) != len(integrity["runs"]):
        raise ValueError("duplicate reviewed or replayed attempt")
    actual = {trial.name for trial in (evidence / "runs").iterdir() if trial.is_dir()}
    if set(reviewed) != set(replayed) or set(reviewed) != actual:
        raise ValueError("attempts remain unreviewed or unreplayed")
    criteria = {case["id"]: case["criteria"] for case in load(evidence / "profile-scenarios.json")["cases"]}
    counts: Counter[str] = Counter()
    supplementary_counts: Counter[str] = Counter()
    for entry in entries:
        items = entry.get("criteria", []) if entry in original else entry.get("checks", [])
        if any(item["verdict"] not in VERDICTS for item in items):
            raise ValueError("unknown review verdict")
        if entry in original:
            if [item["criterion"] for item in items] != criteria[entry["case_id"]]:
                raise ValueError("review omitted or changed an original criterion")
            counts.update(item["verdict"] for item in items)
        else:
            supplementary_counts.update(item["verdict"] for item in items)
        if not {"record.json", "stdout.jsonl", "prompt.txt"}.issubset(entry["reviewed_evidence_hashes"]):
            raise ValueError("review does not bind core trial evidence")
        check_bindings(evidence / "runs" / entry["attempt"], entry["reviewed_evidence_hashes"])
    if dict(counts) != review["summary"]["original_criterion_verdicts"]:
        raise ValueError("criterion totals differ")
    if "supplementary_check_verdicts" in review["summary"] and dict(supplementary_counts) != review["summary"]["supplementary_check_verdicts"]:
        raise ValueError("supplementary totals differ")
    attempts = []
    supplementary_ids = {entry["attempt"] for entry in supplementary}
    for replay in integrity["runs"]:
        trial = evidence / "runs" / replay["attempt"]
        if verify_run(trial) or sha(trial / "record.json") != replay["record_sha256"]:
            raise ValueError("replayed trial changed")
        row = describe_attempt(trial, replay, reviewed[trial.name], trial.name in supplementary_ids)
        if row["bundle_manifest_sha256"] != identity["bundle_manifest_sha256"]:
            raise ValueError("trial package baseline differs")
        if not row["supplementary"] and row["case_id"] != reviewed[trial.name]["case_id"]:
            raise ValueError("review and recorded case differ")
        attempts.append(row)
    by_host = {}
    for host in sorted({"claude", "codex"} | {row["host_id"] for row in attempts}):
        rows = [row for row in attempts if row["host_id"] == host]
        catalog_rows = [row for row in rows if not row["supplementary"]]
        covered = sorted({row["case_id"] for row in catalog_rows if row["completed_inference_session"]})
        host_counts: Counter[str] = Counter()
        for row in catalog_rows:
            host_counts.update(row["criterion_verdicts"])
        by_host[host] = {
            "attempts": len(rows), "completed_host_sessions": sum(row["completed_host_session"] for row in rows),
            "sessions_with_observed_inference": sum(row["inference_observed"] for row in rows),
            "completed_inference_sessions": sum(row["completed_inference_session"] for row in rows),
            "execution_status_counts": dict(Counter(row["execution_status"] for row in rows)),
            "catalog_cases_attempted": sorted({row["case_id"] for row in catalog_rows}),
            "catalog_cases_with_observed_inference": sorted({row["case_id"] for row in catalog_rows if row["inference_observed"]}),
            "catalog_cases_with_completed_inference": covered,
            "catalog_cases_without_completed_inference": sorted(set(criteria) - set(covered)),
            "original_criterion_verdicts": dict(host_counts),
        }
    pairs = [compare(left, right) for left, right in combinations(attempts, 2)
             if not left["supplementary"] and not right["supplementary"] and left["case_id"] == right["case_id"]]
    cross = [pair for pair in pairs if pair["left_host"] != pair["right_host"]]
    repeats = [pair for pair in pairs if pair["left_host"] == pair["right_host"]]
    hosts_completed = [host for host, row in by_host.items() if row["completed_inference_sessions"]]
    status = ("reviewed_cross_host_behavior_partial_coverage" if {"claude", "codex"}.issubset(hosts_completed)
              else "reviewed_behavior_partial_host_coverage" if hosts_completed else "reviewed_host_attempts_no_completed_inference")
    covered_any = set().union(*(set(row["catalog_cases_with_completed_inference"]) for row in by_host.values()))
    observed_any = set().union(*(set(row["catalog_cases_with_observed_inference"]) for row in by_host.values()))
    report = {
        "version": 2, "observed_at": datetime.now(UTC).isoformat(), "status": status,
        **{key: identity[key] for key in ("source_revision", "source_tree_dirty", "bundle_manifest_sha256", "profile_hash", "skill_hashes", "runtime_hashes")},
        "coverage": {"attempts_reviewed": len(attempts), "original_case_attempts_reviewed": len(original),
                     "supplementary_cold_continuations": len(supplementary), "catalog_case_count": len(criteria),
                     "original_criterion_verdicts": dict(counts), "supplementary_check_verdicts": dict(supplementary_counts),
                     "by_host": by_host, "catalog_cases_without_completed_inference": sorted(set(criteria) - covered_any),
                     "catalog_cases_with_observed_inference": sorted(observed_any),
                     "catalog_cases_without_observed_inference": sorted(set(criteria) - observed_any)},
        "attempts": attempts,
        "evidence_validation": {"evidence_error_count": evidence_errors,
                                "state_validation_error_count": integrity.get("state_validation_error_count", 0)},
        "comparisons": {"cross_host_pairs": cross, "same_host_repeat_pairs": repeats,
                        "catalog_cases_with_matched_observed_inference": sorted({pair["case_id"] for pair in cross if pair["both_observed_inference"] and pair["prompt_bytes_equal"] and pair["input_image_bytes_equal"] and pair["same_unchanged_profile"]}),
                        "catalog_cases_with_matched_completed_inference": sorted({pair["case_id"] for pair in cross if pair["both_completed_inference"] and pair["prompt_bytes_equal"] and pair["input_image_bytes_equal"] and pair["same_unchanged_profile"]}),
                        "visual_repeat_pairs": [pair for pair in repeats if pair["case_id"] == "mechanical-pass-visual-rejection"],
                        "interpretation": "Exact prompt and image matches do not equal identical host context, model configuration or tool access; inspect every pair's differences."},
        "separate_outcome_layers": {
            "host_discovery": {host: [{"attempt": row["attempt"], "native_initialization": row["native_initialization"], "reviewed_observations": row["reviewed_host_observations"]} for row in attempts if row["host_id"] == host] for host in by_host},
            "profile_behavior": by_host,
            "controlled_artifact_outcomes": [{"attempt": row["attempt"], "reviewed_observations": row["reviewed_production_observations"], "state_validation_failures": row["state_validation_failures"]} for row in attempts],
            "production_outcomes": {"live_pixellab": "not_exercised", "new_production_art": "not_created", "engine_acceptance": "not_exercised", "animation_or_tile_continuity": "not_exercised"},
        },
        "next_tasks": "evaluations/TODO.spec.md",
        "limitations": review.get("global_limitations", []) + [
            "Separate temporary projects are not an OS sandbox; each launch retains its access configuration.",
            "No profile-disabled control arm; these observations do not measure causal improvement from PIXL.",
            "These bounded trials and repeats do not establish general reliability or a host/model ranking.",
            "Codex and Claude usage fields retain their native accounting; token, latency and cost values are not normalized performance comparisons.",
            "Selected model metadata, observed assistant model labels and observed inference are separate claims.",
            "The original runtime suite and POC receipts were preserved, not rerun by this evaluation.",
        ],
        "evidence_hashes": {name: sha(evidence / name) for name in (
            "identity.json", "profile-scenarios.json", "fixture-oracle.json", "criterion-review.json", "integrity.json",
            "recorder-review.json", "harness-tests.txt", "quality-checks.txt", "claude-auth-recheck.json", "claude-auth-restored.json",
        ) if (evidence / name).is_file()},
    }
    return report


def main() -> None:
    report = build_report(EVIDENCE, freeze())
    report["tooling_hashes"] = {name: sha(REPO / name) for name in (
        "evaluations/host_trials.py", "evaluations/check_host_evidence.py", "evaluations/write_host_report.py",
        "tests/test_host_evidence.py", "tests/test_host_report.py",
    )}
    write_json(EVIDENCE / "report.json", report)
    print(json.dumps({"attempts": len(report["attempts"]), "original_criteria": report["coverage"]["original_criterion_verdicts"], "status": report["status"]}))


if __name__ == "__main__":
    main()
