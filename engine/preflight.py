"""Pré-contrôle avant rendu (≈5 min, 0 token) :
1) chaque visuel de l'épisode DANS L'ORDRE du montage (même téléchargement que le rendu : pixabay:id, miroirs NASA),
   avec détection des quasi-doublons (hash perceptuel) ;
2) pour chaque animation sur photo (annotate, zoomto, layers, beforeafter) : image finale de l'animation
   réellement dessinée par le moteur → on vérifie que cercles/cadres/bandes tombent sur le bon détail."""
import json, os, sys, subprocess, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import imagehash
import render, visuals

ep = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
clips = os.path.join(out, "clips"); report = []

def frame(path, t=2.0):
    if path.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")): return Image.open(path).convert("RGB")
    png = path + ".png"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", path, "-frames:v", "1", png])
    return Image.open(png).convert("RGB")

def sheet(tiles, name, w=320, h=180, cols=8):
    rows = max(1, (len(tiles) + cols - 1) // cols); sh = Image.new("RGB", (cols * w, rows * (h + 20)), "white"); d = ImageDraw.Draw(sh)
    for n, (lab, im) in enumerate(tiles):
        im = im.copy(); im.thumbnail((w, h)); x, y = (n % cols) * w, (n // cols) * (h + 20)
        sh.paste(im, (x, y)); d.text((x + 4, y + h + 4), lab, fill="black")
    sh.save(os.path.join(out, name), quality=85)

# 1) visuels dans l'ordre
tiles, hashes = [], []
for i, s in enumerate(ep["scenes"]):
    srcs = [x["clip"] for x in s.get("shots", [])] + [s[k] for k in ("clip", "image", "before", "after") if s.get(k)]
    for u in srcs:
        n = len(tiles)
        if u.startswith("pixabay:") or u.split("?")[0].lower().endswith((".mp4", ".webm", ".mov")):  # vidéos déjà vues sur la planche scout : pas de téléchargement (rapide)
            tiles.append((f"#{n} sc{i} VIDEO", Image.new("RGB", (320, 180), (40, 40, 60)))); continue
        try:
            p = render.fetch(u, clips); im = frame(p)
        except Exception as e:
            im = Image.new("RGB", (320, 180), "red"); report.append(f"#{n} scène {i} : ILLISIBLE {u[-70:]} ({e!r})"[:200])
        h = imagehash.phash(im)
        for m, (h2, i2) in enumerate(hashes):
            if h - h2 <= 10 and im.getbbox(): report.append(f"#{n} (scène {i}) ≈ #{m} (scène {i2}) QUASI-DOUBLON : {urllib.parse.unquote(u.split('/')[-1])[:60]}")
        hashes.append((h, i)); tiles.append((f"#{n} sc{i}", im))
sheet(tiles, "preflight_sheet.jpg")

# 2) animations sur photo : image finale réellement dessinée
anims = []
for i, s in enumerate(ep["scenes"]):
    k = s.get("kind"); cp = os.path.join(out, f"anim_{i:02d}.mp4"); d = 6.0
    try:
        if k == "annotate": visuals.annotate(cp, d, render.img(s["image"], clips), s.get("marks", []), s.get("question"), s.get("heading"), s.get("at", 0))
        elif k == "zoomto": visuals.zoomto(cp, d, render.img(s["image"], clips), s["box"], s.get("label"), s.get("at", 0))
        elif k == "layers": visuals.layers(cp, d, render.img(s["image"], clips), s["bands"], s.get("top", 420), s.get("heading"), s.get("at", 0))
        elif k == "beforeafter": visuals.beforeafter(cp, d, render.img(s["before"], clips), render.img(s["after"], clips), s.get("label_before", "BEFORE"), s.get("label_after", "AFTER"), s.get("at_before", 0), s.get("at_after", 0))
        else: continue
        for t in (1.5, d - 0.3): anims.append((f"sc{i} {k} t={t}", frame(cp, t)))
    except Exception as e:
        report.append(f"scène {i} ({k}) : ANIMATION EN ÉCHEC {e!r}"[:200])
if anims: sheet(anims, "preflight_anims.jpg", w=640, h=360, cols=4)
open(os.path.join(out, "preflight.txt"), "w").write("\n".join(report) or "OK : aucun quasi-doublon, tout lisible")
print("\n".join(report) or "OK")
