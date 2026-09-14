"""Polls api.pixellab.ai through the session proxy; when a balance call succeeds, launches batch4.py (phase 1) and then
anim4.py (phase 2) as detached background runners, and exits. Logs every probe to watchdog.log."""
import os, sys, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pl2

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

n = 0
while True:
    n += 1
    try:
        b = pl2.balance(); log("REACHABLE — balance", b); break
    except Exception as e:
        if n % 10 == 1: log("blocked:", str(e).split("(Caused by")[-1][:90])
    time.sleep(60)

open("RUNNING", "w").write(time.strftime("%Y-%m-%d %H:%M:%S"))
p1 = subprocess.Popen(["nohup", "python3", "batch4.py"], stdout=open("batch4.log", "a"), stderr=subprocess.STDOUT)
log("phase 1 started, pid", p1.pid)
p1.wait()
log("phase 1 exited", p1.returncode)
p2 = subprocess.Popen(["nohup", "python3", "anim4.py"], stdout=open("anim4.log", "a"), stderr=subprocess.STDOUT)
log("phase 2 started, pid", p2.pid)
