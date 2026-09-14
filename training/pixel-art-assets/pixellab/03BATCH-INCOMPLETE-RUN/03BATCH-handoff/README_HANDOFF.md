# 03BATCH handoff — run this in a session whose sandbox can reach api.pixellab.ai

This folder is the complete PixelLab pipeline for the Waylight project, with the 01BATCH (out/) and 02BATCH (out2/) results
that 03BATCH reads from (portrait sources, story-plate sprites, character IDs), and the 03BATCH spec.

    pip install requests pillow --break-system-packages   # if missing
    cd pl
    python3 -c "import pl2; print(pl2.balance())"          # must print ~1830; if it raises ProxyError, the sandbox is on a restricted allowlist
    nohup python3 batch4.py > batch4.log 2>&1 &            # phase 1: characters, objects, icons, tiles, kits, vehicles, backgrounds, UI, font, portraits (~40 min)
    # when batch4.log says "PHASE 1 DONE":
    nohup python3 anim4.py  > anim4.log  2>&1 &            # phase 2: 57 template animations + 7 custom beats, one 8-direction anim at a time (~5 h)
    # packaging, any time after phase 1 (re-run as animations land):
    python3 plates3.py && python3 codex3.py && python3 package3.py   # → /mnt/user-data/outputs/03batch + 03batch.zip

Key: `.env` (PIXELLAB_KEY=...). If the environment supplies the key as an API credential instead, delete `.env` and remove the
Authorization header in plclient.py `H`.
Never copy `.env` or the key into any delivered file — package3.py greps for it and aborts.
Files: content3.py (spec) · inventory.json (everything already generated — the runners refuse duplicates) · batch4.py / anim4.py
(runners, resumable) · plates3.py · codex3.py · package3.py · pl2.py / plclient.py / batch.py (framework) · pl2_state.json,
batch_state.json, side_state.json, batch3_state.json (character IDs from earlier batches).
