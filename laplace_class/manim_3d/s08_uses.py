"""How the Laplace transform is used - calculus becomes algebra, poles become behaviour.

Scene: HowItsUsed
  * the velocity of e^{st} is s times its position: d/dt <-> multiply by s
  * so a differential equation turns into algebra, H(s) = 1/(s^2 + 2s + 5)
  * each pole p seeds a mode e^{pt}: a spiral rising out of the s-plane
  * move the poles: left half-plane decays (stable), the j omega-axis rings
    forever, the right half-plane blows up (unstable) - Fourier can't even
    describe that last one, Laplace can
"""
from common3d import *

T_MAX = 8.0
S0 = complex(-0.15, 1.5)


class HowItsUsed(LScene):
    def construct(self):
        self.derivative()
        self.ode()
        self.pole_seeds()
        self.summary()
        self.clear_all()

    # ------------------------------------------------------------------
    def derivative(self):
        ax = complex_time_axes(t_range=(0, T_MAX, 1), r=1.6, t_length=9, r_length=3.6)
        camera_at(self, ax.c2p(T_MAX / 2, 0, 0), screen=(-1.6, -0.7), phi=68 * DEGREES, theta=-40 * DEGREES, zoom=0.82)
        self.set_title(r"Derivative $\leftrightarrow$ multiply by $s$")
        labs = ct_labels(ax)
        self.face_camera(*labs)
        helix = complex_curve(ax, lambda t: np.exp(S0 * t), 0, T_MAX, n=600, rmax=1.6, color=SIG, width=4)
        self.play(Create(ax), FadeIn(labs))
        self.play(Create(helix), run_time=2.5)
        T = ValueTracker(0.6)

        def arrows():
            tt = T.get_value()
            p = np.exp(S0 * tt)
            v = 0.7 * S0 * p
            return VGroup(
                cplane_arrow(ax, p, t=tt, color=SIG, width=5, tip=0.18),
                cplane_arrow(ax, p + v, t=tt, start=p, color=YELLOW, width=5, tip=0.18),
            )

        arr = always_redraw(arrows)
        pos_lab = self.hud(MathTex(r"\text{position } e^{st}", font_size=36, color=SIG))
        vel_lab = self.hud(MathTex(r"\text{velocity } \tfrac{d}{dt}e^{st}", font_size=36, color=YELLOW))
        VGroup(pos_lab, vel_lab).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.5)
        self.play(FadeIn(arr), FadeIn(pos_lab), FadeIn(vel_lab))
        self.add(arr)
        self.play(T.animate.set_value(4.5), run_time=5, rate_func=linear)
        self.play(T.animate.set_value(1.6), run_time=2)
        eq = self.panel(VGroup(
            MathTex(r"\frac{d}{dt}\,e^{st} = s\,e^{st}", font_size=48),
            Tex(r"velocity = $s$ $\times$ position", font_size=36, color=YELLOW),
            Tex(r"(turned by $\angle s$, stretched by $|s|$)", font_size=32, color=GREY_A),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).to_corner(UR, buff=0.45))
        self.play(FadeIn(eq))
        self.beat("velocity = s times position")
        rule = self.panel(MathTex(r"\frac{d}{dt} \;\longleftrightarrow\; \times\, s", font_size=56, color=YELLOW)
                          .next_to(eq, DOWN, buff=0.45, aligned_edge=RIGHT))
        self.play(FadeIn(rule, scale=1.2))
        self.beat("so d/dt becomes multiplication by s")
        self.clear_all()

    # ------------------------------------------------------------------
    def ode(self):
        self.set_title("Differential equation $\\to$ algebra")
        lines = VGroup(
            MathTex(r"y''(t) + 2y'(t) + 5y(t) = x(t)", font_size=50),
            MathTex(r"\big\downarrow\ \mathcal{L}", font_size=44, color=GREY_A),
            MathTex(r"s^2\,Y(s) + 2s\,Y(s) + 5\,Y(s) = X(s)", font_size=50),
            MathTex(r"H(s) = \frac{Y(s)}{X(s)} = \frac{1}{s^2 + 2s + 5}", font_size=54, color=YELLOW),
            MathTex(r"\text{poles: } s = -1 \pm 2j", font_size=46, color=POLE_COLOR),
        ).arrange(DOWN, buff=0.35)
        self.hud(lines)
        self.play(FadeIn(lines[0]))
        self.beat("a mass-spring-damper style ODE", hold=1.0)
        self.play(FadeIn(lines[1]), FadeIn(lines[2], shift=0.2 * DOWN))
        self.beat("every d/dt becomes a factor s")
        self.play(FadeIn(lines[3], shift=0.2 * DOWN))
        self.play(FadeIn(lines[4], shift=0.2 * DOWN))
        self.beat("the system function and its poles")
        self.play(FadeOut(lines))

    # ------------------------------------------------------------------
    def pole_seeds(self):
        U, V, TZ = (-2.5, 1.5), (-3, 3), 5.0
        ax = ThreeDAxes(x_range=[U[0], U[1], 1], y_range=[V[0], V[1], 1], z_range=[0, TZ, 1],
                        x_length=5.5, y_length=7, z_length=4.2,
                        axis_config={"stroke_color": AXIS_COLOR, "include_tip": False, "stroke_width": 2, "tick_size": 0.05})
        camera_at(self, ax.c2p(-0.5, 0, 1.6), screen=(-1.6, -0.4), phi=70 * DEGREES, theta=-62 * DEGREES, zoom=0.8)
        self.set_title(r"Each pole $p$ seeds a mode $e^{pt}$")
        floor = splane_floor(ax)
        labs = splane_labels(ax)
        self.face_camera(*labs)
        lhp = roc_floor(ax, right=0, color=GREEN_E, opacity=0.25, edges=False)
        rhp = roc_floor(ax, left=0, color=RED_E, opacity=0.25, edges=False)
        jw = floor_vline(ax, 0, color=YELLOW, width=4)
        st_lab = Tex("stable", font_size=34, color=GREEN_B).move_to(ax.c2p(-1.6, -3.5, 0))
        un_lab = Tex("unstable", font_size=34, color=RED_B).move_to(ax.c2p(0.8, -3.5, 0))
        t_lab = MathTex("t", font_size=38, color=LABEL_COLOR).move_to(ax.c2p(U[0], V[1], TZ + 0.3))
        self.face_camera(st_lab, un_lab, t_lab)
        t_axis = Line(ax.c2p(U[0], V[1], 0), ax.c2p(U[0], V[1], TZ), color=AXIS_COLOR, stroke_width=2)
        self.play(FadeIn(floor), Create(ax.x_axis), Create(ax.y_axis), FadeIn(labs), Create(t_axis), FadeIn(t_lab))

        sig = ValueTracker(-1.0)
        W = 2.0
        K = 0.95  # drawn radius of a mode at t = 0

        def seeds():
            g = VGroup()
            for wsign, col in ((1, SIG), (-1, PURPLE_B)):
                p = complex(sig.get_value(), wsign * W)
                ts = np.linspace(0, TZ, 400)
                zs = K * np.exp(p * ts)
                keep = np.abs(zs) < 1.6
                for run in true_runs(keep):
                    g.add(polyline(pts(ax, p.real + zs[run].real, p.imag + zs[run].imag, ts[run]), col, 4))
                g.add(pole_x(ax, p))
            return g

        modes = always_redraw(seeds)
        self.play(FadeIn(lhp), FadeIn(rhp), Create(jw), FadeIn(st_lab), FadeIn(un_lab))
        self.play(Create(modes), run_time=3)
        self.add(modes)
        self.beat("poles at -1 +- 2j: two spirals rise")

        # impulse response, as a flat plot
        hax = mini_axes(x_range=(0, 6, 1), y_range=(-1, 1, 1), width=4.6, height=2.2, x_label="t", y_label="h(t)")
        hax.to_corner(DR, buff=0.5).shift(0.3 * UP)
        hbg = BackgroundRectangle(hax, fill_color=PANEL_BG, fill_opacity=0.85, buff=0.15)
        hbg.hud_layer = -1

        def h_curve():
            sg = sig.get_value()
            return graph2d(hax, lambda t: np.exp(sg * t) * np.sin(W * t) / W * 1.6, 0, 6, n=300, color=YELLOW, width=4)

        hplot = always_redraw(h_curve)
        h_eq = MathTex(r"h(t) = \tfrac{1}{2}e^{\sigma t}\sin(2t)\,u(t)", font_size=34, color=YELLOW).next_to(hax, UP, buff=0.15)
        self.hud(hbg, hax, h_eq)
        self.hud(hplot, live=True)
        self.play(FadeIn(hbg), FadeIn(hax), FadeIn(h_eq))
        self.play(Create(hplot))
        self.add(hplot)
        self.beat("together: a decaying oscillation h(t)")

        status = [None]

        def say(text, color):
            new = self.panel(Tex(text, font_size=40, color=color).to_corner(UR, buff=0.5).shift(0.5 * DOWN))
            anims = [FadeIn(new)]
            if status[0] is not None:
                anims.append(FadeOut(status[0]))
            status[0] = new
            return anims

        self.play(sig.animate.set_value(-0.3), *say("closer to the axis: slower decay", GREEN_B), run_time=3)
        self.beat("closer to the j omega-axis: rings longer")
        self.play(sig.animate.set_value(0.0), *say("on the axis: rings forever", YELLOW), run_time=3)
        self.beat("on the axis: sustained oscillation")
        self.play(sig.animate.set_value(0.22), *say("right half-plane: blows up", RED_B), run_time=3)
        self.beat("right half-plane: unstable")
        note = self.panel(VGroup(
            Tex(r"$h(t)$ grows: no Fourier transform", font_size=34),
            Tex(r"Laplace still works (ROC $\mathrm{Re}\{s\} > 0.22$)", font_size=34, color=GOOD),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12).next_to(status[0], DOWN, buff=0.3, aligned_edge=RIGHT))
        self.play(FadeIn(note))
        self.beat("Fourier fails here, Laplace doesn't")
        self.play(sig.animate.set_value(-1.0), FadeOut(note), *say("back to stable", GREEN_B), run_time=3)
        self.clear_all()

    # ------------------------------------------------------------------
    def summary(self):
        self.set_title("Why engineers use it")
        items = VGroup(
            MathTex(r"\text{convolution} \;\to\; \text{multiplication:}\quad Y(s) = H(s)\,X(s)", font_size=42),
            MathTex(r"\text{differential equations} \;\to\; \text{algebra}", font_size=42),
            MathTex(r"\text{pole positions} \;\to\; \text{stability}", font_size=42),
            MathTex(r"\text{feedback:}\quad \frac{Y}{X} = \frac{G(s)}{1 + G(s)K(s)}", font_size=42),
            MathTex(r"\text{works for growing signals and unstable systems}", font_size=42, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        self.hud(items)
        for it in items:
            self.play(FadeIn(it, shift=0.2 * RIGHT), run_time=0.8)
        self.beat("the toolkit")
