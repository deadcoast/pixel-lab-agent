import json, time, os, plclient as pl
CH = {
 "diefenbunker/soldier": ("post-apocalyptic bunker soldier, faded olive-drab military fatigues generations old and patched, plate carrier of old canvas webbing, worn combat helmet with a small red maple leaf painted on the side, black C8 carbine rifle held at the ready, pale skin from a life underground, alert clean-shaven face, olive drab canvas tan and gunmetal palette", "mannequin"),
 "diefenbunker/salvager": ("post-apocalyptic bunker engineer surfacing in work gear, grey coveralls with tool belt and knee pads, welding mask pushed up on the head, heavy gloves, headlamp, a pry bar in hand, old military insignia pin on the collar, pale skin, older tired face, grey coverall gunmetal and one small red pin palette", "mannequin"),
 "lamplighter/nomad": ("post-apocalyptic exiled wanderer, long ragged dark hooded cloak over dusty travel clothes, hood up shadowing the face, a shuttered iron lantern held low in one hand with the shutter half closed, walking staff, road-worn boots, small pack, dark charcoal dust brown and a faint dim lantern glow palette, lonely upright silhouette", "mannequin"),
 "waylight/mail_worker": ("post-apocalyptic city mail worker, slate-blue postal tunic with a brass button, white sleeves rolled, canvas mail sack over one shoulder bulging with letters, flat cap, sturdy shoes, young eager face, slate blue bone white and brass palette, clean simple silhouette", "mannequin"),
 "waylight/hauler": ("post-apocalyptic courier hauler, stocky strong figure bent under an enormous towering pack of bundled cargo strapped with rope, slate-blue tunic under a leather harness, walking staff, wide-brimmed hat, thick boots, slate blue hide brown and canvas tan palette, huge pack silhouette", "mannequin"),
 "waylight/donkey": ("pack donkey, grey-brown coat, long ears, laden with two bulging canvas panniers strapped over a wooden pack saddle, rope halter, patient head low, dust grey and canvas tan palette", "horse"),
}
st = json.load(open("side_state.json")) if os.path.exists("side_state.json") else {}
for key, (desc, tpl) in CH.items():
    if key in st: continue
    while True:
        try:
            r = pl.create_character(desc, size=64, seed=7, template=tpl, name=key); st[key] = {"id": r["character_id"], "status": "processing"}; json.dump(st, open("side_state.json", "w"), indent=1); print("queued", key, flush=True); break
        except RuntimeError as e:
            if "429" in str(e): time.sleep(30)
            else: raise
    # wait for this one before queueing the next so we hold at most one slot
    while True:
        d = pl.character(st[key]["id"])
        if d.get("status") == "completed" and d.get("rotation_urls"):
            fac, name = key.split("/"); pl.save_rotations(d, f"out/{fac}/{name}", name); st[key]["status"] = "done"; json.dump(st, open("side_state.json", "w"), indent=1); print("done", key, flush=True); break
        if d.get("status") == "failed": st[key]["status"] = "failed"; print("FAILED", key); break
        time.sleep(20)
print("SIDE DONE")
