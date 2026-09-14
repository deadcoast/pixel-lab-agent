"""Author revision 2: the nominated candidate, its receipts and the retained verdicts.

Evidence bindings are computed from the runtime's own semantic closure so each
receipt binds the exact candidate and criterion scope rather than a guessed list.
"""
import json
import subprocess
import sys
from pathlib import Path

KIT = Path(".agents/skills/pixl-kit").resolve()
sys.path.insert(0, str(KIT / "runtime"))
from pixl import codec  # noqa: E402
from pixl.graph import proof_scope  # noqa: E402

RUNNER = str(KIT / "scripts" / "pixl.py")
AT = "2026-09-11T00:00:00+00:00"

sym = lambda s: {"$symbol": s}
ref = lambda s: {"$ref": s}


def rec(id_, kind, **fields):
    return {"id": id_, "kind": kind, "fields": fields}


def run(*args):
    out = subprocess.run([sys.executable, RUNNER, *args], capture_output=True, text=True)
    if out.returncode:
        print("FAILED:", args, out.stdout, out.stderr)
        sys.exit(1)
    return out.stdout


base = json.load(open("pixl-state/rev1.json"))
records = {r["id"]: r for r in base["records"]}

candidate = rec(
    "x-candidate-1", "X",
    nm="Generated robot sample nominated as family baseline",
    ur="candidate.png",
    dg="d28f90f619400f8a770741b23bb5c1da995e6b6dd017ebab30eac934892c8d8d",
    ct=ref("contract"), kd=sym("sprite"), of=ref("f-baseline"),
)
handoff_report = rec(
    "x-handoff-1", "X",
    nm="Baseline review decision and next step",
    ur="pixl-state/handoff.md",
    dg="d523ad36f8358f84afd76f0d05c001db9e31a5c81cc1b16fc0646fbbdd93b195", kd=sym("report"),
)
records[candidate["id"]] = candidate
records[handoff_report["id"]] = handoff_report

# Resolve the semantic closures from a draft that carries every semantic record.
draft = {"revision": 2, "records": list(records.values()), "format": 2}
Path("pixl-state/rev2-draft.json").write_text(json.dumps(draft, indent=2))
draft_px = run("encode", "pixl-state/rev2-draft.json")
doc = codec.parse(draft_px)

def bind(*ids):
    scope = set()
    for id_ in ids:
        scope |= proof_scope(doc, [id_])
    return [
        {"rf": ref(i), "dg": codec.record_hash(doc.records[i])}
        for i in sorted(scope)
    ]

mechanical_note = (
    "pixl_asset_check plus a local Pillow measurement of candidate.png: 32x32, 366 visible "
    "pixels in exactly the three confirmed palette colours (#56B5BC 198, #25354A 156, "
    "#F4DDA2 12), zero fractional-alpha pixels, one connected opaque component, no colour "
    "outside the palette."
)
visual_note = (
    "Enlarged 12x three-panel comparison (reference | candidate | per-pixel difference) was "
    "inspected directly. The candidate drops two identity features that reference.png has:\n"
    "1. The left head antenna is gone: 24 outline pixels at x7-10, y3-8 are #25354A in the "
    "reference and fully transparent in the candidate. The candidate reads as a one-antenna "
    "robot.\n"
    "2. The right eye is gone: 12 accent pixels at x18-20, y14-17 are #F4DDA2 in the reference "
    "and repainted body teal #56B5BC in the candidate. The candidate reads as one-eyed.\n"
    "Only 36 of 1024 pixels differ and no pixel was added, so every mechanical measurement "
    "still passes. Mirror-test about the sprite centre: the reference's head and face are "
    "symmetric, the candidate's are not."
)

records["e-mech-1"] = rec(
    "e-mech-1", "E", nm="Candidate mechanical measurement",
    ur="pixl-state/evidence/candidate-mechanical.json",
    dg="3847c6ce75034523d38b3cf5b06b3e4a045e551d1da153e64351b7f329926bd8",
    rs=sym("pass"), md=sym("local"), at=AT,
    bs=bind("x-candidate-1", "q-mechanical"),
)
records["e-visual-1"] = rec(
    "e-visual-1", "E", nm="Enlarged candidate/reference visual comparison",
    ur="pixl-state/evidence/candidate-vs-reference.png",
    dg="dc516830241fa5ecd90b296afa80cec1d04da7b7f6e30f3efd9bfeabe4bdc06e",
    rs=sym("fail"), md=sym("visual"), at=AT,
    bs=bind("x-candidate-1", "q-identity", "q-baseline-fitness"),
)

records["v-mech-1"] = rec(
    "v-mech-1", "V", tk=ref("t-sample"), rq=ref("q-mechanical"), xr=ref("x-candidate-1"),
    st=sym("pass"), wh=ref("actor"), at=AT, ev=[ref("e-mech-1")],
    wy="Canvas, palette, binary alpha and single-component silhouette all conform. " + mechanical_note,
)
records["v-identity-1"] = rec(
    "v-identity-1", "V", tk=ref("t-sample"), rq=ref("q-identity"), xr=ref("x-candidate-1"),
    st=sym("fail"), wh=ref("actor"), at=AT, ev=[ref("e-visual-1")],
    wy="Rejected on identity. " + visual_note,
)
records["v-fitness-1"] = rec(
    "v-fitness-1", "V", tk=ref("t-sample"), rq=ref("q-baseline-fitness"), xr=ref("x-candidate-1"),
    st=sym("fail"), wh=ref("actor"), at=AT, ev=[ref("e-visual-1")],
    wy=("Not fit as the family baseline. The two missing features are dropped elements rather "
        "than a deliberate design, and a baseline propagates: every sibling robot derived from "
        "it would inherit the missing antenna and missing eye, and the error would then look "
        "like the family's intended identity rather than a defect. Mechanical conformance is "
        "exactly why this needed a visual check: dimensions and palette cannot detect it."),
)

records["t-sample"]["fields"]["ca"] = [ref("x-candidate-1")]
records["t-sample"]["fields"]["vr"] = [ref("v-mech-1"), ref("v-identity-1"), ref("v-fitness-1")]
records["t-sample"]["fields"]["st"] = sym("active")

records["handoff"] = rec(
    "handoff", "N", wh=ref("actor"),
    fo=[ref("x-candidate-1"), ref("x-reference"), ref("v-identity-1"),
        ref("v-fitness-1"), ref("x-handoff-1"), ref("i-destination")],
    nx=[ref("t-sample")], bl=[], rv=2,
)

final = {"revision": 2, "records": list(records.values()), "format": 2}
Path("pixl-state/rev2.json").write_text(json.dumps(final, indent=2))
print("draft built; fill handoff.md then re-run with FINAL=1")
