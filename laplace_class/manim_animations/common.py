"""Shared styling and s-plane helpers for the Laplace transform animations.

Visual language borrowed from 3Blue1Brown's Laplace series: dark background,
the classic blue/teal/yellow palette, LaTeX everywhere, and the s-plane as the
main stage.
"""
from manim import *
import numpy as np

config.background_color = "#0c0c0f"

_tex = TexTemplate()
_tex.add_to_preamble(r"\usepackage{mathtools}")  # \xleftrightarrow etc.
config.tex_template = _tex

# ---------------------------------------------------------------- palette
SIG = BLUE_C          # time-domain signals
SIG2 = TEAL_C         # second signal / partner curve
WEIGHT = RED_C        # e^{-sigma t} weighting
PROD = YELLOW         # weighted / product signal
POLE_COLOR = RED_B
ZERO_COLOR = GREEN_B
ROC_COLOR = BLUE_D
JW_COLOR = YELLOW
GOOD = GREEN_C
BAD = RED_C


# ---------------------------------------------------------------- text
def make_title(text, font_size=44):
    t = Tex(text, font_size=font_size)
    t.to_edge(UP, buff=0.3)
    return t


def caption(text, font_size=32, color=WHITE):
    return Tex(text, font_size=font_size, color=color)


def check(ok=True, font_size=40):
    if ok:
        return MathTex(r"\checkmark", color=GOOD, font_size=font_size)
    return MathTex(r"\times", color=BAD, font_size=font_size)


def _fmt(v):
    return str(int(v)) if float(v).is_integer() else f"{v:g}"


# ---------------------------------------------------------------- s-plane
class SPlane(VGroup):
    """A NumberPlane dressed up as the complex s-plane (sigma, j omega)."""

    def __init__(
        self,
        x_range=(-3, 3, 1),
        y_range=(-3, 3, 1),
        x_length=5,
        y_length=5,
        numbers=True,
        axis_labels=True,
        number_size=20,
        y_number_side=LEFT,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.plane = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1.2,
                "stroke_opacity": 0.35,
            },
            faded_line_ratio=1,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        )
        self.add(self.plane)
        self.x_min, self.x_max = x_range[0], x_range[1]
        self.y_min, self.y_max = y_range[0], y_range[1]

        if numbers:
            nums = VGroup()
            for x in np.arange(x_range[0], x_range[1] + 1e-9, x_range[2]):
                if abs(x) < 1e-9 or abs(x - x_range[0]) < 1e-9 or abs(x - x_range[1]) < 1e-9:
                    continue
                lab = MathTex(_fmt(round(x, 3)), font_size=number_size, color=GREY_A)
                lab.next_to(self.plane.c2p(x, 0), DOWN, buff=0.07)
                nums.add(lab)
            for y in np.arange(y_range[0], y_range[1] + 1e-9, y_range[2]):
                if abs(y) < 1e-9 or abs(y - y_range[0]) < 1e-9 or abs(y - y_range[1]) < 1e-9:
                    continue
                yv = round(y, 3)
                txt = {1: "j", -1: "-j"}.get(yv, f"{_fmt(yv)}j")
                lab = MathTex(txt, font_size=number_size, color=GREY_A)
                lab.next_to(self.plane.c2p(0, y), y_number_side, buff=0.07)
                nums.add(lab)
            self.numbers = nums
            self.add(nums)

        if axis_labels:
            sx = MathTex(r"\sigma", font_size=30)
            sx.next_to(self.plane.c2p(x_range[1], 0), UP + LEFT * 0.2, buff=0.1)
            sy = MathTex(r"j\omega", font_size=30)
            sy.next_to(self.plane.c2p(0, y_range[1]), RIGHT, buff=0.1).shift(DOWN * 0.15)
            self.axis_labels = VGroup(sx, sy)
            self.add(self.axis_labels)

    # coordinates ------------------------------------------------------
    def c2p(self, x, y=0):
        return self.plane.c2p(x, y)

    def s2p(self, s):
        s = complex(s)
        return self.plane.c2p(s.real, s.imag)

    def unit(self):
        return self.plane.get_x_unit_size()

    # decorations ------------------------------------------------------
    def roc(self, left=None, right=None, color=ROC_COLOR, opacity=0.4, boundary=True):
        l = self.x_min if left is None else min(max(left, self.x_min), self.x_max)
        r = self.x_max if right is None else max(min(right, self.x_max), self.x_min)
        grp = VGroup()
        if r - l < 1e-6:
            return grp
        rect = Polygon(
            self.c2p(l, self.y_min),
            self.c2p(r, self.y_min),
            self.c2p(r, self.y_max),
            self.c2p(l, self.y_max),
            stroke_width=0,
            fill_color=color,
            fill_opacity=opacity,
        )
        grp.add(rect)
        if boundary:
            for edge in (left, right):
                if edge is not None and self.x_min < edge < self.x_max:
                    grp.add(
                        DashedLine(
                            self.c2p(edge, self.y_min),
                            self.c2p(edge, self.y_max),
                            color=color,
                            stroke_width=3,
                            dash_length=0.1,
                        ).set_stroke(opacity=1)
                    )
        return grp

    def pole(self, s, color=POLE_COLOR, size=0.13, width=5):
        return pole_marker(self.s2p(s), color=color, size=size, width=width)

    def zero(self, s, color=ZERO_COLOR, radius=0.11, width=4):
        return zero_marker(self.s2p(s), color=color, radius=radius, width=width)

    def vline(self, sigma, color=YELLOW, width=4):
        return Line(self.c2p(sigma, self.y_min), self.c2p(sigma, self.y_max), color=color, stroke_width=width)

    def jw_axis(self, color=JW_COLOR, width=6):
        return self.vline(0, color=color, width=width)


def pole_marker(point, color=POLE_COLOR, size=0.13, width=5):
    return VGroup(
        Line(point + size * UL, point + size * DR),
        Line(point + size * UR, point + size * DL),
    ).set_stroke(color, width)


def zero_marker(point, color=ZERO_COLOR, radius=0.11, width=4):
    return Circle(radius=radius, color=color, stroke_width=width).move_to(point)


# ---------------------------------------------------------------- time axes
def signal_axes(
    x_range=(-3, 5, 1),
    y_range=(-1.5, 1.5, 0.5),
    x_length=6,
    y_length=3,
    x_label="t",
    y_label=None,
    label_size=30,
):
    ax = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "stroke_color": GREY_B,
            "stroke_width": 2,
            "tick_size": 0.05,
            "tip_width": 0.18,
            "tip_height": 0.18,
        },
    )
    labels = VGroup()
    if x_label:
        labels.add(MathTex(x_label, font_size=label_size).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1))
    if y_label:
        labels.add(MathTex(y_label, font_size=label_size).next_to(ax.y_axis.get_end(), UP, buff=0.1))
    ax.add(labels)
    return ax


def _runs_to_vgroup(runs):
    g = VGroup()
    for pts in runs:
        if len(pts) >= 2:
            g.add(VMobject().set_points_as_corners(pts))
    return g


def clipped_graph(ax, f, x_min, x_max, breaks=(), n=500, y_lim=None, color=SIG, stroke_width=4, opacity=1.0):
    """Graph of f on [x_min, x_max] that simply leaves the axes when |f| gets too big.

    `breaks` lists x-values where f jumps (e.g. 0 for u(t)); no vertical
    segment is drawn across them.
    """
    ymin, ymax = y_lim if y_lim else (ax.y_range[0], ax.y_range[1])
    edges = [x_min] + [b for b in breaks if x_min < b < x_max] + [x_max]
    eps = 1e-5
    runs = []
    with np.errstate(all="ignore"):
        for i in range(len(edges) - 1):
            a = edges[i] + (eps if i > 0 else 0.0)
            b = edges[i + 1] - (eps if i < len(edges) - 2 else 0.0)
            m = max(int(n * (b - a) / (x_max - x_min)), 3)
            xs = np.linspace(a, b, m)
            ys = np.array([f(x) for x in xs], dtype=float)
            finite = np.isfinite(ys)
            inside = finite & (ys >= ymin) & (ys <= ymax)
            keep = inside.copy()
            keep[1:] |= inside[:-1]
            keep[:-1] |= inside[1:]
            keep &= finite | inside
            ys_c = np.clip(np.nan_to_num(ys, nan=0.0, posinf=ymax, neginf=ymin), ymin, ymax)
            run = []
            for x, y, k in zip(xs, ys_c, keep):
                if k:
                    run.append(ax.c2p(x, y))
                elif run:
                    runs.append(run)
                    run = []
            if run:
                runs.append(run)
    g = _runs_to_vgroup(runs)
    g.set_stroke(color, stroke_width, opacity=opacity)
    return g


def clipped_area(ax, f, x_min, x_max, n=300, color=PROD, opacity=0.3):
    """Filled region between f and the t-axis, clipped to the axes' y-range."""
    ymin, ymax = ax.y_range[0], ax.y_range[1]
    xs = np.linspace(x_min, x_max, n)
    with np.errstate(all="ignore"):
        ys = np.array([f(x) for x in xs], dtype=float)
    ys = np.clip(np.nan_to_num(ys, nan=0.0, posinf=ymax, neginf=ymin), ymin, ymax)
    pts = [ax.c2p(x_min, 0)] + [ax.c2p(x, y) for x, y in zip(xs, ys)] + [ax.c2p(x_max, 0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def clipped_path(coords, to_point, xlim, ylim, color=SIG, stroke_width=4):
    """Polyline through 2D `coords` (plane units), dropping parts outside the box."""
    runs, run = [], []
    for x, y in coords:
        if np.isfinite(x) and np.isfinite(y) and xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]:
            run.append(to_point(x, y))
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    return _runs_to_vgroup(runs).set_stroke(color, stroke_width)


def u(t):
    """Unit step."""
    return 1.0 if t >= 0 else 0.0


def fade_all(scene, run_time=1.0):
    """Freeze every always_redraw/updater, then fade the whole stage out."""
    for m in scene.mobjects:
        m.clear_updaters()
    scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)


def clipped_polyline(ax, xs, ys, color=SIG, stroke_width=4, opacity=1.0):
    """Like clipped_graph, but for precomputed samples (xs, ys)."""
    ymin, ymax = ax.y_range[0], ax.y_range[1]
    ys = np.asarray(ys, dtype=float)
    finite = np.isfinite(ys)
    inside = finite & (ys >= ymin) & (ys <= ymax)
    keep = inside.copy()
    keep[1:] |= inside[:-1]
    keep[:-1] |= inside[1:]
    ys_c = np.clip(np.nan_to_num(ys, nan=0.0, posinf=ymax, neginf=ymin), ymin, ymax)
    runs, run = [], []
    for x, y, k in zip(xs, ys_c, keep):
        if k:
            run.append(ax.c2p(x, y))
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    return _runs_to_vgroup(runs).set_stroke(color, stroke_width, opacity=opacity)
