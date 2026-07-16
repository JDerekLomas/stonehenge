"""
Replication check. Rerun the definitive 3-way classifier on the
independently-extracted Stone 4 silhouettes (n=56) plus the Stone 53
carvings (n=41) — 97 total — and compare against:

  (a) The paper's own Bevan "All data" corpus (n=119 carvings), which
      served as the definitive analysis until now.
  (b) The 356 axes + 40 mushrooms reference sets (unchanged).

If our newly-extracted Stone 4 silhouettes give the same qualitative
verdict as the Bevan-derived carving corpus, that validates both
pipelines.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.spatial.distance import mahalanobis
from scipy import stats
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).parent.parent
BEVAN = ROOT / "data" / "raw" / "Early Axes from Bevan.xlsx"
S53_CSV = ROOT / "data" / "raw" / "Stone 53 Measurements.xlsx"
S4_CSV = ROOT / "data" / "stone4_extracted" / "stone4_features.csv"

FEATS = ["Circularity", "Aspect Ratio", "Roundness"]

# =============================================================
# Load
# =============================================================
allf = pd.read_excel(BEVAN, sheet_name="All data")
axes = allf[allf["Type"] == "Axe"][["Circ.", "AR", "Round"]].dropna()
axes.columns = FEATS
mushrooms = allf[allf["Type"] == "Mushroom"][["Circ.", "AR", "Round"]].dropna()
mushrooms.columns = FEATS
bevan_carvings = allf[allf["Type"] == "Carving"][["Circ.", "AR", "Round"]].dropna()
bevan_carvings.columns = FEATS

s53 = pd.read_excel(S53_CSV, sheet_name="Carvings")[
    ["Circularity", "Aspect Ratio", "Roundness"]].dropna()

s4 = pd.read_csv(S4_CSV)[FEATS]

combined = pd.concat([s53, s4], ignore_index=True)

print(f"Reference axes:          n = {len(axes)}")
print(f"Reference mushrooms:     n = {len(mushrooms)}")
print(f"Bevan carving corpus:    n = {len(bevan_carvings)}")
print(f"Independent extractions:")
print(f"  Stone 53 (Lomas 2021):  n = {len(s53)}")
print(f"  Stone 4 (this session):  n = {len(s4)}")
print(f"  Combined:              n = {len(combined)}")

# =============================================================
# Compare distributions: Bevan carvings vs my extraction
# =============================================================
print("\n=== Distribution comparison: Bevan vs independent extraction ===")
for feat in FEATS:
    b = bevan_carvings[feat].values
    c = combined[feat].values
    print(f"{feat:<15}  Bevan: median={np.median(b):.3f}  IQR "
          f"[{np.quantile(b, .25):.3f}, {np.quantile(b, .75):.3f}]   "
          f"Ours: median={np.median(c):.3f}  IQR "
          f"[{np.quantile(c, .25):.3f}, {np.quantile(c, .75):.3f}]")
    u, p = stats.mannwhitneyu(b, c, alternative="two-sided")
    print(f"                Mann-Whitney (two-sided) p = {p:.3f}")

# =============================================================
# Run classifier on our combined 97
# =============================================================
print("\n=== Classifier on independent 97-carving extraction ===")
X_train = pd.concat([axes, mushrooms]).values
y_train = np.array(["axe"]*len(axes) + ["mushroom"]*len(mushrooms))
scaler = StandardScaler().fit(X_train)
Xs = scaler.transform(X_train)

for name, clf in [("LDA", LinearDiscriminantAnalysis()),
                  ("RF", RandomForestClassifier(n_estimators=300, random_state=42))]:
    scores = cross_val_score(clf, Xs, y_train,
                              cv=StratifiedKFold(5, shuffle=True, random_state=42))
    print(f"  {name} CV on axe-vs-mushroom: {scores.mean():.3f} ± {scores.std():.3f}")

lda = LinearDiscriminantAnalysis().fit(Xs, y_train)
rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xs, y_train)

Xs_c = scaler.transform(combined.values)
lda_p = lda.predict_proba(Xs_c)[:, list(lda.classes_).index("mushroom")]
rf_p = rf.predict_proba(Xs_c)[:, list(rf.classes_).index("mushroom")]

print(f"\nAll 97 independent carvings:")
print(f"  LDA: {int((lda_p > 0.5).sum())}/{len(combined)} = "
      f"{100*(lda_p > 0.5).mean():.1f}% mushroom, mean P = {lda_p.mean():.3f}")
print(f"  RF:  {int((rf_p > 0.5).sum())}/{len(combined)} = "
      f"{100*(rf_p > 0.5).mean():.1f}% mushroom, mean P = {rf_p.mean():.3f}")

# Mahalanobis
axe_mean = axes.values.mean(axis=0)
mus_mean = mushrooms.values.mean(axis=0)
axe_cov_inv = np.linalg.pinv(np.cov(axes.values.T))
mus_cov_inv = np.linalg.pinv(np.cov(mushrooms.values.T))

d_axe = np.array([mahalanobis(x, axe_mean, axe_cov_inv) for x in combined.values])
d_mus = np.array([mahalanobis(x, mus_mean, mus_cov_inv) for x in combined.values])
closer_mus = int((d_mus < d_axe).sum())
print(f"  Mahalanobis: {closer_mus}/{len(combined)} = "
      f"{100*closer_mus/len(combined):.1f}% closer to mushroom centroid")

# Per-stone breakdown
for name, sub in [("Stone 53", s53), ("Stone 4", s4)]:
    Xs_s = scaler.transform(sub.values)
    lda_p_s = lda.predict_proba(Xs_s)[:, list(lda.classes_).index("mushroom")]
    rf_p_s = rf.predict_proba(Xs_s)[:, list(rf.classes_).index("mushroom")]
    d_a_s = np.array([mahalanobis(x, axe_mean, axe_cov_inv) for x in sub.values])
    d_m_s = np.array([mahalanobis(x, mus_mean, mus_cov_inv) for x in sub.values])
    print(f"\n{name} (n={len(sub)}):")
    print(f"  LDA:   {int((lda_p_s > 0.5).sum())}/{len(sub)} mushroom, mean P = {lda_p_s.mean():.3f}")
    print(f"  RF:    {int((rf_p_s > 0.5).sum())}/{len(sub)} mushroom, mean P = {rf_p_s.mean():.3f}")
    print(f"  Mahal: {int((d_m_s < d_a_s).sum())}/{len(sub)} closer to mushroom centroid")

# =============================================================
# Same on Bevan's own carvings for comparison
# =============================================================
print("\n=== Same classifier on Bevan's own 119 carving corpus (for comparison) ===")
Xs_b = scaler.transform(bevan_carvings.values)
lda_p_b = lda.predict_proba(Xs_b)[:, list(lda.classes_).index("mushroom")]
rf_p_b = rf.predict_proba(Xs_b)[:, list(rf.classes_).index("mushroom")]
d_a_b = np.array([mahalanobis(x, axe_mean, axe_cov_inv) for x in bevan_carvings.values])
d_m_b = np.array([mahalanobis(x, mus_mean, mus_cov_inv) for x in bevan_carvings.values])
print(f"  LDA:   {int((lda_p_b > 0.5).sum())}/{len(bevan_carvings)} mushroom, "
      f"mean P = {lda_p_b.mean():.3f}")
print(f"  RF:    {int((rf_p_b > 0.5).sum())}/{len(bevan_carvings)} mushroom, "
      f"mean P = {rf_p_b.mean():.3f}")
print(f"  Mahal: {int((d_m_b < d_a_b).sum())}/{len(bevan_carvings)} closer to mushroom centroid")
