"""Scout Titanic : catégories Wikimedia Commons (profondeur 1), recherche Commons avec reprises, Library of Congress, NOAA/NASA/Archive, Pixabay.
Écrit candidates.json + sheet_N.jpg dans scout_titanic/."""
import json, os, sys, io, time, urllib.request, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "engine"))
UA = {"User-Agent": "OddlyLogicalStudio/1.0 (github.com/sebastien311984-bot/youtube-studio)"}
def get(url, tries=4):
    for k in range(tries):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
        except Exception as e:
            err = e; time.sleep(2 + 3 * k)
    print("FAIL", url[:120], err); return None
def fetch(u):
    for k in range(4):
        try:
            time.sleep(0.25); return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
        except Exception: time.sleep(2 + 3 * k)
    raise RuntimeError(u)
API = "https://commons.wikimedia.org/w/api.php?"
def info(titles):
    out = []
    for i in range(0, len(titles), 40):
        r = get(API + urllib.parse.urlencode({"action": "query", "format": "json", "titles": "|".join(titles[i:i+40]), "prop": "imageinfo",
              "iiprop": "url|extmetadata|mediatype|size", "iiurlwidth": 320}))
        for p in (r or {}).get("query", {}).get("pages", {}).values():
            if "imageinfo" not in p: continue
            ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
            out.append({"src": "commons", "url": ii["url"], "thumb": ii.get("thumburl") or ii["url"], "w": ii.get("width"), "h": ii.get("height"), "type": ii.get("mediatype"),
              "licence": m.get("LicenseShortName", {}).get("value", "?"), "author": m.get("Artist", {}).get("value", "?")[:120], "credit": m.get("Credit", {}).get("value", "")[:120],
              "page": ii.get("descriptionurl"), "title": p["title"]})
    return out
def members(cat, kind="file", cap=60):
    t, cont = [], ""
    while len(t) < cap:
        r = get(API + urllib.parse.urlencode({"action": "query", "format": "json", "list": "categorymembers", "cmtitle": cat, "cmtype": kind, "cmlimit": 50, "cmcontinue": cont}))
        if not r: break
        t += [x["title"] for x in r["query"]["categorymembers"]]
        cont = r.get("continue", {}).get("cmcontinue")
        if not cont: break
    return t[:cap]
def search(q, n=15):
    r = get(API + urllib.parse.urlencode({"action": "query", "format": "json", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": n}))
    return [x["title"] for x in (r or {}).get("query", {}).get("search", [])]
CATS = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "cats.txt")) if l.strip() and not l.startswith("#")]
SEARCH = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "searches.txt")) if l.strip() and not l.startswith("#")]
def main():
    os.makedirs("scout_titanic", exist_ok=True); allc = []; seen = set()
    def add(items, q):
        for c in items:
            k = c.get("title") or c["url"]
            if k in seen: continue
            seen.add(k); c["query"] = q; allc.append(c)
    def crawl(cat, depth, cap):
        t = members(cat, "file", cap); subs = members(cat, "subcat", 40) if depth else []
        print(cat, len(t), "files", len(subs), "subcats", flush=True)
        for sc in subs: t += crawl(sc, depth - 1, 25)
        return t
    disc = []
    for w in ["Titanic", "Carpathia", "Titanic wreck", "Titanic survivors", "Titanic lifeboats", "Mackay-Bennett"]:
        r = get(API + urllib.parse.urlencode({"action": "query", "format": "json", "list": "search", "srsearch": w, "srnamespace": 14, "srlimit": 15}))
        disc += [x["title"] for x in (r or {}).get("query", {}).get("search", [])]
    print("DISCOVERED", sorted(set(disc)), flush=True)
    for cat in CATS:
        add(info(crawl(cat, 2, 80)), cat)
    for q in SEARCH:
        add(info(search(q)), "search:" + q); time.sleep(1)
    # Library of Congress
    for q in ["Titanic survivors Carpathia", "Titanic 1912 lifeboat", "Titanic Bain News Service", "iceberg 1912 Atlantic", "Titanic disaster newspaper"]:
        r = get("https://www.loc.gov/pictures/search/?" + urllib.parse.urlencode({"q": q, "fo": "json", "c": 12}))
        for it in (r or {}).get("results", []):
            im = it.get("image", {}); u = im.get("full") or im.get("thumb")
            if not u: continue
            if u.startswith("//"): u = "https:" + u
            th = im.get("thumb") or u
            if th.startswith("//"): th = "https:" + th
            add([{"src": "loc", "url": u, "thumb": th, "type": "BITMAP", "licence": "LoC (verify rights)", "author": str(it.get("creator", ""))[:80], "page": it.get("links", {}).get("item", ""), "title": it.get("title", "")[:90]}], "loc:" + q)
    allc = [c for c in allc if c.get("type") in ("BITMAP", "VIDEO", "DRAWING") and (c.get("w") or 800) >= 600 and "No restriction" not in c["licence"] or c.get("src") != "commons"]
    for k, c in enumerate(allc): c["n"] = k
    json.dump(allc, open("scout_titanic/candidates.json", "w"), indent=1, ensure_ascii=False)
    from PIL import Image, ImageDraw
    W, H, C, R = 192, 132, 10, 10
    for pg in range(0, len(allc), C * R):
        chunk = allc[pg:pg + C * R]; rows = (len(chunk) + C - 1) // C
        sheet = Image.new("RGB", (C * W, rows * H), "black"); dr = ImageDraw.Draw(sheet)
        for j, c in enumerate(chunk):
            x, y = (j % C) * W, (j // C) * H
            try:
                im = Image.open(io.BytesIO(fetch(c["thumb"]))).convert("RGB")
                im.thumbnail((W - 4, H - 16)); sheet.paste(im, (x + 2, y + 2))
            except Exception: pass
            dr.text((x + 3, y + H - 13), f"#{c['n']} {c['type'] or ''} {c['licence'][:14]}", fill="yellow")
        sheet.save(f"scout_titanic/sheet_{pg // (C * R)}.jpg", quality=80)
    print(len(allc), "candidats")
main()
