"""Lecture 6 - The inverse Laplace transform  (restructured: one idea per frame).

InverseLaplaceBuildUp
    Ch.1  Where does it come from?   motivation -> Laplace is a Fourier transform in disguise
                                     -> invert -> multiply by e^{sigma t} -> change of variable
                                     -> the Bromwich integral
    Ch.2  The Bromwich integral in action   (unchanged simulation)
    Ch.3  Closing the contour        Cauchy residues -> add an arc -> residue = e^{-t}
                                     -> t < 0 closes to the right -> the ROC decides which poles are inside
PartialFractionsAndROC
    Ch.1  A better tool for rational X(s)   why Bromwich is heavy -> partial fractions
                                            -> the fundamental pair, right- and left-sided
    Ch.2  The slide problem                 1/((s+1)(s+2)): expansion, then ROC 1, ROC 2, ROC 3 one by one

Every chapter can also be rendered on its own while iterating, e.g.
    manim -pql l6_05_inverse.py IL_Ch1_Derivation
"""
from common import *

T_GRID = np.linspace(-2, 4, 361)
DW = 0.02


# ======================================================================
#  small helpers
# ======================================================================
def reconstruct(sigma, W):
    """(1/2pi) \\int_{-W}^{W} X(sigma + j w) e^{(sigma + j w) t} dw  for X(s) = 1/(s+1)."""
    if W < 1e-3:
        return np.zeros_like(T_GRID)
    n = max(int(W / DW), 1)
    w = (np.arange(n) + 0.5) * (W / n)
    Xv = 1.0 / (sigma + 1 + 1j * w)
    E = np.exp(np.outer(T_GRID, sigma + 1j * w))
    # conjugate symmetry: the -w half is the complex conjugate of the +w half
    return (E @ Xv).real * (W / n) / np.pi


def chapter_card(scene, tag, heading, sub=None):
    """Full-screen chapter title so each chapter starts on a clean frame."""
    parts = [Tex(tag, font_size=30, color=GREY_B), Tex(heading, font_size=50)]
    if sub:
        parts.append(Tex(sub, font_size=30, color=GREY_A))
    g = VGroup(*parts).arrange(DOWN, buff=0.35)
    scene.play(FadeIn(g, shift=UP * 0.2))
    scene.wait(1.4)
    scene.play(FadeOut(g))


def note(text, color=GREY_A, fs=30, maxw=12.4):
    """Caption text.  Long captions are shrunk to maxw so nothing runs off screen
    (right-hand-panel captions pass maxw=6.3 and use explicit \\ line breaks)."""
    m = Tex(text, font_size=fs, color=color)
    if m.width > maxw:
        m.scale_to_fit_width(maxw)
    return m


def morph(a, b):
    """Part-by-part ReplacementTransform between two MathTex with the same number of parts."""
    return [ReplacementTransform(a[i], b[i]) for i in range(len(a))]


def cross_marker(sp, x, y, color=RED_C):
    return MathTex(r"\times", color=color, font_size=44).move_to(sp.c2p(x, y))


def contour_pieces(sp, sigma, R, side):
    """Bromwich line (upwards) + closing arc.  side = 'left' (counter-clockwise) or 'right' (clockwise)."""
    sign = 1 if side == "left" else -1
    vert = Line(sp.c2p(sigma, -R), sp.c2p(sigma, R), color=YELLOW, stroke_width=6)
    arc = ParametricFunction(
        lambda th: sp.c2p(sigma + R * np.cos(PI / 2 + sign * th), R * np.sin(PI / 2 + sign * th)),
        t_range=[0, PI], color=TEAL_C if side == "left" else ORANGE, stroke_width=5)
    return vert, arc


def closed_path(vert, arc):
    p = VMobject()
    p.append_points(vert.get_points())
    p.append_points(arc.get_points())
    return p


# ======================================================================
#  INVERSE LAPLACE BUILD-UP
# ======================================================================
class InverseLaplaceBuildUp(Scene):
    def construct(self):
        self.chapter1()
        self.chapter2()
        self.chapter3()

    # ------------------------------------------------------------------
    #  CHAPTER 1 : derivation, one idea per frame
    # ------------------------------------------------------------------
    def chapter1(self):
        chapter_card(self, "Inverse Laplace  -  chapter 1", "Where does the inverse come from?",
                     "we will build it from the inverse Fourier transform")
        self.c1_motivation()
        self.c1_split_exponent()
        self.c1_taming()
        self.c1_inverse_fourier()
        self.c1_multiply_back()
        self.c1_change_of_variable_geometry()
        self.c1_change_of_variable_algebra()
        self.c1_bromwich()

    # --- 1. what are we even asking? ----------------------------------
    def c1_motivation(self):
        title = make_title("Going backwards")
        xt = MathTex(r"x(t)", font_size=64).move_to(LEFT * 4 + UP * 1.4)
        Xs = MathTex(r"X(s)", font_size=64).move_to(RIGHT * 4 + UP * 1.4)
        fwd = Arrow(xt.get_right() + RIGHT * 0.4, Xs.get_left() + LEFT * 0.4, buff=0, color=TEAL_C)
        fl = MathTex(r"\mathcal{L}", font_size=46, color=TEAL_C).next_to(fwd, UP, buff=0.12)
        defn = MathTex(r"X(s)=\int_{-\infty}^{\infty}x(t)\,e^{-st}\,dt", font_size=40).next_to(fwd, DOWN, buff=0.3)
        self.play(Write(title))
        self.play(Write(xt))
        self.play(GrowArrow(fwd), Write(fl))
        self.play(Write(Xs))
        self.play(Write(defn))
        self.wait(1)

        back = CurvedArrow(Xs.get_bottom() + DOWN * 0.15, xt.get_bottom() + DOWN * 0.15, angle=-TAU / 4,
                           color=YELLOW)
        q = MathTex(r"?", font_size=64, color=YELLOW).move_to(DOWN * 1.35)
        ask = note(r"Can we somehow \emph{undo} the integral?", color=YELLOW, fs=36).move_to(DOWN * 2.3)
        self.play(Create(back), FadeIn(q))
        self.play(FadeIn(ask))
        self.wait(1.2)

        fourier = MathTex(r"\mathcal{F}^{-1}", font_size=58, color=GOLD).move_to(q)
        idea = note(r"We already know one way back: the \textbf{inverse Fourier transform}", color=GOLD, fs=34)
        idea.move_to(ask)
        self.play(FadeTransform(q, fourier), FadeTransform(ask, idea))
        self.wait(0.6)
        hook = note(r"So: can we turn the Laplace transform \emph{into} a Fourier transform?", fs=32)
        hook.next_to(idea, DOWN, buff=0.35)
        self.play(FadeIn(hook, shift=UP * 0.15))
        self.wait(2)
        fade_all(self)

    # --- 2. split e^{-st} -----------------------------------------------
    def c1_split_exponent(self):
        title = make_title(r"Split $s$ into its two parts")
        s_def = MathTex(r"s", r"=", r"\sigma", r"+", r"j\omega", font_size=56).move_to(UP * 2.0)
        s_def[2].set_color(TEAL_C)
        s_def[4].set_color(GOLD)
        lab_sig = note("real part: growth / decay", color=TEAL_C, fs=28).next_to(s_def[2], UP, buff=0.55)
        lab_om = note("imaginary part: frequency", color=GOLD, fs=28).next_to(s_def[4], DOWN, buff=0.55)
        a1 = Arrow(lab_sig.get_bottom(), s_def[2].get_top(), buff=0.08, color=TEAL_C, stroke_width=3)
        a2 = Arrow(lab_om.get_top(), s_def[4].get_bottom(), buff=0.08, color=GOLD, stroke_width=3)
        self.play(Write(title))
        self.play(Write(s_def))
        self.play(FadeIn(lab_sig), GrowArrow(a1))
        self.play(FadeIn(lab_om), GrowArrow(a2))
        self.wait(1)
        self.play(FadeOut(VGroup(lab_sig, lab_om, a1, a2)), s_def.animate.scale(0.7).to_corner(UL, buff=0.7).shift(DOWN * 0.9))

        e1 = MathTex(r"X(s)", "=", r"\int_{-\infty}^{\infty}", r"x(t)", r"e^{-st}", r"dt", font_size=52)
        e2 = MathTex(r"X(\sigma+j\omega)", "=", r"\int_{-\infty}^{\infty}", r"x(t)", r"e^{-(\sigma+j\omega)t}", r"dt",
                     font_size=52)
        e3 = MathTex(r"X(\sigma+j\omega)", "=", r"\int_{-\infty}^{\infty}", r"x(t)", r"e^{-\sigma t}",
                     r"e^{-j\omega t}", r"dt", font_size=52)
        for e in (e1, e2, e3):
            e.move_to(DOWN * 0.4)
        self.play(Write(e1))
        self.wait(0.5)
        self.play(TransformMatchingTex(e1, e2))
        self.wait(0.5)
        self.play(TransformMatchingTex(e2, e3))
        e3[4].set_color(TEAL_C)
        e3[5].set_color(GOLD)
        self.wait(0.3)
        self.play(Indicate(e3[4], color=TEAL_C, scale_factor=1.25), Indicate(e3[5], color=GOLD, scale_factor=1.25))
        self.wait(0.8)

        # regroup:  [x(t) e^{-sigma t}] e^{-j w t}
        e4 = MathTex(r"X(\sigma+j\omega)", "=", r"\int_{-\infty}^{\infty}", r"\big[x(t)\,e^{-\sigma t}\big]",
                     r"\,e^{-j\omega t}", r"dt", font_size=52).move_to(e3)
        e4[3].set_color(TEAL_C)
        e4[4].set_color(GOLD)
        self.play(TransformMatchingTex(e3, e4))
        box = SurroundingRectangle(e4[3], color=YELLOW, buff=0.12)
        g_lab = MathTex(r"g(t)", font_size=44, color=YELLOW).next_to(box, DOWN, buff=0.45)
        g_arrow = Arrow(g_lab.get_top(), box.get_bottom(), buff=0.05, color=YELLOW, stroke_width=3)
        self.play(Create(box), FadeIn(g_lab), GrowArrow(g_arrow))
        self.wait(0.6)
        kernel = note(r"this is exactly the Fourier kernel $e^{-j\omega t}$", color=GOLD, fs=30).next_to(e4[4], UP, buff=0.8)
        k_arrow = Arrow(kernel.get_bottom(), e4[4].get_top(), buff=0.05, color=GOLD, stroke_width=3)
        self.play(FadeIn(kernel), GrowArrow(k_arrow))
        self.wait(2)
        fade_all(self)

    # --- 3. what does x(t) e^{-sigma t} do? ---------------------------------
    def c1_taming(self):
        title = make_title(r"Why bother with $e^{-\sigma t}$?  It tames the signal")
        ax = signal_axes(x_range=(-1, 4, 1), y_range=(0, 4, 1), x_length=8.2, y_length=3.9)
        ax.move_to(DOWN * 0.15)
        sigma = ValueTracker(0.0)
        a = 0.5  # x(t) = e^{0.5 t} u(t): a growing signal

        def curve(f, color, w=5, dashed=False):
            g = ax.plot(lambda t: min(f(t), 3.95), x_range=[0.0, 4], color=color, stroke_width=w)
            return DashedVMobject(g, num_dashes=40) if dashed else g

        xt_graph = curve(lambda t: np.exp(a * t), GREY_B, 3, dashed=True)
        xt_lab = MathTex(r"x(t)=e^{0.5t}u(t)", font_size=32, color=GREY_B).next_to(ax.c2p(0.25, 3.4), RIGHT, buff=0.1)
        g_graph = always_redraw(lambda: curve(lambda t: np.exp((a - sigma.get_value()) * t), YELLOW))
        g_lab = MathTex(r"g(t)=x(t)\,e^{-\sigma t}", font_size=36, color=YELLOW).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        s_num = DecimalNumber(0.0, num_decimal_places=2, font_size=40)
        s_num.add_updater(lambda m: m.set_value(sigma.get_value()))
        s_read = VGroup(MathTex(r"\sigma=", font_size=40), s_num).arrange(RIGHT, buff=0.12)
        s_read.next_to(ax, UP, buff=0.2).align_to(ax, RIGHT)
        self.play(Write(title))
        self.play(Create(ax), FadeIn(xt_graph), FadeIn(xt_lab))
        t1 = note(r"$\sigma=0$: the signal blows up, so $\int |x|\,dt$ diverges. No Fourier transform.",
                  color=RED_B, fs=30).next_to(ax, DOWN, buff=0.3)
        self.add(g_graph)
        self.play(FadeIn(g_lab), FadeIn(s_read), FadeIn(t1))
        self.wait(1.5)
        t2 = note(r"turn up $\sigma$: multiplying by $e^{-\sigma t}$ drags the tail down", color=YELLOW,
                  fs=30).move_to(t1)
        self.play(FadeTransform(t1, t2))
        self.play(sigma.animate.set_value(1.0), run_time=4)
        t3 = note(r"once $\sigma$ is large enough, $g(t)$ decays and its Fourier transform exists", color=GOOD,
                  fs=30).move_to(t1)
        self.play(FadeTransform(t2, t3))
        self.wait(1.2)
        t4 = note(r"that range of good $\sigma$ values is the \textbf{ROC}", color=BLUE_B, fs=32).next_to(t3, DOWN, buff=0.25)
        self.play(FadeIn(t4, shift=UP * 0.1))
        self.wait(2)
        fade_all(self)

    # --- 4. invert the Fourier transform ------------------------------------
    def c1_inverse_fourier(self):
        title = make_title(r"A slice of $X(s)$ is a Fourier transform")
        fact = MathTex(r"X(\sigma_0+j\omega)", "=", r"\mathcal{F}\{x(t)\,e^{-\sigma_0 t}\}", font_size=52)
        fact.move_to(UP * 1.7)
        self.play(Write(title))
        self.play(Write(fact))
        defs = VGroup(
            MathTex(r"g(t)=x(t)\,e^{-\sigma_0 t}", font_size=44, color=TEAL_C),
            MathTex(r"G(j\omega)=X(\sigma_0+j\omega)", font_size=44, color=GOLD),
        ).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        self.play(FadeIn(defs[0], shift=UP * 0.15))
        self.play(FadeIn(defs[1], shift=UP * 0.15))
        self.wait(1)

        d1 = MathTex(r"g(t)", "=", r"\frac{1}{2\pi}", r"\int_{-\infty}^{\infty}", r"G(j\omega)", r"e^{j\omega t}",
                     r"d\omega", font_size=52).move_to(DOWN * 1.5)
        d1[0].set_color(TEAL_C)
        d1[4].set_color(GOLD)
        inv = note(r"inverse Fourier transform", fs=30).next_to(d1, DOWN, buff=0.45)
        self.play(Write(d1), FadeIn(inv))
        self.wait(1)
        d2 = MathTex(r"x(t)\,e^{-\sigma_0 t}", "=", r"\frac{1}{2\pi}", r"\int_{-\infty}^{\infty}",
                     r"X(\sigma_0+j\omega)", r"e^{j\omega t}", r"d\omega", font_size=52).move_to(d1)
        d2[0].set_color(TEAL_C)
        d2[4].set_color(GOLD)
        self.play(*morph(d1, d2), run_time=2)
        self.wait(0.5)
        self.play(Create(SurroundingRectangle(d2, color=YELLOW, buff=0.2)))
        self.wait(2)
        fade_all(self)

    # --- 5. multiply by e^{sigma t} -------------------------------------------
    def c1_multiply_back(self):
        title = make_title(r"We want $x(t)$, not $x(t)e^{-\sigma t}$")
        s1 = MathTex(r"x(t)", r"e^{-\sigma t}", "=", r"\frac{1}{2\pi}", r"\int_{-\infty}^{\infty}",
                     r"X(\sigma+j\omega)", r"e^{j\omega t}", r"d\omega", font_size=50).move_to(UP * 0.8)
        self.play(Write(title))
        self.play(Write(s1))
        self.wait(0.8)
        cap = note(r"multiply \emph{both} sides by $e^{\sigma t}$", color=YELLOW, fs=34).move_to(DOWN * 1.8)
        self.play(FadeIn(cap))
        s2 = MathTex(r"x(t)", r"e^{-\sigma t}", r"e^{\sigma t}", "=", r"e^{\sigma t}", r"\frac{1}{2\pi}",
                     r"\int_{-\infty}^{\infty}", r"X(\sigma+j\omega)", r"e^{j\omega t}", r"d\omega",
                     font_size=50).move_to(s1)
        s2[2].set_color(YELLOW)
        s2[4].set_color(YELLOW)
        self.play(TransformMatchingTex(s1, s2), run_time=1.8)
        self.wait(0.8)

        # left side: e^{-sigma t} e^{sigma t} = 1
        cancel = VGroup(s2[1], s2[2])
        cross = Cross(cancel, stroke_color=RED_C, stroke_width=6)
        cap2 = note(r"on the left they cancel: $e^{-\sigma t}e^{\sigma t}=1$", color=GREY_A, fs=30).move_to(cap)
        self.play(FadeTransform(cap, cap2), Create(cross))
        self.wait(0.6)
        self.play(FadeOut(cross), FadeOut(cancel))

        # right side: pull e^{sigma t} next to e^{j w t}
        s3 = MathTex(r"x(t)", "=", r"\frac{1}{2\pi}", r"\int_{-\infty}^{\infty}", r"X(\sigma+j\omega)",
                     r"e^{\sigma t}", r"e^{j\omega t}", r"d\omega", font_size=50).move_to(UP * 0.8)
        s3[5].set_color(YELLOW)
        cap3 = note(r"on the right, $e^{\sigma t}$ slides inside the integral (it does not depend on $\omega$)",
                    color=GREY_A, fs=30).move_to(cap)
        self.play(
            ReplacementTransform(s2[0], s3[0]), ReplacementTransform(s2[3], s3[1]),
            ReplacementTransform(s2[4], s3[5], path_arc=-PI / 2),
            ReplacementTransform(s2[5], s3[2]), ReplacementTransform(s2[6], s3[3]),
            ReplacementTransform(s2[7], s3[4]), ReplacementTransform(s2[8], s3[6]),
            ReplacementTransform(s2[9], s3[7]),
            FadeTransform(cap2, cap3), run_time=2)
        self.wait(1)

        # merge exponentials
        s4 = MathTex(r"x(t)", "=", r"\frac{1}{2\pi}", r"\int_{-\infty}^{\infty}", r"X(\sigma+j\omega)",
                     r"e^{(\sigma+j\omega)t}", r"d\omega", font_size=50).move_to(s3)
        cap4 = note(r"$e^{\sigma t}e^{j\omega t}=e^{(\sigma+j\omega)t}$", color=YELLOW, fs=34).move_to(cap)
        self.play(
            ReplacementTransform(VGroup(s3[5], s3[6]), s4[5]),
            ReplacementTransform(s3[0], s4[0]), ReplacementTransform(s3[1], s4[1]),
            ReplacementTransform(s3[2], s4[2]), ReplacementTransform(s3[3], s4[3]),
            ReplacementTransform(s3[4], s4[4]), ReplacementTransform(s3[7], s4[6]),
            FadeTransform(cap3, cap4), run_time=1.8)
        self.wait(0.8)
        self.play(Create(SurroundingRectangle(s4, color=YELLOW, buff=0.2)))
        done = note(r"$x(t)$ rebuilt from exponentials $e^{(\sigma+j\omega)t}$, at one fixed $\sigma$", color=YELLOW,
                    fs=32).move_to(DOWN * 2.8)
        self.play(FadeIn(done, shift=UP * 0.1))
        self.wait(2.2)
        fade_all(self)

    # --- 6a. s-plane picture of the change of variable --------------------------
    def c1_change_of_variable_geometry(self):
        title = make_title(r"Change of variable: from $\omega$ to $s$")
        sp = SPlane(x_range=(-3, 2, 1), y_range=(-4, 4, 2), x_length=4.4, y_length=5.4, number_size=18)
        sp.move_to(LEFT * 4.0 + DOWN * 0.5)
        sigma0 = 0.3
        line = DashedLine(sp.c2p(sigma0, -4), sp.c2p(sigma0, 4), color=YELLOW, stroke_width=2, dash_length=0.08)
        w = ValueTracker(-3.3)
        dot = always_redraw(lambda: Dot(sp.c2p(sigma0, w.get_value()), color=YELLOW, radius=0.1))
        s_lab = always_redraw(lambda: MathTex(r"s=\sigma+j\omega", font_size=32, color=YELLOW).next_to(dot, RIGHT, buff=0.15))
        self.play(Write(title))
        self.play(FadeIn(sp))
        self.play(Create(line))
        self.add(dot, s_lab)
        t1 = note(r"fix $\sigma$, let $\omega$ run\\from $-\infty$ to $+\infty$", fs=32, maxw=6.3).move_to(RIGHT * 3.5 + UP * 2.4)
        self.play(FadeIn(t1))
        self.play(w.animate.set_value(3.3), run_time=4)
        t2 = note(r"$s$ climbs a vertical line:\\from $\sigma-j\infty$ to $\sigma+j\infty$", color=YELLOW, fs=32, maxw=6.3)
        t2.next_to(t1, DOWN, buff=0.25)
        self.play(FadeIn(t2, shift=UP * 0.1))
        self.wait(1)

        # ds = j dw : a real step turns 90 degrees
        origin = RIGHT * 2.0 + DOWN * 1.0
        dw = Arrow(origin, origin + RIGHT * 1.7, buff=0, color=GOLD, stroke_width=7)
        dw_lab = MathTex(r"d\omega", font_size=40, color=GOLD).next_to(dw, DOWN, buff=0.15)
        real_note = note(r"a step in $\omega$ is a \emph{real} step", fs=28, color=GREY_A, maxw=6.3).move_to(RIGHT * 3.5 + DOWN * 2.9)
        self.play(GrowArrow(dw), FadeIn(dw_lab), FadeIn(real_note))
        self.wait(0.8)
        turn_note = note(r"in the $s$-plane the step points along $j$\\(multiplying by $j$ turns it by $90^\circ$)",
                         fs=28, color=GREY_A, maxw=6.3).move_to(real_note)
        dws = dw.copy()
        ds_lab = MathTex(r"ds=j\,d\omega", font_size=40, color=YELLOW).move_to(origin + LEFT * 1.35 + UP * 0.9)
        self.play(Rotate(dws, angle=PI / 2, about_point=origin), FadeTransform(real_note, turn_note), run_time=2)
        self.play(FadeIn(ds_lab, shift=LEFT * 0.2), dws.animate.set_color(YELLOW))
        self.wait(1)
        result = MathTex(r"d\omega=\frac{ds}{j}", font_size=48, color=YELLOW).move_to(origin + RIGHT * 3.2 + UP * 0.9)
        self.play(Write(result))
        self.wait(2)
        fade_all(self)

    # --- 6b. the algebra of the substitution ----------------------------------------
    def c1_change_of_variable_algebra(self):
        title = make_title(r"Substitute $s=\sigma+j\omega$")
        P = [r"x(t)", "=", r"\frac{1}{2\pi}", r"\int_{-\infty}^{\infty}", r"X(\sigma+j\omega)", r"e^{(\sigma+j\omega)t}",
             r"d\omega"]
        S4 = MathTex(*P, font_size=52).move_to(UP * 1.0)
        self.play(Write(title))
        self.play(Write(S4))
        self.wait(0.8)

        # step 1: s everywhere, new limits, d omega -> ds/j
        c1 = note(r"1. rename $\sigma+j\omega\to s$,\ \ and the limits follow the line", fs=30, color=YELLOW).move_to(DOWN * 1.6)
        S5 = MathTex(r"x(t)", "=", r"\frac{1}{2\pi}", r"\int_{\sigma-j\infty}^{\sigma+j\infty}", r"X(s)", r"e^{st}",
                     r"\frac{ds}{j}", font_size=52).move_to(S4)
        self.play(FadeIn(c1))
        self.play(*morph(S4, S5)[:6], FadeOut(S4[6]), run_time=2)
        self.wait(0.8)
        c2 = note(r"2. $d\omega=\dfrac{ds}{j}$", fs=30, color=YELLOW).move_to(c1)
        self.play(FadeTransform(c1, c2), FadeIn(S5[6], shift=LEFT * 0.3))
        self.wait(1)

        # step 2: pull 1/j to the front
        c3 = note(r"3. the constant $\dfrac1j$ moves to the front", fs=30, color=YELLOW).move_to(c1)
        S6 = MathTex(r"x(t)", "=", r"\frac{1}{2\pi j}", r"\int_{\sigma-j\infty}^{\sigma+j\infty}", r"X(s)", r"e^{st}",
                     r"ds", font_size=52).move_to(S5)
        self.play(FadeTransform(c2, c3), *morph(S5, S6), run_time=2)
        self.wait(1)
        self.formula = S6
        self.play(Create(SurroundingRectangle(S6, color=YELLOW, buff=0.2)))
        self.wait(2)
        fade_all(self)

    # --- 7. name it ---------------------------------------------------------------------
    def c1_bromwich(self):
        formula = MathTex(r"x(t)", "=", r"\frac{1}{2\pi j}", r"\int_{\sigma-j\infty}^{\sigma+j\infty}", r"X(s)", r"e^{st}",
                          r"ds", font_size=64).move_to(UP * 0.9)
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.25)
        name = Tex(r"The \textbf{Bromwich integral}", font_size=54, color=YELLOW).next_to(box, DOWN, buff=0.6)
        self.play(Write(formula))
        self.play(Create(box))
        self.play(FadeIn(name, shift=UP * 0.2))
        self.wait(2)
        fade_all(self)

        # where is it allowed to live?  ->  inside the ROC
        title = make_title(r"The line must stay inside the ROC")
        sp = SPlane(x_range=(-3, 2, 1), y_range=(-4, 4, 2), x_length=4.6, y_length=5.2, number_size=18)
        sp.move_to(LEFT * 3.6 + DOWN * 0.45)
        pole = sp.pole(-1)
        roc = sp.roc(left=-1, opacity=0.35)
        Xs = MathTex(r"X(s)=\frac{1}{s+1}", font_size=34).next_to(sp, UP, buff=0.1)
        self.play(Write(title))
        self.play(FadeIn(sp), FadeIn(pole), FadeIn(Xs))
        roc_lab = note(r"ROC: $\mathrm{Re}\{s\}>-1$", color=BLUE_B, fs=32).move_to(RIGHT * 3.5 + UP * 1.6)
        self.play(FadeIn(roc), FadeIn(roc_lab))
        good = DashedLine(sp.c2p(0.3, -4), sp.c2p(0.3, 4), color=GOOD, stroke_width=4)
        good_t = note(r"inside the ROC: the integral converges,\\so $x(t)$ is well defined", color=GOOD, fs=30, maxw=6.3)
        good_t.move_to(RIGHT * 3.5 + UP * 0.2)
        self.play(Create(good), FadeIn(good_t))
        self.wait(1.5)
        bad = DashedLine(sp.c2p(-2, -4), sp.c2p(-2, 4), color=RED_C, stroke_width=4)
        bad_t = note(r"outside: $X(s)$ is not defined there,\\so this line would be meaningless", color=RED_B, fs=30, maxw=6.3)
        bad_t.move_to(RIGHT * 3.5 + DOWN * 1.5)
        self.play(Create(bad), FadeIn(bad_t))
        self.wait(2.5)
        fade_all(self)

    # ------------------------------------------------------------------
    #  CHAPTER 2 : the simulation (unchanged apart from the closing part moving to chapter 3)
    # ------------------------------------------------------------------
    def chapter2(self):
        chapter_card(self, "Inverse Laplace  -  chapter 2", "Watching the Bromwich integral work",
                     r"adding up $e^{st}$ along the line")
        self.build_up()

    def build_up(self):
        self.formula = MathTex(r"x(t)", r"=", r"\frac{1}{2\pi j}\int_{\sigma - j\infty}^{\sigma + j\infty} X(s)\,e^{st}\,ds")
        self.formula.scale(0.765).to_edge(UP, buff=0.25)
        self.add(self.formula)

        sigma = ValueTracker(0.3)
        W = ValueTracker(0.0)

        sp = SPlane(x_range=(-3, 2, 1), y_range=(-4, 4, 2), x_length=3.6, y_length=5.2, number_size=18)
        sp.move_to(LEFT * 4.9 + DOWN * 0.6)
        pole = sp.pole(-1)
        Xs = MathTex(r"X(s) = \frac{1}{s+1}", font_size=32).next_to(sp, UP, buff=0.12)
        roc = sp.roc(left=-1, opacity=0.35)

        ax = signal_axes(x_range=(-2, 4, 1), y_range=(-1.5, 1.5, 0.5), x_length=6.8, y_length=4.4)
        ax.move_to(RIGHT * 2.6 + DOWN * 0.55)
        target = DashedVMobject(clipped_graph(ax, lambda t: np.exp(-t) * u(t), 0.001, 4, color=GREY_B, stroke_width=3)[0],
                                num_dashes=40)
        target_lab = MathTex(r"e^{-t}u(t)", font_size=30, color=GREY_B).next_to(ax.c2p(0.6, 1.0), RIGHT, buff=0.1)

        self.play(FadeIn(sp), FadeIn(Xs), FadeIn(pole), FadeIn(roc), Create(ax))
        self.play(Create(target), FadeIn(target_lab))

        def wvis():
            return 3.9 * (1 - np.exp(-W.get_value() / 8))

        brom_line = always_redraw(lambda: DashedLine(
            sp.c2p(sigma.get_value(), -4), sp.c2p(sigma.get_value(), 4), color=YELLOW, stroke_width=2, dash_length=0.08))
        seg = always_redraw(lambda: Line(
            sp.c2p(sigma.get_value(), -wvis()), sp.c2p(sigma.get_value(), wvis() + 1e-3), color=YELLOW, stroke_width=7))
        recon = always_redraw(lambda: clipped_polyline(
            ax, T_GRID, reconstruct(sigma.get_value(), W.get_value()), color=YELLOW, stroke_width=5))

        W_num = DecimalNumber(0, num_decimal_places=1, font_size=32)
        W_num.add_updater(lambda m: m.set_value(W.get_value()))
        W_read = VGroup(MathTex(r"\text{using } |\omega| <", font_size=32), W_num).arrange(RIGHT, buff=0.12)
        W_read.next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        recipe = MathTex(r"x(t) \approx \frac{1}{2\pi}\sum_k X(\sigma + jk\Delta\omega)\,e^{(\sigma + jk\Delta\omega)t}\,\Delta\omega",
                         font_size=32).next_to(ax, DOWN, buff=0.2)

        self.play(Create(brom_line))
        self.add(seg, recon)
        self.play(FadeIn(W_read), FadeIn(recipe))
        self.play(W.animate.set_value(2), run_time=2.5)
        self.wait(0.3)
        self.play(W.animate.set_value(8), run_time=3)
        self.wait(0.3)
        self.play(W.animate.set_value(60), run_time=5, rate_func=rate_functions.ease_in_quad)
        note_ = Tex(r"each point on the line contributes one spinning $e^{st}$;\\together they rebuild $x(t)$",
                    font_size=30, color=YELLOW).move_to(recipe)
        self.play(FadeTransform(recipe, note_))
        self.wait(1.5)

        # --- slide the line around: same answer anywhere inside the ROC
        sig_num = DecimalNumber(0.3, num_decimal_places=2, include_sign=True, font_size=30)
        sig_num.add_updater(lambda m: m.set_value(sigma.get_value()))
        sig_read = VGroup(MathTex(r"\sigma =", font_size=30), sig_num).arrange(RIGHT, buff=0.1).next_to(sp, DOWN, buff=0.15)
        inside = Tex(r"any $\sigma$ inside the ROC gives the \emph{same} $x(t)$", font_size=30, color=GOOD).move_to(note_)
        self.play(FadeIn(sig_read), FadeTransform(note_, inside))
        self.play(sigma.animate.set_value(0.9), run_time=2)
        self.play(sigma.animate.set_value(-0.6), run_time=2.5)
        self.wait(0.5)

        # --- cross the pole: a different (left-sided) signal
        alt = DashedVMobject(clipped_graph(ax, lambda t: -np.exp(-t), -2, -0.001, color=RED_B, stroke_width=3)[0], num_dashes=25)
        alt_lab = MathTex(r"-e^{-t}u(-t)", font_size=30, color=RED_B).next_to(ax.c2p(-1.9, -0.6), RIGHT, buff=0.05)
        outside = Tex(r"line left of the pole: same $X(s)$, \emph{different} ROC $\Rightarrow$ different $x(t)$",
                      font_size=28, color=RED_B).move_to(inside).set_x(1.8)
        self.play(sigma.animate.set_value(-1.5), FadeIn(alt), FadeIn(alt_lab), FadeTransform(inside, outside), run_time=4)
        self.wait(2)
        self.play(sigma.animate.set_value(0.3), FadeOut(alt), FadeOut(alt_lab), run_time=3)
        self.wait(0.5)
        brom_line.clear_updaters()
        fade_all(self)

    # ------------------------------------------------------------------
    #  CHAPTER 3 : closing the contour
    # ------------------------------------------------------------------
    def chapter3(self):
        chapter_card(self, "Inverse Laplace  -  chapter 3", "Closing the contour",
                     "turning a hard line integral into a residue count")
        self.c3_motivation()
        self.c3_add_arc()
        self.c3_residue()
        self.c3_negative_t()
        self.c3_roc_decides()

    def _plane(self, y_shift=-0.4):
        sp = SPlane(x_range=(-4, 4, 1), y_range=(-4, 4, 1), x_length=5.6, y_length=5.6, number_size=18)
        sp.move_to(LEFT * 3.4 + DOWN * 0.4 + UP * (y_shift + 0.4))
        return sp

    # --- a. why would we want a closed loop? -------------------------------------
    def c3_motivation(self):
        title = make_title(r"The line integral is hard. Loops are easy.")
        self.play(Write(title))
        hard = MathTex(r"\int_{\sigma-j\infty}^{\sigma+j\infty} X(s)\,e^{st}\,ds", font_size=52).move_to(UP * 0.7)
        q = note(r"an infinite path through the complex plane: where do we even start?", color=RED_B, fs=32).next_to(hard, DOWN, buff=0.5)
        self.play(Write(hard))
        self.play(FadeIn(q))
        self.wait(2)
        self.play(FadeOut(VGroup(hard, q)))

        sp = self._plane()
        loop = Circle(radius=1.5, color=TEAL_C, stroke_width=5).move_to(sp.c2p(-0.4, 0.2))
        inside_poles = VGroup(cross_marker(sp, -1.2, 0.7, YELLOW), cross_marker(sp, 0.5, -0.5, YELLOW),
                              cross_marker(sp, -0.3, 1.3, YELLOW))
        outside_pole = cross_marker(sp, 3, 2, GREY_B)
        c_lab = MathTex("C", font_size=36, color=TEAL_C).next_to(loop, UR, buff=-0.1)
        self.play(FadeIn(sp))
        self.play(Create(loop), FadeIn(c_lab))
        self.play(FadeIn(inside_poles), FadeIn(outside_pole))
        thm = note(r"Cauchy's residue theorem", color=TEAL_C, fs=36).move_to(RIGHT * 3.4 + UP * 2.4)
        eq = MathTex(r"\oint_C f(s)\,ds", "=", r"2\pi j", r"\sum_{\text{inside }C}", r"\mathrm{Res}", font_size=44).move_to(RIGHT * 3.4 + UP * 1.0)
        self.play(FadeIn(thm))
        self.play(Write(eq))
        self.play(Indicate(inside_poles, color=YELLOW, scale_factor=1.5))
        t_in = note(r"poles \emph{inside} the loop are all that matter", color=YELLOW, fs=30).move_to(RIGHT * 3.4 + DOWN * 0.5)
        self.play(FadeIn(t_in))
        self.wait(1)
        t_out = note(r"poles outside contribute nothing", color=GREY_B, fs=30).next_to(t_in, DOWN, buff=0.3)
        self.play(FadeIn(t_out), Indicate(outside_pole, color=GREY_B))
        self.wait(1.5)
        hook = note(r"Our Bromwich line is not a closed loop.\\Can we close it?", color=YELLOW, fs=34, maxw=6.3).move_to(RIGHT * 3.4 + DOWN * 2.6)
        self.play(FadeIn(hook, shift=UP * 0.15))
        self.wait(2)
        fade_all(self)

    # --- b. add a big arc, and show it contributes nothing ---------------------------
    def c3_add_arc(self):
        title = make_title(r"Close the line with a huge arc  ($t>0$)")
        sp = self._plane()
        pole = sp.pole(-1)
        roc = sp.roc(left=-1, opacity=0.3)
        sigma0, R = 0.3, 3.2
        vert, arc = contour_pieces(sp, sigma0, R, "left")
        line_lab = MathTex(r"\text{line}", font_size=30, color=YELLOW).next_to(vert, RIGHT, buff=0.1).shift(DOWN * 1.2)
        cr = MathTex(r"C_R", font_size=36, color=TEAL_C).next_to(arc.point_from_proportion(0.22), UL, buff=0.1)
        self.play(Write(title))
        self.play(FadeIn(sp), FadeIn(pole), FadeIn(roc))
        self.play(Create(vert), FadeIn(line_lab))
        self.wait(0.5)
        self.play(Create(arc), FadeIn(cr), run_time=2)
        eqA = MathTex(r"\oint_C", "=", r"\int_{\sigma-jR}^{\sigma+jR}", "+", r"\int_{C_R}", font_size=44)
        eqA.move_to(RIGHT * 3.4 + UP * 2.4)
        eqA[2].set_color(YELLOW)
        eqA[4].set_color(TEAL_C)
        same = note(r"(integrand: $X(s)e^{st}$ on all three)", fs=26).next_to(eqA, DOWN, buff=0.15)
        self.play(Write(eqA), FadeIn(same))
        self.wait(1)

        # the bar : |e^{st}| along the arc
        q = note(r"What is $|e^{st}|$ out on the arc?", color=YELLOW, fs=32).move_to(RIGHT * 3.4 + UP * 0.9)
        magn = MathTex(r"|e^{st}|=e^{\mathrm{Re}\{s\}\,t}", font_size=40).next_to(q, DOWN, buff=0.25)
        self.play(FadeIn(q), Write(magn))
        th = ValueTracker(0.0)
        base_y, bar_x = -2.3, 3.4
        tval = 1.0

        def arc_pt():
            ang = PI / 2 + th.get_value()
            return sp.c2p(sigma0 + R * np.cos(ang), R * np.sin(ang))

        def height():
            ang = PI / 2 + th.get_value()
            return 1.9 * np.exp(R * np.cos(ang) * tval) + 0.02

        dot = always_redraw(lambda: Dot(arc_pt(), color=YELLOW, radius=0.11))
        bar = always_redraw(lambda: Rectangle(width=1.0, height=height(), fill_color=ORANGE, fill_opacity=0.9,
                                              stroke_width=0).move_to([bar_x, base_y + height() / 2, 0]))
        floor = Line([bar_x - 1.2, base_y, 0], [bar_x + 1.2, base_y, 0], color=GREY_B)
        bar_lab = MathTex(r"|e^{st}|", font_size=32, color=ORANGE).next_to(floor, DOWN, buff=0.1)
        t_lab = MathTex(r"t=1>0", font_size=32, color=GREY_A).next_to(floor, RIGHT, buff=0.15).shift(UP * 0.2)
        self.add(dot, bar)
        self.play(FadeIn(floor), FadeIn(bar_lab), FadeIn(t_lab))
        self.play(th.animate.set_value(PI / 2), run_time=3)
        self.wait(0.3)
        self.play(th.animate.set_value(PI), run_time=3)
        self.wait(0.4)
        concl = note(r"for $t>0$ it dies off as\\$\mathrm{Re}\{s\}\to-\infty$", color=ORANGE, fs=30, maxw=6.3).move_to(RIGHT * 3.4 + DOWN * 3.45)
        self.play(FadeIn(concl))
        self.wait(1.5)

        # conclusion
        self.play(FadeOut(VGroup(q, magn, bar, dot, floor, bar_lab, t_lab, concl)))
        vanish = MathTex(r"R\to\infty:\quad", r"\int_{C_R}\to 0", font_size=44).move_to(RIGHT * 3.4 + UP * 0.6)
        vanish[1].set_color(TEAL_C)
        self.play(Write(vanish))
        self.play(Indicate(eqA[4], color=TEAL_C, scale_factor=1.3))
        fin = MathTex(r"\int_{\sigma-j\infty}^{\sigma+j\infty}X e^{st}ds", "=", r"\oint_C X e^{st}ds", font_size=38)
        fin.move_to(RIGHT * 3.4 + DOWN * 1.1)
        fin[0].set_color(YELLOW)
        self.play(Write(fin))
        self.play(Create(SurroundingRectangle(fin, color=YELLOW, buff=0.15)))
        caveat = note(r"(this also needs $X(s)$ to decay,\\which is fine for rational $X(s)$)", fs=24, maxw=6.3).move_to(RIGHT * 3.4 + DOWN * 2.6)
        self.play(FadeIn(caveat))
        self.wait(2.5)
        fade_all(self)

    # --- c. count the pole -------------------------------------------------------------
    def c3_residue(self):
        title = make_title(r"The closed loop swallows the pole")
        sp = self._plane()
        pole = sp.pole(-1)
        roc = sp.roc(left=-1, opacity=0.3)
        Xs = MathTex(r"X(s)=\frac{1}{s+1}", font_size=34).next_to(sp, UP, buff=0.1)
        sigma0, R = 0.3, 3.2
        vert, arc = contour_pieces(sp, sigma0, R, "left")
        self.play(Write(title))
        self.play(FadeIn(sp), FadeIn(pole), FadeIn(roc), FadeIn(Xs))
        self.play(Create(vert), Create(arc), run_time=1.5)
        runner = Dot(sp.c2p(sigma0, -R), color=WHITE, radius=0.12)
        path = closed_path(vert, arc)
        self.add(runner)
        ccw = note(r"counter-clockwise", color=GREY_A, fs=26).next_to(sp, DOWN, buff=0.1)
        self.play(FadeIn(ccw), MoveAlongPath(runner, path), run_time=3.5, rate_func=linear)
        self.play(FadeOut(runner), Indicate(pole, color=YELLOW, scale_factor=1.8))

        L = [
            MathTex(r"x(t)", "=", r"\frac{1}{2\pi j}", r"\oint_C X(s)e^{st}ds", font_size=42),
            MathTex(r"=", r"\frac{1}{2\pi j}", r"\cdot", r"2\pi j", r"\sum \mathrm{Res}", font_size=42),
            MathTex(r"=", r"\mathrm{Res}_{s=-1}\frac{e^{st}}{s+1}", font_size=42),
            MathTex(r"=", r"e^{-t}", r"\qquad (t>0)", font_size=46),
        ]
        L[1][1].set_color(YELLOW)
        L[1][3].set_color(YELLOW)
        L[3][1].set_color(GOOD)
        col = VGroup(*L).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 3.4 + UP * 0.2)
        L[1].shift(RIGHT * 0.5)
        L[2].shift(RIGHT * 0.5)
        L[3].shift(RIGHT * 0.5)
        self.play(Write(L[0]))
        self.wait(0.5)
        self.play(Write(L[1]))
        cancel = note(r"$2\pi j$ cancels", color=YELLOW, fs=26).next_to(L[1], RIGHT, buff=0.15).shift(DOWN * 0.45)
        self.play(FadeIn(cancel))
        self.wait(0.8)
        self.play(FadeOut(cancel), Write(L[2]))
        why = note(r"simple pole: the residue is just\\$e^{st}$ evaluated at $s=-1$", fs=26, color=GREY_A, maxw=6.3).move_to(RIGHT * 3.4 + DOWN * 3.3)
        self.play(FadeIn(why))
        self.wait(1)
        self.play(FadeOut(why), Write(L[3]))
        self.play(Create(SurroundingRectangle(L[3], color=GOOD, buff=0.15)))
        self.wait(2.5)
        fade_all(self)

    # --- d. t < 0 -----------------------------------------------------------------------
    def c3_negative_t(self):
        title = make_title(r"What about $t<0$?")
        sp = self._plane()
        pole = sp.pole(-1)
        roc = sp.roc(left=-1, opacity=0.3)
        sigma0, R = 0.3, 3.2
        vert, arc_l = contour_pieces(sp, sigma0, R, "left")
        _, arc_r = contour_pieces(sp, sigma0, R, "right")
        self.play(Write(title))
        self.play(FadeIn(sp), FadeIn(pole), FadeIn(roc), Create(vert))
        t1 = note(r"$|e^{st}|=e^{\mathrm{Re}\{s\}t}$ with $t<0$", fs=34).move_to(RIGHT * 3.4 + UP * 2.2)
        t2 = note(r"it now dies off as $\mathrm{Re}\{s\}\to+\infty$", color=ORANGE, fs=32).next_to(t1, DOWN, buff=0.3)
        self.play(FadeIn(t1))
        self.play(FadeIn(t2))
        self.wait(1)
        t3 = note(r"so close the loop on the \textbf{right}", color=ORANGE, fs=34).next_to(t2, DOWN, buff=0.5)
        self.play(Create(arc_r), FadeIn(t3), run_time=2)
        self.wait(1)
        t4 = note(r"no pole inside the loop", color=GREY_A, fs=32).next_to(t3, DOWN, buff=0.5)
        self.play(FadeIn(t4))
        t5 = MathTex(r"x(t)=0\qquad (t<0)", font_size=46, color=YELLOW).next_to(t4, DOWN, buff=0.4)
        self.play(Write(t5))
        self.wait(1.2)
        both = MathTex(r"t>0:\ e^{-t}\qquad t<0:\ 0\qquad\Longrightarrow\qquad x(t)=e^{-t}u(t)", font_size=40, color=GOOD)
        both.move_to(DOWN * 3.75)
        self.play(Write(both))
        self.wait(2.5)
        fade_all(self)

    # --- e. moving the line flips everything -------------------------------------------------
    def c3_roc_decides(self):
        title = make_title(r"Same $X(s)$, but the line is left of the pole")
        sp = self._plane()
        pole = sp.pole(-1)
        roc = sp.roc(right=-1, opacity=0.3)
        roc_lab = MathTex(r"\mathrm{Re}\{s\}<-1", font_size=32, color=BLUE_B).next_to(sp, DOWN, buff=0.1)
        sigma0, R = -1.8, 2.0
        vert, arc_l = contour_pieces(sp, sigma0, R, "left")
        _, arc_r = contour_pieces(sp, sigma0, R, "right")
        self.play(Write(title))
        self.play(FadeIn(sp), FadeIn(pole), FadeIn(roc), FadeIn(roc_lab), Create(vert))

        a = note(r"$t>0$: close on the left", color=TEAL_C, fs=34).move_to(RIGHT * 3.4 + UP * 2.4)
        self.play(FadeIn(a), Create(arc_l), run_time=1.8)
        a2 = note(r"the pole is \emph{outside} the loop", fs=32).next_to(a, DOWN, buff=0.3)
        self.play(FadeIn(a2), Indicate(pole, color=GREY_B, scale_factor=1.5))
        a3 = MathTex(r"x(t)=0\qquad(t>0)", font_size=42, color=YELLOW).next_to(a2, DOWN, buff=0.3)
        self.play(Write(a3))
        self.wait(1.5)

        b = note(r"$t<0$: close on the right", color=ORANGE, fs=34).move_to(RIGHT * 3.4 + DOWN * 0.4)
        self.play(FadeIn(b), FadeOut(arc_l), Create(arc_r), run_time=1.8)
        b2 = note(r"the pole is \emph{inside},\\but we travel clockwise", fs=30, maxw=6.3).next_to(b, DOWN, buff=0.3)
        runner = Dot(sp.c2p(sigma0, -R), color=WHITE, radius=0.12)
        path = closed_path(vert, arc_r)
        self.add(runner)
        self.play(FadeIn(b2), MoveAlongPath(runner, path), run_time=3, rate_func=linear)
        self.play(FadeOut(runner), Indicate(pole, color=YELLOW, scale_factor=1.8))
        b3 = MathTex(r"x(t)=-\mathrm{Res}=-e^{-t}\qquad(t<0)", font_size=40, color=YELLOW).next_to(b2, DOWN, buff=0.3)
        self.play(Write(b3))
        self.wait(1.5)
        self.play(FadeOut(VGroup(a, a2, a3, b, b2, b3)))
        fin = MathTex(r"x(t)=-e^{-t}u(-t)", font_size=50, color=GOOD).move_to(RIGHT * 3.4 + UP * 0.2)
        self.play(Write(fin), Create(SurroundingRectangle(fin, color=GOOD, buff=0.15)))
        self.wait(1.2)
        moral = note(r"the ROC decides which poles the contour encloses,\\and from which side", color=YELLOW, fs=32, maxw=6.3)
        moral.move_to(RIGHT * 3.4 + DOWN * 1.6)
        self.play(FadeIn(moral, shift=UP * 0.1))
        self.wait(2.5)
        fade_all(self)


# ======================================================================
#  PARTIAL FRACTIONS AND ROC
# ======================================================================
class PartialFractionsAndROC(Scene):
    def construct(self):
        self.chapter1()
        self.chapter2()

    # ------------------------------------------------------------------
    #  CHAPTER 1 : a better tool, and its building block
    # ------------------------------------------------------------------
    def chapter1(self):
        chapter_card(self, "Partial fractions  -  chapter 1", "A better tool for rational $X(s)$",
                     "and the one pair of formulas it needs")
        self.p1_cons()
        self.p1_partial_fractions()
        self.p1_pairs()
        self.p1_why_minus()
        self.p1_rule()

    # --- cons of the Bromwich integral --------------------------------------------------
    def p1_cons(self):
        title = make_title(r"Bromwich works, but it is heavy")
        formula = MathTex(r"x(t)=\frac{1}{2\pi j}\int_{\sigma-j\infty}^{\sigma+j\infty}X(s)\,e^{st}\,ds", font_size=48)
        formula.move_to(UP * 2.2)
        self.play(Write(title))
        self.play(Write(formula))
        self.wait(0.6)
        rows = [
            r"an integral over an \textbf{infinite} line in the complex plane",
            r"we must close the contour, separately for $t>0$ and $t<0$, and \textbf{justify} that the arc vanishes",
            r"then find \textbf{every} residue inside, and track which poles the ROC encloses",
        ]
        items = VGroup()
        for r in rows:
            mark = MathTex(r"\times", font_size=52, color=RED_C)
            txt = Tex(r, font_size=32)
            if txt.width > 11.0:
                txt.scale_to_fit_width(11.0)
            items.add(VGroup(mark, txt).arrange(RIGHT, buff=0.35))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(DOWN * 0.7)
        for it in items:
            self.play(FadeIn(it, shift=RIGHT * 0.3), run_time=1.2)
            self.wait(1.2)
        self.wait(0.5)
        hope = Tex(r"But if $X(s)=\dfrac{N(s)}{D(s)}$ is a \textbf{rational} function, there is a much easier road.",
                   font_size=36, color=YELLOW)
        self.play(FadeOut(items), FadeOut(formula))
        self.play(FadeIn(hope, shift=UP * 0.2))
        self.wait(2)
        fade_all(self)

    # --- partial fractions: why they win ------------------------------------------------
    def p1_partial_fractions(self):
        title = make_title(r"Partial fractions: break it into pieces we can invert")
        X = MathTex(r"X(s)=\frac{5s+7}{(s+1)(s+3)(s+5)}", font_size=50).move_to(UP * 1.9)
        self.play(Write(title))
        self.play(Write(X))
        bad = note(r"inverting this directly looks horrible", color=RED_B, fs=30).next_to(X, DOWN, buff=0.35)
        self.play(FadeIn(bad))
        self.wait(1.2)
        arrow = Arrow(UP * 0.55, DOWN * 0.45, buff=0, color=YELLOW, stroke_width=6)
        pf_lab = note(r"partial fractions", color=YELLOW, fs=30).next_to(arrow, RIGHT, buff=0.25)
        self.play(FadeOut(bad), GrowArrow(arrow), FadeIn(pf_lab))
        pf = MathTex(r"\frac{A}{s+1}", "+", r"\frac{B}{s+3}", "+", r"\frac{C}{s+5}", font_size=56).move_to(DOWN * 1.5)
        pf[0].set_color(TEAL_C)
        pf[2].set_color(GOLD)
        pf[4].set_color(PURPLE_B)
        self.play(Write(pf), run_time=2)
        self.wait(1)
        boxes = VGroup(*[SurroundingRectangle(pf[i], color=pf[i].get_color(), buff=0.12) for i in (0, 2, 4)])
        same = note(r"every piece has the same shape $\dfrac{A}{s+a}$, so we only need to learn \emph{one} pair",
                    color=GREY_A, fs=30).move_to(DOWN * 3.2)
        self.play(Create(boxes))
        self.play(FadeIn(same, shift=UP * 0.1))
        self.wait(1.5)
        lin = note(r"and the inverse transform is linear: invert each piece, then add", color=YELLOW, fs=30).move_to(DOWN * 3.2)
        self.play(FadeTransform(same, lin))
        self.wait(2.5)
        fade_all(self)

    # --- the fundamental pairs ------------------------------------------------------------------
    def p1_pairs(self):
        title = make_title(r"The building block")
        sp = SPlane(x_range=(-3, 2, 1), y_range=(-1.5, 1.5, 1), x_length=5.0, y_length=3.0, number_size=18)
        sp.move_to(LEFT * 3.5 + DOWN * 0.7)
        pole = sp.pole(-1)
        p_lab = MathTex(r"-a", font_size=30).next_to(sp.c2p(-1, 0), DOWN, buff=0.2)
        ax = signal_axes(x_range=(-2, 4, 1), y_range=(-3, 3, 1), x_length=6.0, y_length=3.6)
        ax.move_to(RIGHT * 3.6 + DOWN * 0.7)

        pair_R = MathTex(r"\frac{A}{s+a}", r"\ \longleftrightarrow\ ", r"A\,e^{-at}u(t)", font_size=54)
        pair_R.move_to(UP * 2.3)
        pair_R[2].set_color(TEAL_C)
        roc_R = sp.roc(left=-1, opacity=0.4)
        roc_R_lab = MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\}>-a", font_size=32, color=BLUE_B).next_to(sp, DOWN, buff=0.15)
        g_R = clipped_graph(ax, lambda t: np.exp(-t) * u(t), -2, 4, breaks=[0], color=TEAL_C, stroke_width=6)
        g_lab_R = MathTex(r"(A=a=1)", font_size=26, color=GREY_B).next_to(ax, DOWN, buff=0.15)

        self.play(Write(title))
        self.play(Write(pair_R[0]))
        self.play(FadeIn(sp), FadeIn(pole), FadeIn(p_lab))
        self.wait(0.6)
        self.play(FadeIn(roc_R), FadeIn(roc_R_lab))
        right_t = note(r"ROC to the \textbf{right} of the pole: a \textbf{right-sided} signal", color=TEAL_C, fs=30)
        right_t.next_to(pair_R, DOWN, buff=0.25)
        self.play(FadeIn(right_t))
        self.play(Write(pair_R[1]), Write(pair_R[2]))
        self.play(Create(ax), FadeIn(g_lab_R))
        self.play(Create(g_R), run_time=2)
        self.wait(2)

        # --- flip to the left-sided partner
        pair_L = MathTex(r"\frac{A}{s+a}", r"\ \longleftrightarrow\ ", r"-A\,e^{-at}u(-t)", font_size=54).move_to(pair_R)
        pair_L[2].set_color(RED_B)
        roc_L = sp.roc(right=-1, opacity=0.4)
        roc_L_lab = MathTex(r"\mathrm{ROC}:\ \mathrm{Re}\{s\}<-a", font_size=32, color=BLUE_B).move_to(roc_R_lab)
        g_L = clipped_graph(ax, lambda t: -np.exp(-t) * u(-t), -2, 4, breaks=[0], color=RED_B, stroke_width=6)
        left_t = note(r"ROC to the \textbf{left} of the pole: a \textbf{left-sided} signal", color=RED_B, fs=30).move_to(right_t)
        same = note(r"the algebraic expression is identical; only the ROC changed", color=YELLOW, fs=30).move_to(DOWN * 3.5)
        self.play(FadeTransform(roc_R, roc_L), FadeTransform(roc_R_lab, roc_L_lab), FadeTransform(right_t, left_t),
                  FadeOut(g_R), run_time=1.6)
        self.play(ReplacementTransform(pair_R[2], pair_L[2]), run_time=1.2)
        self.play(Create(g_L), run_time=2)
        self.play(FadeIn(same))
        self.wait(2.5)
        fade_all(self)

    # --- why does the left-sided one carry a minus sign? ------------------------------------------------
    def p1_why_minus(self):
        title = make_title(r"Why the minus sign on the left-sided one?")
        start = MathTex(r"x(t)=-A\,e^{-at}u(-t)", font_size=42, color=RED_B).move_to(UP * 2.55)
        self.play(Write(title))
        self.play(Write(start))
        self.wait(0.6)
        steps = [
            MathTex(r"X(s)", "=", r"\int_{-\infty}^{0}", r"-A\,e^{-at}", r"e^{-st}", r"dt", font_size=38),
            MathTex(r"=", r"-A\int_{-\infty}^{0}", r"e^{-(s+a)t}", r"dt", font_size=38),
            MathTex(r"=", r"\frac{A}{s+a}", r"\Big[e^{-(s+a)t}\Big]_{-\infty}^{0}", font_size=38),
            MathTex(r"=", r"\frac{A}{s+a}", r"\big(1-0\big)", "=", r"\frac{A}{s+a}", font_size=38),
        ]
        steps[0].move_to(UP * 1.25 + LEFT * 1.2)
        for i in range(1, 4):
            steps[i].next_to(steps[i - 1], DOWN, buff=0.3).align_to(steps[0][1], LEFT)
        self.play(Write(steps[0]))
        self.wait(0.8)
        self.play(Write(steps[1]))
        self.wait(0.8)
        self.play(Write(steps[2]))
        self.wait(0.8)
        self.play(Write(steps[3]))
        self.play(Create(SurroundingRectangle(steps[3][4], color=YELLOW, buff=0.12)))
        cond = note(r"the ``$0$'' at $t\to-\infty$ needs $\mathrm{Re}\{s\}<-a$: exactly the left-sided ROC",
                    color=YELLOW, fs=30).move_to(DOWN * 3.5)
        self.play(FadeIn(cond, shift=UP * 0.1))
        self.wait(3)
        fade_all(self)

    # --- the rule, one place -----------------------------------------------------------------------
    def p1_rule(self):
        title = make_title(r"The rule to keep")
        left = VGroup(
            Tex(r"ROC to the \textbf{right}", font_size=36, color=TEAL_C),
            Tex(r"of the pole $-a$", font_size=32, color=GREY_A),
            MathTex(r"\frac{A}{s+a}\ \to\ A\,e^{-at}\,u(t)", font_size=38, color=TEAL_C),
            Tex(r"right-sided", font_size=32, color=TEAL_C),
        ).arrange(DOWN, buff=0.35)
        right = VGroup(
            Tex(r"ROC to the \textbf{left}", font_size=36, color=RED_B),
            Tex(r"of the pole $-a$", font_size=32, color=GREY_A),
            MathTex(r"\frac{A}{s+a}\ \to\ -A\,e^{-at}\,u(-t)", font_size=38, color=RED_B),
            Tex(r"left-sided", font_size=32, color=RED_B),
        ).arrange(DOWN, buff=0.35)
        cards = VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.1)
        b1 = SurroundingRectangle(left, color=TEAL_C, buff=0.3, corner_radius=0.12)
        b2 = SurroundingRectangle(right, color=RED_B, buff=0.3, corner_radius=0.12)
        self.play(Write(title))
        self.play(FadeIn(left), Create(b1))
        self.wait(1)
        self.play(FadeIn(right), Create(b2))
        self.wait(1.5)
        warn = note(r"Never invert a term until you have checked where the ROC sits relative to its pole.",
                    color=YELLOW, fs=32).move_to(DOWN * 3.3)
        self.play(FadeIn(warn, shift=UP * 0.15))
        self.wait(3)
        fade_all(self)

    # ------------------------------------------------------------------
    #  CHAPTER 2 : the slide problem
    # ------------------------------------------------------------------
    def chapter2(self):
        chapter_card(self, "Partial fractions  -  chapter 2", "One $X(s)$, three possible signals",
                     r"worked example from the slides (Ex.\ 9.8--9.11)")
        self.p2_expansion()
        self.p2_overview()
        for k, c in enumerate(self.cases(), start=1):
            self.p2_case(k, c)
        self.p2_recap()

    def cases(self):
        return [
            dict(roc=dict(left=-1), roc_tex=r"\mathrm{Re}\{s\} > -1", kind="right-sided (causal)",
                 sides=(RIGHT, RIGHT),
                 t1=r"e^{-t}u(t)", t2=r"-e^{-2t}u(t)", sum=r"x(t) = \big(e^{-t} - e^{-2t}\big)u(t)",
                 f1=lambda t: np.exp(-t) * u(t), f2=lambda t: -np.exp(-2 * t) * u(t)),
            dict(roc=dict(right=-2), roc_tex=r"\mathrm{Re}\{s\} < -2", kind="left-sided",
                 sides=(LEFT, LEFT),
                 t1=r"-e^{-t}u(-t)", t2=r"+e^{-2t}u(-t)", sum=r"x(t) = \big(-e^{-t} + e^{-2t}\big)u(-t)",
                 f1=lambda t: -np.exp(-t) * u(-t), f2=lambda t: np.exp(-2 * t) * u(-t)),
            dict(roc=dict(left=-2, right=-1), roc_tex=r"-2 < \mathrm{Re}\{s\} < -1", kind="two-sided",
                 sides=(LEFT, RIGHT),
                 t1=r"-e^{-t}u(-t)", t2=r"-e^{-2t}u(t)", sum=r"x(t) = -e^{-t}u(-t) - e^{-2t}u(t)",
                 f1=lambda t: -np.exp(-t) * u(-t), f2=lambda t: -np.exp(-2 * t) * u(t)),
        ]

    # --- partial fractions of the slide problem --------------------------------------------------------
    def p2_expansion(self):
        title = make_title(r"The slide problem")
        Xs = MathTex(r"X(s)=\frac{1}{(s+1)(s+2)}", font_size=56).move_to(UP * 2.0)
        self.play(Write(title))
        self.play(Write(Xs))
        self.wait(0.6)
        form = MathTex(r"=", r"\frac{A}{s+1}", "+", r"\frac{B}{s+2}", font_size=52).next_to(Xs, RIGHT, buff=0.3)
        self.play(Xs.animate.shift(LEFT * 1.6), run_time=0.8)
        form.next_to(Xs, RIGHT, buff=0.3)
        form[1].set_color(TEAL_C)
        form[3].set_color(GOLD)
        self.play(Write(form))
        self.wait(0.8)
        mult = MathTex(r"1", "=", r"A(s+2)", "+", r"B(s+1)", font_size=48).move_to(UP * 0.1)
        mult[2].set_color(TEAL_C)
        mult[4].set_color(GOLD)
        c1 = note(r"multiply through by $(s+1)(s+2)$", fs=28).next_to(mult, UP, buff=0.4)
        self.play(FadeIn(c1), Write(mult))
        self.wait(1)
        a_step = MathTex(r"s=-1:\quad 1=A(1)\ \Rightarrow\ A=1", font_size=42, color=TEAL_C).move_to(DOWN * 1.3)
        b_step = MathTex(r"s=-2:\quad 1=B(-1)\ \Rightarrow\ B=-1", font_size=42, color=GOLD).next_to(a_step, DOWN, buff=0.4).align_to(a_step, LEFT)
        self.play(Write(a_step))
        self.play(Indicate(mult[4], color=GOLD, scale_factor=1.0), Indicate(mult[2], color=TEAL_C))
        self.play(Write(b_step))
        self.wait(1)
        self.play(FadeOut(VGroup(c1, mult, a_step, b_step)))
        res = MathTex(r"X(s)", "=", r"\frac{1}{s+1}", "-", r"\frac{1}{s+2}", font_size=64).move_to(DOWN * 0.3)
        res[2].set_color(TEAL_C)
        res[4].set_color(GOLD)
        self.play(FadeOut(Xs), FadeOut(form), Write(res))
        always = note(r"this algebra is \emph{always the same}, whatever the ROC", color=YELLOW, fs=34).move_to(DOWN * 2.6)
        self.play(FadeIn(always, shift=UP * 0.15))
        self.wait(2.5)
        fade_all(self)

    # --- the three ROCs on one plane -------------------------------------------------------------------
    def p2_overview(self):
        title = make_title(r"Two poles cut the plane into three possible ROCs")
        sp = SPlane(x_range=(-4, 1.5, 1), y_range=(-2, 2, 1), x_length=8.0, y_length=3.6, number_size=18)
        sp.move_to(DOWN * 0.3)
        p1 = sp.pole(-1, color=TEAL_C)
        p2 = sp.pole(-2, color=GOLD)
        l1 = MathTex(r"-1", font_size=32, color=TEAL_C).next_to(sp.c2p(-1, 0), DOWN, buff=0.2)
        l2 = MathTex(r"-2", font_size=32, color=GOLD).next_to(sp.c2p(-2, 0), DOWN, buff=0.2)
        self.play(Write(title))
        self.play(FadeIn(sp), FadeIn(p1), FadeIn(p2), FadeIn(l1), FadeIn(l2))
        regions = [   # numbered like the cases that follow: 1 right, 2 left, 3 between
            (sp.roc(left=-1, opacity=0.4), r"\mathrm{Re}\{s\}>-1", r"\text{ROC 1}", sp.c2p(0.25, 1.5), GREEN_C, 4.2),
            (sp.roc(right=-2, opacity=0.4), r"\mathrm{Re}\{s\}<-2", r"\text{ROC 2}", sp.c2p(-3.0, 1.5), RED_C, -4.2),
            (sp.roc(left=-2, right=-1, opacity=0.4), r"-2<\mathrm{Re}\{s\}<-1", r"\text{ROC 3}", sp.c2p(-1.5, 1.5), BLUE_C, 0.0),
        ]
        for reg, tex, nm, pos, col, xpos in regions:
            reg.set_fill(col, opacity=0.35)
            lab = MathTex(nm, font_size=30, color=col).move_to(pos)
            cond = MathTex(tex, font_size=36, color=col).move_to(RIGHT * xpos + DOWN * 2.75)
            self.play(FadeIn(reg), FadeIn(lab))
            self.play(Write(cond))
            self.wait(0.6)
        nxt = note(r"Each choice of ROC gives a different $x(t)$. Let's take them one at a time.", color=YELLOW, fs=32).move_to(DOWN * 3.55)
        self.play(FadeIn(nxt, shift=UP * 0.15))
        self.wait(2.5)
        fade_all(self)

    # --- one case per frame ------------------------------------------------------------------------------
    def p2_case(self, k, c):
        head = Tex(rf"Case {k}:\ \ ROC $\ {c['roc_tex']}$", font_size=44, color=BLUE_B)
        head.to_edge(UP, buff=0.3)
        expand = MathTex(r"X(s)=", r"\frac{1}{s+1}", r"-", r"\frac{1}{s+2}", font_size=40)
        expand[1].set_color(TEAL_C)
        expand[3].set_color(GOLD)
        expand.next_to(head, DOWN, buff=0.3)
        self.play(Write(head))
        self.play(FadeIn(expand))

        # ---- stage A : read the ROC against each pole
        sp = SPlane(x_range=(-3.5, 1.5, 1), y_range=(-1.5, 1.5, 1), x_length=6.0, y_length=3.0, number_size=18)
        sp.move_to(LEFT * 3.3 + DOWN * 0.8)
        p1 = sp.pole(-1, color=TEAL_C)
        p2 = sp.pole(-2, color=GOLD)
        l1 = MathTex(r"-1", font_size=30, color=TEAL_C).next_to(sp.c2p(-1, 0), DOWN, buff=0.2)
        l2 = MathTex(r"-2", font_size=30, color=GOLD).next_to(sp.c2p(-2, 0), DOWN, buff=0.2)
        region = sp.roc(**c["roc"], opacity=0.45)
        arrows = VGroup(
            Arrow(sp.c2p(-1, 0.8), sp.c2p(-1, 0.8) + c["sides"][0] * 0.6, buff=0, color=TEAL_C, stroke_width=5,
                  max_tip_length_to_length_ratio=0.4),
            Arrow(sp.c2p(-2, 0.8), sp.c2p(-2, 0.8) + c["sides"][1] * 0.6, buff=0, color=GOLD, stroke_width=5,
                  max_tip_length_to_length_ratio=0.4),
        )
        stageA = VGroup(sp, p1, p2, l1, l2, region, arrows)
        self.play(FadeIn(sp), FadeIn(p1), FadeIn(p2), FadeIn(l1), FadeIn(l2))
        self.play(FadeIn(region))
        self.wait(0.5)

        def side_word(side):
            return "right" if np.allclose(side, RIGHT) else "left"

        def kind_word(side):
            return "right-sided" if np.allclose(side, RIGHT) else "left-sided"

        term1 = MathTex(r"\frac{1}{s+1}", r"\ \longrightarrow\ ", c["t1"], font_size=46).move_to(RIGHT * 3.2 + UP * 0.6)
        term2 = MathTex(r"-\frac{1}{s+2}", r"\ \longrightarrow\ ", c["t2"], font_size=46).move_to(RIGHT * 3.2 + DOWN * 1.5)
        for tm, col in ((term1, TEAL_C), (term2, GOLD)):
            tm[0].set_color(col)
            tm[2].set_color(col)
        cap1 = note(rf"ROC is to the {side_word(c['sides'][0])} of the pole $-1$: {kind_word(c['sides'][0])}", color=TEAL_C,
                    fs=28).next_to(term1, DOWN, buff=0.25)
        cap2 = note(rf"ROC is to the {side_word(c['sides'][1])} of the pole $-2$: {kind_word(c['sides'][1])}", color=GOLD,
                    fs=28).next_to(term2, DOWN, buff=0.25)
        self.play(GrowArrow(arrows[0]))
        self.play(FadeIn(cap1))
        self.play(Write(term1))
        self.wait(1)
        self.play(GrowArrow(arrows[1]))
        self.play(FadeIn(cap2))
        self.play(Write(term2))
        self.wait(1.5)

        # ---- stage B : tuck the explanation away and plot
        self.play(FadeOut(cap1), FadeOut(cap2))
        ax = signal_axes(x_range=(-3, 4, 1), y_range=(-2, 2, 1), x_length=6.2, y_length=3.6)
        ax.move_to(RIGHT * 3.6 + DOWN * 1.0)
        terms = VGroup(term1, term2)
        self.play(stageA.animate.scale(0.7).move_to(LEFT * 4.5 + UP * 0.1),
                  terms.animate.scale(0.75).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 4.3 + DOWN * 2.4),
                  run_time=1.5)
        self.play(Create(ax))
        g1 = clipped_graph(ax, c["f1"], -3, 4, breaks=[0], color=TEAL_C, stroke_width=4, opacity=0.9)
        g2 = clipped_graph(ax, c["f2"], -3, 4, breaks=[0], color=GOLD, stroke_width=4, opacity=0.9)
        gs = clipped_graph(ax, lambda t: c["f1"](t) + c["f2"](t), -3, 4, breaks=[0], color=YELLOW, stroke_width=7)
        self.play(Create(g1), run_time=1.3)
        self.play(Create(g2), run_time=1.3)
        total = MathTex(c["sum"], font_size=38, color=YELLOW).next_to(ax, UP, buff=0.25)
        self.play(Write(total))
        self.play(Create(gs), run_time=1.8)
        kind = Tex(c["kind"], font_size=34, color=YELLOW).next_to(ax, DOWN, buff=0.2)
        self.play(FadeIn(kind, shift=UP * 0.1))
        self.wait(3)
        fade_all(self)

    # --- recap ----------------------------------------------------------------------------------------------
    def p2_recap(self):
        title = make_title(r"One $X(s)$, three ROCs, three signals")
        X = MathTex(r"X(s)=\frac{1}{(s+1)(s+2)}", font_size=48).move_to(UP * 2.0)
        rows = VGroup(
            MathTex(r"\mathrm{Re}\{s\}>-1", r"\ \Rightarrow\ ", r"x(t)=\big(e^{-t}-e^{-2t}\big)u(t)", font_size=40),
            MathTex(r"\mathrm{Re}\{s\}<-2", r"\ \Rightarrow\ ", r"x(t)=\big(-e^{-t}+e^{-2t}\big)u(-t)", font_size=40),
            MathTex(r"-2<\mathrm{Re}\{s\}<-1", r"\ \Rightarrow\ ", r"x(t)=-e^{-t}u(-t)-e^{-2t}u(t)", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 0.4)
        for r, col in zip(rows, (GREEN_C, RED_C, BLUE_C)):
            r[0].set_color(col)
        self.play(Write(title))
        self.play(Write(X))
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2))
            self.wait(0.8)
        final = Tex(r"$X(s)$ alone is not enough: you need $X(s)$ \emph{and} its ROC", font_size=36, color=YELLOW)
        final.move_to(DOWN * 3.0)
        self.play(FadeIn(final, shift=UP * 0.15))
        self.wait(1.2)
        last = Tex(r"the ROC picks the time direction of \emph{each} pole's exponential", font_size=34, color=YELLOW)
        last.move_to(final)
        self.play(FadeTransform(final, last))
        self.wait(3)
        fade_all(self)


# ======================================================================
#  single-chapter scenes, handy while iterating (render just one chapter)
# ======================================================================
class IL_Ch1_Derivation(InverseLaplaceBuildUp):
    def construct(self):
        self.chapter1()


class IL_Ch2_Bromwich(InverseLaplaceBuildUp):
    def construct(self):
        self.chapter2()


class IL_Ch3_ClosedContour(InverseLaplaceBuildUp):
    def construct(self):
        self.chapter3()


class PF_Ch1_Tools(PartialFractionsAndROC):
    def construct(self):
        self.chapter1()


class PF_Ch2_Example(PartialFractionsAndROC):
    def construct(self):
        self.chapter2()