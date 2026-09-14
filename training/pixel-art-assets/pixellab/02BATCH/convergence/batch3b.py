"""follow-up: combat templates that exist for the mannequin rig, plus deaths (permadeath, §16)."""
import json, os, time, traceback
import pl2, plclient as pl
import batch3
from batch import save_anim

ATTACK2 = [("farkeeper/spearman", "thrust", "lead-jab"), ("farkeeper/berserker", "swing", "throw-object"), ("reaper/second", "cut", "lead-jab"), ("reaper/admiral", "cut", "lead-jab"),
           ("reaper/blackguard", "punch", "cross-punch"), ("reaper/raider", "strike", "lead-jab"), ("smoke/torch", "flame", "fireball"), ("smoke/smoker", "punch", "cross-punch"),
           ("diefenbunker/soldier", "ready", "fight-stance-idle-8-frames"), ("diefenbunker/jimmy_butler", "ready", "fight-stance-idle-8-frames"), ("cannibal/hunter", "thrust", "lead-jab"),
           ("rebel/militiaman", "ready", "fight-stance-idle-8-frames"), ("farkeeper/longbowman", "ready", "fight-stance-idle-8-frames"), ("lamplighter/marksman", "ready", "fight-stance-idle-8-frames")]
DEATH = [("party/postman", "death", "falling-back-death"), ("farkeeper/spearman", "death", "falling-back-death"), ("reaper/raider", "death", "falling-back-death"),
         ("smoke/torch", "death", "falling-back-death"), ("diefenbunker/soldier", "death", "falling-back-death"), ("reaper/conscript", "death", "falling-back-death"),
         ("reaper/captive", "hit", "taking-punch")]


def cid_of(key, st2, legacy, side):
    if key in st2["jobs"] and st2["jobs"][key]["type"] == "char": return st2["jobs"][key]["id"]
    if key in legacy["chars"]: return legacy["chars"][key]["id"]
    if key in side: return side[key]["id"]
    return None


def main():
    st2 = pl2.load(); legacy = json.load(open("batch_state.json")); side = json.load(open("side_state.json"))
    st = json.load(open(batch3.STATE))
    def save(): json.dump(st, open(batch3.STATE, "w"), indent=1)
    queue = [(k, n, t) for k, n, t in ATTACK2 + DEATH if f"{k}/{n}" not in st["anims"] or st["anims"][f"{k}/{n}"]["status"] == "failed"]
    pl2.log("queue", len(queue))
    while True:
        active = 0
        for ak, a in st["anims"].items():
            if a["status"] != "processing": continue
            try: d = pl.character(a["cid"])
            except Exception as e: active += a["jobs"]; continue
            anims = [x for x in (d.get("animations") or []) if x.get("display_name") == a["name"] or x.get("animation_type") == a["type"]]
            age = time.time() - a["t0"]
            if anims:
                have = {dd["direction"] for dd in anims[0]["directions"] if dd.get("frames")}; need = set(a["dirs"])
                if need <= have or (age > 720 and len(have) >= len(need) - 2):
                    od, name = batch3.out_dir(a["key"]); save_anim(anims[0], f"{od}/{a['name']}", name, a["name"]); a["status"] = "done"; pl2.log("anim done", ak, "" if need <= have else "(partial)"); save(); continue
            if age > 1500: a["status"] = "failed"; pl2.log("anim TIMEOUT", ak); save(); continue
            active += a["jobs"]
        while queue and active + 8 <= 10:
            key, name, tpl = queue.pop(0); cid = cid_of(key, st2, legacy, side); ak = f"{key}/{name}"
            if not cid: pl2.log("no cid", key); continue
            try:
                pl2.post("/animate-character", {"character_id": cid, "template_animation_id": tpl, "mode": "template", "animation_name": name})
                st["anims"][ak] = {"key": key, "cid": cid, "name": name, "type": tpl, "dirs": pl.DIRS, "jobs": 8, "status": "processing", "t0": time.time()}; active += 8; pl2.log("queued", ak, tpl); save()
            except Exception as e: pl2.log("queue error", ak, str(e)[:160]); st["anims"][ak] = {"key": key, "cid": cid, "name": name, "type": tpl, "dirs": [], "jobs": 0, "status": "failed", "t0": time.time()}; save()
        if not queue and not any(a["status"] == "processing" for a in st["anims"].values()):
            pl2.log("PHASE 2B DONE", pl2.balance()); return
        time.sleep(30)


if __name__ == "__main__":
    try: main()
    except Exception: traceback.print_exc()
