"""Caller-side independent verification for the NF-08 asset-lineage increment.

Read-only except for writing work/asset-lineage/caller-independent-checks.json.

usage: python -I caller_verify.py <consumer_root>
"""
import hashlib
import json
import os
import sys

ROOT = os.path.abspath(sys.argv[1])
AL = "work/asset-lineage"


def p(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def sha(rel):
    h = hashlib.sha256()
    with open(p(rel), "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(rel):
    with open(p(rel), encoding="utf-8") as fh:
        return json.load(fh)


def ref(rel):
    return {"path": rel, "sha256": sha(rel)}


checks = []


def check(name, ok, detail):
    checks.append({"check": name, "status": "pass" if ok else "fail", "detail": detail})
    return ok


# ---------------------------------------------------------------- baseline diff
baseline = load(f"{AL}/caller-baseline-hashes.json")
skip = p(AL)
current = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    if os.path.abspath(dirpath).startswith(skip):
        dirnames[:] = []
        continue
    for name in filenames:
        full = os.path.join(dirpath, name)
        rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
        h = hashlib.sha256()
        with open(full, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        current[rel] = h.hexdigest()
base_files = {k: v["sha256"] for k, v in baseline["files"].items()}
changed = sorted(k for k in base_files if k in current and current[k] != base_files[k])
removed = sorted(k for k in base_files if k not in current)
added = sorted(k for k in current if k not in base_files)
check(
    "original_bytes_unchanged_outside_work_asset_lineage",
    not changed and not removed,
    {"baseline_files": len(base_files), "current_files": len(current), "changed": changed, "removed": removed},
)
pycache_added = [a for a in added if "/__pycache__/" in a and a.endswith(".pyc")]
other_added = [a for a in added if a not in pycache_added]
check(
    "no_files_added_outside_work_asset_lineage",
    not added,
    {
        "added_total": len(added),
        "added_python_bytecode_caches_under_installed_kit_runtime": pycache_added,
        "added_other": other_added,
        "note": "Bytecode caches are interpreter side effects of the specialist's CLI reads; they are regenerable and contain no project data. No baseline file changed or disappeared.",
    },
)

# ---------------------------------------------------------------- fixture bytes
fixture = load("work/asset-lineage-inputs/fixture.json")
fx_ok = True
fx_detail = {}
for slot, members in fixture["members"].items():
    for i, m in enumerate(members):
        actual = sha(m["path"])
        fx_detail[f"{slot}[{i}] {m['candidate']}"] = {"expected": m["sha256"], "actual": actual}
        fx_ok &= actual == m["sha256"]
for k, ev in fixture["source_evidence"].items():
    actual = sha(ev["path"])
    fx_detail[f"source_evidence.{k}"] = {"expected": ev["sha256"], "actual": actual}
    fx_ok &= actual == ev["sha256"]
check("fixture_member_and_source_evidence_bytes_match", fx_ok, fx_detail)

# delivered destination bytes equal the family member artifacts
dest = {
    "ready": "assets/ready-confirmed.png",
    "working": "assets/working.png",
    "retry": "assets/error-retry.png",
    "paused": "assets/paused.png",
}
dest_detail = {}
dest_ok = True
for slot, path in dest.items():
    actual = sha(path)
    expected = fixture["members"][slot][0]["sha256"]
    dest_detail[path] = {"expected_member_sha256": expected, "actual": actual}
    dest_ok &= actual == expected
check("destination_assets_equal_member_artifacts", dest_ok, dest_detail)

# ---------------------------------------------------------------- ten reads + caller reads exist
reads = fixture["reads"]
read_refs = {}
all_exist = True
for key, spec in reads.items():
    rel = spec["result_path"]
    exists = os.path.isfile(p(rel))
    all_exist &= exists
    read_refs[key] = ref(rel) if exists else {"path": rel, "sha256": None, "missing": True}
check("ten_specialist_read_results_present", all_exist, read_refs)
caller_refs = {k: ref(v["result_path"]) for k, v in fixture["caller_reads"].items()}
check(
    "caller_context_reads_byte_identical_to_specialist_context_reads",
    caller_refs["original_context"]["sha256"] == read_refs["original_context"]["sha256"]
    and caller_refs["reused_context"]["sha256"] == read_refs["reused_context"]["sha256"],
    {"caller": caller_refs, "specialist": {k: read_refs[k] for k in ("original_context", "reused_context")}},
)

# ---------------------------------------------------------------- state hash agreement
state_file_sha = sha(".pixl/assets/queue.ready/state.px")
oc = load(f"{AL}/caller-original-context.json")
rc = load(f"{AL}/caller-reused-context.json")
of = load(f"{AL}/original-family.json")
rf = load(f"{AL}/reused-family.json")
plars = {a: load(f"{AL}/plar-{a}.json") for a in ("ready", "working", "retry", "paused")}
hashes = {
    "state.px file sha256": state_file_sha,
    "caller-original-context.state_hash": oc["state_hash"],
    "caller-reused-context.state_hash": rc["state_hash"],
    "original-family.hash": of["hash"],
    "reused-family.hash": rf["hash"],
}
for a in ("working", "retry", "paused"):
    hashes[f"plar-{a}.production.hash"] = plars[a]["production"].get("hash")
check("state_hash_agrees_across_public_surfaces_and_state_file", len(set(hashes.values())) == 1, hashes)
plar_file_sha = sha("authoring-plar.txt")
plar_hashes = {"authoring-plar.txt sha256": plar_file_sha}
for a, d in plars.items():
    plar_hashes[f"plar-{a}.hash"] = d["hash"]
check("plar_file_hash_agrees_across_plar_reads", len(set(plar_hashes.values())) == 1, plar_hashes)

# ---------------------------------------------------------------- cross-surface member identities
slots = ["ready", "working", "retry", "paused"]
oc_members = {i: m for i, m in enumerate(oc["members"])}
rc_members = {i: m for i, m in enumerate(rc["members"])}
of_snap = of["families"][0]["snapshots"][0]["files"]
rf_snap = rf["families"][0]["snapshots"][0]["files"]
of_family_members = of["families"][0]["members"]
rf_family_members = rf["families"][0]["members"]
comparison = load(f"{AL}/COMPARISON.json")
cmp_members = comparison["members"]
cross = {}
cross_ok = True
for i, slot in enumerate(slots):
    fx_o, fx_r = fixture["members"][slot]
    row = {
        "fixture": {"original": (fx_o["candidate"], fx_o["sha256"]), "reused": (fx_r["candidate"], fx_r["sha256"])},
        "caller_review_context": {
            "original": (oc_members[i]["candidate"], oc_members[i]["sha256"]),
            "reused": (rc_members[i]["candidate"], rc_members[i]["sha256"]),
        },
        "family_snapshot_files": {
            "original": (of_snap[i]["candidate"], of_snap[i]["sha256"]),
            "reused": (rf_snap[i]["candidate"], rf_snap[i]["sha256"]),
        },
        "family_members": {
            "original": of_family_members[i]["candidate"],
            "reused": rf_family_members[i]["candidate"],
        },
        "comparison": {
            "original": (cmp_members[slot]["original_candidate"], cmp_members[slot]["original_sha256"]),
            "reused": (cmp_members[slot]["reused_candidate"], cmp_members[slot]["reused_sha256"]),
            "same_bytes": cmp_members[slot]["same_bytes"],
        },
    }
    if slot != "ready":
        cont = plars[slot]["production"]["continuation"]["delivery"]
        row["plar_continuation_delivery"] = (cont["candidate"], cont["lineage"]["sha256"], cont["destination"])
    ok = (
        row["fixture"]["original"] == row["caller_review_context"]["original"] == row["family_snapshot_files"]["original"] == row["comparison"]["original"]
        and row["fixture"]["reused"] == row["caller_review_context"]["reused"] == row["family_snapshot_files"]["reused"] == row["comparison"]["reused"]
        and row["family_members"]["original"] == fx_o["candidate"]
        and row["family_members"]["reused"] == fx_r["candidate"]
        and row["comparison"]["same_bytes"] == (fx_o["sha256"] == fx_r["sha256"])
    )
    if slot != "ready":
        ok &= row["plar_continuation_delivery"][0] == fx_r["candidate"] and row["plar_continuation_delivery"][1] == fx_r["sha256"]
    row["agree"] = ok
    cross_ok &= ok
    cross[slot] = row
check("member_identities_and_hashes_agree_across_all_public_surfaces_and_comparison", cross_ok, cross)
check(
    "comparison_families_match_fixture",
    comparison["families"] == fixture["families"],
    {"fixture": fixture["families"], "comparison": comparison["families"]},
)

# ---------------------------------------------------------------- source excerpt returns
wc = load(f"{AL}/working-construction.json")
rfx = load(f"{AL}/ready-fixture.json")
wc_ok = (
    wc["sha256"] == fixture["source_evidence"]["working_construction"]["sha256"]
    and wc["start"] == 1 and wc["end"] == 17
    and "21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629" in wc["text"]
    and "lossless quarter-turn pixel permutation of generated seed" in wc["text"]
    and '"patch_count": 196' in wc["text"]
)
check("working_construction_excerpt_matches_cited_source", wc_ok, {"sha256": wc["sha256"], "start": wc["start"], "end": wc["end"], "bytes": wc["bytes"]})
rfx_ok = (
    rfx["sha256"] == fixture["source_evidence"]["ready_fixture"]["sha256"]
    and '"provider_simulated":true' in rfx["text"]
    and '"connection":"pixellab-test"' in rfx["text"]
    and "controlled-create-0002" in rfx["text"]
    and "Controlled evaluator fixture, not upstream generation." in rfx["text"]
    and '"download_sha256":"fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"' in rfx["text"]
    and '"provider_simulated":false' not in rfx["text"]
)
check("ready_fixture_excerpt_shows_controlled_simulated_provider", rfx_ok, {"sha256": rfx["sha256"], "bytes": rfx["bytes"]})

# ---------------------------------------------------------------- independent journal evidence
journals = {
    "ready r.22e90a2a03fe453a.request": ".pixl/assets/queue.ready/jobs/e7cc448003dc41409ef16591c3793a118859d4e9b4e5f44ff18be8ad07783922.json",
    "working live.working-animation-motion-01.job": ".pixl/assets/queue.ready/jobs/42e54029b82111da019824b279b53fdfb14619720362525d43bec2eb95f72389.json",
    "working live.working-seed.job": ".pixl/assets/queue.ready/jobs/5ba42107ae11f29a06afd9761b418e02767f5734b477c5aa6030cf9c2887743c.json",
    "working live.working-animation-01.job (unused AI animation)": ".pixl/assets/queue.ready/jobs/bfe185a1a7c1d8001374b117cb903da934ce8cf4820772fc2477d918c0df643a.json",
    "working live.working-animation-repair-01.job": ".pixl/assets/queue.ready/jobs/b982e1e81cc34ceef5944159c078afd4d45f7215bd93fc8452782d0f72a60226.json",
    "retry live.retry.job": ".pixl/assets/queue.ready/jobs/f3c4ef548d11058f4103f75c5bed853ca532844892e04d5ed6c7c00dc914f339.json",
    "paused live.paused-02.job": ".pixl/assets/queue.ready/jobs/4b5399fa7a514375970a792c8ef66a695058551084d087d6a88867fca963a877.json",
    "paused live.paused-cutout-01.job": ".pixl/assets/queue.ready/jobs/833f779f2523cb74bffb9aa6400b4176ea8e00a81ef87c4740fbd2268ef9e387.json",
    "paused live.paused.job (failed)": ".pixl/assets/queue.ready/jobs/196ce9300b16516f1b60d362f50a83e0e1f24f841203f99f46ef4ed104d7abcd.json",
}
jdetail = {}
j_ok = True
for label, rel in journals.items():
    d = load(rel)
    name_hash = os.path.basename(rel)[:-5]
    actual = sha(rel)
    imported = [e for e in d["events"] if e["event"] == "imported"]
    jdetail[label] = {
        "path": rel,
        "sha256": actual,
        "content_addressed": actual == name_hash,
        "job": d["intent"]["job"],
        "state": d.get("state"),
        "provider": d["intent"]["request"].get("provider"),
        "tool": d["intent"]["request"].get("tool"),
        "remote_executed_field": d["intent"]["request"].get("remote_executed"),
        "events": [e["event"] for e in d["events"]],
        "imported_sha256": [e["evidence"].get("sha256") or e["evidence"].get("download_sha256") for e in imported],
        "imported_candidate": [e["artifact"]["id"] for e in imported if e.get("artifact")],
    }
    j_ok &= actual == name_hash

expect_import = {
    "ready r.22e90a2a03fe453a.request": "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5",
    "working live.working-animation-motion-01.job": "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc",
    "working live.working-seed.job": "21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629",
    "working live.working-animation-01.job (unused AI animation)": "32615f3de934c991e4f58ce066fc50fdcfdba60ba50fb4f5e9a6454cbd0fddec",
    "retry live.retry.job": "0fb0ab5e486df874bb3d5abba70c5301945bc55fefb895f22eff8860c8b7e5e4",
    "paused live.paused-02.job": "16039251a58ae9658f790d8d8846d4d4ed62ae5736bd954948085499b618c95a",
    "paused live.paused-cutout-01.job": "80d2b823cf1ad6f255987aebc990c184d4be0600b04c965258dfaa54a4f72d92",
}
for label, exp in expect_import.items():
    j_ok &= exp in jdetail[label]["imported_sha256"]
j_ok &= jdetail["paused live.paused.job (failed)"]["state"] == "failed"
check("job_journals_content_addressed_and_import_hashes_as_expected", j_ok, jdetail)

# motion job edits the repair job's remote result; repair edits an upload of the seed strip; construction cites seed
motion = load(journals["working live.working-animation-motion-01.job"])
repair = load(journals["working live.working-animation-repair-01.job"])
construction = load("work/live-family/working-animation-motion-01-construction.json")
chain = {
    "motion_argv_edit_source": motion["intent"]["request"]["arguments"]["argv"][1],
    "repair_remote_id": repair.get("remote_id"),
    "repair_argv_edit_source": repair["intent"]["request"]["arguments"]["argv"][1],
    "construction_seed_sha256": construction["seed_sha256"],
    "construction_operation": construction["operation"],
    "construction_patch_count": construction["patch_count"],
    "motion_patch_count_in_argv": len(json.loads(motion["intent"]["request"]["arguments"]["argv"][3])[0]["pixels"]),
    "seed_artifact_sha256": sha(".pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png"),
    "working_strip_upload_record": load("work/live-family/working-strip-upload.json"),
    "note": "upload:a266e48d... is a provider upload reference; its content is not retained locally and the link seed->upload stays declared, not byte-verified.",
}
chain_ok = (
    chain["motion_argv_edit_source"] == chain["repair_remote_id"]
    and chain["construction_seed_sha256"] == chain["seed_artifact_sha256"]
    and chain["construction_patch_count"] == chain["motion_patch_count_in_argv"] == 196
)
check("working_deterministic_construction_chain_consistent", chain_ok, chain)

# reuse declarations in the state file
state_text = open(p(".pixl/assets/queue.ready/state.px"), encoding="utf-8").read()
reuse = {}
reuse_ok = True
for slot, src in (("working", "live.working-animation-motion-01.candidate"), ("retry", "live.retry.candidate"), ("paused", "live.paused-cutout-01.candidate")):
    line = next((l for l in state_text.splitlines() if l.startswith(f"@artistic2.{slot}.candidate:")), "")
    has = f"source_candidate=~{len(src)}:{src}" in line and "Existing bytes reused, no provider execution; previous acceptance not transferred." in line
    reuse[slot] = {"declared_source_candidate": src, "declaration_present": has}
    reuse_ok &= has
check("artistic2_reuse_provenance_declarations_present_in_state", reuse_ok, reuse)

# snapshot ordering (direction evidence is temporal/declarative, not byte equality)
order = {
    "original_manifest_created_at": of["families"][0]["snapshots"][0]["created_at"],
    "reused_manifest_created_at": rf["families"][0]["snapshots"][0]["created_at"],
    "original_imports_recorded_at": {
        "working": [e["recorded_at"] for e in motion["events"] if e["event"] == "imported"],
    },
}
check(
    "original_snapshot_precedes_reused_snapshot",
    order["original_manifest_created_at"] < order["reused_manifest_created_at"],
    order,
)

# ---------------------------------------------------------------- specialist reports
spec = load(f"{AL}/SPECIALIST-RESULT.json")


def iter_refs(node, trail="$"):
    if isinstance(node, dict):
        if "path" in node and "sha256" in node and isinstance(node.get("sha256"), str) and isinstance(node.get("path"), str):
            yield trail, node
        for k, v in node.items():
            yield from iter_refs(v, f"{trail}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from iter_refs(v, f"{trail}[{i}]")


def verify_refs(doc, label):
    bad = []
    n = 0
    for trail, r in iter_refs(doc):
        n += 1
        rel = r["path"].replace("\\", "/")
        if not os.path.isfile(p(rel)):
            bad.append({"at": trail, "path": r["path"], "problem": "missing"})
            continue
        actual = sha(rel)
        if actual != r["sha256"]:
            bad.append({"at": trail, "path": r["path"], "expected": r["sha256"], "actual": actual})
    check(f"{label}_file_refs_resolve_to_actual_bytes", not bad, {"refs_checked": n, "mismatches": bad})


verify_refs(spec, "specialist_result")
verify_refs(comparison, "comparison")

ops_ok = set(spec["operations"].keys()) == set(reads.keys())
ops_detail = {}
for k in reads:
    r = spec["operations"].get(k)
    if isinstance(r, dict) and isinstance(r.get("result"), dict):
        r = r["result"]
    elif isinstance(r, dict) and isinstance(r.get("ref"), dict):
        r = r["ref"]
    got = (r or {}).get("path"), (r or {}).get("sha256")
    exp = (read_refs[k]["path"], read_refs[k]["sha256"])
    ops_detail[k] = {"specialist": got, "caller_measured": exp, "agree": got == exp}
    ops_ok &= got == exp
check("specialist_operations_map_to_exact_saved_read_files", ops_ok, ops_detail)
check(
    "specialist_result_flags",
    spec.get("new_provider_execution") is False and spec.get("acceptance_created") is False,
    {"new_provider_execution": spec.get("new_provider_execution"), "acceptance_created": spec.get("acceptance_created"), "production_unchanged": spec.get("production_unchanged")},
)

expected_claims = {
    "ready_is_controlled_fixture": True,
    "ready_is_authenticated_provider_generation": False,
    "working_has_retained_deterministic_construction_record": True,
    "working_final_is_provider_generated_animation": False,
    "paused_has_recorded_generation_and_deterministic_cutout": True,
    "retry_has_recorded_generation_request": True,
    "same_bytes_proves_reuse_direction": False,
    "remote_execution_authenticated": False,
}
kc = comparison["key_claims"]
kc_detail = {k: {"specialist": kc.get(k), "caller_independent": v, "agree": kc.get(k) is v} for k, v in expected_claims.items()}
check("key_claims_agree_with_caller_independent_evidence_reading", all(x["agree"] for x in kc_detail.values()), kc_detail)

out = {
    "root": ROOT,
    "all_pass": all(c["status"] == "pass" for c in checks),
    "checks": checks,
}
with open(p(f"{AL}/caller-independent-checks.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=2)
print(json.dumps({"all_pass": out["all_pass"], "failed": [c["check"] for c in checks if c["status"] != "pass"]}))
