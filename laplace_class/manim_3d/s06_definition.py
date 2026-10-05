"""What the Laplace transform is - the definition, and the e^{-sigma t} weighting.

Scene: LaplaceDefinition
  * X(s) = integral of x(t) e^{-st}, s = sigma + j omega
  * X(sigma + j omega) = Fourier transform of x(t) e^{-sigma t}
  * x(t) = e^{0.5t} u(t) has no Fourier transform; a stack of weighted copies
    x(t) e^{-sigma t}, one per sigma, shows which sigma tame it
  * those sigma form the region of convergence; on the s-plane it is the half
    plane Re{s} > 0.5, every omega included
"""
from common3d import *

A = 0.5            # x(t) = e^{A t} u(t)
T_MAX = 6.0
ZMAX = 2.2
SIGMAS = [-0.25, 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]


def sig_color(sigma):
    if abs(sigma - A) < 1e-9:
        return GREY_A
    return BAD if sigma < A else GOOD


class LaplaceDefinition(LScene):
    def construct(self):
        self.definition()
        self.weighting_stack()
        self.onto_the_s_plane()
        self.clear_all()

    # ------------------------------------------------------------------
    def definition(self):
        self.set_title("The Laplace transform")
        defn = MathTex(r"X(s) = \int_{-\infty}^{\infty} x(t)\,e^{-st}\,dt", font_size=60)
        s_def = MathTex(r"s = \sigma + j\omega", font_size=48)
        pair = MathTex(r"x(t) \xleftrightarrow{\ \mathcal{L}\ } X(s)", font_size=48, color=GREY_A)
        g = VGroup(defn, s_def, pair).arrange(DOWN, buff=0.45)
        self.hud(g)
        self.play(Write(defn), run_time=2)
        self.play(FadeIn(s_def, shift=0.2 * UP))
        self.play(FadeIn(pair, shift=0.2 * UP))
        self.beat("the definition")

        split = MathTex(r"X(\sigma + j\omega) = \int_{-\infty}^{\infty}", r"\big[x(t)\,e^{-\sigma t}\big]", r"\,e^{-j\omega t}\,dt",
                        font_size=52)
        split[1].set_color(YELLOW)
        fourier = MathTex(r"= \mathcal{F}\big\{x(t)\,e^{-\sigma t}\big\}", font_size=52, color=YELLOW)
        g2 = VGroup(split, fourier).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(ORIGIN)
        self.hud(g2)
        self.play(FadeOut(pair), FadeOut(s_def), defn.animate.scale(0.75).to_edge(UP, buff=1.1))
        self.play(FadeIn(split))
        self.play(FadeIn(fourier, shift=0.2 * DOWN))
        self.beat("a Fourier transform of the weighted signal")
        self.play(FadeOut(split), FadeOut(fourier), FadeOut(defn))

    # ------------------------------------------------------------------
    def weighting_stack(self):
        ax = ThreeDAxes(x_range=[0, T_MAX, 1], y_range=[-0.5, 1.75, 0.5], z_range=[0, ZMAX, 1],
                        x_length=8, y_length=6, z_length=3,
                        axis_config={"stroke_color": AXIS_COLOR, "include_tip": False, "stroke_width": 2, "tick_size": 0.05})
        self.ax = ax
        camera_at(self, ax.c2p(2.4, 0.65, 0.8), screen=(-0.9, -0.25), phi=64 * DEGREES, theta=-66 * DEGREES, zoom=1.15)
        self.set_title(r"Weighting $x(t) = e^{0.5t}u(t)$ by $e^{-\sigma t}$")
        t_lab = MathTex("t", font_size=36, color=LABEL_COLOR).move_to(ax.c2p(T_MAX + 0.35, -0.5, 0))
        s_lab = MathTex(r"\sigma", font_size=40, color=RED_B).move_to(ax.c2p(-0.35, 1.95, 0))
        self.face_camera(t_lab, s_lab)
        t_axis = Line(ax.c2p(0, -0.5, 0), ax.c2p(T_MAX, -0.5, 0), color=AXIS_COLOR, stroke_width=2)
        s_axis = Line(ax.c2p(0, -0.5, 0), ax.c2p(0, 1.75, 0), color=RED_B, stroke_width=3)
        s_ticks = VGroup(*[MathTex(f"{v:g}", font_size=24, color=GREY_A).move_to(ax.c2p(-0.35, v, 0)) for v in (0, 0.5, 1, 1.5)])
        self.face_camera(*s_ticks)
        self.play(Create(t_axis), Create(s_axis), FadeIn(t_lab), FadeIn(s_lab), FadeIn(s_ticks))

        ts = np.linspace(0, T_MAX, 300)

        def weighted(sigma, color=None, width=4, opacity=1.0):
            return real_curve_y(ax, lambda t: np.exp((A - sigma) * t), sigma, color or sig_color(sigma), width, opacity)

        # the raw signal first (sigma = 0 slice)
        raw = weighted(0.0, color=SIG, width=5)
        raw_lab = MathTex(r"x(t)", font_size=38, color=SIG).move_to(ax.c2p(1.2, 0.0, 2.0))
        self.face_camera(raw_lab)
        self.play(Create(raw), FadeIn(raw_lab), run_time=1.5)
        self.beat("the signal grows: no Fourier transform", hold=1.0)

        stack = VGroup(*[weighted(sg, opacity=0.9) for sg in SIGMAS])
        self.play(FadeOut(raw_lab), FadeOut(raw), LaggedStart(*[Create(c) for c in stack], lag_ratio=0.2), run_time=3)
        legend = VGroup(
            Tex(r"grows: diverges", font_size=34, color=BAD),
            Tex(r"$\sigma = 0.5$: flat", font_size=34, color=GREY_A),
            Tex(r"decays: converges", font_size=34, color=GOOD),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.5).shift(0.6 * DOWN)
        legend = self.panel(legend)
        self.play(FadeIn(legend))
        self.beat("one weighted copy per sigma")

        # sweep a highlighted slice across sigma
        sv = ValueTracker(-0.25)
        slice_m = always_redraw(lambda: weighted(sv.get_value(), color=YELLOW, width=7))
        plane_m = always_redraw(lambda: slice_plane(ax, sv.get_value()))
        num = DecimalNumber(-0.25, num_decimal_places=2, include_sign=True, font_size=42, color=YELLOW)
        row = VGroup(MathTex(r"\sigma =", font_size=42, color=YELLOW), num).arrange(RIGHT, buff=0.15).next_to(legend, DOWN, buff=0.35, aligned_edge=RIGHT)
        num.add_updater(lambda m: m.set_value(sv.get_value()).next_to(row[0], RIGHT, buff=0.15))
        self.hud(row, live=True)
        self.add(plane_m, slice_m)
        self.play(FadeIn(row))
        self.play(sv.animate.set_value(1.5), run_time=6, rate_func=linear)
        self.play(sv.animate.set_value(0.9), run_time=1.5)
        self.beat("sweep sigma: the weight wins once sigma > 0.5")

        # the convergent sigmas on the floor
        roc = Polygon(ax.c2p(0, A, 0), ax.c2p(T_MAX, A, 0), ax.c2p(T_MAX, 1.75, 0), ax.c2p(0, 1.75, 0),
                      stroke_width=0, fill_color=ROC_COLOR, fill_opacity=0.35)
        edge = DashedLine(ax.c2p(0, A, 0), ax.c2p(T_MAX, A, 0), color=BLUE_B, stroke_width=3, dash_length=0.12)
        tag_floor(VGroup(roc, edge))
        roc_lab = MathTex(r"\sigma > 0.5", font_size=40, color=BLUE_B).move_to(ax.c2p(T_MAX + 0.3, 1.2, 0))
        self.face_camera(roc_lab)
        self.play(FadeIn(roc), Create(edge), FadeIn(roc_lab))
        self.beat("these sigmas: the region of convergence")
        num.clear_updaters()
        self.play(*[FadeOut(m) for m in (slice_m, plane_m, row, legend)])
        self.remove(slice_m, plane_m)
        self.stack_bits = VGroup(t_axis, s_axis, t_lab, s_lab, s_ticks, stack, roc, edge, roc_lab)

    # ------------------------------------------------------------------
    def onto_the_s_plane(self):
        self.set_title(r"On the $s$-plane")
        self.play(FadeOut(self.stack_bits), run_time=1.0)
        ax = splane_axes(u_range=(-2, 2), v_range=(-3, 3), z_max=2, x_length=6, y_length=7, z_length=2)
        camera_at(self, ax.c2p(0, 0, 0), screen=(-2.4, -0.5), phi=55 * DEGREES, theta=-70 * DEGREES, zoom=0.9)
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        ticks = floor_ticks(ax, us=[-1, 1], vs=[-2, 2])
        self.play(FadeIn(floor), Create(ax.x_axis), Create(ax.y_axis), FadeIn(labs), FadeIn(ticks))
        roc = roc_floor(ax, left=A)
        self.play(FadeIn(roc))
        jw = floor_vline(ax, 0, color=YELLOW, width=5)
        jw_lab = Tex(r"$j\omega$-axis", font_size=32, color=YELLOW).move_to(ax.c2p(0.05, -3.5, 0))
        self.face_camera(jw_lab)
        info = VGroup(
            MathTex(r"X(s) = \frac{1}{s - 0.5}", font_size=48),
            MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} > 0.5", font_size=44, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.3).to_corner(UR, buff=0.5).shift(0.5 * DOWN)
        info = self.panel(info)
        self.play(FadeIn(info))
        self.beat("every omega works: a half-plane")
        note = self.panel(VGroup(
            Tex(r"$j\omega$-axis not in the ROC:", font_size=36, color=YELLOW),
            Tex(r"no Fourier transform,", font_size=36),
            Tex(r"but the Laplace transform exists", font_size=36, color=GOOD),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12).next_to(info, DOWN, buff=0.4, aligned_edge=RIGHT))
        self.play(Create(jw), FadeIn(jw_lab), FadeIn(note))
        self.beat("Fourier = the j omega-axis, which is outside here")
        self.move_camera(theta=-35 * DEGREES, run_time=3)
        self.wait(0.5)


def real_curve_y(ax, f, y, color, width=4, opacity=1.0, n=300):
    """Graph of f(t) drawn at depth y (a slice of the weighting stack)."""
    t0, t1 = ax.x_range[:2]
    zmax = ax.z_range[1]
    ts = np.linspace(t0, t1, n)
    with np.errstate(all="ignore"):
        zs = np.asarray(f(ts), dtype=float)
    mask = np.isfinite(zs) & (zs <= zmax)
    g = VGroup()
    for run in true_runs(mask):
        g.add(polyline(pts(ax, ts[run], y, np.clip(zs[run], 0, zmax)), color, width, opacity))
    return g


def slice_plane(ax, sigma, color=YELLOW, opacity=0.08):
    t0, t1 = ax.x_range[:2]
    zmax = ax.z_range[1]
    return Polygon(ax.c2p(t0, sigma, 0), ax.c2p(t1, sigma, 0), ax.c2p(t1, sigma, zmax), ax.c2p(t0, sigma, zmax),
                   stroke_color=color, stroke_width=1, stroke_opacity=0.4, fill_color=color, fill_opacity=opacity)
