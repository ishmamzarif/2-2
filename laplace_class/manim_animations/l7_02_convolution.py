"""Lecture 7 - Convolution property.

Scene: ConvolutionBecomesMultiplication
  Left : the painful way, y(t) = \\int x(tau) h(t - tau) dtau with a sliding, flipped h.
  Right: the Laplace way, Y(s) = X(s) H(s) -> partial fractions -> y(t).
  Both give y(t) = (e^{-2t} - e^{-3t}) u(t)  (the same system/input used in the DE slides).
"""
from common import *


def x_sig(t):
    return np.exp(-2 * t) * u(t)


def h_sig(t):
    return np.exp(-3 * t) * u(t)


def y_exact(t):
    return (np.exp(-2 * t) - np.exp(-3 * t)) * u(t)


class ConvolutionBecomesMultiplication(Scene):
    def construct(self):
        title = make_title(r"Convolution in time $=$ multiplication in $s$")
        self.play(Write(title))

        # ------------------------------------------------ left: time domain
        top = signal_axes(x_range=(-1.5, 4, 1), y_range=(0, 1.2, 0.5), x_length=6.6, y_length=2.3, x_label=r"\tau")
        top.move_to(LEFT * 3.4 + UP * 1.25)
        bot = signal_axes(x_range=(-1.5, 4, 1), y_range=(0, 0.2, 0.1), x_length=6.6, y_length=2.3)
        bot.move_to(LEFT * 3.4 + DOWN * 2.1)
        ylab = MathTex(r"y(t) = \int x(\tau)\,h(t-\tau)\,d\tau", font_size=30, color=YELLOW)
        ylab.next_to(bot, UP, buff=0.1).align_to(bot, LEFT).shift(RIGHT * 0.3)
        tick = MathTex("0.1", font_size=20, color=GREY_A).next_to(bot.c2p(0, 0.1), LEFT, buff=0.08)

        t = ValueTracker(-1.0)
        x_graph = clipped_graph(top, x_sig, -1.5, 4, breaks=[0], color=SIG, stroke_width=4)
        h_graph = always_redraw(lambda: clipped_graph(
            top, lambda tau: h_sig(t.get_value() - tau), -1.5, 4, breaks=[t.get_value()], color=GOLD, stroke_width=4))
        area = always_redraw(lambda: VMobject() if t.get_value() <= 0.01 else clipped_area(
            top, lambda tau: x_sig(tau) * h_sig(t.get_value() - tau), 0, t.get_value(), color=GREEN_C, opacity=0.6))
        prod = always_redraw(lambda: VMobject() if t.get_value() <= 0.01 else clipped_graph(
            top, lambda tau: x_sig(tau) * h_sig(t.get_value() - tau), 0, t.get_value(), n=200, color=GREEN_B, stroke_width=3))
        t_line = always_redraw(lambda: DashedLine(top.c2p(t.get_value(), 0), top.c2p(t.get_value(), 1.2),
                                                  color=GREY_B, stroke_width=2, dash_length=0.06))
        t_mark = always_redraw(lambda: MathTex("t", font_size=26, color=GREY_A).next_to(top.c2p(t.get_value(), 1.2), UP, buff=0.05))

        def y_trace():
            tt = t.get_value()
            if tt <= -1.49:
                return VMobject()
            return clipped_graph(bot, y_exact, -1.5, tt, n=300, color=YELLOW, stroke_width=5)

        y_m = always_redraw(y_trace)
        y_dot = always_redraw(lambda: Dot(bot.c2p(t.get_value(), y_exact(t.get_value())), color=YELLOW, radius=0.06))

        legend = VGroup(
            MathTex(r"x(\tau) = e^{-2\tau}u(\tau)", font_size=26, color=SIG),
            MathTex(r"h(t-\tau)", font_size=26, color=GOLD),
            MathTex(r"\text{area} = y(t)", font_size=26, color=GREEN_C),
        ).arrange(RIGHT, buff=0.35).next_to(top, UP, buff=0.12).align_to(top, LEFT)

        self.play(Create(top), Create(bot), FadeIn(tick))
        self.play(Create(x_graph), FadeIn(legend[0]))
        self.play(FadeIn(h_graph), FadeIn(t_line), FadeIn(t_mark), FadeIn(legend[1]))
        flip = Tex(r"flip $h$, slide it to $t$,\\multiply, and add up the area", font_size=32, color=GREY_A)
        flip.move_to(RIGHT * 3.75 + UP * 0.6)
        self.add(area, prod, y_m, y_dot)
        self.play(FadeIn(legend[2]), FadeIn(ylab), FadeIn(flip))
        self.play(t.animate.set_value(0.0), run_time=1.5, rate_func=linear)
        self.play(t.animate.set_value(1.0), run_time=5, rate_func=linear)
        self.play(t.animate.set_value(3.8), run_time=4.5, rate_func=linear)
        self.wait(0.5)

        # ------------------------------------------------ right: s-domain
        box = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.1, color=GREY_B)
        hs = MathTex("H(s)", font_size=32).move_to(box)
        xin = MathTex("X(s)", font_size=32, color=SIG).next_to(box, LEFT, buff=0.9)
        yout = MathTex("Y(s)", font_size=32, color=YELLOW).next_to(box, RIGHT, buff=0.9)
        a1 = Arrow(xin.get_right(), box.get_left(), buff=0.1, stroke_width=3)
        a2 = Arrow(box.get_right(), yout.get_left(), buff=0.1, stroke_width=3)
        diagram = VGroup(box, hs, xin, yout, a1, a2).move_to(RIGHT * 3.75 + UP * 2.25)

        steps = VGroup(
            MathTex(r"X(s) = \frac{1}{s+2},\quad H(s) = \frac{1}{s+3}", font_size=30),
            MathTex(r"Y(s) = X(s)\,H(s) = \frac{1}{(s+2)(s+3)}", font_size=30),
            MathTex(r"= \frac{1}{s+2} - \frac{1}{s+3}", font_size=30),
            MathTex(r"y(t) = \big(e^{-2t} - e^{-3t}\big)u(t)", font_size=32, color=YELLOW),
        ).arrange(DOWN, buff=0.22).next_to(diagram, DOWN, buff=0.4)
        steps[2].align_to(steps[1], LEFT).shift(RIGHT * 1.1)

        self.play(FadeIn(diagram), FadeOut(flip))
        for st in steps:
            self.play(Write(st), run_time=1.2)
        self.wait(0.5)

        exact = DashedVMobject(clipped_graph(bot, y_exact, 0.001, 4, color=RED_B, stroke_width=4)[0], num_dashes=45)
        match = Tex(r"same curve --- one multiplication\\replaced the whole sliding integral", font_size=30, color=GOOD)
        match.next_to(steps, DOWN, buff=0.25)
        self.play(TransformFromCopy(steps[3], exact), run_time=2)
        self.play(FadeIn(match))
        self.wait(1)
        roc = MathTex(r"\text{ROC} \supseteq R_1 \cap R_2:\ \mathrm{Re}\{s\} > -2", font_size=30, color=BLUE_B).next_to(match, DOWN, buff=0.15)
        self.play(FadeIn(roc))
        self.wait(2.5)
        fade_all(self)
