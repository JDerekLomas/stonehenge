"""
Build a labeled Needham-style axe schematic showing all the measurements
and ratios used in the paper's analysis.

Definitions from the ImageJ Processing Instructions doc:
  L     total length
  LB    length of body
  WB    width of butt
  LC    length of chord across the sides
  LC'   length of chord to MO (maximum offset)
  WE    width of cutting edge
  W2    width at middle of body
  W3    width at 80% of the body
  DE    blade edge (curvature depth)
  MO    maximum offset (side curvature)

Derived ratios:
  RWB  = WB / WE      butt width / edge width
  RWB' = WB / L       butt / length
  RWE  = WE / L       edge / length
  RDE  = DE / WE      edge depth / edge width
  EH   = (W2-WB)/LB   expansion of haft end
  RW3  = W3 / LB      relative mid-blade width
  RMO  = MO / LC      relative max offset
  ASC  = LC'/LC       asymmetry of side curvature
  MRW  = (WB+W2+W3)/LB  mean relative width of body

Also standard ImageJ features:
  Area, Perimeter, Height, Width, Circularity, Aspect Ratio, Roundness, Solidity
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIGS = ROOT / "figures"

fig, ax = plt.subplots(figsize=(9, 10))

# Draw a schematic Class 5 flanged bronze axe silhouette
# All coordinates in an arbitrary unit — data coords 0-100
axe_pts = np.array([
    # start at butt (bottom middle), go clockwise
    [35, 5],   # bottom-left butt
    [30, 25],  # left side lower body
    [28, 45],  # left side mid body
    [24, 65],  # left side upper body
    [15, 85],  # left cutting-edge corner
    [10, 92],  # far left of curved cutting edge
    [50, 100], # top of blade curve (midpoint)
    [90, 92],  # far right of cutting edge
    [85, 85],  # right cutting-edge corner
    [76, 65],  # right side upper body
    [72, 45],  # right side mid body
    [70, 25],  # right side lower body
    [65, 5],   # bottom-right butt
])
ax.fill(axe_pts[:, 0], axe_pts[:, 1],
        color="#e5e0d5", edgecolor="#2c2c2c", linewidth=1.5, zorder=1)

# Measurement labels & lines
def hline(y, x0=8, x1=92, label=None, color="#b91c1c", lw=1.3):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw),
                zorder=5)
    if label:
        ax.text((x0+x1)/2, y, label, ha="center", va="center",
                fontsize=10, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="none"), zorder=6)

def vline(x, y0, y1, label=None, color="#b91c1c", lw=1.3):
    ax.annotate("", xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw),
                zorder=5)
    if label:
        ax.text(x, (y0+y1)/2, label, ha="center", va="center",
                fontsize=10, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="none"), zorder=6)

# L — total length (left side, tall arrow)
vline(-3, 5, 100, "L", color="#2c4a70")
# LB — length of body (bottom to blade-edge start)
vline(96, 5, 85, "LB", color="#2c4a70")
# WB — width of butt (bottom)
hline(3, 35, 65, "WB", color="#b91c1c")
# W2 — width at middle of body
hline(45, 28, 72, "W₂", color="#b91c1c")
# W3 — width at 80% of body
hline(69, 22, 78, "W₃", color="#b91c1c")
# WE — width of cutting edge (top of curve base)
hline(89, 10, 90, "WE", color="#b91c1c")
# DE — blade edge (curvature depth)
ax.annotate("", xy=(50, 88), xytext=(50, 100),
            arrowprops=dict(arrowstyle="<->", color="#7a4b0a", lw=1.3),
            zorder=5)
ax.text(53, 94, "DE", fontsize=10, color="#7a4b0a", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                  edgecolor="none"), zorder=6)
# LC — chord across the sides
ax.plot([15, 85], [85, 85], color="#0f5132", linestyle=":", linewidth=1.5,
        zorder=4)
ax.text(50, 82, "LC", ha="center", fontsize=10, color="#0f5132",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                  edgecolor="none"), zorder=6)

# Annotation panels
ax.set_xlim(-15, 110)
ax.set_ylim(-30, 115)
ax.set_aspect("equal")
ax.axis("off")

# Definitions table below
def_text = (
    "$\\bf{Linear\\ measurements\\ (from\\ ImageJ)}$\n"
    "L    — total length (butt to cutting-edge tip)\n"
    "LB   — length of body\n"
    "WB   — width of butt\n"
    "W₂   — width at middle of body\n"
    "W₃   — width at 80% of body\n"
    "WE   — width of cutting edge\n"
    "LC   — chord across the sides (blade base)\n"
    "LC'  — chord to MO (max offset)\n"
    "DE   — depth of cutting-edge curve\n"
    "MO   — maximum side-curvature offset\n\n"
    "$\\bf{Derived\\ ratios}$\n"
    "RWB   = WB / WE     butt-to-edge width ratio\n"
    "RWB'  = WB / L       relative butt width\n"
    "RWE   = WE / L       relative edge width\n"
    "RDE   = DE / WE     relative edge curvature\n"
    "EH    = (W₂−WB)/LB   haft-end expansion\n"
    "RW₃   = W₃ / LB      relative mid-blade width\n"
    "RMO   = MO / LC      relative max offset\n"
    "ASC   = LC' / LC     asymmetry of side curvature\n"
    "MRW   = (WB+W₂+W₃)/LB   mean relative body width\n\n"
    "$\\bf{Standard\\ ImageJ\\ dimensionless\\ features}$\n"
    "Circularity  = 4π·Area / Perimeter²\n"
    "Aspect Ratio = MajorAxis / MinorAxis (fitted ellipse)\n"
    "Roundness    = 4·Area / (π·MajorAxis²)\n"
    "Solidity     = Area / ConvexHullArea\n"
)
ax.text(-13, -3, def_text, fontsize=8.5, verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#f5f5f4",
                  edgecolor="#d6d3d1", linewidth=0.8))

ax.set_title("Axehead shape descriptors (Needham 1983 / paper's ImageJ pipeline)",
             fontsize=12, pad=10)

plt.tight_layout()
plt.savefig(FIGS / "measurement_definitions.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Wrote {FIGS / 'measurement_definitions.png'}")
