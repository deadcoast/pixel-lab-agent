"""Write work/queue.ready/rev3/plar-next-update.json: plar.txt with only queue.ready next/evidence changed.

Usage: python -I build_plar_next.py PROJECT_ROOT EXPECTED_PLAR_SHA256
"""
import copy
import hashlib
import json
import os
import sys

os.chdir(sys.argv[1])


def H(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


assert H("plar.txt") == sys.argv[2]
with open("plar.txt", encoding="utf-8") as f:
    doc = json.load(f)
orig = copy.deepcopy(doc)
a = [x for x in doc["assets"] if x["id"] == "queue.ready"][0]
assert a["production"] == {"store": ".pixl/assets/queue.ready", "task": "r.725292e0867932c7.task",
                           "output": "r.725292e0867932c7.output.ready"}
a["next"] = (
    "First attempt first_request (pixellab-test, remote_id controlled-create-0001, provider_simulated=true) is terminal "
    "failed without an image. Rev2 job r.926cff0e8f7acca0.request was never dispatched (no remote call) and was retired "
    "locally with a failed observation after caller review work/queue.ready/rev2/caller-review.json (f0ab7290...) "
    "requested a criterion change. Rev3 generation prepared in .pixl/assets/queue.ready (revision 9): task "
    "r.725292e0867932c7.task, output r.725292e0867932c7.output.ready, job r.725292e0867932c7.request (prepared, not "
    "dispatched; arguments equal work/queue.ready/rev2/provider-arguments.json bef25100...); packet "
    "work/queue.ready/rev3/request-review.json (de88a037...). Next: caller independently compares the rev3 packet "
    "(criterion asymmetric-check-mark revised) with BRIEF/OWNER/source, rereads PLAR, then claims dispatch of "
    "r.725292e0867932c7.request and submits its exact arguments as the one further controlled pixellab-test request. "
    "No image, style approval or integration exists. Not integrated.")
a["evidence"].append({
    "path": "work/queue.ready/rev3/request-review.json",
    "note": ("Rev3 request/criteria packet (sha256 de88a037a349305e2e29b34bac160aaff069e677ed690cc0dd1f3401eac251c8): "
             "criteria-only revision of rev2 answering caller review f0ab7290...; prepared job r.725292e0867932c7.request, "
             "not dispatched; provider_simulated=true; no image, review or integration.")})
# Only next/evidence of queue.ready may differ.
for k in orig:
    if k != "assets":
        assert orig[k] == doc[k]
for o, n in zip(orig["assets"], doc["assets"]):
    if o["id"] != "queue.ready":
        assert o == n
    else:
        assert {k: v for k, v in o.items() if k not in ("next", "evidence")} == \
               {k: v for k, v in n.items() if k not in ("next", "evidence")}
with open("work/queue.ready/rev3/plar-next-update.json", "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
print(H("work/queue.ready/rev3/plar-next-update.json"))
