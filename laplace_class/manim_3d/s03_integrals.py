"""Background 3 - integrals, improper integrals and convergence.

Scene: IntegralsConverge
  * an integral is accumulated area; to infinity it may settle (converge) or not
  * integrating the spiral e^{-st}: the running total is a path whose velocity is
    the integrand; it spirals into 1/s when Re{s} > 0
  * Re{s} <= 0: the path never settles
  * only sigma matters, because |e^{-st}| = e^{-sigma t}
"""
from common3d import *

T_MAX = 8.0


class IntegralsConverge(LScene):
    def construct(self):
        self.area_part()
        self.spiral_part()
        self.clear_all()

    # ------------------------------------------------------------------
    def area_part(self):
        ax = ThreeDAxes(x_range=[0, T_MAX, 1], y_range=[-0.4, 2.6, 1], z_range=[-1, 1, 1], x_length=9, y_length=4.2, z_length=2,
                        axis_config={"stroke_color": AXIS_COLOR, "include_tip": False, "stroke_width": 2, "tick_size": 0.05})
        camera_at(self, ax.c2p(T_MAX / 2, 1.1, 0), screen=(-0.6, -0.7), phi=0, theta=-90 * DEGREES, zoom=1.08)
        t_lab = MathTex("t", font_size=36, color=LABEL_COLOR).move_to(ax.c2p(T_MAX + 0.35, 0, 0))
        self.face_camera(t_lab)
        self.set_title("Integrals: accumulated area")
        self.play(Create(ax.x_axis), Create(ax.y_axis), FadeIn(t_lab))

        T = ValueTracker(0.0)
        rate = ValueTracker(-1.0)       # f(t) = e^{rate t}

        def f(t):
            return np.exp(rate.get_value() * t)

        def area():
            tt = max(T.get_value(), 1e-3)
            ts = np.linspace(0, tt, 120)
            ys = np.minimum(f(ts), 2.6)
            top = pts(ax, ts, ys, 0)
            poly = Polygon(ax.c2p(0, 0, 0), *top, ax.c2p(tt, 0, 0), stroke_width=0, fill_color=YELLOW, fill_opacity=0.3)
            return poly

        graph = always_redraw(lambda: real_curve(ax, f, 0, T_MAX, n=300, ylim=(-0.4, 2.6), color=SIG, width=5, plane="xy"))
        shade = always_redraw(area)

        def total(tt):
            r = rate.get_value()
            return (np.exp(r * tt) - 1) / r

        value = DecimalNumber(0, num_decimal_places=3, font_size=44, color=YELLOW)
        lhs = MathTex(r"\int_0^{T} f(t)\,dt =", font_size=44)
        row = VGroup(lhs, value).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.5)
        value.add_updater(lambda m: m.set_value(total(T.get_value())).next_to(lhs, RIGHT, buff=0.2))
        self.hud(row, live=True)

        f_lab = MathTex(r"f(t) = e^{-t}", font_size=40, color=SIG).move_to(ax.c2p(1.7, 1.3, 0))
        self.face_camera(f_lab)
        self.play(Create(graph), FadeIn(f_lab), run_time=1.5)
        self.add(graph, shade)
        self.play(FadeIn(row))
        self.play(T.animate.set_value(T_MAX), run_time=5, rate_func=rate_functions.ease_out_sine)
        limit = self.panel(MathTex(r"\int_0^{\infty} e^{-t}\,dt = 1", font_size=44, color=GOOD).next_to(row, DOWN, buff=0.35, aligned_edge=RIGHT))
        conv = self.panel(Tex("converges", font_size=40, color=GOOD).next_to(limit, DOWN, buff=0.25, aligned_edge=RIGHT))
        self.play(FadeIn(limit), FadeIn(conv))
        self.beat("to infinity: the area settles at 1")

        f_lab2 = MathTex(r"f(t) = e^{0.12t}", font_size=40, color=SIG).move_to(ax.c2p(1.7, 2.1, 0))
        self.face_camera(f_lab2)
        self.play(FadeOut(limit), FadeOut(conv), T.animate.set_value(0), run_time=1)
        self.play(rate.animate.set_value(0.12), FadeTransform(f_lab, f_lab2), run_time=1.5)
        self.play(T.animate.set_value(T_MAX), run_time=5, rate_func=linear)
        div = self.panel(Tex("keeps growing: diverges", font_size=40, color=BAD).next_to(row, DOWN, buff=0.35, aligned_edge=RIGHT))
        self.play(FadeIn(div))
        self.beat("a growing integrand: diverges")
        value.clear_updaters()
        self.play(*[FadeOut(m) for m in (graph, shade, f_lab2, row, div, ax.x_axis, ax.y_axis, t_lab)])
        self.remove(graph, shade)

    # ------------------------------------------------------------------
    def spiral_part(self):
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=1.2, t_length=8, r_length=2.6)
        self.set_title(r"Integrating a spiral: $\int_0^{\infty} e^{-st}\,dt$")
        camera_at(self, ax.c2p(T_MAX / 2, 0, 0), screen=(-3.3, -0.5), phi=68 * DEGREES, theta=-38 * DEGREES, zoom=1.1)
        labs = ct_labels(ax)
        self.face_camera(*labs)
        sig = ValueTracker(0.35)
        om = ValueTracker(1.5)
        T = ValueTracker(0.0)

        def s():
            return complex(sig.get_value(), om.get_value())

        def g(t):
            return np.exp(-s() * t)

        def P(t):
            return (1 - np.exp(-s() * t)) / s()

        self.play(Create(ax), FadeIn(labs))
        spiral = always_redraw(lambda: complex_curve(ax, g, 0, T_MAX, n=500, rmax=1.2, color=SIG, width=4))
        g_lab = MathTex(r"e^{-st}", font_size=40, color=SIG).move_to(ax.c2p(2.2, 0, 1.45))
        self.face_camera(g_lab)
        self.play(Create(spiral), FadeIn(g_lab), run_time=2)
        self.add(spiral)

        # flat complex plane for the running total (overlay on the right)
        plane = NumberPlane(
            x_range=(-1.5, 1.5, 0.5), y_range=(-2.0, 1.0, 0.5), x_length=4.2, y_length=4.2,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.3},
            faded_line_ratio=1, axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).to_edge(RIGHT, buff=0.45).shift(0.55 * DOWN)
        p_bg = BackgroundRectangle(plane, fill_color=PANEL_BG, fill_opacity=0.9, buff=0.1)
        p_title = MathTex(r"\text{running total } \int_0^{T} e^{-st}\,dt", font_size=32).next_to(plane, UP, buff=0.12)
        re_l = MathTex(r"\mathrm{Re}", font_size=26, color=RE_COLOR).next_to(plane.c2p(1.5, 0), UP, buff=0.06).shift(0.2 * LEFT)
        im_l = MathTex(r"\mathrm{Im}", font_size=26, color=IM_COLOR).next_to(plane.c2p(0, 1.0), RIGHT, buff=0.08).shift(0.15 * DOWN)
        panel = VGroup(p_bg, plane, p_title, re_l, im_l)
        self.hud(panel)
        self.play(FadeIn(panel))

        def pz(z):
            return plane.c2p(z.real, z.imag)

        def path():
            tt = max(T.get_value(), 1e-3)
            ts = np.linspace(0, tt, max(int(80 * tt), 4))
            zs = P(ts)
            inside = (np.abs(zs.real) <= 1.5) & (zs.imag >= -2.0) & (zs.imag <= 1.0)
            g_ = VGroup()
            for run in true_runs(inside):
                g_.add(polyline([pz(z) for z in zs[run]], YELLOW, 4))
            return g_

        def pen():
            tt = T.get_value()
            p = P(tt)
            v = 0.5 * g(tt)
            if abs(p.real) > 1.5 or not (-2.0 <= p.imag <= 1.0):
                return VGroup()
            grp = VGroup(Dot(pz(p), radius=0.06, color=YELLOW))
            if abs(v) > 0.02:
                grp.add(Arrow(pz(p), pz(p + v), buff=0, color=SIG, stroke_width=4, max_tip_length_to_length_ratio=0.3))
            return grp

        def integrand_arrow():
            tt = T.get_value()
            w = g(tt)
            if abs(w) > 1.2:
                return VGroup()
            return cplane_arrow(ax, w, t=tt, color=SIG, width=4, tip=0.16)

        path_m = always_redraw(path)
        pen_m = always_redraw(pen)
        arr3d = always_redraw(integrand_arrow)
        self.hud(path_m, pen_m, live=True)
        self.add(path_m, pen_m, arr3d)
        self.beat("the integrand: a shrinking spiral", hold=1.0)
        self.play(T.animate.set_value(T_MAX), run_time=8, rate_func=linear)
        target = Dot(pz(1 / s()), radius=0.07, color=GOOD)
        t_lab = MathTex(r"\tfrac{1}{s}", font_size=34, color=GOOD).next_to(target, LEFT, buff=0.1)
        self.hud(target, t_lab)
        self.play(FadeIn(target, scale=2), FadeIn(t_lab))
        result = self.panel(MathTex(r"\int_0^{\infty} e^{-st}\,dt = \frac{1}{s}", font_size=42, color=GOOD).next_to(p_title, UP, buff=0.25))
        self.play(FadeIn(result))
        self.beat("the running total settles at 1/s")

        # move s: the target follows, until sigma <= 0
        target.add_updater(lambda m: m.move_to(pz(1 / s())))
        t_lab.add_updater(lambda m: m.next_to(target, LEFT, buff=0.1))
        self.play(om.animate.set_value(2.6), run_time=2.5)
        self.play(om.animate.set_value(1.5), run_time=1.5)
        self.beat("different omega: still settles", hold=1.0)
        cond = self.panel(MathTex(r"\mathrm{Re}\{s\} > 0", font_size=42, color=GOOD).next_to(result, LEFT, buff=0.5))
        self.play(FadeIn(cond))
        self.play(sig.animate.set_value(0.0), run_time=3)
        self.beat("sigma = 0: circles forever")
        self.play(sig.animate.set_value(-0.06), run_time=2)
        never = self.panel(Tex("never settles", font_size=40, color=BAD).move_to(cond))
        self.play(FadeOut(cond), FadeIn(never), result.animate.set_opacity(0.3))
        self.beat("sigma < 0: spirals out, diverges")

        # only sigma matters
        mag = self.panel(MathTex(r"|e^{-st}| = e^{-\sigma t}", font_size=46, color=YELLOW).to_corner(DL, buff=0.5))
        self.play(FadeIn(mag), FadeOut(never), result.animate.set_opacity(1), sig.animate.set_value(0.35), run_time=2)
        self.beat("the size depends only on sigma")
        for m in (target, t_lab):
            m.clear_updaters()
        self.play(FadeOut(mag), FadeOut(result), FadeOut(g_lab), run_time=0.6)
