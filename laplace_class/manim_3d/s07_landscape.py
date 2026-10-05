"""What the Laplace transform looks like - the |X(s)| landscape over the s-plane.

Scene: SPlaneLandscape
  * X(s) is one complex number per point s: plot its size |X(s)| as height
  * Example 9.1, e^{-t}u(t) -> 1/(s+1): a pole is a chimney going up forever
  * the ROC Re{s} > -1 is the part that counts; the j omega slice is |X(j omega)|,
    the Fourier magnitude
  * Example 9.3: zeros touch the floor, poles shoot up; seen from above the
    landscape is the pole-zero plot
"""
from common3d import *

U = (-3, 2)
V = (-3, 3)
ZMAX = 4.0
RES = (40, 48)


def X91(s):
    return 1 / (s + 1)


def X93(s):
    return (s - 1) / ((s + 1) * (s + 2))


class SPlaneLandscape(LScene):
    def construct(self):
        ax = splane_axes(u_range=U, v_range=V, z_max=ZMAX, x_length=6, y_length=7, z_length=3.2)
        self.ax = ax
        camera_at(self, ax.c2p(-0.5, 0, 0.6), screen=(-1.0, -0.6), phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.82)
        floor = splane_floor(ax)
        labs = splane_labels(ax, z_label=r"|X|")
        self.face_camera(*labs)
        ticks = floor_ticks(ax, us=[-2, -1, 1], vs=[-2, 2])
        self.set_title(r"Picturing $X(s)$")
        info = VGroup(
            Tex(r"Example 9.1", font_size=34, color=GREY_A),
            MathTex(r"x(t) = e^{-t}u(t)", font_size=42),
            MathTex(r"X(s) = \frac{1}{s+1}", font_size=46),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.18).to_corner(UR, buff=0.4)
        info = self.panel(info)
        self.play(FadeIn(floor), Create(ax.x_axis), Create(ax.y_axis), FadeIn(labs[:2]), FadeIn(ticks), FadeIn(info))

        # one complex number per point
        s0 = complex(0.5, 1.0)
        dot = Dot3D(ax.c2p(s0.real, s0.imag, 0), radius=0.07, color=YELLOW)
        val = X91(s0)
        readout = self.panel(MathTex(rf"X(0.5 + j) = {val.real:.2f} {val.imag:+.2f}j", font_size=40, color=YELLOW)
                             .to_corner(DR, buff=0.5))
        self.play(FadeIn(dot, scale=2), FadeIn(readout))
        self.beat("each s gives a complex number X(s)")
        stem = Line(ax.c2p(s0.real, s0.imag, 0), ax.c2p(s0.real, s0.imag, abs(val)), color=YELLOW, stroke_width=5)
        mag = self.panel(MathTex(rf"|X(0.5+j)| = {abs(val):.2f}", font_size=40, color=YELLOW).to_corner(DR, buff=0.5))
        self.play(Create(stem), FadeTransform(readout, mag), Create(ax.z_axis), FadeIn(labs[2]))
        self.beat("its size becomes a height", hold=1.0)

        surf = landscape(ax, X91, res=RES)
        surf.save_state()
        surf.stretch(0.001, 2, about_point=ax.c2p(0, 0, 0))
        self.add(surf)
        self.play(Restore(surf), FadeOut(mag), FadeOut(ax.z_axis), FadeOut(labs[2]), run_time=3)
        height = self.panel(MathTex(r"\text{height} = |X(s)|", font_size=40, color=YELLOW).to_corner(DR, buff=0.5))
        self.play(FadeIn(height))
        self.play(FadeOut(dot), FadeOut(stem))
        self.beat("the landscape |X(s)|")

        pole = pole_x(ax, -1)
        pole_lab = Tex("pole", font_size=36, color=POLE_COLOR).move_to(ax.c2p(-1.3, -0.9, 0))
        self.face_camera(pole_lab)
        up = DashedLine(ax.c2p(-1, 0, ZMAX), ax.c2p(-1, 0, ZMAX * 1.2), color=POLE_COLOR, stroke_width=4, dash_length=0.1)
        inf_lab = MathTex(r"X \to \infty", font_size=36, color=POLE_COLOR).move_to(ax.c2p(-1, 0, ZMAX * 1.3))
        self.face_camera(inf_lab)
        self.play(FadeIn(pole, scale=2), FadeIn(pole_lab), Create(up), FadeIn(inf_lab))
        self.beat("a pole: X(s) blows up at s = -1")

        # the ROC
        roc = roc_floor(ax, left=-1)
        roc_txt = self.panel(MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} > -1", font_size=42, color=BLUE_B)
                             .next_to(info, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(roc), FadeIn(roc_txt), FadeOut(up), FadeOut(inf_lab), FadeOut(height))
        self.play(UpdateFromAlphaFunc(surf, lambda m, a: set_roc_ghost(m, (-1, None), opacity=0.9, ghost=0.9 - 0.78 * a)), run_time=1.5)
        self.beat("only the ROC part is the transform")

        # the j omega slice is the Fourier transform
        sl = jw_slice(ax, X91)
        jw = floor_vline(ax, 0, color=YELLOW, width=4)
        self.play(Create(jw), Create(sl), run_time=2)
        wall = Polygon(ax.c2p(U[0], V[0], 0), ax.c2p(U[0], V[1], 0), ax.c2p(U[0], V[1], 1.6), ax.c2p(U[0], V[0], 1.6),
                       stroke_color=GREY_C, stroke_width=1, fill_color=GREY_D, fill_opacity=0.15)
        tag_floor(wall)
        shadow = sl.copy()
        self.play(FadeIn(wall))
        self.play(shadow.animate.shift(ax.c2p(U[0], 0, 0) - ax.c2p(0, 0, 0)), run_time=2)
        f_lab = MathTex(r"|X(j\omega)| = \frac{1}{\sqrt{1+\omega^2}}", font_size=38, color=YELLOW).move_to(ax.c2p(U[0] - 0.2, 1.6, 2.2))
        self.face_camera(f_lab)
        f_txt = self.panel(Tex(r"the $j\omega$ slice = Fourier magnitude", font_size=36, color=YELLOW).to_edge(DOWN, buff=0.4))
        self.play(FadeIn(f_lab), FadeIn(f_txt))
        self.beat("slice along j omega: the Fourier transform")
        self.move_camera(theta=-20 * DEGREES, run_time=3)
        self.move_camera(theta=-58 * DEGREES, run_time=2)
        self.play(*[FadeOut(m) for m in (sl, shadow, wall, f_lab, f_txt, jw)])

        # Example 9.3: zeros and poles
        info2 = VGroup(
            Tex(r"Example 9.3", font_size=34, color=GREY_A),
            MathTex(r"x(t) = 3e^{-2t}u(t) - 2e^{-t}u(t)", font_size=40),
            MathTex(r"X(s) = \frac{s-1}{(s+1)(s+2)}", font_size=46),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.18).to_corner(UR, buff=0.4)
        info2 = self.panel(info2)
        surf2 = landscape(ax, X93, res=RES, roc=(-1, None))
        poles2 = VGroup(pole_x(ax, -1), pole_x(ax, -2))
        zero = zero_o(ax, 1)
        zero_lab = Tex("zero", font_size=36, color=ZERO_COLOR).move_to(ax.c2p(1.3, -0.8, 0))
        pole_lab2 = Tex("poles", font_size=36, color=POLE_COLOR).move_to(ax.c2p(-1.5, -1.0, 0))
        self.face_camera(zero_lab, pole_lab2)
        roc_txt2 = self.panel(MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} > -1", font_size=42, color=BLUE_B)
                              .next_to(info2, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeTransform(info, info2), FadeTransform(roc_txt, roc_txt2), Transform(surf, surf2),
                  FadeTransform(pole, poles2), FadeTransform(pole_lab, pole_lab2), run_time=3)
        for a, b in zip(surf.submobjects, surf2.submobjects):
            a.is_cap = b.is_cap
        self.play(FadeIn(zero, scale=2), FadeIn(zero_lab))
        rule = self.panel(VGroup(
            MathTex(r"X(s) = \frac{N(s)}{D(s)}", font_size=40),
            MathTex(r"\text{zeros: } N(s) = 0 \ (\circ)", font_size=36, color=ZERO_COLOR),
            MathTex(r"\text{poles: } D(s) = 0 \ (\times)", font_size=36, color=POLE_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.45))
        self.play(FadeIn(rule))
        self.beat("zeros touch the floor, poles shoot up")
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        # from above: the pole-zero plot
        self.play(FadeOut(rule))
        move_camera_to(self, ax.c2p(-0.5, 0, 0), screen=(-1.6, -0.3), phi=0, theta=-90 * DEGREES, zoom=0.95, run_time=3)
        self.play(UpdateFromAlphaFunc(surf, lambda m, a: set_roc_ghost(m, (-1, None), opacity=0.9 - 0.55 * a, ghost=0.12 * (1 - a))),
                  run_time=1.5)
        self.beat("seen from above: the pole-zero plot")
