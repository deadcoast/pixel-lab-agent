"""Caller helper: plar.txt copy with only queue.ready next/evidence changed after rev3 submission.
Usage: python -I build_plar_submitted.py PROJECT_ROOT EXPECTED_PLAR_SHA256 OUT_JSON"""
import copy, hashlib, json, os, sys
os.chdir(sys.argv[1])
assert hashlib.sha256(open("plar.txt","rb").read()).hexdigest()==sys.argv[2]
doc=json.load(open("plar.txt",encoding="utf-8")); orig=copy.deepcopy(doc)
a=[x for x in doc["assets"] if x["id"]=="queue.ready"][0]
a["next"]=("Revised request accepted by the controlled connection: job r.725292e0867932c7.request in .pixl/assets/queue.ready "
 "(task r.725292e0867932c7.task, output r.725292e0867932c7.output.ready) is submitted with remote_id controlled-create-0002 on "
 "pixellab-test (provider_simulated=true, queued, no image). Earlier attempts are preserved: first_request "
 "(controlled-create-0001) failed without an image, and r.926cff0e8f7acca0.request was retired before dispatch. "
 "Neither simulated ID may be retrieved from or reused on a real service. Next: a separately authorized live PixelLab "
 "connection must run its own job under the rev3 contract (or a re-reviewed one). Then retrieve and import the candidate "
 "and inspect it at 1x/3x nearest on #172336 against the 8 saved criteria, including asymmetric-check-mark. Record the "
 "Ready style decision before expanding Working/Retry/Paused, deliver to assets/ready-confirmed.png and exercise "
 "statusCell/compactStatus. Not integrated.")
a["evidence"]+= [
 {"path":"work/queue.ready/rev3/caller-review.json","note":"Independent caller comparison of rev3 packet de88a037...: consistent (the rev2 discrepancy is resolved). sha256 bfae332bf3b30c40a1564c3c80109f9c91efa501c05c091db181ca3318ac2f45."},
 {"path":"work/queue.ready/rev3/provider-response.json","note":"Actual pixellab-test create_image_pro_flash and list_jobs responses: controlled-create-0002 queued, controlled-create-0001 failed; provider_simulated=true; no image. sha256 00c58d27215d0a66442c6f140e4e441c13d4461b5103cb0024e86d9bbcbe946b."},
 {"path":"work/queue.ready/rev3/submission-comparison.json","note":"Submitted, echoed and saved job arguments equal the reviewed rev2/provider-arguments.json (bef25100...). sha256 041a908f25adfe4d11ca882ea3b91cafa3af3045777e941ff173c15953202d00."},
 {"path":".pixl/assets/queue.ready/state.px","note":"PX2 store after the submitted observation: revision 11, hash 2e63e48d79cb4bb5b4b863f689320db38139f51a918d9cf2e2ff01ec7d539970; job r.725292e0867932c7.request submitted; task open; no candidate."}]
# assert nothing else changed
for k in orig:
    if k!="assets": assert orig[k]==doc[k],k
for o,n in zip(orig["assets"],doc["assets"]):
    if o["id"]!="queue.ready": assert o==n
    else: assert {k:v for k,v in o.items() if k not in("next","evidence")}=={k:v for k,v in n.items() if k not in("next","evidence")}
json.dump(doc,open(sys.argv[3],"w",encoding="utf-8"),indent=2)
