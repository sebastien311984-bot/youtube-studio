"""Story-board AVANT rendu (quelques secondes, 0 rendu) : chaque plan réel avec la phrase dite à ce moment.
But : vérifier « l'image montre ce que dit la voix » avant de lancer 40 min de rendu.
Usage : python3 engine/storyboard.py episode.json sortie.jpg"""
import json, sys, io, subprocess, urllib.request
from PIL import Image, ImageDraw
UA = {"User-Agent": "OddlyLogicalStudio/1.0"}
ep = json.load(open(sys.argv[1])); cells = []
for i, s in enumerate(ep["scenes"]):
    if s.get("kind"): continue
    shots = s.get("shots") or [s]; ws = s.get("text", "").split(); k = max(1, len(ws) // len(shots))
    for j, x in enumerate(shots): cells.append((f"{i}.{j}", " ".join(ws[j * k:(j + 1) * k]), x.get("clip", ""), x.get("start", 0)))
W, H, C = 320, 230, 6; rows = (len(cells) + C - 1) // C; sheet = Image.new("RGB", (C * W, rows * H), "white"); dr = ImageDraw.Draw(sheet)
for n, (tag, txt, u, st) in enumerate(cells):
    x, y = (n % C) * W, (n // C) * H; im = None
    try:
        if "images-assets.nasa.gov/image" in u: u = u.replace("~large", "~thumb")
        if u.lower().endswith((".jpg", ".jpeg", ".png")): im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()))
        elif u.startswith("http"):
            b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(st + 1), "-i", u, "-frames:v", "1", "-vf", "scale=316:-2", "-f", "image2", "-"], capture_output=True, timeout=90).stdout
            im = Image.open(io.BytesIO(b))
    except Exception: pass
    if im: im = im.convert("RGB"); im.thumbnail((316, 178)); sheet.paste(im, (x + 2, y + 2))
    else: dr.text((x + 10, y + 80), (u[:40] or "?") + "\n(aperçu indisponible : vérifier au rendu)", fill="red")
    lines = [txt[a:a + 52] for a in range(0, min(len(txt), 156), 52)]
    for m, l in enumerate(lines): dr.text((x + 4, y + 182 + 14 * m), (f"[{tag}] " if m == 0 else "") + l, fill="black")
sheet.save(sys.argv[2], quality=85); print(len(cells), "plans")
