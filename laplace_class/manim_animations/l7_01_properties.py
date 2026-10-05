"""Lecture 7 - Properties of the Laplace transform.

Scenes:
  PropertiesOnSPlane          time shift, s-shift, time scaling, time reversal, conjugation:
                              watch what each one does to the signal AND to the pole/ROC picture.
  DerivativeMeansMultiplyByS  d/dt e^{st} = s e^{st} (velocity = s x position), so d/dt <-> s;
                              u(t) -> delta(t): the zero from s cancels the pole at 0.
  RepeatedPoles               -t x(t) <-> dX/ds:  t^{n-1}e^{-at}/(n-1)! <-> 1/(s+a)^n (Ex. 9.14),
                              and integration <-> 1/s.
"""
from common import *


class PropertiesOnSPlane(Scene):
    def construct(self):
        self.ax = signal_axes(x_range=(-4, 4, 1), y_range=(-1, 2, 1), x_length=6.2, y_length=3.9)
        self.ax.move_to(LEFT * 3.4 + DOWN * 1.0)
        self.sp = SPlane(x_range=(-3, 3, 1), y_range=(-2, 2, 1), x_length=5.0, y_length=3.4)
        self.sp.move_to(RIGHT * 3.65 + DOWN * 1.0)
        base = MathTex(r"x(t) = e^{-t}u(t)\ \xleftrightarrow{\ \mathcal{L}\ }\ \frac{1}{s+1},\ \ \mathrm{Re}\{s\} > -1",
                       font_size=34, color=GREY_A).move_to(UP * 2.55)
        self.title = make_title("Properties: what happens on the $s$-plane?")
        self.play(Write(self.title))
        self.play(Create(self.ax), FadeIn(self.sp), FadeIn(base))
        self.ghost = clipped_graph(self.ax, lambda t: np.exp(-t) * u(t), -4, 4, breaks=[0], color=SIG, stroke_width=3, opacity=0.3)
        self.play(Create(self.ghost))
        self.base = base
        self.formula = None
        self.note = None
        self.cur_stage = []

        self.time_shift()
        self.s_shift()
        self.time_scaling()
        self.time_reversal()
        self.conjugation()
        fade_all(self)

    # ------------------------------------------------------------------ helpers
    def set_text(self, title, formula, note=None, note_color=YELLOW):
        anims = []
        new_title = make_title(title)
        anims.append(FadeTransform(self.title, new_title))
        self.title = new_title
        new_formula = MathTex(formula, font_size=40).move_to(UP * 2.2)
        if self.formula is None:
            anims.append(FadeOut(self.base))
            anims.append(Write(new_formula))
        else:
            anims.append(FadeTransform(self.formula, new_formula))
        self.formula = new_formula
        if self.note is not None:
            anims.append(FadeOut(self.note))
            self.note = None
        self.play(*anims)
        if note:
            self.show_note(note, note_color)

    def show_note(self, text, color=YELLOW):
        new = Tex(text, font_size=30, color=color).to_edge(DOWN, buff=0.3).set_x(0)
        if self.note is None:
            self.play(FadeIn(new, shift=UP * 0.2))
        else:
            self.play(FadeTransform(self.note, new))
        self.note = new

    def stage(self, f_of_t, pole_of, roc_of, breaks_of=lambda: [0]):
        graph = always_redraw(lambda: clipped_graph(self.ax, f_of_t(), -4, 4, breaks=breaks_of(), color=SIG))
        poles = always_redraw(lambda: VGroup(*[self.sp.pole(p) for p in pole_of()]))
        roc = always_redraw(lambda: self.sp.roc(**roc_of(), opacity=0.4))
        return graph, poles, roc

    def freeze(self, *mobs):
        for m in mobs:
            m.clear_updaters()

    def swap_stage(self, *new):
        """Replace the (frozen) previous picture by a new one that starts out identical."""
        self.remove(*self.cur_stage)
        self.add(*new)
        self.cur_stage = list(new)

    # ------------------------------------------------------------------ sections
    def time_shift(self):
        self.set_text("Time shifting", r"x(t - t_0)\ \xleftrightarrow{\ \mathcal{L}\ }\ e^{-st_0}X(s)")
        t0 = ValueTracker(0.0)
        g, p, r = self.stage(
            lambda: (lambda t: np.exp(-(t - t0.get_value())) * u(t - t0.get_value())),
            lambda: [-1], lambda: dict(left=-1), lambda: [t0.get_value()],
        )
        self.play(Create(g), FadeIn(p), FadeIn(r))
        self.cur_stage = [g, p, r]
        self.play(t0.animate.set_value(2.0), run_time=2.5)
        self.show_note(r"delay changes the phase only --- poles and ROC stay put", GOOD)
        self.play(t0.animate.set_value(-1.0), run_time=2)
        self.play(t0.animate.set_value(0.0), run_time=1.5)
        self.freeze(g, p, r)

    def s_shift(self):
        self.set_text("Shifting in the $s$-domain", r"e^{s_0 t}x(t)\ \xleftrightarrow{\ \mathcal{L}\ }\ X(s - s_0)",
                      r"multiplying by $e^{s_0 t}$ slides the whole picture by $\mathrm{Re}\{s_0\}$")
        s0 = ValueTracker(0.0)
        g, p, r = self.stage(
            lambda: (lambda t: np.exp((s0.get_value() - 1) * t) * u(t)),
            lambda: [-1 + s0.get_value()], lambda: dict(left=-1 + s0.get_value()),
        )
        self.swap_stage(r, p, g)
        num = DecimalNumber(0, num_decimal_places=2, include_sign=True, font_size=32)
        num.add_updater(lambda m: m.set_value(s0.get_value()))
        read = VGroup(MathTex("s_0 =", font_size=32), num).arrange(RIGHT, buff=0.1).next_to(self.sp, UP, buff=0.1).align_to(self.sp, RIGHT)
        self.play(FadeIn(read))
        self.play(s0.animate.set_value(0.6), run_time=2)
        self.play(s0.animate.set_value(1.5), run_time=2.5)
        self.show_note(r"pole crosses into the right half-plane $\Rightarrow$ $e^{0.5t}u(t)$ grows", BAD)
        self.play(s0.animate.set_value(-1.0), run_time=3)
        self.show_note(r"slide left $\Rightarrow$ the signal decays faster", GOOD)
        self.play(s0.animate.set_value(0.0), run_time=1.5)
        num.clear_updaters()
        self.play(FadeOut(read))
        self.freeze(g, p, r)

    def time_scaling(self):
        self.set_text("Time scaling", r"x(at)\ \xleftrightarrow{\ \mathcal{L}\ }\ \frac{1}{|a|}X\!\left(\frac{s}{a}\right),\quad \text{ROC} = aR",
                      r"$e^{-at}u(t) \leftrightarrow \frac{1}{s+a}$: squeeze in time $\Rightarrow$ stretch in $s$")
        a = ValueTracker(1.0)
        g, p, r = self.stage(
            lambda: (lambda t: np.exp(-a.get_value() * t) * u(t)),
            lambda: [-a.get_value()], lambda: dict(left=-a.get_value()),
        )
        self.swap_stage(r, p, g)
        num = DecimalNumber(1, num_decimal_places=2, font_size=32)
        num.add_updater(lambda m: m.set_value(a.get_value()))
        read = VGroup(MathTex("a =", font_size=32), num).arrange(RIGHT, buff=0.1).next_to(self.sp, UP, buff=0.1).align_to(self.sp, RIGHT)
        self.play(FadeIn(read))
        self.play(a.animate.set_value(2.5), run_time=2.5)
        self.play(a.animate.set_value(0.4), run_time=3)
        self.play(a.animate.set_value(1.0), run_time=1.5)
        num.clear_updaters()
        self.play(FadeOut(read))
        self.freeze(g, p, r)

    def time_reversal(self):
        self.set_text("Time reversal", r"x(-t)\ \xleftrightarrow{\ \mathcal{L}\ }\ X(-s),\quad \text{ROC} = -R")
        graph = clipped_graph(self.ax, lambda t: np.exp(-t) * u(t), -4, 4, breaks=[0], color=SIG)
        pole = self.sp.pole(-1)
        roc = self.sp.roc(left=-1, opacity=0.4)
        self.swap_stage(roc, pole, graph)
        self.play(
            Rotate(graph, PI, axis=UP, about_point=self.ax.c2p(0, 0)),
            Rotate(VGroup(roc, pole), PI, axis=UP, about_point=self.sp.c2p(0, 0)),
            run_time=3,
        )
        res = MathTex(r"e^{t}u(-t)\ \leftrightarrow\ \frac{1}{1-s},\quad \mathrm{Re}\{s\} < 1", font_size=32, color=YELLOW)
        res.to_edge(DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(res))
        self.note = res
        self.wait(1.5)
        self.play(
            Rotate(graph, -PI, axis=UP, about_point=self.ax.c2p(0, 0)),
            Rotate(VGroup(roc, pole), -PI, axis=UP, about_point=self.sp.c2p(0, 0)),
            run_time=2,
        )

    def conjugation(self):
        self.set_text("Conjugation", r"x^*(t)\ \xleftrightarrow{\ \mathcal{L}\ }\ X^*(s^*)",
                      r"real $x(t)$ $\Rightarrow$ poles/zeros are real or come in conjugate pairs")
        px = ValueTracker(-0.5)
        py = ValueTracker(1.5)
        old = self.cur_stage
        self.play(FadeOut(self.ghost), *[FadeOut(m) for m in old])
        self.cur_stage = []
        g, p, r = self.stage(
            lambda: (lambda t: np.exp(px.get_value() * t) * np.cos(py.get_value() * t) * u(t)),
            lambda: [complex(px.get_value(), py.get_value()), complex(px.get_value(), -py.get_value())],
            lambda: dict(left=px.get_value()),
        )
        link = always_redraw(lambda: DashedLine(
            self.sp.c2p(px.get_value(), py.get_value()), self.sp.c2p(px.get_value(), -py.get_value()),
            color=GREY_B, stroke_width=2, dash_length=0.08))
        labs = always_redraw(lambda: VGroup(
            MathTex("p", font_size=30, color=POLE_COLOR).next_to(self.sp.c2p(px.get_value(), py.get_value()), RIGHT, buff=0.12),
            MathTex("p^*", font_size=30, color=POLE_COLOR).next_to(self.sp.c2p(px.get_value(), -py.get_value()), RIGHT, buff=0.12),
        ))
        sig_lab = MathTex(r"e^{\sigma_p t}\cos(\omega_p t)\,u(t)", font_size=30, color=SIG).next_to(self.ax.c2p(-4, 2), RIGHT, buff=0.2).shift(DOWN * 0.25)
        self.play(FadeIn(r), FadeIn(link), FadeIn(p), FadeIn(labs), Create(g), FadeIn(sig_lab))
        for x_, y_ in [(-0.3, 0.8), (-0.8, 1.9), (-0.25, 1.2)]:
            self.play(px.animate.set_value(x_), py.animate.set_value(y_), run_time=2)
        self.wait(1)
        self.freeze(link, labs, g, p, r)


class DerivativeMeansMultiplyByS(Scene):
    def construct(self):
        self.velocity_picture()
        self.derivative_rule()
        self.step_to_impulse()

    # ------------------------------------------------------------------
    def velocity_picture(self):
        title = make_title(r"Why $\frac{d}{dt}$ turns into multiplication by $s$")
        self.play(Write(title))
        s = complex(-0.08, 1.0)
        S_SCALE = 1.0

        plane = NumberPlane(
            x_range=(-2.5, 2.5, 1), y_range=(-2, 2, 1), x_length=6.25, y_length=5.0,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.6},
            axis_config={"stroke_color": GREY_B},
        ).move_to(RIGHT * 2.9 + DOWN * 0.55)

        sp = SPlane(x_range=(-1.5, 1.5, 1), y_range=(-1.5, 1.5, 1), x_length=3.0, y_length=3.0, number_size=18)
        sp.move_to(LEFT * 4.9 + DOWN * 1.65)
        s_arrow = Arrow(sp.c2p(0, 0), sp.s2p(s * S_SCALE), buff=0, color=YELLOW, stroke_width=5)
        s_lab = MathTex("s", font_size=34, color=YELLOW).next_to(s_arrow.get_end(), UR, buff=0.05)
        s_title = Tex(r"$s$-plane", font_size=28).next_to(sp, UP, buff=0.1)

        eq = MathTex(r"\frac{d}{dt}", r"e^{st}", r"=", r"s", r"\cdot", r"e^{st}", font_size=48)
        eq[1].set_color(SIG)
        eq[5].set_color(SIG)
        eq[3].set_color(YELLOW)
        eq.move_to(LEFT * 4.5 + UP * 1.9)
        words = VGroup(
            Tex("velocity", font_size=28, color=GOLD).next_to(eq[0:2], DOWN, buff=0.2),
            Tex("position", font_size=28, color=SIG).next_to(eq[5], DOWN, buff=0.25),
        )

        self.play(FadeIn(plane), FadeIn(sp), FadeIn(s_title))
        self.play(GrowArrow(s_arrow), FadeIn(s_lab))
        self.play(Write(eq), FadeIn(words))

        t = ValueTracker(0.0)

        def z():
            return np.exp(s * t.get_value())

        def p(w):
            return plane.c2p(w.real, w.imag)

        pos = always_redraw(lambda: Arrow(p(0), p(z()), buff=0, color=SIG, stroke_width=6, max_tip_length_to_length_ratio=0.15))
        vel = always_redraw(lambda: Arrow(p(z()), p(z() + s * z()), buff=0, color=GOLD, stroke_width=6,
                                          max_tip_length_to_length_ratio=0.18))
        trace = always_redraw(lambda: VMobject() if t.get_value() < 0.02 else clipped_path(
            [(w.real, w.imag) for w in np.exp(s * np.linspace(0, t.get_value(), 300))], plane.c2p,
            (-2.5, 2.5), (-2, 2), color=SIG, stroke_width=2).set_stroke(opacity=0.6))
        right_angle = always_redraw(lambda: self.angle_mark(plane, z(), s))
        self.add(trace, pos, vel, right_angle)
        self.play(FadeIn(pos), FadeIn(vel))
        cap = Tex(r"velocity $=$ position rotated by $\angle s$ and scaled by $|s|$", font_size=32, color=GOLD)
        cap.to_edge(DOWN, buff=0.3).shift(RIGHT * 2.5)
        self.play(FadeIn(cap))
        self.play(t.animate.set_value(9), run_time=9, rate_func=linear)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in (plane, sp, s_title, s_arrow, s_lab, words, cap, title)],
                  *[FadeOut(m) for m in (trace, pos, vel, right_angle)], eq.animate.move_to(UP * 2.8))
        for m in (trace, pos, vel, right_angle):
            m.clear_updaters()
        self.eq = eq

    @staticmethod
    def angle_mark(plane, z, s):
        tip = plane.c2p(z.real, z.imag)
        direction = np.array([np.cos(np.angle(z)), np.sin(np.angle(z)), 0.0])
        ext = DashedLine(tip, tip + 0.7 * direction, color=GREY_B, stroke_width=2, dash_length=0.06)
        arc = Arc(radius=0.35, start_angle=np.angle(z), angle=np.angle(s), arc_center=tip,
                  color=YELLOW, stroke_width=3)
        return VGroup(ext, arc)

    # ------------------------------------------------------------------
    def derivative_rule(self):
        l1 = MathTex(r"x(t)", r"=", r"\frac{1}{2\pi j}\int X(s)\,", r"e^{st}", r"\,ds", font_size=42)
        l2 = MathTex(r"\frac{d}{dt}x(t)", r"=", r"\frac{1}{2\pi j}\int X(s)\,", r"s\,e^{st}", r"\,ds", font_size=42)
        l3 = MathTex(r"\frac{d}{dt}x(t)", r"\ \xleftrightarrow{\ \mathcal{L}\ }\ ", r"s", r"X(s)", font_size=48)
        l1[3].set_color(SIG)
        l2[3].set_color(YELLOW)
        l3[2].set_color(YELLOW)
        VGroup(l1, l2).arrange(DOWN, buff=0.45).move_to(UP * 0.55)
        l2.shift(RIGHT * (l1[1].get_x() - l2[1].get_x()))
        l3.next_to(l2, DOWN, buff=0.6)
        self.play(Write(l1))
        self.play(TransformFromCopy(l1, l2), run_time=1.5)
        note = Tex(r"every building block $e^{st}$ just picks up a factor $s$", font_size=32, color=YELLOW).next_to(l3, DOWN, buff=0.4)
        self.play(Write(l3))
        box = SurroundingRectangle(l3, color=YELLOW, buff=0.15)
        self.play(Create(box), FadeIn(note))
        self.wait(1.5)
        why = Tex(r"calculus in time $\Rightarrow$ algebra in $s$", font_size=36, color=GOLD).next_to(note, DOWN, buff=0.3)
        self.play(FadeIn(why, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(VGroup(l1, l2, note, why, self.eq)), VGroup(l3, box).animate.scale(0.8).to_edge(UP, buff=0.3))

    # ------------------------------------------------------------------
    def step_to_impulse(self):
        ax = signal_axes(x_range=(-2, 3, 1), y_range=(0, 1.5, 1), x_length=5.6, y_length=3.4)
        ax.move_to(LEFT * 3.5 + DOWN * 0.9)
        sp = SPlane(x_range=(-2, 2, 1), y_range=(-2, 2, 1), x_length=4.2, y_length=4.2)
        sp.move_to(RIGHT * 3.7 + DOWN * 0.8)
        step = clipped_graph(ax, lambda t: u(t), -2, 3, breaks=[0], color=SIG, stroke_width=5)
        top = MathTex(r"u(t)\ \leftrightarrow\ \frac{1}{s},\ \ \mathrm{Re}\{s\} > 0", font_size=36, color=SIG).move_to(UP * 1.55)
        pole = sp.pole(0, size=0.16)
        roc = sp.roc(left=0, opacity=0.4)
        self.play(Create(ax), FadeIn(sp))
        self.play(Create(step), Write(top), FadeIn(pole), FadeIn(roc))
        self.wait(1)

        impulse = Arrow(ax.c2p(0, 0), ax.c2p(0, 1.3), buff=0, color=YELLOW, stroke_width=7, max_tip_length_to_length_ratio=0.15)
        flat = VGroup(Line(ax.c2p(-2, 0), ax.c2p(0, 0)), Line(ax.c2p(0, 0), ax.c2p(3, 0))).set_stroke(YELLOW, 5)
        d_lab = MathTex(r"\delta(t)", font_size=34, color=YELLOW).next_to(impulse, RIGHT, buff=0.1)
        bottom = MathTex(r"\frac{d}{dt}u(t) = \delta(t)\ \leftrightarrow\ s\cdot\frac{1}{s} = 1", font_size=36, color=YELLOW)
        bottom.move_to(top)
        self.play(ReplacementTransform(step, VGroup(flat, impulse)), FadeIn(d_lab), FadeTransform(top, bottom), run_time=2)

        zero = sp.zero(0, radius=0.2).shift(UP * 1.5)
        z_lab = Tex(r"the factor $s$ is a zero at $0$", font_size=28, color=ZERO_COLOR).next_to(sp, DOWN, buff=0.15)
        self.play(FadeIn(zero), FadeIn(z_lab))
        self.play(zero.animate.move_to(sp.c2p(0, 0)), run_time=1.2)
        self.play(Flash(sp.c2p(0, 0), color=YELLOW, flash_radius=0.5), FadeOut(zero), FadeOut(pole))
        whole = sp.roc(opacity=0.4)
        ext = Tex(r"pole cancelled $\Rightarrow$ ROC grows to the entire $s$-plane", font_size=28, color=GOOD).move_to(z_lab)
        self.play(Transform(roc, whole), FadeTransform(z_lab, ext))
        self.wait(2.5)
        fade_all(self)


class RepeatedPoles(Scene):
    def construct(self):
        title = make_title(r"Differentiation in $s$: repeated poles (Ex.\ 9.14)")
        rule = MathTex(r"-t\,x(t)\ \xleftrightarrow{\ \mathcal{L}\ }\ \frac{dX(s)}{ds}", font_size=40).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), Write(rule))

        ax = signal_axes(x_range=(-1, 6, 1), y_range=(0, 1.2, 0.5), x_length=6.6, y_length=3.6)
        ax.move_to(LEFT * 3.3 + DOWN * 1.1)
        sp = SPlane(x_range=(-3, 1, 1), y_range=(-2, 2, 1), x_length=3.6, y_length=3.6)
        sp.move_to(RIGHT * 4.3 + DOWN * 1.1)
        roc = sp.roc(left=-1, opacity=0.35)
        self.play(Create(ax), FadeIn(sp), FadeIn(roc))

        stages = [
            (lambda t: np.exp(-t) * u(t), r"e^{-t}u(t)", r"\frac{1}{s+1}", 1),
            (lambda t: t * np.exp(-t) * u(t), r"t\,e^{-t}u(t)", r"\frac{1}{(s+1)^2}", 2),
            (lambda t: t**2 / 2 * np.exp(-t) * u(t), r"\frac{t^2}{2}e^{-t}u(t)", r"\frac{1}{(s+1)^3}", 3),
        ]

        def pole_stack(n):
            g = VGroup(sp.pole(-1, size=0.16))
            if n > 1:
                g.add(MathTex(rf"\times {n}", font_size=30, color=POLE_COLOR).next_to(sp.c2p(-1, 0), UP, buff=0.25))
            return g

        def pair(f, sig, X, n):
            graph = clipped_graph(ax, f, -1, 6, breaks=[0], color=[SIG, TEAL_C, GOLD][n - 1], stroke_width=5)
            tex = MathTex(sig, r"\ \leftrightarrow\ ", X, font_size=38).move_to(UP * 1.35)
            tex[0].set_color([SIG, TEAL_C, GOLD][n - 1])
            return graph, tex, pole_stack(n)

        graph, tex, poles = pair(*stages[0])
        self.play(Create(graph), Write(tex), FadeIn(poles))
        self.wait(1)
        for st in stages[1:]:
            g2, t2, p2 = pair(*st)
            mult = MathTex(r"\times t", font_size=36, color=YELLOW).next_to(ax.c2p(3.5, 0.9), RIGHT)
            self.play(FadeIn(mult, scale=1.4))
            self.play(Transform(graph, g2), FadeTransform(tex, t2), Transform(poles, p2), FadeOut(mult), run_time=2)
            tex = t2
            self.wait(1.2)

        general = MathTex(r"\frac{t^{n-1}}{(n-1)!}e^{-at}u(t)\ \xleftrightarrow{\ \mathcal{L}\ }\ \frac{1}{(s+a)^n},\quad \mathrm{Re}\{s\} > -a",
                          font_size=36, color=YELLOW)
        general.move_to(tex)
        note = Tex(r"each extra factor of $t$ stacks one more pole on the same spot", font_size=30, color=GREY_A)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeTransform(tex, general), FadeIn(note))
        self.wait(2)

        integ = MathTex(r"\int_{-\infty}^{t} x(\tau)\,d\tau\ \xleftrightarrow{\ \mathcal{L}\ }\ \frac{1}{s}X(s):\qquad u(t)\to t\,u(t)\ \Leftrightarrow\ \frac{1}{s}\to\frac{1}{s^2}",
                        font_size=30, color=TEAL_B)
        integ.to_edge(DOWN, buff=0.12)
        self.play(FadeTransform(note, integ))
        self.wait(2.5)
        fade_all(self)
