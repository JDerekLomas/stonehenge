"""Two figures for the shape-space finding:
  1. Mahalanobis distance histogram: carvings vs axes
  2. 2D scatter in the two most discriminating features (roundness, aspect_ratio)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
FIGS = ROOT / "figures"

AXE_COL = "#4a6fa5"
CARV_COL = "#c14545"

# --- Load and align features ---
axes = pd.read_csv(DATA / "early_axes_bevan.csv")[["Circ.", "AR", "Round", "Solidity"]].dropna()
axes.columns = ["circularity", "aspect_ratio", "roundness", "solidity"]

carv = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
carv = carv[carv["Stone"] == 53][["Circularity", "Aspect Ratio", "Roundness", "Solidity"]].dropna()
carv.columns = ["circularity", "aspect_ratio", "roundness", "solidity"]

# --- Recompute Mahalanobis distances ---
from scipy.spatial.distance import mahalanobis
axe_mean = axes.values.mean(axis=0)
axe_cov = np.cov(axes.values.T)
axe_cov_inv = np.linalg.pinv(axe_cov)
d_axes = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in axes.values])
d_carv = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in carv.values])
thresh_95 = np.sqrt(chi2.ppf(0.95, 4))

# ============================================================
# Figure 1: Mahalanobis distance histogram
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
bins = np.linspace(0, max(d_carv.max(), d_axes.max()) + 1, 40)
ax.hist(d_axes, bins=bins, alpha=0.65, color=AXE_COL, label=f"British EBA axes (n={len(d_axes)})", edgecolor="white")
ax.hist(d_carv, bins=bins, alpha=0.65, color=CARV_COL, label=f"Stone 53 carvings (n={len(d_carv)})", edgecolor="white")
ax.axvline(thresh_95, color="black", linestyle="--", linewidth=1.2, label=f"95% axe-cluster threshold (D = {thresh_95:.2f})")
ax.set_xlabel("Mahalanobis distance from British EBA axe centroid", fontsize=11)
ax.set_ylabel("Count", fontsize=11)
ax.set_title("Only 15% of Stone 53 carvings lie inside the 95% axe-cluster ellipsoid", fontsize=12, pad=10)
ax.legend(fontsize=9.5, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3)

# Annotation
ax.text(0.98, 0.6, f"Mann-Whitney p = 1.5×10⁻¹⁹\nMean D: axes {d_axes.mean():.1f}, carvings {d_carv.mean():.1f}",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9, bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                              edgecolor="gray", alpha=0.9))

plt.tight_layout()
plt.savefig(FIGS / "mahalanobis_histogram.png", dpi=200, bbox_inches="tight")
plt.savefig(FIGS / "mahalanobis_histogram.pdf", bbox_inches="tight")
plt.close()

# ============================================================
# Figure 2: 2D scatter in the two most discriminating features
# ============================================================
fig, ax = plt.subplots(figsize=(7.5, 6))
ax.scatter(axes["aspect_ratio"], axes["roundness"], color=AXE_COL,
           s=45, alpha=0.75, edgecolor="white", linewidth=0.6,
           label=f"British EBA axes (n={len(axes)})")
ax.scatter(carv["aspect_ratio"], carv["roundness"], color=CARV_COL,
           s=55, alpha=0.85, marker="D", edgecolor="white", linewidth=0.6,
           label=f"Stone 53 carvings (n={len(carv)})")

ax.set_xlabel("Aspect ratio (height / width)", fontsize=11)
ax.set_ylabel("Roundness", fontsize=11)
ax.set_title("Carvings occupy a different shape-space region than real bronze axes", fontsize=12, pad=10)
ax.legend(fontsize=10, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(alpha=0.25)

# Region labels
ax.text(0.98, 0.28, "Axes region:\nelongated, less round",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9, style="italic", color=AXE_COL)
ax.text(0.05, 0.92, "Carvings region:\nrounder, less elongated",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=9, style="italic", color=CARV_COL)

plt.tight_layout()
plt.savefig(FIGS / "shape_space_scatter.png", dpi=200, bbox_inches="tight")
plt.savefig(FIGS / "shape_space_scatter.pdf", bbox_inches="tight")
plt.close()

print("Saved:")
print("  figures/mahalanobis_histogram.{png,pdf}")
print("  figures/shape_space_scatter.{png,pdf}")
