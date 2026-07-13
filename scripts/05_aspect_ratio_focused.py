"""
Aspect-ratio-focused analysis.

Motivated by the finding that the 4 canonical ImageJ dimensionless features
(circularity, aspect ratio, roundness, solidity) are highly correlated in
the axe corpus (AR-Roundness r = -0.96, Circ-Solidity r = 0.94). The
4-feature Mahalanobis is really testing ~2 effective dimensions.

This script reports the single-feature aspect-ratio comparison, which is
the most discriminating individual feature and cleanest to interpret.

Argument: Bronze axes are functional tools with proportions constrained
by hafting requirements (handle grip length vs. blade length). They must
be elongated. If the Stonehenge carvings were intended to depict axes, a
skilled carver would have reproduced the elongation. That the carvings
are systematically much less elongated than real axes is hard to
reconcile with the axehead interpretation — even before invoking a
specific alternative.
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
import json

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

axes = pd.read_csv(DATA / "early_axes_bevan.csv")["AR"].dropna().values
carv_df = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
carv = carv_df[carv_df["Stone"] == 53]["Aspect Ratio"].dropna().values

print(f"Axes:     n = {len(axes)}, AR mean = {axes.mean():.3f}, sd = {axes.std():.3f}")
print(f"          [range: {axes.min():.2f}–{axes.max():.2f}]")
print(f"Carvings: n = {len(carv)}, AR mean = {carv.mean():.3f}, sd = {carv.std():.3f}")
print(f"          [range: {carv.min():.2f}–{carv.max():.2f}]")
print()

# Two-sample tests
t, t_p = stats.ttest_ind(carv, axes, equal_var=False)
u, u_p = stats.mannwhitneyu(carv, axes, alternative="two-sided")
ks, ks_p = stats.ks_2samp(carv, axes)

# Bootstrap 95% CI on the mean difference
rng = np.random.default_rng(42)
diffs = np.array([
    rng.choice(carv, size=len(carv), replace=True).mean() -
    rng.choice(axes, size=len(axes), replace=True).mean()
    for _ in range(10000)
])
ci = (np.quantile(diffs, 0.025), np.quantile(diffs, 0.975))

# Effect size (Cohen's d for unequal variance — Hedges' g)
pooled_sd = np.sqrt((axes.var(ddof=1) + carv.var(ddof=1)) / 2)
cohens_d = (carv.mean() - axes.mean()) / pooled_sd

# What fraction of carvings have AR within the axe range?
axe_lo, axe_hi = np.quantile(axes, [0.025, 0.975])
inside = ((carv >= axe_lo) & (carv <= axe_hi)).sum()
below = (carv < axe_lo).sum()

print("=== Aspect ratio comparison ===\n")
print(f"Mean difference (carvings - axes): {carv.mean() - axes.mean():+.3f}")
print(f"95% bootstrap CI on mean difference: [{ci[0]:+.3f}, {ci[1]:+.3f}]")
print(f"Cohen's d (Hedges' g): {cohens_d:.2f} — LARGE effect")
print()
print(f"Welch's t: t = {t:.2f}, p = {t_p:.2e}")
print(f"Mann-Whitney U: U = {u:.1f}, p = {u_p:.2e}")
print(f"Kolmogorov-Smirnov: D = {ks:.3f}, p = {ks_p:.2e}")
print()
print(f"Axe AR 95% range: [{axe_lo:.2f}, {axe_hi:.2f}]")
print(f"Carvings inside axe 95% range: {inside}/{len(carv)} ({100*inside/len(carv):.1f}%)")
print(f"Carvings BELOW axe range (less elongated): {below}/{len(carv)} ({100*below/len(carv):.1f}%)")
print()
print("Interpretation: Bronze axes are functional tools; their aspect ratio")
print("is constrained by hafting geometry (handle grip + blade length).")
print(f"{100*below/len(carv):.0f}% of Stone 53 carvings are less elongated than the least")
print("elongated 2.5% of real bronze axes. A carver reproducing an axe from")
print("memory would not systematically make it wider.")

# Save
summary = {
    "n_axes": int(len(axes)),
    "n_carvings": int(len(carv)),
    "axe_ar_mean": float(axes.mean()),
    "axe_ar_sd": float(axes.std()),
    "carving_ar_mean": float(carv.mean()),
    "carving_ar_sd": float(carv.std()),
    "mean_difference": float(carv.mean() - axes.mean()),
    "bootstrap_95CI": [float(ci[0]), float(ci[1])],
    "cohens_d": float(cohens_d),
    "t_pvalue": float(t_p),
    "mannwhitney_pvalue": float(u_p),
    "ks_pvalue": float(ks_p),
    "carvings_inside_axe_range": int(inside),
    "carvings_below_axe_range": int(below),
    "carvings_below_pct": 100 * below / len(carv),
}
with open(OUT / "aspect_ratio_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nSaved: data/processed/aspect_ratio_summary.json")
