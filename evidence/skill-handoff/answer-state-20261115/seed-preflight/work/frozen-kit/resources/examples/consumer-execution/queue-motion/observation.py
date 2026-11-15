"""Bridge queue-motion-v1 evidence into the unchanged closed NF-06 report.

Mode strings carry phase and scale. Complete raw observations remain retained;
this conversion does not execute a browser or grant review or acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(project, capture, context, renderer, destinations):
    project = Path(project).resolve()

    def confined(path):
        actual = Path(path).resolve()
        if actual == project or not actual.is_relative_to(project):
            raise ValueError("Observation input is outside the consumer root")
        return actual

    capture, context, renderer, destinations = map(confined, (capture, context, renderer, destinations))

    def child(base, name):
        if not isinstance(name,str) or "\\" in name or Path(name).is_absolute() or any(x in ("", ".", "..") for x in name.split("/")):
            raise ValueError("Noncanonical observation reference")
        path=confined(base / name)
        if not path.is_relative_to(base):
            raise ValueError("Reference escaped its retained directory")
        return path

    def ref(path, expected=None):
        path=confined(path)
        actual=digest(path)
        if expected is not None and actual != expected:
            raise ValueError("Retained input changed: " + str(path))
        return {"path":path.relative_to(project).as_posix(),"sha256":actual}

    observed=json.loads((capture / "capture.json").read_bytes())
    launch=json.loads((capture / "launch.json").read_bytes())
    review=json.loads(context.read_bytes())
    mapping=json.loads(destinations.read_bytes())
    if not isinstance(mapping,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in mapping.items()):
        raise ValueError("Explicit destination map must be an object")
    if Path(observed["project"]).resolve() != project or Path(launch["project"]).resolve() != project:
        raise ValueError("Capture belongs to a different consumer root")
    if mapping != observed["config"]["destinations"] or observed["config"] != launch["config"]:
        raise ValueError("Capture config and explicit destination map disagree")
    manifest_ref=ref(child(project,review["candidate_file"]["path"]),review["candidate_file"]["sha256"])
    manifest=json.loads((project / manifest_ref["path"]).read_bytes())
    # Only explicit context presentation fields are excluded. Unknown extras
    # remain in the comparison so they cannot replace immutable member identity.
    if manifest["candidate"] != review["candidate"] or manifest["files"] != [{k:v for k,v in row.items() if k not in {"retained_path", "lineage"}} for row in review["members"]]:
        raise ValueError("Review context and exact manifest disagree")
    members={row["output"]:row for row in manifest["files"]}
    if set(mapping) != set(members):
        raise ValueError("Map must cover every exact package member")
    served=observed["served_files"]
    destination_rows=[]
    for output,path in mapping.items():
        member=members[output]
        if served.get("consumer/"+path) != member["sha256"]:
            raise ValueError("Mapped member was not actually served: " + output)
        destination_rows.append({"output":output,"candidate":member["candidate"],**ref(child(project,path),member["sha256"])})
    renderer_refs=[ref(child(renderer,name),expected) for name,expected in sorted(observed["renderer_files"].items())]
    for key,expected in served.items():
        if key.startswith("renderer/"):
            ref(child(renderer,key.removeprefix("renderer/")),expected)
    consumer_refs=[ref(child(project,key.removeprefix("consumer/")),expected) for key,expected in sorted(served.items()) if key.startswith("consumer/")]
    if not consumer_refs:
        raise ValueError("No served consumer source identities")
    files, ids=[],{}

    def add(path,role="data",expected=None):
        value=ref(path,expected)
        if value["path"] in ids:
            return ids[value["path"]]
        ident="execution."+str(len(files));ids[value["path"]]=ident
        files.append({"id":ident,**value,"role":role})
        return ident

    def image(cell):
        value=cell["image"]
        return add(child(capture,value["path"]),"image",value["sha256"])

    views=[]
    limitations=["Fixed queue-motion-v1 fixture observations; artistic quality and target-engine acceptance remain separate.",
                 "Phase, preference and scale appear in motion.mode; complete paint clocks, counts, transitions and switch/reconciliation records remain in raw capture.json.",
                 "The bridge reads retained browser evidence; it does not grant acceptance or infer unobserved capability."]
    for cell in observed["views"]:
        if "image" not in cell:
            limitations.append("Unavailable view: " + cell["consumer"] + "/" + cell["state"])
            continue
        outputs=[key for key,path in mapping.items() if path == cell["descriptor"]["path"]]
        for output in outputs:
            if cell["asset"]["sha256"] != members[output]["sha256"]:
                raise ValueError("View differs from exact package member")
        views.append({"consumer":cell["consumer"],"state":cell["state"],"scale":cell["scale"],"output_id":image(cell),"member_outputs":outputs})
    motion=[]
    for phase in observed["phases"]:
        for consumer in ("statusCell","compactStatus"):
            for scale in observed["config"]["scales"]:
                samples=[]
                if phase["status"] == "observed":
                    for sample in phase["samples"]:
                        cells=[c for c in sample["cells"] if c["consumer"] == consumer and c["scale"] == scale]
                        if len(cells) != 1 or "image" not in cells[0]:
                            raise ValueError("Observed phase lacks one actual PNG per consumer/scale")
                        samples.append({"elapsed_ms":sample["elapsed"],"frame":cells[0]["frame"],"output_id":image(cells[0])})
                state=phase["samples"][0]["cells"][0]["state"] if phase["samples"] else "running"
                motion.append({"consumer":consumer,"state":state,"mode":f"queue-motion-v1 / {phase['name']} / {phase['motion']} / {scale}x", "status":"observed" if samples else "unavailable", "frame_count":phase.get("frameCount"),"frame_ms":phase.get("frameMs"),"samples":samples,"limitation":phase.get("reason") or "No phase explanation supplied"})
                if not samples:
                    limitations.append("Partial phase retained without claiming observed qualification: " + phase["name"])
    for path in sorted(p for p in capture.rglob("*") if p.is_file()):
        add(path,"image" if path.suffix.lower() == ".png" else "log" if path.suffix.lower() == ".log" else "data")
    add(context);add(destinations)
    # Parent execution retains config and independent check next to this capture.
    for name in ("config.json","check.json"):
        path=capture.parent / name
        if path.is_file():
            add(path)
    return {"version":1,"candidate":review["candidate"],"binding_hash":review["binding_hash"],"manifest":manifest_ref,"observed_at":observed["observed_at"],
            "renderer":{"name":"queue-motion-v1 isolated consumer execution","command":[launch["browser"],*launch["args"]],"runtime":{"name":"browser","version":observed["browser_version"]["product"]},"files":renderer_refs},
            "consumer_sources":consumer_refs,"destinations":destination_rows,"viewport":observed["viewport"],"views":views,"motion":motion,"files":files,"limitations":list(dict.fromkeys(limitations))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("project","capture","context","renderer","destinations","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    target=args.out.resolve()
    if target.exists() or target == args.project.resolve() or not target.is_relative_to(args.project.resolve()):
        raise ValueError("Report requires a fresh consumer-relative path")
    result=build(args.project,args.capture,args.context,args.renderer,args.destinations)
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write("\n")
    print(json.dumps({"path":str(target),"sha256":digest(target),"renderer_executed":False,"acceptance_created":False}))


if __name__ == "__main__":
    main()
