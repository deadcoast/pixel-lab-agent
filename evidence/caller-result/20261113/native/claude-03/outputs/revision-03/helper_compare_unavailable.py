"""Parent scratch: compare the host MCP pixl_source error (saved verbatim as returned, host-unavailable-return.json),
the maintainer helper's frozen-kit capture (errors/unavailable-observation.json + raw protocol) and the prior flawed
report (../errors/unavailable-observation.json). No path or string normalization; exact JSON value equality."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[3]; r3 = root / "work/compact-caller/revision-03"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
host = json.loads((r3 / "host-unavailable-return.json").read_text("utf-8"))
saved = json.loads((r3 / "errors/unavailable-observation.json").read_text("utf-8"))
proto = [json.loads(l) for l in (r3 / "unavailable-protocol.jsonl").read_text("utf-8").splitlines() if l.strip()]
proto_res = next(x for x in proto if x.get("id") == 2)["result"]
prior = json.loads((root / "work/compact-caller/errors/unavailable-observation.json").read_text("utf-8"))["original_error"]
out = {
 "comparison": "exact JSON value equality, no normalization",
 "host_return_equals_saved_structuredContent": host == saved["structuredContent"],
 "saved_text_block_parses_to_structuredContent": json.loads(saved["content"][0]["text"]) == saved["structuredContent"],
 "raw_protocol_result_equals_saved": proto_res == saved,
 "saved_isError": saved["isError"],
 "prior_report_equals_native": prior == host,
 "prior_report_differs_only_in_detail": {k: (prior.get(k) == host.get(k)) for k in host},
 "native_detail": host["detail"],
 "prior_report_detail": prior["detail"],
 "native_detail_backslash_count": host["detail"].count("\\"),
 "prior_detail_backslash_count": prior["detail"].count("\\"),
 "defect": "Prior errors/unavailable-observation.json collapsed the doubled literal backslashes in detail (exact-error-retention defect, not an artistic failure). Prior file preserved unchanged.",
 "missing_file_still_absent": not (root / "work/compact-caller/intentionally-missing.txt").exists(),
 "files": {p: sha(root / p) for p in ["work/compact-caller/revision-03/host-unavailable-return.json","work/compact-caller/revision-03/errors/unavailable-observation.json","work/compact-caller/revision-03/unavailable-protocol.jsonl","work/compact-caller/revision-03/capture-unavailable-stdout.json","work/compact-caller/errors/unavailable-observation.json","work/compact-caller/revision-03-inputs/capture_unavailable.py"]},
 "helper_provenance": "work/compact-caller/revision-03-inputs/capture_unavailable.py is maintainer-provided correction input, run unmodified with the frozen runtime -B."
}
t = r3 / "unavailable-comparison.json"
if t.exists(): raise SystemExit("exists")
t.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8"); print(json.dumps(out, indent=1, ensure_ascii=False))
