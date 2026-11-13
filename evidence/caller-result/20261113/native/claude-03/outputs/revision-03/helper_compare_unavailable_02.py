"""Parent scratch (second attempt): compare the host MCP pixl_source error, saved via the Write tool as returned
(host-unavailable-return-02.json), with the maintainer helper's frozen-kit capture (errors/unavailable-observation.json
+ raw protocol) and the prior flawed report (../errors/unavailable-observation.json). Exact JSON value equality only.

The first attempt (host-unavailable-return.json, unavailable-comparison.json, helper_compare_unavailable.py) is retained
as a historical failure: that host copy was written through a Bash heredoc and the shell layer halved the doubled
literal backslashes, reproducing the same collapse defect as the prior report and yielding a wrong equality verdict."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
r3 = root / "work/compact-caller/revision-03"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


host = json.loads((r3 / "host-unavailable-return-02.json").read_text("utf-8"))
host_flawed = json.loads((r3 / "host-unavailable-return.json").read_text("utf-8"))
saved = json.loads((r3 / "errors/unavailable-observation.json").read_text("utf-8"))
native = saved["structuredContent"]
proto = [json.loads(l) for l in (r3 / "unavailable-protocol.jsonl").read_text("utf-8").splitlines() if l.strip()]
proto_res = next(x for x in proto if x.get("id") == 2)["result"]
prior = json.loads((root / "work/compact-caller/errors/unavailable-observation.json").read_text("utf-8"))["original_error"]
sep = chr(92)
out = {
    "comparison": "exact JSON value equality, no path or string normalization",
    "host_return_equals_native_structuredContent": host == native,
    "saved_text_block_parses_to_structuredContent": json.loads(saved["content"][0]["text"]) == native,
    "raw_protocol_result_equals_saved_file": proto_res == saved,
    "saved_isError": saved["isError"],
    "prior_report_equals_native": prior == native,
    "prior_report_field_equality_vs_native": {k: (prior.get(k) == native.get(k)) for k in native},
    "native_detail_backslash_count": native["detail"].count(sep),
    "prior_report_detail_backslash_count": prior["detail"].count(sep),
    "host_return_02_backslash_count": host["detail"].count(sep),
    "first_attempt_host_copy_backslash_count": host_flawed["detail"].count(sep),
    "first_attempt_host_copy_equals_prior_flawed": host_flawed == prior,
    "defects": [
        "Prior work/compact-caller/errors/unavailable-observation.json collapsed the doubled literal Windows backslashes in original_error.detail (10 instead of 20). Exact-error-retention defect, not an artistic failure. File preserved unchanged.",
        "Root cause reproduced in revision-03/host-unavailable-return.json and unavailable-comparison.json: writing JSON through a Bash heredoc in this host halves backslash runs. Those first-attempt files are preserved as historical failures; this second attempt used the Write tool and the maintainer helper's raw protocol capture.",
    ],
    "missing_file_still_absent": not (root / "work/compact-caller/intentionally-missing.txt").exists(),
    "files": {p: sha(root / p) for p in [
        "work/compact-caller/revision-03/host-unavailable-return-02.json",
        "work/compact-caller/revision-03/host-unavailable-return.json",
        "work/compact-caller/revision-03/unavailable-comparison.json",
        "work/compact-caller/revision-03/errors/unavailable-observation.json",
        "work/compact-caller/revision-03/unavailable-protocol.jsonl",
        "work/compact-caller/revision-03/capture-unavailable-stdout.json",
        "work/compact-caller/errors/unavailable-observation.json",
        "work/compact-caller/revision-03-inputs/capture_unavailable.py",
    ]},
    "helper_provenance": "work/compact-caller/revision-03-inputs/capture_unavailable.py is maintainer-provided correction input, run unmodified with the frozen runtime -B; not authored by the parent.",
}
t = r3 / "unavailable-comparison-02.json"
if t.exists():
    raise SystemExit("exists")
t.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(out, indent=1, ensure_ascii=False))
