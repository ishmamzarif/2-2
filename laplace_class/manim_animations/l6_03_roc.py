"""Lecture 6 - Region of convergence.

Scenes:
  SameFormulaDifferentROC  Examples 9.1 / 9.2: e^{-at}u(t) and -e^{-at}u(-t) share X(s) = 1/(s+a);
                           a sweeping test line Re{s} = sigma shows which side converges.
  ROCProperties            Property 1 (vertical strips), 3 (finite duration -> whole plane),
                           4-6 via Example 9.7 e^{-b|t|} (right part + left part = strip),
                           including what happens when b <= 0.
"""
from common import *

A = 0.5  # the "a" in e^{-at}


class SameFormulaDifferentROC(Scene):
    def construct(self):
        title = make_title(r"Same $X(s)$, two different signals")
        self.play(Write(title))

        sigma = ValueTracker(1.0)
        rows = []
        specs = [
            dict(y=1.35, yr=(-0.5, 1.5, 0.5), sig=lambda t: np.exp(-A * t) * u(t),
                 name=r"x_1(t) = e^{-at}u(t)", roc=dict(left=-A), roc_tex=r"\mathrm{Re}\{s\} > -a",
                 ok=lambda s: s > -A, integral=r"\int_0^{\infty} e^{-(s+a)t}dt", color=SIG),
            dict(y=-2.05, yr=(-3, 0.5, 1), sig=lambda t: -np.exp(-A * t) * u(-t),
                 name=r"x_2(t) = -e^{-at}u(-t)", roc=dict(right=-A), roc_tex=r"\mathrm{Re}\{s\} < -a",
                 ok=lambda s: s < -A, integral=r"\int_{-\infty}^{0} -e^{-(s+a)t}dt", color=SIG2),
        ]
        for spec in specs:
            ax = signal_axes(x_range=(-4, 4, 1), y_range=spec["yr"], x_length=5.4, y_length=2.5)
            ax.move_to(LEFT * 3.9 + UP * spec["y"])
            graph = clipped_graph(ax, spec["sig"], -4, 4, breaks=[0], color=spec["color"])
            name = MathTex(spec["name"], font_size=30, color=spec["color"])
            name.next_to(ax.c2p(-4, spec["yr"][1]), RIGHT, buff=0.2).shift(DOWN * 0.15)
            if spec["yr"][0] < -1:
                name.next_to(ax.c2p(0.2, -1.6), RIGHT, buff=0.0)

            sp = SPlane(x_range=(-3, 2, 1), y_range=(-2, 2, 1), x_length=3.0, y_length=2.4, number_size=16)
            sp.move_to(RIGHT * 1.0 + UP * spec["y"])
            pole = sp.pole(-A, size=0.11)
            pole_lab = MathTex("-a", font_size=24, color=POLE_COLOR).next_to(pole, UL, buff=0.02)
            Xs = MathTex(r"X(s) = \frac{1}{s+a}", font_size=40).move_to(RIGHT * 4.8 + UP * (spec["y"] + 0.5))
            roc_t = MathTex(spec["roc_tex"], font_size=34, color=BLUE_B).next_to(Xs, DOWN, buff=0.25)
            integral = MathTex(spec["integral"], font_size=30, color=GREY_A).next_to(Xs, UP, buff=0.25)
            roc = sp.roc(**spec["roc"])
            rows.append(dict(ax=ax, graph=graph, name=name, sp=sp, pole=pole, pole_lab=pole_lab, Xs=Xs,
                             roc_t=roc_t, roc=roc, spec=spec, integral=integral))

        for r in rows:
            self.play(Create(r["ax"]), FadeIn(r["name"]), run_time=1)
            self.play(Create(r["graph"]), run_time=1.5)
            self.play(FadeIn(r["sp"]), Write(r["integral"]))
            self.play(Write(r["Xs"]), FadeIn(r["pole"], scale=2), FadeIn(r["pole_lab"]))
            side = RIGHT if "left" in r["spec"]["roc"] else LEFT
            self.play(FadeIn(r["roc"], shift=side * 0.4), Write(r["roc_t"]))
            self.wait(0.5)

        # identical formulas!
        boxes = VGroup(*[SurroundingRectangle(r["Xs"], color=YELLOW, buff=0.1) for r in rows])
        same = Tex("identical!", font_size=32, color=YELLOW).move_to(
            (rows[0]["Xs"].get_center() + rows[1]["Xs"].get_center()) / 2 + DOWN * 0.15)
        self.play(Create(boxes), FadeIn(same, scale=1.3), *[FadeOut(r["integral"]) for r in rows])
        self.wait(1)
        self.play(*[Indicate(r["roc"], color=BLUE_B, scale_factor=1.05) for r in rows],
                  *[Indicate(r["roc_t"]) for r in rows])
        self.wait(0.5)
        self.play(FadeOut(boxes), FadeOut(same))

        # --------------------------------------------- the sweeping test line
        new_title = make_title(r"Test line $\mathrm{Re}\{s\} = \sigma$: does $x(t)\,e^{-\sigma t}$ die out?")
        self.play(FadeTransform(title, new_title))
        movers = []
        for r in rows:
            sp, ax, f, ok = r["sp"], r["ax"], r["spec"]["sig"], r["spec"]["ok"]
            line = always_redraw(lambda sp=sp, ok=ok: sp.vline(
                sigma.get_value(), color=GOOD if ok(sigma.get_value()) else BAD, width=4))
            prod = always_redraw(lambda ax=ax, f=f: clipped_graph(
                ax, lambda t: f(t) * np.exp(-sigma.get_value() * t), -4, 4, breaks=[0], color=PROD, stroke_width=4))
            mark = always_redraw(lambda sp=sp, ok=ok: check(ok(sigma.get_value()), font_size=44)
                                 .next_to(sp, LEFT, buff=0.1).shift(UP * 0.8))
            movers += [line, prod, mark]
            r["graph"].set_stroke(opacity=0.35)
        sig_num = DecimalNumber(1.0, num_decimal_places=2, include_sign=True, font_size=34)
        sig_num.add_updater(lambda m: m.set_value(sigma.get_value()))
        sig_read = VGroup(MathTex(r"\sigma =", font_size=34), sig_num).arrange(RIGHT, buff=0.1)
        sig_read.move_to(RIGHT * 4.8 + UP * 0.1)
        legend = MathTex(r"\text{yellow: } x(t)\,e^{-\sigma t}", font_size=30, color=PROD).next_to(sig_read, DOWN, buff=0.2)
        self.play(*[FadeIn(m) for m in movers], FadeIn(sig_read), FadeIn(legend))
        for target, rt in [(-0.3, 2.0), (-0.5, 1.5), (-1.2, 2.0), (-2.5, 2.5), (-0.9, 1.5), (0.7, 3.0)]:
            self.play(sigma.animate.set_value(target), run_time=rt)
            self.wait(0.3)

        final = Tex(r"The formula alone is \emph{not} the answer --- the ROC is part of $X(s)$",
                    font_size=34, color=YELLOW).to_edge(DOWN, buff=0.15)
        bg = BackgroundRectangle(final, fill_opacity=0.85, buff=0.1)
        self.play(FadeIn(bg), Write(final))
        self.wait(2.5)
        fade_all(self)


class ROCProperties(Scene):
    def construct(self):
        self.property_1()
        self.property_3()
        self.properties_4_to_6()

    # ------------------------------------------------------------------
    def property_1(self):
        title = make_title(r"Property 1: the ROC is made of vertical strips")
        sp = SPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), x_length=5.2, y_length=5.2)
        sp.move_to(LEFT * 3.7 + DOWN * 0.45)
        self.play(Write(title), FadeIn(sp))

        eq1 = MathTex(r"\big|x(t)\,e^{-(\sigma + j\omega)t}\big|", r"=", r"|x(t)|\,e^{-\sigma t}", r"\,\big|e^{-j\omega t}\big|",
                      font_size=40).move_to(RIGHT * 3.0 + UP * 1.5)
        eq1[3].set_color(TEAL_C)
        self.play(Write(eq1))
        one = MathTex(r"=1", font_size=40, color=TEAL_C).next_to(eq1[3], DOWN, buff=0.35)
        self.play(FadeIn(one, shift=UP * 0.2))
        cross = Line(eq1[3].get_corner(DL), eq1[3].get_corner(UR), color=BAD, stroke_width=5)
        self.play(Create(cross))
        only = Tex(r"only $\sigma = \mathrm{Re}\{s\}$ decides convergence", font_size=34, color=YELLOW)
        only.next_to(eq1, DOWN, buff=1.1)
        self.play(FadeIn(only))

        # a point sliding up and down a vertical line keeps the same verdict
        y = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(sp.c2p(1, y.get_value()), color=YELLOW))
        trail = always_redraw(lambda: Line(sp.c2p(1, -3), sp.c2p(1, y.get_value()), color=YELLOW, stroke_width=3)
                              if y.get_value() > -2.99 else VMobject())
        y.set_value(-3)
        verdict = Tex(r"converges here $\Rightarrow$ converges on the whole line", font_size=30, color=GOOD)
        verdict.next_to(only, DOWN, buff=0.4)
        self.add(trail, dot)
        self.play(y.animate.set_value(3), run_time=2.5, rate_func=smooth)
        self.play(FadeIn(verdict))
        strip = sp.roc(left=-0.5, right=2.0, opacity=0.45)
        lines = VGroup(*[sp.vline(x, color=BLUE_B, width=2) for x in np.linspace(-0.45, 1.95, 14)])
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1), run_time=1.5)
        self.play(FadeIn(strip), FadeOut(lines))
        self.remove(trail, dot)
        self.wait(0.6)

        # property 2: no poles inside
        p2 = Tex(r"Property 2: the ROC never contains a pole", font_size=34, color=POLE_COLOR)
        p2.next_to(verdict, DOWN, buff=0.6)
        pole = sp.pole(2.0, size=0.16)
        self.play(FadeIn(p2), FadeIn(pole, scale=2.5))
        self.play(Flash(pole.get_center(), color=POLE_COLOR, flash_radius=0.4))
        why = MathTex(r"X(s_{\text{pole}}) = \infty", font_size=34, color=GREY_A).next_to(p2, DOWN, buff=0.25)
        self.play(FadeIn(why))
        self.wait(1.5)
        fade_all(self)
        self.sp = None

    # ------------------------------------------------------------------
    def property_3(self):
        title = make_title(r"Property 3: finite duration $\Rightarrow$ ROC is the entire $s$-plane")
        sp = SPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), x_length=4.6, y_length=4.6)
        sp.move_to(RIGHT * 4.0 + DOWN * 0.5)
        ax = signal_axes(x_range=(-1, 3, 1), y_range=(0, 3, 1), x_length=6.5, y_length=4.2)
        ax.move_to(LEFT * 3.1 + DOWN * 0.5)
        f = lambda t: np.exp(-t) if 0 <= t <= 2 else 0.0
        graph = clipped_graph(ax, f, -1, 3, breaks=[0, 2], color=SIG)
        name = MathTex(r"x(t) = e^{-t},\ 0 < t < 2", font_size=32, color=SIG).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        self.play(Write(title), Create(ax), FadeIn(sp))
        self.play(Create(graph), FadeIn(name))

        sigma = ValueTracker(0.0)
        prod = always_redraw(lambda: clipped_graph(
            ax, lambda t: f(t) * np.exp(-sigma.get_value() * t), -1, 3, breaks=[0, 2], color=PROD, stroke_width=5))
        area = always_redraw(lambda: clipped_area(ax, lambda t: np.exp(-(1 + sigma.get_value()) * t), 0, 2))
        line = always_redraw(lambda: sp.vline(sigma.get_value(), color=GOOD, width=4))
        legend = MathTex(r"x(t)\,e^{-\sigma t}", font_size=32, color=PROD).next_to(name, RIGHT, buff=0.6)
        self.play(FadeIn(prod), FadeIn(area), Create(line), FadeIn(legend))
        reason = Tex(r"a finite stretch of a bounded curve\\always has finite area --- for \emph{any} $\sigma$",
                     font_size=30).next_to(sp, UP, buff=0.25)
        self.play(FadeIn(reason))
        for target in [-1.5, 2.5, -1.0, 0.5]:
            self.play(sigma.animate.set_value(target), run_time=2)
        whole = sp.roc(opacity=0.45)
        self.play(FadeIn(whole))
        self.wait(1.5)
        fade_all(self)

    # ------------------------------------------------------------------
    def properties_4_to_6(self):
        title = make_title(r"Properties 4--6: right-sided, left-sided, two-sided (Ex.\ 9.7)")
        b = ValueTracker(1.0)
        ax = signal_axes(x_range=(-4, 4, 1), y_range=(0, 2.5, 1), x_length=8, y_length=2.4)
        ax.move_to(UP * 1.45 + LEFT * 1.6)
        sp = SPlane(x_range=(-3, 3, 1), y_range=(-2, 2, 1), x_length=4.8, y_length=3.2, number_size=18)
        sp.move_to(LEFT * 3.4 + DOWN * 2.15)
        self.play(Write(title), Create(ax), FadeIn(sp))

        right_part = always_redraw(lambda: clipped_graph(
            ax, lambda t: np.exp(-b.get_value() * t), 0, 4, color=BLUE_C, stroke_width=5))
        left_part = always_redraw(lambda: clipped_graph(
            ax, lambda t: np.exp(b.get_value() * t), -4, 0, color=RED_C, stroke_width=5))
        name = MathTex(r"x(t) = e^{-b|t|}", font_size=36).next_to(ax, RIGHT, buff=0.3).shift(UP * 0.6)
        split = MathTex(r"=", r"e^{bt}u(-t)", r"+", r"e^{-bt}u(t)", font_size=34).next_to(name, DOWN, aligned_edge=LEFT, buff=0.25)
        split[1].set_color(RED_C)
        split[3].set_color(BLUE_C)
        self.play(Create(left_part), Create(right_part), Write(name))
        self.play(Write(split))

        def regions():
            bb = b.get_value()
            g = VGroup(
                sp.roc(left=-bb, color=BLUE_C, opacity=0.28),
                sp.roc(right=bb, color=RED_C, opacity=0.28),
            )
            if bb > 1e-3:
                g.add(sp.roc(left=-bb, right=bb, color=PURPLE_B, opacity=0.45, boundary=False))
            return g

        def poles():
            bb = b.get_value()
            return VGroup(sp.pole(-bb, size=0.11), sp.pole(bb, size=0.11))

        expl = VGroup(
            MathTex(r"e^{-bt}u(t):\ \mathrm{Re}\{s\} > -b", font_size=32, color=BLUE_C),
            Tex(r"right-sided $\Rightarrow$ ROC extends to the right", font_size=26, color=GREY_A),
            MathTex(r"e^{bt}u(-t):\ \mathrm{Re}\{s\} < b", font_size=32, color=RED_C),
            Tex(r"left-sided $\Rightarrow$ ROC extends to the left", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 3.0 + DOWN * 1.55)

        blue_roc = sp.roc(left=-1, color=BLUE_C, opacity=0.28)
        red_roc = sp.roc(right=1, color=RED_C, opacity=0.28)
        pole_m = poles()
        self.play(FadeIn(pole_m))
        self.play(FadeIn(blue_roc, shift=RIGHT * 0.3), FadeIn(expl[0]), FadeIn(expl[1]))
        self.play(FadeIn(red_roc, shift=LEFT * 0.3), FadeIn(expl[2]), FadeIn(expl[3]))
        strip_lab = MathTex(r"-b < \mathrm{Re}\{s\} < b", font_size=30, color=PURPLE_A)
        strip_lab.next_to(sp, UP, buff=0.1)
        both = Tex(r"two-sided: ROC = overlap = a \emph{strip}", font_size=30, color=PURPLE_A).next_to(strip_lab, RIGHT, buff=0.4)
        purple = sp.roc(left=-1, right=1, color=PURPLE_B, opacity=0.45, boundary=False)
        self.play(FadeIn(purple), FadeIn(strip_lab), FadeIn(both))
        self.wait(1)

        self.remove(blue_roc, red_roc, pole_m, purple)
        roc_m = always_redraw(regions)
        pole_r = always_redraw(poles)
        self.add(roc_m, pole_r)

        b_num = DecimalNumber(1.0, num_decimal_places=2, include_sign=True, font_size=34)
        b_num.add_updater(lambda m: m.set_value(b.get_value()))
        b_read = VGroup(MathTex("b =", font_size=34), b_num).arrange(RIGHT, buff=0.1).next_to(split, DOWN, buff=0.35)
        self.play(FadeIn(b_read))
        self.play(b.animate.set_value(0.4), run_time=2)
        self.play(b.animate.set_value(1.6), run_time=2)
        self.play(b.animate.set_value(0.0), run_time=2.5)
        warn = Tex(r"$b \le 0$: the regions no longer overlap $\Rightarrow$ no Laplace transform at all", font_size=32, color=BAD)
        self.play(b.animate.set_value(-0.5), FadeOut(both), FadeOut(strip_lab), run_time=2)
        warn.next_to(sp, UP, buff=0.1).align_to(sp, LEFT)
        self.play(FadeIn(warn))
        self.wait(1.5)
        self.play(FadeOut(warn), b.animate.set_value(1.0), run_time=2)
        result = MathTex(r"X(s) = \frac{-2b}{s^2 - b^2},\quad -b < \mathrm{Re}\{s\} < b", font_size=36, color=YELLOW)
        result.next_to(sp, UP, buff=0.1).align_to(sp, LEFT)
        self.play(Write(result))
        self.wait(2.5)
        fade_all(self)
