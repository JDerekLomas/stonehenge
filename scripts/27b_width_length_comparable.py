"""
Comparable width/height ratio: use bounding-box measurements from actual
silhouettes for all three classes, so we're comparing apples to apples.

  - Axes:      bounding-box Width/Height of the 41 Needham/Burgess silhouettes
  - Carvings:  bounding-box Width/Height of the 41 Stone 53 silhouettes
  - Mushrooms: bounding-box Width/Height of the 22 mushroom silhouettes

All from the SAME feature extraction pipeline. Comparable.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).parent.parent
CLEAN = ROOT / "data" / "clean_corpus"
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"

df = pd.read_csv(CLEAN / "clean_features.csv")
df["ratio"] = df["Width"] / df["Height"]

groups = {name: df[df["source"] == name]["ratio"].values
          for name in ["axe", "mushroom", "carving"]}

print("Bounding-box Width/Height ratio (comparable across all classes):\n")
for name, arr in groups.items():
    print(f"  {name:<10} n={len(arr):3d}   median = {np.median(arr):.3f}   "
          f"IQR = [{np.quantile(arr, .25):.3f}, {np.quantile(arr, .75):.3f}]")

print("\nMann-Whitney tests:")
u1, p1 = stats.mannwhitneyu(groups["carving"], groups["axe"],
                             alternative="two-sided")
print(f"  carvings vs axes:      U={u1:.0f}, p = {p1:.2e}")
u2, p2 = stats.mannwhitneyu(groups["carving"], groups["mushroom"],
                             alternative="two-sided")
print(f"  carvings vs mushrooms: U={u2:.0f}, p = {p2:.2e}")
u3, p3 = stats.mannwhitneyu(groups["axe"], groups["mushroom"],
                             alternative="two-sided")
print(f"  axes vs mushrooms:     U={u3:.0f}, p = {p3:.2e}")

# Figure
fig, ax = plt.subplots(figsize=(9, 5))
data = [groups["axe"], groups["carving"], groups["mushroom"]]
labels = [f"Axes\nn={len(groups['axe'])}",
          f"Carvings\nn={len(groups['carving'])}",
          f"Mushrooms\nn={len(groups['mushroom'])}"]
colors = ["#4a6fa5", "#c14545", "#7cae5a"]

parts = ax.violinplot(data, showmedians=True, widths=0.72)
for pc, c in zip(parts["bodies"], colors):
    pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.7)
for key in ("cbars", "cmins", "cmaxes", "cmedians"):
    if key in parts:
        parts[key].set_color("black"); parts[key].set_linewidth(1.0)

for i, d in enumerate(data):
    jitter = np.random.default_rng(i).normal(0, 0.06, size=len(d))
    ax.scatter(np.full(len(d), i+1) + jitter, d, s=14, alpha=0.55,
               color=colors[i], edgecolor="none")

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylabel("Bounding-box width / height ratio", fontsize=11.5)
med_axe = np.median(groups["axe"])
med_carv = np.median(groups["carving"])
med_mus = np.median(groups["mushroom"])
ax.set_title(
    f"Bounding-box aspect (comparable across all classes).\n"
    f"Axes {med_axe:.2f} · Carvings {med_carv:.2f} · Mushrooms {med_mus:.2f}. "
    f"Carvings and mushrooms overlap; axes are distinct.",
    fontsize=10.5, pad=8
)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)

# annotation of p-values
ax.text(0.02, 0.97,
        f"Mann-Whitney (two-sided):\n"
        f"  carvings vs axes: p = {p1:.1e}\n"
        f"  carvings vs mushrooms: p = {p2:.1e}\n"
        f"  axes vs mushrooms: p = {p3:.1e}",
        transform=ax.transAxes, va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor="gray", alpha=0.9),
        family="monospace")

plt.tight_layout()
plt.savefig(FIGS / "width_height_bbox_comparable.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'width_height_bbox_comparable.png'}")
