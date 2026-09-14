p='batch.py'; s=open(p).read()
old='''                r = try_post(pl.animate, c["id"], template_animation_id=tpl, name=aname)'''
new='''                tpl_ = {"walk": "walk-6-frames", "breathing-idle": "rest-idle"}.get(tpl, tpl) if TEMPLATE.get(key.split("/")[1]) == "horse" else tpl
                r = try_post(pl.animate, c["id"], template_animation_id=tpl_, name=aname)'''
assert s.count(old)==1; s=s.replace(old,new)
old2='''                st["anims"][ak] = {"status": "processing", "type": tpl}; active += 8; log("queued anim", ak); save(st)'''
new2='''                st["anims"][ak] = {"status": "processing", "type": tpl_}; active += 8; log("queued anim", ak); save(st)'''
assert s.count(old2)==1; s=s.replace(old2,new2)
old3='''                try_post(pl.animate, c["id"], template_animation_id=a["type"], name=aname, directions=missing)'''
assert s.count(old3)==1
open(p,'w').write(s); print("patched")
