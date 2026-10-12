from manim import *
import numpy as np
config.background_color = "#0b0f1a"
Text.set_default(font="Inter Display", weight="BOLD")
MarkupText.set_default(font="Inter Display")
def img(path): return path
class S(ThreeDScene):
    def construct(self):
        tex = 'preflight/clips/world.topo.bathy.200412.3x5400x2700.jpg'
        self.set_camera_orientation(phi=72*DEGREES, theta=-50*DEGREES, zoom=1.15)
        sph = Surface(lambda u, v: 2.3*np.array([np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), -np.cos(v)]), u_range=[0, TAU], v_range=[0, PI], resolution=(64, 32))
        earth = TexturedSurface(sph, tex)
        glow = Sphere(radius=2.42, resolution=(32, 16)).set_color(BLUE_B).set_opacity(0.12)
        eq = ParametricFunction(lambda t: 2.36*np.array([np.cos(t), np.sin(t), 0]), t_range=[0, TAU], color=YELLOW, stroke_width=5)
        title = Text("1,670 km/h", font_size=72, color=YELLOW).to_corner(UL).shift(DOWN*0.2)
        sub = Text("speed at the equator", font_size=30, color=WHITE, weight="NORMAL").next_to(title, DOWN, aligned_edge=LEFT)
        pole = Text("≈ 0 km/h at the poles", font_size=30, weight="NORMAL").to_corner(DR)
        for m in (title, sub, pole): self.add_fixed_in_frame_mobjects(m); m.set_opacity(0)
        self.add(glow, earth)
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(Rotate(earth, angle=PI/3, axis=OUT), run_time=1.5, rate_func=linear)
        self.play(Create(eq), title.animate.set_opacity(1), sub.animate.set_opacity(1), run_time=1.5)
        arrows = VGroup(*[Arrow3D(start=2.36*np.array([np.cos(a), np.sin(a), 0]), end=2.36*np.array([np.cos(a), np.sin(a), 0]) + 1.2*np.array([-np.sin(a), np.cos(a), 0]), color=ORANGE, thickness=0.03) for a in np.linspace(0, TAU, 10, endpoint=False)])
        self.play(LaggedStart(*[FadeIn(x, shift=0.2*OUT) for x in arrows], lag_ratio=0.08), pole.animate.set_opacity(1), run_time=1.8)
        self.play(Rotate(VGroup(earth, eq, arrows), angle=PI/2, axis=OUT), run_time=3, rate_func=linear)
        self.wait(0.1)
