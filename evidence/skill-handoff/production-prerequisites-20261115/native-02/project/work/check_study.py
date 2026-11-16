"""Check sources/reference-observations.md against criterion q_study_complete."""
import hashlib, json

study = open("sources/reference-observations.md", encoding="utf-8").read()

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

ha, hb = sha("reference.png"), sha("reference-b.png")

checks = [
    ("states reference.png identity",
     ha[:8] in study and ha[-5:] in study),
    ("states reference-b.png identity",
     hb[:8] in study and hb[-6:] in study),
    ("states the exact pixel difference count",
     "180 pixels" in study),
    ("states the nature of the difference",
     "#25354A" in study and "#56B5BC" in study and "substitution" in study),
    ("names unresolved projection", "Projection." in study),
    ("names unresolved role differentiation", "Scout and medic differentiation." in study),
    ("names unresolved display scale or engine",
     "display scale" in study.lower()),
    ("names unresolved animation", "Animation poses" in study),
]

result = {
    "criterion": "q_study_complete",
    "candidate": "x_study",
    "candidate_path": "sources/reference-observations.md",
    "candidate_sha256": sha("sources/reference-observations.md"),
    "reference_a_sha256": ha,
    "reference_b_sha256": hb,
    "mode": "local",
    "checks": [{"name": n, "passed": bool(p)} for n, p in checks],
    "outcome": "pass" if all(p for _, p in checks) else "fail",
    "note": "Textual completeness check only. It does not evaluate whether the study is "
            "artistically correct, and it supplies no visual or engine acceptance.",
}
json.dump(result, open("evidence/study-completeness.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(result, indent=1))
