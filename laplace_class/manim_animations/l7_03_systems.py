"""Lecture 7 - Analysing LTI systems with the Laplace transform.

Scenes:
  CausalityAndStability  Example 9.20: H(s) = (s-1)/((s+1)(s-2)) with its three possible ROCs.
                         causal <=> ROC is a right half-plane; stable <=> ROC contains the j omega-axis.
  PoleDragStability      for a causal rational system, drag the poles around and watch h(t):
                         left half-plane = decays, j omega-axis = rings forever, right half-plane = blows up.
"""
from common import *


class CausalityAndStability(Scene):
    def construct(self):
        title = make_title(r"Causality and stability, read off the ROC (Ex.\ 9.20)")
        self.play(Write(title))

        H = MathTex(r"H(s) = \frac{s-1}{(s+1)(s-2)}", r"= \frac{2/3}{s+1} + \frac{1/3}{s-2}", font_size=36)
        H.move_to(LEFT * 3.4 + UP * 2.35)
        self.play(Write(H[0]))
        self.play(Write(H[1]))

        sp = SPlane(x_range=(-3, 3, 1), y_range=(-1.5, 1.5, 1), x_length=5.4, y_length=2.8, number_size=18)
        sp.move_to(LEFT * 3.7 + DOWN * 0.35)
        marks = VGroup(sp.pole(-1), sp.pole(2), sp.zero(1))
        jw = sp.jw_axis(width=5)
        ax = signal_axes(x_range=(-3, 3, 1), y_range=(-1.5, 1.5, 0.5), x_length=6.0, y_length=4.0, y_label="h(t)")
        ax.move_to(RIGHT * 3.6 + DOWN * 1.0)
        self.play(FadeIn(sp), FadeIn(marks), Create(ax))

        rules = VGroup(
            Tex(r"\textbf{causal} $\Leftrightarrow$ ROC is a right half-plane", font_size=28),
            Tex(r"\textbf{stable} $\Leftrightarrow$ ROC contains the $j\omega$-axis", font_size=28, color=JW_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rules_box = SurroundingRectangle(rules, color=GREY_B, buff=0.15, corner_radius=0.08)
        VGroup(rules, rules_box).next_to(sp, DOWN, buff=0.35)
        self.play(FadeIn(rules), Create(rules_box), Create(jw))

        cases = [
            dict(roc=dict(left=2), roc_tex=r"\mathrm{Re}\{s\} > 2",
                 h=r"h(t) = \big(\tfrac{2}{3}e^{-t} + \tfrac{1}{3}e^{2t}\big)u(t)",
                 f=lambda t: (2 / 3 * np.exp(-t) + 1 / 3 * np.exp(2 * t)) * u(t), causal=True, stable=False,
                 verdict="causal, but unstable"),
            dict(roc=dict(left=-1, right=2), roc_tex=r"-1 < \mathrm{Re}\{s\} < 2",
                 h=r"h(t) = \tfrac{2}{3}e^{-t}u(t) - \tfrac{1}{3}e^{2t}u(-t)",
                 f=lambda t: 2 / 3 * np.exp(-t) * u(t) - 1 / 3 * np.exp(2 * t) * u(-t), causal=False, stable=True,
                 verdict="stable, but not causal"),
            dict(roc=dict(right=-1), roc_tex=r"\mathrm{Re}\{s\} < -1",
                 h=r"h(t) = -\big(\tfrac{2}{3}e^{-t} + \tfrac{1}{3}e^{2t}\big)u(-t)",
                 f=lambda t: -(2 / 3 * np.exp(-t) + 1 / 3 * np.exp(2 * t)) * u(-t), causal=False, stable=False,
                 verdict="anticausal and unstable"),
        ]

        def build(c):
            region = sp.roc(**c["roc"], opacity=0.45)
            region.set_z_index(-1)
            roc_lab = MathTex(c["roc_tex"], font_size=30, color=BLUE_B).next_to(sp, UP, buff=0.1).align_to(sp, RIGHT)
            h_tex = MathTex(c["h"], font_size=32, color=SIG).next_to(ax, UP, buff=0.2)
            graph = clipped_graph(ax, c["f"], -3, 3, breaks=[0], color=SIG, stroke_width=5)
            badges = VGroup(
                VGroup(Tex("causal", font_size=30), check(c["causal"])).arrange(RIGHT, buff=0.15),
                VGroup(Tex("stable", font_size=30), check(c["stable"])).arrange(RIGHT, buff=0.15),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax.c2p(-3, 1.5), RIGHT, buff=0.15).shift(DOWN * 0.3)
            verdict = Tex(c["verdict"], font_size=32, color=GOOD if c["stable"] else BAD).next_to(ax, DOWN, buff=0.15)
            return dict(region=region, roc_lab=roc_lab, h_tex=h_tex, graph=graph, badges=badges, verdict=verdict)

        prev = None
        for c in cases:
            cur = build(c)
            if prev is None:
                self.play(FadeIn(cur["region"]), Write(cur["roc_lab"]))
                self.play(Write(cur["h_tex"]), Create(cur["graph"]), run_time=2)
                self.play(FadeIn(cur["badges"]), FadeIn(cur["verdict"]))
            else:
                self.play(Transform(prev["region"], cur["region"]), FadeTransform(prev["roc_lab"], cur["roc_lab"]),
                          FadeOut(prev["graph"]), FadeOut(prev["badges"]), FadeOut(prev["verdict"]),
                          FadeTransform(prev["h_tex"], cur["h_tex"]), run_time=1.5)
                self.remove(prev["region"])
                self.add(cur["region"])
                self.play(Create(cur["graph"]), run_time=1.5)
                self.play(FadeIn(cur["badges"]), FadeIn(cur["verdict"]))
            if c["stable"]:
                self.play(Indicate(jw, color=GOOD, scale_factor=1.0), Flash(sp.c2p(0, 0), color=GOOD))
            self.wait(1.8)
            prev = cur

        final = Tex(r"one $H(s)$, three systems: only the ROC holding the $j\omega$-axis is stable",
                    font_size=34, color=YELLOW).move_to(title)
        self.play(FadeTransform(title, final))
        self.wait(2.5)
        fade_all(self)


class PoleDragStability(Scene):
    def construct(self):
        title = make_title(r"Causal $+$ rational: stable $\Leftrightarrow$ every pole in the left half-plane")
        self.play(Write(title))

        sp = SPlane(x_range=(-3, 2, 1), y_range=(-3, 3, 1), x_length=4.6, y_length=5.5, number_size=18)
        sp.move_to(LEFT * 4.3 + DOWN * 0.55)
        lhp = sp.roc(right=0, color=GREEN_E, opacity=0.25, boundary=False)
        rhp = sp.roc(left=0, color=RED_E, opacity=0.25, boundary=False)
        lhp_t = Tex("stable", font_size=26, color=GREEN_B).move_to(sp.c2p(-2.2, -2.6))
        rhp_t = Tex("unstable", font_size=26, color=RED_B).move_to(sp.c2p(1.2, -2.6))
        jw = sp.jw_axis(width=4)

        ax = signal_axes(x_range=(0, 10, 1), y_range=(-2, 2, 1), x_length=6.6, y_length=4.4, y_label="h(t)")
        ax.move_to(RIGHT * 3.0 + DOWN * 0.7)
        self.play(FadeIn(sp), FadeIn(lhp), FadeIn(rhp), FadeIn(lhp_t), FadeIn(rhp_t), Create(jw), Create(ax))

        # ---------------------------------------------- one real pole
        p = ValueTracker(-1.5)
        Hs = MathTex(r"H(s) = \frac{1}{s - p}", r"\ \Rightarrow\ h(t) = e^{pt}u(t)", font_size=34)
        Hs.next_to(ax, UP, buff=0.25)
        pole = always_redraw(lambda: sp.pole(p.get_value(), size=0.16))
        roc = always_redraw(lambda: sp.roc(left=p.get_value(), opacity=0.3))
        graph = always_redraw(lambda: clipped_graph(ax, lambda t: np.exp(p.get_value() * t), 0, 10, color=SIG, stroke_width=5))

        def badge(rightmost):
            ok = rightmost < -1e-3
            word = "stable" if ok else ("marginal: never dies out" if abs(rightmost) <= 1e-3 else "unstable")
            return VGroup(Tex(r"ROC $\ni j\omega$-axis?", font_size=30), check(ok, font_size=40),
                          Tex(word, font_size=30, color=GOOD if ok else BAD)).arrange(RIGHT, buff=0.2).next_to(ax, DOWN, buff=0.2)

        status = always_redraw(lambda: badge(p.get_value()))
        self.play(Write(Hs), FadeIn(roc), FadeIn(pole), Create(graph), FadeIn(status))
        for target, rt in [(-0.4, 2), (0.0, 2), (0.25, 2), (-1.0, 2.5)]:
            self.play(p.animate.set_value(target), run_time=rt)
            self.wait(0.6)
        for m in (pole, roc, graph, status):
            m.clear_updaters()
        self.play(FadeOut(VGroup(pole, roc, graph, status)))

        # ---------------------------------------------- a complex-conjugate pair
        sig = ValueTracker(-0.6)
        om = ValueTracker(1.5)
        Hs2 = MathTex(r"\text{poles } \sigma \pm j\omega_0", r"\ \Rightarrow\ h(t) \propto e^{\sigma t}\sin(\omega_0 t)\,u(t)", font_size=34)
        Hs2.move_to(Hs)
        poles = always_redraw(lambda: VGroup(sp.pole(complex(sig.get_value(), om.get_value()), size=0.16),
                                             sp.pole(complex(sig.get_value(), -om.get_value()), size=0.16)))
        roc2 = always_redraw(lambda: sp.roc(left=sig.get_value(), opacity=0.3))
        graph2 = always_redraw(lambda: clipped_graph(
            ax, lambda t: np.exp(sig.get_value() * t) * np.sin(om.get_value() * t), 0, 10, n=800, color=SIG, stroke_width=5))
        status2 = always_redraw(lambda: badge(sig.get_value()))
        self.play(FadeTransform(Hs, Hs2), FadeIn(roc2), FadeIn(poles), Create(graph2), FadeIn(status2))
        for s_, o_, rt in [(-0.25, 1.5, 2), (-0.25, 3.0, 2), (0.0, 3.0, 2), (0.0, 1.2, 2), (0.12, 1.2, 2), (-0.5, 2.0, 2.5)]:
            self.play(sig.animate.set_value(s_), om.animate.set_value(o_), run_time=rt)
            self.wait(0.5)
        summary = Tex(r"distance from the $j\omega$-axis = decay rate,\quad height = oscillation frequency",
                      font_size=30, color=YELLOW).move_to(title)
        self.play(FadeTransform(title, summary))
        self.wait(2.5)
        fade_all(self)
