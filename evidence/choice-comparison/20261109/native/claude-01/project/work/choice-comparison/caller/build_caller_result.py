"""Assemble work/choice-comparison/CALLER-RESULT.json from retained files.

Reads exports, the specialist's saved result, the caller's independent
comparison and the caller follow-up. Computes every hash from bytes; never
transcribes tool output. No state change, no provider action.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "work" / "choice-comparison"
OUT = WORK / "CALLER-RESULT.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locator(rel: str) -> dict:
    p = ROOT / rel
    if not p.exists():
        return {"path": rel, "missing": True}
    return {"path": rel, "sha256": sha(p), "bytes": p.stat().st_size}


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    ctx = load("work/choice-comparison/01-context-authoring.json")
    changes = load("work/choice-comparison/02-request-review-changes.json")
    indep = load("work/choice-comparison/caller/independent-comparison.json")
    followup_rel = "work/choice-comparison/caller/specialist-check-and-corrections.json"
    followup = load(followup_rel) if (ROOT / followup_rel).exists() else None
    spec_rel = "work/choice-comparison/specialist/SPECIALIST-RESULT.json"
    spec = load(spec_rel) if (ROOT / spec_rel).exists() else None

    exports = {
        "01_context_authoring": locator("work/choice-comparison/01-context-authoring.json"),
        "02_request_review_changes": locator("work/choice-comparison/02-request-review-changes.json"),
        "03_full_report_before_authoring_01": locator("work/choice-comparison/03-request-review-full-before-authoring-01.json"),
        "04_full_report_after_provenance_correction": locator("work/choice-comparison/04-request-review-full-after-provenance-correction.json"),
        "05_other_intake_focused_successor_choice_destination": locator("work/choice-comparison/05-other-intake-focused-successor.choice.destination.json"),
        "06_other_intake_choice_ready": locator("work/choice-comparison/06-other-intake-choice.ready.json"),
        "07_criterion_literal_diff": locator("work/choice-comparison/07-criterion-literal-diff.json"),
        "08_review_context_working": locator("work/choice-comparison/08-review-context-working-candidate.json"),
        "09_review_context_family": locator("work/choice-comparison/09-review-context-family-candidate.json"),
        "10_review_context_retry": locator("work/choice-comparison/10-review-context-retry-candidate.json"),
        "11_review_context_paused": locator("work/choice-comparison/11-review-context-paused-candidate.json"),
    }
    for key, loc in exports.items():
        if loc.get("missing"):
            raise SystemExit(f"missing export {key}")

    result = {
        "version": 1,
        "assignment": "CHOICE-COMPARISON.md",
        "trial": "focused-choice/successor-comparison, native claude-01",
        "written_at": datetime.now(timezone.utc).isoformat(),
        "status": followup["status"] if followup else "partial: specialist/follow-up pending",
        "kit": ".agents/skills/export-kit",
        "state": {"path": ".pixl/assets/queue.ready/state.px", "sha256": ctx["hash"], "revision": ctx["revision"], "recomputed_sha256": sha(ROOT / ".pixl/assets/queue.ready/state.px"), "unchanged_by_this_trial": sha(ROOT / ".pixl/assets/queue.ready/state.px") == ctx["hash"]},
        "exports": exports,
        "tool_calls": [
            {"tool": "pixl_context", "arguments": {"path": ".pixl/assets/queue.ready/state.px", "focus": "provenance-correction.plan", "view": "authoring"}, "result": "01"},
            {"tool": "pixl_request_review", "arguments": {"packet": ".pixl/assets/queue.ready/state.px", "plan": "provenance-correction.plan", "against_plan": "authoring-01.plan", "view": "changes"}, "result": "02"},
            {"tool": "pixl_request_review", "arguments": changes["before"]["retrieve"]["arguments"], "result": "03", "followed_from": "02.before.retrieve"},
            {"tool": "pixl_request_review", "arguments": changes["after"]["retrieve"]["arguments"], "result": "04", "followed_from": "02.after.retrieve"},
            {"tool": "pixl_context", "arguments": ctx["choice_scope"]["other_intake"][1]["retrieve"]["arguments"], "result": "05", "followed_from": "01.choice_scope.other_intake"},
            {"tool": "pixl_context", "arguments": ctx["choice_scope"]["other_intake"][0]["retrieve"]["arguments"], "result": "06", "followed_from": "01.choice_scope.other_intake"},
            {"tool": "pixl_review_context", "candidates": ["provenance-correction.working.candidate", "native-review.family.candidate", "provenance-correction.retry.candidate", "provenance-correction.paused.candidate"], "results": ["08", "09", "10", "11"]},
        ],
        "plans": {
            "before": changes["before"]["plan"] | {"review_scope_sha256": changes["before"]["review_scope_sha256"]},
            "after": changes["after"]["plan"] | {"review_scope_sha256": changes["after"]["review_scope_sha256"]},
            "comparison_sha256": changes["comparison_sha256"],
            "counts": changes["counts"],
            "not_asserted": "Direct succession or semantic equivalence; the compact view is orientation only. Intermediate plans successor-adoption.plan and successor-adoption-02.plan exist between these two.",
        },
        "choices": {
            "selected_linked": indep["choices"]["selected_linked"],
            "other_intake_unlinked": [{"id": c["id"], "key": c["key"], "status": c["status"]} for c in ctx["choice_scope"]["other_intake"]],
            "followed_retrievals": ["05", "06"],
            "identical_closure_note": indep["choices"]["other_intake_retrievals"]["note"],
            "why_unlinked_is_not_irrelevant": indep["choices"]["why_unlinked_is_not_irrelevant"],
        },
        "specialist": {
            "delegation": "Claude Code Agent tool, subagent_type 'pixl' (named role from the evaluation agents.json: 'PIXL visual asset specialist for source-authority comparison'); model inherited (claude-fable-5-1); run in background while the caller wrote its independent comparison; no SendMessage follow-up needed unless noted in follow-up file",
            "self_reported_identity": spec.get("identity") if spec else None,
            "status": spec.get("status") if spec else None,
            "result": locator(spec_rel),
            "mapping": locator("work/choice-comparison/specialist/criterion-mapping.json"),
            "semantic_review": locator("work/choice-comparison/specialist/semantic-review.json"),
        },
        "caller": {
            "independent_comparison": locator("work/choice-comparison/caller/independent-comparison.json"),
            "independent_comparison_written_before_opening_specialist_output": indep["written_before_opening_specialist_output"],
            "specialist_check_and_corrections": locator(followup_rel),
            "criterion_accounting": indep["criterion_accounting"],
            "conclusions": followup["conclusions"] if followup else None,
            "errors_or_corrections": followup["corrections"] if followup else None,
            "verdict_distinction": indep["verdict_distinction"]["reading"],
        },
        "scripts": {
            "extract_literal_diff": locator("work/choice-comparison/extract_literal_diff.py"),
            "build_independent_comparison": locator("work/choice-comparison/caller/build_independent_comparison.py"),
            "build_caller_result": locator("work/choice-comparison/caller/build_caller_result.py"),
        },
        "preservation": {
            "state_unchanged": sha(ROOT / ".pixl/assets/queue.ready/state.px") == ctx["hash"],
            "no_mutation_tools_called": True,
            "no_global_settings_or_memory_writes": True,
            "new_files_only_under": "work/choice-comparison/",
        },
        "limits": [
            "Read-only comparison of literal criteria and sources; no new acceptance, verdict, provider action or art generation.",
            "Saved completed acceptance (Working, Retry, Paused, family) pre-exists this trial and is not newly earned by reading it.",
            "The earlier interrupted Claude comparison is not resolved; broad artistic or host reliability is not established.",
        ],
        "continuation": followup["continuation"] if followup else "Open the specialist's three files, check them against exports 02/03/04/07 and the independent comparison, write caller/specialist-check-and-corrections.json, rerun this builder.",
    }
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"path": str(OUT.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(OUT), "status": result["status"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
