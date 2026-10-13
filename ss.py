"""Scout étendu (branche jetable) : usage python3 ss.py MODE args...
 search  q1 q2 ... (préfixes commons: nasa: archive: openverse: cat:<Category name> catsearch:<terme>)
 verify  (lit verify.json = liste d'URL) -> verify_out.json
"""
import json, os, sys, io, re, urllib.request, urllib.parse
UA = {"User-Agent": "OddlyLogicalStudio/1.0 (github.com/sebastien311984-bot/youtube-studio)"}
def get(url, t=40): return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t))
def strip(s): return re.sub(r"<[^>]+>", "", s or "").strip()
IP = "url|extmetadata|mediatype|size|mime"
def pages_to_cands(r, q):
    out = []
    for p in r.get("query", {}).get("pages", {}).values():
        if "imageinfo" not in p: continue
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        out.append({"src": "commons", "url": ii["url"], "thumb": ii.get("thumburl"), "w": ii.get("width"), "h": ii.get("height"), "type": ii.get("mediatype"), "mime": ii.get("mime"),
          "licence": m.get("LicenseShortName", {}).get("value", "?"), "author": strip(m.get("Artist", {}).get("value", "?"))[:100],
          "desc": strip(m.get("ImageDescription", {}).get("value", ""))[:260], "page": ii.get("descriptionurl"), "title": p["title"], "query": q})
    return out
def commons(q, n=50):
    r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo", "iiprop": IP, "iiurlwidth": 400}))
    return pages_to_cands(r, q)
def cat(name, n=50, maxp=4):
    out = []; cont = {}
    for _ in range(maxp):
        r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "categorymembers", "gcmtitle": "Category:" + name.replace("Category:", ""), "gcmtype": "file", "gcmlimit": n, "prop": "imageinfo", "iiprop": IP, "iiurlwidth": 400, **cont}))
        out += pages_to_cands(r, "cat:" + name)
        if "continue" in r: cont = r["continue"]
        else: break
    return out
def catsearch(q):
    r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "list": "search", "srsearch": q, "srnamespace": 14, "srlimit": 30}))
    for s in r["query"]["search"]: open("scout/cats.txt","a").write(q+" => "+s["title"]+"\n")
    return []
def nasa(q, n=3):
    out = []
    for pg in range(1, n + 1):
        try: r = get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "image,video", "page": pg}))
        except Exception: break
        for it in r["collection"]["items"]:
            d = it["data"][0]; i = d["nasa_id"]; th = next((l["href"] for l in it.get("links", []) if l.get("rel") == "preview"), None)
            url = f"https://images-assets.nasa.gov/image/{i}/{i}~large.jpg" if d["media_type"] == "image" else f"https://images-assets.nasa.gov/video/{i}/{i}~orig.mp4"
            out.append({"src": "nasa", "id": i, "url": url, "thumb": th, "type": d["media_type"], "licence": "NASA (public domain)", "author": d.get("photographer") or d.get("center", ""), "title": d["title"][:90], "desc": strip(d.get("description", ""))[:260], "date": d.get("date_created", "")[:10], "query": q})
    return out
def openverse(q, n=20):
    r = get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license_type": "commercial", "page_size": n, "mature": "false"}))
    return [{"src": "openverse", "url": h["url"], "thumb": h.get("thumbnail") or h["url"], "type": "image", "w": h.get("width"), "h": h.get("height"), "licence": f"{h['license']} {h.get('license_version') or ''}".strip(), "author": h.get("creator") or "", "title": h.get("title") or "", "page": h.get("foreign_landing_url", ""), "query": q} for h in r.get("results", [])]
def archive(q, n=10):
    r = get("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({"q": f"({q}) AND mediatype:movies", "fl[]": ["identifier", "title", "licenseurl", "creator"], "rows": n, "output": "json"}, doseq=True))
    return [{"src": "archive", "id": d["identifier"], "url": "https://archive.org/details/" + d["identifier"], "thumb": f"https://archive.org/services/img/{d['identifier']}", "type": "video", "licence": d.get("licenseurl", "?"), "author": str(d.get("creator", "")), "title": str(d.get("title", ""))[:90], "query": q} for d in r["response"]["docs"]]
SRC = {"commons": commons, "nasa": nasa, "openverse": openverse, "archive": archive, "catsearch": catsearch, "cat": cat}
def fetch_thumb(c):
    if c.get("_im"): return c["_im"]
    return None
def sheet(cands, tag, outdir, C=6, W=300, H=205, R=5):
    from PIL import Image, ImageDraw
    per = C * R
    for s in range(0, len(cands), per):
        part = cands[s:s + per]; rows = (len(part) + C - 1) // C
        sh = Image.new("RGB", (C * W, rows * H), "black"); dr = ImageDraw.Draw(sh)
        for k, c in enumerate(part):
            x, y = (k % C) * W, (k // C) * H
            try:
                im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(c["thumb"], headers=UA), timeout=30).read())).convert("RGB")
                im.thumbnail((W - 4, H - 26)); sh.paste(im, (x + 2, y + 2))
            except Exception: pass
            t = (c.get("title") or "").replace("File:", "")[:36]
            dr.text((x + 3, y + H - 24), f"#{c['n']} {c['src'][:3]} {c.get('w') or ''}", fill="yellow")
            dr.text((x + 3, y + H - 12), t, fill="white")
        sh.save(f"{outdir}/{tag}_{s // per:02d}.jpg", quality=82)
def main(a):
    os.makedirs("scout", exist_ok=True)
    mode, args = a[0], a[1:]
    if mode == "search":
        tag = args[0]; allc = []; seen = set()
        for q in args[1:]:
            src, _, qq = q.partition(":")
            try: res = SRC[src](qq)
            except Exception as e: print(src, qq, e); res = []
            for c in res:
                if c["url"] in seen: continue
                seen.add(c["url"]); allc.append(c)
        bad = re.compile(r"patch|\.svg|\.pdf|federal register|logo|\.ogg|\.djvu", re.I)
        allc = [c for c in allc if not bad.search(c.get("title", "")) and (c.get("type") in (None, "BITMAP", "image", "video", "VIDEO"))]
        for k, c in enumerate(allc): c["n"] = k
        json.dump(allc, open(f"scout/{tag}.json", "w"), indent=0, ensure_ascii=False)
        sheet(allc, tag, "scout"); print(len(allc), "candidats")
    elif mode == "verify":
        items = json.load(open("verify.json")); out = []
        for it in items:
            u = it["url"]; res = {"url": u}
            try:
                rq = urllib.request.Request(u, headers=UA, method="GET"); rp = urllib.request.urlopen(rq, timeout=60)
                res["status"] = rp.status; res["ctype"] = rp.headers.get("Content-Type"); res["len"] = rp.headers.get("Content-Length")
                if (res["ctype"] or "").startswith("image"):
                    from PIL import Image
                    im = Image.open(io.BytesIO(rp.read(40_000_000))); res["w"], res["h"] = im.size
            except Exception as e: res["status"] = str(e)[:80]
            out.append(res)
        json.dump(out, open("scout/verify_out.json", "w"), indent=0); print(sum(1 for r in out if r["status"] == 200), "/", len(out), "ok")
if __name__ == "__main__": main(sys.argv[1:])
