"""Reproducible checks for revision 16 (2026-11-16, c). Read-only.

1. The state decodes as revision 16 with exactly the 88 revision 15 records unchanged (compared
   with work/rev15.json) plus s_continuation_11 and handoff_12 (90 records).
2. s_continuation_11 digest/line range equals the current 2026-11-16c note bytes; the b, 2026-11-16,
   g and f notes still hash as bound by s_continuation_10 / _9 / _8 / _7; the b result, the
   revision 15 handoff-review files, the retained packet, criteria, validation artifact, source,
   reference, caller-result and earlier work files still match the hashes quoted in revisions 10-16.
3. handoff_12 has rv 16, nx [t_sample], bl [t_scout, t_medic, t_family] and
   fo = [s_continuation_11] + handoff_11.fo.
4. The note quotes the sha256 of every new file it lists (except itself and the files produced
   after it) and does not contain the revision 16 hash.
5. Every NON-KIT file recorded in work/rev16-protected-snapshot.sha256 (taken before any write in
   this correction round; bytecode caches excluded, none existed) still has the same bytes, except
   the two files edited on purpose (SESSION.md and the head state.px/state.px). Kit files are not
   byte-checked one by one: the kit identity is recorded through bundle-manifest.json's sha256
   (snapshot value and current value) plus the runner's own manifest verification, which must
   report status "verified". A kit version change is reported, not treated as a problem. Any
   __pycache__ directory under pixl-kit/ is reported as an observation (kit_bytecode_cache_dirs).
6. Runner `workflow` on the state reports ready [t_sample], no jobs, files verified.
7. Running validate_criteria_v2.py (print-only) leaves criteria-schema-validation.json unchanged.

Run from the consumer root with the selected interpreter:
  python -B -I work/verify_rev16.py [path-to-state, default state.px/state.px]
Pass work/rev16.px to check the encoded candidate before it is committed. Every kit runner
subprocess is started with -B -I, so the verifier itself writes no bytecode into the kit.
"""
import hashlib, json, os, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
STATE = sys.argv[1] if len(sys.argv) > 1 else "state.px/state.px"
NOTE = "deliverables/continuation-2026-11-16c.md"
SNAPSHOT = "work/rev16-protected-snapshot.sha256"
MANIFEST = "pixl-kit/bundle-manifest.json"
KIT_PREFIX = "pixl-kit/"
EDITED_ON_PURPOSE = {"SESSION.md", "state.px/state.px"}
RETAINED = {
    "deliverables/continuation-2026-11-16b.md": "6454d5b65397a7d1b647088055dccfb39e5b58173c34218df436584dae8c62f1",
    "deliverables/specialist-return-2026-11-16b.json": "7d80d6f90dfd6b86497e189e5f68f22f453f93fae9c69af0abc31157a5589114",
    "work/handoff-review-rev15/handoff-inventory-01.json": "47f0a535eca145ff85fa0a38fb64e95e5a6cd8b1d98edb7aa907ae6e28a02ad0",
    "work/handoff-review-rev15/handoff-review-01.json": "5d3175236d4561b0d3912c7141977fb6f5f6c4e34742bdeed2663b996400fd03",
    "work/handoff-review-rev15/handoff-check-01.json": "4c8ce8b287bd667a1be4270ded6a9eb4c7ba03eeb9085801d22004b93930dae0",
    "work/handoff-review-rev15/handoff-review-02.json": "e97a30121162c64b6d1c4ae4152fd51105fac9e5273957a695ca2e87144d2c19",
    "work/handoff-review-rev15/handoff-check-02.json": "fbcd6091b2754b8b9275ccaf170a1fe2dfc779a588fdf2a917ddac763f43873d",
    "work/handoff-review-rev15/build_review.py": "b0f1afcd8b8e9b00b0862a8f701910bae9a6ffccfaed568c1957d66a667c66a0",
    "deliverables/continuation-2026-11-16.md": "157d131cd3979d2b4e7e1729e4accbd2f8446f3573beed6e0fea543eb68fd420",
    "deliverables/continuation-2026-11-15g.md": "001065a3422bfb76997b375f9f66d22324e87a2841eb06d742e166d44fef2e4f",
    "deliverables/continuation-2026-11-15f.md": "9e0df8a1d8d4bbfa6591d16fffe07406f53c639d32b797e320232b15177a135f",
    "deliverables/continuation-2026-11-15e.md": "f174f93971f3044b9731aae34e2704d5e090c5468761361063548d15056d597f",
    "deliverables/continuation-2026-11-15d.md": "826460e5ff96f7dae2bccff8b8df1278e5457614cfaadd3c0510e0f64feeb1dc",
    "deliverables/sample-request/request-review-v2.json": "a596f02addb73ba1c7732cfe05a8071b97b7c7236f26e349fdca5184e0684d73",
    "deliverables/sample-request/sample-creative-brief-v2.json": "f84b262818bbf044eb22716ab5d02eed1103cc65714360fcfc5d9efd019a5b80",
    "deliverables/sample-request/sample-criteria.json": "14c979ea9bbfb686f7a9c693d552facfac5a135c45c3184d969611116611834b",
    "deliverables/sample-request/sample-creative-brief.json": "cc21bf77519ed46e7a6f634718efcc79816a8f9895cc4ece4e89b007bf7380ce",
    "deliverables/sample-request/request-review.json": "ffa933ede2b985eafd4c616e83b4a69d0b34a99002a731439704dcd0d781e78b",
    "deliverables/sample-request/criteria-schema-validation.json": "93643a34d32353b5471fd9943aed8bb3a0bf8cb48a94d8413c42635a1aaeb16a",
    "deliverables/sample-request/validate_criteria.py": "48f3d0f1274b9635284571eed78405955c0e9aa57fa0ee8e57ce2fa955adbe45",
    "deliverables/sample-request/validate_criteria_v2.py": "b582f32737eb5733f6be883c3e08b0ce9423408bb7249caa3b7c32d12011719b",
    "deliverables/sample-request/operation-shortlist.json": "7294d9d779982ee6602412eaed925ca2dab6e0b0c787f314455de6f53ed00186",
    "sources/brief.md": "a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324",
    "sources/controlled-evaluation-answers.md": "87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30",
    "sources/reference-observations.md": "d0862d144da0c4b315af96a8129846b32075fac99826b618ad51c62b6a960495",
    "sources/method-research.md": "1b1503b7a004c884b5b207a965aa85ac4c694f481d2936619a4030557f794e51",
    "reference.png": "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7",
    "reference-b.png": "e76b40ce38aeb436d0f5f0e433c4ac1eb4519bf93a7b29cd7a81a4609914a12a",
    "work/rev15.px": "8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c",
    "work/rev15.json": "ef630f476c6f1ac3fbd8d8d7bf3cda9d009a076453c5a1c7df50dbb4d779d6e4",
    "work/verify_rev15.py": "ff0dcb876c1bd2465c596e179eabc83f0df1a9f4781246dba967d0b758151c99",
    "work/build_rev15.py": "1cce24175089b2c7cb0aa67a3e3b7b138f0e4bfd6f4202b98b3569cb08034c0e",
    "work/rev15-protected-snapshot.sha256": "8f4872b079b393a919fb5b4957983fc9428efd47010da30c8dce00ae4f082dbf",
    "work/rev14.px": "247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af",
    "work/rev14.json": "fc9438e6bec1faf764776d434c6499137a5ef439992381369a93fef103cdb552",
    "work/verify_rev14.py": "e49ba11c72b7a6da5f2dad50237c7ec45e600f0ba553cfd5f3ed9cc7e4753e10",
    "work/rev13.px": "42db4c758d328c521c1f73baae1873b56b14e8a4d4d1b580c1d720dcecd8acd2",
    "CALLER-RESULT-LITERAL-RECONCILIATION.json": "7b033ec23f1307ab3083e8061fb5456a61fc389085b8b00ac36158d0f03229e3",
    "review/caller-comparison-2026-11-16-v6.md": "1c7e717745e00c11ac80b8bc13ff41c0be2c156b9f013bf5b401eea62fc4a0b5",
    "state.px/history/8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c.px": "8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c",
    "state.px/history/247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af.px": "247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af",
}
LISTED_IN_NOTE = ["work/build_rev16.py", "work/verify_rev16.py", SNAPSHOT]
HANDOFF_8_FO = ["s_continuation_7", "s_continuation_6", "s_sample_brief_v2",
                "s_sample_request_review_v2", "s_sample_criteria", "s_sample_brief",
                "s_sample_request_review", "s_eval_answers", "c_sample", "f_sample", "i_alpha",
                "i_animation", "i_backgrounds", "i_canvas", "i_design_language", "i_display_scale",
                "i_engine", "i_lighting", "i_outline", "i_palette", "i_role_diff", "i_sampling",
                "x_aid", "x_study"]
HANDOFF_9_FO = ["s_continuation_8"] + HANDOFF_8_FO
HANDOFF_10_FO = ["s_continuation_9"] + HANDOFF_9_FO
HANDOFF_11_FO = ["s_continuation_10"] + HANDOFF_10_FO
FO = ["s_continuation_11"] + HANDOFF_11_FO


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(*args):
    return json.loads(subprocess.run([PY, "-B", "-I", RUNNER, *args], capture_output=True,
                                     text=True, check=True, encoding="utf-8").stdout)


problems = []
doc = run("decode", STATE)
by = {r["id"]: r for r in doc["records"]}
old = {r["id"]: r for r in json.load(open("work/rev15.json", encoding="utf-8"))["records"]}
if doc["revision"] != 16:
    problems.append(f"revision {doc['revision']} != 16")
if len(by) != 90:
    problems.append(f"{len(by)} records != 90")
if len(old) != 88:
    problems.append(f"work/rev15.json holds {len(old)} records != 88")
for rid, rec in old.items():
    if by.get(rid) != rec:
        problems.append(f"{rid} changed but should be untouched")
if set(by) - set(old) != {"s_continuation_11", "handoff_12"}:
    problems.append(f"unexpected new records: {sorted(set(by) - set(old))}")
if [r["$ref"] for r in old["handoff_11"]["fields"]["fo"]] != HANDOFF_11_FO:
    problems.append("handoff_11.fo in work/rev15.json differs from the recorded list")

f = by.get("s_continuation_11", {}).get("fields")
if not f:
    problems.append("missing s_continuation_11")
else:
    if f["ur"] != NOTE or f["dg"] != sha(NOTE):
        problems.append("s_continuation_11 digest/path mismatch")
    if f["ln"] != [1, open(NOTE, "rb").read().count(b"\n")]:
        problems.append("s_continuation_11 line range mismatch")
    if f["at"] != "2026-11-16" or f["au"] != {"$symbol": "local"}:
        problems.append("s_continuation_11 at/au differ from the plan")
for path, want in RETAINED.items():
    if sha(path) != want:
        problems.append(f"retained file drifted: {path}")
n = by.get("handoff_12", {}).get("fields")
if not n:
    problems.append("missing handoff_12")
elif n["rv"] != 16 or n["nx"] != [{"$ref": "t_sample"}] or \
        n["bl"] != [{"$ref": x} for x in ("t_scout", "t_medic", "t_family")] or \
        n["fo"] != [{"$ref": x} for x in FO] or n["wh"] != {"$ref": "actor"}:
    problems.append("handoff_12 fields differ from the plan")

note = open(NOTE, encoding="utf-8").read()
for path in LISTED_IN_NOTE:
    if sha(path) not in note:
        problems.append(f"note lacks sha256 of {path}")
if STATE == "state.px/state.px" and sha(STATE) in note:
    problems.append("note contains the revision 16 hash, which binds the note's own digest")

# Protected files: byte check for every non-kit entry; kit identity through the manifest.
snapshot_manifest = None
kit_entries = 0
kit_differing = []
for line in open(SNAPSHOT, encoding="utf-8"):
    want, path = line.rstrip("\n").split("  ", 1)
    if "__pycache__" in path:
        continue
    if path.startswith(KIT_PREFIX):
        kit_entries += 1
        if path == MANIFEST:
            snapshot_manifest = want
        try:
            if sha(path) != want:
                kit_differing.append(path)
        except FileNotFoundError:
            kit_differing.append(path + " (missing)")
        continue
    if path in EDITED_ON_PURPOSE:
        continue
    try:
        got = sha(path)
    except FileNotFoundError:
        problems.append(f"snapshot file missing: {path}")
        continue
    if got != want:
        problems.append(f"protected file drifted: {path}")
if snapshot_manifest is None:
    problems.append("snapshot lacks the kit manifest entry")
current_manifest = sha(MANIFEST) if os.path.exists(MANIFEST) else None
readiness = run("readiness", "--root", ".", "--host", "claude", "--installation", "pixl-kit")
manifest_report = readiness.get("installation", {}).get("bundle_manifest", {})
if manifest_report.get("status") != "verified" or manifest_report.get("issues"):
    problems.append(f"kit manifest not verified: {manifest_report}")
if current_manifest and manifest_report.get("sha256") not in (None, current_manifest):
    problems.append("readiness manifest sha256 differs from the measured manifest bytes")
cache_dirs = sorted(os.path.join(dp, d).replace("\\", "/")
                    for dp, dn, _ in os.walk("pixl-kit") for d in dn if d == "__pycache__")
kit_files_now = sum(len(fn) for _, _, fn in os.walk("pixl-kit"))
kit = {
    "manifest_sha256_in_snapshot": snapshot_manifest,
    "manifest_sha256_now": current_manifest,
    "manifest_verification": manifest_report.get("status"),
    "manifest_files_checked": manifest_report.get("files_checked"),
    "kit_entries_in_snapshot": kit_entries,
    "kit_files_now": kit_files_now,
    "kit_changed_since_snapshot": snapshot_manifest != current_manifest,
    "kit_files_differing_from_snapshot": kit_differing,
    "kit_bytecode_cache_dirs": cache_dirs,
}

before = sha("deliverables/sample-request/criteria-schema-validation.json")
subprocess.run([PY, "-B", "-I", "deliverables/sample-request/validate_criteria_v2.py"],
               capture_output=True, text=True, check=True)
if sha("deliverables/sample-request/criteria-schema-validation.json") != before:
    problems.append("validate_criteria_v2.py modified the retained validation artifact")

wf = run("workflow", STATE, "--root", ".")
if wf.get("ready") != ["t_sample"]:
    problems.append(f"ready {wf.get('ready')}")
if not wf.get("files_verified"):
    problems.append("files not verified")
if run("jobs", STATE, "--root", ".").get("jobs"):
    problems.append("unexpected jobs")

print(json.dumps({"state": STATE, "head_sha256": sha(STATE), "canonical_hash": wf.get("hash"),
                  "revision": doc["revision"], "records": len(by), "kit": kit,
                  "problems": problems}, indent=1))
sys.exit(1 if problems else 0)
