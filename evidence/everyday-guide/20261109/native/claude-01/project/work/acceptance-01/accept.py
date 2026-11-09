"""Publish this scoped, actually observed maintainer review through normal PIXL operations."""
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from pixl import codec, graph, plar, service, store

work = Path(__file__).resolve().parent
project = work.parent.parent
folder = ".pixl/assets/queue.ready"
prefix = "provenance-correction"


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(name, value):
    path=work/name
    if name == "motion-review.json" and path.exists():
        return path
    with path.open("x",encoding="utf-8") as handle:
        json.dump(value,handle,ensure_ascii=False,indent=2)
        handle.write("\n")
    return path


def artifact(path):
    return {"path":path.relative_to(project).as_posix(),"sha256":sha256(path.read_bytes()).hexdigest()}


def commit(before, after, label):
    after.revision+=1
    payload={"format":after.format,"revision":after.revision,"records":[{"id":r.id,"kind":r.kind,"fields":codec.to_data(r.fields)} for r in after.records.values()]}
    save(label+"-document.json",payload)
    result=service.call("pixl_commit",{"store":folder,"expect":codec.digest(before),"document":payload},project)
    save(label+"-commit.json",result)
    return result


def verdict(doc, candidate, criterion, task, ident, mode, report, reason):
    receipt=ident+".evidence"
    scope=graph.proof_scope(doc,[candidate,criterion])
    doc.records[receipt]=codec.Record(receipt,"E",{"nm":reason,"ur":report.relative_to(project).as_posix(),"dg":sha256(report.read_bytes()).hexdigest(),"rs":codec.Symbol("pass"),"md":codec.Symbol(mode),"at":now(),"bs":[{"rf":codec.Ref(k),"dg":codec.record_hash(doc.records[k])} for k in sorted(scope)]})
    doc.records[ident]=codec.Record(ident,"V",{"tk":codec.Ref(task),"rq":codec.Ref(criterion),"xr":codec.Ref(candidate),"st":codec.Symbol("pass"),"wh":codec.Ref("acceptance.reviewer"),"wy":reason,"at":now(),"ev":[codec.Ref(receipt)]})
    doc.records[task].fields["vr"].append(codec.Ref(ident))


def complete(task,candidate,label):
    doc=store.load(project/folder)
    result=service.call("pixl_task_complete",{"store":folder,"expect":codec.digest(doc),"task_id":task,"candidates":[candidate]},project)
    save(label+"-complete.json",result)


if sys.argv[1]=="motion":
    assert read(work/"review-checks.json")["status"]=="pass"
    doc=store.load(project/folder); graph.validate(doc,project)
    candidate=prefix+".working.candidate"; criterion=prefix+".working.q.motion-continuity"; task=prefix+".working.task"
    report=save("motion-review.json",{
        "reviewer":"Codex maintainer applying PIXL in a scoped production evaluation","observed_at":now(),
        "candidate":candidate,"candidate_sha256":doc.records[candidate].fields["dg"],"criterion":criterion,"literal_check":doc.records[criterion].fields["ck"],
        "viewed":[artifact(work/"headless-review-03/playback.png"),artifact(work/"headless-review-03/stationary.png"),*[artifact(work/f"observed-views/transition-{i:02d}-{s}x-color.png") for i in range(5) for s in (1,3)]],
        "execution":[artifact(work/"playback-observation-03.json"),artifact(work/"review-checks.json"),artifact(work/"destination-01/render.json"),artifact(work/"destination-01/motion.json")],
        "findings":["Reviewed actual browser-recorded exposures at native 16x16 and nearest 48x48, in order 0,1,2,3,0 and across four observed wraps. The three separated segments remain one rotating activity mark; the last-to-first step continues the same direction and spacing as the other steps.","The chosen loop has consistent visual weight and a stable rotational center. Bounding boxes orbit by a pixel with the asymmetric segments; this is coherent rotation, not a separate anchor jump. Visible composited pixels are exact clockwise quarter-turns including the wrap; hidden RGB at zero alpha has no visual authority.","Actual recorded transition intervals are approximately 100 ms; no extra held phase or distinct wrap discontinuity appears in the reviewed sequence. The UI remains intentionally four-step pixel motion, not interpolated smooth rotation.","Stationary frame zero remains an open segmented activity mark, distinct from Ready's diagonal check and Paused's parallel bars; reduced-media behavior was separately executed in the destination capture."],
        "verdict":"pass","scope":"Agent visual judgment of recorded browser playback plus timing/pixel measurements for this exact loop. No human real-time viewing claim, universal cluster-count rule or general animation-quality qualification.",
        "prior_unavailable":"provenance.working.motion.unavailable; retained and explicitly superseded, not edited into a pass"})
    updated=deepcopy(doc)
    updated.records["acceptance.reviewer"]=codec.Record("acceptance.reviewer","A",{"nm":"Codex maintainer / scoped PIXL production review","rl":codec.Symbol("agent")})
    updated.records["provenance.working.motion.unavailable"].fields["ob"]=True
    verdict(updated,candidate,criterion,task,"acceptance.working.motion","visual",report,"Recorded native/3x playback shows consistent quarter-turn activity through all four wraps, stable center/weight and no extra held phase; scoped visual review passes.")
    commit(doc,updated,"motion-02")
    complete(task,candidate,"working")
    doc=store.load(project/folder)
    result=service.call("pixl_family_snapshot",{"store":folder,"expect":codec.digest(doc),"output_id":prefix+".delivery.output","candidate_id":"acceptance.family.candidate"},project)
    save("family-snapshot.json",result)
    print(json.dumps(result,indent=2))

if sys.argv[1]=="family":
    assert read(work/"package-review-checks.json")["status"]=="pass"
    assert read(work/"package-motion-details.json")["status"]=="pass"
    doc=store.load(project/folder);graph.validate(doc,project)
    candidate="acceptance.family.candidate";task=prefix+".delivery.task"
    snapshot=read(work/"family-snapshot.json")
    reasons={
        "continuity":"The exact four-member package reads as one compact pixel UI family at 1x/3x. Ready's check, Working's separated rotating segments, Retry's connected returning arrow and Paused's paired bars share deliberate stepped treatment, comparable visual weight and a clear cool-blue role. Their differing footprints and internal shading remain appropriate to their symbols. Transparent exterior shows the panel without an unintended matte. Working's observed loop and stationary frame zero preserve that family treatment.",
        "distinction":"Shape carries meaning in color and grayscale: Ready is a diagonal check, Working stays three detached orbiting segments in every phase, Retry is a connected circular return arrow, and Paused has two parallel bars. No Working frame reads as a completion check. Stationary frame zero remains distinct from Ready/Paused and, by the scoped shared-consumer inference, from Retry and the preserved solid Start triangle. No universal motif ban is inferred.",
        "destination":"The exact snapshot files were copied to the reviewed successor destination and freshly executed through both actual consumers. All five backend transitions, labels, four horizontal Working cells, boundary/wrap selection, 1x/3x nearest sampling, alpha compositing and integer screenshot placement pass. Actual media changes reconcile once through the existing animation-frame route; both live consumers retain running state, switch to stationary frame zero for more than 800 ms, and restart at frame zero with all four phases. Reduced matrix cells match exact source frame zero. Original source, renderer and Start asset bytes remain unchanged."
    }
    report=save("family-review.json",{"observed_at":now(),"reviewer":"Codex maintainer applying PIXL in a scoped production evaluation","candidate":candidate,"manifest":artifact(project/snapshot["manifest"]),"package_integration":artifact(work/"package-integration.json"),"criteria":[{"id":prefix+".delivery.q."+key,"literal_check":doc.records[prefix+".delivery.q."+key].fields["ck"],"verdict":"pass","reason":reason} for key,reason in reasons.items()],"visual_inputs":[artifact(work/"headless-review-03/playback.png"),artifact(work/"headless-review-03/stationary.png"),artifact(work/"destination-package-02/destination.png"),*[artifact(work/f"observed-views/transition-{i:02d}-{scale}x-gray.png") for i in range(4) for scale in (1,3)]],"engine_inputs":[artifact(work/"destination-package-02/render.json"),artifact(work/"destination-package-02/motion.json"),artifact(work/"destination-package-checks.json"),artifact(work/"package-review-checks.json"),artifact(work/"package-motion-details.json")],"observation_continuity":"The recorded visual exposures precede this package snapshot but show byte-identical members, verified by the manifest and package integration hashes. Destination execution was rerun after copying the exact snapshot members. No fabricated new viewing, source time or provider execution.","limits":["Acceptance applies to this queue fixture and reviewed successor requirements; not general host or generated-art quality.","Maintainer production review, not an unassisted native Claude/Codex completion.","Recorded sequence review with actual browser timing and pixels; no claim of human real-time perception or exact scheduler guarantees."]})
    updated=deepcopy(doc)
    for key,reason in reasons.items():
        verdict(updated,candidate,prefix+".delivery.q."+key,task,"acceptance.family."+key,"live" if key=="destination" else "visual",report,reason)
    commit(doc,updated,"family-review")
    complete(task,candidate,"family")
    print("Working and collective family tasks completed through normal lifecycle operations.")

if sys.argv[1]=="handoff":
    doc=store.load(project/folder);graph.validate(doc,project)
    assert doc.records[prefix+".delivery.task"].fields["st"].value=="done"
    path="authoring-plar.txt"
    selected_before={a:plar.read(project,path,a) for a in ("queue.ready","queue.working","queue.retry","queue.paused")}
    queue=read(project/path)
    for asset in queue["assets"]:
        if asset["id"] in selected_before:
            asset["status"]="integrated"
            asset["next"]="Scoped successor family and destination accepted. Preserve exact package and earlier attempts; future requirement or artwork changes need their own review."
            asset["evidence"].append({"path":"work/acceptance-01/family-review.json","note":"Actual scoped family/recorded-motion review and fresh isolated destination execution of exact snapshot members; collective task complete. No new generation or general host qualification."})
    result=plar.save(project,queue,sha256((project/path).read_bytes()).hexdigest(),path)
    save("plar-update.json",result)
    for asset,old in selected_before.items():
        assert plar.read(project,path,asset)["requirements_hash"]==old["requirements_hash"]
    flow=service.call("pixl_workflow",{"path":folder+"/state.px"},project)
    family=service.call("pixl_family",{"path":folder+"/state.px","output":prefix+".delivery.output"},project)
    save("workflow-final.json",flow);save("family-final.json",family)
    selected=plar.read(project,path,"queue.working")
    snapshot=read(work/"family-snapshot.json")
    details={"status":"delivered","artifacts":[artifact(project/snapshot["manifest"]),artifact(work/"family-review.json"),artifact(work/"motion-review.json")],"caller_actions":["Scoped Working motion, collective family and exact-package destination review completed. Both actual consumers and normal/reduced/live-switch behavior verified."],"future_work":["Broader generated quality and native host reliability remain development items; this queue successor has no outstanding acceptance check."],"limits":["Maintainer evaluation using isolated headless execution; not a fresh two-host native conformance pass."]}
    handoff=service.call("pixl_plar_handoff",{"path":path,"asset_id":"queue.working","requirements_hash":selected["requirements_hash"],"expect":selected["production"]["continuation"]["state_hash"],"details":details},project)
    save("handoff.json",handoff)
    summary={"observed_at":now(),"status":"delivered","project":project.relative_to(Path.cwd()).as_posix(),"state_revision":doc.revision,"state_hash":codec.digest(doc),"working":"done; all eight requirements pass","family":"done; continuity, distinction and destination pass","candidate":"acceptance.family.candidate","package":snapshot["package"],"manifest":artifact(project/snapshot["manifest"]),"handoff":handoff,"requirements_unchanged":{a:s["requirements_hash"] for a,s in selected_before.items()},"limits":details["limits"]}
    save("DELIVERY.json",summary)
    with (project.parent/"DELIVERY.json").open("x",encoding="utf-8") as output:
        json.dump(summary,output,indent=2);output.write("\n")
    print(json.dumps(summary,indent=2))
