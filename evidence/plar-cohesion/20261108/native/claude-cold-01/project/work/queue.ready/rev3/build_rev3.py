"""Derive rev3 candidate-plan.json and request-review.json from the rev2 artifacts.

Only the caller-requested criterion change (asymmetric-check-mark) plus revision
bookkeeping (scope/name labels) differ from rev2. Provider arguments and connection
are reused by path/hash from rev2 (not copied, not modified).

Usage: python -I build_rev3.py PROJECT_ROOT REQUIREMENTS_HASH STATE_HASH STATE_REVISION
"""
import copy
import difflib
import hashlib
import json
import os
import sys

import jsonschema

os.chdir(sys.argv[1])
RH, STATE_HASH, STATE_REV = sys.argv[2], sys.argv[3], int(sys.argv[4])
R2 = "work/queue.ready/rev2/"
R3 = "work/queue.ready/rev3/"


def H(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(p, doc):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


EXPECT = {
    R2 + "candidate-plan.json": "fff991e0f14699bbb14df51f3cadbb66f912f08b01b3ec3b7ca5f6be37650f5b",
    R2 + "request-review.json": "39b727bda069fb1983f1c74c1eb9a0b1966aa146ad4e194c498eaea4a97385de",
    R2 + "provider-arguments.json": "bef2510035113048070b25172b4b042633a2c7e4dca950915afa5b0aedeefdae",
    R2 + "connection.json": "86fd154ec0a9ad081381d88d132df98a1d04dd0e67e98c800bb9113c6acc3d88",
    R2 + "caller-review.json": "f0ab72906afce249a74ef20be918f2bb302b1625bf3888086c9ba687238f8fa1",
}
for p, h in EXPECT.items():
    assert H(p) == h, (p, H(p))

OLD_CHECK = ("At 1x and at 3x nearest-neighbor scale on #172336, the mark is visibly a check mark whose two arms "
             "are clearly unequal in length (asymmetrical), so that it reads as successful completion. The criterion "
             "does not fix the arm ratio, orientation (left/right), stroke weight or colour; a symmetric V, a cross, "
             "a circle-only badge or an indistinct blob fails.")
NEW_CHECK = ("At 1x and at 3x nearest-neighbor scale on #172336, the mark is visibly a check mark whose two arms "
             "are visibly asymmetrical (for example differing in length and/or angle), so that it reads as successful "
             "completion. The criterion does not fix the arm ratio, orientation (left/right), stroke weight or colour; "
             "a symmetric V, a cross, a circle-only badge or an indistinct blob fails.")

plan2 = load(R2 + "candidate-plan.json")
plan3 = copy.deepcopy(plan2)
plan3["scope"] = plan2["scope"].replace("(queue.ready, rev2)", "(queue.ready, rev3)").replace(
    "recorded in rev2/request-review.json", "recorded in rev3/request-review.json")
assert plan3["scope"] != plan2["scope"]
out = plan3["outputs"][0]
out["name"] = out["name"].replace("(rev2)", "(rev3)")
crit = [c for c in out["criteria"] if c["id"] == "asymmetric-check-mark"]
assert len(crit) == 1 and crit[0]["check"] == OLD_CHECK
crit[0]["check"] = NEW_CHECK
jsonschema.validate(plan3, load(".agents/skills/pixl-kit/runtime/pixl/asset-plan.schema.json"))

# Every other criterion and the contract must be identical to rev2.
for a, b in zip(plan2["outputs"][0]["criteria"], out["criteria"]):
    if a["id"] != "asymmetric-check-mark":
        assert a == b, a["id"]
    else:
        assert {k: v for k, v in a.items() if k != "check"} == {k: v for k, v in b.items() if k != "check"}
assert plan2["outputs"][0]["contract"] == out["contract"]
dump(R3 + "candidate-plan.json", plan3)

args = load(R2 + "provider-arguments.json")
conn = load(R2 + "connection.json")
jsonschema.validate(args, conn["schema"])

pkt2 = load(R2 + "request-review.json")
# Source bytes must be unchanged since rev2.
for s in pkt2["sources"]:
    assert H(s["path"]) == s["sha256"], s["path"]
assert pkt2["plar"]["requirements_hash"] == RH  # requirements unchanged since rev2

pkt = copy.deepcopy(pkt2)
pkt["plar"]["sha256"] = H("plar.txt")
pkt["plar"]["previous"] = {
    "sha256": pkt2["plar"]["sha256"], "requirements_hash": pkt2["plar"]["requirements_hash"],
    "note": ("plar.txt bytes bound by the rev2 packet; the later change was the post-prepare queue.ready next/evidence "
             "update only (requirements_hash unchanged)."),
    "earlier": pkt2["plar"]["previous"]}
pkt["generation"] = ("rev3 (revision of rev2 packet work/queue.ready/rev2/request-review.json after caller review "
                     "changes_requested; criteria-only change)")
pkt["requirements_hash"] = RH
pkt["plar"]["requirements_hash"] = RH
pkt["sources"].append({
    "path": R2 + "caller-review.json", "sha256": H(R2 + "caller-review.json"),
    "role": "independent caller review of the rev2 packet (changes_requested) that this revision answers",
    "locators": ["criterion_comparisons[id=asymmetric-check-mark]", "requested_change", "next_action"]})

req = pkt["request"]
req["path"] = R2 + "provider-arguments.json"
req["sha256"] = H(R2 + "provider-arguments.json")
req["connection"] = {"path": R2 + "connection.json", "sha256": H(R2 + "connection.json")}
req.pop("changes_from_first_generation", None)
req["reused_from_rev2"] = ("Provider arguments and connection are the rev2 files, byte-unchanged and referenced in place; "
                           "caller review f0ab7290... found them consistent and the tick-orientation prompt an accepted "
                           "specialist choice.")
req["changes_from_rev2"] = "none"

crit_doc = pkt["criteria"]
crit_doc["path"] = R3 + "candidate-plan.json"
crit_doc["sha256"] = H(R3 + "candidate-plan.json")
crit_doc.pop("changes_from_first_generation", None)
crit_doc["changes_from_rev2"] = {
    "previous": {"path": R2 + "candidate-plan.json", "sha256": H(R2 + "candidate-plan.json")},
    "caller_review": {"path": R2 + "caller-review.json", "sha256": H(R2 + "caller-review.json"),
                      "verdict": "changes_requested"},
    "revised": [{
        "id": "asymmetric-check-mark", "field": "check",
        "before": OLD_CHECK, "after": NEW_CHECK,
        "reason": ("Caller review: 'clearly unequal in length' was stricter than BRIEF.md line 9 ('a check mark with "
                   "asymmetrical arms') and would reject a brief-conforming mark whose arms differ in angle/direction "
                   "but are equal in length. Display conditions, open ratio/orientation/stroke/colour and the failure "
                   "examples are kept."),
        "diff": list(difflib.unified_diff([OLD_CHECK], [NEW_CHECK], "rev2", "rev3", lineterm="", n=0))}],
    "bookkeeping": ["scope: '(queue.ready, rev2)' -> '(queue.ready, rev3)' and deferred-obligation pointer "
                    "rev2/request-review.json -> rev3/request-review.json",
                    "outputs[0].name: '(rev2)' -> '(rev3)'"],
    "unchanged": ["contract", "geometry", "transparent-background", "ready-meaning", "readability-1x-3x",
                  "cool-blue-accent", "silhouette-without-color", "sample-pixel-craft",
                  "asymmetric-check-mark basis/scope/sources/domain/mode"]}

for c in pkt["choices"]:
    if c["id"] == "tick-orientation":
        c["reason"] = ("The conventional, most recognisable completion tick in left-to-right UIs. The asymmetric-check-mark "
                       "criterion requires only visibly asymmetrical arms (length and/or angle) and does not fix ratio or "
                       "orientation, so a mirrored, differently proportioned or equal-length/unequal-angle asymmetric tick "
                       "still passes. Accepted by caller review f0ab7290... as a prompt choice, not a rejection rule.")

pkt["resume"] = {
    "store": ".pixl/assets/queue.ready",
    "state_before_revision": {"hash": STATE_HASH, "revision": STATE_REV},
    "previous_generations": [
        {"generation": "first", "task": "task", "output": "output.ready", "candidate": None,
         "job": {"id": "first_request", "state": "failed", "remote_id": "controlled-create-0001",
                 "provider": "pixellab-test", "provider_simulated": True, "evidence": R2 + "original-status.json"},
         "packet": {"path": "work/queue.ready/request-review.json", "sha256": H("work/queue.ready/request-review.json")}},
        {"generation": "rev2", "task": "r.926cff0e8f7acca0.task", "output": "r.926cff0e8f7acca0.output.ready",
         "candidate": None,
         "job": {"id": "r.926cff0e8f7acca0.request", "state": "failed", "remote_id": None, "provider_simulated": True,
                 "retirement": ("Local failed observation recorded before any dispatch claim (store revision 7): never "
                                "dispatched, no remote call, no provider observation; retired because caller review "
                                "f0ab7290... requested a criterion change.")},
         "packet": {"path": R2 + "request-review.json", "sha256": H(R2 + "request-review.json")}}],
    "revision_operation": ("pixl_plar_prepare with revise: true and expect = state_before_revision.hash; the returned "
                           "task/output/job IDs are the current ones"),
}
pkt.pop("state_before_revision", None)
pkt["preserved"]["first_generation"] = ("work/queue.ready/* and work/queue.ready/rev2/* files untouched; first_request "
                                        "and r.926cff0e8f7acca0.request jobs and their events preserved.")
pkt["review_status"] = {
    "specialist_self_review": ("Specialist validated the reused arguments against the connection schema, the rev3 plan "
                               "against asset-plan.schema.json, and asserted every other criterion and the contract are "
                               "identical to rev2; self-review only."),
    "previous_caller_review": {"path": R2 + "caller-review.json", "sha256": H(R2 + "caller-review.json"),
                               "verdict": "changes_requested"},
    "independent_caller_review": "not yet performed for rev3 (caller owns it)"}
dump(R3 + "request-review.json", pkt)
print(json.dumps({"plan": H(R3 + "candidate-plan.json"), "packet": H(R3 + "request-review.json")}))
