"""Repérage d'images sur GitHub Actions (réseau libre) : cherche dans plusieurs sources légales,
écrit candidates.json (URL, licence, auteur, page) et une planche contact numérotée à regarder avant d'écrire l'épisode.
Usage : python3 engine/scout.py "requête 1" "requête 2" ...  (préfixe optionnel : commons:, nasa:, archive:, pixabay:)"""
import json, os, sys, io, urllib.request, urllib.parse
UA = {"User-Agent": "OddlyLogicalStudio/1.0 (github.com/sebastien311984-bot/youtube-studio)"}
def get(url): return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))

def commons(q, n=8):
    r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search",
        "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|extmetadata|mediatype|size", "iiurlwidth": 320}))
    out = []
    for p in r.get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        out.append({"src": "commons", "url": ii["url"].split("?")[0], "thumb": ii.get("thumburl"), "w": ii.get("width"), "type": ii.get("mediatype"),
                    "licence": m.get("LicenseShortName", {}).get("value", "?"), "author": m.get("Artist", {}).get("value", "?")[:120],
                    "page": ii.get("descriptionurl"), "title": p["title"]})
    return out

def nasa(q, n=8):
    r = get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "image,video"}))
    out = []
    for it in r["collection"]["items"][:n]:
        d = it["data"][0]; i = d["nasa_id"]; th = next((l["href"] for l in it.get("links", []) if l.get("rel") == "preview"), None)
        url = f"https://images-assets.nasa.gov/image/{i}/{i}~large.jpg" if d["media_type"] == "image" else f"https://images-assets.nasa.gov/video/{i}/{i}~orig.mp4"
        out.append({"src": "nasa", "url": url, "thumb": th, "type": d["media_type"], "licence": "NASA (public domain)", "author": d.get("center", ""), "title": d["title"][:80]})
    return out

def archive(q, n=6):
    r = get("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({"q": f"({q}) AND mediatype:movies AND licenseurl:*publicdomain*", "fl[]": ["identifier", "title", "licenseurl"], "rows": n, "output": "json"}, doseq=True))
    def mp4(i):
        try: return next(f"https://archive.org/download/{i}/{urllib.parse.quote(f['name'])}" for f in get(f"https://archive.org/metadata/{i}")["files"] if f["name"].endswith(".mp4"))
        except Exception: return f"https://archive.org/details/{i}"
    return [{"src": "archive", "url": mp4(d["identifier"]), "thumb": f"https://archive.org/services/img/{d['identifier']}",
             "type": "video", "licence": d.get("licenseurl", "?"), "author": "", "title": str(d.get("title", ""))[:80]} for d in r["response"]["docs"]]

def pixabay(q, n=6):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key: return []
    r = get("https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "q": q, "per_page": n, "video_type": "film", "safesearch": "true"}))
    return [{"src": "pixabay", "url": h["videos"]["large"]["url"] or h["videos"]["medium"]["url"], "thumb": h["videos"]["tiny"]["thumbnail"],
             "type": "video", "licence": "Pixabay", "author": h["user"], "title": h["tags"], "id": f"pixabay:id:{h['id']}"} for h in r["hits"]]

SRC = {"commons": commons, "nasa": nasa, "archive": archive, "pixabay": pixabay}
def main(queries, outdir="scout"):
    os.makedirs(outdir, exist_ok=True); allc = []
    for q in queries:
        src, _, qq = q.partition(":") if q.split(":")[0] in SRC else ("", "", q)
        for name in ([src] if src else ["nasa", "commons", "archive"]):
            try: res = SRC[name](qq)
            except Exception as e: print(f"{name} « {qq} » : {e}"); res = []
            for c in res: c["query"] = qq; allc.append(c)
    for k, c in enumerate(allc): c["n"] = k
    json.dump(allc, open(f"{outdir}/candidates.json", "w"), indent=1, ensure_ascii=False)
    from PIL import Image, ImageDraw
    W, H, C = 240, 150, 8; rows = (len(allc) + C - 1) // C; sheet = Image.new("RGB", (C * W, max(1, rows) * H), "black"); dr = ImageDraw.Draw(sheet)
    for c in allc:
        x, y = (c["n"] % C) * W, (c["n"] // C) * H
        try:
            im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(c["thumb"], headers=UA), timeout=30).read())).convert("RGB")
            im.thumbnail((W - 4, H - 22)); sheet.paste(im, (x + 2, y + 2))
        except Exception: pass
        dr.text((x + 4, y + H - 18), f"#{c['n']} {c['src']} {c['type'] or ''}"[:38], fill="yellow")
    sheet.save(f"{outdir}/sheet.jpg", quality=85); print(len(allc), "candidats")

if __name__ == "__main__": main(sys.argv[1:])
