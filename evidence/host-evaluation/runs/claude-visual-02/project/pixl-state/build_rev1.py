"""Author revision 1: intake choices, contract, sample task, planned output and criteria.

No verdict is published here. PX2 requires the plan and its full semantic scope to
exist unchanged in the saved state that immediately precedes any pass/fail verdict.
"""
import json
import subprocess
import sys

RUNNER = ".agents/skills/pixl-kit/scripts/pixl.py"
STORE = "pixl-state"
AT = "2026-09-11T00:00:00+00:00"
PALETTE = ["#25354A", "#56B5BC", "#F4DDA2"]

sym = lambda s: {"$symbol": s}
ref = lambda s: {"$ref": s}


def rec(id_, kind, **fields):
    return {"id": id_, "kind": kind, "fields": fields}


records = [
    rec("actor", "A", nm="PIXL", rl=sym("agent")),
    rec("user", "A", nm="Project owner", rl=sym("user")),

    rec("s-assignment", "S",
        ur="pixl-state/sources/assignment.md",
        dg="8669aaabd4383d1634c764457ddf3a7bf61d3de757020ca502f36c7fa19916fc",
        ln=[], at=AT, au=sym("local")),
    rec("s-reference", "S",
        ur="reference.png",
        dg="d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7",
        ln=[], at=AT, au=sym("local")),

    rec("i-canvas", "I", pr=ref("project"), wh=ref("user"), ky="px",
        st=sym("confirmed"), vl=[32, 32], so=[ref("s-assignment"), ref("s-reference")],
        wy="The user states the 32 by 32 canvas is already correct; reference.png measures 32x32."),
    rec("i-palette", "I", pr=ref("project"), wh=ref("user"), ky="pl",
        st=sym("confirmed"), vl=PALETTE, so=[ref("s-assignment"), ref("s-reference")],
        wy="The user states the reference palette is already correct. These are the three "
           "visible colours measured in reference.png: outline, body and accent."),
    rec("i-alpha", "I", pr=ref("project"), wh=ref("user"), ky="al",
        st=sym("confirmed"), vl=sym("binary"), so=[ref("s-reference")],
        wy="reference.png has zero fractional-alpha pixels; the family is fully binary-alpha."),
    rec("i-view", "I", pr=ref("project"), wh=ref("user"), ky="vw",
        st=sym("confirmed"), vl=sym("side"), so=[ref("s-reference")],
        wy="reference.png reads as a flat front/side-facing robot bust, not a projected view."),
    rec("i-identity", "I", pr=ref("project"), wh=ref("user"), ky="identity_reference",
        st=sym("confirmed"), vl="reference.png", so=[ref("s-assignment"), ref("s-reference")],
        wy="The user names reference.png as the agreed identity, so it is the authority for "
           "the family's silhouette and face features, not merely an earlier asset."),
    rec("i-identity-features", "I", pr=ref("project"), wh=ref("agent_placeholder"), ky="identity_features",
        st=sym("observed"), vl=["two head antennae", "two eyes", "bilateral symmetry about the sprite centre"],
        so=[ref("s-reference")],
        wy="Measured from reference.png: outline antennae at x7-10 and x21-24 over y3-8, and accent "
           "eyes at x11-13 and x18-20 over y14-17. Recorded as observed, not user-confirmed wording."),
    rec("i-destination", "I", pr=ref("project"), wh=ref("user"), ky="family_destination",
        st=sym("unresolved"), vl=None, so=[],
        wy="The target engine or import destination for the robot family was never stated. "
           "It must be confirmed before any delivery task, and it does not block this sample review."),

    rec("contract", "C", nm="Robot family 32px sprite", px=[32, 32], pl=PALETTE,
        vw=sym("side"), sa=sym("nearest"), al=sym("binary"),
        li="Three-colour robot: dark outline, teal body plate, warm accent for lit features. "
           "Hard pixel edges, no anti-aliasing, single connected silhouette.",
        ch=[ref("i-canvas"), ref("i-palette"), ref("i-view"), ref("i-alpha")]),

    rec("x-reference", "X", nm="Agreed robot identity reference", ur="reference.png",
        dg="d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7",
        ct=ref("contract"), kd=sym("reference")),

    rec("q-mechanical", "Q", nm="Mechanical contract conformance", dm=sym("mechanical"),
        md=sym("local"), wh=ref("actor"), so=[ref("s-assignment")],
        ck="32x32 RGBA; every visible pixel is one of #25354A, #56B5BC or #F4DDA2; zero "
           "fractional-alpha pixels; exactly one connected opaque component."),
    rec("q-identity", "Q", nm="Identity fidelity to reference.png", dm=sym("visual"),
        md=sym("visual"), wh=ref("actor"), so=[ref("s-reference"), ref("s-assignment")],
        ck="Inspected enlarged beside reference.png, the candidate carries the agreed identity: "
           "both head antennae present, both eyes present, and the silhouette bilaterally "
           "symmetric about the sprite centre as in the reference. A feature the reference has "
           "and the candidate drops is a failure even when colours and dimensions match."),
    rec("q-baseline-fitness", "Q", nm="Fitness as the family baseline", dm=sym("other"),
        md=sym("visual"), wh=ref("actor"), so=[ref("s-assignment")],
        ck="The sprite is a sound starting point to derive sibling robots from: its identity "
           "features are the reference's, and any asymmetry present is a deliberate design "
           "feature rather than a dropped element that siblings would inherit."),

    rec("f-baseline", "F", tk=ref("t-sample"), nm="Robot family baseline sprite",
        kd=sym("sprite"), rq=[ref("q-mechanical"), ref("q-identity"), ref("q-baseline-fitness")],
        ct=ref("contract")),

    rec("t-sample", "T", nm="Review candidate.png for the robot family baseline role",
        ow=ref("actor"), pr=ref("project"), dp=[], dc=[], kn=[], st=sym("active"),
        ph=sym("sample"), ip=[ref("x-reference")], op=[ref("f-baseline")], ca=[], vr=[]),

    rec("project", "P", nm="Robot family baseline review", ow=ref("user"),
        sc=[ref("s-assignment"), ref("s-reference")],
        in_=None),
]

# P.in is a reserved Python word in kwargs; patch it in directly.
for r in records:
    if r["id"] == "project":
        del r["fields"]["in_"]
        r["fields"]["in"] = [ref(i) for i in (
            "i-canvas", "i-palette", "i-alpha", "i-view", "i-identity",
            "i-identity-features", "i-destination")]
        r["fields"]["br"] = (
            "Evaluate whether candidate.png is ready to become the baseline sprite for the rest "
            "of the robot family. The agreed visual identity is reference.png. Inputs are 32x32 "
            "RGBA sprites in the project root.")

# i-identity-features is an agent observation, not a user choice.
for r in records:
    if r["id"] == "i-identity-features":
        r["fields"]["wh"] = ref("actor")

doc = {"revision": 1, "records": records, "format": 2}
json.dump(doc, open("pixl-state/rev1.json", "w"), indent=2)

def run(*args):
    out = subprocess.run([sys.executable, RUNNER, *args], capture_output=True, text=True)
    if out.returncode:
        print("FAILED:", args[0], out.stdout, out.stderr)
        sys.exit(1)
    return out.stdout

open("pixl-state/rev1.px", "w", newline="").write(run("encode", "pixl-state/rev1.json"))
print(run("validate", "pixl-state/rev1.px", "--root", "."))
