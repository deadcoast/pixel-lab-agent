"""Write rev3 artifacts for queue.ready from rev2, changing only check-mark-asymmetrical-arms.

Run: python -I build-packet.py PROJECT_ROOT REQUIREMENTS_HASH
provider-arguments.json and connection.json are byte copies of rev2.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

root = Path(sys.argv[1])
req_hash = sys.argv[2]
r2 = root / "work/queue.ready/rev2"
r3 = root / "work/queue.ready/rev3"
P2, P3 = "work/queue.ready/rev2", "work/queue.ready/rev3"


def sha(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


# Byte-identical copies.
for f in ["provider-arguments.json", "connection.json"]:
    (r3 / f).write_bytes((r2 / f).read_bytes())
    assert sha(f"{P3}/{f}") == sha(f"{P2}/{f}")

schema = json.loads((root / "provider-schemas.json").read_text(encoding="utf-8"))["create_image_pro_flash"]
args = json.loads((r3 / "provider-arguments.json").read_text(encoding="utf-8"))
jsonschema.Draft202012Validator(schema).validate(args)
conn = json.loads((r3 / "connection.json").read_text(encoding="utf-8"))
assert conn["schema"] == schema

OLD_CHECK = ("The image visibly uses a check mark whose two arms are of clearly unequal length (asymmetrical), and that "
             "mark conveys successful completion. Either arm may be the longer one, and stroke weight, colour treatment "
             "and construction are not restricted by this criterion.")
NEW_CHECK = ("The image visibly uses a check mark with asymmetrical arms: the mark is not mirror-symmetric about its "
             "vertex. Asymmetry may come, for example, from clearly unequal arm lengths or from clearly different arm "
             "angles/directions; unequal length is one example, not the required condition. The mark conveys successful "
             "completion. Either arm may be the longer one, and stroke weight, colour treatment and construction are not "
             "restricted by this criterion.")

plan = json.loads((r2 / "candidate-plan.json").read_text(encoding="utf-8"))
new_plan = copy.deepcopy(plan)
new_plan["scope"] = (plan["scope"].replace("rev2/request-review.json", "rev3/request-review.json")
                     .replace("(queue.ready, second generation)", "(queue.ready, third generation)"))
assert "third generation" in new_plan["scope"]
crit = {c["id"]: c for c in new_plan["outputs"][0]["criteria"]}
assert crit["check-mark-asymmetrical-arms"]["check"] == OLD_CHECK
crit["check-mark-asymmetrical-arms"]["check"] = NEW_CHECK
assert "the asymmetry of the check-mark arms" in crit["readability-1x-3x"]["check"]
(r3 / "candidate-plan.json").write_text(json.dumps(new_plan, indent=2) + "\n", encoding="utf-8")

# Confirm only the intended criterion text (and scope packet pointer) changed.
for a, b in zip(plan["outputs"][0]["criteria"], new_plan["outputs"][0]["criteria"]):
    if a["id"] != "check-mark-asymmetrical-arms":
        assert a == b
    else:
        assert {k: v for k, v in a.items() if k != "check"} == {k: v for k, v in b.items() if k != "check"}
assert ({k: v for k, v in plan["outputs"][0].items() if k != "criteria"}
        == {k: v for k, v in new_plan["outputs"][0].items() if k != "criteria"})

packet = json.loads((r2 / "request-review.json").read_text(encoding="utf-8"))
packet["requirements_hash"] = req_hash
packet["plar"] = {"path": "plar.txt", "sha256": sha("plar.txt"), "asset_id": "queue.ready", "requirements_hash": req_hash}
packet["revision"] = {
    "kind": "revised contract (third generation; corrects one rev2 criterion only)",
    "supersedes_packet": {"path": f"{P2}/request-review.json", "sha256": sha(f"{P2}/request-review.json")},
    "earlier_packets_retained": [{"path": "work/queue.ready/request-review.json",
                                  "sha256": sha("work/queue.ready/request-review.json")}],
    "caller_review": {"path": f"{P2}/caller-review.json", "sha256": sha(f"{P2}/caller-review.json"),
                      "verdict": "changes_requested"},
    "withdrawal": {"path": f"{P2}/withdrawal.json", "sha256": sha(f"{P2}/withdrawal.json"),
                   "job": "r.f9e2fa53f4fcac2a.request", "dispatched": False},
    "changes": [
        "Criterion check-mark-asymmetrical-arms: rejection condition changed from 'two arms are of clearly unequal "
        "length (asymmetrical)' to visibly asymmetrical arms (the mark is not mirror-symmetric about its vertex); "
        "unequal length and different arm angles/directions are cited as examples, not as the condition. 'Either arm "
        "may be the longer one' and the unrestricted stroke/colour/construction clauses kept. Source: BRIEF.md line 9.",
        "readability-1x-3x text unchanged; its phrase 'the asymmetry of the check-mark arms' now refers to the same "
        "broadened asymmetry.",
        "candidate-plan scope: editorial pointer updates only ('second generation' -> 'third generation', "
        "'rev2/request-review.json' -> 'rev3/request-review.json'); scope meaning unchanged.",
        "No other criterion, choice, deferred obligation, provider argument or connection change. "
        "provider-arguments.json and connection.json are byte copies of the rev2 files; the short-left/long-right "
        "description remains a specialist prompt choice (choices.arm-orientation).",
    ],
}
for s in packet["sources"]:
    s["sha256"] = sha(s["path"])
packet["request"]["path"] = f"{P3}/provider-arguments.json"
packet["request"]["sha256"] = sha(f"{P3}/provider-arguments.json")
packet["request"]["arguments_copied_unchanged_from"] = {"path": f"{P2}/provider-arguments.json",
                                                        "sha256": sha(f"{P2}/provider-arguments.json")}
packet["request"]["connection"] = {
    "path": f"{P3}/connection.json", "sha256": sha(f"{P3}/connection.json"),
    "copied_unchanged_from": {"path": f"{P2}/connection.json", "sha256": sha(f"{P2}/connection.json")},
}
packet["request"]["schema_validation"] = (
    f"Arguments validated against provider-schemas.json#create_image_pro_flash (Draft 2020-12) by {P3}/build-packet.py.")
packet["criteria"]["path"] = f"{P3}/candidate-plan.json"
packet["criteria"]["sha256"] = sha(f"{P3}/candidate-plan.json")
packet["resume"] = {
    "store": ".pixl/assets/queue.ready",
    "state_before_revision": {"revision": 7, "hash": "d4edd839dceb09279859e3913a46f7c7d8c6b6c48aff4e22ec853059ce68e8cb"},
    "prior_generations": [
        {"task": "task", "output": "output.ready", "task_state": "open",
         "packet": "work/queue.ready/request-review.json"},
        {"task": "r.f9e2fa53f4fcac2a.task", "output": "r.f9e2fa53f4fcac2a.output.ready", "task_state": "open",
         "packet": f"{P2}/request-review.json"},
    ],
    "jobs": [
        {"id": "first_request", "task": "task", "provider": "pixellab-test", "tool": "create_image_pro_flash",
         "remote_id": "controlled-create-0001", "state": "failed", "next_action": "review_failure",
         "provider_simulated": True, "evidence": "work/queue.ready/provider-observation-failed.json",
         "note": "Terminal on its originating controlled connection with no image; retained, not reused."},
        {"id": "r.f9e2fa53f4fcac2a.request", "task": "r.f9e2fa53f4fcac2a.task", "provider": "pixellab-test",
         "tool": "create_image_pro_flash", "remote_id": None, "state": "failed", "next_action": "review_failure",
         "provider_simulated": True, "evidence": f"{P2}/withdrawal.json",
         "note": "Prepared rev2 intent withdrawn locally by the caller before any dispatch; no remote identity; "
                 "the OWNER.md line 7 request remains unused."},
    ],
    "preparation": "pixl_plar_prepare revise=true with expect = state hash above; the new task/output/job IDs are "
                   "reported from its result, not assumed.",
}
packet["preserved"]["prior_packet_artifacts"] = (
    "work/queue.ready/*.json (first generation) and work/queue.ready/rev2/* left byte-identical.")
packet["review_status"] = {
    "specialist_self_review": "Specialist validated arguments against the discovered schema and resolved locators "
                              "with pixl_request_review; self-review only.",
    "independent_caller_review": "not yet performed for rev3 (caller owns it)",
}
(r3 / "request-review.json").write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
for f in ["provider-arguments.json", "candidate-plan.json", "connection.json", "request-review.json"]:
    print(f, sha(f"{P3}/{f}"))
