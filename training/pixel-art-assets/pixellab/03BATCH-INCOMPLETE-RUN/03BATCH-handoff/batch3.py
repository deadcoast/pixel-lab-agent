"""Phase 2 — animations for the Convergence batch. Template anims (8 dirs, 1 gen/dir) queued one at a time under the cap;
custom v3 hero animations (south only) run alongside in the spare slots."""
import os, sys, json, time, traceback
import pl2, plclient as pl
from batch import save_anim
from PIL import Image

CAP = 10
STATE = "batch3_state.json"

# (character key in pl2_state or legacy out/, animation name, template id)
HORSE = {"farkeeper/captain", "animals/draft_horse", "animals/light_horse"}
NEW = ["diefenbunker/douglas_reed", "diefenbunker/sarah_oconnel", "diefenbunker/jimmy_butler", "diefenbunker/enforcement_trooper", "diefenbunker/work_crew",
       "lamplighter/sniper", "lamplighter/marksman", "lamplighter/nomad_hauler", "lamplighter/nomad_elder",
       "reaper/overseer", "reaper/household_woman", "reaper/child", "reaper/captive", "waylight/haven_courier",
       "cannibal/hunter", "cannibal/hearth_keeper", "cannibal/lookout", "raider/rover", "raider/bandit", "rebel/militiaman", "rebel/speaker",
       "flamekeeper/furnace_warden", "flamekeeper/stoker", "irongiant/frame_pilot", "irongiant/working_frame",
       "waylight/mason", "waylight/forrester", "waylight/path_presser", "farkeeper/captain", "animals/draft_horse", "animals/light_horse"]
IDLE = ["diefenbunker/douglas_reed", "diefenbunker/sarah_oconnel", "diefenbunker/jimmy_butler", "lamplighter/sniper", "reaper/overseer", "reaper/captive",
        "cannibal/hunter", "cannibal/hearth_keeper", "flamekeeper/furnace_warden", "irongiant/frame_pilot", "irongiant/working_frame", "farkeeper/captain"]
ATTACK = [("farkeeper/spearman", "attack", "attack"), ("farkeeper/berserker", "attack", "attack"), ("farkeeper/pugugly", "punch", "cross-punch"), ("farkeeper/pugugly", "uppercut", "surprise-uppercut"),
          ("reaper/second", "attack", "attack"), ("reaper/admiral", "attack", "attack"), ("reaper/blackguard", "attack", "attack"), ("reaper/raider", "attack", "attack"),
          ("smoke/torch", "attack", "attack"), ("smoke/smoker", "attack", "attack"), ("diefenbunker/soldier", "attack", "attack"), ("diefenbunker/jimmy_butler", "attack", "attack"),
          ("lamplighter/sniper", "crouch", "crouching"), ("cannibal/hunter", "attack", "attack"), ("rebel/militiaman", "attack", "attack")]
STORY = [("party/postman", "pickup", "picking-up"), ("lamplighter/nomad_hauler", "haul", "pull-heavy-object"), ("waylight/path_presser", "push", "pushing"),
         ("reaper/captive", "sadwalk", "sad-walk"), ("reaper/captive", "getup", "getting-up"), ("diefenbunker/work_crew", "dig", "pull-heavy-object")]
CUSTOM = [("lamplighter/sniper", "aim", "kneels down on one knee, raises the scoped rifle to the shoulder and aims steadily, cloak settling"),
          ("party/postman", "handover", "holds out a letter with both hands toward the viewer and gives a small deliberate bow, then straightens"),
          ("diefenbunker/sarah_oconnel", "weld", "crouches and welds a seam with the torch, bright sparks flying, then lifts the goggles"),
          ("cannibal/hearth_keeper", "stir", "sets the pot down and stirs it slowly with the ladle, then looks up")]


def cid_of(key, st2, legacy):
    if key in st2["jobs"] and st2["jobs"][key]["type"] == "char": return st2["jobs"][key]["id"]
    if key in legacy["chars"]: return legacy["chars"][key]["id"]
    if key.startswith("party/"): return legacy["chars"].get(key, {}).get("id")
    return None


def out_dir(key):
    fac, name = key.split("/")
    return (f"out2/{fac}/{name}" if os.path.isdir(f"out2/{fac}/{name}") else f"out/{fac}/{name}"), name


def main():
    st2 = pl2.load(); legacy = json.load(open("batch_state.json"))
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"anims": {}}
    def save(): json.dump(st, open(STATE, "w"), indent=1)
    queue = []
    for k in NEW: queue.append((k, "walk", "walk-6-frames" if k in HORSE else "walk", None))
    for k in IDLE: queue.append((k, "idle", "rest-idle" if k in HORSE else "breathing-idle", None))
    for k, n, t in ATTACK: queue.append((k, n, t, None))
    for k, n, t in STORY: queue.append((k, n, t, None))
    customs = list(CUSTOM)
    pl2.log("queue", len(queue), "template anims,", len(customs), "custom")
    while True:
        # refresh
        active = 0
        for ak, a in st["anims"].items():
            if a["status"] != "processing": continue
            key = a["key"]; cid = a["cid"]
            try: d = pl.character(cid)
            except Exception as e: pl2.log("poll error", ak, str(e)[:120]); active += a["jobs"]; continue
            anims = [x for x in (d.get("animations") or []) if x.get("display_name") == a["name"] or x.get("animation_type") == a["type"]]
            age = time.time() - a["t0"]
            if anims:
                dirs = anims[0]["directions"]; have = {dd["direction"] for dd in dirs if dd.get("frames")}
                need = set(a["dirs"])
                if need <= have:
                    od, name = out_dir(key); save_anim(anims[0], f"{od}/{a['name']}", name, a["name"]); a["status"] = "done"; pl2.log("anim done", ak); save(); continue
                if age > 720 and len(have) >= max(1, len(need) - 2):
                    od, name = out_dir(key); save_anim(anims[0], f"{od}/{a['name']}", name, a["name"]); a["status"] = "done"; pl2.log("anim done (partial)", ak, sorted(have)); save(); continue
            if age > 1500: a["status"] = "failed"; pl2.log("anim TIMEOUT", ak); save(); continue
            active += a["jobs"]
        # queue customs in spare slots (1 job each)
        while customs and active + 1 <= CAP:
            key, name, action = customs.pop(0); cid = cid_of(key, st2, legacy)
            if not cid: pl2.log("no cid", key); continue
            try:
                pl2.post("/animate-character", {"character_id": cid, "mode": "v3", "action_description": action, "animation_name": name, "directions": ["south"], "frame_count": 8})
                st["anims"][f"{key}/{name}"] = {"key": key, "cid": cid, "name": name, "type": None, "dirs": ["south"], "jobs": 1, "status": "processing", "t0": time.time()}; active += 1; pl2.log("queued custom", key, name); save()
            except Exception as e: pl2.log("custom error", key, name, str(e)[:200])
        # queue the next template anim if 8 slots are free
        while queue and active + 8 <= CAP:
            key, name, tpl, _ = queue.pop(0); cid = cid_of(key, st2, legacy)
            if not cid: pl2.log("no cid", key); continue
            ak = f"{key}/{name}"
            if ak in st["anims"]: continue
            try:
                pl2.post("/animate-character", {"character_id": cid, "template_animation_id": tpl, "mode": "template", "animation_name": name})
                st["anims"][ak] = {"key": key, "cid": cid, "name": name, "type": tpl, "dirs": pl.DIRS, "jobs": 8, "status": "processing", "t0": time.time()}; active += 8; pl2.log("queued", ak, tpl); save()
            except Exception as e:
                pl2.log("queue error", ak, str(e)[:200]); st["anims"][ak] = {"key": key, "cid": cid, "name": name, "type": tpl, "dirs": [], "jobs": 0, "status": "failed", "t0": time.time()}; save()
        if not queue and not customs and not any(a["status"] == "processing" for a in st["anims"].values()):
            pl2.log("PHASE 2 DONE", pl2.balance()); return
        time.sleep(30)


if __name__ == "__main__":
    try: main()
    except Exception: traceback.print_exc()
