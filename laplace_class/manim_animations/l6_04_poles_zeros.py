"""Lecture 6 - Poles and zeros of rational Laplace transforms.

Scene: PoleZeroLandscape (3D)
  |X(s)| drawn as a landscape over the s-plane. Poles are infinitely tall
  "tent poles", zeros are points where the sheet touches the floor.
    Example 9.5: X(s) = (s-1)^2/((s+1)(s-2))              (two poles, double zero)
    Example 9.4: X(s) = (2s^2+5s+12)/((s+2)(s^2+2s+10))   (complex-conjugate poles)
  For 9.4 the ROC contains the j omega-axis, so the slice along it is |X(j omega)|,
  the Fourier magnitude.
"""
from common import *

ZMAX = 3.0
U_RANGE = (-3.5, 2.5)
V_RANGE = (-4.0, 4.0)
RES = (48, 64)


def X95(s):
    return (s - 1) ** 2 / ((s + 1) * (s - 2))


def X94(s):
    return (2 * s**2 + 5 * s + 12) / ((s + 2) * (s**2 + 2 * s + 10))


def mag(F, u, v):
    try:
        val = abs(F(complex(u, v)))
    except ZeroDivisionError:
        return ZMAX
    return min(val, ZMAX) if np.isfinite(val) else ZMAX


EX95 = dict(F=X95, poles=[-1, 2], zeros=[1, 1],
            tex=r"X(s) = \frac{(s-1)^2}{(s+1)(s-2)}", tag=r"\text{Example 9.5}")
EX94 = dict(F=X94, poles=[-2, -1 + 3j, -1 - 3j], zeros=[-1.25 + 2.107j, -1.25 - 2.107j],
            tex=r"X(s) = \frac{2s^2+5s+12}{(s+2)(s^2+2s+10)}", tag=r"\text{Example 9.4}")


class PoleZeroLandscape(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[*U_RANGE, 1], y_range=[*V_RANGE, 1], z_range=[0, ZMAX, 1],
            x_length=6, y_length=8, z_length=3,
            axis_config={"stroke_color": GREY_B, "include_tip": False},
        )
        floor = NumberPlane(
            x_range=[*U_RANGE, 1], y_range=[*V_RANGE, 1], x_length=6, y_length=8,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.35},
            axis_config={"stroke_opacity": 0},
        )
        floor.shift(axes.c2p(0, 0, 0) - floor.c2p(0, 0))
        sig_lab = MathTex(r"\sigma", font_size=40).move_to(axes.c2p(U_RANGE[1] + 0.35, 0, 0))
        jw_lab = MathTex(r"j\omega", font_size=40).move_to(axes.c2p(0, V_RANGE[1] + 0.4, 0))
        ticks = VGroup()
        for x in [-3, -2, -1, 1, 2]:
            ticks.add(MathTex(str(x), font_size=22, color=GREY_A).move_to(axes.c2p(x, -0.3, 0)))
        for y in [-3, 3]:
            ticks.add(MathTex(f"{y}j", font_size=22, color=GREY_A).move_to(axes.c2p(-0.4, y, 0)))

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=0.82)
        self.add(floor, axes, sig_lab, jw_lab, ticks)

        # ------------------------------------------------ helpers
        def markers(ex):
            g = VGroup()
            for p in ex["poles"]:
                g.add(pole_marker(axes.c2p(np.real(p), np.imag(p), 0), size=0.15, width=6))
            for i, z in enumerate(ex["zeros"]):
                r = 0.13 + 0.07 * sum(1 for w in ex["zeros"][:i] if abs(w - z) < 1e-9)  # nested rings for repeats
                g.add(zero_marker(axes.c2p(np.real(z), np.imag(z), 0), radius=r, width=5))
            return g

        def surface(ex):
            F = ex["F"]
            surf = Surface(
                lambda u, v: axes.c2p(u, v, mag(F, u, v)),
                u_range=U_RANGE, v_range=V_RANGE, resolution=RES,
                fill_opacity=0.88, stroke_width=0.25, stroke_color=BLUE_E,
            )
            surf.set_fill_by_value(
                axes=axes,
                colorscale=[(BLUE_E, 0.0), (BLUE_C, 0.5), (TEAL_C, 1.2), (YELLOW, 2.2), (RED_C, ZMAX)],
                axis=2,
            )
            return surf

        def slice_curve(ex):
            F = ex["F"]
            return ParametricFunction(
                lambda w: axes.c2p(0, w, mag(F, 0, w) + 0.03), t_range=[V_RANGE[0], V_RANGE[1], 0.02],
                color=YELLOW, stroke_width=7,
            )

        def formula(ex):
            f = MathTex(ex["tex"], font_size=34)
            tag = MathTex(ex["tag"], font_size=30, color=GREY_A)
            g = VGroup(tag, f).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.35)
            bg = BackgroundRectangle(g, fill_opacity=0.75, buff=0.15)
            return VGroup(bg, g)

        def fixed(*mobs):
            self.add_fixed_in_frame_mobjects(*mobs)
            for m in mobs:
                self.remove(m)

        # ------------------------------------------------ 1. flat pole-zero plot
        form = formula(EX95)
        fixed(form)
        self.play(FadeIn(form))
        mk = markers(EX95)
        self.play(LaggedStart(*[FadeIn(m, scale=2.5) for m in mk], lag_ratio=0.3))
        legend = VGroup(
            VGroup(pole_marker(ORIGIN, size=0.12, width=5), Tex(r"pole: $X(s) = \infty$", font_size=30)).arrange(RIGHT, buff=0.2),
            VGroup(zero_marker(ORIGIN, radius=0.1), Tex(r"zero: $X(s) = 0$", font_size=30)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4)
        legend_bg = BackgroundRectangle(legend, fill_opacity=0.75, buff=0.15)
        legend = VGroup(legend_bg, legend)
        fixed(legend)
        self.play(FadeIn(legend))
        self.wait(1)

        # ------------------------------------------------ 2. raise the landscape
        surf = surface(EX95)
        surf.save_state()
        surf.stretch(0.001, 2, about_point=axes.c2p(0, 0, 0))
        self.move_camera(phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.72, run_time=3)
        height_lab = MathTex(r"\text{height} = |X(s)|", font_size=32, color=YELLOW).next_to(form, DOWN, aligned_edge=LEFT, buff=0.2)
        fixed(height_lab)
        self.add(surf)
        self.play(Restore(surf), FadeIn(height_lab), run_time=3)
        tent = Tex(r"poles stick up forever, like tent poles", font_size=32, color=RED_B).to_edge(DOWN, buff=0.4)
        fixed(tent)
        self.play(FadeIn(tent))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        zero_note = Tex(r"the double zero at $s=1$ pins the sheet to the floor", font_size=32, color=GREEN_B).to_edge(DOWN, buff=0.4)
        fixed(zero_note)
        self.play(FadeOut(tent), FadeIn(zero_note))
        self.wait(4)
        self.stop_ambient_camera_rotation()

        # ------------------------------------------------ 3. morph to Example 9.4
        form94 = formula(EX94)
        fixed(form94)
        cc_note = Tex(r"real signal $\Rightarrow$ complex poles come in conjugate pairs", font_size=32, color=RED_B).to_edge(DOWN, buff=0.4)
        fixed(cc_note)
        surf94 = surface(EX94)
        self.move_camera(phi=60 * DEGREES, theta=-62 * DEGREES, run_time=2)
        self.play(
            Transform(surf, surf94), Transform(mk, markers(EX94)),
            FadeTransform(form, form94), FadeOut(zero_note),
            height_lab.animate.next_to(form94, DOWN, aligned_edge=LEFT, buff=0.2),
            run_time=3,
        )
        self.play(FadeIn(cc_note))
        self.begin_ambient_camera_rotation(rate=-0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # ------------------------------------------------ 4. the j omega slice = Fourier
        slice94 = slice_curve(EX94)
        jw_line = Line(axes.c2p(0, V_RANGE[0], 0), axes.c2p(0, V_RANGE[1], 0), color=YELLOW, stroke_width=4)
        fourier_note = Tex(r"ROC $\ni j\omega$-axis: the slice along it is $|X(j\omega)|$, the Fourier magnitude",
                           font_size=32, color=YELLOW).to_edge(DOWN, buff=0.4)
        fixed(fourier_note)
        self.move_camera(phi=70 * DEGREES, theta=-12 * DEGREES, run_time=3)
        self.play(FadeOut(cc_note), FadeIn(fourier_note), Create(jw_line))
        self.play(Create(slice94), surf.animate.set_fill(opacity=0.55), run_time=2.5)
        self.wait(3)

        # ------------------------------------------------ 5. back to the flat view + ROC
        roc = Polygon(
            axes.c2p(-1, V_RANGE[0], 0), axes.c2p(U_RANGE[1], V_RANGE[0], 0),
            axes.c2p(U_RANGE[1], V_RANGE[1], 0), axes.c2p(-1, V_RANGE[1], 0),
            stroke_width=0, fill_color=ROC_COLOR, fill_opacity=0.45,
        )
        roc_edge = DashedLine(axes.c2p(-1, V_RANGE[0], 0), axes.c2p(-1, V_RANGE[1], 0), color=BLUE_B)
        roc_note = Tex(r"right-sided: ROC $\mathrm{Re}\{s\} > -1$, to the right of the rightmost poles",
                       font_size=32, color=BLUE_B).to_edge(DOWN, buff=0.4)
        roc_note = VGroup(BackgroundRectangle(roc_note, fill_opacity=0.85, buff=0.1), roc_note)
        fixed(roc_note)
        self.play(FadeOut(slice94), FadeOut(jw_line), FadeOut(fourier_note))
        self.play(surf.animate.stretch(0.001, 2, about_point=axes.c2p(0, 0, 0)).set_fill(opacity=0.0).set_stroke(opacity=0), run_time=2.5)
        self.remove(surf)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.82, run_time=2.5)
        self.play(FadeIn(roc), Create(roc_edge), FadeIn(roc_note))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])
