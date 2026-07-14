"""
Definitive analysis on the paper's full labeled corpus:
  - 356 Axes
  - 119 Carvings
  - 40 Mushrooms

All with matched ImageJ shape features. This supersedes the smaller
subsets used earlier.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path
from scipy import stats
from scipy.spatial.distance import mahalanobis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

# =========================================================
# Load
# =========================================================
xlsx = DATA / "Early Axes from Bevan.xlsx"
allf = pd.read_excel(xlsx, sheet_name="All data")

FEATS_XL = ["Circ.", "AR", "Round", "Solidity"]
FEATS = ["Circularity", "Aspect Ratio", "Roundness", "Solidity"]
DIMENSIONLESS3 = ["Circularity", "Aspect Ratio", "Roundness"]

allf = allf[["Type", "Label"] + FEATS_XL].dropna()
allf.columns = ["type", "id"] + FEATS
print(f"Full corpus with shape features: {len(allf)} rows")
print(allf["type"].value_counts())
print()

axes = allf[allf["type"] == "Axe"].reset_index(drop=True)
carvings = allf[allf["type"] == "Carving"].reset_index(drop=True)
mushrooms = allf[allf["type"] == "Mushroom"].reset_index(drop=True)

# =========================================================
# Descriptive stats
# =========================================================
print("=== Descriptive statistics (medians ± IQR) ===")
for name, df in [("Axes", axes), ("Carvings", carvings), ("Mushrooms", mushrooms)]:
    print(f"\n{name} (n = {len(df)}):")
    for f in FEATS:
        med = df[f].median()
        q1, q3 = df[f].quantile(0.25), df[f].quantile(0.75)
        print(f"  {f:<15}  median = {med:.3f}  IQR = [{q1:.3f}, {q3:.3f}]")

# =========================================================
# Two-class classifier: axe vs mushroom, then predict carvings
# =========================================================
print("\n=== Classifier: axe vs mushroom (all 3 features) ===")
X_train = pd.concat([axes[DIMENSIONLESS3], mushrooms[DIMENSIONLESS3]]).values
y_train = np.array(["axe"]*len(axes) + ["mushroom"]*len(mushrooms))
scaler = StandardScaler().fit(X_train)
Xs = scaler.transform(X_train)

for name, clf in [
    ("LDA", LinearDiscriminantAnalysis()),
    ("Random Forest", RandomForestClassifier(n_estimators=300, random_state=42)),
]:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(clf, Xs, y_train, cv=cv, scoring="accuracy")
    print(f"  {name}: CV acc = {scores.mean():.3f} ± {scores.std():.3f}")

# Predict carvings
Xs_carv = scaler.transform(carvings[DIMENSIONLESS3].values)
lda = LinearDiscriminantAnalysis().fit(Xs, y_train)
rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xs, y_train)
mus_idx_lda = list(lda.classes_).index("mushroom")
mus_idx_rf = list(rf.classes_).index("mushroom")
lda_p = lda.predict_proba(Xs_carv)[:, mus_idx_lda]
rf_p = rf.predict_proba(Xs_carv)[:, mus_idx_rf]

n_c = len(carvings)
print(f"\n=== Carving predictions (n = {n_c}) ===")
print(f"  LDA: {int((lda_p > 0.5).sum())} / {n_c} = {100*(lda_p>0.5).mean():.1f}% mushroom  "
      f"(mean P = {lda_p.mean():.3f})")
print(f"  RF:  {int((rf_p > 0.5).sum())} / {n_c} = {100*(rf_p>0.5).mean():.1f}% mushroom  "
      f"(mean P = {rf_p.mean():.3f})")

# Mahalanobis: closer to axe or mushroom centroid?
Xa = axes[DIMENSIONLESS3].values
Xm = mushrooms[DIMENSIONLESS3].values
Xc = carvings[DIMENSIONLESS3].values

axe_mean = Xa.mean(axis=0)
mus_mean = Xm.mean(axis=0)
axe_cov_inv = np.linalg.pinv(np.cov(Xa.T))
mus_cov_inv = np.linalg.pinv(np.cov(Xm.T))
d_axe = np.array([mahalanobis(p, axe_mean, axe_cov_inv) for p in Xc])
d_mus = np.array([mahalanobis(p, mus_mean, mus_cov_inv) for p in Xc])
closer_mus = int((d_mus < d_axe).sum())
print(f"\n  Mahalanobis: {closer_mus} / {n_c} = {100*closer_mus/n_c:.1f}% carvings"
      f" closer to mushroom centroid")

# Attach predictions
out = carvings.copy()
out["lda_p_mus"] = lda_p
out["rf_p_mus"] = rf_p
out["d_axe"] = d_axe
out["d_mus"] = d_mus
out["closer_to_mushroom"] = d_mus < d_axe
out.to_csv(OUT / "definitive_carving_predictions.csv", index=False)
print(f"\nSaved: {OUT / 'definitive_carving_predictions.csv'}")

# =========================================================
# Three-way violin figure
# =========================================================
fig, axarr = plt.subplots(1, 3, figsize=(13, 4.5))
COLS = {"axe": "#4a6fa5", "mushroom": "#7cae5a", "carving": "#c14545"}
for ax, feat in zip(axarr, DIMENSIONLESS3):
    data = [axes[feat].values, carvings[feat].values, mushrooms[feat].values]
    labels = [f"Axes\n(n={len(axes)})",
              f"Carvings\n(n={len(carvings)})",
              f"Mushrooms\n(n={len(mushrooms)})"]
    colors = [COLS["axe"], COLS["carving"], COLS["mushroom"]]
    parts = ax.violinplot(data, showmedians=True, widths=0.75)
    for pc, c in zip(parts["bodies"], colors):
        pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.7)
    for key in ("cbars", "cmins", "cmaxes", "cmedians"):
        if key in parts:
            parts[key].set_color("black"); parts[key].set_linewidth(1.0)
    for i, d in enumerate(data):
        jitter = np.random.default_rng(i).normal(0, 0.06, size=len(d))
        ax.scatter(np.full(len(d), i+1) + jitter, d, s=6, alpha=0.28,
                   color=colors[i], edgecolor="none")
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(feat, fontsize=11)
    ax.set_title(feat, fontsize=11, pad=6)
    for s in ax.spines.values():
        if s.spine_type in ("top", "right"): s.set_visible(False)
    ax.grid(axis="y", alpha=0.25)
fig.suptitle(
    f"Definitive shape comparison across the paper's full labeled corpus: "
    f"{len(axes)} axes, {len(carvings)} carvings, {len(mushrooms)} mushrooms",
    fontsize=11.5, y=1.02
)
plt.tight_layout()
plt.savefig(FIGS / "definitive_violin.png", dpi=200, bbox_inches="tight",
            facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'definitive_violin.png'}")

# =========================================================
# Definitive summary JSON
# =========================================================
summary = {
    "n_axes": int(len(axes)),
    "n_carvings": int(len(carvings)),
    "n_mushrooms": int(len(mushrooms)),
    "medians": {
        "axe": {f: float(axes[f].median()) for f in FEATS},
        "carving": {f: float(carvings[f].median()) for f in FEATS},
        "mushroom": {f: float(mushrooms[f].median()) for f in FEATS},
    },
    "carvings_closer_to_mushroom_mahal": closer_mus,
    "carvings_predicted_mushroom_lda": int((lda_p > 0.5).sum()),
    "carvings_predicted_mushroom_rf": int((rf_p > 0.5).sum()),
    "mean_p_mushroom_lda": float(lda_p.mean()),
    "mean_p_mushroom_rf": float(rf_p.mean()),
}
with open(OUT / "definitive_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"Saved: {OUT / 'definitive_summary.json'}")
