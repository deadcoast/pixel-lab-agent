import hashlib, json, re, sys
from datetime import datetime, timedelta, timezone
P = "deliverables/sample-request/criteria-schema-validation.json"
TARGET = "93643a34d32353b5471fd9943aed8bb3a0bf8cb48a94d8413c42635a1aaeb16a"
cur = open(P, "rb").read()
print("current", hashlib.sha256(cur).hexdigest())
text = cur.decode("utf-8")
m = re.search(r'"validated_at": "([^"]+)"', text)
assert m, "no validated_at"
start = datetime(2026, 11, 15, 22, 0, 0, tzinfo=timezone.utc)
for s in range(0, 4 * 3600):
    ts = (start + timedelta(seconds=s)).isoformat(timespec="seconds")
    cand = text.replace(m.group(1), ts, 1).encode("utf-8")
    if hashlib.sha256(cand).hexdigest() == TARGET:
        open(P, "wb").write(cand)
        print("restored with validated_at", ts)
        print("hash now", hashlib.sha256(open(P, "rb").read()).hexdigest())
        sys.exit(0)
print("NOT FOUND"); sys.exit(1)
