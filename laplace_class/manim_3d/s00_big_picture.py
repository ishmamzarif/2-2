"""Opening - the big picture of what the Laplace transform does.

Scene: BigPicture
  * a signal x(t) = e^{-0.5t} cos(2t) u(t) becomes a landscape over the s-plane
  * the poles (where the oscillation and decay live) shoot up
  * the Fourier transform is just one slice of it, along the j omega-axis
  * roadmap for the talk
"""
from common3d import *


def Xs(s):
    return (s + 0.5) / ((s + 0.5) ** 2 + 4)


class BigPicture(LScene):
    def construct(self):
        ax = splane_axes(u_range=(-3, 2), v_range=(-4, 4), z_max=3, x_length=5.5, y_length=8, z_length=3)
        camera_at(self, ax.c2p(-0.5, 0, 0.6), screen=(1.6, -0.6), phi=62 * DEGREES, theta=-56 * DEGREES, zoom=0.72)

        # the signal
        sax = mini_axes(x_range=(0, 6, 1), y_range=(-1.1, 1.1, 1), width=4.4, height=2.2, x_label="t", y_label="x(t)", size=26)
        sax.to_corner(UL, buff=0.5).shift(0.5 * DOWN)
        sg = graph2d(sax, lambda t: np.exp(-0.5 * t) * np.cos(2 * t), 0, 6, color=SIG, width=4)
        s_eq = MathTex(r"x(t) = e^{-0.5t}\cos(2t)\,u(t)", font_size=36, color=SIG).next_to(sax, DOWN, buff=0.25)
        self.hud(sax, sg, s_eq)
        self.play(FadeIn(sax), Create(sg), FadeIn(s_eq), run_time=2)
        self.beat("a signal in time", hold=1.0)

        arrow = MathTex(r"\xrightarrow{\ \ \mathcal{L}\ \ }", font_size=60, color=YELLOW).next_to(s_eq, DOWN, buff=0.5)
        self.hud(arrow)
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        self.play(FadeIn(arrow), FadeIn(floor), Create(ax.x_axis), Create(ax.y_axis), FadeIn(labs))
        surf = landscape(ax, Xs, res=(40, 56), roc=(-0.5, None))
        surf.save_state()
        surf.stretch(0.001, 2, about_point=ax.c2p(0, 0, 0))
        self.add(surf)
        self.play(Restore(surf), run_time=3)
        x_eq = self.panel(MathTex(r"X(s) = \frac{s + 0.5}{(s+0.5)^2 + 4}", font_size=42).to_corner(UR, buff=0.4))
        self.play(FadeIn(x_eq))
        self.beat("becomes a landscape over the s-plane")

        poles = VGroup(pole_x(ax, complex(-0.5, 2)), pole_x(ax, complex(-0.5, -2)))
        p_lab = Tex("poles", font_size=36, color=POLE_COLOR).move_to(ax.c2p(-1.4, 2.0, 0))
        self.face_camera(p_lab)
        self.play(FadeIn(poles, scale=2), FadeIn(p_lab))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.beat("poles: the decay rate and the frequency")

        sl = jw_slice(ax, Xs, zmax=3)
        jw = floor_vline(ax, 0, color=YELLOW, width=4)
        f_lab = self.panel(Tex(r"Fourier transform = one slice ($j\omega$-axis)", font_size=34, color=YELLOW)
                           .next_to(x_eq, DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(Create(jw), Create(sl), FadeIn(f_lab), run_time=2)
        self.beat("Fourier is one slice of it")

        defn = self.panel(MathTex(r"X(s) = \int_{-\infty}^{\infty} x(t)\,e^{-st}\,dt", font_size=46, color=YELLOW)
                          .to_corner(DL, buff=0.5))
        self.play(FadeIn(defn))
        self.beat("the formula we will unpack")
        self.clear_all()

        road = VGroup(
            Tex(r"1.\ \ background: complex numbers, $e^{st}$, integrals, Fourier", font_size=40),
            Tex(r"2.\ \ how it comes up: LTI systems", font_size=40),
            Tex(r"3.\ \ what it is: definition, the $s$-plane", font_size=40),
            Tex(r"4.\ \ how it is used", font_size=40),
            Tex(r"5.\ \ the region of convergence", font_size=40),
            Tex(r"6.\ \ the inverse transform", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        self.set_title("Roadmap")
        self.hud(road)
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in road], lag_ratio=0.2), run_time=3)
        self.beat("roadmap")
