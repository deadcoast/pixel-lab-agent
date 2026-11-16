import json
rev = json.load(open("work/rev10.json", encoding="utf-8"))
recs = {r["id"]: r for r in rev["records"]} if isinstance(rev.get("records"), list) else rev["records"]
def fields(rid):
    r = recs[rid]
    return r.get("fields", r)
crit = json.load(open("deliverables/sample-request/sample-criteria.json", encoding="utf-8"))
out = crit["outputs"][0]
c = fields("c_sample")
print("intent == c_sample.li:", out["contract"]["intent"] == c["li"])
print("size == px:", out["contract"]["size"] == c["px"], "palette == pl:", out["contract"]["palette"] == c["pl"])
for q in out["criteria"]:
    f = fields(q["id"])
    print(q["id"], "check==ck:", q["check"] == f["ck"], "| domain", q["domain"], "==", f["dm"], "| mode", q["mode"], "==", f["md"], "| wh", f["wh"])
print("f_sample.rq:", [x["$ref"] if isinstance(x, dict) else x for x in fields("f_sample")["rq"]])
