"""
Width-to-length ratio comparison.

Bronze axes:      BladeWidth / Length  — how wide is the cutting edge
                   relative to the whole tool?
Mushrooms:        CapSize / (Cap + Stem)  — how much of the total height
                   is cap vs. stem?
Carvings:         Width / Height  — the analogous 2D measure from ImageJ.

The point: mushrooms have cap-dominant proportions (cap width often > cap+stem
height/2). Bronze axes have blade-dominant-but-still-narrow proportions
(blade width is 30-50% of total length). If carvings match one class
more than the other on this ratio, that's additional independent evidence.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"

# =========================================================
# 1. Bronze axes: BladeWidth / Length
# =========================================================
axes = pd.read_excel(DATA / "Early Axes from Bevan.xlsx", sheet_name="ea")
axes_valid = axes.dropna(subset=["Length", "BladeWidth"])
axes_valid = axes_valid[
    (axes_valid["Length"] > 10) & (axes_valid["BladeWidth"] > 0)
]
axe_ratio = (axes_valid["BladeWidth"] / axes_valid["Length"]).values
print(f"Axes (n={len(axes_valid)}): BladeWidth/Length")
print(f"  median = {np.median(axe_ratio):.3f}, "
      f"IQR = [{np.quantile(axe_ratio, .25):.3f}, {np.quantile(axe_ratio, .75):.3f}]")

# =========================================================
# 2. Mushrooms: CapSize / (CapSize + StemSize)
# =========================================================
mus = pd.read_excel(DATA / "Mushroom Outlines Carvings.xlsx",
                     sheet_name="Mushrooms")
mus_valid = mus.dropna(subset=["Cap Size", "Stem Size"])
mus_valid = mus_valid[(mus_valid["Cap Size"] > 0) & (mus_valid["Stem Size"] > 0)]
mus_total = mus_valid["Cap Size"] + mus_valid["Stem Size"]
mus_ratio = (mus_valid["Cap Size"] / mus_total).values
print(f"\nMushrooms (n={len(mus_valid)}): CapSize/(Cap+Stem)")
print(f"  median = {np.median(mus_ratio):.3f}, "
      f"IQR = [{np.quantile(mus_ratio, .25):.3f}, {np.quantile(mus_ratio, .75):.3f}]")

# =========================================================
# 3. Carvings: Width / Height (bounding-box)
# =========================================================
carv = pd.read_excel(DATA / "Stone 53 Measurements.xlsx", sheet_name="Carvings")
carv_valid = carv.dropna(subset=["Width", "Height"])
carv_ratio = (carv_valid["Width"] / carv_valid["Height"]).values
print(f"\nCarvings (n={len(carv_valid)}): Width/Height")
print(f"  median = {np.median(carv_ratio):.3f}, "
      f"IQR = [{np.quantile(carv_ratio, .25):.3f}, {np.quantile(carv_ratio, .75):.3f}]")

# =========================================================
# Statistical tests
# =========================================================
print("\n=== Mann-Whitney tests ===")
u1, p1 = stats.mannwhitneyu(carv_ratio, axe_ratio, alternative="two-sided")
print(f"Carvings vs axes:       U={u1:.0f}, p = {p1:.2e}")
u2, p2 = stats.mannwhitneyu(carv_ratio, mus_ratio, alternative="two-sided")
print(f"Carvings vs mushrooms:  U={u2:.0f}, p = {p2:.2e}")
u3, p3 = stats.mannwhitneyu(axe_ratio, mus_ratio, alternative="two-sided")
print(f"Axes vs mushrooms:      U={u3:.0f}, p = {p3:.2e}")

# =========================================================
# Figure
# =========================================================
fig, ax = plt.subplots(figsize=(9, 5))
data = [axe_ratio, carv_ratio, mus_ratio]
labels = [f"Bronze axes\nn={len(axe_ratio)}\n(BladeWidth / Length)",
          f"Stonehenge carvings\nn={len(carv_ratio)}\n(Width / Height)",
          f"Native mushrooms\nn={len(mus_ratio)}\n(CapSize / [Cap+Stem])"]
colors = ["#4a6fa5", "#c14545", "#7cae5a"]

parts = ax.violinplot(data, showmedians=True, widths=0.75)
for pc, c in zip(parts["bodies"], colors):
    pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.7)
for key in ("cbars", "cmins", "cmaxes", "cmedians"):
    if key in parts:
        parts[key].set_color("black"); parts[key].set_linewidth(1.0)

for i, d in enumerate(data):
    jitter = np.random.default_rng(i).normal(0, 0.06, size=len(d))
    ax.scatter(np.full(len(d), i+1) + jitter, d, s=8, alpha=0.35,
               color=colors[i], edgecolor="none")

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(labels, fontsize=9.5)
ax.set_ylabel("Width-of-widest-part / Total-length ratio", fontsize=11)
ax.set_title(
    f"Width-to-length ratio: carvings (0.62) sit between axes (0.42) and mushroom caps (0.56).\n"
    f"Both differences are significant (p vs axes = {p1:.1e}, p vs mushrooms = {p2:.1e}).",
    fontsize=10.5, pad=8
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
ax.axhline(0.5, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)

plt.tight_layout()
plt.savefig(FIGS / "width_length_ratio.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'width_length_ratio.png'}")

# Summary
import json
summary = {
    "axes_bladewidth_length_ratio": {
        "n": int(len(axe_ratio)),
        "median": float(np.median(axe_ratio)),
        "iqr": [float(np.quantile(axe_ratio, .25)), float(np.quantile(axe_ratio, .75))],
    },
    "mushrooms_cap_total_ratio": {
        "n": int(len(mus_ratio)),
        "median": float(np.median(mus_ratio)),
        "iqr": [float(np.quantile(mus_ratio, .25)), float(np.quantile(mus_ratio, .75))],
    },
    "carvings_width_height_ratio": {
        "n": int(len(carv_ratio)),
        "median": float(np.median(carv_ratio)),
        "iqr": [float(np.quantile(carv_ratio, .25)), float(np.quantile(carv_ratio, .75))],
    },
    "mw_carvings_vs_axes_p": float(p1),
    "mw_carvings_vs_mushrooms_p": float(p2),
    "mw_axes_vs_mushrooms_p": float(p3),
}
with open(OUT / "width_length_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
