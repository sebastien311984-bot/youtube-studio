"""Contrôle mécanique d'un épisode avant push (les règles techniques vivent ici, pas dans les consignes)."""
import json, sys
ep = json.load(open(sys.argv[1])); errs = []; queries = []
for i, s in enumerate(ep["scenes"]):
    k, w = s.get("kind"), len(s.get("text", "").split())
    if k and k not in ("intro", "diagram", "stat", "scale", "timeline", "versus", "quiz", "kinetic", "rank", "annotate", "beforeafter", "outro", "zoomto", "layers", "globe", "manim"): errs.append(f"scène {i} : type inconnu « {k} » (titre = option, pas un type)")
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

# Règles « spectateur » (2026-10-11) : bloquantes
DARK = ("stat", "scale", "timeline", "versus", "quiz", "kinetic", "rank", "diagram")
for i, s in enumerate(ep["scenes"]):
    if s.get("kind") in DARK and len(s.get("text", "").split()) / 2.6 > 12:
        errs.append(f"scène {i} : écran infographique trop long (~{len(s['text'].split())/2.6:.0f} s > 12 s) → couper ou mettre sur une vraie image (bloquant spectateur)")
if ep["scenes"] and ep["scenes"][0].get("kind"):
    errs.append("scène 0 : l'accroche doit être de vraies images, pas une infographie (bloquant spectateur)")
for k, sp in enumerate(ep.get("shorts", []), 1):
    for j in (range(sp["from"], sp["to"]) if "from" in sp else range(len(sp.get("scenes", [])))):
        if (ep["scenes"] if "from" in sp else sp["scenes"])[j].get("kind") in DARK: errs.append(f"short {k} : scène {j} est une infographie → un Short doit être sur de vraies images (bloquant spectateur)")

# Monétisation (contenu « inauthentique / réutilisé », règles YouTube 2025) : la vidéo doit TRANSFORMER les images
ORIG = ("annotate", "zoomto", "layers", "beforeafter", "diagram", "scale", "timeline", "versus", "stat", "quiz", "kinetic", "rank", "globe", "manim")
_w = lambda s: max(len(s.get("text", "").split()) / 2.6, s.get("min", 0))
_tot = sum(_w(s) for s in ep["scenes"]) or 1
_orig = sum(_w(s) for s in ep["scenes"] if s.get("kind") in ORIG or (s.get("kind", "footage") == "footage" and (s.get("label") or s.get("fact") or s.get("hud"))))
if _orig / _tot < 0.45: errs.append(f"monétisation : seulement {100*_orig/_tot:.0f} % du temps avec un apport visuel original (animations, annotations, encarts) → viser ≥ 45 % (bloquant monétisation)")
if not ep.get("youtube", {}).get("sources") and "Sources" not in ep.get("youtube", {}).get("description", ""):
    errs.append("monétisation : description sans section « Sources » (études, NOAA/NASA…) (bloquant monétisation)")
# Rétention / satisfaction (2026-10-12) : fiche stratégie obligatoire + rythme mesuré
st = ep.get("strategy", {})
for f in ("viewer", "hook", "promise", "payoff", "takeaway"):
    if not st.get(f): errs.append(f"stratégie : champ « {f} » manquant (bloquant rétention)")
_sc = [s for s in ep["scenes"] if s.get("kind") != "outro"]
if _sc and len(_sc[0].get("text", "").split()) > 22: errs.append("scène 0 : accroche > ~8 s → couper pour poser la question plus vite (bloquant rétention)")
t, last = 0, 0
for i, s in enumerate(_sc):
    t += _w(s)
    if s.get("reveal") or s.get("beat"): last = t
    elif t - last > 40: errs.append(f"scène {i} : aucune relance (reveal/beat) depuis {t-last:.0f} s (bloquant rétention)"); last = t
for i in range(2, len(_sc)):
    k3 = [_sc[j].get("kind", "footage") for j in (i-2, i-1, i)]
    if len(set(k3)) == 1 and k3[0] != "footage": errs.append(f"scène {i} : 3 fois de suite « {k3[0]} » → varier le procédé visuel")
if _sc and not _sc[-1].get("payoff"): errs.append("fin : la dernière scène doit porter « payoff »: true (réponse à la promesse) (bloquant rétention)")
print("\n".join(errs) or "OK"); sys.exit(1 if any(k in e for e in errs for k in ("courbe", "titre", "inaccessible", "schéma", "répétition", "type inconnu", "sans image", "au hasard", "bloquant spectateur", "bloquant monétisation", "bloquant rétention")) else 0)
