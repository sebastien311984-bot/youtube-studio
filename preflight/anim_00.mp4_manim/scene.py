from manim import *
import numpy as np
config.background_color = "#0b0f1a"
def img(path): return path
class S(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-40*DEGREES)
        earth = Surface(lambda u, v: np.array([np.cos(u)*np.cos(v), np.sin(u)*np.cos(v), np.sin(v)])*2.2,
            u_range=[0, TAU], v_range=[-PI/2, PI/2], resolution=(48, 24))
        earth.set_style(fill_opacity=1, stroke_width=0)
        earth.set_fill_by_texture = None
        earth.set_color_by_gradient(BLUE_E, TEAL_D, BLUE_D)
        eq = ParametricFunction(lambda t: np.array([2.25*np.cos(t), 2.25*np.sin(t), 0]), t_range=[0, TAU], color=YELLOW, stroke_width=6)
        axis = Line3D(start=[0,0,-3.2], end=[0,0,3.2], color=WHITE)
        title = Text("1,670 km/h at the equator", font_size=48, color=YELLOW).to_corner(UL)
        pole = Text("≈ 0 km/h at the poles", font_size=40).to_corner(DL)
        self.add_fixed_in_frame_mobjects(title, pole); title.set_opacity(0); pole.set_opacity(0)
        self.play(FadeIn(earth), Create(axis), run_time=1.5)
        self.play(Create(eq), title.animate.set_opacity(1), run_time=1.5)
        arrows = VGroup(*[Arrow3D(start=2.25*np.array([np.cos(a), np.sin(a), 0]), end=2.25*np.array([np.cos(a), np.sin(a), 0]) + 1.1*np.array([-np.sin(a), np.cos(a), 0]), color=ORANGE) for a in np.linspace(0, TAU, 8, endpoint=False)])
        self.play(LaggedStart(*[GrowFromPoint(x, x.get_start()) for x in arrows], lag_ratio=0.1), pole.animate.set_opacity(1), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.25)
        self.play(Rotate(VGroup(earth, eq, arrows), angle=PI/2, axis=OUT), run_time=3)
                self.wait(0.01)