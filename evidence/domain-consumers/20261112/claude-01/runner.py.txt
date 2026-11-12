"""TM-08 controlled consumers; local geometry acceptance never accepts their art."""
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

from evaluations import readiness_case
from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT, run
from pixl import candidate_review, codec, delivery, graph, store
from pixl.codec import Document, Record, Ref, Symbol

WORK = "work/domain-consumers"
INPUTS = "work/domain-consumer-inputs"
KIT = readiness_case.KIT
PROJECT = ROOT / "examples/domain-consumer-project"
PROFILES = {"terrain": "tile-neighborhood-v1", "animation": "sprite-animation-v1"}


def config(domain: str) -> dict:
    terrain = domain == "terrain"
    count = 16 if terrain else 4
    directory, prefix = ("terrain", "tile") if terrain else ("motion", "frame")
    value = {"version": 1, "profile": PROFILES[domain],
             "modules": {domain: f"src/{domain}.ts"},
             "destinations": {f"member.{i}.output": f"assets/{directory}/{prefix}-{i}.png"
                              for i in range(count)},
             "scales": [1, 3], "timeout_seconds": 90}
    if not terrain:
        value.update(observed_wraps=2, phase_timeout_ms=10000)
    return value


def state(domain: str) -> str:
    return f".pixl/assets/{domain}/state.px"


def seed_family(root: Path, domain: str) -> dict:
    """Publish measured local-only members and an UNREVIEWED family snapshot.

    No test fixture verdicts are used. Every member has only a dimensions/alpha
    requirement, measured here. Visual continuity and destination requirements
    belong to the open family and have no verdicts.
    """
    configuration = config(domain)
    terrain = domain == "terrain"
    paths = list(configuration["destinations"].values())
    folder = root / Path(state(domain)).parent
    records = {}

    def add(id_, kind, **fields):
        records[id_] = Record(id_, kind, fields)

    add("actor", "A", nm="Controlled consumer preparation", rl=Symbol("agent"))
    add("user", "A", nm="Authored diagnostic project", rl=Symbol("user"))
    brief = root / "BRIEF.md"
    add("source", "S", ur="BRIEF.md", dg=sha(brief),
        ln=[1, len(brief.read_text(encoding="utf-8").splitlines())], at="2026-11-12", au=Symbol("local"))
    add("project", "P", nm=f"TM-08 controlled {domain}", ow=Ref("actor"),
        sc=[Ref("source")], **{"in": [Ref("choice"), Ref("destination")]})
    add("choice", "I", pr=Ref("project"), wh=Ref("user"), ky="pixel_size", st=Symbol("confirmed"),
        vl=[16, 16], so=[Ref("source")], wy="Explicit diagnostic geometry only")
    add("destination", "I", pr=Ref("project"), wh=Ref("user"), ky="delivery_target",
        st=Symbol("confirmed"), vl=f"{PROFILES[domain]} at native 1x and nearest 3x",
        so=[Ref("source")], wy="Authored executable browser destination")
    add("contract", "C", nm="Controlled cell geometry", px=[16, 16], pl=[], vw=Symbol("side"),
        sa=Symbol("nearest"), al=Symbol("binary"), li="No artistic acceptance implied", ch=[Ref("choice")])
    add("q.geometry", "Q", nm="Measured diagnostic geometry", dm=Symbol("mechanical"), md=Symbol("local"),
        ck="PNG is 16x16 with binary alpha; terrain is fully opaque", wh=Ref("actor"), so=[Ref("source")])
    add("q.continuity", "Q", nm="Inspect intended continuity", dm=Symbol("continuity"), md=Symbol("visual"),
        ck=("Land/water material joins follow the vertex grids in both neighborhoods" if terrain else
            "Feet remain planted across all uneven-duration poses; inspect loop and one-shot in context"),
        wh=Ref("actor"), so=[Ref("source")])
    add("q.destination", "Q", nm="Observe actual consumer", dm=Symbol("engine"), md=Symbol("live"),
        ck="Inspect exact mapped pixels, declared geometry and timeline at 1x/3x in the actual browser",
        wh=Ref("actor"), so=[Ref("source")])
    add("decision", "D", wh=Ref("actor"), wt="Use declared controlled geometry to qualify the renderer",
        wr=[Ref("contract")], wy="The measured PNG contract enables an unreviewed family; art remains open",
        rs=[Ref("source")], pc=[Ref("adoption.e")])
    for task_id, phase, outputs, deps in [
        ("sample.task", "sample", ["member.0.output"], []),
        ("members.task", "production", [f"member.{i}.output" for i in range(1, len(paths))], ["sample.task"]),
        ("delivery.task", "delivery", ["delivery.output"], ["sample.task", "members.task"]),
    ]:
        add(task_id, "T", nm=f"{phase} diagnostic {domain}", ow=Ref("actor"), pr=Ref("project"),
            dp=[Ref(x) for x in deps], dc=[] if phase == "sample" else [Ref("decision")], kn=[],
            st=Symbol("open"), ph=Symbol(phase), ip=[] if phase == "sample" else [Ref("member.0")],
            op=[Ref(x) for x in outputs], ca=[], vr=[])
    for i, path in enumerate(paths):
        task_id = "sample.task" if i == 0 else "members.task"
        add(f"member.{i}.output", "F", tk=Ref(task_id), nm=f"Controlled {domain} {i}",
            kd=Symbol("sprite"), ct=Ref("contract"), rq=[Ref("q.geometry")],
            **({} if i == 0 else {"bs": Ref("member.0")}))
        add(f"member.{i}", "X", nm=f"Controlled {domain} {i}", ur=path, dg=sha(root / path),
            ct=Ref("contract"), kd=Symbol("sprite"), of=Ref(f"member.{i}.output"))
        records[task_id].fields["ca"].append(Ref(f"member.{i}"))
    add("delivery.output", "F", tk=Ref("delivery.task"), nm="Unreviewed diagnostic family",
        kd=Symbol("report"), rq=[Ref("q.continuity"), Ref("q.destination")], bs=Ref("member.0"),
        mb=[Ref(f"member.{i}.output") for i in range(len(paths))], ds=[Ref("destination")])
    doc = Document(0, records, format=2)
    adoption_path = f"{INPUTS}/{domain}-adoption.json"
    write_json(root / adoption_path, {"scope": "Authored mechanical-only preparation decision",
                                     "contract": codec.record_hash(records["contract"]),
                                     "artistic_acceptance": False, "human_acceptance": False})
    add("adoption.e", "E", nm="Explicit local geometry adoption", ur=adoption_path,
        dg=sha(root / adoption_path), rs=Symbol("pass"), md=Symbol("local"), at="2026-11-12",
        bs=[{"rf": Ref(x), "dg": codec.record_hash(records[x])}
            for x in sorted(graph.proof_scope(doc, ["decision"]))])
    store.initialize(folder, doc, root)

    def publish():
        current = store.load(folder)
        doc.revision = current.revision + 1
        store.commit(folder, doc, codec.digest(current), root)

    for task_id, indices in (("sample.task", range(1)), ("members.task", range(1, len(paths)))):
        for i in indices:
            path = paths[i]
            with Image.open(root / path) as im:
                im.load()
                alpha = set(im.convert("RGBA").getchannel("A").tobytes())
                assert im.format == "PNG" and im.size == (16, 16) and alpha <= {0, 255}
                assert not terrain or alpha == {255}
            receipt = f"{INPUTS}/{domain}-member-{i}-geometry.json"
            write_json(root / receipt, {"path": path, "sha256": sha(root / path), "size": [16, 16],
                                        "alpha_values": sorted(alpha), "result": "pass",
                                        "scope": "Measured local geometry only; visual/destination/human unreviewed"})
            eid, vid = f"geometry.{i}.e", f"geometry.{i}.v"
            add(eid, "E", nm="Measured PNG dimensions and alpha", ur=receipt, dg=sha(root / receipt),
                rs=Symbol("pass"), md=Symbol("local"), at="2026-11-12",
                bs=[{"rf": Ref(x), "dg": codec.record_hash(records[x])}
                    for x in sorted(graph.proof_scope(doc, [f"member.{i}", "q.geometry"]))])
            add(vid, "V", tk=Ref(task_id), rq=Ref("q.geometry"), xr=Ref(f"member.{i}"),
                st=Symbol("pass"), wh=Ref("actor"), wy="Actual PNG geometry measured; no appearance claim",
                at="2026-11-12", ev=[Ref(eid)])
            records[task_id].fields["vr"].append(Ref(vid))
        records[task_id].fields["st"] = Symbol("active")
        publish()
        records[task_id].fields["st"] = Symbol("done")
        publish()
    delivery.snapshot(folder, codec.digest(store.load(folder)), "delivery.output", "delivery.candidate", root)
    context = candidate_review.context(store.load(folder), root, "delivery.candidate")
    write_json(root / INPUTS / f"{domain}-context.json", context)
    write_json(root / INPUTS / f"{domain}-config.json", configuration)
    return context


def project(root: Path, *, defects=False) -> dict:
    """Copy diagnostic source; optional pixel faults preserve correct metadata."""
    if any((root / name).exists() for name in ("assets", "src", ".pixl", INPUTS)):
        raise ValueError("Use a fresh diagnostic project; preserve existing assets, source and state")
    shutil.copytree(PROJECT, root, dirs_exist_ok=True)
    changes = {}
    if defects:
        for name in ("assets/terrain/tile-6.png", "assets/motion/frame-2.png"):
            path = root / name
            before = sha(path)
            with Image.open(path) as source:
                im = source.convert("RGBA")
            if "terrain" in name:
                ImageDraw.Draw(im).rectangle((0, 0, 7, 7), fill="#72b36c")
            else:
                shifted = Image.new("RGBA", im.size)
                shifted.paste(im, (0, 2))
                im = shifted
            im.save(path)
            changes[name] = {"original_sha256": before, "controlled_sha256": sha(path)}
    for domain in PROFILES:
        seed_family(root, domain)
    return {"controlled": True, "pixel_changes": changes, "generated_art": False,
            "family_artistic_acceptance": False, "human_acceptance": False}


def prepare(destination: Path, host: str, python: Path, *, package=None, consumer=None) -> Path:
    destination = destination.resolve()
    root = readiness_case.prepare(destination, host, "clean", python.resolve(), package=package, consumer=consumer)
    preparation = project(root, defects=True)
    (root / WORK).mkdir(parents=True)
    role = "pixl" if host == "codex" else "pixl:pixl"
    guidance = f"""Explicit TM-08 consumer qualification evaluation in {root.as_posix()}.
Use the actual named {role} specialist to complete DOMAIN-CONSUMERS.md.
Installed kit: {(root / KIT).as_posix()}; Python: {python.resolve().as_posix()}.
Read BRIEF.md. Keep all original source, pixels, production records and kit unchanged.
Write only under {WORK}. No provider calls, installation, global/memory changes,
candidate reviews/verdicts or acceptance. M1/M2 and broader M3/M4 remain open.
"""
    assignment = f"""# Qualify the two controlled domain consumers

Delegate to one actual named `{role}` specialist (Codex: agent_type="pixl", fork_turns="none").
Retain its actual identity and wait for completion. It MUST read the complete installed
`skills/pixl/SKILL.md`, `resources/agent/PROFILE.md` and consumer-execution workflow reference.
Use this kit's actual paths; locate the profile if its shared path differs.

The specialist must read BRIEF.md, both src modules and the two config/context files
under {INPUTS}. These controlled families have only measured geometry accepted.
Family visual continuity and destination requirements remain unreviewed. No real art
quality or human acceptance is assigned. For each domain `terrain` and `animation`:
1. Inspect the public tool schema or CLI help, then use `pixl_consumer_execute` (or
   frozen public CLI) on `.pixl/assets/<domain>/state.px`, candidate
   `delivery.candidate`, exact `<domain>-config.json`, out `{WORK}/<domain>-01`.
   Save the actual full returned JSON to `{WORK}/<domain>-result.json` using the
   advertised result_path or exact CLI stdout. Do not transcribe or invent receipts.
2. Read the returned report, checks, cleanup and NF-06 observation. View actual
   screenshot/canvas PNGs with an image tool at both 1x and 3x, covering both terrain
   neighborhoods, every animation frame and its anchored context. Timing samples
   establish observed playback; stills do not establish subjective live viewing.
3. Judge the BRIEF's material joins and planted-floor intent from actual pixels.
   A mechanical pass is not visual continuity. Give any defect a precise asset/frame,
   visible symptom, contextual evidence, likely correction and preservation scope.
   Do not edit pixels or metadata, nominate, review, accept, or submit provider work.

Write {WORK}/SPECIALIST-RESULT.json with operations (terrain/animation exact result
references), viewed_images (exact path/sha256 refs), findings, mechanical_vs_visual,
production_unchanged=true, acceptance_created=false, limitations and next_action.

Caller: independently read both COMPLETE saved operation results and specialist
report. Compare actual hashes/status/checks/cleanup and unchanged production state.
View the returned images too, including every frame and both neighborhoods at both
scales. Do not rerun merely to duplicate observation. Write {WORK}/CALLER-RESULT.json
with native_child, specialist_result, operations, viewed_images, independent_checks,
findings, production_unchanged=true, acceptance_created=false, scope, limitations and
next_action. Every reference is {{"path":"consumer-relative/path","sha256":"actual digest"}}.
Keep CF-09 actual generated-art revision and human acceptance separate and open.
"""
    for name in ("AGENTS.md", "SESSION.md"):
        (root / name).write_text(guidance, encoding="utf-8")
    (root / "DOMAIN-CONSUMERS.md").write_text(assignment, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete DOMAIN-CONSUMERS.md.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch.update(case="domain-consumers", artifact_roots=[WORK])
    write_json(destination / "launch.json", launch)
    identity = json.loads((destination / "identity.json").read_bytes())
    identity.update(case="domain-consumers", inputs=inventory(root, ("__pycache__",)),
                    baseline_production=inventory(root / ".pixl"), preparation=preparation,
                    configs={d: reference(root / INPUTS / f"{d}-config.json") for d in PROFILES},
                    runner=reference(Path(__file__)))
    write_json(destination / "identity.json", identity)
    (destination / "runner.py.txt").rename(destination / "setup-runner.py.txt")
    shutil.copyfile(__file__, destination / "runner.py.txt")
    return root


def retain(destination: Path):
    if (destination / "preservation.json").exists() or (destination / "outputs").exists():
        raise ValueError("Keep prior evidence; retain a new continuation separately")
    launch, identity = [json.loads((destination / name).read_bytes()) for name in ("launch.json", "identity.json")]
    root = Path(launch["cwd"])
    if (root / WORK).exists():
        shutil.copytree(root / WORK, destination / "outputs")
    current = inventory(root, ("__pycache__",))
    changed = [name for name, digest in identity["inputs"].items() if current.get(name) != digest]
    unexpected = [name for name in current if name in changed or
                  name not in identity["inputs"] and not name.startswith(WORK + "/")]
    if unexpected:
        with zipfile.ZipFile(destination / "unexpected-delta.zip", "x", zipfile.ZIP_DEFLATED) as archive:
            for name in unexpected:
                archive.write(root / name, name)
    write_json(destination / "preservation.json", {"changed": changed,
        "removed": [name for name in identity["inputs"] if name not in current],
        "new": {name: digest for name, digest in current.items() if name not in identity["inputs"]},
        "production_unchanged": inventory(root / ".pixl") == identity["baseline_production"]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("destination", type=Path)
    prep.add_argument("--host", choices=("codex", "claude"), required=True)
    prep.add_argument("--python", type=Path, default=readiness_case.DEFAULT_PYTHON)
    prep.add_argument("--package", type=Path)
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    execute.add_argument("--timeout", type=float, default=1200)
    args = parser.parse_args()
    if args.action == "prepare":
        print(prepare(args.destination, args.host, args.python, package=args.package))
    else:
        run(args.destination.resolve(), timeout=args.timeout)
        retain(args.destination.resolve())


if __name__ == "__main__":
    main()
