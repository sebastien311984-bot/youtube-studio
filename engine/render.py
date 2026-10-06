"""Moteur Oddly Logical Science (v0) : épisode JSON -> MP4 16:9.
Voix Edge TTS (minutage mot à mot), plans NASA recadrés avec lent travelling, étalonnage,
fondus enchaînés, sous-titres et titres animés (ASS), musique d'ambiance synthétisée avec ducking.
Usage : python3 render.py episode.json clips_dir out.mp4"""
import asyncio, json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visuals

W, H, FPS, SR, XF = 1920, 1080, 30, 44100, 0.6
CA = "/root/.ccr/ca-bundle.crt"

def sh(*a): subprocess.run(a, check=True)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def tts(text, voice, path):
    if os.path.exists(CA):  # proxy de l'environnement Claude ; inutile sur GitHub Actions
        import certifi, ssl; certifi.where = lambda: CA
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=CA)
    import edge_tts
    words = []
    async def run():
        c = edge_tts.Communicate(text, voice, rate="-4%", pitch="-4Hz", boundary="WordBoundary")
        with open(path, "wb") as f:
            async for ch in c.stream():
                if ch["type"] == "audio": f.write(ch["data"])
                elif ch["type"] == "WordBoundary": words.append((ch["offset"] / 1e7, ch["duration"] / 1e7, ch["text"]))
    asyncio.run(run()); return words

def fetch(src, clips_dir):
    """Un plan peut être un fichier local ou une URL (téléchargée une seule fois, mise en cache)."""
    if not src.startswith("http"): return os.path.join(clips_dir, src)
    os.makedirs(clips_dir, exist_ok=True); local = os.path.join(clips_dir, src.rsplit("/", 1)[-1])
    if not os.path.exists(local): sh("curl", "-sSL", "--retry", "3", "-o", local, src)
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
    sh("ffmpeg", "-v", "error", "-y", *inp, "-t", str(d), "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", out)

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
        a = bounds[sp["from"]]; b = min(bounds[sp["to"]], a + 58)
        if b - a < 30: b = min(bounds[-1] - 2, a + 45)  # un Short doit durer au moins 30 s
        tf = out[:-4] + f"_short{k}.txt"; open(tf, "w").write(sp["title"].upper())
        vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.15[bg];"
              f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,"
              f"drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Black.otf:textfile={tf}:fontsize=64:fontcolor=white:"
              f"borderw=6:bordercolor=black:x=(w-tw)/2:y=360,"
              f"drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf:text='FULL VIDEO ON THE CHANNEL':fontsize=38:fontcolor=0xFFC840:x=(w-tw)/2:y=1560,"
              f"fade=t=out:st={b - a - 0.6:.2f}:d=0.6")
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-i", out, "-filter_complex", vf, "-c:v", "libx264", "-preset", "medium",
           "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out[:-4] + f"_short{k}.mp4")
        os.remove(tf)

def music(total, voice_env, cuts):
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
    # « hits » cinématiques + whoosh aux transitions
    for c in cuts:
        i = int(c * SR); m = int(1.2 * SR); x = np.arange(m) / SR
        hit = (np.sin(2 * np.pi * 45 * x) * 0.9 + rng.standard_normal(m) * 0.15) * np.exp(-x * 3.5)
        sw = int(0.8 * SR); xs = np.arange(sw) / SR
        whoosh = np.convolve(rng.standard_normal(sw), np.ones(30) / 30, "same") * np.sin(np.pi * xs / 0.8) ** 3 * 2.2
        if i - sw > 0: out[i - sw:i] += whoosh * 0.5
        out[i:i + m] += hit[:max(0, min(m, n - i))] * 0.5
    env = np.minimum(1, t / 2) * np.minimum(1, (total - t) / 2.5)
    return out * env * (1 - 0.6 * voice_env)

def main(ep_path, clips_dir, out):
    ep = json.load(open(ep_path)); work = os.path.join(os.path.dirname(os.path.abspath(out)), "_work"); os.makedirs(work, exist_ok=True)
    voice = ep.get("voice", "en-US-AndrewMultilingualNeural")
    scenes, t, events, cuts = [], 0.0, [], []
    srt_words, yt_chapters, thumb_src, starts, trans = [], [], None, [], []
    for i, s in enumerate(ep["scenes"]):
        vp = os.path.join(work, f"v{i}.mp3")
        words = tts(s["text"], voice, vp) if s.get("text") else []
        vd = dur(vp) if words else 0
        d = max(s.get("min", 0), vd + s.get("pad", 0.7) + s.get("lead", 0.3))
        cp = os.path.join(work, f"c{i}.mp4"); kind = s.get("kind", "footage")
        if kind == "intro": visuals.intro(cp, d + XF)
        elif kind == "diagram": visuals.diagram(cp, d + XF, s["elements"], s.get("heading"))
        elif kind == "stat": visuals.bigstat(cp, d + XF, s["value"], s.get("prefix", ""), s.get("suffix", ""), s.get("caption", ""))
        elif kind == "scale": visuals.scale(cp, d + XF, s["items"], s.get("heading", ""))
        elif kind == "timeline": visuals.timeline(cp, d + XF, s["events"], s.get("heading", ""))
        elif kind == "versus": visuals.versus(cp, d + XF, s["left"], s["right"], s.get("heading", ""))
        elif kind == "quiz": visuals.quiz(cp, d + XF, s["question"], s["options"], s["answer"])
        elif kind == "kinetic": visuals.kinetic(cp, d + XF, s["words"])
        elif kind == "rank": visuals.rank(cp, d + XF, s["number"], s["title_rank"], s.get("sub", ""))
        else:
            # plusieurs plans dans une scène : coupe toutes les ~4 s pour garder du rythme
            shots = s.get("shots") or [{"clip": s["clip"], "start": s.get("start", 0), "move": s.get("move", "in")}]
            sd = (d + XF) / len(shots); parts = []
            for j, sh_ in enumerate(shots):
                pp = os.path.join(work, f"c{i}_{j}.mp4"); parts.append(pp)
                clip(fetch(sh_["clip"], clips_dir), sh_.get("start", 0), sd, pp, sh_.get("move", "in"))
            if len(parts) == 1: os.replace(parts[0], cp)
            else:
                lst = os.path.join(work, f"l{i}.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
                sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", cp)
        scenes.append((cp, d, vp if words else None, t + s.get("lead", 0.3)))
        events += captions(words, t + s.get("lead", 0.3))
        srt_words += [(t + s.get("lead", 0.3) + w0, w1, w2) for (w0, w1, w2) in words]
        if s.get("yt_chapter") or s.get("chapter"): yt_chapters.append((t, s.get("yt_chapter") or s["chapter"][1].title()))
        if s.get("kind") != "diagram" and s.get("kind") != "stat" and i == ep.get("thumbnail", {}).get("scene"): thumb_src = (cp, d)
        if "label" in s: events += label(t + 0.8, min(d - 1, 5), *s["label"])
        if "fact" in s: events += fact(t + min(2.5, d / 3), min(6, d - 1), s["fact"])
        if "chapter" in s: events += chapter(t + 0.2, *s["chapter"])
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
    n = int(total * SR); vtrack = np.zeros(n)
    for _, _, vp, st in scenes:
        if not vp: continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vp, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
        v = np.frombuffer(raw, np.int16).astype(float) / 32768; i = int(st * SR); m = min(len(v), n - i); vtrack[i:i + m] += v[:m]
    k = int(0.15 * SR); env = np.convolve(np.abs(vtrack), np.ones(k) / k, "same"); env = np.minimum(1, env / 0.04)
    mix = vtrack * 1.15 + music(total, env, cuts[1:]) * 0.33
    mix = np.tanh(mix * 1.1) * 0.93
    wav = os.path.join(work, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    sh("ffmpeg", "-v", "error", "-y", *inputs, "-i", wav, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", f"{len(scenes)}:a",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out)
    make_shorts(ep, out, starts + [total])
    import publish_kit
    publish_kit.write_all(ep, out, srt_words, yt_chapters, thumb_src)
    print(out, round(total, 1), "s")

if __name__ == "__main__":
    main(*sys.argv[1:4])
