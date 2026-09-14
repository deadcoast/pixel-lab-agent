#!/usr/bin/env python3
"""03BATCH — Hearth and Road — local runner.

    python run.py --key <PIXELLAB_API_KEY>

One command: installs the two dependencies if missing, checks the balance, runs phase 1 (characters, objects, icons,
emblems, tiles, kits, vehicles, backgrounds, UI, font, portraits), then phase 2 (animations), then zips the results as
03batch_out3.zip next to this file. Safe to stop (Ctrl+C) and re-run — every finished job is skipped on resume.

Options:  --phase 1|2|all (default all)   --no-zip   --key can also come from the PIXELLAB_KEY environment variable
"""
import os, sys, time, argparse, subprocess, shutil, threading

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "pipeline")


def rule(ch="-", n=78): return ch * n


def ensure_deps():
    missing = []
    for mod, pkg in (("requests", "requests"), ("PIL", "pillow")):
        try: __import__(mod)
        except ImportError: missing.append(pkg)
    if missing:
        print(f"installing {', '.join(missing)} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *missing])


def main():
    ap = argparse.ArgumentParser(description="03BATCH local runner")
    ap.add_argument("--key", default=os.environ.get("PIXELLAB_KEY", ""), help="PixelLab API key")
    ap.add_argument("--phase", default="all", choices=["1", "2", "all"])
    ap.add_argument("--no-zip", action="store_true")
    a = ap.parse_args()
    if not a.key: sys.exit("no key: pass --key <PIXELLAB_API_KEY> or set PIXELLAB_KEY")
    ensure_deps()
    os.environ["PIXELLAB_KEY"] = a.key.strip()
    os.chdir(PIPE); sys.path.insert(0, PIPE)
    import pl2, content3 as c
    try: b0 = pl2.balance()
    except Exception as e: sys.exit(f"PixelLab unreachable or key refused: {str(e)[:200]}")
    n_obj = len(c.OBJECTS); n_anim = len(c.SIDE_WALK) + len(c.RUN) + len(c.NEW_WALK) + len(c.IDLE) + len(c.TEMPLATE)
    print(rule("="))
    print("  03BATCH  Hearth and Road                                 balance {:>6.0f} generations".format(b0))
    print(rule("="))
    print(f"  phase 1  {len(c.CHARS):>3} characters   {n_obj:>3} map objects   {len(c.OBJECTS8)} vehicles x8   {len(c.ICONS) + len(c.EMBLEMS):>3} icons+emblems")
    print(f"           {len(c.TILESETS):>3} tilesets     {len(c.ROADS):>3} road sets     {len(c.BUILDINGS)} building kits   {len(c.PLATES):>3} backgrounds")
    print(f"           {len(c.UI):>3} UI pieces    {len(c.FONTS):>3} font          {len(c.PORTRAITS):>2} portraits")
    print(f"  phase 2  {n_anim:>3} template animations (8 directions)   {len(c.CUSTOM)} custom hero beats (south)")
    print(f"  output   {os.path.join(PIPE, 'out3')}")
    print(f"  resume   re-run the same command at any time; finished jobs are skipped")
    print(rule())
    t0 = time.time()
    if a.phase in ("1", "all"):
        import batch4; print("PHASE 1 — creations"); batch4.main()
    if a.phase in ("2", "all"):
        import anim4; print("PHASE 2 — animations (one 8-direction set at a time; expect hours)"); anim4.main()
    b1 = pl2.balance()
    print(rule()); print(f"  done in {(time.time() - t0) / 60:.0f} min   spent {b0 - b1:.0f}   balance {b1:.0f}")
    if not a.no_zip:
        zpath = os.path.join(HERE, "03batch_out3")
        if os.path.exists(zpath + ".zip"): os.remove(zpath + ".zip")
        stage = os.path.join(HERE, "_stage"); shutil.rmtree(stage, ignore_errors=True); os.makedirs(stage)
        if os.path.isdir("out3"): shutil.copytree("out3", os.path.join(stage, "out3"))
        for f in ("pl3_state.json", "anim4_state.json"):
            if os.path.exists(f): shutil.copy(f, stage)
        shutil.make_archive(zpath, "zip", stage); shutil.rmtree(stage)
        print(f"  zipped   {zpath}.zip  ({os.path.getsize(zpath + '.zip') // 1024 // 1024} MB) — upload this back to the session")
    print(rule("="))


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nstopped — re-run the same command to resume")
