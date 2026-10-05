"""ROC properties 1-5.

Scene: ROCProperties
  * P1  |x(t) e^{-st}| = |x(t)| e^{-sigma t}: omega only spins, never resizes,
        so whole vertical lines converge together - the ROC is vertical strips
  * P2  no poles inside the ROC (X is infinite there)
  * P3  finite duration (Example 9.6): the ROC is the whole plane; the apparent
        pole at s = -a cancels, the landscape has zeros instead of a spike
  * P4/P5  the weight surface e^{-sigma t}: for t > 0 it only shrinks as sigma
        grows (right-sided -> ROC extends right); for t < 0 it shrinks as sigma
        decreases (left-sided -> ROC extends left)
"""
from common3d import *

A = 1.0


class ROCProperties(LScene):
    def construct(self):
        self.p1_strips()
        self.p2_no_poles()
        self.p3_finite()
        self.p45_sided()
        self.clear_all()

    # ------------------------------------------------------------------
    def p1_strips(self):
        T_MAX, R = 6.0, 1.3
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=R, t_length=8, r_length=3.0)
        camera_at(self, ax.c2p(T_MAX / 2, 0, 0), screen=(0.2, -0.9), phi=68 * DEGREES, theta=-38 * DEGREES, zoom=0.92)
        self.set_title("Property 1: vertical strips")
        labs = ct_labels(ax)
        self.face_camera(*labs)
        sig = -0.6
        eq = self.panel(VGroup(
            MathTex(r"\big|x(t)\,e^{-(\sigma + j\omega)t}\big| = |x(t)|\,e^{-\sigma t}", font_size=42),
            MathTex(r"\text{since } |e^{-j\omega t}| = 1", font_size=34, color=GREY_A),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.4))
        self.play(Create(ax), FadeIn(labs), FadeIn(eq))

        def integrand(w):
            return lambda t: np.exp(-(complex(sig, w) + A) * t)

        s1 = complex_curve(ax, integrand(1.5), 0, T_MAX, n=500, rmax=R, color=SIG, width=4)
        s2 = complex_curve(ax, integrand(4.0), 0, T_MAX, n=700, rmax=R, color=PURPLE_B, width=4)
        env = envelope(ax, -(sig + A), T_MAX, R, color=GREY_B)
        l1 = self.hud(MathTex(r"s = -0.6 + 1.5j", font_size=34, color=SIG))
        l2 = self.hud(MathTex(r"s = -0.6 + 4j", font_size=34, color=PURPLE_B))
        VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.5).shift(3.4 * RIGHT)
        sig_note = self.hud(Tex(r"$x(t) = e^{-t}u(t)$", font_size=34, color=GREY_A).next_to(VGroup(l1, l2), UP, buff=0.2, aligned_edge=LEFT))
        self.play(FadeIn(sig_note), Create(s1), FadeIn(l1), run_time=2)
        self.play(Create(s2), FadeIn(l2), run_time=2)
        self.play(FadeIn(env))
        self.beat("different omega, same envelope")

        sp = MiniSPlane(x_range=(-3, 1, 1), y_range=(-3, 3, 1), width=2.5, height=3.2, size=20).to_corner(DL, buff=0.35)
        dots = VGroup(*[Dot(sp.c2p(sig, w), radius=0.06, color=YELLOW) for w in np.arange(-2.5, 2.6, 0.5)])
        line = sp.vline(sig, color=YELLOW, width=3)
        strip = sp.region(left=-A)
        self.hud(sp, dots, line, strip)
        self.play(FadeIn(sp), LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.08))
        self.play(Create(line))
        self.beat("a whole vertical line converges together")
        self.play(FadeIn(strip), FadeOut(dots))
        self.beat("so the ROC is a union of vertical lines")
        self.clear_all()

    # ------------------------------------------------------------------
    def p2_no_poles(self):
        self.set_title("Property 2: no poles inside the ROC")
        sp = MiniSPlane(x_range=(-3, 2, 1), y_range=(-2, 2, 1), width=4.6, height=3.7, size=24).shift(3.2 * LEFT + 0.3 * DOWN)
        roc = sp.region(left=-A)
        pole = sp.pole(-A, size=0.14, width=6)
        lab = MathTex(r"X(s) = \infty", font_size=36, color=POLE_COLOR).next_to(pole, UL, buff=0.1)
        note = VGroup(
            Tex(r"at a pole $X(s) = \infty$,", font_size=40),
            Tex(r"so the integral cannot", font_size=40),
            Tex(r"converge there", font_size=40),
            Tex(r"$\Rightarrow$ poles sit on ROC edges,", font_size=38, color=BLUE_B),
            Tex(r"never inside", font_size=38, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(sp, RIGHT, buff=0.7)
        self.hud(sp, roc, pole, lab, note)
        self.play(FadeIn(sp), FadeIn(roc), FadeIn(pole, scale=2), FadeIn(lab))
        self.play(FadeIn(note[:3]))
        self.play(FadeIn(note[3:]))
        self.beat("poles bound the ROC")
        self.play(*[FadeOut(m) for m in (sp, roc, pole, lab, note)])

    # ------------------------------------------------------------------
    def p3_finite(self):
        T = 2.0
        ax = splane_axes(u_range=(-3, 2), v_range=(-4, 4), z_max=3.5, x_length=5.5, y_length=8, z_length=3.0)
        camera_at(self, ax.c2p(-0.5, 0, 0.6), screen=(-2.0, -0.6), phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.74)
        self.set_title("Property 3: finite duration $\\Rightarrow$ the whole plane")
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        info = self.panel(VGroup(
            Tex(r"Example 9.6", font_size=32, color=GREY_A),
            MathTex(r"x(t) = e^{-t}\ \text{ for } 0 < t < 2", font_size=40),
            MathTex(r"X(s) = \frac{1 - e^{-(s+1)\,2}}{s+1}", font_size=44),
            MathTex(r"\mathrm{ROC}: \text{ every } s", font_size=40, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.18).to_corner(UR, buff=0.4))

        def X96(s):
            if abs(s + A) < 1e-6:
                return T
            return (1 - np.exp(-(s + A) * T)) / (s + A)

        roc = roc_floor(ax)
        self.play(FadeIn(floor), Create(ax.x_axis), Create(ax.y_axis), FadeIn(labs), FadeIn(info), FadeIn(roc))
        surf = landscape(ax, X96, res=(40, 56))
        surf.save_state()
        surf.stretch(0.001, 2, about_point=ax.c2p(0, 0, 0))
        self.add(surf)
        self.play(Restore(surf), run_time=2.5)
        gp = ax.c2p(-A, 0, 0)
        ghost_pole = VGroup(DashedLine(gp + 0.2 * (UP + LEFT), gp + 0.2 * (DOWN + RIGHT), dash_length=0.06),
                            DashedLine(gp + 0.2 * (UP + RIGHT), gp + 0.2 * (DOWN + LEFT), dash_length=0.06)).set_stroke(GREY_B, 4)
        top = Dot3D(ax.c2p(-A, 0, T), radius=0.08, color=YELLOW)
        gp_lab = self.panel(MathTex(r"s = -1:\ \ \tfrac{0}{0} \to 2 \quad \text{(height 2, not } \infty)", font_size=38, color=YELLOW)
                            .to_edge(DOWN, buff=0.4))
        self.play(FadeIn(ghost_pole), FadeIn(top, scale=2), FadeIn(gp_lab))
        self.beat("no spike at s = -1: the pole cancels")
        zeros = VGroup(zero_o(ax, complex(-A, np.pi)), zero_o(ax, complex(-A, -np.pi)))
        z_note = self.panel(Tex(r"zeros where $e^{-(s+1)2} = 1$: $\ s = -1 \pm j\pi, \dots$", font_size=34, color=ZERO_COLOR)
                            .to_edge(DOWN, buff=0.35))
        self.play(FadeIn(zeros), FadeOut(gp_lab), FadeIn(z_note))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.beat("finite everywhere: big on the left, but never infinite")
        self.clear_all()

    # ------------------------------------------------------------------
    def p45_sided(self):
        ZM = 4.5
        ax = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-0.5, 0.5, 0.5], z_range=[0, ZM, 1], x_length=8, y_length=5, z_length=3,
                        axis_config={"stroke_color": AXIS_COLOR, "include_tip": False, "stroke_width": 2, "tick_size": 0.05})
        camera_at(self, ax.c2p(0, 0, 0.8), screen=(-1.2, -0.7), phi=64 * DEGREES, theta=-62 * DEGREES, zoom=0.82)
        self.set_title(r"Properties 4 \& 5: the weight $e^{-\sigma t}$")
        t_lab = MathTex("t", font_size=36, color=LABEL_COLOR).move_to(ax.c2p(3.35, -0.5, 0))
        s_lab = MathTex(r"\sigma", font_size=40, color=RED_B).move_to(ax.c2p(-3.3, 0.6, 0))
        self.face_camera(t_lab, s_lab)
        t_axis = Line(ax.c2p(-3, -0.5, 0), ax.c2p(3, -0.5, 0), color=AXIS_COLOR, stroke_width=2)
        s_axis = Line(ax.c2p(-3, -0.5, 0), ax.c2p(-3, 0.5, 0), color=RED_B, stroke_width=3)
        zero_line = DashedLine(ax.c2p(0, -0.5, 0), ax.c2p(0, 0.5, 0), color=GREY_B, stroke_width=2, dash_length=0.1)

        def wsurf(t_lo=-3, t_hi=3, opacity=0.85):
            s = Surface(lambda u, v: ax.c2p(u, v, min(np.exp(-v * u), ZM)), u_range=[t_lo, t_hi], v_range=[-0.5, 0.5],
                        resolution=(36, 16), fill_opacity=opacity, stroke_width=0.3, stroke_color=BLUE_E, checkerboard_colors=False)
            s.set_fill_by_value(axes=ax, colorscale=HEIGHT_SCALE, axis=2)
            return s

        surf = wsurf()
        self.play(Create(t_axis), Create(s_axis), FadeIn(t_lab), FadeIn(s_lab), Create(zero_line))
        self.play(FadeIn(surf), run_time=2)
        self.beat("the weight e^{-sigma t} over (t, sigma)", hold=1.0)

        sp = MiniSPlane(x_range=(-2, 2, 1), y_range=(-2, 2, 1), width=2.6, height=2.6, size=20).to_corner(DR, buff=0.4)
        self.hud(sp)
        self.play(FadeIn(sp))

        def slice_curve(sigma, t_lo, t_hi, color):
            ts = np.linspace(t_lo, t_hi, 200)
            zs = np.minimum(np.exp(-sigma * ts), ZM)
            return polyline(pts(ax, ts, sigma, zs + 0.02), color, 6)

        for right in (True, False):
            lo, hi = (0, 3) if right else (-3, 0)
            s0, s1 = (-0.2, 0.4) if right else (0.2, -0.4)
            lit = wsurf(lo, hi, 0.9)
            title = (r"right-sided: only $t > 0$ matters" if right else r"left-sided: only $t < 0$ matters")
            note = self.panel(VGroup(
                Tex(title, font_size=38, color=YELLOW),
                MathTex((r"\sigma_1 > \sigma_0 \Rightarrow e^{-\sigma_1 t} \le e^{-\sigma_0 t}\ \ (t > 0)" if right
                         else r"\sigma_1 < \sigma_0 \Rightarrow e^{-\sigma_1 t} \le e^{-\sigma_0 t}\ \ (t < 0)"), font_size=36),
            ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.4).shift(0.5 * DOWN))
            self.play(surf.animate.set_fill(opacity=0.12).set_stroke(opacity=0.1), FadeIn(lit), FadeIn(note))
            c0 = slice_curve(s0, lo, hi, GREY_A)
            c1 = slice_curve(s1, lo, hi, GOOD)
            l0 = MathTex(r"\sigma_0", font_size=34, color=GREY_A).move_to(ax.c2p(hi if right else lo, s0, 0.15) + (0.35 * RIGHT if right else 0.35 * LEFT))
            l1 = MathTex(r"\sigma_1", font_size=34, color=GOOD).move_to(ax.c2p(hi if right else lo, s1, 0.15) + (0.35 * RIGHT if right else 0.35 * LEFT))
            self.face_camera(l0, l1)
            self.play(Create(c0), FadeIn(l0))
            self.play(Create(c1), FadeIn(l1))
            region = sp.region(left=s0) if right else sp.region(right=s0)
            self.hud(region)
            self.play(FadeIn(region))
            self.beat(("right-sided: ROC extends to the right" if right else "left-sided: ROC extends to the left"))
            self.play(*[FadeOut(m) for m in (lit, note, c0, c1, l0, l1, region)], surf.animate.set_fill(opacity=0.85).set_stroke(opacity=1))
