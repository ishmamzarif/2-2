"""Background 4 - a Fourier recap, and where it breaks.

Scene: FourierRecap
  * a waterfall: a pulse is a sum of cosines, one per frequency; the heights
    of the cosines are the spectrum X(j omega)
  * a growing signal e^{0.25t}u(t): the Fourier integrand is a growing spiral,
    the integral diverges - no Fourier transform
  * multiply by e^{-sigma t} first: for sigma > 0.25 the spiral shrinks and the
    integral converges. That weighted Fourier transform is the Laplace transform.
"""
from common3d import *

DW = 0.5                     # frequency spacing of the waterfall
KS = list(range(13))         # components k = 0 .. 12 (omega up to 6)
FRONT = -1.0                 # omega-coordinate of the lane where the sum is drawn


def X_pulse(w):
    """Fourier transform of the unit-height pulse on |t| < 1."""
    w = np.asarray(w, dtype=float)
    with np.errstate(all="ignore"):
        return np.where(np.abs(w) < 1e-9, 2.0, 2 * np.sin(w) / w)


def coef(k):
    w = k * DW
    return float(X_pulse(w)) * DW / (2 * np.pi if k == 0 else np.pi)


class FourierRecap(LScene):
    def construct(self):
        self.waterfall()
        self.when_fourier_fails()
        self.clear_all()

    # ------------------------------------------------------------------
    def waterfall(self):
        ax = ThreeDAxes(x_range=[-4, 4, 1], y_range=[FRONT, 6.5, 1], z_range=[-0.5, 1.25, 0.5],
                        x_length=9, y_length=6.5, z_length=3)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-68 * DEGREES, zoom=0.78, frame_center=ax.c2p(0.3, 2.3, 0.2))
        self.set_title("Fourier: a sum of sinusoids")

        front_axis = Line(ax.c2p(-4, FRONT, 0), ax.c2p(4.2, FRONT, 0), color=AXIS_COLOR, stroke_width=2)
        t_lab = MathTex("t", font_size=36, color=LABEL_COLOR).move_to(ax.c2p(4.5, FRONT, 0))
        w_axis = Line(ax.c2p(4.4, 0, 0), ax.c2p(4.4, 6.5, 0), color=AXIS_COLOR, stroke_width=2)
        w_lab = MathTex(r"\omega", font_size=40, color=LABEL_COLOR).move_to(ax.c2p(4.4, 6.9, 0))
        x_lab = MathTex(r"x(t)", font_size=40, color=YELLOW).move_to(ax.c2p(-4.6, FRONT, 0.9))
        self.face_camera(t_lab, w_lab, x_lab)

        pulse = VGroup(
            polyline(pts(ax, [-4, -1, -1, 1, 1, 4], FRONT, [0, 0, 1, 1, 0, 0]), GREY_B, 3),
        )
        self.play(Create(front_axis), FadeIn(t_lab), Create(pulse), FadeIn(x_lab), run_time=1.5)
        self.beat("a pulse", hold=1.0)

        K = ValueTracker(-1)
        ts = np.linspace(-4, 4, 400)

        def partial_sum():
            k_max = int(round(K.get_value()))
            if k_max < 0:
                return VGroup()
            ys = sum(coef(k) * np.cos(k * DW * ts) for k in range(k_max + 1))
            return polyline(pts(ax, ts, FRONT, ys), YELLOW, 5)

        summ = always_redraw(partial_sum)
        self.add(summ)
        self.play(Create(w_axis), FadeIn(w_lab))

        comps = VGroup()
        for k in KS:
            w = k * DW
            c = coef(k)
            base = DashedLine(ax.c2p(-4, w, 0), ax.c2p(4, w, 0), color=GREY_D, stroke_width=1, dash_length=0.1)
            wave = polyline(pts(ax, ts, w, c * np.cos(w * ts)), SIG, 3)
            comps.add(VGroup(base, wave))
            rt = 0.6 if k < 4 else 0.25
            self.play(FadeIn(base), Create(wave), run_time=rt)
            slider = wave.copy().set_stroke(YELLOW, 3, opacity=0.8)
            self.play(slider.animate.shift(ax.c2p(0, FRONT, 0) - ax.c2p(0, w, 0)).set_stroke(opacity=0.0),
                      K.animate.set_value(k), run_time=rt + 0.15)
            self.remove(slider)
            if k == 2:
                self.beat("each wave slides forward and adds in", hold=1.0)
        self.beat("13 sinusoids already make the pulse")

        # the heights of the waves: the spectrum, on the side wall
        ws = np.linspace(0, 6.2, 300)
        cs = X_pulse(ws) * DW / np.pi
        spec = polyline(pts(ax, 4.4, ws, cs), YELLOW, 4)
        dots = VGroup(*[Dot3D(ax.c2p(4.4, k * DW, coef(k) * (2 if k == 0 else 1)), radius=0.05, color=YELLOW) for k in KS])
        stems = VGroup(*[Line(ax.c2p(4.0, k * DW, coef(k)), ax.c2p(4.4, k * DW, coef(k) * (2 if k == 0 else 1)),
                              color=GREY_B, stroke_width=1.5) for k in KS])
        spec_lab = MathTex(r"X(j\omega)", font_size=40, color=YELLOW).move_to(ax.c2p(5.0, -0.7, 0.55))
        self.face_camera(spec_lab)
        self.play(Create(stems), run_time=1)
        self.play(Create(spec), FadeIn(dots), FadeIn(spec_lab), run_time=2)
        eqs = VGroup(
            MathTex(r"X(j\omega) = \int_{-\infty}^{\infty} x(t)\,e^{-j\omega t}\,dt", font_size=40),
            MathTex(r"x(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} X(j\omega)\,e^{j\omega t}\,d\omega", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.4)
        eqs = self.panel(eqs)
        self.play(FadeIn(eqs[1][0]), FadeIn(eqs[0]))
        self.beat("the spectrum: how much of each frequency")
        self.play(FadeIn(eqs[1][1]))
        self.beat("and back: add them all up")
        self.move_camera(theta=-40 * DEGREES, run_time=4)
        self.beat("the waterfall from another angle", hold=1.0)
        self.clear_all()

    # ------------------------------------------------------------------
    def when_fourier_fails(self):
        T_MAX, R = 8.0, 2.0
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=R, t_length=9, r_length=4)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-40 * DEGREES, gamma=0, zoom=0.82, frame_center=ax.c2p(T_MAX / 2 - 0.4, 0, 0.35))
        self.set_title("When Fourier fails")
        labs = ct_labels(ax)
        self.face_camera(*labs)
        a, w = 0.25, 2.0
        sig = ValueTracker(0.0)

        def z(t):
            return np.exp(complex(a - sig.get_value(), -w) * t)

        sig_eq = MathTex(r"x(t) = e^{0.25t}\,u(t)", font_size=44, color=SIG)
        sig_eq = self.panel(sig_eq.to_corner(UR, buff=0.5))
        self.play(Create(ax), FadeIn(labs), FadeIn(sig_eq))
        spiral = always_redraw(lambda: complex_curve(ax, z, 0, T_MAX, n=600, rmax=R, color=SIG, width=4))
        env = always_redraw(lambda: envelope(ax, a - sig.get_value(), T_MAX, R))
        integrand = self.hud(MathTex(r"x(t)\,e^{-j\omega t}", font_size=42).move_to([0.4, 2.9, 0]))
        self.play(Create(spiral), FadeIn(integrand), run_time=3)
        self.add(spiral)
        self.play(FadeIn(env))
        self.add(env)
        diverge = VGroup(
            MathTex(r"\int_0^{\infty} x(t)\,e^{-j\omega t}\,dt \;=\; \infty", font_size=42, color=BAD),
            Tex("no Fourier transform", font_size=38, color=BAD),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(sig_eq, DOWN, buff=0.35, aligned_edge=RIGHT)
        diverge = self.panel(diverge)
        self.play(FadeIn(diverge))
        self.beat("a growing spiral: the integral diverges")

        # the fix: weight by e^{-sigma t}
        integrand2 = MathTex(r"x(t)\,", r"e^{-\sigma t}", r"\,e^{-j\omega t}", font_size=42).move_to(integrand)
        integrand2[1].set_color(RED_B)
        self.hud(integrand2)
        sig_num = DecimalNumber(0, num_decimal_places=2, font_size=44, color=RED_B)
        sig_row = VGroup(MathTex(r"\sigma =", font_size=44, color=RED_B), sig_num).arrange(RIGHT, buff=0.15)
        sig_row.next_to(sig_eq, DOWN, buff=0.35, aligned_edge=RIGHT)
        sig_num.add_updater(lambda m: m.set_value(sig.get_value()).next_to(sig_row[0], RIGHT, buff=0.15))
        self.hud(sig_row, live=True)
        self.play(FadeOut(diverge), FadeTransform(integrand, integrand2), FadeIn(sig_row))
        self.beat("idea: first multiply by e^{-sigma t}", hold=1.0)
        self.play(sig.animate.set_value(0.25), run_time=3)
        self.beat("sigma = 0.25: just balanced", hold=1.0)
        self.play(sig.animate.set_value(0.6), run_time=3)
        conv = self.panel(VGroup(
            MathTex(r"\sigma > 0.25:\ \text{converges}", font_size=42, color=GOOD),
            MathTex(r"\mathcal{F}\{x(t)e^{-\sigma t}\} = X(\sigma + j\omega)", font_size=42, color=YELLOW),
            Tex("the Laplace transform", font_size=38, color=YELLOW),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(sig_row, DOWN, buff=0.35, aligned_edge=RIGHT))
        self.play(FadeIn(conv[0]), FadeIn(conv[1][0]))
        self.beat("weighted enough: it converges")
        self.play(FadeIn(conv[1][1]), FadeIn(conv[1][2]))
        self.beat("Fourier of the weighted signal = Laplace")
        sig_num.clear_updaters()
