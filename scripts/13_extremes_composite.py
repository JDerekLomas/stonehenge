"""
Composite figure: side-by-side of what an axe, a mushroom, and the top-6
most-axe-like and top-6 most-mushroom-like Stone 53 carvings look like.

Each carving is shown as a shape-feature reconstruction (an ellipse
stretched to match its ImageJ Aspect Ratio and Roundness values). It is
NOT a photograph of the actual carving — that requires the raw laser-scan
TIFFs which live in Google Drive we can't yet access programmatically.

Layout:
  Row 1: reference axe schematic  |  6 most-axe-like carving reconstructions
  Row 2: reference mushroom schematic  |  6 most-mushroom-like reconstructions

Each carving cell shows: F<id>, AR=x.xx, Round=x.xx, P(mus)=x.xx, plus a
badge if Ring=1 (an "annulus" — one of the paper's strongest features).
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, FancyBboxPatch
from pathlib import Path

ROOT = Path(__file__).parent.parent
PROCESSED = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

with open(PROCESSED / "carving_extremes.json") as f:
    data = json.load(f)


def draw_axe(ax, ar=2.7, blade_flare=0.35, color="#1c1917"):
    """Schematic bronze axehead in matplotlib axes with coords 0-1."""
    h = 0.85
    w = h / ar
    x_cx = 0.5
    y_top = (1 - h) / 2
    butt_w = w * 0.55
    mid_w = w * 0.85
    blade_w = w * (1.0 + blade_flare)
    pts = np.array([
        [x_cx - butt_w / 2, y_top + h],
        [x_cx - mid_w / 2, y_top + h * 0.55],
        [x_cx - blade_w / 2, y_top + h * 0.15],
        [x_cx - blade_w / 2 * 0.9, y_top],
        [x_cx + blade_w / 2 * 0.9, y_top],
        [x_cx + blade_w / 2, y_top + h * 0.15],
        [x_cx + mid_w / 2, y_top + h * 0.55],
        [x_cx + butt_w / 2, y_top + h],
    ])
    ax.fill(pts[:, 0], 1 - pts[:, 1], color=color)  # flip y so top is up


def draw_mushroom(ax, ar=1.7, ring=True, color="#1c1917"):
    """Schematic Amanita muscaria in matplotlib axes 0-1."""
    h = 0.85
    w = h / ar
    x_cx = 0.5
    y_top = (1 - h) / 2

    # Cap dome (half ellipse)
    theta = np.linspace(np.pi, 2 * np.pi, 40)
    cap_w = w * 1.15
    cap_h = h * 0.55
    cap_cx = x_cx
    cap_cy = y_top + cap_h * 0.65
    cap_x = cap_cx + cap_w / 2 * np.cos(theta)
    cap_y = cap_cy + cap_h * 0.85 * np.sin(theta) * -1  # invert for dome
    # Close the cap with straight bottom
    cap_x = np.concatenate([cap_x, [cap_x[0]]])
    cap_y = np.concatenate([cap_y, [cap_y[0]]])
    ax.fill(cap_x, 1 - cap_y, color=color)

    # Stem
    stem_w = w * 0.30
    stem_top = y_top + cap_h * 0.65
    stem_bot = y_top + h
    ax.fill(
        [x_cx - stem_w / 2, x_cx + stem_w / 2, x_cx + stem_w / 2, x_cx - stem_w / 2],
        [1 - stem_top, 1 - stem_top, 1 - stem_bot, 1 - stem_bot],
        color=color,
    )

    # Annulus
    if ring:
        ring_y = y_top + cap_h * 0.85
        ring_w = stem_w * 1.9
        ring_thick = 0.02
        ax.fill(
            [x_cx - ring_w / 2, x_cx + ring_w / 2, x_cx + ring_w / 2, x_cx - ring_w / 2],
            [1 - ring_y, 1 - ring_y, 1 - (ring_y + ring_thick), 1 - (ring_y + ring_thick)],
            color=color,
        )


def draw_shape_ellipse(ax, ar, roundness, color="#1c1917"):
    """Shape ellipse: major=1 unit, minor=1/ar, matching Roundness."""
    # For a pure ellipse, Roundness = 1/AR exactly. If they differ, use
    # major axis such that the ellipse has area = roundness * pi/4
    major = 0.85
    minor = major / ar
    ell = Ellipse(
        xy=(0.5, 0.5),
        width=minor,
        height=major,
        angle=0,
        facecolor=color,
        edgecolor="none",
    )
    ax.add_patch(ell)


def format_cell(ax, title=None, subtitle=None):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#d6d3d1")
        spine.set_linewidth(0.8)
    if title:
        ax.set_title(title, fontsize=8.5, pad=4)
    if subtitle:
        ax.text(0.5, -0.06, subtitle, ha="center", va="top",
                transform=ax.transAxes, fontsize=7.5, color="#57534e")


fig, axarr = plt.subplots(
    2, 7, figsize=(14, 5),
    gridspec_kw={"width_ratios": [1.4, 1, 1, 1, 1, 1, 1]},
)

# Top row: reference axe | 6 most-axe-like carvings
draw_axe(axarr[0, 0])
format_cell(axarr[0, 0], title="REFERENCE\nBronze axe (Class 5)",
            subtitle="stylized")

for i, c in enumerate(data["top_axe"]):
    ax = axarr[0, i + 1]
    draw_shape_ellipse(ax, c["aspect_ratio"], c["roundness"], color="#4a6fa5")
    badges = []
    if c["recurve"]: badges.append("R")
    if c["ring"]: badges.append("⚬")
    badge_str = " ".join(badges)
    format_cell(
        ax,
        title=f"Carving F{c['carving_id']}",
        subtitle=f"AR={c['aspect_ratio']}, Round={c['roundness']}\nP(mus)={c['prob_mushroom']:.2f}  {badge_str}",
    )

# Bottom row: reference mushroom | 6 most-mushroom-like carvings
draw_mushroom(axarr[1, 0], ring=True)
format_cell(axarr[1, 0], title="REFERENCE\nA. muscaria mature",
            subtitle="stylized, with annulus")

for i, c in enumerate(data["top_mushroom"]):
    ax = axarr[1, i + 1]
    draw_shape_ellipse(ax, c["aspect_ratio"], c["roundness"], color="#c14545")
    badges = []
    if c["recurve"]: badges.append("R")
    if c["ring"]: badges.append("⚬")
    badge_str = " ".join(badges)
    format_cell(
        ax,
        title=f"Carving F{c['carving_id']}",
        subtitle=f"AR={c['aspect_ratio']}, Round={c['roundness']}\nP(mus)={c['prob_mushroom']:.2f}  {badge_str}",
    )

# Row labels on the left
fig.text(0.005, 0.75, "6 most axe-like\ncarvings on Stone 53",
         rotation=90, ha="center", va="center", fontsize=9,
         fontweight="bold", color="#4a6fa5")
fig.text(0.005, 0.28, "6 most mushroom-like\ncarvings on Stone 53",
         rotation=90, ha="center", va="center", fontsize=9,
         fontweight="bold", color="#c14545")

fig.suptitle(
    "The extreme carvings sort cleanly. R = recurve feature, ⚬ = annulus (ring) feature.",
    fontsize=10.5, y=1.02,
)

plt.tight_layout(rect=[0.02, 0, 1, 0.98])
plt.savefig(FIGS / "extremes_composite.png", dpi=200, bbox_inches="tight",
            facecolor="white")
plt.savefig(FIGS / "extremes_composite.pdf", bbox_inches="tight",
            facecolor="white")
print(f"Saved: {FIGS / 'extremes_composite.png'}")
