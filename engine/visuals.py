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
                             "-i", "-", "-t", str(d), "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", out],
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
        (cx, cy), r = el["c"], el["r"]; a0, a1 = el.get("a0", 0), el.get("a1", 360); n = 120
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
