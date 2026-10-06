"""Génère les éléments de marque réutilisables : intro (4 s) et outro / écran de fin (15 s), avec son.
Usage : python3 brand_assets.py <dossier_sortie>"""
import os, sys, wave, math, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visuals as v, render as r
from PIL import Image, ImageDraw

def with_sound(video, d, out, cuts):
    n = int(d * r.SR); mix = r.music(d, np.zeros(n), cuts) * 0.5
    wav = out + ".wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(r.SR); w.writeframes((np.tanh(mix) * 0.9 * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
    os.remove(wav); os.remove(video)

def outro(path, d=15.0):
    """Écran de fin : logo + « SUBSCRIBE », deux cadres vides pour les éléments de fin YouTube."""
    def fr(t):
        im = v._bg(t, 41); layer = Image.new("RGBA", (v.W, v.H), (0, 0, 0, 0)); dr = ImageDraw.Draw(layer)
        a = v.ease(t / 0.8)
        dr.text((v.W / 2, 150), "ODDLY LOGICAL SCIENCE", font=v.font("Black", 84), fill=(255, 255, 255, int(255 * a)), anchor="mm")
        dr.text((v.W / 2, 235), "THE UNIVERSE IS STRANGER THAN YOU THINK", font=v.font("SemiBold", 32), fill=v.PAL["gold"] + (int(255 * a),), anchor="mm")
        b = v.ease((t - 0.6) / 0.6)
        for x0 in (190, 1010):  # emplacements des vidéos suggérées (Studio > Écran de fin)
            dr.rounded_rectangle((x0, 360, x0 + 720, 765), 24, outline=(255, 255, 255, int(150 * b)), width=4)
            dr.text((x0 + 360, 562), "WATCH NEXT", font=v.font("Bold", 40), fill=(255, 255, 255, int(70 * b)), anchor="mm")
        p = 1 + 0.05 * math.sin(t * 5); c = v.ease((t - 1.0) / 0.5)
        w, h = int(520 * p), int(110 * p)
        dr.rounded_rectangle((v.W / 2 - w / 2, 900 - h / 2, v.W / 2 + w / 2, 900 + h / 2), 55, fill=(230, 40, 50, int(255 * c)))
        dr.text((v.W / 2, 900), "SUBSCRIBE", font=v.font("Black", int(56 * p)), fill=(255, 255, 255, int(255 * c)), anchor="mm")
        im = v._glow(im, layer, 14)
        f = min(1, t / 0.4, (d - t) / 0.8)
        return Image.eval(im, lambda x: int(x * max(0, f)))
    v._render(path, d, fr)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    v.intro(os.path.join(out, "_i.mp4"), 4.0); with_sound(os.path.join(out, "_i.mp4"), 4.0, os.path.join(out, "intro.mp4"), [0.9])
    outro(os.path.join(out, "_o.mp4"), 15.0); with_sound(os.path.join(out, "_o.mp4"), 15.0, os.path.join(out, "outro_end_screen.mp4"), [1.0])
    print("ok")
