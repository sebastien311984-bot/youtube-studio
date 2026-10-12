"""Plans générés par le moteur : intro cinématique, schémas « main qui dessine », chiffres chocs.
Chaque fonction écrit un MP4 1920x1080 30 i/s de durée d."""
import math, random, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def font(w, s):
    if (w, s) not in _fc: _fc[(w, s)] = ImageFont.truetype(FD + f"InterDisplay-{w}.otf", s)
    return _fc[(w, s)]

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def _writer(out, d):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-t", str(d), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out],
                            stdin=subprocess.PIPE)

def _render(out, d, frame_fn):
    p = _writer(out, d)
    for i in range(int(d * FPS) + 1): p.stdin.write(frame_fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait()

# ---------------------------------------------------------------- intro cinématique
def intro(out, d=4.0, name="ODDLY LOGICAL SCIENCE", tagline="THE UNIVERSE IS STRANGER THAN YOU THINK"):
    rnd = random.Random(11)
    stars = [(rnd.random() * W, rnd.random() * H, rnd.random()) for _ in range(260)]
    def fr(t):
        im = Image.new("RGB", (W, H), (3, 4, 10)); dr = ImageDraw.Draw(im)
        z = 1 + 0.25 * t / d  # étoiles qui s'approchent (hyper-espace doux)
        for x, y, b in stars:
            sx, sy = W / 2 + (x - W / 2) * z, H / 2 + (y - H / 2) * z
            c = int(60 + 160 * b * min(1, t / 0.8)); r = 1 + b * 1.5 * z
            dr.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(c, c, min(255, c + 30)))
        # faisceau lumineux horizontal qui balaie
        glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow)
        sweep = ease((t - 0.3) / 1.2)
        gd.rectangle((0, H / 2 - 3, W * sweep, H / 2 + 3), fill=255)
        glow = glow.filter(ImageFilter.GaussianBlur(18))
        im = Image.composite(Image.new("RGB", (W, H), (255, 190, 90)), im, glow.point(lambda v: int(v * 0.9)))
        # logo : lettres qui apparaissent avec espacement qui se resserre
        a = ease((t - 0.9) / 1.0)
        if a > 0:
            txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(txt)
            sp = 40 * (1 - a) + 12; f = font("Black", 108)
            widths = [td.textlength(ch, font=f) + sp for ch in name]; x = W / 2 - sum(widths) / 2
            for ch, wch in zip(name, widths):
                td.text((x, H / 2 - 40), ch, font=f, fill=(255, 255, 255, int(255 * a)), anchor="lm"); x += wch
            b = ease((t - 1.8) / 0.8)
            td.text((W / 2, H / 2 + 60), tagline, font=font("SemiBold", 34), fill=(255, 200, 64, int(255 * b)), anchor="mm")
            halo = txt.filter(ImageFilter.GaussianBlur(14))
            im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), halo), txt).convert("RGB")
        fade = min(1, t / 0.4, (d - t) / 0.5)
        return Image.eval(im, lambda v: int(v * max(0, fade)))
    _render(out, d, fr)

# ---------------------------------------------------------------- schéma « main qui dessine »
PAPER, INK = (246, 242, 232), (28, 30, 38)
COL = {"ink": INK, "red": (214, 64, 46), "orange": (236, 136, 32), "blue": (40, 110, 200), "gold": (214, 160, 20), "green": (40, 150, 90)}

def _path(el):
    """Échantillonne un élément en liste de points (pour révéler le trait progressivement)."""
    t = el["type"]
    if t in ("line", "arrow"):
        (x1, y1), (x2, y2) = el["from"], el["to"]; n = 60
        return [(x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n) for k in range(n + 1)]
    if t in ("circle", "arc"):
        (cx, cy), r = el.get("c") or el["center"], el["r"]; a0, a1 = el.get("a0", 0), el.get("a1", 360); n = 120
        return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    if t == "curve":  # Bézier quadratique : [p0, p1, p2]
        (x0, y0), (x1, y1), (x2, y2) = el["pts"]; n = 80
        return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * x1 + u * u * x2, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * y1 + u * u * y2) for u in (k / n for k in range(n + 1))]
    return []

def _pencil(dr, x, y):
    """Crayon stylisé dont la pointe est en (x, y)."""
    ang = math.radians(-35); L, w = 230, 26
    ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
    tip = (x, y); cone = (x + ux * 46, y + uy * 46)
    body_a = (cone[0] + px * w / 2, cone[1] + py * w / 2); body_b = (cone[0] - px * w / 2, cone[1] - py * w / 2)
    end_a = (body_a[0] + ux * L, body_a[1] + uy * L); end_b = (body_b[0] + ux * L, body_b[1] + uy * L)
    dr.polygon([(x + 8, y + 10), (body_a[0] + 8, body_a[1] + 10), (end_a[0] + 8, end_a[1] + 10), (end_b[0] + 8, end_b[1] + 10), (body_b[0] + 8, body_b[1] + 10)], fill=(0, 0, 0, 50))
    dr.polygon([tip, body_a, body_b], fill=(232, 196, 150))
    dr.polygon([tip, (x + ux * 16 + px * 5, y + uy * 16 + py * 5), (x + ux * 16 - px * 5, y + uy * 16 - py * 5)], fill=INK)
    dr.polygon([body_a, end_a, end_b, body_b], fill=(250, 196, 40))
    dr.line([((body_a[0] + body_b[0]) / 2, (body_a[1] + body_b[1]) / 2), ((end_a[0] + end_b[0]) / 2, (end_a[1] + end_b[1]) / 2)], fill=(220, 160, 20), width=3)
    ea2 = (end_a[0] + ux * 34, end_a[1] + uy * 34); eb2 = (end_b[0] + ux * 34, end_b[1] + uy * 34)
    dr.polygon([end_a, ea2, eb2, end_b], fill=(236, 120, 140))

def diagram(out, d, elements, title=None):
    """elements : liste d'objets {type: line|arrow|circle|arc|curve|text|drops, color, width, ...}
    dessinés l'un après l'autre par le crayon ; le schéma reste affiché à la fin."""
    rnd = random.Random(5)
    draw_t = d * 0.8; n = len(elements)
    weights = [2.0 if e["type"] == "text" else 1.0 for e in elements]; tot = sum(weights)
    spans, acc = [], 0.4
    for wgt in weights: span = (draw_t - 0.4) * wgt / tot; spans.append((acc, acc + span)); acc += span
    paths = [_path(e) for e in elements]
    paper = Image.new("RGB", (W, H), PAPER); pd = ImageDraw.Draw(paper)
    for _ in range(9000):  # grain du papier
        x, y = rnd.randrange(W), rnd.randrange(H); v = rnd.randint(-10, 6)
        pd.point((x, y), fill=tuple(max(0, min(255, c + v)) for c in PAPER))
    def fr(t):
        im = paper.copy(); dr = ImageDraw.Draw(im, "RGBA"); tip = None
        if title:
            a = ease(t / 0.5); dr.text((W / 2, 90), title, font=font("Black", 64), fill=INK + (int(255 * a),), anchor="mm")
            dr.line((W / 2 - 220 * a, 135, W / 2 + 220 * a, 135), fill=COL["red"], width=6)
        for el, (s0, s1), pts in zip(elements, spans, paths):
            p = (t - s0) / (s1 - s0)
            if p <= 0: continue
            p = min(1, p); col = COL.get(el.get("color", "ink"), INK); wdt = el.get("width", 7)
            if el["type"] == "text":
                txt = el["text"]; k = max(1, int(len(txt) * p)); f = font(el.get("weight", "Bold"), el.get("size", 48))
                dr.text(tuple(el["at"]), txt[:k], font=f, fill=col, anchor=el.get("anchor", "lm"))
                if p < 1:
                    bb = dr.textbbox(tuple(el["at"]), txt[:k], font=f, anchor=el.get("anchor", "lm")); tip = (bb[2] + 4, bb[3] - 6)
            elif el["type"] == "drops":  # gouttes qui tombent le long d'une courbe (pluie coronale)
                for j, (x, y) in enumerate(el["at"]):
                    fall = ((t - s0) * 140 + j * 37) % el.get("len", 220)
                    a = int(255 * min(1, p * 3))
                    dr.ellipse((x - 9, y + fall - 14, x + 9, y + fall + 14), fill=col + (a,))
            else:
                k = max(2, int(len(pts) * p)); seg = pts[:k]
                dr.line(seg, fill=col, width=wdt, joint="curve")
                if p < 1: tip = seg[-1]
                elif el["type"] == "arrow":
                    (x1, y1), (x2, y2) = el["from"], el["to"]; ang = math.atan2(y2 - y1, x2 - x1); L = 34
                    dr.polygon([(x2, y2), (x2 - L * math.cos(ang - 0.45), y2 - L * math.sin(ang - 0.45)), (x2 - L * math.cos(ang + 0.45), y2 - L * math.sin(ang + 0.45))], fill=col)
        if tip is None and t < draw_t + 0.3: tip = (W * 0.86, H * 0.86)  # crayon au repos
        if tip is not None and t < draw_t + 0.6: _pencil(dr, *tip)
        z = 1 + 0.04 * t / d  # léger zoom pour la vie
        cw, ch = int(W / z), int(H / z)
        return im.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
    _render(out, d, fr)

# ---------------------------------------------------------------- chiffre choc plein écran
def bigstat(out, d, value, prefix="", suffix="", caption="", color=(255, 200, 64)):
    rnd = random.Random(2)
    parts = [(rnd.random() * W, rnd.random() * H, rnd.uniform(0.3, 1)) for _ in range(90)]
    def fr(t):
        im = Image.new("RGB", (W, H), (8, 9, 18)); dr = ImageDraw.Draw(im)
        for x, y, s in parts:
            yy = (y - t * 60 * s) % H; c = int(40 + 60 * s); dr.ellipse((x - 2, yy - 2, x + 2, yy + 2), fill=(c, c, c + 20))
        v = value * ease(t / (d * 0.55)); txt = f"{prefix}{v:,.0f}{suffix}" if float(value).is_integer() else f"{prefix}{v:,.1f}{suffix}"
        pop = 1 + 0.08 * max(0, 1 - abs(t - d * 0.55) / 0.15)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.text((W / 2, H / 2 - 40), txt, font=font("Black", int(230 * pop)), fill=color + (255,), anchor="mm")
        a = ease((t - 0.5) / 0.6)
        ld.text((W / 2, H / 2 + 120), caption, font=font("Bold", 52), fill=(235, 235, 245, int(255 * a)), anchor="mm")
        glow = layer.filter(ImageFilter.GaussianBlur(22))
        im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), glow), layer).convert("RGB")
        return im
    _render(out, d, fr)

# ================================================================ PACK DE FORMATS v2
PAL = {"gold": (255, 200, 64), "red": (235, 70, 60), "blue": (70, 150, 255), "green": (60, 210, 140),
       "purple": (170, 110, 255), "white": (240, 242, 250), "orange": (255, 140, 40)}
def _bg(t, seed=3, tint=(8, 10, 22)):
    """Fond sombre animé : dégradé + poussière d'étoiles qui dérive."""
    rnd = random.Random(seed); im = Image.new("RGB", (W, H), tint); d = ImageDraw.Draw(im)
    for _ in range(140):
        x, y, s = rnd.random() * W, rnd.random() * H, rnd.uniform(0.3, 1)
        x = (x + t * 12 * s) % W; c = int(40 + 70 * s); d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=(c, c, c + 25))
    return im
def _glow(im, layer, r=18):
    return Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(r))), layer).convert("RGB")
def _col(c): return PAL.get(c, c) if isinstance(c, str) else tuple(c)

def scale(out, d, items, heading=""):
    """Comparaison d'échelle : cercles côte à côte (taille réelle relative), le plus grand en dernier.
    items : [{label, size, color, note}] ; size = taille relative (ex. Terre 1, Soleil 109)."""
    smax = max(i["size"] for i in items)
    def fr(t):
        im = _bg(t); layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        if heading: dr.text((W / 2, 90), heading, font=font("Black", 60), fill=(255, 255, 255, 255), anchor="mm")
        n = len(items); step = d * 0.7 / n
        # zoom arrière progressif : on commence centré sur les petits objets
        k = sum(ease((t - j * step) / 0.8) for j in range(n)); cur = max(1, min(n, k))
        visible_max = items[min(n - 1, int(cur - 0.001))]["size"]
        unit = 300 / max(visible_max, 1e-9) if visible_max < smax else 300 / smax
        unit = min(unit, 300 / items[0]["size"])
        sizes = [max(3, it["size"] * unit * ease((t - j * step) / 0.8)) for j, it in enumerate(items)]
        shown = [j for j in range(n) if ease((t - j * step) / 0.8) > 0]
        total = sum(2 * sizes[j] + 70 for j in shown) - 70
        x = max(100, W / 2 - total / 2); cy = 590
        for j in shown:
            it, r, p = items[j], sizes[j], ease((t - j * step) / 0.8)
            col = _col(it.get("color", "gold"))
            dr.ellipse((x, cy - r, x + 2 * r, cy + r), fill=col + (235,))
            above = r < 60 and j % 2 == 0  # petits objets : étiquettes alternées au-dessus / en dessous
            ly = cy - r - 60 if above else cy + max(r, 30) + 55
            dr.text((x + r, ly), it["label"], font=font("Bold", 40), fill=(255, 255, 255, int(255 * p)), anchor="mm")
            if it.get("note"): dr.text((x + r, ly + 50), it["note"], font=font("Medium", 30), fill=PAL["gold"] + (int(255 * p),), anchor="mm")
            x += 2 * r + 70
        return _glow(im, layer, 12)
    _render(out, d, fr)

def timeline(out, d, events, heading=""):
    """Frise : une ligne se trace, chaque date apparaît avec un point qui « pop ». events : [{year, text}]"""
    n = len(events); x0, x1, y = 160, W - 160, 600
    def fr(t):
        im = _bg(t, 5); layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        if heading: dr.text((W / 2, 110), heading, font=font("Black", 60), fill=(255, 255, 255, 255), anchor="mm")
        p = ease(t / (d * 0.75)); xe = x0 + (x1 - x0) * p
        dr.line((x0, y, xe, y), fill=PAL["gold"] + (255,), width=8)
        for j, ev in enumerate(events):
            frac = j / max(1, n - 1); xj = x0 + (x1 - x0) * frac
            tj = (1 - (1 - frac) ** (1 / 3)) * d * 0.75  # instant où la ligne atteint ce point
            if t < tj: continue
            pj = ease((t - tj) / 0.5)
            r = 18 + 10 * max(0, 1 - abs((xe - xj) / 120 - 0.5))
            dr.ellipse((xj - r, y - r, xj + r, y + r), fill=PAL["gold"] + (255,))
            up = j % 2 == 0; ty = y - 90 if up else y + 90
            dr.text((xj, ty), str(ev["year"]), font=font("Black", 54), fill=(255, 255, 255, int(255 * pj)), anchor="mm")
            dr.multiline_text((xj, ty + (-70 if up else 70)), ev["text"], font=font("SemiBold", 30), fill=PAL["gold"] + (int(255 * pj),), anchor="mm", align="center")
        return _glow(im, layer, 10)
    _render(out, d, fr)

def versus(out, d, left, right, heading=""):
    """Écran partagé VS. left/right : {name, color, stats:[\"...\", ...]}"""
    def fr(t):
        im = _bg(t, 9); layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        for side, it in ((0, left), (1, right)):
            p = ease((t - side * 0.25) / 0.6); col = _col(it.get("color", "blue" if side == 0 else "red"))
            xo = (-1 if side == 0 else 1) * (1 - p) * 500; cx = W * (0.27 if side == 0 else 0.73) + xo
            dr.rounded_rectangle((cx - 380, 230, cx + 380, 900), 40, fill=col + (55,), outline=col + (255,), width=5)
            dr.text((cx, 310), it["name"].upper(), font=font("Black", 64), fill=(255, 255, 255, int(255 * p)), anchor="mm")
            for k, st in enumerate(it.get("stats", [])):
                q = ease((t - 0.8 - k * 0.45 - side * 0.2) / 0.4)
                dr.text((cx, 440 + k * 105), st, font=font("Bold", 42), fill=(255, 255, 255, int(255 * q)), anchor="mm")
        b = ease((t - 0.5) / 0.4); s = int(70 + 40 * (1 - b) + 6 * math.sin(t * 6))
        dr.ellipse((W / 2 - s, 565 - s, W / 2 + s, 565 + s), fill=PAL["gold"] + (int(255 * b),))
        dr.text((W / 2, 565), "VS", font=font("Black", int(s * 0.9)), fill=(10, 10, 20, int(255 * b)), anchor="mm")
        if heading: dr.text((W / 2, 120), heading, font=font("Black", 56), fill=(255, 255, 255, 255), anchor="mm")
        return _glow(im, layer, 14)
    _render(out, d, fr)

def quiz(out, d, question, options, answer):
    """Quiz interactif : question, options, compte à rebours de 3 s, révélation de la bonne réponse."""
    t_rev = d - 1.6
    def fr(t):
        im = _bg(t, 13, (14, 8, 26)); layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        dr.text((W / 2, 130), "CAN YOU GUESS?", font=font("Black", 44), fill=PAL["gold"] + (255,), anchor="mm")
        dr.multiline_text((W / 2, 250), question, font=font("Black", 62), fill=(255, 255, 255, int(255 * ease(t / 0.5))), anchor="mm", align="center")
        for k, op in enumerate(options):
            p = ease((t - 0.5 - k * 0.3) / 0.4); y = 430 + k * 140
            good = k == answer and t > t_rev; bad = k != answer and t > t_rev
            fill = (PAL["green"] + (220,)) if good else ((60, 60, 80, 120) if bad else (255, 255, 255, 40))
            dr.rounded_rectangle((W / 2 - 520, y, W / 2 + 520, y + 110), 30, fill=fill, outline=(255, 255, 255, int(200 * p)), width=3)
            dr.text((W / 2 - 470, y + 55), "ABCD"[k], font=font("Black", 50), fill=PAL["gold"] + (int(255 * p),), anchor="mm")
            dr.text((W / 2 - 410, y + 55), op, font=font("Bold", 46), fill=(255, 255, 255, int(255 * p)), anchor="lm")
        if t < t_rev:  # anneau de compte à rebours
            rem = max(0, t_rev - max(t, t_rev - 3)); frac = rem / 3 if t > t_rev - 3 else 1
            cx, cy, r = W - 200, 160, 70
            dr.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 60), width=10)
            dr.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * frac, fill=PAL["gold"] + (255,), width=10)
            dr.text((cx, cy), str(int(math.ceil(rem))) if t > t_rev - 3 else "?", font=font("Black", 64), fill=(255, 255, 255, 255), anchor="mm")
        return _glow(im, layer, 10)
    _render(out, d, fr)

def kinetic(out, d, words, accent_every=3):
    """Typographie cinétique : les mots « claquent » au centre, un sur trois en doré."""
    n = len(words); per = d * 0.85 / n
    def fr(t):
        im = _bg(t, 21); layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        k = min(n - 1, int(t / per)); lt = (t - k * per) / per
        s = 1.6 - 0.6 * ease(lt / 0.25)
        for back in range(1, 3):  # mots précédents en arrière-plan
            if k - back >= 0:
                dr.text((W / 2, H / 2 - 170 * back), words[k - back].upper(), font=font("Black", 70), fill=(255, 255, 255, 60 // back), anchor="mm")
        col = PAL["gold"] if (k + 1) % accent_every == 0 else PAL["white"]
        dr.text((W / 2, H / 2), words[k].upper(), font=font("Black", int(150 * s)), fill=col + (int(255 * min(1, lt * 6)),), anchor="mm")
        return _glow(im, layer, 16)
    _render(out, d, fr)

def rank(out, d, number, title, sub=""):
    """Carton de classement « #3 » pour les vidéos Top N."""
    def fr(t):
        im = _bg(t, 31); layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        p = ease(t / 0.5); s = 1 + 0.5 * (1 - p)
        dr.text((W * 0.3, H / 2), f"#{number}", font=font("Black", int(330 * s)), fill=PAL["gold"] + (int(255 * p),), anchor="mm")
        q = ease((t - 0.4) / 0.5); xo = 300 * (1 - q)
        dr.text((W * 0.52 + xo, H / 2 - 40), title.upper(), font=font("Black", 76), fill=(255, 255, 255, int(255 * q)), anchor="lm")
        if sub: dr.text((W * 0.52 + xo, H / 2 + 50), sub, font=font("SemiBold", 40), fill=PAL["gold"] + (int(255 * q),), anchor="lm")
        return _glow(im, layer, 20)
    _render(out, d, fr)

# ---------------------------------------------------------------- image réelle figée + explication dessinée dessus
def _still(src, at=0.0):
    """Image fixe 1920x1080 depuis une photo ou une vidéo (image extraite à `at` s)."""
    if src.lower().rsplit(".", 1)[-1] in ("mp4", "webm", "ogv", "mov", "mkv", "m4v"):
        png = src + f".still{at:.1f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at), "-i", src, "-frames:v", "1", png], check=True); src = png
    im = Image.open(src).convert("RGB"); r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    return im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))

def annotate(out, d, src, marks, question=None, heading=None, at=0.0):
    """On fige un plan réel, on pose (option) une question, puis les repères se dessinent un à un :
    circle {c:[x,y], r}, box {box:[x0,y0,x1,y1]}, arrow {from, to}, measure {from, to} (trait coté), label {at:[x,y]}.
    Chaque repère : text (court), color (gold, red, blue, green, white). Coordonnées sur 1920x1080."""
    base = _still(src, at); q0 = 2.2 if question else 0.4
    step = max(0.9, (d - q0 - 1.0) / max(1, len(marks)))
    def fr(t):
        z = 1 + 0.06 * smooth(t / d); w, h = int(W / z), int(H / z)
        im = base.crop(((W - w) // 2, (H - h) // 2, (W - w) // 2 + w, (H - h) // 2 + h)).resize((W, H), Image.BICUBIC)
        dim = 0.55 * smooth((t - q0 + 0.6) / 0.6) if marks else 0
        im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), min(0.45, dim))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        def P(x, y): return (W / 2 + (x - W / 2) * z, H / 2 + (y - H / 2) * z)
        for k, m in enumerate(marks):
            p = smooth((t - q0 - k * step) / 0.7)
            if p <= 0: continue
            col = _col(m.get("color", "gold")); a = int(255 * min(1, p * 1.4)); typ = m.get("type", "circle"); lab = None
            if typ == "circle":
                (x, y), r = P(*m["c"]), m.get("r", 80) * z
                dr.arc((x - r, y - r, x + r, y + r), -90, -90 + 360 * p, fill=col + (a,), width=7); lab = (x + r + 18, y - 20)
            elif typ == "box":
                x0, y0 = P(*m["box"][:2]); x1, y1 = P(*m["box"][2:])
                dr.rectangle((x0, y0, x0 + (x1 - x0) * p, y0 + (y1 - y0) * p), outline=col + (a,), width=6); lab = (x0, y1 + 14)
            elif typ in ("arrow", "measure"):
                (x0, y0), (x1, y1) = P(*m["from"]), P(*m["to"]); xe, ye = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
                dr.line((x0, y0, xe, ye), fill=col + (a,), width=7)
                ang = math.atan2(ye - y0, xe - x0)
                if typ == "arrow" and p > 0.95:
                    for s_ in (2.6, -2.6): dr.line((xe, ye, xe + 34 * math.cos(ang + s_), ye + 34 * math.sin(ang + s_)), fill=col + (a,), width=7)
                if typ == "measure":
                    for (cx, cy) in ((x0, y0), (xe, ye)):
                        nx, ny = -math.sin(ang) * 22, math.cos(ang) * 22; dr.line((cx - nx, cy - ny, cx + nx, cy + ny), fill=col + (a,), width=6)
                lab = ((x0 + xe) / 2 + 22, (y0 + ye) / 2 - 22)
            elif typ == "label":
                lab = P(*m["at"])
            if m.get("text") and lab and p > 0.5:
                f = font("Bold", 40); tw = dr.textlength(m["text"], font=f); x, y = lab; x = min(x, W - tw - 50)
                dr.rounded_rectangle((x - 16, y - 10, x + tw + 16, y + 56), 12, fill=(12, 14, 22, int(a * 0.85)), outline=col + (a,), width=3)
                dr.text((x, y), m["text"], font=f, fill=(255, 255, 255, a))
        if question and t < q0 + 1.2:
            a = int(255 * min(smooth(t / 0.4), smooth((q0 + 1.2 - t) / 0.5))); f = font("Black", 64)
            tw = dr.textlength(question, font=f); dr.text(((W - tw) / 2, H - 200), question, font=f, fill=(255, 255, 255, a), stroke_width=4, stroke_fill=(0, 0, 0, a))
        if heading:
            f = font("Bold", 34); dr.text((70, 60), heading.upper(), font=f, fill=(255, 210, 90, 230), stroke_width=2, stroke_fill=(0, 0, 0, 200))
        return _glow(im, lay, 10)
    _render(out, d, fr)

# ---------------------------------------------------------------- avant / après avec volet animé
def beforeafter(out, d, src_before, src_after, label_before="BEFORE", label_after="AFTER", at_before=0.0, at_after=0.0):
    A, B = _still(src_before, at_before), _still(src_after, at_after)
    def fr(t):
        p = smooth((t - 1.2) / max(1.0, d * 0.45)); x = int(W * (1 - p))
        im = A.copy(); im.paste(B.crop((x, 0, W, H)), (x, 0)); dr = ImageDraw.Draw(im); f = font("Black", 48)
        if 0 < x < W: dr.line((x, 0, x, H), fill=(255, 255, 255), width=6)
        dr.text((60, H - 120), label_before, font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
        if p > 0.15: tw = dr.textlength(label_after, font=f); dr.text((W - tw - 60, H - 120), label_after, font=f, fill=(255, 210, 90), stroke_width=4, stroke_fill=(0, 0, 0))
        return im
    _render(out, d, fr)


# ---------------------------------------------------------------- écran de fin (20 s, zones pour les éléments YouTube)
def outro(out, d, src=None, line1="COULD YOU SURVIVE?", line2="WATCH NEXT"):
    """Fond : dernière image floutée + logo ; cadre vidéo à gauche et cercle « S'abonner » à droite
    (positions alignées sur le modèle d'écran de fin YouTube « 1 vidéo + abonnement »)."""
    if src:
        base = _still(src).filter(ImageFilter.GaussianBlur(22))
        base = Image.eval(base, lambda v: int(v * 0.35))
    else:
        base = None
    box = (150, 300, 150 + 900, 300 + 506)            # vidéo suggérée (16:9)
    cx, cy, r = 1500, 553, 190                         # bouton S'abonner (cercle)
    def fr(t):
        im = base.copy() if base else _bg(t)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        a = ease(t / 0.8); A = int(255 * a)
        dr.text((W / 2, 120), "ODDLY LOGICAL SCIENCE", font=font("Black", 64), fill=(255, 255, 255, A), anchor="mm")
        dr.text((W / 2, 190), line1, font=font("SemiBold", 34), fill=(255, 200, 64, A), anchor="mm")
        p = ease((t - 0.4) / 0.9)
        x0, y0, x1, y1 = box; g = 6 + 4 * math.sin(t * 3)
        dr.rounded_rectangle((x0, y0, x0 + (x1 - x0) * p, y1), radius=18, outline=(255, 200, 64, A), width=6)
        dr.text(((x0 + x1) / 2, y1 + 50), line2, font=font("Bold", 40), fill=(255, 255, 255, A), anchor="mm")
        rr = r * ease((t - 0.7) / 0.6) + g * 0.5
        dr.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(255, 60, 60, A), width=8)
        dr.text((cx, cy + r + 50), "SUBSCRIBE", font=font("Bold", 40), fill=(255, 255, 255, A), anchor="mm")
        im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), lay.filter(ImageFilter.GaussianBlur(10))), lay)
        fade = min(1, (d - t) / 0.6)
        return Image.eval(im.convert("RGB"), lambda v: int(v * max(0, fade)))
    _render(out, d, fr)


# ---------------------------------------------------------------- zoom dessiné sur une vraie photo (effet « carte qui zoome »)
def zoomto(out, d, src, box, label=None, at=0.0):
    """La photo entière, un cadre lumineux se dessine autour de `box` [x0,y0,x1,y1] (repère 1920x1080),
    puis la caméra plonge dedans ; `label` apparaît à l'arrivée."""
    base = _still(src, at); x0, y0, x1, y1 = box
    bw = max(x1 - x0, (y1 - y0) * W / H); bh = bw * H / W; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    def fr(t):
        p = smooth((t - 1.4) / max(1.0, d - 3.0))
        w = W + (bw - W) * p; h = H + (bh - H) * p
        l = min(max(0, (W / 2) + (cx - W / 2) * p - w / 2), W - w); tp = min(max(0, (H / 2) + (cy - H / 2) * p - h / 2), H - h)
        im = base.crop((int(l), int(tp), int(l + w), int(tp + h))).resize((W, H), Image.LANCZOS)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        a = ease((t - 0.3) / 0.8) * (1 - p)
        if a > 0.02:
            sx, sy = W / w, H / h; r = [(x0 - l) * sx, (y0 - tp) * sy, (x1 - l) * sx, (y1 - tp) * sy]
            dr.rectangle(r, outline=(255, 200, 64, int(255 * a)), width=6)
        b = ease((t - d + 1.6) / 0.6)
        if label and b > 0:
            f = font("Bold", 52); tw = dr.textlength(label, font=f)
            dr.rounded_rectangle((W / 2 - tw / 2 - 26, H - 170, W / 2 + tw / 2 + 26, H - 90), 14, fill=(10, 12, 20, int(210 * b)))
            dr.text((W / 2, H - 130), label, font=f, fill=(255, 210, 90, int(255 * b)), anchor="mm")
        im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), lay.filter(ImageFilter.GaussianBlur(8))), lay)
        return im.convert("RGB")
    _render(out, d, fr)

# ---------------------------------------------------------------- coupe dessinée par-dessus une vraie photo
def layers(out, d, src, bands, top=420, heading=None, at=0.0):
    """Une ligne de coupe descend sur la photo et révèle des couches translucides étiquetées.
    bands : [{name, color, h}] de haut en bas à partir de `top` (px)."""
    base = _still(src, at)
    def fr(t):
        im = base.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        y = top
        for k, b in enumerate(bands):
            p = ease((t - 0.6 - k * 0.9) / 0.8)
            if p <= 0: break
            col = _col(b.get("color", "blue")); hh = b.get("h", 160)
            dr.rectangle((0, y, W * p, y + hh), fill=col + (95,))
            dr.line((0, y, W * p, y), fill=col + (255,), width=5)
            dr.text((60, y + hh / 2), b["name"], font=font("Bold", 46), fill=(255, 255, 255, int(255 * p)), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0, int(200 * p)))
            y += hh
        if heading:
            a = ease(t / 0.6); dr.text((60, 60), heading, font=font("Bold", 34), fill=(255, 200, 64, int(255 * a)), stroke_width=2, stroke_fill=(0, 0, 0, int(200 * a)))
        return Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")
    _render(out, d, fr)

# ---------------------------------------------------------------- HUD documentaire sur vidéo réelle (la vidéo continue de jouer)
def hud(out, d, panels):
    """Calque transparent (MOV qtrle RGBA) posé sur un plan réel. panels = liste de :
    counter {label, value, from=0, unit, sub, pos, at}   — chiffre qui défile (style National Geographic)
    gauge   {label, value, max, unit, pos, at}           — cadran circulaire qui se remplit
    lock    {box:[x0,y0,x1,y1], text, at}                 — crochets de visée qui se resserrent sur un détail réel
    pos : bl, br, tl, tr. at : seconde d'apparition."""
    POS = {"bl": (70, H - 330), "br": (W - 590, H - 330), "tl": (70, 70), "tr": (W - 590, 70)}
    def card(dr, x, y, a, p, label, big, sub, col, w=520):
        dr.rounded_rectangle((x, y, x + w, y + 220), 18, fill=(6, 10, 18, int(150 * a)), outline=(255, 255, 255, int(40 * a)), width=2)
        dr.rectangle((x, y + 24, x + 6, y + 24 + 172 * p), fill=col + (int(255 * a),))
        dr.text((x + 34, y + 26), label.upper(), font=font("SemiBold", 28), fill=(200, 210, 225, int(255 * a)))
        dr.text((x + 32, y + 64), big, font=font("Black", 96), fill=(255, 255, 255, int(255 * a)))
        if sub: dr.text((x + 34, y + 172), sub, font=font("Medium", 28), fill=col + (int(255 * a),))
    def fr(t):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        for pn in panels:
            t0 = pn.get("at", 0.6); a = smooth((t - t0) / 0.5) * smooth((d - 0.2 - t) / 0.4)
            if a <= 0: continue
            p = ease((t - t0) / 1.8); col = _col(pn.get("color", "gold")); typ = pn.get("type", "counter")
            if typ in ("counter", "gauge"):
                x, y = POS[pn.get("pos", "bl")]; x += int((1 - smooth((t - t0) / 0.5)) * (-40 if x < W / 2 else 40))
                v0, v1 = pn.get("from", 0), pn["value"]; v = v0 + (v1 - v0) * p
                txt = (f"{v:,.0f}" if abs(v1) >= 10 else f"{v:.1f}") + pn.get("unit", "")
                if typ == "counter": card(dr, x, y, a, p, pn["label"], txt, pn.get("sub", ""), col)
                else:
                    x = min(x, W - 730); card(dr, x, y, a, p, pn["label"], txt, pn.get("sub", ""), col, 660)
                    cx, cy, r = x + 580, y + 130, 52; frac = min(1, v / pn.get("max", v1 or 1))
                    dr.arc((cx - r, cy - r, cx + r, cy + r), 135, 405, fill=(255, 255, 255, int(60 * a)), width=10)
                    dr.arc((cx - r, cy - r, cx + r, cy + r), 135, 135 + 270 * frac, fill=col + (int(255 * a),), width=10)
            elif typ == "lock":
                x0, y0, x1, y1 = pn["box"]; s = 1 + 0.6 * (1 - p); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                hw, hh = (x1 - x0) / 2 * s, (y1 - y0) / 2 * s; L = min(hw, hh) * 0.35; c = col + (int(255 * a),)
                for sx in (-1, 1):
                    for sy in (-1, 1):
                        X, Y = cx + sx * hw, cy + sy * hh
                        dr.line((X, Y, X - sx * L, Y), fill=c, width=6); dr.line((X, Y, X, Y - sy * L), fill=c, width=6)
                if pn.get("text") and p > 0.6:
                    f = font("Bold", 36); tw = dr.textlength(pn["text"], font=f); tx = min(max(40, cx - tw / 2), W - tw - 40); ty = cy + hh + 18
                    if ty > H - 120: ty = cy - hh - 70
                    dr.rounded_rectangle((tx - 14, ty - 6, tx + tw + 14, ty + 50), 8, fill=(6, 10, 18, int(190 * a)))
                    dr.text((tx, ty), pn["text"], font=f, fill=c)
        return lay
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-t", str(d), "-c:v", "qtrle", out], stdin=subprocess.PIPE)
    for i in range(int(d * FPS) + 1): p.stdin.write(fr(i / FPS).tobytes())
    p.stdin.close(); p.wait()

# ---------------------------------------------------------------- globe photoréaliste (texture NASA équirectangulaire)
def globe(out, d, texture, lon0=0.0, lon1=60.0, lat=15.0, light=(-0.6, 0.3, 0.75), zoom0=1.0, zoom1=1.0, marks=None, title=None, sub=None):
    """Planète qui tourne, éclairée (terminateur jour/nuit), halo atmosphérique, fond étoilé.
    marks : lignes de latitude ({lat, color, label}) et points ({lon, lat, color, label}) qui suivent la rotation."""
    import numpy as np
    tex = Image.open(texture).convert("RGB"); tex.thumbnail((4096, 2048)); T = np.asarray(tex).astype(np.float32) / 255; th, tw = T.shape[:2]
    L = np.array(light, float); L /= np.linalg.norm(L); marks = marks or []
    stars = _bg(0, seed=9, tint=(2, 3, 8)); lat0 = np.radians(lat)
    def fr(t):
        p = smooth(t / d); lon = np.radians(lon0 + (lon1 - lon0) * p); z = zoom0 + (zoom1 - zoom0) * p
        R = int(H * 0.40 * z); cx, cy = W // 2, H // 2
        ys, xs = np.mgrid[-R:R, -R:R].astype(np.float32) / R; r2 = xs ** 2 + ys ** 2; m = r2 <= 1
        zz = np.sqrt(np.clip(1 - r2, 0, 1)); X, Y, Z = xs, -ys, zz  # vue
        # rotation inverse (inclinaison puis longitude)
        Y2 = Y * np.cos(lat0) + Z * np.sin(lat0); Z2 = -Y * np.sin(lat0) + Z * np.cos(lat0)
        la = np.arcsin(np.clip(Y2, -1, 1)); lo = np.arctan2(X, Z2) + lon
        u = ((lo / (2 * np.pi) + 0.5) % 1 * (tw - 1)).astype(int); v = ((0.5 - la / np.pi) * (th - 1)).astype(int)
        col = T[v, u]; sh = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
        col = col * (0.12 + 0.95 * sh[..., None] ** 0.8)
        rim = np.clip(1 - zz, 0, 1) ** 3; col = col * (1 - 0.35 * rim[..., None]) + np.array([0.35, 0.6, 1.0]) * rim[..., None] * 0.55 * (0.3 + sh[..., None])
        im = stars.copy(); halo = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(halo)
        hd.ellipse((cx - R * 1.06, cy - R * 1.06, cx + R * 1.06, cy + R * 1.06), fill=(90, 150, 255, 90))
        im = Image.alpha_composite(im.convert("RGBA"), halo.filter(ImageFilter.GaussianBlur(R * 0.06)))
        sphere = Image.fromarray((np.clip(col, 0, 1) * 255).astype(np.uint8)); mask = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
        im.paste(sphere, (cx - R, cy - R), mask)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        def proj(lo_, la_):  # monde → écran ; None si face cachée
            x = np.cos(la_) * np.sin(lo_ - lon); y = np.sin(la_); zc = np.cos(la_) * np.cos(lo_ - lon)
            yv = y * np.cos(lat0) - zc * np.sin(lat0); zv = y * np.sin(lat0) + zc * np.cos(lat0)
            return (cx + x * R, cy - yv * R) if zv > 0 else None
        for k, mk in enumerate(marks):
            a = smooth((t - mk.get("at", 0.8)) / 0.8)
            if a <= 0: continue
            c = _col(mk.get("color", "gold")) + (int(255 * a),)
            if "lon" in mk:
                pt = proj(np.radians(mk["lon"]), np.radians(mk["lat"]))
                if pt:
                    rr = 12 + 6 * math.sin(t * 5); dr.ellipse((pt[0] - rr, pt[1] - rr, pt[0] + rr, pt[1] + rr), outline=c, width=5)
                    if mk.get("label"): dr.text((pt[0] + 26, pt[1] - 22), mk["label"], font=font("Bold", 38), fill=(255, 255, 255, int(255 * a)), stroke_width=3, stroke_fill=(0, 0, 0, int(200 * a)))
            else:
                pts = [proj(np.radians(L_), np.radians(mk["lat"])) for L_ in np.linspace(-180, 180, 241)]; seg = []
                for q in pts + [None]:
                    if q: seg.append(q)
                    elif len(seg) > 1: dr.line(seg, fill=c, width=5); seg = []
                    else: seg = []
                if mk.get("label"):
                    q = proj(lon + np.radians(40), np.radians(mk["lat"]))
                    if q: dr.text((q[0] + 14, q[1] - 48), mk["label"], font=font("Bold", 38), fill=(255, 255, 255, int(255 * a)), stroke_width=3, stroke_fill=(0, 0, 0, int(200 * a)))
        if title:
            a = int(255 * smooth((t - 0.4) / 0.7)); dr.text((90, 80), title, font=font("Black", 84), fill=(255, 210, 90, a))
            if sub: dr.text((92, 182), sub, font=font("Medium", 38), fill=(230, 235, 245, a))
        return _glow(im.convert("RGB"), lay, 6)
    _render(out, d, fr)
