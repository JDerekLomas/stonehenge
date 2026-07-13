"""
Recurve analysis: tightening the paper's strongest quantitative finding.

Original claim (paper):
  - Stone 53 carvings:   13 / 41 have recurve  (31.7%)
  - Stone 4 carvings:    24 / 60 have recurve  (40.0%)
  - British EBA axes:     7 / 105 have recurve  (7%)

Question: is the difference in recurve rate statistically meaningful, and how large is it?
This script does the tests the original paper skipped.
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
import json

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"
OUT.mkdir(exist_ok=True, parents=True)
FIGS.mkdir(exist_ok=True, parents=True)


def wilson_ci(k, n, alpha=0.05):
    """Wilson score interval for a binomial proportion. More reliable than
    normal-approximation, especially for small n or extreme p."""
    if n == 0:
        return (0.0, 0.0)
    z = stats.norm.ppf(1 - alpha / 2)
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    halfwidth = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, centre - halfwidth), min(1.0, centre + halfwidth))


def cohens_h(p1, p2):
    """Effect size for difference in two proportions (arcsine-transformed)."""
    phi1 = 2 * np.arcsin(np.sqrt(p1))
    phi2 = 2 * np.arcsin(np.sqrt(p2))
    return phi1 - phi2


def h_interp(h):
    a = abs(h)
    if a < 0.2:
        return "negligible"
    if a < 0.5:
        return "small"
    if a < 0.8:
        return "medium"
    return "large"


def analysis(name, k_carve, n_carve, k_axe, n_axe):
    """Run the full recurve analysis for a single carving set vs axe set."""
    p_c = k_carve / n_carve
    p_a = k_axe / n_axe
    ci_c = wilson_ci(k_carve, n_carve)
    ci_a = wilson_ci(k_axe, n_axe)

    table = np.array([[k_carve, n_carve - k_carve],
                      [k_axe, n_axe - k_axe]])
    # Fisher exact is more appropriate than chi-sq for small expected counts
    or_, fisher_p = stats.fisher_exact(table, alternative="two-sided")

    chi2, chi_p, dof, expected = stats.chi2_contingency(table)

    # Cohen's h effect size
    h = cohens_h(p_c, p_a)

    # Bayesian: uniform Beta(1,1) priors, sample from posterior
    rng = np.random.default_rng(42)
    post_c = rng.beta(k_carve + 1, n_carve - k_carve + 1, 20000)
    post_a = rng.beta(k_axe + 1, n_axe - k_axe + 1, 20000)
    diff = post_c - post_a
    p_c_gt_a = float((diff > 0).mean())
    diff_ci = (float(np.quantile(diff, 0.025)), float(np.quantile(diff, 0.975)))

    result = {
        "comparison": name,
        "carvings": {"k": int(k_carve), "n": int(n_carve),
                     "p": round(p_c, 4),
                     "ci95": [round(ci_c[0], 4), round(ci_c[1], 4)]},
        "axes": {"k": int(k_axe), "n": int(n_axe),
                 "p": round(p_a, 4),
                 "ci95": [round(ci_a[0], 4), round(ci_a[1], 4)]},
        "difference_pp": round((p_c - p_a) * 100, 2),
        "cohens_h": round(h, 3),
        "cohens_h_interp": h_interp(h),
        "odds_ratio": round(or_, 3),
        "fisher_p": float(fisher_p),
        "chi2": round(chi2, 3),
        "chi2_p": float(chi_p),
        "posterior_p_carvings_gt_axes": p_c_gt_a,
        "posterior_diff_95CI": [round(diff_ci[0], 4), round(diff_ci[1], 4)],
    }
    return result


def main():
    # --- Load local carvings sheet (Stone 53 only in current data) ---
    carv = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
    carv = carv[carv["Stone"] == 53].copy()
    carv["Recurve"] = carv["Recurve"].fillna(0).astype(int)
    k_s53 = int(carv["Recurve"].sum())
    n_s53 = int(len(carv))

    # --- Values from the original paper for the analyses we don't have local data for ---
    # Stone 4 counts and axe recurve counts are from the paper text.
    k_s4, n_s4 = 24, 60          # 40% recurve on Stone 4 (per paper)
    k_axe, n_axe = 7, 105        # 7% recurve in Needham's British EBA axes (per paper)

    results = [
        analysis("Stone 53 carvings vs British EBA axes",
                 k_s53, n_s53, k_axe, n_axe),
        analysis("Stone 4 carvings vs British EBA axes",
                 k_s4, n_s4, k_axe, n_axe),
        analysis("All Stonehenge carvings (S53 + S4) vs British EBA axes",
                 k_s53 + k_s4, n_s53 + n_s4, k_axe, n_axe),
    ]

    with open(OUT / "recurve_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== RECURVE ANALYSIS RESULTS ===\n")
    for r in results:
        c = r["carvings"]
        a = r["axes"]
        print(f"{r['comparison']}")
        print(f"  Carvings:  {c['k']}/{c['n']}  =  {c['p']*100:.1f}%  "
              f"(95% CI: {c['ci95'][0]*100:.1f}%–{c['ci95'][1]*100:.1f}%)")
        print(f"  Axes:      {a['k']}/{a['n']}  =  {a['p']*100:.1f}%  "
              f"(95% CI: {a['ci95'][0]*100:.1f}%–{a['ci95'][1]*100:.1f}%)")
        print(f"  Difference: {r['difference_pp']} percentage points")
        print(f"  Cohen's h:  {r['cohens_h']}  ({r['cohens_h_interp']})")
        print(f"  Odds ratio: {r['odds_ratio']}")
        print(f"  Fisher exact p:  {r['fisher_p']:.2e}")
        print(f"  Chi² = {r['chi2']}, p = {r['chi2_p']:.2e}")
        print(f"  Bayesian  P(recurve rate in carvings > axes) = "
              f"{r['posterior_p_carvings_gt_axes']:.4f}")
        print(f"  Posterior 95% CI on the difference: "
              f"{r['posterior_diff_95CI']}")
        print()


if __name__ == "__main__":
    main()
