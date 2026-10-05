"""How the Laplace transform comes up - LTI systems and their eigenfunctions.

Scene: HowItComesUp
  * convolution as a waterfall: the output is a sum of delayed copies of the
    input, weighted by h(tau)
  * feed in e^{st}: a delayed copy of the spiral is the same spiral, rotated
    and scaled by the complex number e^{-s tau}
  * so every copy, and their sum, is a multiple of e^{st}: y = H(s) e^{st}
  * H(s) = integral of h(tau) e^{-s tau}: on s = j omega it is the frequency
    response (Fourier), anywhere else it is the Laplace transform of h
"""
from common3d import *

DTAU = 0.5
TAUS = np.arange(0, 3.01, DTAU)


def h(tau):
    return np.exp(-0.8 * np.asarray(tau)) * (np.asarray(tau) >= 0)


def bump(t):
    """A smooth input pulse on [0, 1.5]."""
    t = np.asarray(t, dtype=float)
    return np.where((t >= 0) & (t <= 1.5), np.sin(np.pi * t / 1.5) ** 2, 0.0)


def support(tau):
    """Times where the delayed bump lives (plus a little flat lead-in and tail)."""
    return np.linspace(tau - 0.4, tau + 1.9, 120)


class HowItComesUp(LScene):
    def construct(self):
        self.convolution_waterfall()
        self.eigenfunction()
        self.clear_all()

    # ------------------------------------------------------------------
    def convolution_waterfall(self):
        ax = ThreeDAxes(x_range=[-1, 7, 1], y_range=[-1.2, 3.4, 1], z_range=[0, 1.2, 0.5], x_length=9, y_length=5.5, z_length=2.6)
        camera_at(self, ax.c2p(2.4, 1.0, 0.5), screen=(-0.6, -0.6), phi=66 * DEGREES, theta=-58 * DEGREES, zoom=1.0)
        self.set_title("LTI systems: convolution")
        FR = -1.2
        diagram = VGroup(
            MathTex("x(t)", font_size=40, color=SIG),
            Arrow(LEFT, RIGHT, buff=0, color=GREY_B, stroke_width=3).scale(0.5),
            MathTex("h(t)", font_size=40).add_background_rectangle(color=GREY_E, opacity=1, buff=0.15),
            Arrow(LEFT, RIGHT, buff=0, color=GREY_B, stroke_width=3).scale(0.5),
            MathTex("y(t)", font_size=40, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        conv = MathTex(r"y(t) = \int h(\tau)\,x(t-\tau)\,d\tau", font_size=40)
        top = VGroup(diagram, conv).arrange(DOWN, buff=0.25, aligned_edge=RIGHT).to_corner(UR, buff=0.4)
        top = self.panel(top)
        self.play(FadeIn(top))
        self.beat("an LTI system", hold=1.0)

        ts = np.linspace(-1, 7, 500)
        t_axis = Line(ax.c2p(-1, FR, 0), ax.c2p(7.2, FR, 0), color=AXIS_COLOR, stroke_width=2)
        tau_axis = Line(ax.c2p(-1.2, 0, 0), ax.c2p(-1.2, 3.4, 0), color=AXIS_COLOR, stroke_width=2)
        t_lab = MathTex("t", font_size=34, color=LABEL_COLOR).move_to(ax.c2p(7.5, FR, 0))
        tau_lab = MathTex(r"\tau", font_size=38, color=LABEL_COLOR).move_to(ax.c2p(-1.2, 3.75, 0))
        self.face_camera(t_lab, tau_lab)
        x_in = polyline(pts(ax, support(0.0), 0, bump(support(0.0))), SIG, 4)
        x_lab = MathTex("x(t)", font_size=36, color=SIG).move_to(ax.c2p(0.75, 0, 1.45))
        self.face_camera(x_lab)
        self.play(Create(t_axis), Create(tau_axis), FadeIn(t_lab), FadeIn(tau_lab), Create(x_in), FadeIn(x_lab), run_time=1.5)

        # the weights h(tau) on the side wall
        tt = np.linspace(0, 3.4, 200)
        h_curve = polyline(pts(ax, -1.2, tt, h(tt)), RED_B, 4)
        h_dots = VGroup(*[Dot3D(ax.c2p(-1.2, tau, float(h(tau))), radius=0.05, color=RED_B) for tau in TAUS])
        h_lab = MathTex(r"h(\tau)", font_size=36, color=RED_B).move_to(ax.c2p(-1.6, 0.4, 1.3))
        self.face_camera(h_lab)
        self.play(Create(h_curve), FadeIn(h_dots), FadeIn(h_lab), run_time=1.2)
        self.beat("weights h(tau) along the tau axis", hold=1.0)

        copies = VGroup()
        for tau in TAUS[1:]:
            copies.add(polyline(pts(ax, support(tau), tau, float(h(tau)) * bump(support(tau) - tau)), SIG, 3, opacity=0.9))
        self.play(LaggedStart(*[Create(c) for c in copies], lag_ratio=0.25), run_time=3)
        self.beat("delayed copies x(t - tau), scaled by h(tau)")

        # their sum is the output (drawn in the front lane)
        y_vals = DTAU * sum(float(h(tau)) * bump(ts - tau) for tau in TAUS)
        y_curve = polyline(pts(ax, ts, FR, y_vals), YELLOW, 5)
        y_lab = MathTex("y(t)", font_size=38, color=YELLOW).move_to(ax.c2p(2.2, FR, 1.0))
        self.face_camera(y_lab)
        sliders = VGroup(x_in.copy(), *[c.copy() for c in copies])
        self.play(*[m.animate.shift(ax.c2p(0, FR, 0) - ax.c2p(0, tau, 0)).set_stroke(opacity=0.15)
                    for m, tau in zip(sliders, TAUS)],
                  Create(y_curve), run_time=2.5)
        self.play(FadeOut(sliders), FadeIn(y_lab))
        self.beat("add them up: the output y(t)")
        self.clear_all()

    # ------------------------------------------------------------------
    def eigenfunction(self):
        T_MAX, R = 8.0, 1.6
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=R, t_length=9, r_length=3.4)
        camera_at(self, ax.c2p(T_MAX / 2, 0, 0), screen=(-1.6, -0.6), phi=68 * DEGREES, theta=-40 * DEGREES, zoom=0.86)
        self.set_title(r"Feed in $e^{st}$")
        labs = ct_labels(ax)
        self.face_camera(*labs)
        s = complex(0.05, 2.0)
        tau = 0.6

        def e_st(t):
            return np.exp(s * t)

        spiral = complex_curve(ax, e_st, 0, T_MAX, n=600, rmax=R, color=SIG, width=4)
        in_lab = MathTex(r"e^{st}", font_size=40, color=SIG).move_to(ax.c2p(T_MAX + 0.3, 0.2, 1.5))
        self.face_camera(in_lab)
        self.play(Create(ax), FadeIn(labs))
        self.play(Create(spiral), FadeIn(in_lab), run_time=3)
        self.beat("the input spiral", hold=1.0)

        # a delayed copy
        delayed = complex_curve(ax, lambda t: np.exp(s * (t - tau)), 0, T_MAX, n=600, rmax=R, color=PURPLE_B, width=4)
        d_lab = MathTex(r"e^{s(t-\tau)}", font_size=40, color=PURPLE_B).move_to(ax.c2p(T_MAX + 0.3, 0.2, -1.4))
        self.face_camera(d_lab)
        moving = spiral.copy().set_stroke(PURPLE_B)
        self.play(moving.animate.shift(RIGHT * ax.x_axis.get_unit_size() * tau), run_time=2)
        self.play(FadeIn(delayed), FadeOut(moving), FadeIn(d_lab))
        self.beat("delay it by tau")

        eq = MathTex(r"e^{s(t-\tau)}", r"=", r"e^{-s\tau}", r"\,e^{st}", font_size=46)
        eq[0].set_color(PURPLE_B)
        eq[2].set_color(YELLOW)
        eq[3].set_color(SIG)
        note = Tex(r"a complex number:\\ rotate + scale", font_size=32, color=YELLOW)
        blk = VGroup(eq, note).arrange(DOWN, buff=0.2).to_corner(UR, buff=0.45)
        blk = self.panel(blk)
        self.play(FadeIn(blk))
        twin = spiral.copy().set_stroke(YELLOW, 6, opacity=0.9)
        origin = ax.c2p(0, 0, 0)
        k = np.exp(-s.real * tau)
        self.add(twin)
        self.play(Rotate(twin, angle=-s.imag * tau, axis=RIGHT, about_point=origin), run_time=2.5)
        self.play(twin.animate.stretch(k, 1, about_point=origin).stretch(k, 2, about_point=origin), run_time=1)
        self.beat("same spiral, turned by omega*tau")
        self.play(FadeOut(twin))

        # every copy is a multiple of e^{st}, so the sum is too
        derivation = VGroup(
            MathTex(r"y(t) = \int h(\tau)\, e^{s(t-\tau)}\,d\tau", font_size=40),
            MathTex(r"= e^{st} \int h(\tau)\,e^{-s\tau}\,d\tau", font_size=40),
            MathTex(r"= H(s)\, e^{st}", font_size=44, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.45)
        derivation = self.panel(derivation)
        self.play(FadeOut(blk), FadeIn(derivation[0]), FadeIn(derivation[1][0]))
        self.play(FadeIn(derivation[1][1]))
        H = 1 / (s + 1)          # h(t) = e^{-t} u(t)
        out = complex_curve(ax, lambda t: H * np.exp(s * t), 0, T_MAX, n=600, rmax=R, color=YELLOW, width=5)
        out_lab = MathTex(r"H(s)\,e^{st}", font_size=40, color=YELLOW).move_to(ax.c2p(T_MAX + 0.4, 0.3, 0.5))
        self.face_camera(out_lab)
        self.play(FadeOut(delayed), FadeOut(d_lab), FadeIn(derivation[1][2]))
        self.play(TransformFromCopy(spiral, out), FadeIn(out_lab), run_time=2.5)
        self.beat("out comes the same spiral, times H(s)")

        name = VGroup(
            MathTex(r"H(s) = \int_{-\infty}^{\infty} h(\tau)\,e^{-s\tau}\,d\tau", font_size=44, color=YELLOW),
            MathTex(r"s = j\omega:\ \text{frequency response (Fourier)}", font_size=36),
            MathTex(r"\text{any } s:\ \text{the Laplace transform of } h", font_size=36, color=YELLOW),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.22).to_corner(UR, buff=0.45)
        name = self.panel(name)
        self.play(FadeOut(derivation), FadeIn(name[0]), FadeIn(name[1][0]))
        self.beat("H(s): one complex number per s")
        self.play(FadeIn(name[1][1]))
        self.play(FadeIn(name[1][2]))
        self.beat("s = j omega: Fourier; any s: Laplace")
