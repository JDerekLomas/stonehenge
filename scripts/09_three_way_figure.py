"""Figure: three-way distributions of the discriminating shape features."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

# Load
axes = pd.read_csv(DATA / "early_axes_bevan.csv")[["Circ.", "AR", "Round"]].dropna()
axes.columns = ["Circularity", "Aspect Ratio", "Roundness"]

carv = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
carv = carv[carv["Stone"] == 53][["Circularity", "Aspect Ratio", "Roundness"]].dropna()

mus = pd.read_csv(PROCESSED / "muscaria_shape_features.csv")[["Circularity", "Aspect Ratio", "Roundness"]]

AXE_COL = "#4a6fa5"
CARV_COL = "#c14545"
MUS_COL = "#7cae5a"

# ============================================================
# Figure 1: violin/box plots for each feature
# ============================================================
fig, axarr = plt.subplots(1, 3, figsize=(13, 4.5))
features = ["Circularity", "Aspect Ratio", "Roundness"]

for ax, feat in zip(axarr, features):
    data = [axes[feat].values, carv[feat].values, mus[feat].values]
    labels = [f"Axes\n(n={len(axes)})",
              f"Carvings\n(n={len(carv)})",
              f"A. muscaria\n(n={len(mus)})"]
    colors = [AXE_COL, CARV_COL, MUS_COL]

    parts = ax.violinplot(data, showmeans=False, showmedians=True, widths=0.7)
    for pc, c in zip(parts["bodies"], colors):
        pc.set_facecolor(c)
        pc.set_edgecolor("black")
        pc.set_alpha(0.65)
    for key in ("cbars", "cmins", "cmaxes", "cmedians"):
        if key in parts:
            parts[key].set_color("black")
            parts[key].set_linewidth(1.0)

    # Overlay individual points with slight jitter
    for i, d in enumerate(data):
        jitter = np.random.default_rng(i).normal(0, 0.05, size=len(d))
        ax.scatter(np.full(len(d), i + 1) + jitter, d,
                   s=8, alpha=0.35, color=colors[i], edgecolor="none")

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(feat, fontsize=11)
    ax.set_title(feat, fontsize=11, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25)

fig.suptitle("Stone 53 carvings match A. muscaria, not British EBA axes",
             fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig(FIGS / "three_way_violin.png", dpi=200, bbox_inches="tight")
plt.savefig(FIGS / "three_way_violin.pdf", bbox_inches="tight")
plt.close()

# ============================================================
# Figure 2: 2D scatter in AR / Roundness
# ============================================================
fig, ax = plt.subplots(figsize=(7.5, 6))
for df_, c, label, marker in [
    (axes, AXE_COL, f"British EBA axes (n={len(axes)})", "o"),
    (mus, MUS_COL, f"A. muscaria (n={len(mus)})", "s"),
    (carv, CARV_COL, f"Stone 53 carvings (n={len(carv)})", "D"),
]:
    ax.scatter(df_["Aspect Ratio"], df_["Roundness"], color=c,
               s=55, alpha=0.72, edgecolor="white", linewidth=0.6,
               marker=marker, label=label)

ax.set_xlabel("Aspect ratio (major / minor axis)", fontsize=11)
ax.set_ylabel("Roundness", fontsize=11)
ax.set_title("The Stone 53 carvings cluster with A. muscaria in shape space",
             fontsize=12, pad=10)
ax.legend(fontsize=10, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "three_way_scatter.png", dpi=200, bbox_inches="tight")
plt.savefig(FIGS / "three_way_scatter.pdf", bbox_inches="tight")
plt.close()

print("Saved: figures/three_way_violin.{png,pdf}")
print("Saved: figures/three_way_scatter.{png,pdf}")
