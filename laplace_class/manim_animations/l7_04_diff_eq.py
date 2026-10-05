"""Lecture 7 - Differential equations and system models.

Scenes:
  ODEBecomesAlgebra  dy/dt + 3y = x  ->  sY + 3Y = X  ->  H(s) = 1/(s+3); drive it with e^{-2t}u(t)
                     and solve by partial fractions; then the general LCCDE -> rational H(s).
  SpringMassPoles    y'' + mu y' + 4y = 0: as the damping mu changes, the two poles slide around
                     the s-plane and the mass on the spring moves exactly as the poles predict.
                     (Same physics as 3Blue1Brown's Laplace prelude.)
"""
from common import *


class ODEBecomesAlgebra(Scene):
    def construct(self):
        title = make_title(r"Differential equations become algebra")
        self.play(Write(title))

        # ---------------------------------------------- d/dt -> s
        eq_t = MathTex(r"\frac{dy(t)}{dt}", r"+", r"3", r"y(t)", r"=", r"x(t)", font_size=54).move_to(UP * 1.75)
        eq_s = MathTex(r"s", r"Y(s)", r"+", r"3", r"Y(s)", r"=", r"X(s)", font_size=54).move_to(DOWN * 0.15)
        eq_t[0].set_color(GOLD)
        eq_s[0].set_color(YELLOW)
        arrow = Arrow(eq_t.get_bottom(), eq_s.get_top(), buff=0.2, color=GREY_B)
        arrow_lab = Tex(r"$\mathcal{L}$, zero initial conditions", font_size=28, color=GREY_A).next_to(arrow, RIGHT, buff=0.15)
        self.play(Write(eq_t))
        self.play(GrowArrow(arrow), FadeIn(arrow_lab))
        self.play(
            TransformFromCopy(eq_t[0], VGroup(eq_s[0], eq_s[1])),
            *[TransformFromCopy(eq_t[i], eq_s[i + 1]) for i in range(1, 6)],
            run_time=2,
        )
        rule = Tex(r"every $\frac{d}{dt}$ becomes a factor $s$", font_size=32, color=YELLOW).next_to(eq_s, DOWN, buff=0.35)
        self.play(FadeIn(rule))
        self.wait(1)

        eq_f = MathTex(r"(s+3)\,Y(s) = X(s)", font_size=48).move_to(eq_s)
        self.play(FadeOut(rule), TransformMatchingShapes(eq_s, eq_f))
        Hs = MathTex(r"H(s) = \frac{Y(s)}{X(s)} = \frac{1}{s+3}", font_size=48).next_to(eq_f, DOWN, buff=0.5)
        hbox = SurroundingRectangle(Hs, color=YELLOW, buff=0.15)
        self.play(Write(Hs), Create(hbox))
        self.wait(1.5)

        # ---------------------------------------------- solve for a concrete input
        Hgrp = VGroup(Hs, hbox)
        self.play(FadeOut(VGroup(eq_t, arrow, arrow_lab, eq_f)), Hgrp.animate.scale(0.7).to_corner(UL, buff=0.4).shift(DOWN * 0.7))

        sp = SPlane(x_range=(-4, 1, 1), y_range=(-1.5, 1.5, 1), x_length=4.4, y_length=2.4, number_size=18)
        sp.move_to(RIGHT * 4.2 + UP * 1.55)
        h_pole = sp.pole(-3)
        roc = sp.roc(left=-3, opacity=0.35)
        badge = VGroup(
            VGroup(Tex("causal", font_size=26), check(True, 32)).arrange(RIGHT, buff=0.1),
            VGroup(Tex("stable", font_size=26), check(True, 32)).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.4).next_to(sp, DOWN, buff=0.12)
        self.play(FadeIn(sp), FadeIn(roc), FadeIn(h_pole), FadeIn(badge))

        steps = VGroup(
            MathTex(r"x(t) = e^{-2t}u(t)\ \leftrightarrow\ X(s) = \frac{1}{s+2}", font_size=32, color=SIG),
            MathTex(r"Y(s) = H(s)X(s) = \frac{1}{(s+2)(s+3)}", font_size=32),
            MathTex(r"= \frac{1}{s+2} - \frac{1}{s+3}", font_size=32),
            MathTex(r"y(t) = \big(e^{-2t} - e^{-3t}\big)u(t)", font_size=36, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(Hgrp, DOWN, buff=0.4).align_to(Hgrp, LEFT)
        steps[2].shift(RIGHT * 1.6)

        ax = signal_axes(x_range=(-0.5, 4, 1), y_range=(0, 1.1, 0.5), x_length=6.0, y_length=2.7)
        ax.move_to(RIGHT * 3.6 + DOWN * 2.15)
        x_graph = clipped_graph(ax, lambda t: np.exp(-2 * t) * u(t), -0.5, 4, breaks=[0], color=SIG, stroke_width=4)
        y_graph = clipped_graph(ax, lambda t: (np.exp(-2 * t) - np.exp(-3 * t)) * u(t), -0.5, 4, breaks=[0], color=YELLOW, stroke_width=5)
        legend = VGroup(MathTex("x(t)", font_size=28, color=SIG), MathTex("y(t)", font_size=28, color=YELLOW)).arrange(RIGHT, buff=0.4)
        legend.next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)

        self.play(Write(steps[0]), Create(ax), Create(x_graph), FadeIn(legend[0]))
        x_pole = sp.pole(-2, color=SIG)
        self.play(FadeIn(x_pole, scale=2))
        self.play(Write(steps[1]))
        self.play(Write(steps[2]))
        self.play(Write(steps[3]), Create(y_graph), FadeIn(legend[1]), run_time=2)
        self.wait(2)

        # ---------------------------------------------- the general LCCDE
        fade_all(self, run_time=0.8)
        title2 = make_title(r"Any linear constant-coefficient DE does the same")
        lines = VGroup(
            MathTex(r"\sum_{k=0}^{N} a_k \frac{d^k y(t)}{dt^k}", r"=", r"\sum_{k=0}^{M} b_k \frac{d^k x(t)}{dt^k}", font_size=40),
            MathTex(r"\Big(\sum_{k=0}^{N} a_k s^k\Big) Y(s)", r"=", r"\Big(\sum_{k=0}^{M} b_k s^k\Big) X(s)", font_size=40),
            MathTex(r"H(s) = \frac{Y(s)}{X(s)}", r"=", r"\frac{\sum_{k=0}^{M} b_k s^k}{\sum_{k=0}^{N} a_k s^k}", font_size=44),
        ).arrange(DOWN, buff=0.55).next_to(title2, DOWN, buff=0.5)
        for l in lines[1:]:
            l.shift(RIGHT * (lines[0][1].get_x() - l[1].get_x()))
        self.play(Write(title2))
        self.play(Write(lines[0]))
        self.play(TransformFromCopy(lines[0], lines[1]), run_time=1.5)
        self.play(TransformFromCopy(lines[1], lines[2]), run_time=1.5)
        box = SurroundingRectangle(lines[2], color=YELLOW, buff=0.15)
        notes = VGroup(
            Tex(r"numerator roots $\Rightarrow$ zeros \quad denominator roots $\Rightarrow$ poles", font_size=30),
            Tex(r"the DE fixes the formula; causality (or stability) picks the ROC", font_size=30, color=BLUE_B),
        ).arrange(DOWN, buff=0.2).next_to(box, DOWN, buff=0.35)
        self.play(Create(box), FadeIn(notes[0]))
        self.play(FadeIn(notes[1]))
        self.wait(3)
        fade_all(self)


# ---------------------------------------------------------------------------
K = 4.0          # spring constant (m = 1) -> natural frequency 2
T_MAX = 8.0


def roots(mu):
    d = np.sqrt(complex(mu * mu - 4 * K))
    return (-mu + d) / 2, (-mu - d) / 2


def response(mu, t):
    """Free response with y(0) = 1, y'(0) = 0 of y'' + mu y' + K y = 0."""
    r1, r2 = roots(mu)
    t = np.asarray(t, dtype=float)
    if abs(r1 - r2) < 1e-6:
        r = r1.real
        return np.exp(r * t) * (1 - r * t)
    return ((r1 * np.exp(r2 * t) - r2 * np.exp(r1 * t)) / (r1 - r2)).real


def regime(mu):
    if mu < -1e-3:
        return r"negative damping: poles in the RHP $\Rightarrow$ unstable", BAD
    if abs(mu) <= 1e-3:
        return r"no damping: poles on the $j\omega$-axis, rings forever", JW_COLOR
    if mu < 4 - 1e-3:
        return r"underdamped: complex pair $\Rightarrow$ decaying oscillation", BLUE_B
    if mu <= 4 + 1e-3:
        return r"critically damped: the poles collide at $s=-2$", GOLD
    return r"overdamped: two real poles $\Rightarrow$ no oscillation", GREEN_B


class SpringMassPoles(Scene):
    def construct(self):
        title = make_title(r"A mass on a spring: the poles choreograph the motion")
        self.play(Write(title))

        mu = ValueTracker(0.8)
        tc = ValueTracker(0.0)

        # ---------------------------------------------- equations (top left)
        eqs = VGroup(
            MathTex(r"\ddot y + \mu\,\dot y + 4y = 0,\quad y(0)=1", font_size=32),
            MathTex(r"\xrightarrow{\ \mathcal{L}\ }\ (s^2 + \mu s + 4)\,Y(s) = s + \mu", font_size=32),
            MathTex(r"\text{poles: } s = \frac{-\mu \pm \sqrt{\mu^2 - 16}}{2}", font_size=32, color=POLE_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UL, buff=0.4).shift(DOWN * 0.75)

        # ---------------------------------------------- s-plane (bottom left)
        sp = SPlane(x_range=(-5, 1, 1), y_range=(-3, 3, 1), x_length=4.0, y_length=3.5, number_size=16)
        sp.next_to(eqs, DOWN, buff=0.3).align_to(eqs, LEFT)
        circle = Circle(radius=2 * sp.unit(), color=GREY_B, stroke_width=1.5).move_to(sp.c2p(0, 0))
        circle.stretch(sp.plane.get_y_unit_size() / sp.unit(), 1)
        circle = DashedVMobject(circle, num_dashes=40)
        lhp = sp.roc(right=0, color=GREEN_E, opacity=0.2, boundary=False)

        poles = always_redraw(lambda: VGroup(*[sp.pole(r, size=0.14) for r in roots(mu.get_value())]))

        # ---------------------------------------------- apparatus (top right)
        wall_x, floor_y, X0, AMP = 0.9, 1.15, 4.0, 1.35
        wall = VGroup(Line([wall_x, floor_y, 0], [wall_x, floor_y + 1.1, 0], stroke_width=4),
                      *[Line([wall_x, floor_y + 0.12 * i, 0], [wall_x - 0.15, floor_y + 0.12 * i - 0.12, 0], stroke_width=2)
                        for i in range(1, 10)]).set_color(GREY_B)
        floor = Line([wall_x, floor_y, 0], [6.9, floor_y, 0], color=GREY_B, stroke_width=3)
        eq_mark = DashedLine([X0, floor_y - 0.15, 0], [X0, floor_y + 1.05, 0], color=GREY_C, stroke_width=1.5)

        def block_x():
            y = float(response(mu.get_value(), tc.get_value()))
            return X0 + AMP * np.clip(y, -1.25, 1.25)

        def spring_mob():
            x1 = block_x() - 0.45
            yc = floor_y + 0.38
            n, amp, lead = 9, 0.17, 0.15
            pts = [np.array([wall_x, yc, 0]), np.array([wall_x + lead, yc, 0])]
            L = x1 - wall_x - 2 * lead
            for i in range(1, 2 * n):
                pts.append(np.array([wall_x + lead + L * i / (2 * n), yc + amp * (1 if i % 2 else -1), 0]))
            pts += [np.array([x1 - lead, yc, 0]), np.array([x1, yc, 0])]
            return VMobject().set_points_as_corners(pts).set_stroke(GREY_A, 3)

        def block_mob():
            b = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.06, fill_color=BLUE_D, fill_opacity=1,
                                 stroke_color=BLUE_B, stroke_width=3)
            b.move_to([block_x(), floor_y + 0.38, 0])
            return VGroup(b, MathTex("m", font_size=30).move_to(b))

        spring = always_redraw(spring_mob)
        block = always_redraw(block_mob)

        # ---------------------------------------------- response graph (bottom right)
        ax = signal_axes(x_range=(0, T_MAX, 1), y_range=(-1.3, 1.3, 1), x_length=6.3, y_length=2.8, y_label="y(t)")
        ax.move_to(RIGHT * 3.35 + DOWN * 1.9)
        ts = np.linspace(0, T_MAX, 500)
        curve = always_redraw(lambda: clipped_polyline(ax, ts, response(mu.get_value(), ts), color=YELLOW, stroke_width=4))
        cursor = always_redraw(lambda: Dot(
            ax.c2p(tc.get_value(), float(np.clip(response(mu.get_value(), tc.get_value()), -1.3, 1.3))), color=WHITE, radius=0.06))

        mu_num = DecimalNumber(0.8, num_decimal_places=2, include_sign=True, font_size=32)
        mu_num.add_updater(lambda m: m.set_value(mu.get_value()))
        mu_read = VGroup(MathTex(r"\mu =", font_size=32), mu_num).arrange(RIGHT, buff=0.1).move_to(RIGHT * 1.6 + UP * 2.75)
        reg = always_redraw(lambda: Tex(regime(mu.get_value())[0], font_size=28, color=regime(mu.get_value())[1])
                            .next_to(ax, DOWN, buff=0.15))

        self.play(FadeIn(eqs[0]))
        self.play(FadeIn(eqs[1]))
        self.play(FadeIn(eqs[2]))
        self.play(FadeIn(sp), FadeIn(lhp), Create(circle), FadeIn(poles))
        self.play(FadeIn(wall), Create(floor), FadeIn(eq_mark), FadeIn(spring), FadeIn(block), Create(ax), FadeIn(mu_read))
        self.add(curve, cursor, reg)

        def tick(m, dt):
            m.set_value((m.get_value() + dt) % T_MAX)

        tc.add_updater(tick)
        self.add(tc)
        self.wait(6)

        for target, rt, hold in [(0.0, 3, 4), (1.8, 3, 2), (4.0, 3, 3), (5.0, 2.5, 3), (-0.4, 4, 4), (1.2, 3, 2)]:
            self.play(mu.animate.set_value(target), run_time=rt)
            self.wait(hold)

        tc.clear_updaters()
        moral = Tex(r"left/right position of the poles $\Rightarrow$ decay/growth;\quad height $\Rightarrow$ how fast it wiggles",
                    font_size=30, color=YELLOW).move_to(title)
        self.play(FadeTransform(title, moral))
        self.wait(2.5)
        fade_all(self)
