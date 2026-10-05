"""Shared look and 3D helpers for the from-scratch Laplace transform series.

Same visual language as ../manim_animations (dark background, blue/teal/yellow
palette, LaTeX everywhere), but every scene is 3D. Two coordinate conventions:

* complex-time space: x = t, y = Re, z = Im   (e^{st} is a helix running left to right)
* s-plane landscape:  x = sigma, y = omega, z = |X(s)|

Scenes are built for presenting: little text on screen, and `self.beat(label)`
marks a natural pause point. Beat times are written to beats/<Scene>.json and
used by the presenter player and the chapter markers.
"""
from manim import *
from manim.camera.camera import Camera
from manim.camera.three_d_camera import ThreeDCamera
import cairo
import json
from pathlib import Path
import numpy as np

config.background_color = "#0c0c0f"

_tex = TexTemplate()
_tex.add_to_preamble(r"\usepackage{mathtools}")
config.tex_template = _tex

BEATS_DIR = Path(__file__).resolve().parent / "beats"

# ---------------------------------------------------------------- palette
SIG = BLUE_C          # signals / e^{st}
SIG2 = TEAL_C
WEIGHT = RED_C        # e^{-sigma t}
PROD = YELLOW
RE_COLOR = TEAL_C     # real part, cos
IM_COLOR = GOLD_C     # imaginary part, sin
POLE_COLOR = RED_B
ZERO_COLOR = GREEN_B
ROC_COLOR = BLUE_D
JW_COLOR = YELLOW
GOOD = GREEN_C
BAD = RED_C
AXIS_COLOR = GREY_B
LABEL_COLOR = GREY_A
PANEL_BG = "#0c0c0f"

HEIGHT_SCALE = [(BLUE_E, 0.0), (BLUE_C, 0.6), (TEAL_C, 1.3), (YELLOW, 2.2), (RED_C, 3.0)]


# ---------------------------------------------------------------- framing
def view_center(point, screen=(0.0, 0.0), phi=70 * DEGREES, theta=-40 * DEGREES, gamma=0.0, zoom=1.0):
    """frame_center that puts the 3D `point` at frame position `screen` (x, y)
    for the given camera angles (ignoring the mild perspective)."""
    R = rotation_about_z(gamma) @ rotation_matrix(-phi, RIGHT) @ rotation_about_z(-theta - PI / 2)
    v = np.array([screen[0] / zoom, screen[1] / zoom, 0.0])
    return np.asarray(point, dtype=float) - R.T @ v


def camera_at(scene, point, screen=(0.0, 0.0), phi=70 * DEGREES, theta=-40 * DEGREES, zoom=1.0, gamma=0.0):
    """set_camera_orientation with the framing given as 'point lands at screen'."""
    scene.set_camera_orientation(phi=phi, theta=theta, gamma=gamma, zoom=zoom,
                                 frame_center=view_center(point, screen, phi, theta, gamma, zoom))


def move_camera_to(scene, point, screen=(0.0, 0.0), phi=70 * DEGREES, theta=-40 * DEGREES, zoom=1.0, gamma=0.0, **kw):
    scene.move_camera(phi=phi, theta=theta, gamma=gamma, zoom=zoom,
                      frame_center=view_center(point, screen, phi, theta, gamma, zoom), **kw)


# ---------------------------------------------------------------- tagging
def tag_hud(mob, *_):
    """Overlay: drawn flat on the frame, ignoring the camera. Survives copies."""
    for m in mob.get_family():
        m.is_hud = True
    return mob


def tag_floor(mob):
    """Lies on the s-plane floor: always drawn before (under) the 3D surfaces."""
    for m in mob.get_family():
        m.layer = "floor"
    return mob


def depth_sorted(mob):
    """Sort with the surfaces by depth, but keep the stroke colour unshaded."""
    for m in mob.get_family():
        m.shade_in_3d = True
        m.no_shading = True
    return mob


class HUDCamera(ThreeDCamera):
    """ThreeDCamera with three draw layers: floor, 3D (depth sorted), overlays.

    ThreeDCamera tracks fixed-in-frame mobjects by identity, which breaks for
    copies (FadeTransform, TransformMatchingTex) and rebuilt submobjects
    (DecimalNumber, always_redraw). Here overlays are tagged instead.
    """

    def transform_points_pre_display(self, mobject, points):
        if getattr(mobject, "is_hud", False):
            return Camera.transform_points_pre_display(self, mobject, points)
        return super().transform_points_pre_display(mobject, points)

    # ThreeDCamera already applies frame_center in its projection. The stock 2D
    # path applies it a second time, and the cairo context even caches the
    # frame_center of the moment it was created. Both are pinned to the origin
    # here, so frame_center is a plain look-at point and overlays never drift.
    def get_cairo_context(self, pixel_array):
        cached = self.get_cached_cairo_context(pixel_array)
        if cached:
            return cached
        pw, ph = self.pixel_width, self.pixel_height
        fw, fh = self.frame_width, self.frame_height
        surface = cairo.ImageSurface.create_for_data(pixel_array.data, cairo.FORMAT_ARGB32, pw, ph)
        ctx = cairo.Context(surface)
        ctx.scale(pw, ph)
        ctx.set_matrix(cairo.Matrix(pw / fw, 0, 0, -(ph / fh), pw / 2, ph / 2))
        self.cache_cairo_context(pixel_array, ctx)
        return ctx

    def points_to_subpixel_coords(self, mobject, points):
        points = self.transform_points_pre_display(mobject, points)
        result = np.zeros((len(points), 2))
        result[:, 0] = points[:, 0] * (self.pixel_width / self.frame_width) + self.pixel_width / 2
        result[:, 1] = points[:, 1] * -(self.pixel_height / self.frame_height) + self.pixel_height / 2
        return result

    def get_mobjects_to_display(self, *args, **kwargs):
        mobjects = Camera.get_mobjects_to_display(self, *args, **kwargs)
        rot = self.get_rotation_matrix()

        def key(m):
            if getattr(m, "is_hud", False):
                return (3, getattr(m, "hud_layer", 0))
            if getattr(m, "layer", None) == "floor":
                return (0, 0.0)
            if getattr(m, "shade_in_3d", False):
                return (1, float(np.dot(m.get_z_index_reference_point(), rot.T)[2]))
            return (2, 0.0)

        return sorted(mobjects, key=key)

    def modified_rgbas(self, vmobject, rgbas):
        if getattr(vmobject, "no_shading", False):
            return rgbas
        return super().modified_rgbas(vmobject, rgbas)


class LScene(ThreeDScene):
    """Base scene: overlay text, camera-facing labels, beats."""

    def __init__(self, **kwargs):
        super().__init__(camera_class=HUDCamera, **kwargs)

    def setup(self):
        super().setup()
        self.beats = []
        self._title = None
        self._live_huds = []

    def update_mobjects(self, dt):
        super().update_mobjects(dt)
        for m in self._live_huds:  # after every updater, so rebuilt submobjects get tagged
            tag_hud(m)

    # overlays ---------------------------------------------------------
    def hud(self, *mobs, live=False):
        """Tag mobjects as overlays (not added to the scene). live=True keeps
        re-tagging, for mobjects whose submobjects get rebuilt."""
        for m in mobs:
            tag_hud(m)
            if live:
                self._live_huds.append(m)
        return mobs[0] if len(mobs) == 1 else VGroup(*mobs)

    def face_camera(self, *mobs):
        """3D-positioned labels that always face the camera (not added to the scene).

        A plain VGroup is unpacked so each label pivots about its own centre."""
        for m in mobs:
            for lab in (m.submobjects if type(m) is VGroup else [m]):
                self.renderer.camera.add_fixed_orientation_mobjects(lab)
        return mobs[0] if len(mobs) == 1 else VGroup(*mobs)

    def set_title(self, text, run_time=0.8):
        new = self.hud(Tex(text, font_size=40, color=GREY_A).to_corner(UL, buff=0.35))
        if self._title is None:
            self.play(FadeIn(new, shift=0.2 * DOWN), run_time=run_time)
        else:
            self.play(FadeOut(self._title, shift=0.2 * UP), FadeIn(new, shift=0.2 * DOWN), run_time=run_time)
        self._title = new
        return new

    def panel(self, mob, buff=0.15, opacity=0.8):
        """Overlay with a dark backing rectangle so it reads over 3D content.

        Returns VGroup(background, mob); the background always draws beneath
        overlay text, whatever order things are added in."""
        bg = BackgroundRectangle(mob, fill_color=PANEL_BG, fill_opacity=opacity, buff=buff)
        bg.hud_layer = -1
        return self.hud(VGroup(bg, mob))

    # pacing -----------------------------------------------------------
    def beat(self, label, hold=1.5):
        """A natural pause point for the presenter."""
        self.beats.append({"t": round(float(self.time), 3), "label": label})
        self.wait(hold)

    def clear_all(self, run_time=1.0):
        for m in self.mobjects:
            m.clear_updaters()
        self.stop_ambient_camera_rotation()
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)
        self._title = None

    def tear_down(self):
        super().tear_down()
        BEATS_DIR.mkdir(exist_ok=True)
        data = {"scene": type(self).__name__, "duration": round(float(self.time), 3), "beats": self.beats}
        (BEATS_DIR / f"{type(self).__name__}.json").write_text(json.dumps(data, indent=1))


# ---------------------------------------------------------------- polylines
def pts(ax, *coords):
    """Vectorised ax.c2p: arrays of coordinates -> (n, 3) array of points."""
    arrs = [np.atleast_1d(np.asarray(c, dtype=float)) for c in coords]
    n = max(len(a) for a in arrs)
    arrs = [np.broadcast_to(a, (n,)) for a in arrs]
    return np.asarray(ax.c2p(*arrs)).T.reshape(n, 3)


def polyline(points, color=SIG, width=4, opacity=1.0):
    m = VMobject()
    if len(points) >= 2:
        m.set_points_as_corners(points)
    m.set_stroke(color, width, opacity=opacity)
    return m


def true_runs(mask):
    """Index arrays of consecutive True runs, each padded by one neighbour."""
    idx = np.flatnonzero(mask)
    if len(idx) == 0:
        return []
    splits = np.flatnonzero(np.diff(idx) > 1) + 1
    out = []
    for run in np.split(idx, splits):
        lo, hi = max(run[0] - 1, 0), min(run[-1] + 1, len(mask) - 1)
        out.append(np.arange(lo, hi + 1))
    return out


def complex_curve(ax, z, t0, t1, n=400, rmax=None, color=SIG, width=4, opacity=1.0, depth=False, seg=5):
    """Curve t -> (t, Re z(t), Im z(t)) in complex-time axes.

    `z` must accept numpy arrays. Parts with |z| > rmax are dropped (the curve
    ends on the boundary). depth=True cuts it into short depth-sorted pieces
    so it can pass behind surfaces.
    """
    ts = np.linspace(t0, t1, n)
    with np.errstate(all="ignore"):
        zs = np.asarray(z(ts), dtype=complex) * np.ones_like(ts)
    finite = np.isfinite(zs)
    mask = finite if rmax is None else finite & (np.abs(zs) <= rmax)
    grp = VGroup()
    for run in true_runs(mask):
        zr = zs[run].copy()
        tr = ts[run]
        if rmax is not None:
            big = ~np.isfinite(zr) | (np.abs(zr) > rmax)
            if big.any():
                # pull the overshooting end points back onto the boundary
                zr[big] = np.nan_to_num(zr[big]) / np.maximum(np.abs(np.nan_to_num(zr[big])), 1e-9) * rmax
        p3 = pts(ax, tr, zr.real, zr.imag)
        if depth:
            for i in range(0, len(p3) - 1, seg):
                grp.add(polyline(p3[i:i + seg + 1], color, width, opacity))
        else:
            grp.add(polyline(p3, color, width, opacity))
    if depth:
        depth_sorted(grp)
    return grp


def real_curve(ax, f, t0, t1, n=300, ylim=None, color=SIG, width=4, opacity=1.0, plane="xz", offset=0.0):
    """Graph of a real function drawn in a coordinate plane of 3D axes.

    plane="xz": points (t, offset, f(t))   (a wall)
    plane="xy": points (t, f(t), offset)   (the floor)
    """
    ts = np.linspace(t0, t1, n)
    with np.errstate(all="ignore"):
        ys = np.asarray(f(ts), dtype=float) * np.ones_like(ts)
    lo, hi = ylim if ylim else (-np.inf, np.inf)
    mask = np.isfinite(ys) & (ys >= lo) & (ys <= hi)
    grp = VGroup()
    for run in true_runs(mask):
        yr = np.clip(np.nan_to_num(ys[run], nan=0.0, posinf=hi, neginf=lo), lo, hi)
        tr = ts[run]
        if plane == "xz":
            p3 = pts(ax, tr, offset, yr)
        else:
            p3 = pts(ax, tr, yr, offset)
        grp.add(polyline(p3, color, width, opacity))
    return grp


# ---------------------------------------------------------------- the complex plane inside complex-time space
def cpoint(ax, z, t=0.0):
    """Point of complex value z in the complex plane sitting at time t."""
    return ax.c2p(t, np.real(z), np.imag(z))


def cplane_arrow(ax, z, t=0.0, start=0j, color=SIG, width=5, tip=0.22):
    """Flat arrow from `start` to `z`, lying in the complex plane at time t."""
    a, b = cpoint(ax, start, t), cpoint(ax, z, t)
    d = b - a
    L = np.linalg.norm(d)
    if L < 1e-6:
        return VGroup(Line(a, a + 1e-4 * UP, stroke_width=0))
    unit = d / L
    tip = min(tip, 0.45 * L)
    perp = np.cross(RIGHT, unit)
    base = b - tip * unit
    line = Line(a, base, color=color, stroke_width=width)
    head = Polygon(b, base + 0.55 * tip * perp, base - 0.55 * tip * perp, stroke_width=0, fill_color=color, fill_opacity=1)
    return VGroup(line, head)


def cplane_arc(ax, r, a0, a1, t=0.0, color=WHITE, width=3, n=60):
    phis = np.linspace(a0, a1, max(int(n * abs(a1 - a0) / TAU) + 2, 6))
    return polyline(pts(ax, t, r * np.cos(phis), r * np.sin(phis)), color, width)


def cplane_grid(ax, t=0.0, step=0.5, opacity=0.35):
    r0, r1 = ax.y_range[:2]
    g = VGroup()
    for v in np.arange(np.ceil(r0 / step) * step, r1 + 1e-9, step):
        if abs(v) < 1e-9:
            continue
        g.add(Line(ax.c2p(t, v, r0), ax.c2p(t, v, r1)), Line(ax.c2p(t, r0, v), ax.c2p(t, r1, v)))
    g.set_stroke(BLUE_D, 1, opacity=opacity)
    return g


def shadow_walls(ax, opacity=0.12, step=1.0):
    """The Im = -r floor and the Re = +r back wall of complex-time space."""
    t0, t1 = ax.x_range[:2]
    r = ax.y_range[1]
    floor = Polygon(ax.c2p(t0, -r, -r), ax.c2p(t1, -r, -r), ax.c2p(t1, r, -r), ax.c2p(t0, r, -r),
                    stroke_width=0, fill_color=GREY_D, fill_opacity=opacity)
    wall = Polygon(ax.c2p(t0, r, -r), ax.c2p(t1, r, -r), ax.c2p(t1, r, r), ax.c2p(t0, r, r),
                   stroke_width=0, fill_color=GREY_D, fill_opacity=opacity)
    grid = VGroup()
    for tt in np.arange(t0, t1 + 1e-9, step):
        grid.add(Line(ax.c2p(tt, -r, -r), ax.c2p(tt, r, -r)), Line(ax.c2p(tt, r, -r), ax.c2p(tt, r, r)))
    grid.add(Line(ax.c2p(t0, 0, -r), ax.c2p(t1, 0, -r)), Line(ax.c2p(t0, r, 0), ax.c2p(t1, r, 0)))
    grid.set_stroke(GREY_C, 1, opacity=0.35)
    return tag_floor(VGroup(floor, wall, grid))


def envelope(ax, sigma, t_max, rmax, color=RED_B, t_min=0.0):
    """Translucent funnel of radius e^{sigma t} around the t-axis, t in [t_min, t_max],
    cut where the radius would exceed rmax."""
    lo, hi = t_min, t_max
    if sigma > 1e-9:
        hi = min(hi, np.log(rmax) / sigma)
    elif sigma < -1e-9:
        lo = max(lo, np.log(rmax) / sigma)
    if hi - lo < 0.05:
        hi = lo + 0.05
    return Surface(
        lambda u, v: ax.c2p(u, np.exp(sigma * u) * np.cos(v), np.exp(sigma * u) * np.sin(v)),
        u_range=[lo, hi], v_range=[0, TAU], resolution=(28, 18),
        fill_color=color, fill_opacity=0.10, stroke_color=color, stroke_width=0.6, stroke_opacity=0.35,
        checkerboard_colors=False,
    )


# ---------------------------------------------------------------- axes
def complex_time_axes(t_range=(0, 8, 1), r=1.5, t_length=9.0, r_length=3.4, tips=False):
    """x = t, y = Re, z = Im."""
    return ThreeDAxes(
        x_range=list(t_range), y_range=[-r, r, 1], z_range=[-r, r, 1],
        x_length=t_length, y_length=r_length, z_length=r_length,
        axis_config={"stroke_color": AXIS_COLOR, "include_tip": tips, "stroke_width": 2, "tick_size": 0.05},
    )


def ct_labels(ax, t_label="t", size=36):
    """Camera-facing axis names for complex-time axes (pass to scene.face_camera)."""
    x1 = ax.x_range[1]
    y1 = ax.y_range[1]
    z1 = ax.z_range[1]
    return VGroup(
        MathTex(t_label, font_size=size, color=LABEL_COLOR).move_to(ax.c2p(x1 + 0.35, 0, 0)),
        MathTex(r"\mathrm{Re}", font_size=size - 4, color=RE_COLOR).move_to(ax.c2p(0, y1 + 0.35, 0)),
        MathTex(r"\mathrm{Im}", font_size=size - 4, color=IM_COLOR).move_to(ax.c2p(0, 0, z1 + 0.3)),
    )


def splane_axes(u_range=(-3, 3), v_range=(-3, 3), z_max=3.0, x_length=6.0, y_length=6.0, z_length=3.0, step=1):
    """x = sigma, y = omega, z = height (e.g. |X(s)|)."""
    return ThreeDAxes(
        x_range=[u_range[0], u_range[1], step], y_range=[v_range[0], v_range[1], step], z_range=[0, z_max, 1],
        x_length=x_length, y_length=y_length, z_length=z_length,
        axis_config={"stroke_color": AXIS_COLOR, "include_tip": False, "stroke_width": 2, "tick_size": 0.05},
    )


def splane_floor(ax, step=1, opacity=0.35):
    u0, u1 = ax.x_range[:2]
    v0, v1 = ax.y_range[:2]
    lines = VGroup()
    for u in np.arange(np.ceil(u0 / step) * step, u1 + 1e-9, step):
        lines.add(Line(ax.c2p(u, v0, 0), ax.c2p(u, v1, 0)))
    for v in np.arange(np.ceil(v0 / step) * step, v1 + 1e-9, step):
        lines.add(Line(ax.c2p(u0, v, 0), ax.c2p(u1, v, 0)))
    lines.set_stroke(BLUE_D, 1, opacity=opacity)
    return tag_floor(lines)


def splane_labels(ax, size=36, z_label=None):
    u1 = ax.x_range[1]
    v1 = ax.y_range[1]
    g = VGroup(
        MathTex(r"\sigma", font_size=size, color=LABEL_COLOR).move_to(ax.c2p(u1 + 0.35, 0, 0)),
        MathTex(r"j\omega", font_size=size, color=LABEL_COLOR).move_to(ax.c2p(0, v1 + 0.4, 0)),
    )
    if z_label:
        g.add(MathTex(z_label, font_size=size - 4, color=LABEL_COLOR).move_to(ax.c2p(0, 0, ax.z_range[1] + 0.45)))
    return g


def floor_ticks(ax, us=(), vs=(), size=24, flat=True):
    """Tick numbers printed on the floor (flat) along the sigma and j omega axes."""
    g = VGroup()
    for u in us:
        g.add(MathTex(_fmt(u), font_size=size, color=LABEL_COLOR).move_to(ax.c2p(u, -0.28, 0)))
    for v in vs:
        txt = {1: "j", -1: "-j"}.get(v, f"{_fmt(v)}j")
        g.add(MathTex(txt, font_size=size, color=LABEL_COLOR).move_to(ax.c2p(-0.32, v, 0)))
    return tag_floor(g) if flat else g


def _fmt(v):
    return str(int(v)) if float(v).is_integer() else f"{v:g}"


# ---------------------------------------------------------------- s-plane decorations (3D)
def roc_floor(ax, left=None, right=None, color=ROC_COLOR, opacity=0.35, edges=True):
    u0, u1 = ax.x_range[:2]
    v0, v1 = ax.y_range[:2]
    l = u0 if left is None else max(left, u0)
    r = u1 if right is None else min(right, u1)
    g = VGroup()
    if r > l:
        g.add(Polygon(ax.c2p(l, v0, 0), ax.c2p(r, v0, 0), ax.c2p(r, v1, 0), ax.c2p(l, v1, 0),
                      stroke_width=0, fill_color=color, fill_opacity=opacity))
    if edges:
        for e in (left, right):
            if e is not None and u0 < e < u1:
                g.add(DashedLine(ax.c2p(e, v0, 0), ax.c2p(e, v1, 0), color=color, stroke_width=3, dash_length=0.12))
    return tag_floor(g)


def floor_vline(ax, sigma, color=YELLOW, width=5, v_range=None):
    v0, v1 = v_range if v_range else ax.y_range[:2]
    return tag_floor(Line(ax.c2p(sigma, v0, 0), ax.c2p(sigma, v1, 0), color=color, stroke_width=width))


def pole_x(ax, s, size=0.16, color=POLE_COLOR, width=6, z=0.0):
    p = ax.c2p(np.real(s), np.imag(s), z)
    return VGroup(Line(p + size * (UP + LEFT), p + size * (DOWN + RIGHT)),
                  Line(p + size * (UP + RIGHT), p + size * (DOWN + LEFT))).set_stroke(color, width)


def zero_o(ax, s, radius=0.14, color=ZERO_COLOR, width=5, z=0.0):
    return Circle(radius=radius, color=color, stroke_width=width).move_to(ax.c2p(np.real(s), np.imag(s), z))


def pz_markers(ax, poles=(), zeros=(), floor=False):
    g = VGroup()
    for p in poles:
        g.add(pole_x(ax, p))
    for i, zz in enumerate(zeros):
        rep = sum(1 for w in list(zeros)[:i] if abs(w - zz) < 1e-9)
        g.add(zero_o(ax, zz, radius=0.14 + 0.08 * rep))
    return tag_floor(g) if floor else g


# ---------------------------------------------------------------- landscapes
def safe_abs(F, s):
    with np.errstate(all="ignore"):
        try:
            v = abs(F(s))
        except ZeroDivisionError:
            return np.inf
    return v if np.isfinite(v) else np.inf


def landscape(ax, F, u_range=None, v_range=None, res=(48, 48), zmax=None, roc=None,
              opacity=0.9, ghost=0.12, colorscale=None, stroke=0.3):
    """Surface of |F(sigma + j omega)|, clipped at zmax.

    Faces entirely above zmax are hidden (not removed, so two landscapes with
    the same resolution can Transform into each other): poles read as open
    chimneys going up forever. roc=(left, right) dims faces outside the ROC.
    """
    u_range = u_range or tuple(ax.x_range[:2])
    v_range = v_range or tuple(ax.y_range[:2])
    zmax = zmax if zmax is not None else ax.z_range[1]

    def h(u, v):
        return min(safe_abs(F, complex(u, v)), zmax)

    surf = Surface(lambda u, v: ax.c2p(u, v, h(u, v)), u_range=u_range, v_range=v_range, resolution=res,
                   fill_opacity=opacity, stroke_width=stroke, stroke_color=BLUE_E, checkerboard_colors=False)
    surf.set_fill_by_value(axes=ax, colorscale=colorscale or HEIGHT_SCALE, axis=2)
    for f in surf.submobjects:
        f.is_cap = min(h(f.u1, f.v1), h(f.u2, f.v1), h(f.u1, f.v2), h(f.u2, f.v2)) >= zmax - 1e-6
    set_roc_ghost(surf, roc, opacity=opacity, ghost=ghost)
    return surf


def set_roc_ghost(surf, roc=None, opacity=0.9, ghost=0.12):
    """Full opacity inside roc=(left, right) (None = unbounded), ghosted outside."""
    left, right = roc if roc is not None else (None, None)
    left = -np.inf if left is None else left
    right = np.inf if right is None else right
    for f in surf.submobjects:
        if getattr(f, "is_cap", False):
            f.set_fill(opacity=0)
            f.set_stroke(opacity=0)
            continue
        uc = 0.5 * (f.u1 + f.u2)
        inside = left < uc < right
        f.set_fill(opacity=opacity if inside else ghost)
        f.set_stroke(opacity=1.0 if inside else ghost)
    return surf


def roc_transition(surf, old=None, new=None, opacity=0.9, ghost=0.12, **kw):
    """Animation: the lit part of a landscape moves from ROC `old` to ROC `new`
    (each a (left, right) pair, None = the whole plane)."""
    def inside(f, roc):
        if roc is None:
            return True
        l, r = roc
        uc = 0.5 * (f.u1 + f.u2)
        return (l is None or uc > l) and (r is None or uc < r)

    faces = surf.submobjects
    f0 = [opacity if inside(f, old) else ghost for f in faces]
    f1 = [opacity if inside(f, new) else ghost for f in faces]
    s0 = [1.0 if inside(f, old) else ghost for f in faces]
    s1 = [1.0 if inside(f, new) else ghost for f in faces]

    def upd(m, a):
        for f, a0, a1, b0, b1 in zip(m.submobjects, f0, f1, s0, s1):
            if getattr(f, "is_cap", False):
                f.set_fill(opacity=0)
                f.set_stroke(opacity=0)
            else:
                f.set_fill(opacity=a0 + (a1 - a0) * a)
                f.set_stroke(opacity=b0 + (b1 - b0) * a)

    return UpdateFromAlphaFunc(surf, upd, **kw)


def jw_slice(ax, F, sigma=0.0, v_range=None, zmax=None, color=YELLOW, width=6, lift=0.03, n=400):
    v0, v1 = v_range or ax.y_range[:2]
    zmax = zmax if zmax is not None else ax.z_range[1]
    vs = np.linspace(v0, v1, n)
    hs = np.array([safe_abs(F, complex(sigma, v)) for v in vs])
    mask = hs <= zmax
    g = VGroup()
    for run in true_runs(mask):
        hr = np.minimum(hs[run], zmax)
        g.add(polyline(pts(ax, sigma, vs[run], hr + lift), color, width))
    return g


# ---------------------------------------------------------------- 2D overlay plots
class MiniSPlane(VGroup):
    """A small flat s-plane for overlays (tag it with scene.hud)."""

    def __init__(self, x_range=(-3, 3, 1), y_range=(-3, 3, 1), width=3.0, height=3.0, numbers=True, size=20, **kw):
        super().__init__(**kw)
        self.plane = NumberPlane(
            x_range=x_range, y_range=y_range, x_length=width, y_length=height,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.3},
            faded_line_ratio=1, axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        )
        self.add(self.plane)
        self.x_min, self.x_max = x_range[:2]
        self.y_min, self.y_max = y_range[:2]
        self.labels = VGroup(
            MathTex(r"\sigma", font_size=size + 6).next_to(self.plane.c2p(x_range[1], 0), RIGHT, buff=0.08),
            MathTex(r"j\omega", font_size=size + 6).next_to(self.plane.c2p(0, y_range[1]), UP, buff=0.06),
        )
        self.add(self.labels)
        if numbers:
            nums = VGroup()
            for x in np.arange(x_range[0], x_range[1] + 1e-9, x_range[2]):
                if abs(x) > 1e-9 and x_range[0] < x < x_range[1]:
                    nums.add(MathTex(_fmt(round(x, 3)), font_size=size, color=GREY_A).next_to(self.plane.c2p(x, 0), DOWN, buff=0.05))
            self.add(nums)
        self.bg = BackgroundRectangle(self, fill_color=PANEL_BG, fill_opacity=0.85, buff=0.12)
        self.bg.hud_layer = -1
        self.add_to_back(self.bg)

    def c2p(self, x, y=0):
        return self.plane.c2p(x, y)

    def s2p(self, s):
        s = complex(s)
        return self.plane.c2p(s.real, s.imag)

    def region(self, left=None, right=None, color=ROC_COLOR, opacity=0.4, edges=True):
        l = self.x_min if left is None else max(left, self.x_min)
        r = self.x_max if right is None else min(right, self.x_max)
        g = VGroup()
        if r > l:
            g.add(Polygon(self.c2p(l, self.y_min), self.c2p(r, self.y_min), self.c2p(r, self.y_max), self.c2p(l, self.y_max),
                          stroke_width=0, fill_color=color, fill_opacity=opacity))
        if edges:
            for e in (left, right):
                if e is not None and self.x_min < e < self.x_max:
                    g.add(DashedLine(self.c2p(e, self.y_min), self.c2p(e, self.y_max), color=color, stroke_width=2.5, dash_length=0.08))
        return g

    def pole(self, s, size=0.09, color=POLE_COLOR, width=4):
        p = self.s2p(s)
        return VGroup(Line(p + size * (UP + LEFT), p + size * (DOWN + RIGHT)),
                      Line(p + size * (UP + RIGHT), p + size * (DOWN + LEFT))).set_stroke(color, width)

    def zero(self, s, radius=0.08, color=ZERO_COLOR, width=3.5):
        return Circle(radius=radius, color=color, stroke_width=width).move_to(self.s2p(s))

    def vline(self, sigma, color=YELLOW, width=4):
        return Line(self.c2p(sigma, self.y_min), self.c2p(sigma, self.y_max), color=color, stroke_width=width)


def mini_axes(x_range=(-3, 5, 1), y_range=(-1.5, 1.5, 1), width=4.0, height=2.0, x_label="t", y_label=None, size=26):
    """Small flat time-axes for overlays (tag with scene.hud)."""
    ax = Axes(x_range=list(x_range), y_range=list(y_range), x_length=width, y_length=height,
              axis_config={"stroke_color": GREY_B, "stroke_width": 2, "tick_size": 0.04, "tip_width": 0.14, "tip_height": 0.14})
    labs = VGroup()
    if x_label:
        labs.add(MathTex(x_label, font_size=size).next_to(ax.x_axis.get_end(), RIGHT, buff=0.08))
    if y_label:
        labs.add(MathTex(y_label, font_size=size).next_to(ax.y_axis.get_end(), UP, buff=0.06))
    ax.add(labs)
    return ax


def graph2d(ax, f, x0, x1, n=300, color=SIG, width=4, breaks=()):
    """Graph on flat Axes, clipped to the axes' y-range, no vertical jump segments."""
    ymin, ymax = ax.y_range[:2]
    edges = [x0] + [b for b in breaks if x0 < b < x1] + [x1]
    g = VGroup()
    for a, b in zip(edges[:-1], edges[1:]):
        xs = np.linspace(a + (1e-6 if a != x0 else 0), b - (1e-6 if b != x1 else 0), max(int(n * (b - a) / (x1 - x0)), 4))
        with np.errstate(all="ignore"):
            ys = np.asarray(f(xs), dtype=float) * np.ones_like(xs)
        mask = np.isfinite(ys) & (ys >= ymin) & (ys <= ymax)
        for run in true_runs(mask):
            yr = np.clip(np.nan_to_num(ys[run], nan=0.0, posinf=ymax, neginf=ymin), ymin, ymax)
            g.add(polyline(pts(ax, xs[run], yr), color, width))
    return g


def u(t):
    """Unit step, numpy-friendly."""
    return (np.asarray(t) >= 0).astype(float)
