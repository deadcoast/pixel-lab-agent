"""Caller's independent check of the specialist's saved result.

Re-derives every structural claim from the exact exports and state bytes
(coverage, hashes, literal text, r4 identity, verdict records, quotes) and
records the caller's conclusions and corrections. Writes
work/choice-comparison/caller/specialist-check-and-corrections.json.
No state change, no provider action.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "work" / "choice-comparison"
OUT = WORK / "caller" / "specialist-check-and-corrections.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    spec = load("work/choice-comparison/specialist/SPECIALIST-RESULT.json")
    mapping = load("work/choice-comparison/specialist/criterion-mapping.json")
    semantic = load("work/choice-comparison/specialist/semantic-review.json")
    changes = load("work/choice-comparison/02-request-review-changes.json")
    before = load("work/choice-comparison/03-request-review-full-before-authoring-01.json")
    after = load("work/choice-comparison/04-request-review-full-after-provenance-correction.json")
    diff7 = load("work/choice-comparison/07-criterion-literal-diff.json")
    indep = load("work/choice-comparison/caller/independent-comparison.json")
    r4 = load("work/focused-successor/specialist-proposal-r4.json")

    # 1. Specialist artifact hashes match its own self-report.
    artifact_hashes = {}
    for a in spec["artifacts"]:
        actual = sha(ROOT / a["path"])
        artifact_hashes[a["path"]] = {"claimed": a["sha256"], "actual": actual, "match": actual == a["sha256"]}

    # 2. Coverage of all 20 old / 23 new IDs and hashes against the compact index.
    bi = {x["id"]: x["record_sha256"] for x in changes["criterion_index"]["before"]}
    ai = {x["id"]: x["record_sha256"] for x in changes["criterion_index"]["after"]}
    fb = {c["id"]: c for c in before["criteria"]}
    fa = {c["id"]: c for c in after["criteria"]}
    old_seen, new_seen, text_mismatch, identical_disagree = {}, {}, [], []
    mine7 = {r["key"]: r for r in diff7["criteria"]}
    for p in mapping["pairs"]:
        o = p["old"]
        old_seen[o["id"]] = o["record_sha256"]
        if o["check"] != fb[o["id"]]["check"]:
            text_mismatch.append(o["id"])
        for n in p["new"] + (p.get("split_diagnostics") or []):
            new_seen[n["id"]] = n["record_sha256"]
            if n["check"] != fa[n["id"]]["check"]:
                text_mismatch.append(n["id"])
        if mine7[p["key"]].get("check_text_identical") != p["check_text_identical"]:
            identical_disagree.append(p["key"])
    coverage = {
        "old_ids_complete": set(old_seen) == set(bi), "old_hashes_match": all(old_seen[k] == bi[k] for k in old_seen if k in bi),
        "new_ids_complete": set(new_seen) == set(ai), "new_hashes_match": all(new_seen[k] == ai[k] for k in new_seen if k in ai),
        "old_count": len(old_seen), "new_count": len(new_seen),
        "check_text_matches_full_reports": not text_mismatch, "text_mismatches": text_mismatch,
        "check_text_identical_flags_agree_with_07": not identical_disagree, "disagreements": identical_disagree,
        "specialist_index_copy_equals_compact_index": {x["id"]: x["record_sha256"] for x in mapping["criterion_index"]["before"]} == bi and {x["id"]: x["record_sha256"] for x in mapping["criterion_index"]["after"]} == ai,
    }

    # 3. r4 identity claim: current 23 checks equal r4 successor_checks except one cross-reference ID.
    cur = {c["id"].replace("provenance-correction.", ""): c["check"] for c in after["criteria"]}
    r4c = {}
    for e in r4["criteria"]:
        for sc in e.get("successor_checks") or []:
            sid = (sc.get("id") or sc.get("successor_id"))
            for pref in ("successor-adoption-02.", "successor-adoption.", "focused-successor."):
                sid = sid.replace(pref, "")
            r4c[sid] = sc.get("check")
    r4_diff = {}
    for k, v in cur.items():
        if k not in r4c:
            r4_diff[k] = "absent in r4"
        elif r4c[k] != v:
            ops = [(op, r4c[k][i1:i2], v[j1:j2]) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, r4c[k], v).get_opcodes() if op != "equal"]
            r4_diff[k] = ops
    r4_check = {"r4_successor_check_count": len(r4c), "identical": len(cur) - len(r4_diff), "differences": r4_diff,
                "claim_verified": set(r4_diff) == {"working.q.activity-not-success"} and all(a == "authoring" and b == "provenance" or a == "01" and b == "correction" for _, a, b in r4_diff.get("working.q.activity-not-success", []))}

    # 4. Verdict records in state bytes.
    state = (ROOT / ".pixl/assets/queue.ready/state.px").read_text(encoding="utf-8")
    def vrec(vid: str) -> dict | None:
        m = re.search(r"@" + re.escape(vid) + r":V\{([^}]*)\}", state)
        if not m:
            return None
        body = m.group(1)
        return {
            "at": re.search(r"at=~\d+:([^;]+)", body).group(1) if re.search(r"at=~\d+:([^;]+)", body) else None,
            "st": re.search(r"st=([a-z]+)", body).group(1),
            "rq": re.search(r"rq=@([^;]+)", body).group(1),
            "obsolete_flag": "ob=+" in body,
            "wy_prefix": (re.search(r"wy=~\d+:(.{0,120})", body).group(1) if re.search(r"wy=~\d+:(.{0,120})", body) else None),
        }
    verdicts = {vid: vrec(vid) for vid in [
        "provenance.working.motion.unavailable", "native-review.working.motion.verdict.0",
        "provenance.working.review.verdict.0", "provenance.working.review.verdict.1", "provenance.working.review.verdict.2",
        "provenance.working.review.verdict.3", "provenance.working.review.verdict.4", "provenance.working.review.verdict.5",
        "provenance.working.engine.verdict",
    ]}
    verdict_checks = {
        "unavailable_retained_and_obsolete": verdicts["provenance.working.motion.unavailable"] is not None and verdicts["provenance.working.motion.unavailable"]["st"] == "unavailable" and verdicts["provenance.working.motion.unavailable"]["obsolete_flag"],
        "superseding_pass_is_native_review_id": verdicts["native-review.working.motion.verdict.0"] is not None and verdicts["native-review.working.motion.verdict.0"]["st"] == "pass" and verdicts["native-review.working.motion.verdict.0"]["rq"] == "provenance-correction.working.q.motion-continuity",
        "review_verdicts_1_and_2_state_retained_observation": all(verdicts[v] and verdicts[v]["wy_prefix"].startswith("Fresh corrected-scope verdict based on explicitly retained unchanged observation, not new viewing") for v in ("provenance.working.review.verdict.1", "provenance.working.review.verdict.2")),
        "records": verdicts,
    }

    # 5. Quote exactness in semantic-review themes.
    allb = " ".join(c["check"] for c in before["criteria"])
    alla = " ".join(c["check"] for c in after["criteria"])
    def flat(q):
        if isinstance(q, str):
            return [q]
        if isinstance(q, dict):
            return sum((flat(v) for v in q.values()), [])
        if isinstance(q, list):
            return sum((flat(v) for v in q), [])
        return []
    quote_checks = []
    for t in semantic["themes"]:
        for side, corpus in (("before_quote", allb), ("after_quote", alla)):
            for q in flat(t[side]):
                exact = q in corpus
                elided = (not exact) and q.startswith("... ") and q[4:] in corpus
                quote_checks.append({"theme": t["id"], "side": side, "exact": exact, "elided_exact_tail": elided, "labelled_note": (not exact and not elided and len(q) < 80), "text_head": q[:70]})
    quote_summary = {"total": len(quote_checks), "exact": sum(1 for q in quote_checks if q["exact"]), "elided_exact_tail": sum(1 for q in quote_checks if q["elided_exact_tail"]), "labelled_notes": [q for q in quote_checks if q["labelled_note"]], "unexplained": [q for q in quote_checks if not (q["exact"] or q["elided_exact_tail"] or q["labelled_note"])]}

    # 6. Measured claims: caller re-ran pixl_asset_check (alpha full) on the four PNGs; values transcribed from those tool results.
    measured = {
        "renderer-successor/assets/working.png": {"caller_asset_check": {"width": 64, "height": 16, "visible_pixels": 128, "visible_colors": 9, "fractional_alpha_pixels": 0, "opaque_components": 12, "visible_bbox": [3, 2, 62, 14], "sha256": "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc"}, "specialist_claim": "64x16, 128 visible px, 12 components, 0 fractional alpha", "match": True},
        "renderer-successor/assets/error-retry.png": {"caller_asset_check": {"visible_pixels": 54, "visible_colors": 31, "opaque_components": 1, "fractional_alpha_pixels": 0}, "specialist_claim": "54 px, 31 colours, 1 component", "match": True},
        "renderer-successor/assets/paused.png": {"caller_asset_check": {"visible_pixels": 60, "visible_colors": 20, "opaque_components": 2, "fractional_alpha_pixels": 0}, "specialist_claim": "60 px, 20 colours, 2 components", "match": True},
        "renderer-successor/assets/ready-confirmed.png": {"caller_asset_check": {"visible_pixels": 29, "visible_colors": 1, "opaque_components": 1}, "specialist_claim": "29 px, 1 colour; (112,185,237) = #70b9ed = start.svg fill", "match": True, "start_svg_fill_checked": "#70b9ed" in (ROOT / "renderer-successor/assets/start.svg").read_text(encoding="utf-8")},
        "note": "Counts are measurements (4-connectivity, nonzero alpha). They verify the specialist's numbers; they are not acceptance thresholds. 'Selective AA' in Retry shows as 31 colours with zero fractional alpha: anti-aliasing here is colour blending against the expected panel, not partial transparency.",
    }

    # 7. Judgment comparison: specialist vocabulary vs caller classes.
    judgments = []
    mine = {r["key"]: r for r in indep["criteria"]}
    for p in mapping["pairs"]:
        judgments.append({"key": p["key"], "specialist": p["obligation_judgment"], "caller": mine[p["key"]]["obligation_change"]})

    conclusions = [
        "Coverage verified independently: every one of the 20 original and 23 successor criterion IDs and record hashes appears in the specialist mapping and matches the compact index and both full reports; every quoted check text is byte-equal to the full reports.",
        "The specialist's identity is retained as reported and as invoked: Claude Code Agent tool, subagent_type 'pixl' (the named role in agents.json), model inherited (claude-fable-5-1), pixl:pixl skill loaded. This is a named native PIXL role, not a generic child. The caller cannot verify the child's internal skill load beyond its report and its file contents, which follow the kit's request-review structure.",
        "Interpretations agree with the caller's independent reading written before opening the specialist files. Vocabulary differs: the specialist's 'narrowed' means the owner-attributed rejection surface shrank (more permissive), where the caller wrote 'outcome unchanged / expert recipe demoted'. The substance is the same for every pair. No pair is judged equivalent on the basis of ID alignment; both sides treat alignment as structural.",
        "Theme authority is named in both reviews: BRIEF.md lines 3/7/9 as the only owner source; src/queue-view-successor.ts and renderer-successor/view.mjs as consumer/fixture authority; the PLAR queue.working caller update for the stationary reduced-motion requirement; SUCCESSOR-ADOPTION.md and FOCUSED-SUCCESSOR.md as assignment scope; caller-comparison-final D1-D4 as prior review history; PIXL expert judgment for pacing, selective AA and blur exclusion. The specialist additionally cites PROFILE.md transparency guidance for 'deliberate backing permitted'; the caller grounds the same reading in choice.ready's 'no backing plate' being a specialist sample choice.",
        "Verdict distinction verified in state bytes: provenance.working.motion.unavailable (unavailable, ob=+, 11:29:46) is retained; the current pass on motion-continuity is native-review.working.motion.verdict.0 (16:16:09). The six provenance.working.review.verdict.0-5 passes at 11:29:40 declare themselves re-scoped reuse of retained observation, not new viewing; the later native-review family views are the actual exterior viewings. Added diagnostics erased nothing.",
        "The specialist's r4-identity finding is verified: 22 of 23 current checks are byte-identical to the r4 proposal's successor checks; the remaining one differs only in a cross-reference ID. Its four image measurements were re-measured by the caller with pixl_asset_check and match.",
        "Current acceptance (Working, Retry, Paused, family) pre-exists at revision 126 and was neither created nor re-earned here. The state hash is unchanged.",
    ]
    corrections = [
        {"id": "C1", "target": "caller delegation brief", "error": "Described the current superseding motion pass as 'provenance.working.review.verdict.*'.", "correction": "The superseding pass is native-review.working.motion.verdict.0 (supersedes provenance.working.motion.unavailable). provenance.working.review.verdict.0-5 cover geometry, alpha diagnostic, transparent-exterior, frame-assembly, activity-not-success and style-coherence; consumers is provenance.working.engine.verdict. The caller's independent comparison already used the correct ID; this entry retains the brief's error and its correction.", "raised_by": "specialist", "accepted": True},
        {"id": "C2", "target": "caller wording of the Working visual transparency pass", "error": "Risk of describing provenance.working.review.verdict.2 as a fresh 11:29 viewing.", "correction": "State bytes say it rests on explicitly retained unchanged observation. Describe it as a re-scoped reuse of earlier viewing; cite the native-review family views as the actual exterior viewings.", "raised_by": "specialist", "accepted": True},
        {"id": "C3", "target": "specialist semantic-review.json theme quotes", "error": None, "observation": "Two quote slots are not verbatim substrings: theme b after 'retry and paused' is a labelled note ('identical to before'), and theme c before 'consumers (timing clause)' is an elided quote whose tail is exact. Neither misquotes a criterion; retained as a note, no correction needed.", "raised_by": "caller", "accepted": "n/a"},
        {"id": "C4", "target": "specialist obligation_counts", "error": None, "observation": "Counts (unchanged 8, clarified 8, re-scoped 10, narrowed 7, widened 5) sum over multi-label pairs and must not be read as 20 single classifications. The caller's class per pair is retained separately.", "raised_by": "caller", "accepted": "n/a"},
        {"id": "C5", "target": "caller tooling", "error": "First extract_literal_diff.py run mis-sliced stage/local keys (file sha256 a5c87df7f56a8611c8038369c8a259f70adcb6a991b347b0e399df6b8985229e, overwritten by the corrected 53563ead...).", "correction": "Pairing was unaffected (equal offset both sides); corrected file retained and used by the specialist. Recorded for transparency.", "raised_by": "caller", "accepted": True},
    ]

    result = {
        "version": 1,
        "kind": "caller_specialist_check_and_corrections",
        "reviewer_role": "independent native caller (parent Claude Code session, claude-fable-5-1)",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "delivered: specialist review verified against exact exports; two caller-side corrections accepted; no interpretation error found in the current 23 criteria; no state change",
        "specialist_files": artifact_hashes,
        "specialist_result_sha256": sha(ROOT / "work/choice-comparison/specialist/SPECIALIST-RESULT.json"),
        "specialist_identity_as_reported": spec["identity"],
        "specialist_identity_as_invoked": "Claude Code Agent tool, subagent_type 'pixl' from agents.json ('PIXL visual asset specialist for source-authority comparison'), run_in_background true, completion notification received; model inherited",
        "coverage": coverage,
        "r4_identity_claim": r4_check,
        "verdict_records": verdict_checks,
        "quotes": quote_summary,
        "measured_claims": measured,
        "judgment_comparison": judgments,
        "conclusions": conclusions,
        "corrections": corrections,
        "continuation": "No state operation is required. The successor is complete at revision 126; nothing here changes that. If a future proposal is authored, narrow the whole-file source ranges on provenance.source.proposal/comparison and use per-clause source lists; do not edit retained records. The earlier interrupted Claude comparison remains unresolved by this trial.",
    }
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"path": str(OUT.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(OUT), "coverage": coverage, "r4_claim_verified": r4_check["claim_verified"], "verdicts": {k: v for k, v in verdict_checks.items() if k != "records"}, "quotes": {k: v for k, v in quote_summary.items() if k != "labelled_notes"}, "artifact_hashes_match": all(a["match"] for a in artifact_hashes.values())}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
