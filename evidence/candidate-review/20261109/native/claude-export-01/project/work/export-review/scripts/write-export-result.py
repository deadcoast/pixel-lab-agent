"""Assemble work/export-review/EXPORT-RESULT.json from retained summaries and the
verification output. Hashes are recomputed from files, never typed by hand.

Usage: python -I write-export-result.py <project-root>
"""
import datetime as dt
import hashlib
import json
import os
import sys

ROOT = os.path.abspath(sys.argv[1])
OUT_REL = "work/export-review/EXPORT-RESULT.json"


def rel(p):
    return os.path.join(ROOT, p.replace("/", os.sep))


def read(p):
    with open(rel(p), "rb") as fh:
        return fh.read()


def ident(p):
    data = read(p)
    return {"path": p, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def load(p):
    return json.loads(read(p).decode("utf-8"))


verification = load("work/export-review/06-verification.json")
assert verification["all_checks_passed"] is True, verification["failed_checks"]
s01 = load("work/export-review/01-family-review-context.mcp-summary.json")
s02 = load("work/export-review/02-family-report.mcp-summary.json")
s03 = load("work/export-review/03-identical-review-cli-stdout.json")
s04 = load("work/export-review/04-family-review-context-cli-stdout.json")
s05 = load("work/export-review/05-family-report-cli-stdout.json")
exports = {e["result_path"]: e for e in verification["exports"]}


def export_entry(summary, summary_rel, extra=None):
    v = exports[summary["result_path"]]
    entry = {
        "result_saved": summary["result_saved"],
        "result": ident(summary["result_path"]),
        "returned_summary": summary,
        "summary_retained_as": ident(summary_rel),
        "verified": {
            "sha256_matches_summary": v["sha256_matches"],
            "bytes_match_summary": v["bytes_match"],
            "parses_as_utf8_json": v["parses_as_utf8_json"],
        },
    }
    if extra:
        entry.update(extra)
    return entry


state_hash = "23718b6d027836af49f3548fcb38979bd4afca032e8113d7a9222c7c570c8c49"
mcp_server = ("python.exe .agents/skills/export-kit/scripts/pixl.py mcp --root <project> "
              "(stdio server 'pixl-local' launched by the host from claude-export-01/mcp.json; "
              "confirmed from the live process command line)")
cli = "C:/github/pixel-lab-agent/.venv/Scripts/python.exe -I .agents/skills/export-kit/scripts/pixl.py"

result = {
    "trial": "candidate-review/20261109/native/claude-export-01",
    "assignment": "EXPORT-ASSIGNMENT.md",
    "written_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
    "caller": "Claude Code main session (claude-fable-5-1) acting as the native caller; no specialist delegation was used for this serialization/retry check.",
    "kit": {
        "current": ".agents/skills/export-kit",
        "bundle_manifest": ident(".agents/skills/export-kit/bundle-manifest.json"),
        "spec_read": ident(".agents/skills/export-kit/resources/spec/candidate-review.md"),
        "preserved_unused": [".agents/skills/pixl-kit", ".agents/skills/review-kit"],
        "mcp_server": mcp_server,
        "cli": cli,
        "python": verification["python"],
    },
    "scope": "Bounded verification of result_path/--result-path exports and one identical-review retry on the completed review. Not an art review, generation job, named-role selection or new rendering.",
    "calls": [
        {
            "step": 1,
            "interface": "mcp",
            "tool": "pixl_review_context",
            "arguments": {"path": ".pixl/assets/queue.ready/state.px", "candidate_id": "native-review.family.candidate",
                          "result_path": "work/export-review/01-family-review-context.json"},
            **export_entry(s01, "work/export-review/01-family-review-context.mcp-summary.json"),
            "note": "Summary file is the verbatim compact tool response; the result file was written by the kit.",
        },
        {
            "step": 1,
            "interface": "cli",
            "command": f"{cli} review-context .pixl/assets/queue.ready/state.px native-review.family.candidate --root . --result-path work/export-review/04-family-review-context-cli.json",
            "exit": read("work/export-review/04-family-review-context-cli-exit.txt").decode().strip(),
            **export_entry(s04, "work/export-review/04-family-review-context-cli-stdout.json",
                           {"byte_identical_to_mcp_export": next(c for c in verification["checks"] if c["check"].startswith("MCP and CLI review-context"))["ok"]}),
        },
        {
            "step": 2,
            "interface": "mcp",
            "tool": "pixl_family",
            "arguments": {"path": ".pixl/assets/queue.ready/state.px", "output": "provenance-correction.delivery.output",
                          "result_path": "work/export-review/02-family-report.json"},
            **export_entry(s02, "work/export-review/02-family-report.mcp-summary.json"),
        },
        {
            "step": 2,
            "interface": "cli",
            "command": f"{cli} family .pixl/assets/queue.ready/state.px provenance-correction.delivery.output --root . --result-path work/export-review/05-family-report-cli.json",
            "exit": read("work/export-review/05-family-report-cli-exit.txt").decode().strip(),
            **export_entry(s05, "work/export-review/05-family-report-cli-stdout.json",
                           {"byte_identical_to_mcp_export": next(c for c in verification["checks"] if c["check"].startswith("MCP and CLI family"))["ok"]}),
        },
        {
            "step": 3,
            "interface": "cli",
            "tool": "candidate-review",
            "command": f"{cli} candidate-review .pixl/assets/queue.ready native-review.family.candidate native-review.family.collective work/export-review/identical-review.json --expect {state_hash} --root . --result-path work/export-review/03-identical-review-result.json",
            "exit": read("work/export-review/03-identical-review-cli-exit.txt").decode().strip(),
            "stderr": ident("work/export-review/03-identical-review-cli-stderr.txt"),
            "request_file_passed_unchanged": verification["identical_request"],
            **export_entry(s03, "work/export-review/03-identical-review-cli-stdout.json"),
            "note": "The saved request file was passed by path so the exact bytes were replayed; the CLI was chosen over the MCP tool because the MCP form would have required re-typing the 23 KB observation object.",
        },
    ],
    "state": {
        "path": ".pixl/assets/queue.ready/state.px",
        "store": ".pixl/assets/queue.ready",
        "expected_state_hash": state_hash,
        "validate_via_export_kit": verification["validate"],
        "state_file": verification["state_file"],
        "store_files_modified_after_assignment": verification["store_files_modified_after_assignment"],
        "history_file_count": verification["history_file_count"],
        "unchanged": verification["validate"]["hash"] == state_hash and verification["validate"]["revision"] == 126,
    },
    "acceptance": {
        "candidate": "native-review.family.candidate",
        "output": "provenance-correction.delivery.output",
        "task": "provenance-correction.delivery.task",
        "from_review_context": {k: verification["review_context"][k] for k in (
            "task_status", "nominated", "current_acceptance", "snapshot_acceptance", "binding_hash", "candidate_file", "criteria")},
        "from_family_report": {k: verification["family"][k] for k in (
            "state", "candidate", "blockers", "snapshot_blockers", "pending_jobs", "requirements", "members")},
        "family_snapshot_creation_status": [
            {k: s.get(k) for k in ("candidate", "sha256", "created_at", "source_state_sha256", "retention_is_acceptance", "stale")}
            for s in verification["family"]["snapshots"]],
        "distinction": "Creation status (snapshot_acceptance.accepted false; retention_is_acceptance false; source state 5c9c5409...) is immutable and describes the manifest at revision 123. Current acceptance (all_required_pass true, task_complete true, nominated true, three pass verdicts) is read from revision 126 and remains complete.",
        "snapshot_blockers_note": "snapshot_blockers reports that the delivery task is done so no new snapshot can be created; this is expected for a completed family and is not a current-acceptance blocker (blockers is empty).",
    },
    "retry": {
        "review_id": "native-review.family.collective",
        "request": verification["identical_request"],
        "result": verification["replay"],
        "reused_review": verification["replay"]["reused_review"],
        "publications": verification["replay"]["publications"],
        "state_hash_after": verification["replay"]["state_hash"],
        "revision_after": verification["replay"]["revision"],
        "review_report": verification["review_report"],
        "equals_prior_cli_replay": next(c for c in verification["checks"] if c["check"].startswith("replay: parsed result equals prior"))["ok"],
        "prior_cli_replay": ident("work/native-review/12-caller-family-replay-result.json"),
        "conclusion": "Identical replay reused the existing review with zero publications; state hash, revision, report SHA, binding hash and the three verdict IDs are unchanged.",
    },
    "historical_files": {
        "creation_receipt_original": {**verification["creation_receipt"],
                                      "status": "Preserved unchanged. Still not valid JSON (unescaped Windows backslashes). It is the specialist's saved copy of the revision-123 family-snapshot receipt; it is not rewritten or relabeled."},
        "creation_receipt_caller_corrected": {**verification["creation_receipt_corrected"],
                                              "status": "Preserved unchanged; parses; carries the revision-123 creation receipt plus the caller note."},
        "creation_receipt_revision_in_history": next(c for c in verification["checks"] if c["check"].startswith("history: creation receipt"))["ok"],
        "current_usable_results": {
            "family_review_context": [ident("work/export-review/01-family-review-context.json"), ident("work/export-review/04-family-review-context-cli.json")],
            "family_report": [ident("work/export-review/02-family-report.json"), ident("work/export-review/05-family-report-cli.json")],
            "identical_review_retry": ident("work/export-review/03-identical-review-result.json"),
        },
        "other_prior_files_verified_unchanged": {p: v for p, v in verification["prior_files"].items()},
    },
    "verification": {
        "script": ident("work/export-review/scripts/verify-exports.py"),
        "output": ident("work/export-review/06-verification.json"),
        "checks": len(verification["checks"]),
        "all_checks_passed": verification["all_checks_passed"],
        "failed_checks": verification["failed_checks"],
        "method": "Native Python 3.14 (-I) re-read every exported file, recomputed SHA-256/byte counts against the returned summaries, parsed as UTF-8 JSON, ran export-kit validate as a subprocess, hashed the retained review report and manifest, and compared the replay to the prior replay result.",
    },
    "errors": [],
    "limits": [
        "This verifies export serialization and one idempotent retry of a historical review through the current kit; it does not establish art quality, named-role selection or new rendering.",
        "The MCP result-path summaries were copied verbatim from the tool responses into *.mcp-summary.json files; the CLI summaries are captured stdout. All full JSON results were written by the kit, not transcribed.",
        "This consumer copy is untracked by git, so 'unchanged' for prior files rests on hashes observed at the start of this trial and on store mtimes, not version control.",
    ],
    "files_written_this_trial": sorted(
        os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
        for dp, _d, fs in os.walk(rel("work/export-review")) for f in fs
        if os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/") not in ("work/export-review/identical-review.json", OUT_REL)
    ),
}

with open(rel(OUT_REL), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(result, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print(json.dumps(ident(OUT_REL)))
