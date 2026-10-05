"""Examples 9.1 and 9.2 - right-sided vs left-sided: same X(s), different ROC.

Scene: RightVsLeftSided
  * 9.1  x(t) = e^{-t} u(t): the integrand e^{-(s+1)t} lives on t > 0 and shrinks
         only when sigma > -1          ->  1/(s+1),  Re{s} > -1
  * 9.2  x(t) = -e^{-t} u(-t): the integrand lives on t < 0 and shrinks towards
         t -> -infinity only when sigma < -1   ->  1/(s+1),  Re{s} < -1
  * same formula, opposite regions: the ROC is part of the answer
"""
from common3d import *

A = 1.0
W = 2.0          # omega of the test point (just to make the integrand spin)
TR = 5.0
R = 1.5


class RightVsLeftSided(LScene):
    def construct(self):
        ax = complex_time_axes(t_range=(-TR, TR, 1), r=R, t_length=10, r_length=3.4)
        self.ax = ax
        camera_at(self, ax.c2p(0, 0, 0), screen=(0.6, -0.4), phi=70 * DEGREES, theta=-50 * DEGREES, zoom=0.78)
        labs = ct_labels(ax)
        self.face_camera(*labs)
        self.sig = ValueTracker(-0.4)
        self.inset()
        self.play(FadeIn(ax), FadeIn(labs), FadeIn(self.inset_group), FadeIn(self.dot), FadeIn(self.s_lab))
        self.example(right=True)
        self.example(right=False)
        self.compare()
        self.clear_all()

    # ------------------------------------------------------------------
    def inset(self):
        sp = MiniSPlane(x_range=(-3, 1, 1), y_range=(-3, 3, 1), width=2.6, height=3.4, size=20).to_corner(DL, buff=0.35)
        pole = sp.pole(-A)
        edge = DashedLine(sp.c2p(-A, -3), sp.c2p(-A, 3), color=GREY_B, stroke_width=2, dash_length=0.08)
        dot = Dot(sp.c2p(self.sig.get_value(), W), radius=0.08, color=YELLOW)
        dot.add_updater(lambda m: m.move_to(sp.c2p(self.sig.get_value(), W)))
        lab = MathTex("s", font_size=28, color=YELLOW)
        lab.add_updater(lambda m: m.next_to(dot, UR, buff=0.03))
        title = Tex(r"$s$-plane", font_size=28, color=GREY_A).next_to(sp, UP, buff=0.1)
        self.hud(sp, pole, edge, dot, lab, title)
        self.sp, self.dot, self.s_lab = sp, dot, lab
        self.inset_group = VGroup(sp, pole, edge, title)

    def verdict(self, right):
        ok = (self.sig.get_value() > -A) if right else (self.sig.get_value() < -A)
        t = Tex("converges" if ok else "diverges", font_size=40, color=GOOD if ok else BAD)
        return t

    # ------------------------------------------------------------------
    def example(self, right):
        ax, sig, sp = self.ax, self.sig, self.sp
        sign = 1.0 if right else -1.0
        t0, t1 = (0.0, TR) if right else (-TR, 0.0)
        if right:
            self.set_title(r"Example 9.1: right-sided $x(t) = e^{-t}u(t)$")
        else:
            self.set_title(r"Example 9.2: left-sided $x(t) = -e^{-t}u(-t)$")

        # the signal itself, as a small flat plot
        sax = mini_axes(x_range=(-3, 3, 1), y_range=(-1.3, 1.3, 1), width=3.6, height=1.7, x_label="t", y_label="x(t)", size=24)
        sax.to_corner(UR, buff=0.4).shift(0.55 * DOWN)
        sbg = BackgroundRectangle(sax, fill_color=PANEL_BG, fill_opacity=0.85, buff=0.12)
        sbg.hud_layer = -1
        sgraph = graph2d(sax, (lambda t: np.exp(-A * t) * (t >= 0)) if right else (lambda t: -np.exp(-A * t) * (t < 0)),
                         -3, 3, color=SIG, width=4, breaks=(0,))
        self.hud(sbg, sax, sgraph)
        self.play(FadeIn(sbg), FadeIn(sax), Create(sgraph))

        def f(t):
            s = complex(sig.get_value(), W)
            return sign * np.exp(-(s + A) * t)

        if not right:
            self.play(sig.animate.set_value(-1.6), run_time=1)
        spiral = always_redraw(lambda: complex_curve(ax, f, t0, t1, n=500, rmax=R, color=YELLOW, width=4))
        env = always_redraw(lambda: envelope(ax, -(sig.get_value() + A), t1, R, color=GREY_B, t_min=t0))
        integrand = self.hud(MathTex(r"x(t)\,e^{-st} = " + (r"e^{-(s+1)t}" if right else r"-e^{-(s+1)t}"),
                                     font_size=40, color=YELLOW).move_to([0.6, 2.85, 0]))
        verdict = always_redraw(lambda: self.verdict(right).next_to(self.sp, RIGHT, buff=0.35).align_to(self.sp, DOWN))
        self.hud(verdict, live=True)
        self.play(Create(spiral), FadeIn(env), FadeIn(integrand), run_time=2)
        self.add(spiral, env)
        self.play(FadeIn(verdict))
        self.add(verdict)
        self.beat("the integrand spiral" + (" for t > 0" if right else " for t < 0"), hold=1.0)

        path = [-0.7, -1.0, -1.35, -0.4] if right else [-1.3, -1.0, -0.65, -1.6]
        for i, v in enumerate(path):
            self.play(sig.animate.set_value(v), run_time=2.5)
            self.wait(0.5)
            if i == 2:
                self.beat("across sigma = -1 it " + ("diverges" if right else "diverges"), hold=1.0)

        roc = sp.region(left=-A) if right else sp.region(right=-A)
        self.hud(roc)
        self.play(FadeIn(roc))
        self.remove(self.dot, self.s_lab)
        self.add(self.dot, self.s_lab)
        result = VGroup(
            MathTex(r"X(s) = \frac{1}{s+1}", font_size=46),
            MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} " + (">" if right else "<") + r" -1", font_size=42, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(sax, DOWN, buff=0.35, aligned_edge=RIGHT)
        result = self.panel(result)
        self.play(FadeIn(result))
        self.beat("Example 9." + ("1" if right else "2") + ": 1/(s+1), ROC " + ("right" if right else "left") + " of -1")
        self.play(*[FadeOut(m) for m in (spiral, env, integrand, verdict, sgraph, sax, sbg, result, roc)])
        self.remove(spiral, env, verdict)

    # ------------------------------------------------------------------
    def compare(self):
        self.set_title("Same formula, different signals")
        for m in self.mobjects:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._title], run_time=1)
        mid = MathTex(r"X(s) = \frac{1}{s+1}", font_size=52, color=YELLOW).to_edge(UP, buff=0.85)
        cols = VGroup()
        for right in (True, False):
            sp = MiniSPlane(x_range=(-3, 1, 1), y_range=(-2, 2, 1), width=3.0, height=2.1, size=20)
            reg = sp.region(left=-A) if right else sp.region(right=-A)
            pole = sp.pole(-A)
            sax = mini_axes(x_range=(-3, 3, 1), y_range=(-1.3, 1.3, 1), width=3.6, height=1.5, x_label="t", size=24)
            g = graph2d(sax, (lambda t: np.exp(-A * t) * (t >= 0)) if right else (lambda t: -np.exp(-A * t) * (t < 0)),
                        -3, 3, color=SIG, width=4, breaks=(0,))
            sig_tex = MathTex(r"e^{-t}u(t)" if right else r"-e^{-t}u(-t)", font_size=40, color=SIG)
            roc_tex = MathTex(r"\mathrm{Re}\{s\} > -1" if right else r"\mathrm{Re}\{s\} < -1", font_size=36, color=BLUE_B)
            col = VGroup(VGroup(sp, reg, pole), roc_tex, VGroup(sax, g), sig_tex).arrange(DOWN, buff=0.22)
            cols.add(col)
        cols.arrange(RIGHT, buff=1.8).next_to(mid, DOWN, buff=0.35)
        self.hud(cols, mid)
        self.play(FadeIn(mid))
        self.play(FadeIn(cols[0]), FadeIn(cols[1]))
        self.beat("the ROC decides which signal you meant")
