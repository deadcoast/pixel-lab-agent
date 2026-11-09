"""Caller independent verification of the specialist's everyday-guide artifacts.

Run from the consumer root with the selected Python (-I). Writes
work/everyday-guide/caller/verification.json and prints a compact summary.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.abspath(sys.argv[1])
SPEC = "work/everyday-guide/specialist"
CALLER = "work/everyday-guide/caller"
EXPECTED_STATE = "23718b6d027836af49f3548fcb38979bd4afca032e8113d7a9222c7c570c8c49"
EXPECTED_REVIEW = "59faea6482a769cc452444f1d94a5b85ff356ec7d0c558778738127861b81294"
EXPECTED_BINDING = "48752d9d65836801fde700b5f125e424cae21ee15c536628b5abde38740db443"
EXPECTED_MANIFEST = "ec59b8245619463446cb86b639e7b387e748917fb5c520a085984b85c89df5d0"


def p(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def sha(rel):
    h = hashlib.sha256()
    with open(p(rel), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest(), os.path.getsize(p(rel))


def load(rel):
    with open(p(rel), "rb") as f:
        return json.loads(f.read().decode("utf-8"))


checks = []


def check(name, ok, detail=None):
    checks.append({"check": name, "ok": bool(ok), "detail": detail})
    return ok


report = load(f"{SPEC}/SPECIALIST-REPORT.json")

# 1. Every artifact the specialist listed exists with the stated sha/bytes.
bad = []
for art in report["artifacts"]:
    try:
        h, n = sha(art["path"])
        if h != art["sha256"] or n != art["bytes"]:
            bad.append({"path": art["path"], "stated": art["sha256"], "actual": h, "bytes_stated": art["bytes"], "bytes_actual": n})
    except FileNotFoundError:
        bad.append({"path": art["path"], "missing": True})
check("specialist_report_artifact_hashes_match_disk", not bad, {"artifacts": len(report["artifacts"]), "mismatches": bad})

# 2. Each export summary's result_sha256/result_bytes matches the exported file bytes; the file parses.
export_pairs = [
    ("04-authoring-context", "work/everyday-guide/specialist/04-authoring-context.json"),
    ("05-family-review-context", "work/everyday-guide/specialist/05-family-review-context.json"),
    ("06-family-report", "work/everyday-guide/specialist/06-family-report.json"),
    ("08-family-replay-result", "work/everyday-guide/specialist/08-family-replay-result.json"),
    ("12-handoff-result", "work/everyday-guide/specialist/12-handoff-result.json"),
]
export_results = {}
for stem, result_rel in export_pairs:
    summary = load(f"{SPEC}/{stem}.summary.json")
    h, n = sha(result_rel)
    parsed = load(result_rel)
    export_results[stem] = {
        "summary_result_path": summary.get("result_path"),
        "summary_result_sha256": summary.get("result_sha256"),
        "summary_result_bytes": summary.get("result_bytes"),
        "disk_sha256": h,
        "disk_bytes": n,
        "result_saved": summary.get("result_saved"),
        "hash_domains": summary.get("hash_domains"),
        "summary_state_hash": summary.get("state_hash") or summary.get("hash"),
        "parsed_type": type(parsed).__name__,
    }
    ok = (
        summary.get("result_saved") is True
        and summary.get("result_path") == result_rel
        and summary.get("result_sha256") == h
        and summary.get("result_bytes") == n
        and (summary.get("hash_domains") or {}).get("result_sha256") == "file_sha256"
    )
    check(f"export_{stem}_summary_matches_file", ok, export_results[stem])

# 3. Replay result: reuse without publication, same review report, same state.
replay = load(f"{SPEC}/08-family-replay-result.json")
replay_view = {k: replay.get(k) for k in ("reused_review", "publications", "remote_executed", "review_sha256", "state_hash", "revision", "review", "candidate", "task_status", "hash_domains")}
check(
    "specialist_replay_reused_without_publication",
    replay.get("reused_review") is True
    and replay.get("publications") == []
    and replay.get("remote_executed") in (False, None)
    and replay.get("review_sha256") == EXPECTED_REVIEW
    and replay.get("state_hash") == EXPECTED_STATE
    and replay.get("revision") == 126,
    replay_view,
)
verdict_ids = None
for key in ("verdicts", "criteria"):
    if key in replay:
        verdict_ids = replay[key]
        break
replay_view["verdicts_or_criteria"] = verdict_ids

# 3b. Caller's own replay through the kit CLI (file-based, unchanged observation).
caller_replay_rel = f"{CALLER}/replay-result.json"
if os.path.exists(p(caller_replay_rel)):
    cr = load(caller_replay_rel)
    cr_summary = load(f"{CALLER}/replay-result.summary.json")
    h, n = sha(caller_replay_rel)
    check(
        "caller_replay_reused_without_publication",
        cr.get("reused_review") is True and cr.get("publications") == [] and cr.get("review_sha256") == EXPECTED_REVIEW and cr.get("state_hash") == EXPECTED_STATE and cr.get("revision") == 126
        and cr_summary.get("result_sha256") == h and cr_summary.get("result_bytes") == n,
        {k: cr.get(k) for k in ("reused_review", "publications", "remote_executed", "review_sha256", "state_hash", "revision")} | {"summary_sha_matches": cr_summary.get("result_sha256") == h},
    )
    # Same semantic result as the specialist's replay apart from nothing (both full results compared).
    check("caller_and_specialist_replay_results_equal", cr == replay, None if cr == replay else {"differing_keys": sorted(k for k in set(cr) | set(replay) if cr.get(k) != replay.get(k))})
else:
    check("caller_replay_reused_without_publication", False, "caller replay result missing")

# 4. Validate after replay and after handoff: same revision/hash as the start.
for stem in ("09-validate-after", "13-validate-final"):
    v = load(f"{SPEC}/{stem}.json")
    check(f"{stem}_state_unchanged", v.get("valid") is True and v.get("hash") == EXPECTED_STATE and v.get("revision") == 126 and v.get("files_verified") is True and v.get("records") == 794, {k: v.get(k) for k in ("valid", "format", "revision", "hash", "records", "files_verified", "hash_domains")})

# 5. Review report file hashes to its directory name and embeds the same observation as identical-review.json.
review_rel = f".pixl/assets/queue.ready/reviews/{EXPECTED_REVIEW}/review.json"
rh, _ = sha(review_rel)
check("retained_review_report_hashes_to_name", rh == EXPECTED_REVIEW, {"path": review_rel, "sha256": rh})
review_report = load(review_rel)
obs = load("work/export-review/identical-review.json")
orig = load("work/native-review/07-family-review-request.json")
embedded = review_report.get("request") or review_report.get("observation")
check("identical_review_equals_original_request_and_embedded_report_request", obs == orig and (embedded == obs if embedded is not None else False), {"identical_eq_original": obs == orig, "embedded_key_present": embedded is not None, "embedded_eq_identical": embedded == obs, "identical_sha256": sha("work/export-review/identical-review.json")[0], "original_sha256": sha("work/native-review/07-family-review-request.json")[0]})
check("observation_binding_hash_matches_context", obs.get("binding_hash") == EXPECTED_BINDING, obs.get("binding_hash"))

# 6. Family review context (specialist export and caller export) agree; creation vs current acceptance distinct.
ctx_s = load(f"{SPEC}/05-family-review-context.json")
ctx_c = load(f"{CALLER}/review-context-family.json")
check("caller_and_specialist_review_context_equal", ctx_s == ctx_c, {"specialist_sha256": sha(f"{SPEC}/05-family-review-context.json")[0], "caller_sha256": sha(f"{CALLER}/review-context-family.json")[0]})
crit = ctx_c.get("criteria") or []
crit_view = [{"id": c.get("id"), "status": c.get("status"), "verdict": c.get("verdict")} for c in crit]
snap = ctx_c.get("snapshot_acceptance") or {}
cur = ctx_c.get("current_acceptance") or {}
check(
    "family_prior_acceptance_unchanged",
    ctx_c.get("state_hash") == EXPECTED_STATE
    and ctx_c.get("binding_hash") == EXPECTED_BINDING
    and ctx_c.get("task_status") == "done"
    and snap.get("accepted") is False
    and cur.get("all_required_pass") is True
    and cur.get("task_complete") is True
    and sorted(c.get("verdict") for c in crit) == [f"native-review.family.collective.verdict.{i}" for i in range(3)]
    and all(c.get("status") == "pass" for c in crit),
    {"state_hash": ctx_c.get("state_hash"), "binding_hash": ctx_c.get("binding_hash"), "task_status": ctx_c.get("task_status"), "nominated": ctx_c.get("nominated"), "snapshot_acceptance": snap, "current_acceptance": cur, "criteria": crit_view, "manifest_sha256": ctx_c.get("manifest_sha256") or (ctx_c.get("manifest") or {}).get("sha256")},
)

# 7. Manifest members: manifest sha, member hashes vs renderer-successor/assets and assets/.
manifest_rel = f".pixl/assets/queue.ready/deliveries/{EXPECTED_MANIFEST}/manifest.json"
mh, _ = sha(manifest_rel)
manifest = load(manifest_rel)
members = []
for m in manifest.get("files", []):
    entry = {"candidate": m.get("candidate"), "output": m.get("output"), "sha256": m.get("sha256"), "file": m.get("path"), "bytes": m.get("bytes")}
    entry["copied_file_sha256"] = sha(f".pixl/assets/queue.ready/deliveries/{EXPECTED_MANIFEST}/" + entry["file"])[0] if entry["file"] else None
    members.append(entry)
asset_hashes = {rel: sha(rel)[0] for rel in ("renderer-successor/assets/working.png", "renderer-successor/assets/ready-confirmed.png", "renderer-successor/assets/error-retry.png", "renderer-successor/assets/paused.png", "assets/working.png", "assets/ready-confirmed.png", "assets/error-retry.png", "assets/paused.png") if os.path.exists(p(rel))}
manifest_member_shas = {m["sha256"] for m in members}
check("manifest_hashes_to_name_and_copies_match", mh == EXPECTED_MANIFEST and len(members) == 4 and all(m["copied_file_sha256"] == m["sha256"] for m in members) and (manifest.get("acceptance") or {}).get("accepted") is False, {"manifest_sha256": mh, "accepted_at_creation": (manifest.get("acceptance") or {}).get("accepted"), "source_state_sha256": manifest.get("source_state_sha256"), "created_at": manifest.get("created_at"), "members": members})
check("destination_assets_are_manifest_members", all(h in manifest_member_shas for h in asset_hashes.values()) and len(asset_hashes) == 8 and len(manifest_member_shas) == 4, asset_hashes)

# 8. Handoff file: hashes to its name; its identities match fresh focused PLAR read (CLI before, CLI specialist after, MCP caller after).
handoff_rel = report["handoff"]["path"]
hh, hn = sha(handoff_rel)
handoff = load(handoff_rel)
hres = load(f"{SPEC}/12-handoff-result.json")
hsum = load(f"{SPEC}/12-handoff-result.summary.json")
plar_before = load(f"{CALLER}/plar-read-before.json")
plar_spec_before = load(f"{SPEC}/01-plar-read.json")
plar_spec_after = load(f"{SPEC}/10-plar-read-after.json")
plar_mcp_after = load(f"{CALLER}/plar-read-mcp-after.json")


def plar_identity(d):
    return {"hash": d.get("hash"), "requirements_hash": d.get("requirements_hash"), "state_hash": d["production"]["continuation"]["state_hash"], "store": d["production"]["continuation"]["store"], "action": d["production"]["continuation"]["action"], "asset_status": d["asset"]["status"], "task": d["production"].get("task"), "task_state": d["production"].get("task_state"), "revision": d["production"].get("revision")}


ids = {"caller_cli_before": plar_identity(plar_before), "specialist_cli_before": plar_identity(plar_spec_before), "specialist_cli_after": plar_identity(plar_spec_after), "caller_mcp_after": plar_identity(plar_mcp_after)}
check("plar_reads_agree_before_and_after", len({json.dumps(v, sort_keys=True) for v in ids.values()}) == 1, ids)
check("plar_reads_semantically_equal_except_root_form", all(json.loads(json.dumps(d).replace("\\\\", "/")) == json.loads(json.dumps(plar_before).replace("\\\\", "/")) for d in (plar_spec_before, plar_spec_after, plar_mcp_after)), None)


def find_keys(obj, wanted, path="$", out=None):
    if out is None:
        out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in wanted and isinstance(v, (str, int)):
                out.setdefault(k, []).append((f"{path}.{k}", v))
            find_keys(v, wanted, f"{path}.{k}", out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_keys(v, wanted, f"{path}[{i}]", out)
    return out


found = find_keys(handoff, {"requirements_hash", "state_hash", "expect", "asset_id", "store", "next", "status", "path"})
req_vals = {v for _, v in found.get("requirements_hash", [])}
state_vals = {v for _, v in found.get("state_hash", [])} | {v for _, v in found.get("expect", [])}
fresh = ids["caller_mcp_after"]
check(
    "handoff_identities_match_fresh_focused_plar",
    hh == os.path.basename(handoff_rel).split(".")[0]
    and hsum.get("result_saved") is True
    and hres.get("sha256") == hh
    and hres.get("path") == handoff_rel
    and hres.get("requirements_hash") == fresh["requirements_hash"]
    and hres.get("state_hash") == fresh["state_hash"]
    and (hres.get("hash_domains") or {}) == {"requirements_hash": "selected_requirements_sha256", "state_hash": "canonical_state_sha256", "sha256": "file_sha256"}
    and handoff.get("requirements_hash") == fresh["requirements_hash"]
    and (handoff.get("selection") or {}).get("hash") == fresh["hash"]
    and (handoff.get("selection") or {}).get("current") is True
    and (handoff.get("resume") or {}).get("state_hash") == fresh["state_hash"]
    and (handoff.get("resume") or {}).get("action") == "delivered"
    and req_vals == {fresh["requirements_hash"]}
    and state_vals <= {fresh["state_hash"]}
    and fresh["state_hash"] in state_vals
    and fresh["hash"] not in state_vals
    and fresh["hash"] not in req_vals,
    {"handoff_path": handoff_rel, "handoff_sha256": hh, "bytes": hn, "requirements_hash_values": sorted(req_vals), "state_hash_values": sorted(state_vals), "plar_file_hash_only_in_selection": {"selection": handoff.get("selection"), "not_used_as_state_guard": fresh["hash"] not in state_vals}, "resume_action": (handoff.get("resume") or {}).get("action"), "resume_state_hash": (handoff.get("resume") or {}).get("state_hash"), "top_level_keys": sorted(handoff.keys()), "handoff_result": hres, "handoff_summary": hsum},
)
resume_delivery = (handoff.get("resume") or {}).get("delivery") or {}
fresh_delivery = plar_mcp_after["production"]["continuation"].get("delivery") or {}
check("handoff_resume_equals_fresh_continuation", (handoff.get("resume") or {}) == plar_mcp_after["production"]["continuation"], {"resume_delivery_complete": resume_delivery.get("complete"), "families": resume_delivery.get("families"), "fresh_equal": (handoff.get("resume") or {}) == plar_mcp_after["production"]["continuation"]})
handoff_next = handoff.get("next")
handoff_details = handoff.get("details") or {}
handoff_view = {
    "next": handoff_next,
    "asset_id": handoff.get("asset_id") or handoff.get("asset"),
    "requirements_hash": handoff.get("requirements_hash"),
    "details_status": handoff_details.get("status"),
    "details_keys": sorted(handoff_details.keys()),
    "caller_actions_count": len(handoff_details.get("caller_actions") or []),
    "future_work_count": len(handoff_details.get("future_work") or []),
    "production_keys": sorted((handoff.get("production") or {}).keys()) if isinstance(handoff.get("production"), dict) else None,
}
check("handoff_has_truthful_status_and_scope", handoff_details.get("status") == "delivered" and (handoff_details.get("future_work") or []) and (handoff_details.get("caller_actions") is not None), handoff_view)

# 9. Source range: the retrieved text equals lines 18-21 of the current file and the file hash matches.
src = load(f"{SPEC}/07-source-range.json")
src_sha, _ = sha("src/queue-view-successor.ts")
with open(p("src/queue-view-successor.ts"), "rb") as f:
    raw_src = f.read().decode("utf-8")
lines = raw_src.splitlines(keepends=True)
start, end = src.get("start"), src.get("end")
expected_text = "".join(lines[start - 1:end]) if start and end else None  # exact bytes incl. CRLF line endings
returned_text = src.get("text")
check("source_range_matches_current_file", src.get("sha256") == src_sha == report["source_range"]["sha256"] and returned_text is not None and returned_text == expected_text and len(returned_text.encode("utf-8")) == src.get("bytes") and (src.get("hash_domains") or {}).get("sha256") == "file_sha256" and "reducedMotion) return 0" in returned_text, {"path_from_specialist_report": report["source_range"]["path"], "sha256_returned": src.get("sha256"), "sha256_disk": src_sha, "start": start, "end": end, "bytes": src.get("bytes"), "returned_text": returned_text, "exact_match_including_crlf": returned_text == expected_text})

# 10. Tree diff: only the handoff file was added; nothing changed or removed outside work/everyday-guide.
td = load(f"{CALLER}/tree-diff.json")
check("consumer_tree_only_gained_handoff_file", td["added"] == [handoff_rel] and td["removed"] == [] and td["changed"] == [], td)

# 11. Specialist did not use MCP root other than consumer; roots reported.
roots = {"specialist_consumer_root": report.get("consumer_root"), "plar_project_root_cli": plar_before.get("project_root"), "plar_project_root_mcp": plar_mcp_after.get("project_root"), "handoff_result_root_fields": {k: v for k, v in hres.items() if "root" in k}}
check("roots_resolve_to_this_consumer", all(os.path.normcase(os.path.normpath(str(r))) == os.path.normcase(ROOT) for r in (roots["specialist_consumer_root"], roots["plar_project_root_cli"], roots["plar_project_root_mcp"]) if r), roots)

summary = {"root": ROOT, "checks_total": len(checks), "checks_ok": sum(1 for c in checks if c["ok"]), "failed": [c["check"] for c in checks if not c["ok"]], "checks": checks}
with open(p(f"{CALLER}/verification.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1, ensure_ascii=False)
for c in checks:
    print(("OK  " if c["ok"] else "FAIL"), c["check"])
print("failed:", summary["failed"])
