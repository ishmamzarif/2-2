"""Inverse Laplace in practice - partial fractions and the ROC (Examples 9.9-9.11).

Scene: PartialFractions
  * 1/((s+1)(s+2)) = 1/(s+1) - 1/(s+2) by the cover-up method
  * the rule for one term A/(s+a): ROC to the right -> A e^{-at} u(t),
    ROC to the left -> -A e^{-at} u(-t)
  * on the landscape: each pole looks towards the ROC; that side decides whether
    its term lives in t > 0 or t < 0. Three ROCs, three signals.
"""
from common3d import *

C1 = TEAL_C      # term of the pole at -1
C2 = GOLD_C      # term of the pole at -2


def X(s):
    return 1 / ((s + 1) * (s + 2))


class PartialFractions(LScene):
    def construct(self):
        self.algebra()
        self.rule()
        self.three_cases()
        self.recipe()
        self.clear_all()

    # ------------------------------------------------------------------
    def algebra(self):
        self.set_title("Partial fractions")
        l1 = MathTex(r"X(s) = \frac{1}{(s+1)(s+2)}", r"=", r"\frac{A}{s+1}", r"+", r"\frac{B}{s+2}", font_size=54)
        l1[2].set_color(C1)
        l1[4].set_color(C2)
        l2 = MathTex(r"A = (s+1)X(s)\Big|_{s=-1} = \frac{1}{s+2}\Big|_{s=-1} = 1", font_size=44, color=C1)
        l3 = MathTex(r"B = (s+2)X(s)\Big|_{s=-2} = \frac{1}{s+1}\Big|_{s=-2} = -1", font_size=44, color=C2)
        l4 = MathTex(r"X(s) = ", r"\frac{1}{s+1}", r"-", r"\frac{1}{s+2}", font_size=58)
        l4[1].set_color(C1)
        l4[3].set_color(C2)
        g = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.45)
        self.hud(g)
        self.play(FadeIn(l1))
        self.beat("split into simple terms", hold=1.0)
        self.play(FadeIn(l2, shift=0.2 * DOWN))
        self.play(FadeIn(l3, shift=0.2 * DOWN))
        self.beat("cover-up: A = 1, B = -1")
        self.play(FadeIn(l4, shift=0.2 * DOWN))
        self.beat("the expansion is always the same")
        self.play(FadeOut(g))

    # ------------------------------------------------------------------
    def rule(self):
        self.set_title(r"One term, two possible inverses")
        cols = VGroup()
        for right in (True, False):
            sp = MiniSPlane(x_range=(-2, 1, 1), y_range=(-1.5, 1.5, 1), width=3.2, height=2.0, size=20)
            reg = sp.region(left=-1) if right else sp.region(right=-1)
            pole = sp.pole(-1)
            head = Tex(r"ROC to the right" if right else r"ROC to the left", font_size=36, color=BLUE_B)
            pair = MathTex(r"\frac{A}{s+a} \leftrightarrow A\,e^{-at}u(t)" if right else r"\frac{A}{s+a} \leftrightarrow -A\,e^{-at}u(-t)",
                           font_size=40)
            sax = mini_axes(x_range=(-3, 3, 1), y_range=(-1.4, 1.4, 1), width=3.6, height=1.6, x_label="t", size=24)
            gr = graph2d(sax, (lambda t: np.exp(-t) * (t >= 0)) if right else (lambda t: -np.exp(-t) * (t < 0)), -3, 3,
                         color=SIG, width=4, breaks=(0,))
            kind = Tex(r"right-sided (causal)" if right else r"left-sided (anticausal)", font_size=32, color=GREY_A)
            cols.add(VGroup(head, VGroup(sp, reg, pole), pair, VGroup(sax, gr), kind).arrange(DOWN, buff=0.25))
        cols.arrange(RIGHT, buff=1.4).shift(0.3 * DOWN)
        self.hud(cols)
        self.play(FadeIn(cols[0]))
        self.play(FadeIn(cols[1]))
        self.beat("which side of the pole is the ROC on?")
        self.play(FadeOut(cols))

    # ------------------------------------------------------------------
    def three_cases(self):
        ax = splane_axes(u_range=(-3.5, 1.5), v_range=(-3, 3), z_max=3.5, x_length=6, y_length=6, z_length=2.6)
        camera_at(self, ax.c2p(-1, 0, 0.3), screen=(-2.6, -0.4), phi=55 * DEGREES, theta=-70 * DEGREES, zoom=0.82)
        self.set_title(r"Examples 9.9 -- 9.11")
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        ticks = floor_ticks(ax, us=[-3, -2, -1, 1], vs=[-2, 2])
        surf = landscape(ax, X, res=(44, 44), opacity=0.75)
        p1 = pole_x(ax, -1, color=C1, width=7)
        p2 = pole_x(ax, -2, color=C2, width=7)
        self.play(FadeIn(floor), Create(ax.x_axis), Create(ax.y_axis), FadeIn(labs), FadeIn(ticks), FadeIn(surf), FadeIn(p1), FadeIn(p2),
                  run_time=2)

        sax = mini_axes(x_range=(-3, 3, 1), y_range=(-1.6, 1.6, 1), width=4.4, height=2.4, x_label="t", size=24)
        sax.to_corner(DR, buff=0.45)
        sbg = BackgroundRectangle(sax, fill_color=PANEL_BG, fill_opacity=0.88, buff=0.15)
        sbg.hud_layer = -1
        self.hud(sbg, sax)
        self.play(FadeIn(sbg), FadeIn(sax))

        def arrow_from(pole, right, color):
            d = 0.9 if right else -0.9
            return Arrow(ax.c2p(pole, -2.3, 0), ax.c2p(pole + d, -2.3, 0), buff=0, color=color, stroke_width=6,
                         max_tip_length_to_length_ratio=0.35)

        cases = [
            ("Example 9.9", (-1, None), r"\mathrm{Re}\{s\} > -1", (True, True),
             lambda t: np.exp(-t) * (t >= 0), lambda t: -np.exp(-2 * t) * (t >= 0),
             r"x(t) = \big(e^{-t} - e^{-2t}\big)u(t)"),
            ("Example 9.10", (None, -2), r"\mathrm{Re}\{s\} < -2", (False, False),
             lambda t: -np.exp(-t) * (t < 0), lambda t: np.exp(-2 * t) * (t < 0),
             r"x(t) = \big(-e^{-t} + e^{-2t}\big)u(-t)"),
            ("Example 9.11", (-2, -1), r"-2 < \mathrm{Re}\{s\} < -1", (False, True),
             lambda t: -np.exp(-t) * (t < 0), lambda t: -np.exp(-2 * t) * (t >= 0),
             r"x(t) = -e^{-t}u(-t) - e^{-2t}u(t)"),
        ]
        prev, prev_roc = [], None
        for name, roc_lr, roc_tex, (r1, r2), f1, f2, total in cases:
            roc = roc_floor(ax, left=roc_lr[0], right=roc_lr[1])
            a1 = tag_floor(arrow_from(-1, r1, C1))
            a2 = tag_floor(arrow_from(-2, r2, C2))
            g1 = graph2d(sax, f1, -3, 3, color=C1, width=3, breaks=(0,))
            g2 = graph2d(sax, f2, -3, 3, color=C2, width=3, breaks=(0,))
            gs = graph2d(sax, lambda t: f1(t) + f2(t), -3, 3, color=YELLOW, width=5, breaks=(0,))
            info = self.panel(VGroup(
                Tex(name, font_size=32, color=GREY_A),
                MathTex(r"\mathrm{ROC}:\ " + roc_tex, font_size=40, color=BLUE_B),
                MathTex(r"\tfrac{1}{s+1}:\ " + (r"e^{-t}u(t)" if r1 else r"-e^{-t}u(-t)"), font_size=38, color=C1),
                MathTex(r"-\tfrac{1}{s+2}:\ " + (r"-e^{-2t}u(t)" if r2 else r"e^{-2t}u(-t)"), font_size=38, color=C2),
                MathTex(total, font_size=38, color=YELLOW),
            ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.4))
            self.hud(g1, g2, gs)
            self.play(*[FadeOut(m) for m in prev], FadeIn(roc), roc_transition(surf, prev_roc, roc_lr, opacity=0.75),
                      FadeIn(info[0]), FadeIn(info[1][0]), FadeIn(info[1][1]), run_time=1.5)
            self.play(GrowArrow(a1), FadeIn(info[1][2]), Create(g1))
            self.play(GrowArrow(a2), FadeIn(info[1][3]), Create(g2))
            self.play(FadeIn(info[1][4]), Create(gs))
            self.beat(name + ": " + roc_tex.replace("\\mathrm{Re}\\{s\\}", "Re s"))
            prev, prev_roc = [roc, a1, a2, g1, g2, gs, info], roc_lr

    # ------------------------------------------------------------------
    def recipe(self):
        self.clear_all()
        self.set_title("The recipe")
        steps = VGroup(
            Tex(r"1.\ \ expand $X(s)$ in partial fractions $\sum \frac{A_i}{s + a_i}$", font_size=42),
            Tex(r"2.\ \ for each pole, see which side the ROC is on", font_size=42),
            Tex(r"3.\ \ right: $A_i\,e^{-a_i t}u(t)$ \quad left: $-A_i\,e^{-a_i t}u(-t)$", font_size=42, color=YELLOW),
            Tex(r"4.\ \ add the terms", font_size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        self.hud(steps)
        for st in steps:
            self.play(FadeIn(st, shift=0.2 * RIGHT), run_time=0.8)
        self.beat("partial fractions + ROC = inverse transform")
