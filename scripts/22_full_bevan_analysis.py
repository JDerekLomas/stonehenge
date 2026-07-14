"""
Rerun analyses using the FULL Bevan corpus (515 axes with ImageJ features),
not the 124-axe subset we've been using. Also join with the 292-axe
Corpus sheet to attach Needham typology labels.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from scipy.spatial.distance import mahalanobis
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

# =========================================================
# 1. Load full Bevan "All data" — 515 axes with ImageJ features
# =========================================================
xlsx = DATA / "Early Axes from Bevan.xlsx"
bevan_all = pd.read_excel(xlsx, sheet_name="All data")
print(f"Full Bevan corpus (All data): {bevan_all.shape}")
print(f"Type counts: {bevan_all['Type'].value_counts().to_dict()}")

# Only rows with valid shape features
bevan = bevan_all[["Circ.", "AR", "Round", "Solidity"]].dropna()
bevan.columns = ["Circularity", "Aspect Ratio", "Roundness", "Solidity"]
print(f"With shape features: n = {len(bevan)}")
print(f"AR:  median={bevan['Aspect Ratio'].median():.2f}  IQR=[{bevan['Aspect Ratio'].quantile(0.25):.2f},"
      f" {bevan['Aspect Ratio'].quantile(0.75):.2f}]")
print(f"Round: median={bevan['Roundness'].median():.3f}")
print()

# =========================================================
# 2. Load the Corpus sheet: 292 axes with typology + flags
# =========================================================
corpus = pd.read_excel(xlsx, sheet_name="Corpus")
print(f"Curated Corpus: n = {len(corpus)}")
print(f"BasicType counts:")
print(corpus["BasicType"].value_counts().to_dict())
print()

# Recurve flag distribution
if "Recurve" in corpus.columns:
    total = corpus["Recurve"].notna().sum()
    yes = corpus["Recurve"].sum()
    print(f"Recurve: {int(yes)} / {int(total)} axes = {100*yes/total:.1f}%")

# =========================================================
# 3. Recompute the recurve chi-square with proper axe counts
# =========================================================
carv = pd.read_excel(DATA / "Stone 53 Measurements.xlsx", sheet_name="Carvings")
k_carv = int(carv["Recurve"].fillna(0).sum())
n_carv = int(len(carv))
print(f"\nStone 53 carvings: {k_carv}/{n_carv} recurved = {100*k_carv/n_carv:.1f}%")

# Also load Stone 4 counts from paper
k_s4, n_s4 = 24, 60

# Use full Corpus recurve count as axe reference
if "Recurve" in corpus.columns:
    axe_valid = corpus[corpus["Recurve"].notna()]
    k_axe = int(axe_valid["Recurve"].sum())
    n_axe = int(len(axe_valid))
else:
    k_axe, n_axe = 7, 105

print(f"Full corpus axes: {k_axe}/{n_axe} recurved = {100*k_axe/n_axe:.1f}%")

# Fisher exact and Cohen's h
def cohens_h(p1, p2):
    return 2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))

for name, k, n in [
    ("Stone 53", k_carv, n_carv),
    ("Stone 4",  k_s4,   n_s4),
    ("Combined", k_carv+k_s4, n_carv+n_s4),
]:
    p_c = k / n
    p_a = k_axe / n_axe
    or_, p = stats.fisher_exact([[k, n-k], [k_axe, n_axe-k_axe]], alternative="two-sided")
    h = cohens_h(p_c, p_a)
    print(f"  {name}: {k}/{n}={100*p_c:.1f}% vs axes {100*p_a:.1f}% | OR={or_:.2f} p={p:.2e} h={h:.2f}")

# =========================================================
# 4. Full-corpus Mahalanobis comparison
# =========================================================
carv_shape = carv[["Circularity", "Aspect Ratio", "Roundness", "Solidity"]].dropna()
print(f"\nMahalanobis analysis: {len(bevan)} axes vs {len(carv_shape)} Stone 53 carvings")

# Use dimensionless features only (3D: circ, AR, round)
axe_X = bevan[["Circularity", "Aspect Ratio", "Roundness"]].values
carv_X = carv_shape[["Circularity", "Aspect Ratio", "Roundness"]].values

axe_mean = axe_X.mean(axis=0)
axe_cov_inv = np.linalg.pinv(np.cov(axe_X.T))
d_carv = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in carv_X])
d_axe = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in axe_X])

# 95% chi-square threshold in 3D
thresh_95 = np.sqrt(stats.chi2.ppf(0.95, 3))
axe_inside = (d_axe <= thresh_95).mean()
carv_inside = (d_carv <= thresh_95).mean()
u, p_u = stats.mannwhitneyu(d_carv, d_axe, alternative="greater")

print(f"  Axes inside 95% axe ellipsoid: {100*axe_inside:.1f}% (validates model)")
print(f"  Carvings inside 95% axe ellipsoid: {100*carv_inside:.1f}%")
print(f"  Mann-Whitney U p-value: {p_u:.2e}")

# Save full-Bevan features + summary
bevan.to_csv(OUT / "bevan_full_shape.csv", index=False)
import json
summary = {
    "n_axes": int(len(bevan)),
    "n_carvings": int(len(carv_shape)),
    "axe_ar_median": float(bevan["Aspect Ratio"].median()),
    "axe_round_median": float(bevan["Roundness"].median()),
    "carv_ar_median": float(carv_shape["Aspect Ratio"].median()),
    "carv_round_median": float(carv_shape["Roundness"].median()),
    "carvings_inside_95_pct": 100 * carv_inside,
    "axes_inside_95_pct": 100 * axe_inside,
    "mann_whitney_p": float(p_u),
    "recurve": {
        "stone53_pct": 100*k_carv/n_carv,
        "stone4_pct": 100*k_s4/n_s4,
        "axes_full_corpus_pct": 100*k_axe/n_axe,
        "stone53_n": [int(k_carv), int(n_carv)],
        "stone4_n": [int(k_s4), int(n_s4)],
        "axes_full_n": [int(k_axe), int(n_axe)],
    },
}
with open(OUT / "full_bevan_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"\nSaved: {OUT / 'full_bevan_summary.json'}")
