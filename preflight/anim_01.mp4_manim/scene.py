from manim import *
import numpy as np
config.background_color = "#0b0f1a"
def img(path): return path
class S(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 300, 50], y_range=[0, 100, 20], x_length=11, y_length=5.5, axis_config={"color": GREY_B, "include_numbers": True, "font_size": 28}).shift(DOWN*0.4)
        xl = Text("Pan temperature (°C)", font_size=30).next_to(ax.x_axis, DOWN)
        yl = Text("Drop lifetime (s)", font_size=30).rotate(PI/2).next_to(ax.y_axis, LEFT)
        self.play(Create(ax), FadeIn(xl, yl), run_time=1.5)
        f = lambda x: 80*np.exp(-(x-100)/25) if x < 190 else 5 + 70*(1-np.exp(-(x-190)/20))
        curve = ax.plot(lambda x: min(95, f(x)) if x > 100 else 95, x_range=[100, 300, 1], color=YELLOW, stroke_width=6)
        self.play(Create(curve), run_time=3, rate_func=linear)
        dot = Dot(ax.c2p(190, f(190)), color=RED, radius=0.12)
        lab = Text("Leidenfrost point ≈ 200 °C", font_size=34, color=RED).next_to(dot, UR)
        self.play(GrowFromCenter(dot), Write(lab), Flash(dot, color=RED), run_time=1.5)
                self.wait(0.01)