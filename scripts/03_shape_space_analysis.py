"""
Shape-space analysis: how far is each Stone 53 carving from the axe cluster
in the shape-feature space that both datasets share?

Shared ImageJ features between the Bevan axes and the Stone 53 carvings:
  - Area, Perimeter, Height, Width
  - Circularity (Circ.)
  - Aspect Ratio (AR)
  - Roundness (Round)
  - Solidity

Steps:
  1. Extract the shared features from both datasets.
  2. Standardize each feature (z-score using axe mean/sd — axes are the reference).
  3. Compute Mahalanobis distance from each carving to the axe centroid.
  4. Compare to the null distribution of intra-axe Mahalanobis distances.
  5. Report chi-squared p-value for each carving under the "is an axe" hypothesis.
  6. Report classification: how many carvings are within the 95% axe-cluster ellipsoid?
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import mahalanobis
from pathlib import Path
import json

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

SHARED_FEATURES_AXE = ["Area", "Perim.", "Height", "Width", "Circ.", "AR", "Round", "Solidity"]
SHARED_FEATURES_CARV = ["Area", "Perimeter", "Height", "Width", "Circularity", "Aspect Ratio", "Roundness", "Solidity"]
CANONICAL_NAMES = ["area", "perimeter", "height", "width", "circularity", "aspect_ratio", "roundness", "solidity"]


def load_axes():
    df = pd.read_csv(DATA / "early_axes_bevan.csv")
    x = df[SHARED_FEATURES_AXE].copy()
    x.columns = CANONICAL_NAMES
    return x.dropna().reset_index(drop=True)


def load_carvings():
    df = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
    df = df[df["Stone"] == 53].copy()
    x = df[SHARED_FEATURES_CARV].copy()
    x.columns = CANONICAL_NAMES
    x["carving_id"] = df["Carving#"].values
    return x.dropna().reset_index(drop=True)


def mahalanobis_distances(points, centroid, cov_inv):
    return np.array([mahalanobis(p, centroid, cov_inv) for p in points])


def main():
    axes = load_axes()
    carvings = load_carvings()
    carving_ids = carvings["carving_id"].values
    carvings_num = carvings.drop(columns=["carving_id"])

    print(f"Axes:     n={len(axes)}, features={CANONICAL_NAMES}")
    print(f"Carvings: n={len(carvings_num)} (Stone 53 only)")
    print()

    # --- Key modeling decision: the two datasets are in different UNIT SYSTEMS ---
    # Bevan axes:  Area in ~10,000s (pixels)                — silhouettes on a 400x500 canvas
    # Carvings:    Area in ~0.001-0.01 (proportion of image)  — normalized differently
    #
    # We CANNOT directly compare raw values. We compare the DIMENSIONLESS shape features
    # only (Circularity, AR, Roundness, Solidity), which are already normalized to size.
    #
    # This is a critical methodological point for the paper.

    dimensionless = ["circularity", "aspect_ratio", "roundness", "solidity"]

    axe_pts = axes[dimensionless].values
    carv_pts = carvings_num[dimensionless].values

    # Report descriptive stats
    print("=== Descriptive statistics (dimensionless shape features) ===\n")
    print(f"{'Feature':<15} {'Axe mean±sd':<20} {'Carving mean±sd':<20} {'Δ (carv - axe)':<15}")
    for i, feat in enumerate(dimensionless):
        a_mean, a_sd = axe_pts[:, i].mean(), axe_pts[:, i].std()
        c_mean, c_sd = carv_pts[:, i].mean(), carv_pts[:, i].std()
        delta = c_mean - a_mean
        print(f"{feat:<15} {a_mean:.3f} ± {a_sd:.3f}     {c_mean:.3f} ± {c_sd:.3f}     {delta:+.3f}")
    print()

    # Univariate t-tests with FDR correction
    print("=== Univariate comparisons (Welch's t + FDR) ===\n")
    from scipy.stats import false_discovery_control  # scipy >=1.11
    ps, ts = [], []
    for i, feat in enumerate(dimensionless):
        t, p = stats.ttest_ind(carv_pts[:, i], axe_pts[:, i], equal_var=False)
        ts.append(t); ps.append(p)
    fdr = false_discovery_control(ps)
    for feat, t, p, q in zip(dimensionless, ts, ps, fdr):
        star = "***" if q < 0.001 else ("**" if q < 0.01 else ("*" if q < 0.05 else ""))
        print(f"  {feat:<15} t = {t:+.2f}   p = {p:.4f}   q(FDR) = {q:.4f}  {star}")
    print()

    # Mahalanobis distance from each carving to the axe centroid
    axe_mean = axe_pts.mean(axis=0)
    axe_cov = np.cov(axe_pts.T)
    axe_cov_inv = np.linalg.pinv(axe_cov)

    d_axes = mahalanobis_distances(axe_pts, axe_mean, axe_cov_inv)
    d_carvings = mahalanobis_distances(carv_pts, axe_mean, axe_cov_inv)

    # Under multivariate normality, D² ~ chi²(k). k = 4 features here.
    k = len(dimensionless)
    thresh_95 = np.sqrt(stats.chi2.ppf(0.95, k))
    thresh_99 = np.sqrt(stats.chi2.ppf(0.99, k))

    print(f"=== Mahalanobis distance from axe centroid (k={k} dims) ===\n")
    print(f"Axes:      mean D = {d_axes.mean():.2f}, median = {np.median(d_axes):.2f}, "
          f"max = {d_axes.max():.2f}")
    print(f"Carvings:  mean D = {d_carvings.mean():.2f}, median = {np.median(d_carvings):.2f}, "
          f"max = {d_carvings.max():.2f}")
    print()
    print(f"95% axe-cluster threshold: D = {thresh_95:.2f}")
    print(f"99% axe-cluster threshold: D = {thresh_99:.2f}")
    print()

    n_inside_95 = int((d_carvings <= thresh_95).sum())
    n_inside_99 = int((d_carvings <= thresh_99).sum())
    n_carv = len(d_carvings)
    axe_inside_95 = int((d_axes <= thresh_95).sum())
    print(f"Axes  inside 95% ellipsoid:  {axe_inside_95}/{len(d_axes)}  "
          f"({100*axe_inside_95/len(d_axes):.1f}%)   [validates the model]")
    print(f"Carvings inside 95% ellipsoid: {n_inside_95}/{n_carv}  "
          f"({100*n_inside_95/n_carv:.1f}%)")
    print(f"Carvings inside 99% ellipsoid: {n_inside_99}/{n_carv}  "
          f"({100*n_inside_99/n_carv:.1f}%)")
    print()

    # Nonparametric: is the median Mahalanobis distance for carvings > axes?
    u, u_p = stats.mannwhitneyu(d_carvings, d_axes, alternative="greater")
    print(f"Mann-Whitney U (carvings > axes in Mahalanobis distance):")
    print(f"  U = {u:.1f}, p = {u_p:.2e}")
    print()

    # Save per-carving results
    per_carving = pd.DataFrame({
        "carving_id": carving_ids,
        "mahalanobis_dist": d_carvings,
        "chi2_p": [1 - stats.chi2.cdf(d**2, k) for d in d_carvings],
        "in_95_axe_ellipsoid": d_carvings <= thresh_95,
    })
    per_carving.to_csv(OUT / "carvings_axe_distance.csv", index=False)

    summary = {
        "n_axes": int(len(axes)),
        "n_carvings": int(n_carv),
        "features_used": dimensionless,
        "axe_centroid": axe_mean.tolist(),
        "axe_mean_mahal": float(d_axes.mean()),
        "carving_mean_mahal": float(d_carvings.mean()),
        "carvings_inside_95_pct": 100 * n_inside_95 / n_carv,
        "carvings_inside_99_pct": 100 * n_inside_99 / n_carv,
        "axes_inside_95_pct": 100 * axe_inside_95 / len(d_axes),
        "mann_whitney_U": float(u),
        "mann_whitney_p": float(u_p),
        "univariate_qFDR": {feat: float(q) for feat, q in zip(dimensionless, fdr)},
    }
    with open(OUT / "shape_space_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Saved: data/processed/carvings_axe_distance.csv")
    print("Saved: data/processed/shape_space_summary.json")


if __name__ == "__main__":
    main()
