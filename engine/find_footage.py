"""Trouve des plans HD domaine public (NASA SVS + NASA Image Library) pour un sujet.
Usage : python3 find_footage.py "black hole" [max]   -> lignes  id | titre | largeur | url
Sortie volontairement compacte pour économiser les tokens."""
import json, sys, ssl, os, urllib.request, urllib.parse
CA = "/root/.ccr/ca-bundle.crt"
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else None
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "OddlyLogical/1.0"}), timeout=40, context=ctx))
q, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8
for r in get("https://svs.gsfc.nasa.gov/api/search/?" + urllib.parse.urlencode({"search": q, "limit": n}))["results"]:
    try: d = get(f"https://svs.gsfc.nasa.gov/api/{r['id']}")
    except Exception: continue
    best = {}
    def walk(o):
        if isinstance(o, dict):
            u, w = o.get("url", ""), o.get("width") or 0
            if isinstance(u, str) and u.endswith(".mp4") and 1900 <= w <= 2200 and (o.get("height") or 0) <= 1100: best.setdefault(u, w)
            [walk(v) for v in o.values()]
        elif isinstance(o, list): [walk(v) for v in o]
    walk(d)
    for u, w in list(best.items())[:3]: print(f"SVS {r['id']} | {r['title'][:50]} | {w} | {u}")
