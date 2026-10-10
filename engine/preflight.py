"""Pré-contrôle avant rendu (≈3 min, 0 token) : télécharge chaque photo de l'épisode DANS L'ORDRE du montage,
détecte les quasi-doublons (hash perceptuel, même photo recadrée/autre format/série) et produit une planche numérotée."""
import json, os, sys, subprocess, urllib.parse
from PIL import Image, ImageDraw
import imagehash
sys.path.insert(0, os.path.dirname(__file__)); import render
ep = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
items = []
for i, s in enumerate(ep["scenes"]):
    srcs = [x["clip"] for x in s.get("shots", [])] + [s[k] for k in ("image", "before", "after") if s.get(k)]
    if s.get("clip"): srcs.append(s["clip"])
    for u in srcs: items.append((i, u))
thumbs, hashes, report = [], [], []
for n, (i, u) in enumerate(items):
    f = os.path.join(out, f"{n:03d}")
    if u.startswith("http"):
        subprocess.run(["curl", "-sSLf", "--max-time", "60", "--retry", "2", "-A", "OddlyLogicalStudio/1.0 (github.com/sebastien311984-bot/youtube-studio)", "-o", f, u])
    else:
        f = u
    try:
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", f, "-frames:v", "1", f + ".png"]); f = f + ".png"
        im = Image.open(f).convert("RGB"); im.thumbnail((320, 180))
    except Exception:
        im = Image.new("RGB", (320, 180), "red"); report.append(f"#{n} scène {i} : ILLISIBLE {u[-70:]}")
        thumbs.append((n, i, im)); continue
    h = imagehash.phash(im)
    for m, (h2, i2) in enumerate(hashes):
        if h - h2 <= 10: report.append(f"#{n} (scène {i}) ≈ #{m} (scène {i2}) QUASI-DOUBLON : {urllib.parse.unquote(u.split('/')[-1])[:60]}")
    hashes.append((h, i)); thumbs.append((n, i, im))
C = 8; rows = (len(thumbs) + C - 1) // C
sheet = Image.new("RGB", (C * 320, rows * 200), "white"); d = ImageDraw.Draw(sheet)
for n, i, im in thumbs:
    x, y = (n % C) * 320, (n // C) * 200; sheet.paste(im, (x, y)); d.text((x + 4, y + 182), f"#{n} scène {i}", fill="black")
sheet.save(os.path.join(out, "preflight_sheet.jpg"), quality=85)
open(os.path.join(out, "preflight.txt"), "w").write("\n".join(report) or "OK : aucun quasi-doublon")
print("\n".join(report) or "OK")
