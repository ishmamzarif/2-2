"""Introduction to the inverse Laplace transform (the Bromwich integral).

Scene: InverseLaplace
  * derivation: X(sigma + j omega) is the Fourier transform of x(t) e^{-sigma t};
    invert the Fourier transform, multiply by e^{sigma t}, substitute s
  * geometry: walk up a vertical line Re{s} = sigma inside the ROC
  * each point s on the line contributes X(s) e^{st}: a waterfall of growing
    waves that adds up to the decaying e^{-t} u(t)
  * slide the line past the pole and the very same X(s) gives -e^{-t} u(-t)
  * closing the contour: the Cauchy residue theorem (beyond this course)
"""
from common3d import *

DW = 0.5
KS = list(range(13))
GAIN = 2.5
SIG_R = 0.3          # a line to the right of the pole
SIG_L = -1.5         # a line to the left of the pole


def X(s):
    return 1 / (s + 1)


def bromwich(sigma, ts, W=150.0, dw=0.01):
    """x(t) = (1/pi) * integral_0^W Re{X(sigma + j w) e^{(sigma + j w) t}} dw (real x)."""
    w = np.arange(0, W, dw)
    s = sigma + 1j * w
    vals = np.real(X(s)[None, :] * np.exp(np.outer(ts, s)))
    return np.trapezoid(vals, w, axis=1) / np.pi


def comp(sigma, k, ts):
    wk = k * DW
    c = (0.5 if k == 0 else 1.0) * DW / np.pi
    return c * np.real(X(sigma + 1j * wk) * np.exp((sigma + 1j * wk) * ts))


class InverseLaplace(LScene):
    def construct(self):
        self.derivation()
        self.the_line()
        self.waterfall()
        self.move_the_line()
        self.contour()
        self.clear_all()

    # ------------------------------------------------------------------
    def derivation(self):
        self.set_title("The inverse Laplace transform")
        rows = VGroup(
            MathTex(r"X(\sigma + j\omega) = \mathcal{F}\big\{x(t)\,e^{-\sigma t}\big\}", font_size=46),
            MathTex(r"x(t)\,e^{-\sigma t} = \frac{1}{2\pi}\int_{-\infty}^{\infty} X(\sigma + j\omega)\,e^{j\omega t}\,d\omega",
                    font_size=46),
            MathTex(r"x(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} X(\sigma + j\omega)\,e^{(\sigma + j\omega)t}\,d\omega", font_size=46),
            MathTex(r"x(t) = \frac{1}{2\pi j}\int_{\sigma - j\infty}^{\sigma + j\infty} X(s)\,e^{st}\,ds", font_size=54, color=YELLOW),
        ).arrange(DOWN, buff=0.4)
        notes = VGroup(
            Tex("Laplace = Fourier of the weighted signal", font_size=30, color=GREY_A),
            Tex("undo the Fourier transform", font_size=30, color=GREY_A),
            Tex(r"multiply both sides by $e^{\sigma t}$", font_size=30, color=GREY_A),
            Tex(r"$s = \sigma + j\omega,\ ds = j\,d\omega$; \ $\sigma$ in the ROC", font_size=30, color=YELLOW),
        )
        for n, r in zip(notes, rows):
            n.next_to(r, RIGHT, buff=0.4)
        grp = VGroup(rows, notes)
        grp.scale_to_fit_width(13.2).move_to(0.2 * DOWN)
        self.hud(grp)
        for i in range(4):
            self.play(FadeIn(rows[i], shift=0.2 * DOWN), FadeIn(notes[i]))
            self.beat(["start from the Fourier view", "invert the Fourier transform", "multiply by e^{sigma t}",
                       "the Bromwich integral"][i], hold=1.0 if i < 3 else 1.5)
        self.play(FadeOut(grp))

    # ------------------------------------------------------------------
    def landscape_stage(self):
        ax = splane_axes(u_range=(-3, 2), v_range=(-4, 4), z_max=4, x_length=5.5, y_length=8, z_length=3)
        camera_at(self, ax.c2p(-0.5, 0, 0.5), screen=(-2.0, -0.6), phi=60 * DEGREES, theta=-56 * DEGREES, zoom=0.74)
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        roc = roc_floor(ax, left=-1)
        surf = landscape(ax, X, res=(40, 56), roc=(-1, None))
        pole = pole_x(ax, -1)
        return ax, VGroup(floor, ax.x_axis, ax.y_axis, labs, roc, surf, pole), surf

    def the_line(self):
        self.set_title(r"Walk up a line inside the ROC")
        ax, stage, surf = self.landscape_stage()
        info = self.panel(VGroup(
            MathTex(r"X(s) = \frac{1}{s+1},\ \ \mathrm{Re}\{s\} > -1", font_size=40),
            MathTex(r"x(t) = \frac{1}{2\pi j}\int_{\sigma - j\infty}^{\sigma + j\infty} X(s)\,e^{st}\,ds", font_size=40, color=YELLOW),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).to_corner(UR, buff=0.4))
        self.play(FadeIn(stage), FadeIn(info), run_time=2)
        line = floor_vline(ax, SIG_R, color=YELLOW, width=5)
        sl = jw_slice(ax, X, sigma=SIG_R, color=YELLOW, width=6)
        lab = MathTex(r"\mathrm{Re}\{s\} = \sigma", font_size=34, color=YELLOW).move_to(ax.c2p(SIG_R + 0.2, -4.5, 0))
        self.face_camera(lab)
        self.play(Create(line), FadeIn(lab))
        self.play(Create(sl), run_time=2)
        self.beat("the values of X(s) along the line")
        each = self.panel(Tex(r"each point $s$ on the line adds a spiral $X(s)\,e^{st}$", font_size=36, color=YELLOW)
                          .to_edge(DOWN, buff=0.4))
        self.play(FadeIn(each))
        self.beat("each point contributes X(s) e^{st}", hold=1.0)
        self.clear_all()

    # ------------------------------------------------------------------
    def waterfall(self):
        FR = -1.0
        ax = ThreeDAxes(x_range=[-2, 5, 1], y_range=[FR, 6.5, 1], z_range=[-1.2, 1.6, 0.5], x_length=9, y_length=6.5, z_length=3)
        camera_at(self, ax.c2p(1.5, 2.6, 0.2), screen=(-0.6, -0.8), phi=64 * DEGREES, theta=-66 * DEGREES, zoom=0.82)
        self.set_title(r"Adding up $X(s)\,e^{st}$ along the line")
        ts = np.linspace(-2, 5, 500)
        t_axis = Line(ax.c2p(-2, FR, 0), ax.c2p(5.2, FR, 0), color=AXIS_COLOR, stroke_width=2)
        t_lab = MathTex("t", font_size=36, color=LABEL_COLOR).move_to(ax.c2p(5.5, FR, 0))
        w_axis = Line(ax.c2p(5.4, 0, 0), ax.c2p(5.4, 6.5, 0), color=AXIS_COLOR, stroke_width=2)
        w_lab = MathTex(r"\omega", font_size=40, color=LABEL_COLOR).move_to(ax.c2p(5.4, 6.9, 0))
        self.face_camera(t_lab, w_lab)
        target = polyline(pts(ax, ts, FR, np.exp(-ts) * (ts >= 0)), GREY_B, 2.5, opacity=0.8)
        tgt_lab = MathTex(r"e^{-t}u(t)", font_size=36, color=GREY_A).move_to(ax.c2p(-1.6, FR, 1.15))
        self.face_camera(tgt_lab)
        formula = self.panel(MathTex(r"x(t) \approx \frac{\Delta\omega}{2\pi}\sum_k X(\sigma + jk\Delta\omega)\,e^{(\sigma + jk\Delta\omega)t}",
                                     font_size=38).to_corner(UR, buff=0.4))
        self.play(Create(t_axis), FadeIn(t_lab), Create(w_axis), FadeIn(w_lab), Create(target), FadeIn(tgt_lab), FadeIn(formula))

        K = ValueTracker(-1)

        def partial():
            k_max = int(round(K.get_value()))
            if k_max < 0:
                return VGroup()
            ys = sum(comp(SIG_R, k, ts) for k in range(k_max + 1))
            return polyline(pts(ax, ts, FR, np.clip(ys, -1.2, 1.6)), YELLOW, 5)

        summ = always_redraw(partial)
        self.add(summ)
        for k in KS:
            wk = k * DW
            ys = GAIN * comp(SIG_R, k, ts)
            base = DashedLine(ax.c2p(-2, wk, 0), ax.c2p(5, wk, 0), color=GREY_D, stroke_width=1, dash_length=0.1)
            keep = np.abs(ys) <= 1.6
            wave = VGroup(*[polyline(pts(ax, ts[r], wk, ys[r]), SIG, 3) for r in true_runs(keep)])
            rt = 0.6 if k < 3 else 0.22
            self.play(FadeIn(base), Create(wave), run_time=rt)
            slider = wave.copy().set_stroke(YELLOW, 3, opacity=0.7)
            self.play(slider.animate.shift(ax.c2p(0, FR, 0) - ax.c2p(0, wk, 0)).set_stroke(opacity=0), K.animate.set_value(k),
                      run_time=rt + 0.15)
            self.remove(slider)
            if k == 2:
                self.beat("each wave grows like e^{sigma t}...", hold=1.0)
        self.beat("...yet together they rebuild e^{-t}u(t)")
        fine = polyline(pts(ax, ts, FR, np.clip(bromwich(SIG_R, ts), -1.2, 1.6)), YELLOW, 5)
        more = self.panel(Tex(r"all frequencies: the integral", font_size=36, color=YELLOW).to_edge(DOWN, buff=0.4))
        self.play(FadeIn(more), Transform(summ, fine), run_time=2)
        summ.clear_updaters()
        self.beat("in the limit: exactly x(t)")
        self.move_camera(theta=-40 * DEGREES, run_time=3)
        self.wait(0.5)
        self.clear_all()

    # ------------------------------------------------------------------
    def move_the_line(self):
        self.set_title(r"Move the line past the pole")
        ax, stage, surf = self.landscape_stage()
        sv = ValueTracker(SIG_R)
        line = always_redraw(lambda: floor_vline(ax, sv.get_value(), color=YELLOW, width=5))
        self.play(FadeIn(stage), Create(line), run_time=1.5)
        self.add(line)
        sax = mini_axes(x_range=(-3, 3, 1), y_range=(-3, 1.4, 1), width=4.2, height=2.6, x_label="t", y_label="x(t)", size=24)
        sax.to_corner(UR, buff=0.45).shift(0.4 * DOWN)
        sbg = BackgroundRectangle(sax, fill_color=PANEL_BG, fill_opacity=0.85, buff=0.15)
        sbg.hud_layer = -1
        ts = np.linspace(-3, 3, 400)
        g_r = graph2d(sax, lambda t: np.interp(t, ts, bromwich(SIG_R, ts)), -3, 3, color=YELLOW, width=4)
        g_l = graph2d(sax, lambda t: np.interp(t, ts, bromwich(SIG_L, ts)), -3, 3, color=YELLOW, width=4)
        cap_r = MathTex(r"\sigma = 0.3:\ \ e^{-t}u(t)", font_size=36, color=YELLOW).next_to(sax, DOWN, buff=0.2)
        cap_l = MathTex(r"\sigma = -1.5:\ \ -e^{-t}u(-t)", font_size=36, color=YELLOW).next_to(sax, DOWN, buff=0.2)
        self.hud(sbg, sax, g_r, g_l, cap_r, cap_l)
        self.play(FadeIn(sbg), FadeIn(sax), Create(g_r), FadeIn(cap_r))
        self.beat("line right of the pole: e^{-t}u(t)")
        self.play(sv.animate.set_value(-0.97), run_time=2.5)
        self.play(sv.animate.set_value(-1.03), FadeOut(g_r), FadeOut(cap_r), roc_transition(surf, (-1, None), (None, -1)),
                  FadeIn(g_l), FadeIn(cap_l), run_time=1.2)
        self.play(sv.animate.set_value(SIG_L), run_time=1.5)
        flip = self.panel(Tex(r"same $X(s)$, line left of the pole: the left-sided signal", font_size=34, color=YELLOW)
                          .to_edge(DOWN, buff=0.4))
        self.play(FadeIn(flip))
        self.beat("left of the pole: -e^{-t}u(-t)")
        self.clear_all()

    # ------------------------------------------------------------------
    def contour(self):
        self.set_title(r"Closing the contour (a peek)")
        sp = MiniSPlane(x_range=(-3, 2, 1), y_range=(-3, 3, 1), width=4.6, height=5.2, size=22).shift(2.6 * LEFT + 0.35 * DOWN)
        pole = sp.pole(-1, size=0.12, width=6)
        line = sp.vline(SIG_R, color=YELLOW, width=5)
        R = 2.55
        center = sp.c2p(SIG_R, 0)
        unit = sp.plane.get_x_unit_size()
        left_arc = Arc(radius=R * unit, start_angle=PI / 2, angle=PI, arc_center=center, color=GOOD, stroke_width=5)
        right_arc = Arc(radius=R * unit, start_angle=-PI / 2, angle=PI, arc_center=center, color=BAD, stroke_width=5)
        notes = VGroup(
            Tex(r"$t > 0$: close to the left,", font_size=36, color=GOOD),
            Tex(r"the pole is inside: $x(t) = e^{-t}$", font_size=36, color=GOOD),
            Tex(r"$t < 0$: close to the right,", font_size=36, color=BAD),
            Tex(r"nothing inside: $x(t) = 0$", font_size=36, color=BAD),
            MathTex(r"\oint_C f(s)\,ds = 2\pi j \sum \text{residues inside } C", font_size=36, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(sp, RIGHT, buff=0.6)
        notes[2].shift(0.2 * DOWN)
        notes[3].shift(0.2 * DOWN)
        notes[4].shift(0.4 * DOWN)
        self.hud(sp, pole, line, left_arc, right_arc, notes)
        self.play(FadeIn(sp), FadeIn(pole), Create(line))
        self.play(Create(left_arc), FadeIn(notes[0]), FadeIn(notes[1]), run_time=2)
        self.beat("t > 0: enclose the pole")
        self.play(Create(right_arc), FadeIn(notes[2]), FadeIn(notes[3]), run_time=2)
        self.beat("t < 0: enclose nothing")
        self.play(FadeIn(notes[4]))
        self.beat("the residue theorem does the integral", hold=1.0)
