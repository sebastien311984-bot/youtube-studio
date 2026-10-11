"""Contrôle mécanique d'un épisode avant push (les règles techniques vivent ici, pas dans les consignes)."""
import json, sys
ep = json.load(open(sys.argv[1])); errs = []; queries = []
for i, s in enumerate(ep["scenes"]):
    k, w = s.get("kind"), len(s.get("text", "").split())
    if k and k not in ("intro", "diagram", "stat", "scale", "timeline", "versus", "quiz", "kinetic", "rank", "annotate", "beforeafter", "outro", "zoomto", "layers"): errs.append(f"scène {i} : type inconnu « {k} » (titre = option, pas un type)")
    if not k and not (s.get("clip") or s.get("shots")): errs.append(f"scène {i} : plan réel sans image (clip/shots)")
    if k == "diagram":
        for el in s.get("elements", []):
            if el.get("type") in ("circle", "arc") and not ((el.get("c") or el.get("center")) and "r" in el): errs.append(f"scène {i} : schéma — cercle/arc sans centre « c » ou rayon « r »")
            if el.get("type") in ("line", "arrow") and not ("from" in el and "to" in el): errs.append(f"scène {i} : schéma — ligne/flèche sans « from »/« to »")
            if el.get("type") == "curve" and len(el.get("pts", [])) != 3: errs.append(f"scène {i} : schéma — courbe sans 3 points « pts »")
    if not k:
        shots = s.get("shots") or [s]
        if w / 2.6 > 6 and len(shots) < round(w / 2.6 / 5): errs.append(f"scène {i} : {len(shots)} plan(s) pour ~{w/2.6:.0f} s (le moteur complétera, mais varier les requêtes)")
        queries += [x["clip"] for x in shots if x.get("clip", "").startswith("pixabay:")]
    if k == "diagram":
        for e in s["elements"]:
            if e.get("type") in ("curve",) and len(e.get("pts", [])) != 3: errs.append(f"scène {i} : courbe à {len(e['pts'])} points (3 requis)")
    for line in s.get("fact", "").split("\\N"):
        if len(line) > 45: errs.append(f"scène {i} : ligne d'encart > 45 car.")
import urllib.request
for i, s in enumerate(ep["scenes"]):  # chaque image/vidéo directe doit être téléchargeable (un 403 = rendu planté ou plan noir)
    for x in (s.get("shots") or ([s] if s.get("clip") else [])):
        u = x.get("clip", "")
        if u.startswith("http") and "wikimedia.org" not in u and "usgs.gov" not in u:  # bloqués depuis Claude, vérifiés au rendu
            try: urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "OddlyLogicalStudio/1.0"}), timeout=20)
            except Exception as e: errs.append(f"scène {i} : URL inaccessible ({e}) {u[-60:]}")
from collections import Counter
_uses = Counter(sh.get("clip") for sc in ep["scenes"] for sh in (sc.get("shots") or ([sc] if sc.get("clip") else [])) if sh.get("clip"))
for c, n in _uses.items():
    if n > 2: errs.append(f"répétition : image/vidéo utilisée {n} fois (max 2, idéalement 1) → {c[-60:]}")
dups = {q for q in queries if queries.count(q) > 1}
if dups: errs.append(f"requêtes Pixabay en double : {sorted(dups)}")
if len(ep.get("youtube", {}).get("title", "")) > 60: errs.append("titre YouTube > 60 car.")
errs += [f"plan au hasard interdit (pixabay:requête) : {u}" for u in __import__("re").findall(r'"(pixabay:(?!id:)[^"]+)"', open(sys.argv[1]).read())]
print("\n".join(errs) or "OK"); sys.exit(1 if any(k in e for e in errs for k in ("courbe", "titre", "inaccessible", "schéma", "répétition", "type inconnu", "sans image", "au hasard")) else 0)
