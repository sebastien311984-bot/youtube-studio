"""Trouve des plans HD domaine public (NASA SVS + NASA Image Library) pour un sujet.
Usage : python3 find_footage.py "black hole" [max]   -> lignes  id | titre | largeur | url
Sortie volontairement compacte pour économiser les tokens."""
import json, re, sys, ssl, os, urllib.request, urllib.parse
CA = "/root/.ccr/ca-bundle.crt"
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else None
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "OddlyLogicalStudio/1.0 (https://github.com/sebastien311984-bot/youtube-studio; educational YouTube channel)"}), timeout=40, context=ctx))
if sys.argv[1] == "--commons":  # vidéos Wikimedia Commons (crédit obligatoire : voir la page « desc »)
    q, n = sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": q + " filetype:video", "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "format": "json"}))
    for p_ in d.get("query", {}).get("pages", {}).values():
        ii = p_["imageinfo"][0]; m = ii.get("extmetadata", {})
        lic = m.get("LicenseShortName", {}).get("value", "?"); art = re.sub(r"<[^>]+>", "", m.get("Artist", {}).get("value", "?")).strip()[:40]
        print(f"COMMONS | {p_['title'][5:60]} | {ii.get('width')}x{ii.get('height')} | {lic} | {art} | {ii['url'].split('?')[0]}")
    sys.exit()
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
