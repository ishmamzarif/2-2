"""Background 1 - complex numbers, Euler's formula, and e^{j omega t} as a helix.

Scene: ComplexToEuler
  * the complex plane, z = a + jb, multiplying by j rotates by 90 degrees
  * polar form; multiplying = rotate + scale
  * Euler: e^{j theta} walks the unit circle, shadows cos and sin
  * add time as a third axis: e^{j omega t} is a helix; its shadows are cos and sin waves
  * cos(omega t) = two opposite helices added together
"""
from common3d import *

W0 = 2.0          # default angular frequency
T_MAX = 8.0


class ComplexToEuler(LScene):
    def construct(self):
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=1.5, t_length=9, r_length=3.4)
        self.ax = ax
        self.set_camera_orientation(phi=90 * DEGREES, theta=0, zoom=1.6, frame_center=ax.c2p(0, 1.5, 0))
        self.complex_plane()
        self.euler()
        self.helix()
        self.cosine_from_two_helices()
        self.clear_all()

    # ------------------------------------------------------------------
    def complex_plane(self):
        ax = self.ax
        grid = cplane_grid(ax, step=0.5)
        re_lab = MathTex(r"\mathrm{Re}", font_size=30, color=RE_COLOR).move_to(ax.c2p(0, 1.75, 0.12))
        im_lab = MathTex(r"\mathrm{Im}", font_size=30, color=IM_COLOR).move_to(ax.c2p(0, 0.18, 1.68))
        self.face_camera(re_lab, im_lab)
        self.set_title("Complex numbers")
        self.play(Create(grid), Create(ax.y_axis), Create(ax.z_axis), FadeIn(re_lab), FadeIn(im_lab), run_time=1.5)
        self.plane_bits = VGroup(grid, re_lab, im_lab)
        self.beat("the complex plane", hold=1.0)

        # z = a + jb
        z0 = 1.1 + 0.7j
        zt = ComplexValueTracker(z0)
        arrow = always_redraw(lambda: cplane_arrow(ax, zt.get_value(), color=SIG, width=5))
        a_line = DashedLine(cpoint(ax, z0), cpoint(ax, z0.real), color=GREY_B, stroke_width=2, dash_length=0.06)
        b_line = DashedLine(cpoint(ax, z0), cpoint(ax, 1j * z0.imag), color=GREY_B, stroke_width=2, dash_length=0.06)
        a_lab = MathTex("a", font_size=30, color=RE_COLOR).move_to(ax.c2p(0, z0.real, -0.16))
        b_lab = MathTex("b", font_size=30, color=IM_COLOR).move_to(ax.c2p(0, -0.14, z0.imag))
        z_lab = MathTex("z = a + jb", font_size=32, color=SIG).move_to(ax.c2p(0, z0.real + 0.15, z0.imag + 0.2))
        self.face_camera(a_lab, b_lab, z_lab)
        self.play(GrowFromPoint(arrow, cpoint(ax, 0)), run_time=0.8)
        self.add(arrow)
        self.play(Create(a_line), Create(b_line), FadeIn(a_lab), FadeIn(b_lab), FadeIn(z_lab))
        self.beat("z = a + jb")

        # multiply by j
        self.play(FadeOut(a_line), FadeOut(b_line), FadeOut(a_lab), FadeOut(b_lab), FadeOut(z_lab), run_time=0.6)
        ghost = cplane_arrow(ax, z0, color=SIG, width=3).set_opacity(0.35)
        self.add(ghost)
        times_j = self.panel(MathTex(r"\times\, j", font_size=44, color=YELLOW).to_corner(UR, buff=0.5))
        arc = always_redraw(lambda: cplane_arc(ax, 0.45, np.angle(z0), np.angle(z0) + np.angle(zt.get_value() / z0) % TAU, color=YELLOW, width=3))
        self.add(arc)
        self.play(FadeIn(times_j))
        self.play(_rotate_tracker(zt, z0, PI / 2), run_time=1.5)
        ninety = MathTex(r"90^\circ", font_size=28, color=YELLOW).move_to(ax.c2p(0, 0.05, 0.62))
        self.face_camera(ninety)
        self.play(FadeIn(ninety))
        self.beat("multiply by j: rotate 90 degrees")

        jj = self.panel(MathTex(r"\times\, j \times j = \times (-1)", font_size=44, color=YELLOW).to_corner(UR, buff=0.5))
        self.play(FadeOut(ninety), FadeTransform(times_j, jj))
        self.play(_rotate_tracker(zt, 1j * z0, PI / 2), run_time=1.5)
        j2 = self.panel(MathTex(r"j^2 = -1", font_size=48, color=YELLOW).next_to(jj, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(j2, shift=0.2 * DOWN))
        self.beat("j squared = -1")

        # polar form
        self.remove(arc)
        self.play(FadeOut(jj), FadeOut(j2), FadeOut(ghost), zt.animate.set_value(z0), run_time=1.0)
        r_lab = MathTex("r", font_size=32, color=SIG).move_to(cpoint(ax, z0 * 0.5) + 0.25 * normalize(np.cross(RIGHT, cpoint(ax, z0) - cpoint(ax, 0))))
        th_arc = cplane_arc(ax, 0.38, 0, np.angle(z0), color=YELLOW, width=3)
        th_lab = MathTex(r"\theta", font_size=32, color=YELLOW).move_to(ax.c2p(0, 0.55, 0.16))
        self.face_camera(r_lab, th_lab)
        polar = self.panel(MathTex(r"z = r(\cos\theta + j\sin\theta)", font_size=42).to_corner(UR, buff=0.5))
        self.play(FadeIn(r_lab), Create(th_arc), FadeIn(th_lab), FadeIn(polar))
        self.beat("polar form: length and angle")

        # multiplying = rotate + scale
        w = 0.8 * np.exp(1j * 50 * DEGREES)
        w_arrow = cplane_arrow(ax, w, color=IM_COLOR, width=4)
        w_lab = MathTex("w", font_size=32, color=IM_COLOR).move_to(cpoint(ax, w * 1.18))
        self.face_camera(w_lab)
        rule = self.panel(MathTex(r"|zw| = |z|\,|w| \qquad \angle zw = \angle z + \angle w", font_size=40).to_corner(UR, buff=0.5))
        self.play(FadeOut(r_lab), FadeOut(th_arc), FadeOut(th_lab), FadeOut(polar), GrowFromPoint(w_arrow, cpoint(ax, 0)), FadeIn(w_lab))
        ghost = cplane_arrow(ax, z0, color=SIG, width=3).set_opacity(0.35)
        self.add(ghost)
        self.play(FadeIn(rule))
        self.play(_rotate_tracker(zt, z0, np.angle(w), scale=abs(w)), run_time=2)
        zw_lab = MathTex("zw", font_size=32, color=SIG).move_to(cpoint(ax, z0 * w * 1.22))
        self.face_camera(zw_lab)
        self.play(FadeIn(zw_lab))
        self.beat("multiplying = rotate and scale")

        self.play(*[FadeOut(m) for m in (ghost, w_arrow, w_lab, zw_lab, rule)], FadeOut(arrow), run_time=0.8)
        self.remove(arrow)

    # ------------------------------------------------------------------
    def euler(self):
        ax = self.ax
        self.set_title("Euler's formula")
        circle = cplane_arc(ax, 1.0, 0, TAU, color=GREY_B, width=2)
        th = ValueTracker(0.0)
        arrow = always_redraw(lambda: cplane_arrow(ax, np.exp(1j * th.get_value()), color=SIG, width=5))
        cos_seg = always_redraw(lambda: Line(cpoint(ax, 0), cpoint(ax, np.cos(th.get_value())), color=RE_COLOR, stroke_width=7))
        sin_seg = always_redraw(lambda: Line(cpoint(ax, np.cos(th.get_value())), cpoint(ax, np.exp(1j * th.get_value())), color=IM_COLOR, stroke_width=7))
        cos_lab = MathTex(r"\cos\theta", font_size=30, color=RE_COLOR)
        sin_lab = MathTex(r"\sin\theta", font_size=30, color=IM_COLOR)
        cos_lab.add_updater(lambda m: m.move_to(ax.c2p(0, 0.5 * np.cos(th.get_value()), -0.18 if np.sin(th.get_value()) >= 0 else 0.18)))
        sin_lab.add_updater(lambda m: m.move_to(ax.c2p(0, np.cos(th.get_value()) + (0.38 if np.cos(th.get_value()) >= 0 else -0.38), 0.5 * np.sin(th.get_value()))))
        self.face_camera(cos_lab, sin_lab)
        th.set_value(40 * DEGREES)
        formula = self.panel(MathTex(r"e^{j\theta} = \cos\theta + j\sin\theta", font_size=46).to_corner(UR, buff=0.5))
        self.play(Create(circle), FadeIn(formula))
        self.play(GrowFromPoint(arrow, cpoint(ax, 0)), run_time=0.8)
        self.add(arrow)
        self.play(Create(cos_seg), Create(sin_seg), FadeIn(cos_lab), FadeIn(sin_lab))
        self.beat("Euler's formula")
        self.play(th.animate.set_value(40 * DEGREES + TAU), run_time=5, rate_func=linear)
        polar = self.panel(MathTex(r"z = r\,e^{j\theta}", font_size=46, color=SIG).next_to(formula, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(polar, shift=0.2 * DOWN))
        self.beat("any z = r e^{j theta}")
        for m in (cos_lab, sin_lab):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in (cos_seg, sin_seg, cos_lab, sin_lab, arrow, polar, formula)], run_time=0.8)
        self.remove(arrow, cos_seg, sin_seg)
        self.circle = circle

    # ------------------------------------------------------------------
    def helix(self):
        ax = self.ax
        self.set_title(r"Add time: $e^{j\omega t}$")
        T = ValueTracker(0.0)
        om = ValueTracker(W0)

        def z(t):
            return np.exp(1j * om.get_value() * t)

        formula = self.panel(MathTex(r"e^{j\omega t} = \cos\omega t + j\sin\omega t", font_size=44).to_corner(UR, buff=0.5))
        # first just spin in place: the angle grows with time
        spin = ValueTracker(0.0)
        spinning = always_redraw(lambda: cplane_arrow(ax, np.exp(1j * W0 * spin.get_value()), color=SIG, width=4))
        self.play(FadeIn(formula), GrowFromPoint(spinning, cpoint(ax, 0)))
        self.play(spin.animate.set_value(TAU / W0), run_time=3, rate_func=linear)
        self.remove(spinning)
        tip_arrow = always_redraw(lambda: cplane_arrow(ax, z(T.get_value()), t=T.get_value(), color=SIG, width=4))
        self.add(tip_arrow)
        self.beat("spinning as time passes", hold=1.0)

        # swing the camera: time becomes a third axis
        t_lab = MathTex("t", font_size=36, color=LABEL_COLOR).move_to(ax.c2p(T_MAX + 0.4, 0, 0))
        self.face_camera(t_lab)
        self.move_camera(phi=70 * DEGREES, theta=-42 * DEGREES, zoom=0.95, frame_center=ax.c2p(T_MAX / 2, 0, -0.3),
                         added_anims=[Create(ax.x_axis), FadeIn(t_lab), FadeOut(self.plane_bits[0]), self.circle.animate.set_stroke(opacity=0.5)],
                         run_time=3)
        helix = always_redraw(lambda: complex_curve(ax, z, 0, max(T.get_value(), 1e-3), n=max(int(60 * T.get_value()), 4), color=SIG, width=5))
        self.add(helix)
        self.play(T.animate.set_value(T_MAX), run_time=6, rate_func=linear)
        lab = MathTex(r"e^{j\omega t}", font_size=40, color=SIG).move_to(ax.c2p(T_MAX + 0.2, 0.2, 1.3))
        self.face_camera(lab)
        self.play(FadeIn(lab))
        self.beat("a helix: rotation + time")

        # shadows on the floor and the back wall
        walls = shadow_walls(ax)
        self.play(FadeIn(walls), run_time=1)
        self.play(T.animate.set_value(0), FadeOut(lab), run_time=1.5)
        r = ax.y_range[1]
        cos_sh = always_redraw(lambda: real_curve(ax, lambda t: np.cos(om.get_value() * t), 0, max(T.get_value(), 1e-3),
                                                  n=max(int(60 * T.get_value()), 4), color=RE_COLOR, width=4, plane="xy", offset=-r))
        sin_sh = always_redraw(lambda: real_curve(ax, lambda t: np.sin(om.get_value() * t), 0, max(T.get_value(), 1e-3),
                                                  n=max(int(60 * T.get_value()), 4), color=IM_COLOR, width=4, plane="xz", offset=r))

        def proj_lines():
            tt = T.get_value()
            zz = z(tt)
            p = ax.c2p(tt, zz.real, zz.imag)
            return VGroup(
                DashedLine(p, ax.c2p(tt, zz.real, -r), color=RE_COLOR, stroke_width=2, dash_length=0.07),
                DashedLine(p, ax.c2p(tt, r, zz.imag), color=IM_COLOR, stroke_width=2, dash_length=0.07),
            )

        projs = always_redraw(proj_lines)
        self.add(cos_sh, sin_sh, projs)
        self.play(T.animate.set_value(T_MAX), run_time=7, rate_func=linear)
        cos_lab = MathTex(r"\cos\omega t", font_size=36, color=RE_COLOR).move_to(ax.c2p(T_MAX + 0.6, 0, -r))
        sin_lab = MathTex(r"\sin\omega t", font_size=36, color=IM_COLOR).move_to(ax.c2p(T_MAX + 0.6, r, 0.9))
        self.face_camera(cos_lab, sin_lab)
        self.play(FadeIn(cos_lab), FadeIn(sin_lab), FadeOut(projs))
        self.remove(projs)
        self.beat("shadows: cos on the floor, sin on the wall")

        # change omega
        om_num = DecimalNumber(W0, num_decimal_places=1, include_sign=True, font_size=42, color=YELLOW)
        om_num.add_updater(lambda m: m.set_value(om.get_value()))
        om_read = VGroup(MathTex(r"\omega =", font_size=42, color=YELLOW), om_num).arrange(RIGHT, buff=0.15)
        om_read.next_to(formula, DOWN, buff=0.3, aligned_edge=RIGHT)
        om_num.add_updater(lambda m: m.next_to(om_read[0], RIGHT, buff=0.15))
        self.hud(om_read, live=True)
        self.play(FadeIn(om_read))
        self.play(om.animate.set_value(4.0), run_time=2.5)
        self.wait(0.5)
        self.play(om.animate.set_value(1.0), run_time=2.5)
        self.wait(0.5)
        self.play(om.animate.set_value(-2.0), run_time=3)
        self.beat("omega: how fast it spins (sign = direction)")
        self.play(om.animate.set_value(W0), run_time=2)
        om_num.clear_updaters()
        self.play(FadeOut(om_read), FadeOut(formula), FadeOut(cos_lab), FadeOut(sin_lab), FadeOut(cos_sh), FadeOut(sin_sh), FadeOut(walls))
        self.remove(cos_sh, sin_sh)
        self.helix_m, self.tip_arrow, self.T = helix, tip_arrow, T

    # ------------------------------------------------------------------
    def cosine_from_two_helices(self):
        ax = self.ax
        T = self.T
        self.set_title(r"$\cos\omega t$ from two helices")
        neg = complex_curve(ax, lambda t: np.exp(-1j * W0 * t), 0, T_MAX, n=500, color=PURPLE_B, width=4)
        pos_lab = MathTex(r"e^{j\omega t}", font_size=36, color=SIG).move_to(ax.c2p(T_MAX + 0.3, -0.3, 1.25))
        neg_lab = MathTex(r"e^{-j\omega t}", font_size=36, color=PURPLE_B).move_to(ax.c2p(T_MAX + 0.3, -0.3, -1.25))
        self.face_camera(pos_lab, neg_lab)
        self.play(Create(neg), FadeIn(pos_lab), FadeIn(neg_lab), run_time=2.5)
        self.beat("two helices, opposite twist", hold=1.0)

        formula = self.panel(MathTex(r"\cos\omega t = \frac{e^{j\omega t} + e^{-j\omega t}}{2}", font_size=46).to_corner(UR, buff=0.5))
        self.play(FadeIn(formula), T.animate.set_value(0), run_time=1.5)

        def arrows():
            tt = T.get_value()
            a = np.exp(1j * W0 * tt)
            b = np.exp(-1j * W0 * tt)
            return VGroup(
                cplane_arrow(ax, b, t=tt, color=PURPLE_B, width=4),
                cplane_arrow(ax, (a + b) / 2, t=tt, color=YELLOW, width=6),
            )

        arr = always_redraw(arrows)
        cos_curve = always_redraw(lambda: complex_curve(ax, lambda t: np.cos(W0 * t) + 0j, 0, max(T.get_value(), 1e-3),
                                                        n=max(int(60 * T.get_value()), 4), color=YELLOW, width=6))
        self.add(arr, cos_curve)
        self.play(T.animate.set_value(T_MAX), run_time=7, rate_func=linear)
        self.beat("the sum stays in the real plane")
        side = self.panel(Tex(r"side view: imaginary parts cancel", font_size=34, color=GREY_A).to_edge(DOWN, buff=0.4))
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.9, added_anims=[FadeIn(side)], run_time=2.5)
        self.beat("side view: sin and -sin cancel")
        top = self.panel(Tex(r"top view: real parts agree", font_size=34, color=GREY_A).to_edge(DOWN, buff=0.4))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.9, added_anims=[FadeOut(side), FadeIn(top), FadeOut(pos_lab), FadeOut(neg_lab)],
                         run_time=2.5)
        self.beat("top view: cos(omega t)")
        self.play(FadeOut(top), run_time=0.5)
        self.tip_arrow.clear_updaters()
        self.play(*[FadeOut(m) for m in (neg, formula)], run_time=0.8)


def _rotate_tracker(tracker, z_start, angle, scale=1.0):
    """Animate a ComplexValueTracker along an arc (rotation about 0), optionally scaling."""
    return UpdateFromAlphaFunc(
        tracker,
        lambda m, a: m.set_value(z_start * (1 + (scale - 1) * a) * np.exp(1j * angle * a)),
    )
