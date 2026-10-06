"""Kit de publication YouTube généré avec chaque vidéo :
<nom>.srt (sous-titres anglais : YouTube les traduit automatiquement), <nom>_thumb.jpg (miniature 1280x720),
<nom>_youtube.md (titre, description SEO avec chapitres, tags, réglages, traductions du titre)."""
import os, subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

FD = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(FD + f"InterDisplay-{w}.otf", s)
def ts(t, srt=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}" if srt else (f"{h}:{m:02d}:{int(s):02d}" if h else f"{m}:{int(s):02d}")

def srt(words, path):
    lines, g = [], []
    for w in words:
        g.append(w)
        if len(g) >= 7 or w[2][-1:] in ".?!": lines.append(g); g = []
    if g: lines.append(g)
    with open(path, "w") as f:
        for k, g in enumerate(lines, 1):
            f.write(f"{k}\n{ts(g[0][0], True)} --> {ts(g[-1][0] + g[-1][1] + 0.2, True)}\n{' '.join(w[2] for w in g)}\n\n")

def thumbnail(src, path, text, sub="", accent=(255, 196, 40), shift=True, circle=True):
    """Miniature : image choc agrandie + contraste, texte énorme à contour, flèche/cercle rouge, marque."""
    W, H = 1280, 720
    if src:
        cp, d = src; tmp = path + ".png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(d * 0.55), "-i", cp, "-frames:v", "1", tmp], check=True)
        im = Image.open(tmp).convert("RGB").resize((W, H), Image.LANCZOS); os.remove(tmp)
        if shift:  # agrandit et décale : le sujet central passe à droite, le texte à gauche
            im = im.resize((int(W * 1.5), int(H * 1.5)), Image.LANCZOS).crop((0, int(H * 0.25), W, int(H * 1.25)))
    else: im = Image.new("RGB", (W, H), (10, 10, 20))
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.35)).enhance(1.25)
    shade = Image.new("L", (W, H)); sd = ImageDraw.Draw(shade)
    for x in range(W): sd.line([(x, 0), (x, H)], fill=int(200 * max(0, 1 - x / (W * 0.62))))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)
    d = ImageDraw.Draw(im)
    words = text.upper().split(); lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) > 11 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    size = 128 if len(lines) <= 2 else 104; y = H / 2 - len(lines) * size * 0.55
    for k, ln in enumerate(lines):
        col = accent if k == len(lines) - 1 else (255, 255, 255)
        d.text((60, y), ln, font=font("Black", size), fill=col, stroke_width=10, stroke_fill=(0, 0, 0)); y += size * 1.05
    if sub:
        f = font("Black", 40); tw = d.textlength(sub.upper(), font=f)
        d.rounded_rectangle((60, y + 14, 60 + tw + 40, y + 78), 12, fill=(225, 30, 40))
        d.text((80, y + 46), sub.upper(), font=f, fill=(255, 255, 255), anchor="lm")
    # cercle rouge sur la zone d'intérêt (droite)
    cx, cy, r = int(W * 0.75), int(H * 0.5), 175
    for k in range(3 if circle else 0): d.ellipse((cx - r - k * 3, cy - r - k * 3, cx + r + k * 3, cy + r + k * 3), outline=(235, 30, 40), width=8)
    d.text((W - 24, H - 22), "ODDLY LOGICAL SCIENCE", font=font("Bold", 24), fill=(255, 255, 255), anchor="rs", stroke_width=3, stroke_fill=(0, 0, 0))
    im.save(path, quality=92)

def write_all(ep, out, words, chapters, thumb_src):
    base = out[:-4]; yt = ep.get("youtube", {})
    srt(words, base + ".srt")
    th = ep.get("thumbnail", {})
    thumbnail(thumb_src, base + "_thumb.jpg", th.get("text", ep["title"]), th.get("sub", ""), shift=th.get("shift", True), circle=th.get("circle", True))
    ch = [(0.0, "Intro")] + [c for c in chapters if c[0] >= 10]
    desc = yt.get("description", "").strip() + "\n\n⏱️ CHAPTERS\n" + "\n".join(f"{ts(t)} {n}" for t, n in ch)
    desc += "\n\n🎥 " + ep.get("credits", "") + "\nAll footage is public domain or used under its license.\n\n" + " ".join("#" + h for h in yt.get("hashtags", []))
    md = [f"# YouTube kit — {ep['title']}", "", "## Title", yt.get("title", ep["title"]), "",
          "## Description", "```", desc, "```", "", "## Tags", ", ".join(yt.get("tags", [])), "",
          "## Title translations (Studio > Languages)", *[f"- {k}: {v}" for k, v in yt.get("translations", {}).items()], "",
          "## Settings", "- Category: Science & Technology · Language: English · Caption: upload the .srt file (English)",
          "- Audience: not made for kids · License: Standard YouTube · Allow embedding: yes",
          "- Altered or synthetic content: No (real NASA footage + animations)",
          "- Chapters: automatic from the description (first chapter at 0:00)",
          "- End screen: subscribe + best video; Cards: related video at 70%",
          "- Thumbnail: upload the _thumb.jpg file (1280x720)"]
    open(base + "_youtube.md", "w").write("\n".join(md) + "\n")
