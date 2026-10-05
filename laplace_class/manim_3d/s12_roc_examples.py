"""ROC property 6-8 and Examples 9.7, 9.8.

Scene: ROCStrips
  * P6 / Example 9.7: e^{-b|t|} = right part + left part; the ROCs Re{s} > -b and
    Re{s} < b overlap in a strip; as b shrinks to 0 the strip vanishes - no
    Laplace transform at all
  * P7 / P8: a rational X(s) has ROC edges at poles; right-sided -> right of the
    rightmost pole, left-sided -> left of the leftmost, two-sided -> a strip
  * Example 9.8: 1/((s+1)(s+2)) admits three ROCs - three different signals
"""
from common3d import *

U = (-3, 2.5)
V = (-3.5, 3.5)


class ROCStrips(LScene):
    def construct(self):
        ax = splane_axes(u_range=U, v_range=V, z_max=3.5, x_length=6, y_length=7, z_length=2.8)
        self.ax = ax
        camera_at(self, ax.c2p(-0.25, 0, 0.4), screen=(-2.0, -0.6), phi=58 * DEGREES, theta=-62 * DEGREES, zoom=0.8)
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        ticks = floor_ticks(ax, us=[-2, -1, 1, 2], vs=[-3, 3])
        self.add(floor, ax.x_axis, ax.y_axis, labs, ticks)
        self.two_sided()
        self.rational_rules()
        self.three_rocs()
        self.clear_all()

    # ------------------------------------------------------------------
    def two_sided(self):
        ax = self.ax
        self.set_title(r"Property 6: two-sided $\Rightarrow$ a strip")
        b = ValueTracker(1.0)
        sax = mini_axes(x_range=(-3, 3, 1), y_range=(-0.2, 1.2, 1), width=4.2, height=1.6, x_label="t", size=24)
        sax.to_corner(UR, buff=0.45).shift(0.5 * DOWN)
        sbg = BackgroundRectangle(sax, fill_color=PANEL_BG, fill_opacity=0.85, buff=0.15)
        sbg.hud_layer = -1

        def parts():
            bb = b.get_value()
            return VGroup(
                graph2d(sax, lambda t: np.exp(bb * t) * (t < 0), -3, 3, color=RED_B, width=4, breaks=(0,)),
                graph2d(sax, lambda t: np.exp(-bb * t) * (t >= 0), -3, 3, color=SIG, width=4, breaks=(0,)),
            )

        sig = always_redraw(parts)
        sig_eq = MathTex(r"x(t) = e^{-b|t|} = ", r"e^{-bt}u(t)", r" + ", r"e^{bt}u(-t)", font_size=38)
        sig_eq[1].set_color(SIG)
        sig_eq[3].set_color(RED_B)
        sig_eq.next_to(sax, DOWN, buff=0.25).align_to(sax, RIGHT)
        self.hud(sbg, sax, sig_eq)
        self.hud(sig, live=True)
        self.play(FadeIn(sbg), FadeIn(sax), FadeIn(sig_eq), Create(sig))
        self.add(sig)
        self.beat("Example 9.7: a two-sided signal, split in two", hold=1.0)

        def right_roc():
            return roc_floor(ax, left=-b.get_value(), color=BLUE_D, opacity=0.28)

        def left_roc():
            return roc_floor(ax, right=b.get_value(), color=RED_D, opacity=0.28)

        rr = always_redraw(right_roc)
        lr = always_redraw(left_roc)
        poles = always_redraw(lambda: VGroup(pole_x(ax, -b.get_value()), pole_x(ax, b.get_value())))
        roc_eqs = self.panel(VGroup(
            MathTex(r"e^{-bt}u(t):\ \ \mathrm{Re}\{s\} > -b", font_size=36, color=BLUE_B),
            MathTex(r"e^{bt}u(-t):\ \ \mathrm{Re}\{s\} < b", font_size=36, color=RED_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).next_to(sig_eq, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(roc_eqs[0]), FadeIn(roc_eqs[1][0]), FadeIn(rr), FadeIn(poles))
        self.add(rr, poles)
        self.play(FadeIn(roc_eqs[1][1]), FadeIn(lr))
        self.add(lr)
        strip_note = self.panel(MathTex(r"\text{overlap: } -b < \mathrm{Re}\{s\} < b", font_size=40, color=PURPLE_B)
                                .next_to(roc_eqs, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(strip_note))
        self.beat("both ROCs overlap in a strip")

        surf = landscape(ax, lambda s: -2 * 1.0 / (s**2 - 1.0), res=(40, 48), roc=(-1, 1))
        self.play(FadeIn(surf), run_time=2)
        x_eq = self.panel(MathTex(r"X(s) = \frac{-2b}{s^2 - b^2}", font_size=42).to_corner(DL, buff=0.45))
        self.play(FadeIn(x_eq))
        self.beat("the landscape, strip lit")
        self.play(FadeOut(surf), FadeOut(x_eq))

        b_num = DecimalNumber(1.0, num_decimal_places=2, font_size=40, color=YELLOW)
        b_row = VGroup(MathTex("b =", font_size=40, color=YELLOW), b_num).arrange(RIGHT, buff=0.15).to_corner(DL, buff=0.5)
        b_num.add_updater(lambda m: m.set_value(b.get_value()).next_to(b_row[0], RIGHT, buff=0.15))
        self.hud(b_row, live=True)
        self.play(FadeIn(b_row))
        self.play(b.animate.set_value(0.35), run_time=3)
        self.beat("smaller b: a thinner strip", hold=1.0)
        self.play(b.animate.set_value(-0.4), run_time=3)
        none = self.panel(Tex(r"$b \le 0$: no overlap, no Laplace transform", font_size=38, color=BAD).to_edge(DOWN, buff=0.4))
        self.play(FadeIn(none))
        self.beat("b <= 0: the strip is gone")
        b_num.clear_updaters()
        self.play(*[FadeOut(m) for m in (sig, sbg, sax, sig_eq, rr, lr, poles, roc_eqs, strip_note, none, b_row)])
        self.remove(sig, rr, lr, poles)

    # ------------------------------------------------------------------
    def rational_rules(self):
        ax = self.ax
        self.set_title(r"Properties 7 \& 8: rational $X(s)$")
        ps = [-2.0, -1.0, 1.0]
        poles = VGroup(*[pole_x(ax, p) for p in ps])
        lines = VGroup(*[DashedLine(ax.c2p(p, V[0], 0), ax.c2p(p, V[1], 0), color=GREY_B, stroke_width=2, dash_length=0.12)
                         for p in ps])
        tag_floor(lines)
        rule = self.panel(VGroup(
            Tex(r"ROC edges pass through poles", font_size=38),
            Tex(r"right-sided: right of the rightmost pole", font_size=34, color=SIG),
            Tex(r"left-sided: left of the leftmost pole", font_size=34, color=RED_B),
            Tex(r"two-sided: a strip between poles", font_size=34, color=PURPLE_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.4))
        self.play(FadeIn(poles), Create(lines), FadeIn(rule[0]), FadeIn(rule[1][0]))
        self.beat("poles chop the plane into strips", hold=1.0)
        for i, (l, r, col) in enumerate([(1.0, None, BLUE_D), (None, -2.0, RED_D), (-1.0, 1.0, PURPLE_D)]):
            reg = roc_floor(ax, left=l, right=r, color=col, opacity=0.4)
            self.play(FadeIn(reg), FadeIn(rule[1][i + 1]))
            self.wait(1.2)
            self.play(FadeOut(reg))
        self.beat("the allowed ROCs")
        self.play(FadeOut(poles), FadeOut(lines), FadeOut(rule))

    # ------------------------------------------------------------------
    def three_rocs(self):
        ax = self.ax
        self.set_title(r"Example 9.8: one $X(s)$, three signals")

        def X(s):
            return 1 / ((s + 1) * (s + 2))

        eq = self.panel(MathTex(r"X(s) = \frac{1}{(s+1)(s+2)}", font_size=46).to_corner(UR, buff=0.4))
        surf = landscape(ax, X, res=(44, 48))
        surf.save_state()
        surf.stretch(0.001, 2, about_point=ax.c2p(0, 0, 0))
        self.add(surf)
        poles = VGroup(pole_x(ax, -1), pole_x(ax, -2))
        self.play(FadeIn(eq), Restore(surf), FadeIn(poles), run_time=2.5)
        self.beat("two poles: -1 and -2", hold=1.0)

        sax = mini_axes(x_range=(-3, 3, 1), y_range=(-0.6, 0.6, 0.5), width=4.2, height=2.0, x_label="t", size=24)
        sax.to_corner(DR, buff=0.45)
        sbg = BackgroundRectangle(sax, fill_color=PANEL_BG, fill_opacity=0.85, buff=0.15)
        sbg.hud_layer = -1
        self.hud(sbg, sax)
        self.play(FadeIn(sbg), FadeIn(sax))
        cases = [
            ((-1, None), r"\mathrm{Re}\{s\} > -1", r"\big(e^{-t} - e^{-2t}\big)u(t)", lambda t: (np.exp(-t) - np.exp(-2 * t)) * (t >= 0),
             "right of both poles: right-sided"),
            ((None, -2), r"\mathrm{Re}\{s\} < -2", r"\big(-e^{-t} + e^{-2t}\big)u(-t)", lambda t: (-np.exp(-t) + np.exp(-2 * t)) * (t < 0),
             "left of both poles: left-sided"),
            ((-2, -1), r"-2 < \mathrm{Re}\{s\} < -1", r"-e^{-t}u(-t) - e^{-2t}u(t)", lambda t: np.where(t < 0, -np.exp(-t), -np.exp(-2 * t)),
             "between the poles: two-sided"),
        ]
        prev = []
        prev_roc = None
        for (l, r), roc_tex, sig_tex, f, label in cases:
            roc = roc_floor(ax, left=l, right=r)
            g = graph2d(sax, f, -3, 3, color=YELLOW, width=4, breaks=(0,))
            txt = self.panel(VGroup(
                MathTex(r"\mathrm{ROC}:\ " + roc_tex, font_size=40, color=BLUE_B),
                MathTex(r"x(t) = " + sig_tex, font_size=38, color=YELLOW),
            ).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).next_to(eq, DOWN, buff=0.3, aligned_edge=RIGHT))
            self.hud(g)
            anims = [FadeIn(roc), FadeIn(txt), Create(g), roc_transition(surf, prev_roc, (l, r))]
            anims += [FadeOut(m) for m in prev]
            self.play(*anims, run_time=2)
            self.beat(label)
            prev = [roc, txt, g]
            prev_roc = (l, r)
        self.play(*[FadeOut(m) for m in prev], FadeOut(sbg), FadeOut(sax))
        nxt = self.panel(Tex(r"which one? the ROC decides $\Rightarrow$ inverse transform next", font_size=36, color=GREY_A)
                         .to_edge(DOWN, buff=0.4))
        self.play(FadeIn(nxt))
        self.beat("the ROC picks the signal", hold=1.0)
