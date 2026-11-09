"""Check actual recorded playback and destination pixels, independent of judgments."""
import base64
import io
import json
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

work = Path(__file__).resolve().parent
project = work.parent.parent
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
digest = lambda p: sha256(p.read_bytes()).hexdigest()
observed = read(work / "playback-observation-03.json")
checks = []


def check(ok, name):
    checks.append({"check": name, "pass": bool(ok)})


def equal(left, right):
    return all(high == 0 for _, high in ImageChops.difference(left, right).getextrema())


def expected(path, frame, scale, gray=False):
    source = Image.open(project / path).convert("RGBA")
    crop = source.crop((frame * 16, 0, frame * 16 + 16, 16))
    result = Image.new("RGBA", (16, 16), "#172336")
    result.alpha_composite(crop)
    result = result.resize((16 * scale, 16 * scale), Image.Resampling.NEAREST)
    if gray:
        # The review page's stated Rec.709 comparison, including its background.
        result.putdata([(round(.2126*r+.7152*g+.0722*b),)*3+(a,) for r,g,b,a in result.getdata()])
    return result


for row in observed["assets"].values():
    check(digest(project / row["path"]) == row["sha256"], "reviewed asset hash: " + row["path"])
transitions = observed["transitions"]
frames = [v["frame"] for v in transitions]
check(frames == [i % 4 for i in range(17)], "four complete ordered cycles including fourth-to-first wraps")
check(observed["complete_cycles"] == 4, "four observed wraps")
check(len(observed["samples"]) >= 80, "playback has dense actual requestAnimationFrame observations")
out = work / "observed-views"
out.mkdir(exist_ok=True)
for i, transition in enumerate(transitions):
    for view in transition["views"]:
        data = base64.b64decode(view["png"].split(",",1)[1])
        path = out / f"transition-{i:02d}-{view['scale']}x-{'gray' if view['gray'] else 'color'}.png"
        path.write_bytes(data)
        actual = Image.open(io.BytesIO(data)).convert("RGBA")
        check(equal(actual, expected(observed["assets"]["running"]["path"],transition["frame"],view["scale"],view["gray"])), "actual playback canvas: " + path.name)

motion = read(work / "destination-01/motion.json")
phase_results = []
for phase in motion["phases"]:
    seen=set()
    for sample in phase["samples"]:
        check(sample["reduced"] == phase["reduced"], "actual media preference: " + phase["name"])
        for cell in sample["cells"]:
            seen.add(cell["frame"])
            image_path=work / "destination-01" / cell["image"]["path"]
            check(digest(image_path)==cell["image"]["sha256"],"destination retained pixel hash")
            check(equal(Image.open(image_path).convert("RGBA"),expected(cell["path"],cell["frame"],3)),"destination pixel/frame correspondence")
            check(cell["label"]=="Working" and cell["smoothing"] is False and cell["width"]==cell["height"]==48,"destination label/sampling/size")
            check(not phase["reduced"] or cell["frame"]==0,"reduced mode stationary frame zero")
    elapsed=phase["samples"][-1]["at"]-phase["samples"][0]["at"]
    check(seen==({0} if phase["reduced"] else {0,1,2,3}) and elapsed>=800,"destination phase coverage: "+phase["name"])
    phase_results.append({"name":phase["name"],"frames":sorted(seen),"samples":len(phase["samples"]),"elapsed_ms":elapsed})

destination=read(work / "destination-checks.json")
check(destination["status"]=="pass","existing destination checker")
sheet=Image.open(project/observed["assets"]["running"]["path"]).convert("RGBA")
cells=[sheet.crop((16*i,0,16*i+16,16)) for i in range(4)]
turns=[equal(cells[(i+1)%4],cells[i].transpose(Image.Transpose.ROTATE_270)) for i in range(4)]
# A measurement of this chosen recipe, not an owner rule for every animation.
measurements={"clockwise_quarter_turn_matches":turns,"alpha_boxes":[list(c.getchannel('A').getbbox()) for c in cells],"alpha_mass":[sum(c.getchannel('A').getdata()) for c in cells]}
intervals=[round(transitions[i]["at"]-transitions[i-1]["at"],3) for i in range(1,len(transitions))]
result={"status":"pass" if all(x["pass"] for x in checks) else "fail","checks":len(checks),"failures":[x for x in checks if not x["pass"]],"destination_checks":len(destination["observations"]),"playback_samples":len(observed["samples"]),"transition_frames":frames,"transition_intervals_ms":intervals,"measurements":measurements,"destination_phases":phase_results,"scope":"Observed frame/canvas and retained-file checks; qualitative motion and family verdicts are authored separately after image review."}
(work/"review-checks.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
# User-facing preview from the actual observed exposures; raw captures remain above.
preview=[Image.open(out/f"transition-{i:02d}-3x-color.png").convert("RGB") for i in range(4)]
preview[0].save(work/"working-preview.gif",save_all=True,append_images=preview[1:],duration=100,loop=0)
print(json.dumps(result,indent=2))
assert result["status"]=="pass"
