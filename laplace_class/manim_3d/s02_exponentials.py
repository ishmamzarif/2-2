"""Background 2 - the complex exponential e^{st}, s = sigma + j omega.

Scene: ComplexExponentials
  * real exponentials e^{sigma t}: decay, constant, growth
  * e^{st} = e^{sigma t} e^{j omega t}: a helix wrapped on a funnel of radius e^{sigma t}
  * a point s on the s-plane picks one spiral; tour the plane
  * map: left half decays, right half grows, j omega-axis spins forever
  * a conjugate pair s, s* adds up to the real signal e^{sigma t} cos(omega t)
"""
from common3d import *

T_MAX = 8.0
R = 2.0


class ComplexExponentials(LScene):
    def construct(self):
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=R, t_length=9, r_length=4)
        self.ax = ax
        sig = ValueTracker(-0.35)
        om = ValueTracker(0.0)
        self.sig, self.om = sig, om

        def z(t):
            return np.exp(complex(sig.get_value(), om.get_value()) * t)

        self.z = z
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ax.c2p(T_MAX / 2 - 0.4, 0.5, 0))
        self.real_exponentials()
        self.add_spin()
        self.tour()
        self.conjugate_pair()
        self.clear_all()

    # ------------------------------------------------------------------
    def real_exponentials(self):
        ax, sig, z = self.ax, self.sig, self.z
        labs = ct_labels(ax)
        t_lab, re_lab, im_lab = labs
        self.face_camera(t_lab, re_lab, im_lab)
        self.im_lab = im_lab
        self.set_title(r"Real exponentials $e^{\sigma t}$")
        self.play(Create(ax.x_axis), Create(ax.y_axis), FadeIn(t_lab), FadeIn(re_lab))
        curve = always_redraw(lambda: complex_curve(ax, z, 0, T_MAX, n=500, rmax=R, color=SIG, width=5))
        self.curve = curve

        sig_num = DecimalNumber(sig.get_value(), num_decimal_places=2, include_sign=True, font_size=44, color=RED_B)
        sig_row = VGroup(MathTex(r"\sigma =", font_size=44, color=RED_B), sig_num).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.5)
        sig_num.add_updater(lambda m: m.set_value(sig.get_value()).next_to(sig_row[0], RIGHT, buff=0.15))
        self.hud(sig_row, live=True)
        self.sig_row = sig_row
        self.play(Create(curve), FadeIn(sig_row), run_time=1.5)
        self.add(curve)
        tag = self.panel(Tex("decays", font_size=38, color=GREEN_B).next_to(sig_row, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(tag))
        self.beat("sigma < 0: decays")
        tag2 = self.panel(Tex("constant", font_size=38, color=GREY_A).next_to(sig_row, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(sig.animate.set_value(0.0), FadeTransform(tag, tag2), run_time=2)
        self.beat("sigma = 0: constant", hold=1.0)
        tag3 = self.panel(Tex("grows", font_size=38, color=RED_B).next_to(sig_row, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(sig.animate.set_value(0.12), FadeTransform(tag2, tag3), run_time=2)
        self.beat("sigma > 0: grows")
        self.play(sig.animate.set_value(-0.2), FadeOut(tag3), run_time=1.5)

    # ------------------------------------------------------------------
    def add_spin(self):
        ax, sig, om = self.ax, self.sig, self.om
        self.set_title(r"Complex exponentials $e^{st}$")
        formula = MathTex(r"e^{st}", r"=", r"e^{\sigma t}", r"\, e^{j\omega t}", font_size=48)
        formula[2].set_color(RED_B)
        formula[3].set_color(SIG)
        s_def = MathTex(r"s = \sigma + j\omega", font_size=40)
        size_note = Tex("size", font_size=30, color=RED_B).next_to(formula[2], DOWN, buff=0.15)
        spin_note = Tex("spin", font_size=30, color=SIG).next_to(formula[3], DOWN, buff=0.15)
        block = VGroup(formula, size_note, spin_note)
        block.to_corner(UR, buff=0.5)
        s_def.next_to(block, DOWN, buff=0.3, aligned_edge=RIGHT)
        block = self.panel(VGroup(block, s_def))
        self.play(FadeOut(self.sig_row), FadeIn(block))
        self.sig_row[1].clear_updaters()
        self.block = block

        # tilt into 3D while the spin is switched on
        self.move_camera(phi=68 * DEGREES, theta=-40 * DEGREES, zoom=0.84, frame_center=ax.c2p(T_MAX / 2 - 0.4, 0, 0.35),
                         added_anims=[Create(ax.z_axis), FadeIn(self.im_lab), om.animate.set_value(2.0)], run_time=4)
        self.beat("e^{st}: a spiral")

        env = always_redraw(lambda: envelope(ax, sig.get_value(), T_MAX, R))
        self.play(FadeIn(env), run_time=1.2)
        self.add(env)
        self.env = env
        self.beat("its envelope e^{sigma t}", hold=1.0)

    # ------------------------------------------------------------------
    def tour(self):
        ax, sig, om = self.ax, self.sig, self.om
        sp = MiniSPlane(x_range=(-1, 1, 0.5), y_range=(-4, 4, 2), width=2.6, height=3.6, size=20).to_corner(DL, buff=0.35)
        dot = Dot(sp.c2p(sig.get_value(), om.get_value()), radius=0.08, color=YELLOW)
        dot.add_updater(lambda m: m.move_to(sp.c2p(sig.get_value(), om.get_value())))
        s_lab = MathTex("s", font_size=30, color=YELLOW)
        s_lab.add_updater(lambda m: m.next_to(dot, UR, buff=0.04))
        title = Tex(r"$s$-plane", font_size=30, color=GREY_A).next_to(sp, UP, buff=0.12)
        self.hud(sp, dot, s_lab, title)
        self.play(FadeIn(sp), FadeIn(title), FadeIn(dot, scale=2), FadeIn(s_lab))
        self.sp, self.dot, self.s_lab = sp, dot, s_lab
        self.beat("each s is one spiral", hold=1.0)

        def go(s_, o_, rt=2.5):
            self.play(sig.animate.set_value(s_), om.animate.set_value(o_), run_time=rt)

        go(-0.35, 2.0)
        self.beat("left of the axis: shrinks")
        go(0.0, 2.0)
        self.beat("on the j omega-axis: spins forever")
        go(0.1, 2.0)
        self.beat("right of the axis: grows")
        go(-0.15, 4.0)
        self.wait(0.6)
        go(-0.15, 1.0)
        self.wait(0.6)
        go(-0.15, -2.0, rt=3)
        self.beat("omega: faster, slower, reversed")
        go(-0.3, 0.0)
        self.beat("on the real axis: no spin")

        # the map of the plane
        lhp = sp.region(right=0, color=GREEN_E, opacity=0.4, edges=False)
        rhp = sp.region(left=0, color=RED_E, opacity=0.4, edges=False)
        jw = sp.vline(0, color=YELLOW, width=4)
        d_lab = Tex("decay", font_size=24, color=GREEN_B).move_to(sp.c2p(-0.5, -3.3))
        g_lab = Tex("growth", font_size=24, color=RED_B).move_to(sp.c2p(0.5, -3.3))
        self.hud(lhp, rhp, jw, d_lab, g_lab)
        self.play(FadeIn(lhp), FadeIn(rhp), Create(jw), FadeIn(d_lab), FadeIn(g_lab))
        # keep the dot on top of the shading
        self.remove(self.dot, self.s_lab)
        self.add(self.dot, self.s_lab)
        go(-0.2, 2.0)
        self.beat("the map of the s-plane")

    # ------------------------------------------------------------------
    def conjugate_pair(self):
        ax, sig, om, sp = self.ax, self.sig, self.om, self.sp
        self.set_title("A conjugate pair makes a real signal")
        cdot = Dot(sp.c2p(sig.get_value(), -om.get_value()), radius=0.08, color=PURPLE_B)
        c_lab = MathTex(r"s^*", font_size=28, color=PURPLE_B).next_to(cdot, DR, buff=0.04)
        self.hud(cdot, c_lab)
        self.play(FadeOut(self.env), FadeIn(cdot, scale=2), FadeIn(c_lab))
        self.remove(self.env)
        conj = complex_curve(ax, lambda t: np.exp(complex(sig.get_value(), -om.get_value()) * t), 0, T_MAX, n=500, rmax=R, color=PURPLE_B, width=4)
        self.play(Create(conj), run_time=2.5)
        real = complex_curve(ax, lambda t: np.exp(sig.get_value() * t) * np.cos(om.get_value() * t) + 0j, 0, T_MAX, n=500,
                             rmax=R, color=YELLOW, width=6)
        formula = self.panel(MathTex(r"\frac{e^{st} + e^{s^* t}}{2} = e^{\sigma t}\cos\omega t", font_size=44).to_corner(UR, buff=0.5))
        self.play(FadeOut(self.block), FadeIn(formula))
        self.play(Create(real), run_time=3)
        self.beat("conjugate pair = damped cosine")
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ax.c2p(T_MAX / 2 - 0.4, 0.4, 0), run_time=3)
        self.beat("seen from above: e^{sigma t} cos(omega t)")

