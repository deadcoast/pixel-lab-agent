p='batch.py'; s=open(p).read()
old='''        anims = [x for x in (d.get("animations") or []) if x.get("animation_type") == a["type"] or x.get("display_name") == aname]
        if anims and all(len(dd.get("frames", [])) > 0 for dd in anims[0]["directions"]) and len(anims[0]["directions"]) >= 8:
            fac, name = ck.split("/"); save_anim(anims[0], f"{OUT}/{fac}/{name}/{aname}", name, aname); a["status"] = "done"; log("anim done", key)'''
new='''        anims = [x for x in (d.get("animations") or []) if x.get("animation_type") == a["type"] or x.get("display_name") == aname]
        a.setdefault("t0", time.time()); age = time.time() - a["t0"]
        if anims and all(len(dd.get("frames", [])) > 0 for dd in anims[0]["directions"]) and len(anims[0]["directions"]) >= 8:
            fac, name = ck.split("/"); save_anim(anims[0], f"{OUT}/{fac}/{name}/{aname}", name, aname); a["status"] = "done"; log("anim done", key)
        elif anims and age > 600 and len(anims[0]["directions"]) >= 6:
            have = {dd["direction"] for dd in anims[0]["directions"]}; missing = [dd for dd in pl.DIRS if dd not in have]
            if missing and not a.get("retried"):
                try_post(pl.animate, c["id"], template_animation_id=a["type"], name=aname, directions=missing); a["retried"] = True; a["t0"] = time.time(); log("re-queued missing", key, missing)
            elif not missing or a.get("retried"):
                fac, name = ck.split("/"); save_anim(anims[0], f"{OUT}/{fac}/{name}/{aname}", name, aname); a["status"] = "done"; log("anim done (partial)", key, sorted(have))'''
assert s.count(old)==1; s=s.replace(old,new); open(p,'w').write(s); print("patched")
