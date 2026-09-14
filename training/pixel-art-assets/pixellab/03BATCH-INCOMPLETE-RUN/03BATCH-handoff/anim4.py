"""03BATCH phase 2 — animations. One 8-direction template animation at a time under the 10-job cap; custom v3 hero beats
(south only) fill the spare slots. Partial sets accepted after 12 min with ≥6 directions; one re-queue of missing directions
is left to the packager. Everything is written under out3/<faction>/<name>/<anim>/."""
import os, sys, json, time, traceback
import pl2, plclient as pl
from batch import save_anim
from content3 import HORSE, SIDE_WALK, RUN, NEW_WALK, IDLE, TEMPLATE, CUSTOM

CAP = 10
STATE = "anim4_state.json"
INV = json.load(open("inventory.json"))
RUN_FALLBACK = ["running-8-frames", "running-6-frames", "running-4-frames", "run", "running"]


def load_states():
    st3 = json.load(open("pl3_state.json")) if os.path.exists("pl3_state.json") else {"jobs": {}}
    st2 = json.load(open("pl2_state.json")); legacy = json.load(open("batch_state.json")); side = json.load(open("side_state.json"))
    return st3, st2, legacy, side


def cid_of(key, st3, st2, legacy, side):
    for st in (st3, st2):
        j = st["jobs"].get(key)
        if j and j.get("type") == "char" and j.get("status") == "done": return j["id"]
    if key in legacy["chars"]: return legacy["chars"][key]["id"]
    if key in side: return side[key]["id"]
    return None


def out_dir(key):
    fac, name = key.split("/"); return f"out3/{fac}/{name}", name


def tpl_for(key, base):
    if key in HORSE: return {"walk": "walk-6-frames", "breathing-idle": "rest-idle"}.get(base, base)
    return base


def main():
    st3, st2, legacy, side = load_states()
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"anims": {}}
    def save(): json.dump(st, open(STATE, "w"), indent=1)
    queue = []
    for k in SIDE_WALK: queue.append((k, "walk", tpl_for(k, "walk")))
    for k in RUN: queue.append((k, "run", "running-8-frames"))
    for k in NEW_WALK: queue.append((k, "walk", tpl_for(k, "walk")))
    for k in IDLE: queue.append((k, "idle", tpl_for(k, "breathing-idle")))
    for k, n, t in TEMPLATE: queue.append((k, n, t))
    # refuse anything already generated in an earlier batch; drop characters that do not exist and are not being made
    def known(k):
        if cid_of(k, st3, st2, legacy, side): return True
        j = st3["jobs"].get(k); return bool(j and j.get("status") == "processing")
    queue = [(k, n, t) for k, n, t in queue if INV["anims"].get(f"{k}/{n}") != "done" and known(k)]
    customs = [(k, n, a) for k, n, a in CUSTOM if INV["anims"].get(f"{k}/{n}") != "done" and known(k)]
    pl2.log("queue", len(queue), "template anims,", len(customs), "custom; balance", pl2.balance())
    b0 = pl2.balance()
    while True:
        st3, st2, legacy, side = load_states()
        active = 0
        for ak, a in st["anims"].items():
            if a["status"] != "processing": continue
            key = a["key"]; cid = a["cid"]
            try: d = pl.character(cid)
            except Exception as e: pl2.log("poll error", ak, str(e)[:120]); active += a["jobs"]; continue
            anims = [x for x in (d.get("animations") or []) if x.get("display_name") == a["name"] or (a["type"] and x.get("animation_type") == a["type"])]
            age = time.time() - a["t0"]
            if anims:
                dirs = anims[0]["directions"]; have = {dd["direction"] for dd in dirs if dd.get("frames")}
                need = set(a["dirs"])
                if need <= have:
                    od, name = out_dir(key); save_anim(anims[0], f"{od}/{a['name']}", name, a["name"]); a["status"] = "done"; pl2.log("anim done", ak); save(); continue
                if age > 720 and len(have) >= max(1, len(need) - 2):
                    od, name = out_dir(key); save_anim(anims[0], f"{od}/{a['name']}", name, a["name"]); a["status"] = "done"; a["partial"] = sorted(need - have); pl2.log("anim done (partial)", ak, sorted(have)); save(); continue
            if age > 1500: a["status"] = "failed"; pl2.log("anim TIMEOUT", ak); save(); continue
            active += a["jobs"]
        # customs in spare slots
        while customs and active + 1 <= CAP:
            key, name, action = customs.pop(0); cid = cid_of(key, st3, st2, legacy, side)
            if not cid: pl2.log("no cid (yet)", key, name); customs.append((key, name, action)); break
            try:
                pl2.post("/animate-character", {"character_id": cid, "mode": "v3", "action_description": action, "animation_name": name, "directions": ["south"], "frame_count": 8})
                st["anims"][f"{key}/{name}"] = {"key": key, "cid": cid, "name": name, "type": None, "dirs": ["south"], "jobs": 1, "status": "processing", "t0": time.time()}; active += 1; pl2.log("queued custom", key, name); save()
            except Exception as e: pl2.log("custom error", key, name, str(e)[:300])
        # next template anim when 8 slots are free (keep a reserve of 120 generations)
        if queue and active + 8 <= CAP:
            try:
                if pl2.balance() < 120: pl2.log("RESERVE reached — dropping", len(queue), "template anims and", len(customs), "customs"); queue.clear(); customs.clear()
            except Exception: pass
        while queue and active + 8 <= CAP:
            key, name, tpl = queue.pop(0); cid = cid_of(key, st3, st2, legacy, side)
            ak = f"{key}/{name}"
            if ak in st["anims"] and st["anims"][ak]["status"] != "failed": continue
            if not cid:
                j = st3["jobs"].get(key)
                if j and j.get("status") == "failed": pl2.log("character failed, anim dropped", ak); continue
                pl2.log("no cid (yet)", key); queue.append((key, name, tpl)); break
            tries = RUN_FALLBACK if tpl == "running-8-frames" else [tpl]
            ok = False
            for t in tries:
                try:
                    pl2.post("/animate-character", {"character_id": cid, "template_animation_id": t, "mode": "template", "animation_name": name})
                    st["anims"][ak] = {"key": key, "cid": cid, "name": name, "type": t, "dirs": pl.DIRS, "jobs": 8, "status": "processing", "t0": time.time()}; active += 8; pl2.log("queued", ak, t); save(); ok = True; break
                except Exception as e:
                    msg = str(e); pl2.log("queue error", ak, t, msg[:400])
                    if "429" in msg or "concurrent" in msg: time.sleep(30); queue.insert(0, (key, name, tpl)); ok = True; break
            if not ok: st["anims"][ak] = {"key": key, "cid": cid, "name": name, "type": tpl, "dirs": [], "jobs": 0, "status": "failed", "t0": time.time()}; save()
        if not queue and not customs and not any(a["status"] == "processing" for a in st["anims"].values()):
            b1 = pl2.balance(); pl2.log("PHASE 2 DONE — spent", b0 - b1, "balance", b1); st["spent"] = b0 - b1; save(); return
        if active == 0 and (queue or customs):
            idle_loops = st.get("idle_loops", 0) + 1; st["idle_loops"] = idle_loops
            if idle_loops > 240: pl2.log("giving up on characters that never arrived:", [k for k, _, _ in queue], [k for k, _, _ in customs]); queue.clear(); customs.clear()
        else: st["idle_loops"] = 0
        time.sleep(30)


if __name__ == "__main__":
    try: main()
    except Exception: traceback.print_exc()
