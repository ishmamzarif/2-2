"""Lecture 6 - Introduction: why general complex exponentials e^{st}?

Scene: ExponentialsOnSPlane
  * e^{st} is an eigenfunction of every LTI system: e^{st} -> H(s) e^{st}
  * each point s = sigma + j omega of the s-plane is one "pure" signal e^{st}
  * sigma controls growth/decay, omega controls spinning
"""
from common import *


class ExponentialsOnSPlane(Scene):
    def construct(self):
        self.eigenfunction_intro()
        self.s_plane_tour()

    # ------------------------------------------------------------------
    def eigenfunction_intro(self):
        title = make_title(r"Why build everything out of $e^{st}$?")
        box = RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, color=GREY_B)
        box_label = MathTex(r"h(t)", font_size=48)
        sys_text = Tex("LTI system", font_size=28, color=GREY_B).next_to(box, UP, buff=0.15)
        inp = MathTex(r"e^{st}", font_size=60, color=SIG).next_to(box, LEFT, buff=1.7)
        out = MathTex(r"H(s)", r"\,e^{st}", font_size=60).next_to(box, RIGHT, buff=1.7)
        out[0].set_color(YELLOW)
        out[1].set_color(SIG)
        a1 = Arrow(inp.get_right(), box.get_left(), buff=0.2, color=GREY_A)
        a2 = Arrow(box.get_right(), out.get_left(), buff=0.2, color=GREY_A)
        diagram = VGroup(box, box_label, sys_text, inp, out, a1, a2).shift(UP * 1.3)

        self.play(Write(title))
        self.play(Create(box), FadeIn(box_label), FadeIn(sys_text))
        self.play(FadeIn(inp, shift=RIGHT * 0.5))
        self.play(GrowArrow(a1))
        self.play(GrowArrow(a2), TransformFromCopy(inp, out[1]), FadeIn(out[0], scale=1.6))
        self.wait(0.5)

        note = Tex(
            r"Same shape comes out --- only scaled by the number $H(s)$",
            font_size=34,
        ).next_to(diagram, DOWN, buff=0.6)
        hs = MathTex(
            r"H(s) = \int_{-\infty}^{\infty} h(\tau)\,e^{-s\tau}\,d\tau",
            font_size=44,
        ).next_to(note, DOWN, buff=0.3)
        hs[0][0:4].set_color(YELLOW)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.play(Write(hs))
        self.wait(1)

        s_def = MathTex(r"s", r"=", r"\sigma", r"+", r"j\omega", font_size=60)
        s_def[2].set_color(RED_B)
        s_def[4].set_color(TEAL_C)
        s_def.next_to(hs, DOWN, buff=0.35)
        fourier = Tex(r"Fourier only used $s = j\omega$.\ \ Laplace lets $s$ roam the whole plane.", font_size=32, color=GREY_A)
        fourier.next_to(s_def, DOWN, buff=0.25)
        self.play(Write(s_def))
        self.play(FadeIn(fourier))
        self.wait(1.5)
        fade_all(self)

    # ------------------------------------------------------------------
    def s_plane_tour(self):
        sig = ValueTracker(0.0)
        om = ValueTracker(2.0)
        t = ValueTracker(0.0)
        T_END = TAU

        # --- the s-plane (left)
        splane = SPlane(x_range=(-1, 1, 0.5), y_range=(-3, 3, 1), x_length=3.0, y_length=5.4, y_number_side=RIGHT)
        splane.move_to(LEFT * 5.2 + DOWN * 0.45)
        s_title = Tex(r"$s$-plane", font_size=34).next_to(splane, UP, buff=0.15)

        # --- the output plane where e^{st} lives (middle)
        oplane = NumberPlane(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            x_length=4.2,
            y_length=4.2,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.6},
            axis_config={"stroke_color": GREY_B},
        ).move_to(LEFT * 0.9 + DOWN * 0.45)
        unit_circle = Circle(radius=oplane.get_x_unit_size(), color=GREY_C, stroke_width=1.5).move_to(oplane.c2p(0, 0))
        o_title = MathTex(r"e^{st}\ \text{in the complex plane}", font_size=32).next_to(oplane, UP, buff=0.15)

        # --- graph of the imaginary part (right), sharing the vertical scale
        ax = Axes(
            x_range=(0, 6.6, 1),
            y_range=(-2, 2, 1),
            x_length=4.4,
            y_length=4.2,
            axis_config={"stroke_color": GREY_B, "tip_width": 0.18, "tip_height": 0.18, "include_ticks": False},
        )
        ax.shift(oplane.c2p(0, 0) - ax.c2p(0, 0) + RIGHT * 2.75)
        t_lab = MathTex("t", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        g_title = MathTex(r"\mathrm{Im}\{e^{st}\} = e^{\sigma t}\sin(\omega t)", font_size=30)
        g_title.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)

        def z(tt):
            return np.exp(complex(sig.get_value(), om.get_value()) * tt)

        s_dot = always_redraw(lambda: Dot(splane.c2p(sig.get_value(), om.get_value()), color=YELLOW, radius=0.09))
        s_lab = always_redraw(lambda: MathTex("s", color=YELLOW, font_size=34).next_to(s_dot, UL, buff=0.02))

        def vec():
            w = z(t.get_value())
            return Arrow(
                oplane.c2p(0, 0), oplane.c2p(w.real, w.imag), buff=0, color=SIG, stroke_width=5,
                max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=8,
            )

        def spiral():
            tt = t.get_value()
            if tt < 0.02:
                return VMobject()
            ts = np.linspace(0, tt, max(int(200 * tt / T_END), 3))
            pts = [z(x) for x in ts]
            return clipped_path([(p.real, p.imag) for p in pts], oplane.c2p, (-2, 2), (-2, 2), color=SIG, stroke_width=3)

        def graph():
            tt = t.get_value()
            if tt < 0.02:
                return VMobject()
            return clipped_graph(ax, lambda x: z(x).imag, 0, tt, n=int(250 * tt / T_END) + 3, color=TEAL_C, stroke_width=4)

        def proj():
            tt = t.get_value()
            w = z(tt)
            if abs(w.imag) > 2:
                return VMobject()
            return DashedLine(oplane.c2p(w.real, w.imag), ax.c2p(tt, w.imag), color=GREY_B, stroke_width=1.5, dash_length=0.08)

        def gdot():
            tt = t.get_value()
            w = z(tt)
            if abs(w.imag) > 2:
                return VMobject()
            return Dot(ax.c2p(tt, w.imag), color=TEAL_C, radius=0.06)

        vec_m = always_redraw(vec)
        spiral_m = always_redraw(spiral)
        graph_m = always_redraw(graph)
        proj_m = always_redraw(proj)
        gdot_m = always_redraw(gdot)

        # readouts under the s-plane
        sig_num = DecimalNumber(0, num_decimal_places=2, include_sign=True, font_size=30, color=RED_B)
        om_num = DecimalNumber(2, num_decimal_places=2, include_sign=True, font_size=30, color=TEAL_C)
        sig_num.add_updater(lambda m: m.set_value(sig.get_value()))
        om_num.add_updater(lambda m: m.set_value(om.get_value()))
        readout = VGroup(
            VGroup(MathTex(r"\sigma =", font_size=30, color=RED_B), sig_num).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"\omega =", font_size=30, color=TEAL_C), om_num).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.4).next_to(splane, DOWN, buff=0.2)

        self.play(
            FadeIn(splane), FadeIn(s_title), FadeIn(oplane), Create(unit_circle), FadeIn(o_title),
            Create(ax), FadeIn(t_lab), FadeIn(g_title), run_time=1.5,
        )
        self.play(FadeIn(s_dot, scale=2), FadeIn(s_lab), FadeIn(readout))
        self.add(spiral_m, graph_m, vec_m, proj_m, gdot_m)

        cap = [None]

        def set_caption(text, color=WHITE):
            new = Tex(text, font_size=34, color=color).to_edge(UP, buff=0.3)
            if cap[0] is None:
                self.play(FadeIn(new, shift=DOWN * 0.2))
            else:
                self.play(FadeTransform(cap[0], new))
            cap[0] = new

        def run_time_axis(rt=5):
            self.play(t.animate.set_value(T_END), run_time=rt, rate_func=linear)

        # 1. on the j omega axis: pure rotation
        set_caption(r"$\sigma = 0$: pure spinning, $e^{j\omega t}$ \ (Fourier's building block)", color=TEAL_C)
        run_time_axis()
        self.wait(0.5)

        # 2. left half-plane: decaying
        t.set_value(0)
        self.play(sig.animate.set_value(-0.35), run_time=1.5)
        set_caption(r"$\sigma < 0$: spiral inwards $\Rightarrow$ decaying oscillation", color=BLUE_B)
        run_time_axis()
        self.wait(0.5)

        # 3. right half-plane: growing
        t.set_value(0)
        self.play(sig.animate.set_value(0.1), run_time=1.5)
        set_caption(r"$\sigma > 0$: spiral outwards $\Rightarrow$ growing oscillation", color=RED_B)
        run_time_axis()
        self.wait(0.5)

        # 4. real axis: no spin
        t.set_value(0)
        self.play(sig.animate.set_value(-0.5), om.animate.set_value(0), run_time=1.5)
        set_caption(r"$\omega = 0$: no spinning, just a real exponential $e^{\sigma t}$", color=YELLOW)
        run_time_axis(3)
        self.wait(0.5)

        # 5. roam the plane with the full curve visible
        set_caption(r"Every point $s$ is a different pure signal $e^{st}$")
        for s_, o_ in [(-0.3, 1.0), (-0.15, 3.0), (0.0, 2.5), (0.08, 1.5), (-0.6, -2.0), (-0.25, 2.0)]:
            self.play(sig.animate.set_value(s_), om.animate.set_value(o_), run_time=1.8)
            self.wait(0.2)

        lhp = splane.roc(right=0, color=GREEN_E, opacity=0.35, boundary=False)
        rhp = splane.roc(left=0, color=RED_E, opacity=0.35, boundary=False)
        jw = splane.jw_axis()
        lhp_t = Tex("decay", font_size=26, color=GREEN_B).move_to(splane.c2p(-0.5, -2.6))
        rhp_t = Tex("growth", font_size=26, color=RED_B).move_to(splane.c2p(0.5, -2.6))
        self.play(FadeIn(lhp), FadeIn(rhp), FadeIn(lhp_t), FadeIn(rhp_t))
        self.play(Create(jw))
        set_caption(r"Laplace transform: \emph{how much} of each $e^{st}$ is inside $x(t)$?", color=YELLOW)
        self.wait(2.5)
        fade_all(self)
