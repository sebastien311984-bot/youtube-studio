"""Moteur Oddly Logical Science (v0) : épisode JSON -> MP4 16:9.
Voix Edge TTS (minutage mot à mot), plans NASA recadrés avec lent travelling, étalonnage,
fondus enchaînés, sous-titres et titres animés (ASS), musique d'ambiance synthétisée avec ducking.
Usage : python3 render.py episode.json clips_dir out.mp4"""
import asyncio, json, os, re, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visuals

W, H, FPS, SR, XF = 1920, 1080, 30, 44100, 0.6
CA = "/root/.ccr/ca-bundle.crt"

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
JOBS, CONCATS = [], []
def _run(job):
    try: job[0](*job[1])
    except Exception as e:  # erreur lisible dans les annotations GitHub (logs inaccessibles)
        import traceback; tb = traceback.format_exc().strip().splitlines()
        print(f"::error::{job[0].__name__} {str(job[1][0]).rsplit('/', 1)[-1]} : {e!r} | " + " | ".join(tb[-4:]), flush=True); raise

def sh(*a): subprocess.run(a, check=True)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

TONES = {  # débit / hauteur par ton : casse la monotonie de la voix de synthèse
    "neutral": ("-4%", "-4Hz"), "calm": ("-9%", "-6Hz"), "tense": ("+3%", "-2Hz"),
    "urgent": ("+8%", "+0Hz"), "reveal": ("-12%", "-8Hz"), "warm": ("-6%", "-2Hz")}
AUTO_TONE = {"stat": "reveal", "kinetic": "reveal", "rank": "reveal", "quiz": "tense", "timeline": "calm", "diagram": "warm"}

def humanize(path):
    """Voix plus chaude, moins « robot » : grave adouci, sifflantes calmées, compression douce, légère pièce. Durée inchangée."""
    tmp = path + ".h.mp3"
    af = ("highpass=f=75,equalizer=f=180:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.2:g=1.5,"
          "equalizer=f=6800:t=q:w=2:g=-3.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
          "aecho=0.9:0.9:28|47:0.10|0.06")
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-af", af, "-c:a", "libmp3lame", "-q:a", "2", tmp])
    if r.returncode == 0: os.replace(tmp, path)

def tts(text, voice, path, tone="neutral"):
    if os.path.exists(CA):  # proxy de l'environnement Claude ; inutile sur GitHub Actions
        import certifi, ssl; certifi.where = lambda: CA
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=CA)
    import edge_tts
    words = []
    async def run():
        c = edge_tts.Communicate(text, voice, rate=TONES.get(tone, TONES["neutral"])[0], pitch=TONES.get(tone, TONES["neutral"])[1], boundary="WordBoundary")
        with open(path, "wb") as f:
            async for ch in c.stream():
                if ch["type"] == "audio": f.write(ch["data"])
                elif ch["type"] == "WordBoundary": words.append((ch["offset"] / 1e7, ch["duration"] / 1e7, ch["text"]))
    for k in range(4):  # Edge TTS échoue parfois (NoAudioReceived) : on réessaie au lieu de planter le rendu
        try: words.clear(); asyncio.run(run()); break
        except Exception as e:
            if k == 3: raise
            print("TTS : nouvel essai", k + 1, e); __import__("time").sleep(5 * (k + 1))
    humanize(path); return words

PIXA_USED = set()  # vidéos Pixabay déjà utilisées : jamais deux fois le même plan dans une vidéo

LAST_STILL = [None]
def img(src, clips_dir):
    """Image d'une animation sur photo : si la source échoue, dernière photo valide (jamais de rendu planté)."""
    p = fetch(src, clips_dir) or LAST_STILL[0]
    if not p and os.path.isdir(clips_dir):  # aucune photo encore : n'importe quelle image déjà téléchargée
        ims = sorted(f for f in os.listdir(clips_dir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
        p = os.path.join(clips_dir, ims[0]) if ims else None
    if not p: print(f"::error::image introuvable pour une animation : {src}", flush=True)
    return p

def fetch(src, clips_dir):
    """Un plan peut être un fichier local ou une URL (téléchargée une seule fois, mise en cache)."""
    if src.startswith("pixabay:"):  # « pixabay:requête[#rang] » : recherche au moment du rendu (clé dans le secret GitHub)
        import urllib.request, urllib.parse
        q, _, rank = src[8:].partition("#"); key = os.environ.get("PIXABAY_API_KEY", "")
        if not key: raise SystemExit("PIXABAY_API_KEY manquant (secret GitHub)")
        UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) OddlyLogicalStudio/1.0"}
        if q.startswith("id:"):  # « pixabay:id:12345 » : plan choisi à l'œil sur la planche du scout → exactement celui-là
            url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "id": q[3:]})
            hits = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))["hits"]
        else:
            # requête complète uniquement (plus de raccourcissement : c'est ce qui donnait des vaches pour « boats on mud »),
            # vrais films seulement, et au moins la moitié des mots de la requête doivent figurer dans les tags du plan
            url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "q": q, "per_page": 50, "safesearch": "true", "video_type": "film"})
            hits = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))["hits"]
            words = [w for w in q.lower().split() if len(w) > 2]
            def score(h): tg = h.get("tags", "").lower(); return sum(w.rstrip("s") in tg for w in words)
            hits = sorted([h for h in hits if score(h) * 2 >= len(words)], key=score, reverse=True)
            if not hits: print(f"Pixabay : rien de pertinent pour {q!r} → plan retiré (les autres plans de la scène le couvrent)"); return None
        BAD = ("green screen", "greenscreen", "chroma", "cartoon", "animation", "3d", "character", "covid", "mask", "text", "intro", "logo")
        hits = [h for h in hits if not any(b in h.get("tags", "").lower() for b in BAD)] or hits  # ni fond vert, ni dessin animé, ni texte
        hits = [h for h in hits if h["videos"]["large"]["width"] >= 1920 or h["videos"]["medium"]["width"] >= 1920] or hits
        if not hits: print(f"Pixabay : aucun résultat pour {q!r} → plan retiré"); return None
        r = min(int(rank or 0), len(hits) - 1); hits = hits[r:] + hits[:r]
        h = next((h for h in hits if h["id"] not in PIXA_USED), hits[0])
        if h["id"] in PIXA_USED: print(f"Pixabay : plus de plan inédit pour {q!r}, plan réutilisé")
        PIXA_USED.add(h["id"])
        v = h["videos"]
        src = v["large"]["url"] if v["large"]["url"] else v["medium"]["url"]
    if not src.startswith("http"): return src if os.path.exists(src) else os.path.join(clips_dir, src)
    os.makedirs(clips_dir, exist_ok=True); local = os.path.join(clips_dir, src.rsplit("/", 1)[-1])
    if not os.path.exists(local):
        t0 = time.time()
        alts = [src]
        if "images-assets.nasa.gov" in src:  # NASA refuse parfois ~large : on essaie ~orig puis ~medium, UA navigateur
            alts += [src.replace("~large", "~orig"), src.replace("~large", "~medium")]
            pia = re.search(r"/(PIA\d{5})/", src)
            if pia: alts.append(f"https://photojournal.jpl.nasa.gov/jpeg/{pia.group(1)}.jpg")  # miroir JPL
        for u in alts:
            for ua in ("OddlyLogicalStudio/1.0 (github.com/sebastien311984-bot/youtube-studio)", "Mozilla/5.0 (X11; Linux x86_64)"):
                r = subprocess.run(["curl", "-sSLf", "--retry", "2", "--max-time", "120", "-A", ua, "-o", local, u])
                if r.returncode == 0: break
            if r.returncode == 0: break
        if r.returncode != 0:  # source trop lente ou absente : on retire le plan au lieu de bloquer tout le rendu
            if os.path.exists(local): os.remove(local)
            print(f"Téléchargement abandonné ({time.time() - t0:.0f} s) → plan retiré : {src.rsplit('/', 1)[-1][:60]}", flush=True); return None
        if local.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".webp")): LAST_STILL[0] = local
        print(f"Téléchargé {os.path.getsize(local) / 1e6:.0f} Mo en {time.time() - t0:.0f} s : {src.rsplit('/', 1)[-1][:60]}", flush=True)
    return local

def clip(src, start, d, out, move):
    # recadrage 16:9 agrandi de 12 %, puis travelling lent (zoom avant/arrière ou panoramique)
    zw, zh = int(W * 1.12), int(H * 1.12)
    base = f"scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={zw}:{zh},"
    if move in ("left", "right"):
        x = f"(iw-ow)*(1-t/{d})" if move == "left" else f"(iw-ow)*t/{d}"
        vf = base + f"crop={W}:{H}:{x}:(ih-oh)/2,"
    else:  # zoom lent avant ("in") ou arrière ("out"), évalué image par image
        z = f"(1.01+0.10*t/{d})" if move == "in" else f"(1.11-0.10*t/{d})"
        vf = base + f"scale=w='trunc({W}*{z}/2)*2':h=-2:eval=frame,crop={W}:{H},"
    vf += "eq=contrast=1.08:saturation=1.12:gamma=0.97,vignette=PI/5,fps=30,format=yuv420p"
    still = src.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"))
    inp = ["-loop", "1", "-framerate", "30", "-t", str(d), "-i", src] if still else ["-stream_loop", "-1", "-ss", str(start), "-t", str(d), "-i", src]
    sh("ffmpeg", "-v", "error", "-y", *inp, "-t", str(d), "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out)

def ass_time(t): t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Display,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,4,2,2,160,160,70,1
Style: Label,Inter Display,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,6,0,1,0,0,7,0,0,0,1
Style: Big,Inter Display,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,8,0,1,0,6,5,0,0,0,1
Style: Small,Inter Display,34,&H0040C8FF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,14,0,1,0,3,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
GOLD = "&H0040C8FF&"  # BGR

def captions(words, t0):
    """Groupes de 2 à 6 mots ; mot prononcé en doré."""
    ev, g = [], []
    groups = []
    for w in words:
        g.append(w)
        nxt = words[words.index(w) + 1] if words.index(w) + 1 < len(words) else None
        pause = nxt is not None and nxt[0] - (w[0] + w[1]) > 0.28  # fin de phrase (TTS ne renvoie pas la ponctuation)
        if len(g) >= 6 or pause or (len(g) >= 2 and w[2][-1:] in ".,?!;:"): groups.append(g); g = []
    if g: groups.append(g)
    for gr in groups:
        end_g = gr[-1][0] + gr[-1][1] + 0.15
        for i, (st, d, _) in enumerate(gr):
            nxt = gr[i + 1][0] if i + 1 < len(gr) else end_g
            txt = " ".join((f"{{\\c{GOLD}}}{w[2]}{{\\c&HFFFFFF&}}" if j == i else w[2]) for j, w in enumerate(gr))
            ev.append(f"Dialogue: 1,{ass_time(t0 + st)},{ass_time(t0 + nxt)},Sub,,0,0,0,,{txt}")
    return ev

def label(t0, d, title, sub):
    """Bandeau info en bas à gauche : barre dorée qui se déploie + texte."""
    a, b = ass_time(t0), ass_time(t0 + d)
    return [
        f"Dialogue: 2,{a},{b},Label,,0,0,0,,{{\\an7\\pos(110,120)\\p1\\c{GOLD}\\fad(250,300)\\t(0,400,\\fscx100)\\fscx0}}m 0 0 l 8 0 8 110 0 110{{\\p0}}",
        f"Dialogue: 2,{a},{b},Label,,0,0,0,,{{\\an7\\pos(140,118)\\fad(300,300)\\fs46\\bord0\\shad3}}{title}",
        f"Dialogue: 2,{a},{b},Label,,0,0,0,,{{\\an7\\pos(142,176)\\fad(500,300)\\fs30\\c{GOLD}\\bord0\\shad2\\fsp5}}{sub}",
    ]

def fact(t0, d, text):
    """Encart « DID YOU KNOW? » en haut à droite, glisse depuis la droite. Retour à la ligne : \\N"""
    a, b = ass_time(t0), ass_time(t0 + d)
    mv = lambda x, y: f"\\an7\\move({x + 700},{y},{x},{y},0,350)\\fad(0,350)"
    return [
        f"Dialogue: 4,{a},{b},Label,,0,0,0,,{{{mv(1080, 90)}\\p1\\c&H201812&\\alpha&H30&}}m 0 0 l 780 0 780 150 0 150{{\\p0}}",
        f"Dialogue: 4,{a},{b},Label,,0,0,0,,{{{mv(1080, 90)}\\p1\\c{GOLD}}}m 0 0 l 10 0 10 150 0 150{{\\p0}}",
        f"Dialogue: 5,{a},{b},Label,,0,0,0,,{{{mv(1115, 110)}\\fs28\\c{GOLD}\\bord0\\fsp6}}DID YOU KNOW?",
        f"Dialogue: 5,{a},{b},Label,,0,0,0,,{{{mv(1115, 152)}\\fs34\\bord0\\fsp0\\q2}}{text}",
    ]

def chapter(t0, num, title):
    a, b = ass_time(t0), ass_time(t0 + 3.2)
    return [f"Dialogue: 6,{a},{b},Small,,0,0,0,,{{\\an5\\pos(960,430)\\fad(400,500)\\fsp30\\t(0,3200,\\fsp14)}}{num}",
            f"Dialogue: 6,{a},{b},Big,,0,0,0,,{{\\an5\\pos(960,520)\\fs96\\fad(600,500)\\blur3\\t(0,600,\\blur0)}}{title}"]

TRANSITIONS = ["fade", "smoothleft", "fade", "circleopen", "fadeblack", "zoomin", "fade", "slideup", "fadewhite", "dissolve", "smoothright", "radial"]

def teaser(t0, d, text):
    a, b = ass_time(t0), ass_time(t0 + d)
    return [f"Dialogue: 6,{a},{b},Label,,0,0,0,,{{\\an7\\move(-600,250,110,250,0,300)\\fad(0,300)\\fs28\\c{GOLD}\\bord0\\fsp8}}COMING UP",
            f"Dialogue: 6,{a},{b},Label,,0,0,0,,{{\\an7\\move(-600,288,110,288,0,300)\\fad(0,300)\\fs44\\bord0\\shad3\\fsp1}}{text}"]

def progress_bar(t0, total, marks):
    a, b, ms = ass_time(t0), ass_time(total - 1.5), int((total - 1.5 - t0) * 1000)
    ev = [f"Dialogue: 7,{a},{b},Label,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\c&HFFFFFF&\\alpha&HC0&\\fad(500,500)}}m 0 0 l 1920 0 1920 7 0 7{{\\p0}}",
          f"Dialogue: 8,{a},{b},Label,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\c{GOLD}\\fscx0\\t(0,{ms},\\fscx100)\\fad(500,500)}}m 0 0 l 1920 0 1920 7 0 7{{\\p0}}"]
    for m in marks:  # repères de chapitres
        x = int(1920 * (m - t0) / max(1, total - 1.5 - t0))
        if 0 < x < 1920: ev.append(f"Dialogue: 9,{a},{b},Label,,0,0,0,,{{\\an7\\pos({x},0)\\p1\\c&H000000&\\fad(500,500)}}m 0 0 l 4 0 4 7 0 7{{\\p0}}")
    return ev

def subscribe_nudge(t0, d=4.0):
    a, b = ass_time(t0), ass_time(t0 + d)
    return [f"Dialogue: 9,{a},{b},Label,,0,0,0,,{{\\an3\\pos(1830,1000)\\fad(200,300)\\p1\\c&H3020E0&\\fscx0\\fscy0\\t(0,250,\\fscx110\\fscy110)\\t(250,400,\\fscx100\\fscy100)}}m 0 0 l 330 0 330 76 0 76{{\\p0}}",
            f"Dialogue: 10,{a},{b},Label,,0,0,0,,{{\\an5\\pos(1665,962)\\fad(400,300)\\fs36\\bord0\\fsp4}}SUBSCRIBE"]

def make_shorts(ep, out, bounds):
    """Shorts verticaux 1080x1920 (≤ 58 s) : vidéo au centre, fond flouté, titre en haut.
    ep["shorts"] = [{"from": i, "to": j, "title": "..."}] (indices de scènes, j exclu) ; par défaut l'accroche."""
    specs = ep.get("shorts") or [{"from": 1, "to": min(len(bounds) - 1, 5), "title": ep.get("short_title", ep["title"])}]
    for k, sp in enumerate(specs, 1):
        src = out
        if sp.get("scenes"):  # Short AUTONOME (2026-10-11) : son propre script (accroche + contexte + révélation + appel), rendu à part
            sub = dict(ep, scenes=sp["scenes"], shorts=[], burn_captions=True, title=sp["title"]); sub.pop("thumbnail", None)
            sj = out[:-4] + f"_short{k}_ep.json"; json.dump(sub, open(sj, "w")); src = out[:-4] + f"_short{k}_h.mp4"
            subprocess.run([sys.executable, os.path.abspath(__file__), sj, os.path.dirname(os.path.abspath(out)) + "/../clips", src, "--short"], check=True)
            a, b = 0.0, min(dur(src), 58.0)
        else:
            a = bounds[sp["from"]]; b = min(bounds[sp["to"]], a + 58)
        if b - a < 20: b = min(bounds[-1] - 2, a + 25)  # données chaîne : 20-30 s = meilleur taux de complétion
        tf = out[:-4] + f"_short{k}.txt"; import textwrap; open(tf, "w").write("\n".join(textwrap.wrap(sp["title"].upper(), 18)))  # 9:16 : titre sur plusieurs lignes, jamais coupé
        vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.15[bg];"
              f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,"
              f"drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Black.otf:textfile={tf}:fontsize=62:line_spacing=14:fontcolor=white:"
              f"borderw=6:bordercolor=black:x=(w-tw)/2:y=300,"
              f"drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf:text='FULL VIDEO ON THE CHANNEL':fontsize=38:fontcolor=0xFFC840:x=(w-tw)/2:y=1560,"
              f"drawbox=x=240:y=1380:w=600:h=110:color=0xE53935@0.95:t=fill:enable='gte(t,{b - a - 4:.2f})',"
              f"drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Black.otf:text='SUBSCRIBE':fontsize=64:fontcolor=white:x=(w-tw)/2:y=1405:enable='gte(t,{b - a - 4:.2f})'")  # appel à l'abonnement (4 dernières s) : objectif 1 000 abonnés  # pas de fondu final : la fin boucle sur le début
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-i", src, "-filter_complex", vf, "-c:v", "libx264", "-preset", "medium",
           "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out[:-4] + f"_short{k}.mp4")
        os.remove(tf)

AMBIENCE = {}

def music(total, voice_env, cuts, risers=()):
    n = int(total * SR); t = np.arange(n) / SR; rng = np.random.default_rng(3)
    out = np.zeros(n)
    # nappe : accords lents (Am - F - C - G), harmoniques douces, battements
    chords = [(110, 130.81, 164.81), (87.31, 110, 130.81), (130.81, 164.81, 196), (98, 123.47, 146.83)]
    seg = 6.0
    for k in range(int(total / seg) + 1):
        a = int(k * seg * SR); b = min(n, int((k + 1) * seg * SR) + SR)
        if a >= n: break
        tt = t[a:b] - k * seg; env = np.minimum(1, tt / 1.5) * np.minimum(1, np.maximum(0, (seg + 1 - tt)) / 1.5)
        for f0 in chords[k % 4]:
            for h, amp in ((1, .10), (2, .04), (0.5, .08)):
                out[a:b] += amp * env * np.sin(2 * np.pi * f0 * h * tt + 0.3 * np.sin(2 * np.pi * 0.15 * tt)) * 0.6
    # grondement grave (sous-basse filtrée)
    rum = np.convolve(rng.standard_normal(n), np.ones(400) / 400, "same") * 3.0
    out += rum * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t))
    # ambiance du lieu (champ « ambience » de l'épisode) : donne de la matière sonore au sujet
    if AMBIENCE.get("kind") == "ocean":  # houle : bruit filtré grave qui monte et retombe comme des vagues
        surf = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same")
        swell = np.maximum(0, np.sin(2 * np.pi * 0.11 * t + np.sin(2 * np.pi * 0.023 * t))) ** 2
        out += surf * swell * 1.6 * AMBIENCE.get("level", 1.0)
        out += np.convolve(rng.standard_normal(n), np.ones(900) / 900, "same") * 2.0 * AMBIENCE.get("level", 1.0)  # grondement du large
    # « hits » cinématiques + whoosh aux transitions
    for c in cuts:
        i = int(c * SR); m = int(1.2 * SR); x = np.arange(m) / SR
        hit = (np.sin(2 * np.pi * 45 * x) * 0.9 + rng.standard_normal(m) * 0.15) * np.exp(-x * 3.5)
        sw = int(0.8 * SR); xs = np.arange(sw) / SR
        whoosh = np.convolve(rng.standard_normal(sw), np.ones(30) / 30, "same") * np.sin(np.pi * xs / 0.8) ** 3 * 2.2
        if i - sw > 0: out[i - sw:i] += whoosh * 0.5
        out[i:i + m] += hit[:max(0, min(m, n - i))] * 0.5
    # montées de tension (riser) qui finissent pile sur les révélations, puis 0,4 s de quasi-silence avant l'impact
    for c in risers:
        L = 2.0; i1 = int(c * SR); i0 = max(0, i1 - int(L * SR)); m = i1 - i0
        if m <= 0 or i1 > n: continue
        x = np.arange(m) / SR; f = 200 + 1400 * (x / L) ** 2
        sweep = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.10 + np.convolve(rng.standard_normal(m), np.ones(20) / 20, "same") * 0.8
        out[i0:i1] += sweep * (x / L) ** 2 * 0.5
        g0 = max(0, i1 - int(0.4 * SR)); out[g0:i1] *= np.linspace(1, 0.15, i1 - g0)
    env = np.minimum(1, t / 2) * np.minimum(1, (total - t) / 2.5)
    return out * env * (1 - 0.6 * voice_env)

DUB_VOICES = {"es": "es-MX-JorgeNeural", "pt": "pt-BR-AntonioNeural", "hi": "hi-IN-MadhurNeural", "fr": "fr-FR-RemyMultilingualNeural",
              "de": "de-DE-FlorianMultilingualNeural", "ar": "ar-SA-HamedNeural", "id": "id-ID-ArdiNeural", "ja": "ja-JP-KeitaNeural"}

def dub_track(ep, lang, texts, slots, total, cuts, risers, work, out):
    n = int(total * SR); vtrack = np.zeros(n)
    for i, (txt, (st, slot)) in enumerate(zip(texts, slots)):
        if not txt: continue
        vp = os.path.join(work, f"dub_{lang}_{i}.mp3"); tts(txt, DUB_VOICES[lang], vp, ep["scenes"][i].get("tone") or AUTO_TONE.get(ep["scenes"][i].get("kind", ""), "neutral")); vd = dur(vp)
        tempo = min(1.4, vd / slot) if slot > 0 and vd > slot else 1.0  # accélère légèrement si la traduction est plus longue
        if tempo > 1.0: print(f"Doublage {lang} scène {i} : accéléré x{tempo:.2f}")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vp, "-filter:a", f"atempo={tempo:.3f}", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
        v = np.frombuffer(raw, np.int16).astype(float) / 32768; a = int(st * SR); m = min(len(v), n - a); vtrack[a:a + m] += v[:m]
    k = int(0.15 * SR); env = np.convolve(np.abs(vtrack), np.ones(k) / k, "same"); env = np.minimum(1, env / 0.04)
    mix = np.tanh((vtrack * 1.15 + music(total, env, cuts[1:], [r for r in risers if r > 2.5]) * 0.33) * 1.1) * 0.93
    wav = os.path.join(work, f"dub_{lang}.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    sh("ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "aac", "-b:a", "160k", out)

def review_sheet(video, review):
    """Planche de revue : chaque plan réel avec la phrase dite au même moment, pour vérifier que l'image montre ce que dit la voix."""
    from PIL import Image, ImageDraw
    W, H, C = 320, 230, 6; rows = (len(review) + C - 1) // C; sheet = Image.new("RGB", (C * W, max(1, rows) * H), "white"); dr = ImageDraw.Draw(sheet)
    for n, (tm, txt, tag) in enumerate(review):
        x, y = (n % C) * W, (n // C) * H; fr = video + f".r{n}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{tm:.2f}", "-i", video, "-frames:v", "1", "-vf", "scale=316:-2", fr])
        try: sheet.paste(Image.open(fr), (x + 2, y + 2)); os.remove(fr)
        except Exception: pass
        lines = [txt[a:a + 52] for a in range(0, min(len(txt), 156), 52)]
        dr.text((x + 4, y + 182), f"[{tag}] " + (lines[0] if lines else ""), fill="black")
        for m, l in enumerate(lines[1:]): dr.text((x + 4, y + 196 + 14 * m), l, fill="black")
    sheet.save(video.replace(".mp4", "_review.jpg"), quality=85)

def main(ep_path, clips_dir, out):
    ep = json.load(open(ep_path)); work = os.path.join(os.path.dirname(os.path.abspath(out)), "_work"); os.makedirs(work, exist_ok=True)
    voice = ep.get("voice", "en-US-AndrewMultilingualNeural"); AMBIENCE.update(ep.get("ambience", {}))
    if ep.get("shorts_only") and "--short" not in sys.argv:  # épisode de Shorts autonomes seulement (pas de vidéo longue)
        make_shorts(ep, out, [0.0]); print("Shorts autonomes rendus"); return
    scenes, t, events, cuts = [], 0.0, [], []
    srt_words, yt_chapters, thumb_src, starts, trans = [], [], None, [], []
    review = []  # (instant, texte dit à ce moment, scène.plan) → planche de revue image/texte
    for i, s in enumerate(ep["scenes"]):
        vp = os.path.join(work, f"v{i}.mp3")
        words = tts(s["text"], voice, vp, s.get("tone") or AUTO_TONE.get(s.get("kind", ""), "neutral")) if s.get("text") else []
        vd = dur(vp) if words else 0
        d = max(s.get("min", 0), vd + s.get("pad", 0.7) + s.get("lead", 0.3))
        cp = os.path.join(work, f"c{i}.mp4"); kind = s.get("kind", "footage")
        if kind == "intro": JOBS.append((visuals.intro, (cp, d + XF)))
        elif kind == "diagram": JOBS.append((visuals.diagram, (cp, d + XF, s["elements"], s.get("heading"))))
        elif kind == "stat": JOBS.append((visuals.bigstat, (cp, d + XF, s["value"], s.get("prefix", ""), s.get("suffix", ""), s.get("caption", ""))))
        elif kind == "scale": JOBS.append((visuals.scale, (cp, d + XF, s["items"], s.get("heading", ""))))
        elif kind == "timeline": JOBS.append((visuals.timeline, (cp, d + XF, s["events"], s.get("heading", ""))))
        elif kind == "versus": JOBS.append((visuals.versus, (cp, d + XF, s["left"], s["right"], s.get("heading", ""))))
        elif kind == "quiz": JOBS.append((visuals.quiz, (cp, d + XF, s["question"], s["options"], s["answer"])))
        elif kind == "kinetic": JOBS.append((visuals.kinetic, (cp, d + XF, s["words"])))
        elif kind == "annotate": JOBS.append((visuals.annotate, (cp, d + XF, img(s["image"], clips_dir), s.get("marks", []), s.get("question"), s.get("heading"), s.get("at", 0))))
        elif kind == "beforeafter": JOBS.append((visuals.beforeafter, (cp, d + XF, img(s["before"], clips_dir), img(s["after"], clips_dir), s.get("label_before", "BEFORE"), s.get("label_after", "AFTER"), s.get("at_before", 0), s.get("at_after", 0))))
        elif kind == "zoomto": JOBS.append((visuals.zoomto, (cp, d + XF, img(s["image"], clips_dir), s["box"], s.get("label"), s.get("at", 0))))
        elif kind == "layers": JOBS.append((visuals.layers, (cp, d + XF, img(s["image"], clips_dir), s["bands"], s.get("top", 420), s.get("heading"), s.get("at", 0))))
        elif kind == "outro": JOBS.append((visuals.outro, (cp, d + XF, img(s["image"], clips_dir) if s.get("image") else None, s.get("line1", "COULD YOU SURVIVE?"), s.get("line2", "WATCH NEXT"))))
        elif kind == "rank": JOBS.append((visuals.rank, (cp, d + XF, s["number"], s["title_rank"], s.get("sub", ""))))
        else:
            # plusieurs plans dans une scène : coupe toutes les ~4 s pour garder du rythme
            shots = s.get("shots") or [{"clip": s["clip"], "start": s.get("start", 0), "move": s.get("move", "in")}]
            # garde-fou : jamais un plan de plus de ~5 s (sinon un rush court tourne en boucle à l'écran)
            need = max(1, round((d + XF) / 4.5))
            STILL = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")
            is_still = lambda c: c.split("?")[0].lower().endswith(STILL)
            vids = [x for x in shots if not is_still(x["clip"])]
            if len(shots) < need:  # règle 2026-10-11 : JAMAIS un plan répété (photo ou vidéo) → plans allongés
                print(f"Scène {i} : {len(shots)} plan(s) pour {d:.0f} s → plans allongés, aucun plan répété")
            if False:
                print(f"Scène {i} : {len(shots)} plan(s) pour {d:.0f} s → {need} plans générés automatiquement")
                moves = ["in", "left", "out", "right"]
                shots = [dict(shots[j % len(shots)], move=moves[j % 4],
                              start=shots[j % len(shots)].get("start", 0) + (j // len(shots)) * 4.5) for j in range(need)]
            sd = (d + XF) / len(shots); parts = []
            ws = s.get("text", "").split(); k = max(1, len(ws) // len(shots))
            review += [(t + (j + 0.5) * sd, " ".join(ws[j * k:(j + 1) * k]), f"{i}.{j}") for j in range(len(shots))]
            got = {}  # séquentiel (anti-doublon Pixabay) ; un plan répété par le garde-fou réutilise le MÊME fichier,
            srcs = [got.setdefault(sh_["clip"], fetch(sh_["clip"], clips_dir)) if sh_["clip"] not in got else got[sh_["clip"]] for sh_ in shots]  # jamais une nouvelle vidéo Pixabay au hasard
            keep = [k for k, x in enumerate(srcs) if x]  # plans Pixabay jugés hors sujet : retirés, on recycle les plans restants
            if not keep: raise SystemExit(f"Scène {i} : aucun plan pertinent — ajouter une image officielle ou une infographie")
            if len(keep) < len(srcs):  # plan inutilisable : retiré, les autres s'allongent (pas de doublon)
                srcs = [srcs[k] for k in keep]; shots = [shots[k] for k in keep]
                sd = (d + XF) / len(shots)
            parts = [os.path.join(work, f"c{i}_{j}.mp4") for j in range(len(shots))]
            JOBS.extend((clip, (a, b.get("start", 0), sd, c, b.get("move", "in"))) for a, b, c in zip(srcs, shots, parts))
            CONCATS.append((parts, cp, i))  # assemblé après le rendu parallèle de toutes les scènes
        print(f"Scène {i} préparée ({kind}, {d:.0f} s)", flush=True)
        scenes.append((cp, d, vp if words else None, t + s.get("lead", 0.3)))
        if ep.get("burn_captions", False): events += captions(words, t + s.get("lead", 0.3))  # sous-titres incrustés désactivés : ils se superposent aux sous-titres YouTube et restent en anglais sur les pistes doublées
        srt_words += [(t + s.get("lead", 0.3) + w0, w1, w2) for (w0, w1, w2) in words]
        if s.get("yt_chapter") or s.get("chapter"): yt_chapters.append((t, s.get("yt_chapter") or s["chapter"][1].title()))
        if s.get("kind") != "diagram" and s.get("kind") != "stat" and i == ep.get("thumbnail", {}).get("scene"): thumb_src = (cp, d)
        if i == 0 and ep.get("thumbnail", {}).get("image"):  # photo de miniature choisie
            tp = fetch(ep["thumbnail"]["image"], clips_dir)
            if tp: thumb_src = (tp, None)
        if isinstance(s.get("label"), list) and s.get("kind", "footage") not in ("zoomto",): events += label(t + 0.8, min(d - 1, 5), *s["label"])
        if "fact" in s: events += fact(t + min(2.5, d / 3), min(6, d - 1), s["fact"])
        if "chapter" in s and s.get("kind", "footage") in ("footage", "annotate") and not s.get("question"): events += chapter(t + 0.2, *s["chapter"])  # jamais par-dessus une infographie
        if "title" in s:
            a, b = ass_time(t + 0.4), ass_time(t + d)
            events += [f"Dialogue: 3,{a},{b},Big,,0,0,0,,{{\\an5\\pos(960,500)\\fad(800,500)\\blur2\\t(0,800,\\blur0)\\fsp20\\t(0,{int(d*1000)},\\fsp4)}}{s['title'][0]}",
                       f"Dialogue: 3,{a},{b},Small,,0,0,0,,{{\\an5\\pos(960,610)\\fad(1400,500)}}{s['title'][1]}"]
        if "teaser" in s: events += teaser(t + max(0.5, d - 3.5), 3.2, s["teaser"])
        starts.append(t); trans.append(s.get("transition")); cuts.append(t); t += d
    total = t + XF
    # vidéo : chaîne de fondus enchaînés
    inputs, fc, prev, off = [], [], "0:v", 0.0
    for i, (cp, d, _, _) in enumerate(scenes): inputs += ["-i", cp]
    for i in range(1, len(scenes)):
        off += scenes[i - 1][1]
        tr = trans[i] or TRANSITIONS[i % len(TRANSITIONS)]
        fc.append(f"[{prev}][{i}:v]xfade=transition={tr}:duration={XF}:offset={off:.3f}[x{i}]"); prev = f"x{i}"
    events += progress_bar(starts[1] if len(starts) > 1 else 0, total, [c[0] for c in yt_chapters])
    events += subscribe_nudge(total * ep.get("subscribe_at", 0.3))
    ass = os.path.join(work, "subs.ass"); open(ass, "w").write(ASS_HEAD + "\n".join(events) + "\n")
    fc.append(f"[{prev}]ass={ass}:fontsdir=/usr/share/fonts/opentype/inter,fade=t=in:st=0:d=1,fade=t=out:st={total - 1.5:.2f}:d=1.5[v]")
    # audio : voix placées + musique
    t0 = time.time()  # toutes les scènes (infographies + plans) rendues en parallèle sur les 4 cœurs
    with ProcessPoolExecutor(4) as ex:
        for f in [ex.submit(_run, j) for j in JOBS]: f.result()
    for parts, cp, i in CONCATS:
        if len(parts) == 1: os.replace(parts[0], cp)
        else:
            lst = os.path.join(work, f"l{i}.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
            sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", cp)
    print(f"Scènes rendues en {time.time() - t0:.0f} s ({len(JOBS)} tâches en parallèle)")
    n = int(total * SR); vtrack = np.zeros(n)
    for _, _, vp, st in scenes:
        if not vp: continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vp, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
        v = np.frombuffer(raw, np.int16).astype(float) / 32768; i = int(st * SR); m = min(len(v), n - i); vtrack[i:i + m] += v[:m]
    k = int(0.15 * SR); env = np.convolve(np.abs(vtrack), np.ones(k) / k, "same"); env = np.minimum(1, env / 0.04)
    risers = [st for st, sc in zip(starts, ep["scenes"]) if sc.get("kind") in ("stat", "rank", "kinetic", "quiz") or "title" in sc]
    mix = vtrack * 1.15 + music(total, env, cuts[1:], [r for r in risers if r > 2.5]) * 0.33
    mix = np.tanh(mix * 1.1) * 0.93
    wav = os.path.join(work, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    sh("ffmpeg", "-v", "error", "-y", *inputs, "-i", wav, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", f"{len(scenes)}:a",
       "-c:v", "libx264", "-preset", "faster", "-crf", "21", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out)
    voice_slots = [(st, d - (st - t0) - 0.2) for (_, d, vp, st), t0 in zip(scenes, starts)]
    json.dump({"total": total, "starts": starts, "slots": voice_slots, "risers": risers, "cuts": cuts},
              open(out.replace(".mp4", "_timing.json"), "w"))  # minutage : permet de doubler la vidéo plus tard
    with ThreadPoolExecutor(6) as ex:  # pistes audio doublées en parallèle (même musique, même minutage)
        list(ex.map(lambda lt: dub_track(ep, lt[0], lt[1], voice_slots, total, cuts, risers, work, out.replace(".mp4", f"_{lt[0]}.m4a")),
                    ep.get("dub", {}).items()))
    review_sheet(out, review)
    b = os.path.basename(out)[:-4]; langs = list(ep.get("dub", {}))
    open(out.replace(".mp4", "_CONSIGNES_CHROME.md"), "w").write(f"""# Consignes pour Claude dans Chrome — {ep.get('youtube', {}).get('title', ep['title'])}
Dans YouTube Studio (chaîne Oddly Logical Science), mets en ligne `{b}.mp4`.
1. Titre, description, tags, traductions du titre/description : copier depuis `{b}_youtube.md`. Catégorie « Science & Technology ».
2. Miniature : `{b}_thumb.jpg`. Sous-titres anglais : `{b}.srt`.
3. « Contenu modifié ou synthétique » : Non (sauf si `{b}_youtube.md` dit le contraire).
4. Visibilité : Programmée (date/heure données par Claude). Ne jamais publier en Public sans accord.
5. Onglet Langues → pour chaque fichier {', '.join(f'`{b}_{l}.m4a`' for l in langs) or '(aucun)'} : ajouter la langue → Piste audio → envoyer. Si l'option n'existe pas, s'arrêter et le signaler.
6. Après publication : épingler en commentaire la question finale de la vidéo, et créer un post Communauté « Quiz » (onglet Créer > Post > Quiz) reprenant le quiz de la vidéo avec un lien vers elle (si l'option Quiz n'est pas disponible, faire un Sondage).
7. Ne PAS publier les Shorts maintenant : ils sortent après la vidéo, 1 par jour, avec « Vidéo associée » = cette vidéo.
""")
    if "--short" in sys.argv: print(out, round(total, 1), "s (short autonome)"); return
    make_shorts(ep, out, starts + [total])
    import publish_kit
    publish_kit.write_all(ep, out, srt_words, yt_chapters, thumb_src)
    print(out, round(total, 1), "s")

if __name__ == "__main__":
    main(*sys.argv[1:4])
