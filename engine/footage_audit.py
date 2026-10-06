"""Audit : nombre de vidéos domaine public (NASA) + vidéos Wikimedia Commons par sujet."""
import json, sys, urllib.request, urllib.parse, ssl, concurrent.futures as cf
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "OddlyLogicalAudit/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=30, context=ctx))
def nasa(q):
    try: return get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "video"}))["collection"]["metadata"]["total_hits"]
    except Exception as e: return -1
def nasa_img(q):
    try: return get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "image"}))["collection"]["metadata"]["total_hits"]
    except Exception: return -1
def commons(q):
    try: return get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": q + " filetype:video", "srnamespace": 6, "srlimit": 1, "format": "json"}))["query"]["searchinfo"]["totalhits"]
    except Exception: return -1
TOPICS = [l.split("|") for l in open(sys.argv[1]).read().strip().splitlines()]
def row(t):
    title, q = t[0].strip(), t[1].strip()
    return title, q, nasa(q), nasa_img(q), commons(q)
with cf.ThreadPoolExecutor(8) as ex:
    for title, q, nv, ni, cv in ex.map(row, TOPICS):
        print(f"{title}|{q}|{nv}|{ni}|{cv}")
