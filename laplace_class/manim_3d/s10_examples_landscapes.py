"""Examples 9.3, 9.4, 9.5 - landscapes, and the ROC as an intersection.

Scene: LandscapeExamples
  * 9.3  3e^{-2t}u(t) - 2e^{-t}u(t): each term has its own half-plane; the ROC
         is where both converge, Re{s} > -1
  * 9.4  e^{-2t}u(t) + e^{-t}cos(3t)u(t): cos splits into two exponentials, so a
         conjugate pair of poles; the ROC contains the j omega-axis and the slice
         there (the Fourier magnitude) peaks near omega = +-3
  * 9.5  delta(t) - 4/3 e^{-t}u(t) + 1/3 e^{2t}u(t): ROC Re{s} > 2 misses the
         j omega-axis - no Fourier transform; far away |X| -> 1 (the delta)
"""
from common3d import *

U = (-3, 3)
V = (-4, 4)
ZMAX = 4.0
RES = (44, 56)


def X93(s):
    return (s - 1) / ((s + 1) * (s + 2))


def X94(s):
    return (2 * s**2 + 5 * s + 12) / ((s + 2) * (s**2 + 2 * s + 10))


def X95(s):
    return (s - 1) ** 2 / ((s + 1) * (s - 2))


class LandscapeExamples(LScene):
    def construct(self):
        ax = splane_axes(u_range=U, v_range=V, z_max=ZMAX, x_length=6, y_length=8, z_length=3.0)
        self.ax = ax
        camera_at(self, ax.c2p(0, 0, 0.5), screen=(-1.9, -0.5), phi=60 * DEGREES, theta=-60 * DEGREES, zoom=0.74)
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        ticks = floor_ticks(ax, us=[-2, -1, 1, 2], vs=[-3, 3])
        self.add(floor, ax.x_axis, ax.y_axis, labs, ticks)
        self.ex93()
        self.ex94()
        self.ex95()
        self.clear_all()

    # ------------------------------------------------------------------
    def info(self, rows):
        g = VGroup(*rows).arrange(DOWN, aligned_edge=RIGHT, buff=0.18).to_corner(UR, buff=0.4)
        return self.panel(g)

    def ex93(self):
        ax = self.ax
        self.set_title("Example 9.3: the ROC is an intersection")
        info = self.info([
            MathTex(r"x(t) = 3e^{-2t}u(t) - 2e^{-t}u(t)", font_size=40),
            MathTex(r"3e^{-2t}u(t) \;\leftrightarrow\; \frac{3}{s+2},\ \ \mathrm{Re}\{s\} > -2", font_size=36, color=TEAL_B),
            MathTex(r"-2e^{-t}u(t) \;\leftrightarrow\; \frac{-2}{s+1},\ \ \mathrm{Re}\{s\} > -1", font_size=36, color=GOLD_B),
        ])
        self.play(FadeIn(info[0]), FadeIn(info[1][0]))
        r1 = roc_floor(ax, left=-2, color=TEAL_D, opacity=0.3)
        r2 = roc_floor(ax, left=-1, color=GOLD_D, opacity=0.3)
        p1, p2 = pole_x(ax, -2), pole_x(ax, -1)
        self.play(FadeIn(info[1][1]), FadeIn(r1), FadeIn(p1))
        self.play(FadeIn(info[1][2]), FadeIn(r2), FadeIn(p2))
        self.beat("each term has its own half-plane")
        both = roc_floor(ax, left=-1)
        res = self.panel(VGroup(
            MathTex(r"X(s) = \frac{s-1}{(s+1)(s+2)}", font_size=44),
            MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} > -1", font_size=40, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(info, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeOut(r1), FadeOut(r2), FadeIn(both), FadeIn(res))
        self.beat("both must converge: Re{s} > -1")

        surf = landscape(self.ax, X93, res=RES, roc=(-1, None))
        surf.save_state()
        surf.stretch(0.001, 2, about_point=ax.c2p(0, 0, 0))
        self.add(surf)
        zero = zero_o(ax, 1)
        self.play(Restore(surf), FadeIn(zero), run_time=2.5)
        self.beat("the landscape, ROC lit", hold=1.0)
        self.surf, self.roc, self.marks, self.info_m, self.res_m = surf, both, VGroup(p1, p2, zero), info, res

    # ------------------------------------------------------------------
    def ex94(self):
        ax = self.ax
        self.set_title("Example 9.4: decay with oscillation")
        info = self.info([
            MathTex(r"x(t) = e^{-2t}u(t) + e^{-t}\cos(3t)\,u(t)", font_size=38),
            MathTex(r"e^{-t}\cos 3t = \tfrac12 e^{-(1-3j)t} + \tfrac12 e^{-(1+3j)t}", font_size=36, color=GREY_A),
            MathTex(r"X(s) = \frac{2s^2+5s+12}{(s+2)(s^2+2s+10)}", font_size=40),
            MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} > -1", font_size=38, color=BLUE_B),
        ])
        surf2 = landscape(ax, X94, res=RES, roc=(-1, None))
        marks2 = VGroup(pole_x(ax, -2), pole_x(ax, complex(-1, 3)), pole_x(ax, complex(-1, -3)),
                        zero_o(ax, complex(-1.25, 2.107)), zero_o(ax, complex(-1.25, -2.107)))
        self.play(FadeOut(self.info_m), FadeOut(self.res_m), FadeIn(info), Transform(self.surf, surf2),
                  FadeTransform(self.marks, marks2), run_time=3)
        for a, b in zip(self.surf.submobjects, surf2.submobjects):
            a.is_cap = b.is_cap
        self.marks = marks2
        cc = self.panel(Tex(r"real signal $\Rightarrow$ complex poles come in conjugate pairs", font_size=34, color=POLE_COLOR)
                        .to_edge(DOWN, buff=0.35))
        self.play(FadeIn(cc))
        self.beat("poles at -2 and -1 +- 3j")
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        sl = jw_slice(ax, X94, zmax=ZMAX)
        jw = floor_vline(ax, 0, color=YELLOW, width=4)
        f_txt = self.panel(Tex(r"ROC contains the $j\omega$-axis: the slice is the Fourier magnitude, peaking near $\omega = \pm 3$",
                               font_size=32, color=YELLOW).to_edge(DOWN, buff=0.35))
        move_camera_to(self, ax.c2p(0, 0, 0.5), screen=(-1.9, -0.5), phi=72 * DEGREES, theta=-14 * DEGREES, zoom=0.74,
                       added_anims=[FadeOut(cc), FadeIn(f_txt)], run_time=3)
        self.play(Create(jw), Create(sl), UpdateFromAlphaFunc(self.surf, lambda m, a: set_roc_ghost(m, (-1, None), 0.9 - 0.4 * a)),
                  run_time=2.5)
        self.beat("the j omega slice: resonance peaks")
        self.play(FadeOut(sl), FadeOut(jw), FadeOut(f_txt))
        move_camera_to(self, ax.c2p(0, 0, 0.5), screen=(-1.9, -0.5), phi=60 * DEGREES, theta=-60 * DEGREES, zoom=0.74, run_time=2.5)
        self.info_m = info

    # ------------------------------------------------------------------
    def ex95(self):
        ax = self.ax
        self.set_title("Example 9.5: a signal with an impulse")
        info = self.info([
            MathTex(r"x(t) = \delta(t) - \tfrac43 e^{-t}u(t) + \tfrac13 e^{2t}u(t)", font_size=38),
            MathTex(r"\mathcal{L}\{\delta(t)\} = 1 \ \ (\text{every } s)", font_size=36, color=GREY_A),
            MathTex(r"X(s) = \frac{(s-1)^2}{(s+1)(s-2)}", font_size=42),
            MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\} > 2", font_size=38, color=BLUE_B),
        ])
        surf3 = landscape(ax, X95, res=RES, roc=(2, None))
        roc3 = roc_floor(ax, left=2)
        marks3 = VGroup(pole_x(ax, -1), pole_x(ax, 2), zero_o(ax, 1, radius=0.14), zero_o(ax, 1, radius=0.22))
        self.play(FadeOut(self.info_m), FadeIn(info), Transform(self.surf, surf3), FadeTransform(self.marks, marks3),
                  FadeTransform(self.roc, roc3), run_time=3)
        for a, b in zip(self.surf.submobjects, surf3.submobjects):
            a.is_cap = b.is_cap
        dz = Tex("double zero", font_size=32, color=ZERO_COLOR).move_to(ax.c2p(1, -0.75, 0))
        self.face_camera(dz)
        self.play(FadeIn(dz))
        self.beat("double zero at 1, poles at -1 and 2")
        jw = floor_vline(ax, 0, color=YELLOW, width=4)
        note = self.panel(VGroup(
            Tex(r"$j\omega$-axis outside the ROC: no Fourier transform", font_size=34, color=YELLOW),
            Tex(r"(the $e^{2t}$ term grows)", font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.35))
        self.play(Create(jw), FadeIn(note))
        self.beat("ROC Re{s} > 2: no Fourier transform")
        far = self.panel(Tex(r"far from the poles $|X(s)| \to 1$: the $\delta(t)$ part", font_size=34, color=GREY_A).to_edge(DOWN, buff=0.4))
        self.play(FadeOut(note), FadeIn(far))
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.beat("far from the poles the delta leaves height 1", hold=1.0)
