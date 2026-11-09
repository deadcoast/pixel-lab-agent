"""Round-2 (artifact-based restart): derive the pixl_plar_save document from the
adopt proposal by applying exactly the caller's three choices, and write a delta
ledger. No PLAR/PX2 write happens here."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PROPOSAL = ROOT / "work/render-recheck-pixl/plar-update-proposal.json"
OUT_DOC = ROOT / "work/render-recheck-pixl/plar-update-saved.json"
OUT_DELTA = ROOT / "work/render-recheck-pixl/plar-saved-delta.json"

EXPECTED_PROPOSAL_SHA = "3865fb6e7a715bf1880346f4017945cf88a9ee3d3e7e238ade1cce523ca7c69a"
U18_NEW = ("Existing vector Start control reused unchanged (sha256 ee2ba2fe...); observed rendered by both "
           "consumers for idle in the representative renderer (work/render-recheck-pixl-01): browser-rasterised "
           "with anti-aliased edges at 1x (28 intermediate pixels) and smooth re-rasterisation at 3x (84).")
U18_RESTORED = "Existing vector Start control to reuse unchanged; inspected as SVG source, not rendered UI."

NEW_EVIDENCE = [
    {
        "path": "work/render-recheck-review/caller-style-decision.json",
        "note": ("Caller scoped style decision under RENDER-STAGE.md lines 4-6: ADOPT the delivered Ready sample "
                 "fc5e43ae... as the family style baseline (edge treatment, stroke weight, fill/colour role, "
                 "margin/footprint, alpha policy only; does not establish other members' silhouettes, motion, "
                 "meaning, non-colour distinction, family continuity, PixelLab quality or production-host display). "
                 "sha256 bcb41bead8a81709f760cd72058e7da94b0a649b3ed93073ee9fac50a47d8f30."),
    },
    {
        "path": "work/render-recheck-caller-01/render.json",
        "note": ("Independent caller renderer-recheck capture (sha256 "
                 "d47c54a20abdff5d59f122d5e97415a9bdd613f696eeb088169608177f6632d9); destination.png a7f8ed81... "
                 "byte-identical to the specialist capture; renderer-recheck/check.py 104/104 "
                 "(work/render-recheck-caller-01-check.json)."),
    },
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


proposal_sha = sha(PROPOSAL)
if proposal_sha != EXPECTED_PROPOSAL_SHA:
    sys.exit(f"proposal hash drift: {proposal_sha}")

doc = json.loads(PROPOSAL.read_text(encoding="utf-8"))
assets = {a["id"]: a for a in doc["assets"]}

# Delta 1: drop U18 (restore queue.start existing[0].role to the live plar.txt text).
start = assets["queue.start"]
if start["existing"][0]["role"] != U18_NEW:
    sys.exit("queue.start existing[0].role does not match the U18 proposal text")
start["existing"][0]["role"] = U18_RESTORED

# Delta 2: append two evidence entries to queue.ready (hash-safe field).
ready = assets["queue.ready"]
before = len(ready["evidence"])
for entry in NEW_EVIDENCE:
    if any(e["path"] == entry["path"] for e in ready["evidence"]):
        sys.exit(f"evidence already present: {entry['path']}")
ready["evidence"].extend(NEW_EVIDENCE)

# U11 kept: assert the queue.working renderer_frame_extraction observation is present and untouched.
working = assets["queue.working"]
rfe = [r for r in working["requirements"] if r["property"] == "renderer_frame_extraction"]
if len(rfe) != 1 or rfe[0]["authority"] != "observation":
    sys.exit("U11 renderer_frame_extraction not present as observation")

OUT_DOC.write_text(dump(doc), encoding="utf-8")

# Structural diff against the proposal, to prove nothing else changed.
orig = json.loads(PROPOSAL.read_text(encoding="utf-8"))


def diff(a, b, path="$", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append({"path": f"{path}.{k}", "change": "added"})
            elif k not in b:
                out.append({"path": f"{path}.{k}", "change": "removed"})
            else:
                diff(a[k], b[k], f"{path}.{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(min(len(a), len(b))):
            diff(a[i], b[i], f"{path}[{i}]", out)
        for i in range(min(len(a), len(b)), len(b)):
            out.append({"path": f"{path}[{i}]", "change": "appended"})
        for i in range(min(len(a), len(b)), len(a)):
            out.append({"path": f"{path}[{i}]", "change": "truncated"})
    elif a != b:
        out.append({"path": path, "change": "modified"})
    return out


delta = {
    "version": 1,
    "role": "Delta ledger: what work/render-recheck-pixl/plar-update-saved.json changes versus the adopt proposal "
            "work/render-recheck-pixl/plar-update-proposal.json. Written by the round-2 PIXL instance "
            "(artifact-based restart; the round-1 instance could not be resumed).",
    "base_proposal": {"path": "work/render-recheck-pixl/plar-update-proposal.json", "sha256": proposal_sha,
                      "variant": "adopt"},
    "saved_document": {"path": "work/render-recheck-pixl/plar-update-saved.json", "sha256": sha(OUT_DOC)},
    "expect_for_save": "71f493b9203f70afe77a4f25c27f4e524a5aa748604a94577bec47b4a97d10de",
    "caller_choices_applied": [
        {
            "id": "D1-drop-U18",
            "ledger_entry": "U18",
            "where": "queue.start",
            "field": "existing[0].role",
            "proposal_value": U18_NEW,
            "saved_value": U18_RESTORED,
            "why": "Caller choice: keep queue.start's requirements_hash d25bb8982e69cb1f0a2fb448893bfa29432f21f498368312e58cbdba26250c42 stable; the renderer observation for Start lives in queue.start evidence (work/render-recheck-pixl-01/render.json) and next (U19), both hash-safe.",
            "hash_covered": True,
        },
        {
            "id": "D2-evidence-caller-decision",
            "ledger_entry": "A01 at_save_time",
            "where": "queue.ready",
            "field": f"evidence[{before}]",
            "saved_value": NEW_EVIDENCE[0],
            "why": "Gives the approved_style_reference 'requirement' authority an addressable owner decision artifact (hash-safe field).",
            "hash_covered": False,
        },
        {
            "id": "D3-evidence-caller-capture",
            "ledger_entry": "new (caller instruction)",
            "where": "queue.ready",
            "field": f"evidence[{before + 1}]",
            "saved_value": NEW_EVIDENCE[1],
            "why": "Link the caller's independent renderer-recheck capture and 104/104 re-check (hash-safe field).",
            "hash_covered": False,
        },
    ],
    "kept_as_proposed": ["U11 (queue.working renderer_frame_extraction unknown -> observation; hash-covered)",
                         "U19 (queue.start next)", "queue.start evidence link to work/render-recheck-pixl-01/render.json",
                         "all other U* and A* entries of the adopt variant"],
    "structural_diff_vs_proposal": diff(orig, doc),
    "expected_requirements_hash_effects": {
        "queue.start": "unchanged d25bb898... (U18 dropped)",
        "queue.ready": "changes (as in the proposal; evidence is excluded from the hash)",
        "queue.working": "changes (U11 + A02/A03)",
        "queue.retry": "changes (A02/A03)",
        "queue.paused": "changes (A02/A03)",
    },
}
OUT_DELTA.write_text(dump(delta), encoding="utf-8")
print(json.dumps({"saved_document_sha256": sha(OUT_DOC), "delta_sha256": sha(OUT_DELTA),
                  "diff": delta["structural_diff_vs_proposal"]}, indent=2))
