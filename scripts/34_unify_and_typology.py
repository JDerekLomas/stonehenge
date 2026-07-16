"""
Two things:
  (A) Rerun every analysis that used a smaller subset on the full
      356-axe Bevan reference. Regenerates:
        - aspect-ratio summary (was n=124 axes, now n=356)
        - multivariate Mahalanobis (was n=124 axes, now n=356)
        - bounding-box W/H comparable (was n=41 axes, now n=356)
      Also regenerates the corresponding figures.
  (B) Per-Needham-class centroid analysis. Joins the 292-row Corpus
      sheet (which has BasicType = Class 2/3/4/5) with the 356-row
      All-data sheet (which has ImageJ features), computes per-class
      centroids, and asks: if a Stonehenge carving IS an axe, which
      Needham class would it be?
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from scipy.spatial.distance import mahalanobis, cdist

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

BEVAN = DATA / "Early Axes from Bevan.xlsx"
CARV = DATA / "Stone 53 Measurements.xlsx"

# =============================================================
# Load full labeled data
# =============================================================
allf = pd.read_excel(BEVAN, sheet_name="All data")
allf = allf[allf["Type"] == "Axe"]  # keep only real axes
axes = allf[["Label", "Area", "Perim.", "Width", "Height", "Circ.", "AR", "Round", "Solidity"]].dropna()
axes.columns = ["Label", "Area", "Perimeter", "Width", "Height",
                "Circularity", "Aspect Ratio", "Roundness", "Solidity"]
print(f"Full axe reference: n = {len(axes)}")

carv_source = pd.read_excel(CARV, sheet_name="Carvings")
carv = carv_source[["Carving#", "Circularity", "Aspect Ratio", "Roundness",
                    "Solidity", "Width", "Height"]].dropna(subset=["Circularity"])
print(f"Stone 53 carvings: n = {len(carv)}")

DIM3 = ["Circularity", "Aspect Ratio", "Roundness"]

# =============================================================
# (A) Rerun analyses with full 356
# =============================================================
print("\n=== (A) Unified analyses on full 356 axes ===\n")

# Aspect ratio
axe_ar = axes["Aspect Ratio"].values
carv_ar = carv["Aspect Ratio"].values
d, p_ks = stats.ks_2samp(carv_ar, axe_ar)
_, p_t = stats.ttest_ind(carv_ar, axe_ar, equal_var=False)
cd = (carv_ar.mean() - axe_ar.mean()) / np.sqrt(
    (axe_ar.var(ddof=1) + carv_ar.var(ddof=1)) / 2
)
axe_lo, axe_hi = np.quantile(axe_ar, [0.025, 0.975])
below = int((carv_ar < axe_lo).sum())
inside = int(((carv_ar >= axe_lo) & (carv_ar <= axe_hi)).sum())
print(f"Aspect ratio:")
print(f"  axes (n={len(axe_ar)}): median = {np.median(axe_ar):.2f}, IQR = "
      f"[{np.quantile(axe_ar, .25):.2f}, {np.quantile(axe_ar, .75):.2f}]")
print(f"  carvings (n={len(carv_ar)}): median = {np.median(carv_ar):.2f}, IQR = "
      f"[{np.quantile(carv_ar, .25):.2f}, {np.quantile(carv_ar, .75):.2f}]")
print(f"  Cohen's d = {cd:.2f}, KS D = {d:.3f} p = {p_ks:.2e}, t p = {p_t:.2e}")
print(f"  Axe 95% AR range: [{axe_lo:.2f}, {axe_hi:.2f}]")
print(f"  Carvings inside axe 95% range: {inside}/{len(carv_ar)} ({100*inside/len(carv_ar):.0f}%)")
print(f"  Carvings BELOW axe 95% range: {below}/{len(carv_ar)} ({100*below/len(carv_ar):.0f}%)")

ar_summary = {
    "n_axes": int(len(axe_ar)),
    "n_carvings": int(len(carv_ar)),
    "axe_ar_median": float(np.median(axe_ar)),
    "carv_ar_median": float(np.median(carv_ar)),
    "cohens_d": float(cd),
    "ks_p": float(p_ks),
    "welch_p": float(p_t),
    "carvings_below_pct": 100 * below / len(carv_ar),
}
with open(OUT / "aspect_ratio_summary_v2.json", "w") as f:
    json.dump(ar_summary, f, indent=2)

# Mahalanobis on 3D dimensionless
axe_X = axes[DIM3].values
carv_X = carv[DIM3].values
axe_mean = axe_X.mean(axis=0)
axe_cov_inv = np.linalg.pinv(np.cov(axe_X.T))
d_axes = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in axe_X])
d_carv = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in carv_X])
thresh_95 = np.sqrt(stats.chi2.ppf(0.95, 3))
axe_inside = (d_axes <= thresh_95).mean()
carv_inside = (d_carv <= thresh_95).mean()
u, p_u = stats.mannwhitneyu(d_carv, d_axes, alternative="greater")
print(f"\nMahalanobis (n={len(axe_X)} axes, {len(carv_X)} carvings, 3D):")
print(f"  Axes inside 95% ellipsoid: {100*axe_inside:.1f}%")
print(f"  Carvings inside 95% ellipsoid: {100*carv_inside:.1f}%")
print(f"  Mann-Whitney p = {p_u:.2e}")

mahal_summary = {
    "n_axes": int(len(axe_X)),
    "n_carvings": int(len(carv_X)),
    "features": DIM3,
    "axe_inside_95_pct": 100 * axe_inside,
    "carving_inside_95_pct": 100 * carv_inside,
    "mann_whitney_p": float(p_u),
}
with open(OUT / "shape_space_summary_v2.json", "w") as f:
    json.dump(mahal_summary, f, indent=2)

# Bounding-box W/H — need Width and Height on axes; the All data has them
axe_wh = axes["Width"] / axes["Height"]
carv_wh = carv["Width"] / carv["Height"]
mus = pd.read_csv(ROOT / "data" / "clean_corpus" / "clean_features.csv")
mus_wh = (mus[mus["source"] == "mushroom"]["Width"] /
          mus[mus["source"] == "mushroom"]["Height"]).values

_, p_ca = stats.mannwhitneyu(carv_wh, axe_wh, alternative="two-sided")
_, p_cm = stats.mannwhitneyu(carv_wh, mus_wh, alternative="two-sided")
_, p_am = stats.mannwhitneyu(axe_wh, mus_wh, alternative="two-sided")
print(f"\nBounding-box W/H (n={len(axe_wh)} axes, {len(carv_wh)} carvings, {len(mus_wh)} mushrooms):")
print(f"  Axes median: {axe_wh.median():.3f}")
print(f"  Carvings median: {carv_wh.median():.3f}")
print(f"  Mushrooms median: {np.median(mus_wh):.3f}")
print(f"  Carvings vs axes p = {p_ca:.2e}")
print(f"  Carvings vs mushrooms p = {p_cm:.2e}")
print(f"  Axes vs mushrooms p = {p_am:.2e}")

wh_summary = {
    "n_axes": int(len(axe_wh)),
    "n_carvings": int(len(carv_wh)),
    "n_mushrooms": int(len(mus_wh)),
    "axe_median": float(axe_wh.median()),
    "carving_median": float(carv_wh.median()),
    "mushroom_median": float(np.median(mus_wh)),
    "carvings_vs_axes_p": float(p_ca),
    "carvings_vs_mushrooms_p": float(p_cm),
    "axes_vs_mushrooms_p": float(p_am),
}
with open(OUT / "width_height_summary_v2.json", "w") as f:
    json.dump(wh_summary, f, indent=2)

# =============================================================
# Regenerate figures
# =============================================================
# Bounding-box W/H
fig, ax = plt.subplots(figsize=(9, 5))
data = [axe_wh.values, carv_wh.values, mus_wh]
labels = [f"Axes\nn={len(axe_wh)}", f"Carvings\nn={len(carv_wh)}",
          f"Mushrooms\nn={len(mus_wh)}"]
colors = ["#4a6fa5", "#c14545", "#7cae5a"]
parts = ax.violinplot(data, showmedians=True, widths=0.72)
for pc, c in zip(parts["bodies"], colors):
    pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.7)
for k in ("cbars", "cmins", "cmaxes", "cmedians"):
    if k in parts: parts[k].set_color("black"); parts[k].set_linewidth(1.0)
for i, d_ in enumerate(data):
    jitter = np.random.default_rng(i).normal(0, 0.06, size=len(d_))
    ax.scatter(np.full(len(d_), i+1) + jitter, d_, s=8, alpha=0.35,
               color=colors[i], edgecolor="none")
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylabel("Bounding-box width / height ratio", fontsize=11.5)
ax.set_title(
    f"Bounding-box aspect on the full Bevan corpus (n={len(axe_wh)} axes).\n"
    f"Axes {axe_wh.median():.2f} · Carvings {carv_wh.median():.2f} · "
    f"Mushrooms {np.median(mus_wh):.2f}.  Carvings and mushrooms overlap; axes are distinct.",
    fontsize=10.5, pad=8
)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
ax.text(0.02, 0.97,
        f"Mann-Whitney (two-sided):\n"
        f"  carvings vs axes: p = {p_ca:.1e}\n"
        f"  carvings vs mushrooms: p = {p_cm:.1e}\n"
        f"  axes vs mushrooms: p = {p_am:.1e}",
        transform=ax.transAxes, va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor="gray", alpha=0.9), family="monospace")
plt.tight_layout()
plt.savefig(FIGS / "width_height_bbox_v2.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'width_height_bbox_v2.png'}")

# Mahalanobis histogram
fig, ax = plt.subplots(figsize=(8, 4.5))
bins = np.linspace(0, max(d_carv.max(), d_axes.max()) + 1, 40)
ax.hist(d_axes, bins=bins, alpha=0.65, color="#4a6fa5",
        label=f"British EBA axes (n={len(d_axes)})", edgecolor="white")
ax.hist(d_carv, bins=bins, alpha=0.7, color="#c14545",
        label=f"Stone 53 carvings (n={len(d_carv)})", edgecolor="white")
ax.axvline(thresh_95, color="black", linestyle="--", linewidth=1.2,
           label=f"95% axe-cluster threshold (D = {thresh_95:.2f})")
ax.set_xlabel("Mahalanobis distance from British EBA axe centroid (3D)", fontsize=11)
ax.set_ylabel("Count", fontsize=11)
ax.set_title(f"Full Bevan reference (n={len(d_axes)}). "
             f"{100*carv_inside:.0f}% of carvings inside 95% axe ellipsoid; "
             f"Mann-Whitney p = {p_u:.1e}",
             fontsize=11, pad=8)
ax.legend(fontsize=9.5, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(FIGS / "mahalanobis_histogram_v2.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'mahalanobis_histogram_v2.png'}")

# =============================================================
# (B) Per-Needham-class centroid analysis
# =============================================================
print("\n=== (B) Per-Needham-class analysis ===\n")

# Load ea (7308-row metadata) for typology join
ea = pd.read_excel(BEVAN, sheet_name="ea")
print(f"ea sheet rows: {len(ea)}")

# All data "Label" is "1002.tif" — the number is the ArtefactID.
axes_j = axes.copy()
import re
def _id(label):
    m = re.match(r"(\d+)", str(label))
    return int(m.group(1)) if m else None
axes_j["ArtefactID"] = axes_j["Label"].apply(_id)
axes_j = axes_j.dropna(subset=["ArtefactID"])
axes_j["ArtefactID"] = axes_j["ArtefactID"].astype(int)

# Join
joined = pd.merge(
    axes_j,
    ea[["ArtefactID", "BasicType"]].dropna(subset=["BasicType"]),
    on="ArtefactID", how="inner"
)
print(f"Joined: {len(joined)} axes with both features and BasicType")
print(joined["BasicType"].value_counts())

# Compute per-class centroids
class_centroids = {}
for cls, sub in joined.groupby("BasicType"):
    if len(sub) < 3:
        continue
    class_centroids[cls] = sub[DIM3].values.mean(axis=0)
    print(f"  {cls} centroid: {class_centroids[cls]}")

# Also aggregate centroid across all axes and mushroom centroid
allmus = pd.read_csv(ROOT / "data" / "clean_corpus" / "clean_features.csv")
mus_all = allmus[allmus["source"] == "mushroom"][DIM3].values

class_names = list(class_centroids.keys()) + ["Mushroom (all)"]
centroids = np.array(list(class_centroids.values()) + [mus_all.mean(axis=0)])
print(f"\nClasses in play: {class_names}")

# Standardize and assign
from sklearn.preprocessing import StandardScaler
all_for_scale = np.vstack([joined[DIM3].values, mus_all, carv_X])
scaler = StandardScaler().fit(all_for_scale)
carv_s = scaler.transform(carv_X)
cent_s = scaler.transform(centroids)

# Nearest centroid per carving
dists = cdist(carv_s, cent_s)
assign = dists.argmin(axis=1)
counts = pd.Series([class_names[i] for i in assign]).value_counts()
print(f"\nCarving nearest-class assignments (n={len(carv_X)}):")
for k, v in counts.items():
    print(f"  {k}: {v}")

# Per-class summary
per_class_summary = {
    "n_carvings": int(len(carv_X)),
    "class_counts": counts.to_dict(),
    "class_centroids": {k: list(v) for k, v in zip(class_names, centroids.tolist())},
    "class_sizes": {cls: int(len(sub)) for cls, sub in joined.groupby("BasicType")},
}
with open(OUT / "per_class_centroid_summary.json", "w") as f:
    json.dump(per_class_summary, f, indent=2)
print(f"\nSaved: {OUT / 'per_class_centroid_summary.json'}")

# Figure
fig, ax = plt.subplots(figsize=(9, 5))
vals = [counts.get(n, 0) for n in class_names]
colors2 = ["#2c7fb8", "#41b6c4", "#a1dab4", "#fdae61", "#7cae5a"][:len(class_names)]
bars = ax.bar(range(len(class_names)), vals, color=colors2,
              edgecolor="white", linewidth=0.8)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 0.5, str(v),
            ha="center", fontsize=9.5)
ax.set_xticks(range(len(class_names)))
ax.set_xticklabels(class_names, rotation=15, ha="right", fontsize=10)
ax.set_ylabel(f"Carvings assigned (of {len(carv_X)}) to nearest centroid", fontsize=11)
mushroom_ct = counts.get("Mushroom (all)", 0)
ax.set_title(
    f"Per-class assignment: 4 Needham axe-class centroids + mushroom centroid.\n"
    f"{mushroom_ct}/{len(carv_X)} carvings ({100*mushroom_ct/len(carv_X):.0f}%) "
    f"assign to the mushroom centroid rather than any Needham axe class.",
    fontsize=10.5, pad=8
)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "per_needham_class_assignments.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'per_needham_class_assignments.png'}")
