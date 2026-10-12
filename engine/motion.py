"""Animations explicatives de niveau « documentaire » avec Manim (moteur de 3Blue1Brown).
Une scène `{"kind": "manim", "code": "<corps de construct()>"}` : le script de la vidéo écrit l'animation sur mesure
(globe texturé qui tourne, flèches de vitesse, graphiques qui se tracent, coupes, particules…).
Fonctions utilitaires disponibles dans le code : img(url) → chemin local d'une image (texture NASA, photo)."""
import os, subprocess, textwrap, shutil

HEADER = '''from manim import *
import numpy as np
config.background_color = "#0b0f1a"
def img(path): return path
class S(%s):
    def construct(self):
'''

def render(out, d, code, assets=None, three_d=False):
    work = out + "_manim"; os.makedirs(work, exist_ok=True)
    body = textwrap.indent(textwrap.dedent(code).strip() + "\nself.wait(0.1)\n", " " * 8)
    if assets:  # url → chemin local, injectés comme variables
        body = "".join(" " * 8 + f"{k} = {v!r}\n" for k, v in assets.items()) + body
    src = os.path.join(work, "scene.py"); open(src, "w").write(HEADER % ("ThreeDScene" if three_d else "Scene") + body)
    r = subprocess.run(["manim", "render", "-q", "h", "--fps", "30", "-r", "1920,1080", "--disable_caching",
                        "--media_dir", work, "-o", "anim.mp4", src, "S"], capture_output=True, text=True)
    mp4 = next((os.path.join(dp, f) for dp, _, fs in os.walk(work) for f in fs if f == "anim.mp4"), None)
    if r.returncode or not mp4:
        raise RuntimeError("Manim : " + (r.stderr or r.stdout)[-1500:])
    # durée exacte de la scène : on étire la fin (dernière image figée) ou on coupe
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", f"tpad=stop_mode=clone:stop_duration={d},fps=30,format=yuv420p",
                    "-t", str(d), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
    shutil.rmtree(work, ignore_errors=True)
