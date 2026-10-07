"""Contrôle mécanique d'un épisode avant push (les règles techniques vivent ici, pas dans les consignes)."""
import json, sys
ep = json.load(open(sys.argv[1])); errs = []; queries = []
for i, s in enumerate(ep["scenes"]):
    k, w = s.get("kind"), len(s.get("text", "").split())
    if not k:
        shots = s.get("shots") or [s]
        if w / 2.6 > 6 and len(shots) < round(w / 2.6 / 5): errs.append(f"scène {i} : {len(shots)} plan(s) pour ~{w/2.6:.0f} s (le moteur complétera, mais varier les requêtes)")
        queries += [x["clip"] for x in shots if x.get("clip", "").startswith("pixabay:")]
    if k == "diagram":
        for e in s["elements"]:
            if e.get("type") in ("curve",) and len(e.get("pts", [])) != 3: errs.append(f"scène {i} : courbe à {len(e['pts'])} points (3 requis)")
    for line in s.get("fact", "").split("\\N"):
        if len(line) > 45: errs.append(f"scène {i} : ligne d'encart > 45 car.")
dups = {q for q in queries if queries.count(q) > 1}
if dups: errs.append(f"requêtes Pixabay en double : {sorted(dups)}")
if len(ep.get("youtube", {}).get("title", "")) > 60: errs.append("titre YouTube > 60 car.")
print("\n".join(errs) or "OK"); sys.exit(1 if any("courbe" in e or "titre" in e for e in errs) else 0)
