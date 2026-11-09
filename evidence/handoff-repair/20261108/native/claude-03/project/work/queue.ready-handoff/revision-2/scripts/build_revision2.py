"""Build the revision-2 corrected-proposal artifacts from the retained revision-1 files.

Revision 1 (work/queue.ready-handoff/*.json) is read only and kept byte-for-byte.
Revision 2 changes exactly:
  1. request-review.json  sources[OWNER.md].locators: 'lines 8-9' -> 'lines 8-10' (caller finding 1),
     criteria.path/sha256 and criteria.changes -> revision-2 files, a new 'revision' block,
     review_status updated for the performed caller comparison of revision 1,
     plar.hash_at_authoring -> the plar.txt hash current while authoring revision 2.
  2. candidate-plan.json  only criterion ready-meaning.basis is clarified (caller finding 2).
  3. candidate-plan-changes.json  corrected_plan re-pointed; 'revision_2' section appended.
Nothing else is edited; no PX2 state, verdict or provider action is involved.
"""
import copy
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(r"C:\github\pixel-lab-agent\evidence\handoff-repair\20261108\native\claude-03\project")
REV1 = ROOT / "work" / "queue.ready-handoff"
REV2 = REV1 / "revision-2"
SCHEMA = ROOT / ".agents" / "skills" / "pixl-kit" / "runtime" / "pixl" / "asset-plan.schema.json"

REV1_PACKET_SHA = "14eb7e3eb53a78e4393425fcd800b5355935adb1c5880e06ee2d1978befc47e9"
REV1_PLAN_SHA = "a22f704dfd4432f2750cfacb7a37efda98925d1da40830981cb07da3a88baa3f"
REV1_CHANGES_SHA = "a4629aa44561944a1e929232b4ea8b564f1ffacd7e6b931eb1cd422bf5ece40c"
PLAR_HASH_NOW = "0ede0be80131e8c4b071fe06fb4318d69148a4f80282d3b95c49f9f3e377df20"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: pathlib.Path, expect: str):
    actual = sha(p)
    assert actual == expect, f"{p} changed: {actual} != {expect}"
    return json.loads(p.read_text(encoding="utf-8"))


def dump(p: pathlib.Path, doc) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return sha(p)


# plar.txt must still be the hash the caller verified; revision 2 records it as hash_at_authoring.
assert sha(ROOT / "plar.txt") == PLAR_HASH_NOW, "plar.txt changed since the caller's verification"

# ---------------------------------------------------------------- candidate-plan.json (revision 2)
plan = load(REV1 / "candidate-plan.json", REV1_PLAN_SHA)
plan2 = copy.deepcopy(plan)
crit = next(c for c in plan2["outputs"][0]["criteria"] if c["id"] == "ready-meaning")
OLD_BASIS_HEAD = (
    "BRIEF.md line 9 is the owner requirement for the check-mark motif, the asymmetrical arms "
    "and the successful-completion meaning. "
)
assert crit["basis"].startswith(OLD_BASIS_HEAD)
CLARIFICATION = (
    "The parenthetical 'one arm clearly shorter than the other' in the check is the specialist's "
    "reading of the owner's term 'asymmetrical arms', not additional owner wording: asymmetry is "
    "read as unequal arm length, which is the conventional check-mark form (a short stroke meeting "
    "a longer stroke at a low vertex). A V shape with equal-length arms distinguished only by unequal "
    "stroke weight is not what 'check mark' names, so this reading excludes no brief-conforming check "
    "mark. No arm ratio is imposed; any clearly unequal pair of arm lengths satisfies the clause. "
)
crit["basis"] = OLD_BASIS_HEAD + CLARIFICATION + crit["basis"][len(OLD_BASIS_HEAD):]
# Guard: only the basis of ready-meaning changed.
diff_paths = []
for c1, c2 in zip(plan["outputs"][0]["criteria"], plan2["outputs"][0]["criteria"]):
    for k in c1:
        if c1[k] != c2[k]:
            diff_paths.append((c1["id"], k))
assert diff_paths == [("ready-meaning", "basis")], diff_paths
assert {k: v for k, v in plan.items() if k != "outputs"} == {k: v for k, v in plan2.items() if k != "outputs"}
assert plan["outputs"][0]["contract"] == plan2["outputs"][0]["contract"]

import jsonschema  # noqa: E402  (bundled requirement; validates the corrected plan)

jsonschema.validate(plan2, json.loads(SCHEMA.read_text(encoding="utf-8")))
plan2_sha = dump(REV2 / "candidate-plan.json", plan2)
print("revision-2/candidate-plan.json", plan2_sha)

# ---------------------------------------------------------------- candidate-plan-changes.json (revision 2)
changes = load(REV1 / "candidate-plan-changes.json", REV1_CHANGES_SHA)
changes2 = copy.deepcopy(changes)
changes2["corrected_plan"] = {
    "path": "work/queue.ready-handoff/revision-2/candidate-plan.json",
    "sha256": plan2_sha,
    "supersedes": {
        "path": "work/queue.ready-handoff/candidate-plan.json",
        "sha256": REV1_PLAN_SHA,
        "note": "Revision-1 corrected plan; retained byte-for-byte. Differs from revision 2 only in the ready-meaning basis.",
    },
}
changes2["revision_2"] = {
    "supersedes": {
        "path": "work/queue.ready-handoff/candidate-plan-changes.json",
        "sha256": REV1_CHANGES_SHA,
    },
    "trigger": "Independent caller comparison of the revision-1 packet (14eb7e3e...) returned two findings; this revision resolves both. Neither finding changes any check text, authority, scope or source pointer in the plan.",
    "criterion_changes": [
        {
            "id": "ready-meaning",
            "field": "basis",
            "old_check": crit["check"],
            "new_check": "unchanged",
            "old_basis": plan["outputs"][0]["criteria"][2]["basis"],
            "new_basis": crit["basis"],
            "caller_finding": "The check adds '(one arm clearly shorter than the other)' to the owner's phrase 'asymmetrical arms' (BRIEF.md line 9). The caller accepts this as the plain reading of a check mark but requires the basis to say explicitly that it is the specialist's reading of the owner's term, that an equal-arm V with unequal stroke weight is not what 'check mark' names, and that no arm ratio is imposed.",
            "source_obligation": "BRIEF.md line 9: 'Ready must visibly use a check mark with asymmetrical arms to convey successful completion.' The owner names the motif (check mark) and the asymmetry; the owner does not define asymmetry or fix a ratio.",
            "literal_additions": "None to the check. The basis now states who supplied the parenthetical (the specialist), what reading it encodes (unequal arm length, the conventional check-mark form), what it does not exclude (any brief-conforming check mark) and what it does not impose (an arm ratio).",
            "discriminating_alternative": "A V shape whose two arms are equal in length and differ only in stroke weight. It is not rejected by the asymmetry parenthetical as an excluded check mark; it is not a check mark in the first place, because 'check mark' names the short-stroke/long-stroke form. Every check mark with clearly unequal arm lengths, of any ratio, stroke width, cap or backing, passes.",
            "disposition": "Clarify the basis only; keep the check text, authority (requirement), scope and the five source pointers identical to revision 1.",
            "effect_on_delivered_candidate": "None. Historical verdict ready.delivery.review.verdict.2 stands under the historical text; no new verdict is recorded.",
        }
    ],
    "packet_changes_noted": [
        "request-review.json sources[OWNER.md].locators: 'lines 8-9: ... integration and art acceptance remain future work' corrected to 'lines 8-10'. OWNER.md line 8 ends at 'the accepted revised request:', line 9 carries 'no image or renderer is supplied, no style is already approved, and integration and', and the clause 'art acceptance remain future work' is on line 10. The paraphrase was right; its stated bound was one line short (caller finding 1).",
        "Every other string locator in request-review.json sources[] (BRIEF.md 3/5/7/9; SOURCE-MAP.md 3; src/queue.ts 1, 3; src/queue-view.ts 3, 6, 9, 10-11; assets/start.svg 1; provider-schemas.json 2-33, 34-42; provider-contract-origin.json 4; OWNER.md 2-11, 7; STAGE.md 2-6, 7-8, 10-11, 13-14; PHASE.md 2-6, 7, 10-11; work/queue.ready-revision/connection.json 2, 50) was re-opened against the file and found to sit inside its stated inclusive bounds. No other correction was needed.",
    ],
    "unchanged": "All six criterion IDs, every check text, authority label, scope and sources[].lines are identical to revision 1. The revision-1 per-criterion comparisons above remain the old-to-new record against the historical plan.",
}
changes2["not_done"] = changes["not_done"] + [
    "Revision 2 adds no verdict, no state commit and no generation; it only clarifies one basis and corrects one packet locator bound.",
]
changes2_sha = dump(REV2 / "candidate-plan-changes.json", changes2)
print("revision-2/candidate-plan-changes.json", changes2_sha)

# ---------------------------------------------------------------- request-review.json (revision 2)
packet = load(REV1 / "request-review.json", REV1_PACKET_SHA)
packet2 = copy.deepcopy(packet)

owner = next(s for s in packet2["sources"] if s["path"] == "OWNER.md")
OLD_LOC = "lines 8-9: deliverable ends at the accepted revised request; no image or renderer supplied; integration and art acceptance remain future work"
NEW_LOC = "lines 8-10: deliverable ends at the accepted revised request; no image or renderer supplied; integration and art acceptance remain future work"
assert OLD_LOC in owner["locators"]
owner["locators"][owner["locators"].index(OLD_LOC)] = NEW_LOC

packet2["plar"]["hash_at_authoring"] = PLAR_HASH_NOW
packet2["criteria"]["path"] = "work/queue.ready-handoff/revision-2/candidate-plan.json"
packet2["criteria"]["sha256"] = plan2_sha
packet2["criteria"]["changes"]["path"] = "work/queue.ready-handoff/revision-2/candidate-plan-changes.json"
packet2["criteria"]["changes"]["sha256"] = changes2_sha
packet2["criteria"]["changes"]["note"] = (
    packet2["criteria"]["changes"]["note"]
    + " Revision 2 appends a 'revision_2' section for the ready-meaning basis clarification and the OWNER.md locator fix."
)
packet2["review_status"] = {
    "specialist_self_review": packet["review_status"]["specialist_self_review"]
    + " Revision 2: every sources[] string locator re-opened against its file; one bound (OWNER.md) corrected; ready-meaning basis made explicit about the specialist's reading of 'asymmetrical arms'.",
    "independent_caller_review": (
        "Performed on revision 1 (packet 14eb7e3e...) by the calling agent, which returned two findings: "
        "(1) OWNER.md locator 'lines 8-9' overreached its bound by one line; (2) the ready-meaning basis must "
        "state explicitly that '(one arm clearly shorter than the other)' is the specialist's reading of "
        "'asymmetrical arms', that an equal-arm V with unequal stroke weight is not a check mark, and that no "
        "arm ratio is imposed. Both are resolved in this revision. The caller accepted the remaining five "
        "criteria and the cool-blue-accent demotion as consistent. The caller's comparison of this revision-2 "
        "packet is pending; its review file is expected at work/queue.ready-handoff/caller-review.json."
    ),
}

revision_block = {
    "number": 2,
    "supersedes": {
        "path": "work/queue.ready-handoff/request-review.json",
        "sha256": REV1_PACKET_SHA,
    },
    "changes": [
        {
            "field": "sources[path=OWNER.md].locators[2]",
            "old": OLD_LOC,
            "new": NEW_LOC,
            "why": "Caller finding 1 (citation defect). OWNER.md line 8 = 'attempts and contracts. The assigned deliverable ends at the accepted revised request:'; line 9 = 'no image or renderer is supplied, no style is already approved, and integration and'; line 10 = 'art acceptance remain future work. Do not fabricate images, provider observations,'. The paraphrased clause 'art acceptance remain future work' is on line 10, outside the stated 8-9 bound. The bound is widened to the file-local inclusive range 8-10 that actually contains the cited text.",
        },
        {
            "field": "sources[] (all other string locators)",
            "old": "as revision 1",
            "new": "unchanged",
            "why": "Re-verified against the files in this revision: BRIEF.md lines 3, 5, 7, 9; SOURCE-MAP.md line 3; src/queue.ts lines 1 and 3; src/queue-view.ts lines 3, 6, 9 and 10-11; assets/start.svg line 1; provider-schemas.json lines 2-33 and 34-42; provider-contract-origin.json line 4; OWNER.md lines 2-11 and 7; STAGE.md lines 2-6, 7-8, 10-11 and 13-14; PHASE.md lines 2-6, 7 and 10-11; work/queue.ready-revision/connection.json lines 2 and 50. Each paraphrase sits inside its stated bound; no other overreach found.",
        },
        {
            "field": "criteria.path / criteria.sha256",
            "old": "work/queue.ready-handoff/candidate-plan.json " + REV1_PLAN_SHA,
            "new": "work/queue.ready-handoff/revision-2/candidate-plan.json " + plan2_sha,
            "why": "Caller finding 2 (basis clarification). Only criterion ready-meaning.basis changed: it now states that '(one arm clearly shorter than the other)' is the specialist's reading of the owner's term 'asymmetrical arms' (asymmetry read as unequal arm length, the conventional check-mark form), that a V with equal arms and unequal stroke weight is not what 'check mark' names, and that no arm ratio is imposed. Check text, authority, scope and sources are identical to revision 1; the plan remains valid against asset-plan.schema.json.",
        },
        {
            "field": "criteria.changes",
            "old": "work/queue.ready-handoff/candidate-plan-changes.json " + REV1_CHANGES_SHA,
            "new": "work/queue.ready-handoff/revision-2/candidate-plan-changes.json " + changes2_sha,
            "why": "The change log gains a 'revision_2' section describing the basis clarification and noting the OWNER.md locator fix; corrected_plan now points at the revision-2 plan with its sha256.",
        },
        {
            "field": "review_status",
            "old": "independent_caller_review: unperformed",
            "new": "performed on revision 1 with two findings (both resolved here); comparison of revision 2 pending",
            "why": "Records the actual review state so the packet does not claim the caller comparison is still unperformed.",
        },
        {
            "field": "plar.hash_at_authoring",
            "old": packet["plar"]["hash_at_authoring"],
            "new": PLAR_HASH_NOW,
            "why": "The plar.txt bytes current while authoring this revision (the revision-1 value was the pre-save hash of that stage). requirements_hash is unchanged.",
        },
    ],
    "unchanged": "request (historical provider-arguments.json fd0fa324... bound to pixellab-test / connection.json e137fb43...), specialist_assessment (revision-1 file 9ed5ee87..., still valid), integration_recheck (revision-1 file fe5de0a3..., still valid), choices, deferred_obligations, historical_contract, plar_corrections, resume, workspace, stage.",
}

# Place the revision block directly after the version/asset identity fields.
ordered = {}
for k, v in packet2.items():
    ordered[k] = v
    if k == "requirements_hash":
        ordered["revision"] = revision_block
packet2 = ordered

# Guards: nothing else differs from revision 1.
changed_top = [k for k in set(packet) | set(packet2) if packet.get(k) != packet2.get(k)]
assert sorted(changed_top) == sorted(["sources", "plar", "criteria", "review_status", "revision"]), changed_top
src_diff = [(a["path"], k) for a, b in zip(packet["sources"], packet2["sources"]) for k in a if a[k] != b[k]]
assert src_diff == [("OWNER.md", "locators")], src_diff
for k in ("request", "specialist_assessment", "integration_recheck", "choices", "deferred_obligations",
          "historical_contract", "plar_corrections", "resume", "workspace", "stage"):
    assert packet[k] == packet2[k], k

packet2_sha = dump(REV2 / "request-review.json", packet2)
print("revision-2/request-review.json", packet2_sha)

# Revision-1 files are untouched.
assert sha(REV1 / "request-review.json") == REV1_PACKET_SHA
assert sha(REV1 / "candidate-plan.json") == REV1_PLAN_SHA
assert sha(REV1 / "candidate-plan-changes.json") == REV1_CHANGES_SHA
print("revision-1 files unchanged")
