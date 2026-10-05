"""Lecture 6 - The Laplace transform definition and its link to Fourier.

Scenes:
  LaplaceAsWeightedFourier  X(sigma + j omega) = F{ x(t) e^{-sigma t} }: the weight tames a
                            signal whose Fourier transform does not exist.
  IntegralAsSpiral          the integral of e^{-st} drawn as tip-to-tail vectors spiralling
                            into the point 1/s (only when Re{s} > 0).
"""
from common import *


class LaplaceAsWeightedFourier(Scene):
    def construct(self):
        # ------------------------------------------------ the algebra
        eq1 = MathTex(r"X(s)", r"=", r"\int_{-\infty}^{\infty} x(t)\, e^{-st}\,dt", font_size=50)
        self.play(Write(eq1))
        self.wait(0.6)
        sub = MathTex(r"s = \sigma + j\omega", font_size=40, color=GREY_A).next_to(eq1, DOWN, buff=0.5)
        self.play(FadeIn(sub, shift=UP * 0.2))

        eq2 = MathTex(
            r"X(\sigma + j\omega)", r"=", r"\int_{-\infty}^{\infty}", r"\big[x(t)\,e^{-\sigma t}\big]",
            r"\,e^{-j\omega t}\,dt", font_size=50,
        )
        eq2[3].set_color(PROD)
        self.play(
            ReplacementTransform(eq1[0], eq2[0]), ReplacementTransform(eq1[1], eq2[1]),
            ReplacementTransform(eq1[2], VGroup(*eq2[2:])), FadeOut(sub),
        )
        eq3 = MathTex(r"=\ \mathcal{F}\big\{", r"x(t)\,e^{-\sigma t}", r"\big\}", font_size=50)
        eq3[1].set_color(PROD)
        eq3.next_to(eq2, DOWN, buff=0.4).align_to(eq2[1], LEFT)
        self.play(Write(eq3))
        box = SurroundingRectangle(VGroup(eq2, eq3), color=YELLOW, buff=0.2, corner_radius=0.1)
        key = Tex(r"Laplace $=$ Fourier transform of a \emph{tamed} version of $x(t)$", font_size=34, color=YELLOW)
        key.next_to(box, DOWN, buff=0.3)
        self.play(Create(box), FadeIn(key))
        self.wait(1.5)
        header = VGroup(eq2, eq3, box)
        self.play(FadeOut(key), header.animate.scale(0.62).to_edge(UP, buff=0.2))

        # ------------------------------------------------ the picture
        sigma = ValueTracker(0.0)
        A = 0.5  # x(t) = e^{A t} u(t)

        ax = signal_axes(x_range=(-1, 6, 1), y_range=(0, 3, 1), x_length=7.2, y_length=4.0)
        ax.move_to(LEFT * 2.8 + DOWN * 1.75)
        splane = SPlane(x_range=(-2, 2, 1), y_range=(-2, 2, 1), x_length=3.6, y_length=3.6)
        splane.move_to(RIGHT * 4.6 + DOWN * 0.55)
        s_title = Tex(r"$s$-plane", font_size=30).next_to(splane, UP, buff=0.1)

        x_graph = clipped_graph(ax, lambda t: np.exp(A * t) * u(t), -1, 6, breaks=[0], color=SIG)
        x_lab = MathTex(r"x(t) = e^{0.5t}u(t)", font_size=32, color=SIG)
        x_lab.next_to(ax, UP, buff=1.05).align_to(ax, LEFT)
        no_ft = MathTex(r"\int |x(t)|\,dt = \infty \ \Rightarrow\ \text{no Fourier transform}", font_size=30, color=BAD)
        no_ft.next_to(x_lab, RIGHT, buff=0.4)

        self.play(Create(ax), FadeIn(splane), FadeIn(s_title))
        self.play(Create(x_graph), FadeIn(x_lab))
        self.play(FadeIn(no_ft))
        self.wait(1)

        pole = splane.pole(A)
        pole_lab = MathTex(r"0.5", font_size=24, color=POLE_COLOR).next_to(pole, DR, buff=0.02)

        weight = always_redraw(lambda: clipped_graph(
            ax, lambda t: np.exp(-sigma.get_value() * t), 0, 6, color=WEIGHT, stroke_width=3, opacity=0.8))
        prod = always_redraw(lambda: clipped_graph(
            ax, lambda t: np.exp((A - sigma.get_value()) * t) * u(t), -1, 6, breaks=[0], color=PROD, stroke_width=5))
        area = always_redraw(lambda: clipped_area(
            ax, lambda t: np.exp((A - sigma.get_value()) * t), 0, 6, color=PROD, opacity=0.25))

        w_lab = MathTex(r"e^{-\sigma t}", font_size=32, color=WEIGHT)
        p_lab = MathTex(r"x(t)\,e^{-\sigma t}", font_size=32, color=PROD)
        legend = VGroup(w_lab, p_lab).arrange(RIGHT, buff=0.5).next_to(x_lab, DOWN, aligned_edge=LEFT, buff=0.2)

        sig_num = DecimalNumber(0, num_decimal_places=2, font_size=34)
        sig_num.add_updater(lambda m: m.set_value(sigma.get_value()))
        sig_read = VGroup(MathTex(r"\sigma =", font_size=34), sig_num).arrange(RIGHT, buff=0.12)
        sig_read.next_to(splane, DOWN, buff=0.25)

        def area_readout():
            s = sigma.get_value()
            lhs = MathTex(r"\int_0^\infty x(t)e^{-\sigma t}dt =", font_size=30)
            if s <= A + 1e-3:
                rhs = MathTex(r"\infty", font_size=34, color=BAD)
            else:
                rhs = DecimalNumber(1 / (s - A), num_decimal_places=2, font_size=30, color=GOOD)
            return VGroup(lhs, rhs).arrange(RIGHT, buff=0.12).next_to(sig_read, DOWN, buff=0.2)

        area_read = always_redraw(area_readout)

        def test_line():
            s = sigma.get_value()
            col = GOOD if s > A + 1e-3 else BAD
            return splane.vline(s, color=col, width=5)

        line = always_redraw(test_line)

        self.play(FadeIn(pole), FadeIn(pole_lab))
        self.play(FadeIn(weight), FadeIn(legend), FadeIn(sig_read))
        self.add(area, prod, x_graph)
        self.play(FadeIn(prod), FadeIn(area), Create(line), FadeIn(area_read))
        self.wait(0.5)

        for target, rt in [(0.3, 2.5), (0.5, 2), (1.2, 3.5), (0.75, 2), (1.6, 2.5)]:
            self.play(sigma.animate.set_value(target), run_time=rt)
            self.wait(0.4)

        roc = splane.roc(left=A, opacity=0.4)
        roc_lab = Tex("ROC", font_size=30, color=BLUE_B).move_to(splane.c2p(1.35, 1.5))
        concl = Tex(r"ROC: $\mathrm{Re}\{s\} > 0.5$ --- every line in it tames $x(t)$", font_size=30, color=BLUE_B)
        concl.move_to(no_ft, aligned_edge=LEFT)
        self.play(FadeIn(roc), FadeIn(roc_lab))
        jw = splane.jw_axis(width=4)
        self.play(Create(jw))
        self.play(FadeTransform(no_ft, concl))
        self.wait(2.5)
        fade_all(self)


class IntegralAsSpiral(Scene):
    def construct(self):
        title = MathTex(
            r"\mathcal{L}\{u(t)\}", r"=", r"\int_0^{\infty} e^{-st}\,dt", font_size=48,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        sig = ValueTracker(0.3)
        om = ValueTracker(1.0)

        def s_val():
            return complex(sig.get_value(), om.get_value())

        # ------------------------------------------------ planes
        splane = SPlane(x_range=(-1, 1, 0.5), y_range=(-2, 2, 1), x_length=2.6, y_length=4.4, number_size=18)
        splane.move_to(LEFT * 5.4 + DOWN * 0.5)
        s_title = Tex(r"$s$-plane", font_size=28).next_to(splane, UP, buff=0.1)
        s_dot = always_redraw(lambda: Dot(splane.s2p(s_val()), color=YELLOW, radius=0.08))
        s_lab = always_redraw(lambda: MathTex("s", font_size=30, color=YELLOW).next_to(s_dot, UR, buff=0.02))

        XL, YL = (-1.5, 2.0), (-2.5, 1.0)
        cplane = NumberPlane(
            x_range=(*XL, 1), y_range=(*YL, 1), x_length=5.4, y_length=5.4,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.7},
            axis_config={"stroke_color": GREY_B},
        ).move_to(RIGHT * 3.3 + DOWN * 0.55)
        c_title = Tex("complex plane", font_size=28, color=GREY_A).next_to(cplane, UP, buff=0.1)
        one = MathTex("1", font_size=24, color=GREY_A).next_to(cplane.c2p(1, 0), DOWN + RIGHT * 0.3, buff=0.06)

        def c2p(z):
            return cplane.c2p(z.real, z.imag)

        self.play(FadeIn(splane), FadeIn(s_title), FadeIn(cplane), FadeIn(c_title), FadeIn(one))
        self.play(FadeIn(s_dot, scale=2), FadeIn(s_lab))

        # ------------------------------------------------ 1. the integrand spins and shrinks
        integrand = MathTex(r"e^{-st}", r"=", r"e^{-\sigma t}", r"\,e^{-j\omega t}", font_size=40)
        integrand[2].set_color(RED_B)
        integrand[3].set_color(TEAL_C)
        integrand.move_to(LEFT * 1.75 + UP * 2.1)
        notes = VGroup(
            Tex("shrinks", font_size=26, color=RED_B).next_to(integrand[2], DOWN, buff=0.15),
            Tex("spins", font_size=26, color=TEAL_C).next_to(integrand[3], DOWN, buff=0.15),
        )
        self.play(Write(integrand), FadeIn(notes))

        t = ValueTracker(0.0)
        vec = always_redraw(lambda: Arrow(
            c2p(0), c2p(np.exp(-s_val() * t.get_value())), buff=0, color=SIG, stroke_width=5,
            max_tip_length_to_length_ratio=0.2,
        ))
        tip_trace = always_redraw(lambda: VMobject() if t.get_value() < 0.02 else clipped_path(
            [(z.real, z.imag) for z in np.exp(-s_val() * np.linspace(0, t.get_value(), 200))],
            cplane.c2p, XL, YL, color=SIG, stroke_width=2,
        ).set_stroke(opacity=0.5))
        self.add(tip_trace, vec)
        self.play(t.animate.set_value(10), run_time=5, rate_func=linear)
        self.wait(0.3)
        self.play(FadeOut(vec), FadeOut(tip_trace))

        # ------------------------------------------------ 2. Riemann sum, tip to tail
        riemann = MathTex(r"\int_0^{\infty} e^{-st}dt \approx \sum_k e^{-s t_k}\,\Delta t", font_size=34)
        riemann.next_to(integrand, DOWN, buff=0.7).set_x(-1.75)
        self.play(Write(riemann))

        dt, N = 0.3, 45
        s0 = s_val()
        arrows = VGroup()
        pos = 0j
        for k in range(N):
            step = np.exp(-s0 * k * dt) * dt
            col = interpolate_color(BLUE_B, BLUE_E, k / N)
            arrows.add(Arrow(c2p(pos), c2p(pos + step), buff=0, color=col, stroke_width=3,
                             max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=10))
            pos += step
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=6)

        target = always_redraw(lambda: Dot(c2p(1 / s_val()), color=YELLOW if sig.get_value() > 0 else BAD, radius=0.09))
        target_lab = always_redraw(lambda: MathTex(r"1/s" if sig.get_value() > 0 else r"1/s\ (\text{never reached})",
                                                   font_size=32, color=YELLOW if sig.get_value() > 0 else BAD)
                                   .next_to(target, RIGHT, buff=0.1))
        self.play(FadeIn(target, scale=2), FadeIn(target_lab))
        self.wait(1)

        # ------------------------------------------------ 3. the smooth running integral
        running = MathTex(r"\int_0^{T} e^{-st}dt", r"=", r"\frac{1 - e^{-sT}}{s}", font_size=34)
        running.next_to(riemann, DOWN, buff=0.4).set_x(-1.75)
        limit = MathTex(r"\xrightarrow{\,T\to\infty\,}\ \frac{1}{s}", r"\quad\text{if } \mathrm{Re}\{s\} > 0", font_size=34)
        limit[1].set_color(YELLOW)
        limit.next_to(running, DOWN, buff=0.3).set_x(-1.75)

        def spiral():
            s = s_val()
            Ts = np.linspace(0, 30, 900)
            zs = (1 - np.exp(-s * Ts)) / s
            return clipped_path([(z.real, z.imag) for z in zs], cplane.c2p, XL, YL, color=SIG, stroke_width=4)

        spiral_m = always_redraw(spiral)
        self.play(FadeOut(arrows, lag_ratio=0.02), Create(spiral_m), Write(running), run_time=2.5)
        self.play(Write(limit))
        self.wait(1)

        # ------------------------------------------------ 4. move s around
        sig_num = DecimalNumber(0.3, num_decimal_places=2, include_sign=True, font_size=28)
        sig_num.add_updater(lambda m: m.set_value(sig.get_value()))
        sig_read = VGroup(MathTex(r"\sigma =", font_size=28), sig_num).arrange(RIGHT, buff=0.1)
        sig_read.next_to(splane, DOWN, buff=0.2)
        self.play(FadeIn(sig_read))
        for s_, o_ in [(0.6, 0.8), (1.0, 0.0), (0.5, -0.9), (0.1, 1.0), (0.02, 1.0)]:
            self.play(sig.animate.set_value(s_), om.animate.set_value(o_), run_time=2)
            self.wait(0.3)
        warn = Tex(r"$\sigma \to 0$: it just circles forever", font_size=30, color=ORANGE)
        warn.next_to(limit, DOWN, buff=0.35).set_x(-1.75)
        self.play(FadeIn(warn))
        self.wait(1)
        self.play(sig.animate.set_value(-0.06), run_time=2)
        warn2 = Tex(r"$\sigma < 0$: spirals outward, the integral diverges", font_size=30, color=BAD)
        warn2.move_to(warn)
        self.play(FadeTransform(warn, warn2))
        self.wait(1.2)

        roc = splane.roc(left=0, opacity=0.45)
        self.play(FadeIn(roc), sig.animate.set_value(0.4), om.animate.set_value(0.6), FadeOut(warn2), run_time=2)
        result = MathTex(r"u(t)\ \xleftrightarrow{\ \mathcal{L}\ }\ \frac{1}{s},\quad \mathrm{Re}\{s\} > 0", font_size=36)
        result.move_to(warn2).shift(DOWN * 0.3)
        rbox = SurroundingRectangle(result, color=YELLOW, buff=0.15)
        self.play(Write(result), Create(rbox))
        self.wait(2.5)
        fade_all(self)
