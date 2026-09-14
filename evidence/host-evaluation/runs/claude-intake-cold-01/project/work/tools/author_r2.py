"""Author PX2 revision 2: study receipts, verdicts, task completion, handoff.

Reads the committed revision-1 state, appends the two E receipts and the two V
verdicts for the edge study, closes `study_edges`, and records a handoff.
Writes work/state/candidate-r2.json. Encode and commit are separate steps.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / ".agents" / "skills" / "pixl-kit"
sys.path.insert(0, str(KIT / "runtime"))

from pixl import codec  # noqa: E402

AT = "2026-09-11T00:00:00+00:00"
OUT = ROOT / "work" / "state"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def ref(i):
    return {"$ref": i}


def sym(s):
    return {"$symbol": s}


doc = codec.parse((ROOT / "state.px" / "state.px").read_bytes())
hashes = {id_: codec.record_hash(r) for id_, r in doc.records.items()}


def binding(*ids):
    return [{"rf": ref(i), "dg": hashes[i]} for i in ids]


# The candidate's semantic closure plus both criteria closures, plus the two
# reference images the checks actually recompute from.
SCOPE = ("x_study", "edge_study", "q_study_repro", "q_study_decidable",
         "actor", "brief", "measure", "kmethods", "ref_a", "ref_b")

added = [
    {"id": "e_study_repro", "kind": "E", "fields": {
        "nm": "Independent recomputation of every study measurement",
        "ur": "work/evidence/repro-check.json",
        "dg": sha("work/evidence/repro-check.json"),
        "rs": sym("pass"), "md": sym("local"), "at": AT,
        "bs": binding(*SCOPE)}},
    {"id": "e_study_decide", "kind": "E", "fields": {
        "nm": "Agent visual inspection of the contact sheet and dark-ground crop",
        "ur": "work/evidence/decidability-inspection.md",
        "dg": sha("work/evidence/decidability-inspection.md"),
        "rs": sym("pass"), "md": sym("visual"), "at": AT,
        "bs": binding(*SCOPE)}},
    {"id": "v_study_repro", "kind": "V", "fields": {
        "tk": ref("study_edges"), "rq": ref("q_study_repro"),
        "xr": ref("x_study"), "st": sym("pass"), "wh": ref("actor"), "at": AT,
        "wy": "Re-ran work/tools/edge_study.py: measurement.json, the contact "
              "sheet and all three variant PNGs regenerate byte-identically "
              "from the two supplied references. work/tools/verify_study.py "
              "then recomputed 34 claims from the PNGs alone, independently of "
              "measurement.json, and matched each against the literal report "
              "text: 34 pass, 0 fail, including both input digests, the 390-cell "
              "silhouette, the 180 differing pixels and the 92/82/58 ring depth "
              "profile.",
        "ev": [ref("e_study_repro")]}},
    {"id": "v_study_decide", "kind": "V", "fields": {
        "tk": ref("study_edges"), "rq": ref("q_study_decidable"),
        "xr": ref("x_study"), "st": sym("pass"), "wh": ref("actor"), "at": AT,
        "wy": "Viewed the contact sheet and the dark-ground crop as images. All "
              "three treatments appear on light, dark and busy grounds at native "
              "scale, x4 and x8; the report names a weakest cell per treatment "
              "and those cells are the ones that actually look weakest. The "
              "sheet carries no printed row labels, so it is decidable beside "
              "the report rather than alone: recorded as a limitation, not a "
              "failure. This does not choose edge_treatment.",
        "ev": [ref("e_study_decide")]}},
    {"id": "n_r2", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": [ref("ch_edges"), ref("ch_canvas"), ref("ch_scale"),
               ref("ch_engine"), ref("ch_light")],
        "nx": [ref("sample_scout")],
        "bl": [ref("sample_scout"), ref("make_medic"), ref("deliver_family")],
        "rv": 2}},
]

records = []
for id_, record in doc.records.items():
    fields = codec.to_data(record.fields)
    if id_ == "study_edges":
        fields["st"] = sym("done")
        fields["vr"] = [ref("v_study_repro"), ref("v_study_decide")]
    records.append({"id": id_, "kind": record.kind, "fields": fields})
records.extend(added)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "candidate-r2.json").write_text(
    json.dumps({"revision": 2, "format": 2, "records": records}, indent=2) + "\n",
    encoding="utf-8")
print("wrote", OUT / "candidate-r2.json", len(records), "records")
