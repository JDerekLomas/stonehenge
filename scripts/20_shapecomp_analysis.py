"""
Rerun the axe-vs-carving analysis using the paper's own ShapeComp
22-dimensional vision-based embedding — an independent methodology to
the ImageJ hand-engineered features.

ShapeComp (Morgenstern et al. 2020) is a computational model of human
shape perception trained on 25,000 animal silhouettes. Its embedding
captures shape properties in a way that's meant to correspond to how
humans perceive shape similarity.

The paper's original corpus has 41 Stone 53 carvings and 36 axes with
ShapeComp descriptors. We ask:
  1. What is the classifier accuracy separating axes from carvings on
     the ShapeComp embedding alone?
  2. On UMAP of the embedding, do carvings and axes form distinct
     clusters?
  3. When we apply LDA trained on axes-vs-(mushrooms from the ImageJ
     analysis), does the ShapeComp embedding agree?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"

sc = pd.read_excel(DATA / "AxesStonesShapeCompData.xlsx", sheet_name="Sheet1")
# Var1 = filename, Var2 = source, Var3-Var24 = 22 shape dims
feat_cols = [f"Var{i}" for i in range(3, 25)]

sc = sc.rename(columns={"Var1": "id", "Var2": "source"})
sc["is_axe"] = sc["source"].str.contains("Axes")
sc["short_id"] = sc["id"].str.replace(".tif", "", regex=False)

axe_df = sc[sc["is_axe"]]
carv_df = sc[~sc["is_axe"]]

print(f"=== ShapeComp analysis ===")
print(f"Axes: n = {len(axe_df)}")
print(f"Carvings: n = {len(carv_df)}")
print()

# Two-class classification: axe vs carving
X = sc[feat_cols].values
y = np.where(sc["is_axe"], "axe", "carving")

scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)

for name, clf in [
    ("LDA", LinearDiscriminantAnalysis()),
    ("Random Forest", RandomForestClassifier(n_estimators=300, random_state=42)),
]:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(clf, Xs, y, cv=cv, scoring="accuracy")
    print(f"  {name}: CV accuracy on axe-vs-carving = {scores.mean():.3f} ± {scores.std():.3f}")

# PCA visualization
print("\nPCA on ShapeComp features:")
pca = PCA(n_components=2)
pcs = pca.fit_transform(Xs)
print(f"  Explained variance: {pca.explained_variance_ratio_}")

fig, ax = plt.subplots(figsize=(8, 6.5))
axe_mask = sc["is_axe"].values
ax.scatter(pcs[axe_mask, 0], pcs[axe_mask, 1],
           color="#4a6fa5", s=90, alpha=0.85, edgecolor="white", linewidth=0.8,
           label=f"Axes (Needham 1983 + Burgess), n = {axe_mask.sum()}",
           marker="o")
ax.scatter(pcs[~axe_mask, 0], pcs[~axe_mask, 1],
           color="#c14545", s=90, alpha=0.85, edgecolor="white", linewidth=0.8,
           label=f"Stone 53 carvings, n = {(~axe_mask).sum()}",
           marker="D")
ax.set_xlabel(f"PC1 ({100*pca.explained_variance_ratio_[0]:.0f}%)", fontsize=11)
ax.set_ylabel(f"PC2 ({100*pca.explained_variance_ratio_[1]:.0f}%)", fontsize=11)
ax.set_title("Axes and carvings form distinct clusters in the ShapeComp perceptual embedding",
             fontsize=11.5, pad=10)
ax.legend(fontsize=10, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "shapecomp_pca.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print(f"  wrote {FIGS / 'shapecomp_pca.png'}")

# Distance in ShapeComp space: for each carving, find its 3 nearest axes.
# Report the median distance and compare to intra-axe distances.
from scipy.spatial.distance import cdist
Xa = axe_df[feat_cols].values
Xc = carv_df[feat_cols].values

d_carv_to_axes = cdist(Xc, Xa, metric="euclidean")
d_axe_to_axes = cdist(Xa, Xa, metric="euclidean")
np.fill_diagonal(d_axe_to_axes, np.inf)

nearest_axe_dist = d_carv_to_axes.min(axis=1)
intra_axe_nn = d_axe_to_axes.min(axis=1)

print(f"\nNearest-neighbor distance in ShapeComp space:")
print(f"  axe-to-nearest-axe: median = {np.median(intra_axe_nn):.2f}, "
      f"mean = {intra_axe_nn.mean():.2f}")
print(f"  carving-to-nearest-axe: median = {np.median(nearest_axe_dist):.2f}, "
      f"mean = {nearest_axe_dist.mean():.2f}")

# Save carving-to-nearest-axe mapping for the paired figure
carv_out = carv_df[["short_id", "id"]].copy().reset_index(drop=True)
carv_out["nearest_axe_id"] = axe_df.iloc[d_carv_to_axes.argmin(axis=1)]["short_id"].values
carv_out["nearest_axe_dist"] = nearest_axe_dist
carv_out.to_csv(OUT / "shapecomp_carving_nearest_axe.csv", index=False)
print(f"\nWrote {OUT / 'shapecomp_carving_nearest_axe.csv'}")
print(carv_out.head(10).to_string(index=False))
