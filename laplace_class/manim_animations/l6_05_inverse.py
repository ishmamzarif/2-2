"""Lecture 6 - The inverse Laplace transform.

Scenes:
  InverseLaplaceBuildUp   derive x(t) = 1/(2 pi j) \\int X(s) e^{st} ds, then literally add up the
                          e^{st} along the Bromwich line and watch x(t) = e^{-t}u(t) appear.
                          Sliding the line across the pole flips the answer to -e^{-t}u(-t).
                          Finally: closing the contour and the residue theorem.
  PartialFractionsAndROC  Examples 9.8 - 9.11: 1/((s+1)(s+2)) = 1/(s+1) - 1/(s+2), and the three
                          possible ROCs give three different time signals.
"""
from common import *

T_GRID = np.linspace(-2, 4, 361)
DW = 0.02


def reconstruct(sigma, W):
    """(1/2pi) \\int_{-W}^{W} X(sigma + j w) e^{(sigma + j w) t} dw  for X(s) = 1/(s+1)."""
    if W < 1e-3:
        return np.zeros_like(T_GRID)
    n = max(int(W / DW), 1)
    w = (np.arange(n) + 0.5) * (W / n)
    Xv = 1.0 / (sigma + 1 + 1j * w)
    E = np.exp(np.outer(T_GRID, sigma + 1j * w))
    # conjugate symmetry: the -w half is the complex conjugate of the +w half
    return (E @ Xv).real * (W / n) / np.pi


class InverseLaplaceBuildUp(Scene):
    def construct(self):
        self.derivation()
        self.build_up()

    # ------------------------------------------------------------------
    def derivation(self):
        title = make_title("Running the Laplace transform backwards")
        lines = VGroup(
            MathTex(r"X(\sigma + j\omega)", r"=", r"\mathcal{F}\{x(t)\,e^{-\sigma t}\}"),
            MathTex(r"x(t)\,e^{-\sigma t}", r"=", r"\frac{1}{2\pi}\int_{-\infty}^{\infty} X(\sigma + j\omega)\,e^{j\omega t}\,d\omega"),
            MathTex(r"x(t)", r"=", r"\frac{1}{2\pi}\int_{-\infty}^{\infty} X(\sigma + j\omega)\,e^{(\sigma + j\omega)t}\,d\omega"),
            MathTex(r"x(t)", r"=", r"\frac{1}{2\pi j}\int_{\sigma - j\infty}^{\sigma + j\infty} X(s)\,e^{st}\,ds"),
        )
        for l in lines:
            l.scale(0.85)
        lines.arrange(DOWN, buff=0.45).next_to(title, DOWN, buff=0.45)
        for l in lines[1:]:
            l.align_to(lines[0], LEFT).shift(RIGHT * (lines[0][1].get_x() - l[1].get_x()))
        notes = VGroup(
            Tex("Laplace = Fourier of the tamed signal", font_size=28, color=GREY_A),
            Tex("inverse Fourier transform", font_size=28, color=GREY_A),
            Tex(r"multiply by $e^{\sigma t}$", font_size=28, color=GREY_A),
            Tex(r"$s = \sigma + j\omega,\ ds = j\,d\omega$", font_size=28, color=GREY_A),
        )
        for n, l in zip(notes, lines):
            n.next_to(l, RIGHT, buff=0.5)
        group = VGroup(lines, notes)
        if group.width > 13.4:
            group.scale(13.4 / group.width)
        group.set_x(0)
        self.play(Write(title))
        for l, n in zip(lines, notes):
            self.play(Write(l), FadeIn(n, shift=LEFT * 0.2), run_time=1.6)
            self.wait(0.4)
        box = SurroundingRectangle(lines[3], color=YELLOW, buff=0.15)
        brom = Tex(r"Bromwich integral: add up $e^{st}$ along a vertical line \emph{inside the ROC}", font_size=32, color=YELLOW)
        brom.next_to(box, DOWN, buff=0.3).set_x(0)
        self.play(Create(box), FadeIn(brom))
        self.wait(2)
        self.formula = lines[3]
        self.play(FadeOut(VGroup(title, lines[:3], notes, box, brom)))
        self.play(self.formula.animate.scale(0.9).to_edge(UP, buff=0.25))

    # ------------------------------------------------------------------
    def build_up(self):
        sigma = ValueTracker(0.3)
        W = ValueTracker(0.0)

        sp = SPlane(x_range=(-3, 2, 1), y_range=(-4, 4, 2), x_length=3.6, y_length=5.2, number_size=18)
        sp.move_to(LEFT * 4.9 + DOWN * 0.6)
        pole = sp.pole(-1)
        Xs = MathTex(r"X(s) = \frac{1}{s+1}", font_size=32).next_to(sp, UP, buff=0.12)
        roc = sp.roc(left=-1, opacity=0.35)

        ax = signal_axes(x_range=(-2, 4, 1), y_range=(-1.5, 1.5, 0.5), x_length=6.8, y_length=4.4)
        ax.move_to(RIGHT * 2.6 + DOWN * 0.55)
        target = DashedVMobject(clipped_graph(ax, lambda t: np.exp(-t) * u(t), 0.001, 4, color=GREY_B, stroke_width=3)[0],
                                num_dashes=40)
        target_lab = MathTex(r"e^{-t}u(t)", font_size=30, color=GREY_B).next_to(ax.c2p(0.6, 1.0), RIGHT, buff=0.1)

        self.play(FadeIn(sp), FadeIn(Xs), FadeIn(pole), FadeIn(roc), Create(ax))
        self.play(Create(target), FadeIn(target_lab))

        def wvis():
            return 3.9 * (1 - np.exp(-W.get_value() / 8))

        brom_line = always_redraw(lambda: DashedLine(
            sp.c2p(sigma.get_value(), -4), sp.c2p(sigma.get_value(), 4), color=YELLOW, stroke_width=2, dash_length=0.08))
        seg = always_redraw(lambda: Line(
            sp.c2p(sigma.get_value(), -wvis()), sp.c2p(sigma.get_value(), wvis() + 1e-3), color=YELLOW, stroke_width=7))
        recon = always_redraw(lambda: clipped_polyline(
            ax, T_GRID, reconstruct(sigma.get_value(), W.get_value()), color=YELLOW, stroke_width=5))

        W_num = DecimalNumber(0, num_decimal_places=1, font_size=32)
        W_num.add_updater(lambda m: m.set_value(W.get_value()))
        W_read = VGroup(MathTex(r"\text{using } |\omega| <", font_size=32), W_num).arrange(RIGHT, buff=0.12)
        W_read.next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        recipe = MathTex(r"x(t) \approx \frac{1}{2\pi}\sum_k X(\sigma + jk\Delta\omega)\,e^{(\sigma + jk\Delta\omega)t}\,\Delta\omega",
                         font_size=32).next_to(ax, DOWN, buff=0.2)

        self.play(Create(brom_line))
        self.add(seg, recon)
        self.play(FadeIn(W_read), FadeIn(recipe))
        self.play(W.animate.set_value(2), run_time=2.5)
        self.wait(0.3)
        self.play(W.animate.set_value(8), run_time=3)
        self.wait(0.3)
        self.play(W.animate.set_value(60), run_time=5, rate_func=rate_functions.ease_in_quad)
        note = Tex(r"each point on the line contributes one spinning $e^{st}$;\\together they rebuild $x(t)$",
                   font_size=30, color=YELLOW).move_to(recipe)
        self.play(FadeTransform(recipe, note))
        self.wait(1.5)

        # --- slide the line around: same answer anywhere inside the ROC
        sig_num = DecimalNumber(0.3, num_decimal_places=2, include_sign=True, font_size=30)
        sig_num.add_updater(lambda m: m.set_value(sigma.get_value()))
        sig_read = VGroup(MathTex(r"\sigma =", font_size=30), sig_num).arrange(RIGHT, buff=0.1).next_to(sp, DOWN, buff=0.15)
        inside = Tex(r"any $\sigma$ inside the ROC gives the \emph{same} $x(t)$", font_size=30, color=GOOD).move_to(note)
        self.play(FadeIn(sig_read), FadeTransform(note, inside))
        self.play(sigma.animate.set_value(0.9), run_time=2)
        self.play(sigma.animate.set_value(-0.6), run_time=2.5)
        self.wait(0.5)

        # --- cross the pole: a different (left-sided) signal
        alt = DashedVMobject(clipped_graph(ax, lambda t: -np.exp(-t), -2, -0.001, color=RED_B, stroke_width=3)[0], num_dashes=25)
        alt_lab = MathTex(r"-e^{-t}u(-t)", font_size=30, color=RED_B).next_to(ax.c2p(-1.9, -0.6), RIGHT, buff=0.05)
        outside = Tex(r"line left of the pole: same $X(s)$, \emph{different} ROC $\Rightarrow$ different $x(t)$",
                      font_size=28, color=RED_B).move_to(inside).set_x(1.8)
        self.play(sigma.animate.set_value(-1.5), FadeIn(alt), FadeIn(alt_lab), FadeTransform(inside, outside), run_time=4)
        self.wait(2)
        self.play(sigma.animate.set_value(0.3), FadeOut(alt), FadeOut(alt_lab), run_time=3)
        self.wait(0.5)

        # --- closing the contour (t > 0): residues
        self.remove(seg)
        brom_line.clear_updaters()
        R = 3.2
        arc = ParametricFunction(lambda th: sp.c2p(0.3 + R * np.cos(th), R * np.sin(th)),
                                 t_range=[PI / 2, 3 * PI / 2], color=TEAL_C, stroke_width=5)
        vert = Line(sp.c2p(0.3, -R), sp.c2p(0.3, R), color=YELLOW, stroke_width=6)
        cr = MathTex("C_R", font_size=30, color=TEAL_C).next_to(arc.point_from_proportion(0.5), RIGHT, buff=0.15).shift(UP * 0.6)
        residue = MathTex(r"t>0:\ \ x(t) = \sum \mathrm{Res}\big[X(s)e^{st}\big]_{\text{poles inside}} = e^{-t}",
                          font_size=30, color=TEAL_C).move_to(outside).shift(UP * 0.15)
        self.play(Create(vert), Create(arc), FadeIn(cr), FadeTransform(outside, residue), run_time=2.5)
        self.play(Indicate(pole, color=TEAL_C, scale_factor=1.8))
        practice = Tex(r"in practice: partial fractions + a table of known pairs", font_size=28, color=GREY_A)
        practice.next_to(residue, DOWN, buff=0.1)
        self.play(FadeIn(practice))
        self.wait(2.5)
        fade_all(self)


class PartialFractionsAndROC(Scene):
    def construct(self):
        title = make_title(r"One $X(s)$, three possible signals (Ex.\ 9.8--9.11)")
        self.play(Write(title))

        # --------------------------------------------- partial fractions
        Xs = MathTex(r"X(s) = \frac{1}{(s+1)(s+2)}", font_size=38).move_to(LEFT * 3.4 + UP * 2.45)
        self.play(Write(Xs))
        expand = MathTex(r"=", r"\frac{1}{s+1}", r"-", r"\frac{1}{s+2}", font_size=38).next_to(Xs, RIGHT, buff=0.2)
        expand[1].set_color(TEAL_C)
        expand[3].set_color(GOLD)
        cover = VGroup(
            MathTex(r"A = (s+1)X(s)\big|_{s=-1} = 1", font_size=30, color=TEAL_C),
            MathTex(r"B = (s+2)X(s)\big|_{s=-2} = -1", font_size=30, color=GOLD),
        ).arrange(RIGHT, buff=0.8).next_to(VGroup(Xs, expand), DOWN, buff=0.35)
        self.play(FadeIn(cover[0], shift=DOWN * 0.2))
        self.play(FadeIn(cover[1], shift=DOWN * 0.2))
        self.play(Write(expand))
        self.wait(1)
        self.play(FadeOut(cover))

        # --------------------------------------------- stage
        sp = SPlane(x_range=(-3, 1, 1), y_range=(-1.5, 1.5, 1), x_length=4.8, y_length=2.4, number_size=18)
        sp.move_to(LEFT * 4.1 + DOWN * 2.2)
        p1 = sp.pole(-1, color=TEAL_C)
        p2 = sp.pole(-2, color=GOLD)
        ax = signal_axes(x_range=(-3, 4, 1), y_range=(-2, 2, 1), x_length=6.2, y_length=4.4)
        ax.move_to(RIGHT * 3.6 + DOWN * 1.15)
        rule = VGroup(
            Tex(r"pole with ROC on its \textbf{right} $\Rightarrow$ right-sided: $\ \frac{A}{s+a} \leftrightarrow A e^{-at}u(t)$", font_size=26),
            Tex(r"pole with ROC on its \textbf{left} $\Rightarrow$ left-sided: $\ \frac{A}{s+a} \leftrightarrow -A e^{-at}u(-t)$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rule_bg = SurroundingRectangle(rule, color=GREY_B, buff=0.12, corner_radius=0.08)
        VGroup(rule, rule_bg).next_to(sp, UP, buff=0.18).align_to(sp, LEFT)
        self.play(FadeIn(sp), FadeIn(p1), FadeIn(p2), Create(ax))
        self.play(FadeIn(rule), Create(rule_bg))

        cases = [
            dict(roc=dict(left=-1), roc_tex=r"\mathrm{Re}\{s\} > -1", kind="right-sided (causal)",
                 sides=(RIGHT, RIGHT),
                 t1=r"e^{-t}u(t)", t2=r"-e^{-2t}u(t)", sum=r"x(t) = \big(e^{-t} - e^{-2t}\big)u(t)",
                 f1=lambda t: np.exp(-t) * u(t), f2=lambda t: -np.exp(-2 * t) * u(t)),
            dict(roc=dict(right=-2), roc_tex=r"\mathrm{Re}\{s\} < -2", kind="left-sided",
                 sides=(LEFT, LEFT),
                 t1=r"-e^{-t}u(-t)", t2=r"+e^{-2t}u(-t)", sum=r"x(t) = \big(-e^{-t} + e^{-2t}\big)u(-t)",
                 f1=lambda t: -np.exp(-t) * u(-t), f2=lambda t: np.exp(-2 * t) * u(-t)),
            dict(roc=dict(left=-2, right=-1), roc_tex=r"-2 < \mathrm{Re}\{s\} < -1", kind="two-sided",
                 sides=(LEFT, RIGHT),
                 t1=r"-e^{-t}u(-t)", t2=r"-e^{-2t}u(t)", sum=r"x(t) = -e^{-t}u(-t) - e^{-2t}u(t)",
                 f1=lambda t: -np.exp(-t) * u(-t), f2=lambda t: -np.exp(-2 * t) * u(t)),
        ]

        def build(c):
            region = sp.roc(**c["roc"], opacity=0.45)
            roc_lab = MathTex(c["roc_tex"], font_size=30, color=BLUE_B).next_to(sp, DOWN, buff=0.12)
            arrows = VGroup(
                Arrow(sp.c2p(-1, 0.6), sp.c2p(-1, 0.6) + c["sides"][0] * 0.55, buff=0, color=TEAL_C, stroke_width=5,
                      max_tip_length_to_length_ratio=0.4),
                Arrow(sp.c2p(-2, 0.6), sp.c2p(-2, 0.6) + c["sides"][1] * 0.55, buff=0, color=GOLD, stroke_width=5,
                      max_tip_length_to_length_ratio=0.4),
            )
            terms = VGroup(
                MathTex(r"\tfrac{1}{s+1}", r"\ \longrightarrow\ ", c["t1"], font_size=34),
                MathTex(r"-\tfrac{1}{s+2}", r"\ \longrightarrow\ ", c["t2"], font_size=34),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            terms[0][0].set_color(TEAL_C)
            terms[0][2].set_color(TEAL_C)
            terms[1][0].set_color(GOLD)
            terms[1][2].set_color(GOLD)
            terms.next_to(VGroup(Xs, expand), DOWN, buff=0.22).align_to(Xs, LEFT)
            total = MathTex(c["sum"], font_size=34, color=YELLOW).next_to(ax, UP, buff=0.15)
            kind = Tex(c["kind"], font_size=32, color=YELLOW).next_to(ax, DOWN, buff=0.2)
            g1 = clipped_graph(ax, c["f1"], -3, 4, breaks=[0], color=TEAL_C, stroke_width=3, opacity=0.7)
            g2 = clipped_graph(ax, c["f2"], -3, 4, breaks=[0], color=GOLD, stroke_width=3, opacity=0.7)
            gs = clipped_graph(ax, lambda t: c["f1"](t) + c["f2"](t), -3, 4, breaks=[0], color=YELLOW, stroke_width=6)
            return dict(region=region, roc_lab=roc_lab, arrows=arrows, terms=terms, total=total, kind=kind,
                        g1=g1, g2=g2, gs=gs)

        prev = None
        for c in cases:
            cur = build(c)
            if prev is None:
                self.play(FadeIn(cur["region"]), Write(cur["roc_lab"]))
                self.play(GrowArrow(cur["arrows"][0]), GrowArrow(cur["arrows"][1]))
                self.play(Write(cur["terms"][0]))
                self.play(Create(cur["g1"]))
                self.play(Write(cur["terms"][1]))
                self.play(Create(cur["g2"]))
                self.play(Write(cur["total"]), Create(cur["gs"]), FadeIn(cur["kind"]))
            else:
                self.play(
                    Transform(prev["region"], cur["region"]),
                    FadeTransform(prev["roc_lab"], cur["roc_lab"]),
                    Transform(prev["arrows"], cur["arrows"]),
                    run_time=1.5,
                )
                self.remove(prev["region"], prev["arrows"])
                self.add(cur["region"], cur["arrows"])
                self.play(
                    FadeTransform(prev["terms"], cur["terms"]),
                    FadeOut(prev["g1"]), FadeOut(prev["g2"]), FadeOut(prev["gs"]),
                    FadeTransform(prev["total"], cur["total"]), FadeTransform(prev["kind"], cur["kind"]),
                )
                self.play(Create(cur["g1"]), Create(cur["g2"]), run_time=1.5)
                self.play(Create(cur["gs"]), run_time=1.5)
            self.wait(2)
            prev = cur

        final = Tex(r"the ROC picks the time direction of \emph{each} pole's exponential", font_size=32, color=YELLOW)
        final.move_to(title)
        self.play(FadeTransform(title, final))
        self.wait(2.5)
        fade_all(self)
