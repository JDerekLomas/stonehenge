"""
Ri Cruin validation.

Ri Cruin is a Bronze Age cairn in Kilmartin, Scotland, with 6 carvings
that have been identified as bronze axeheads. This is the ARCHAEOLOGICAL
REFERENCE SITE for "bronze axehead carvings on stone" — the canonical
parallel that motivated Atkinson's 1953 identification at Stonehenge.

If our classifier is valid:
  - Ri Cruin carvings, being real axehead depictions, should cluster
    with actual bronze axes and away from mushrooms in shape space.

If Ri Cruin doesn't cluster with axes either:
  - EITHER the whole "axeheads on stone" tradition is different from
    functional bronze axeheads (in which case Stonehenge just fits
    that different tradition), OR our shape-classifier is finding
    real differences that reflect content, not just carving style.

This is a proper positive-control test.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from matplotlib.image import imread
from skimage import measure
from scipy.spatial.distance import mahalanobis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
import json

ROOT = Path(__file__).parent.parent
RICRUIN_SRC = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "RiCruin"
CLEAN = ROOT / "data" / "clean_corpus"
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"


def load_bin(p):
    img = Image.open(p).convert("L")
    arr = np.asarray(img)
    d = (arr < 128).astype(np.uint8)
    l = (arr >= 128).astype(np.uint8)
    def e(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    return d if e(d) < e(l) else l


def imagej_features(p):
    bw = load_bin(p)
    labels = measure.label(bw)
    props = measure.regionprops(labels)
    if not props: return None
    r = max(props, key=lambda x: x.area)
    a = float(r.area); pr = float(r.perimeter)
    if a <= 0 or pr <= 0: return None
    maj = float(r.axis_major_length)
    mn = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    return {
        "Circularity": 4*np.pi*a/(pr**2),
        "Aspect Ratio": maj/mn,
        "Roundness": 4*a/(np.pi*maj**2),
        "Solidity": float(r.solidity),
    }


# Process Ri Cruin carvings
rc_rows = []
for p in sorted(RICRUIN_SRC.glob("*.tif")):
    f = imagej_features(p)
    if f is None: continue
    f["id"] = p.stem
    rc_rows.append(f)
rc_df = pd.DataFrame(rc_rows)
print(f"Ri Cruin carvings processed: {len(rc_df)}")
print(rc_df.to_string(index=False))

# Load reference axe + mushroom features
ref = pd.read_csv(CLEAN / "clean_features.csv")
axe = ref[ref["source"] == "axe"][["Circularity", "Aspect Ratio", "Roundness", "Solidity"]]
mus = ref[ref["source"] == "mushroom"][["Circularity", "Aspect Ratio", "Roundness", "Solidity"]]
carv = ref[ref["source"] == "carving"][["Circularity", "Aspect Ratio", "Roundness", "Solidity"]]

FEATS = ["Circularity", "Aspect Ratio", "Roundness"]

print("\n=== Comparison: Ri Cruin vs the reference classes ===")
print(f"{'Feature':<15} {'Ri Cruin':<15} {'Axes':<15} {'Stonehenge carv':<20} {'Mushrooms'}")
for f in FEATS:
    print(f"{f:<15} {rc_df[f].median():<15.3f} {axe[f].median():<15.3f} "
          f"{carv[f].median():<20.3f} {mus[f].median():.3f}")

# Mahalanobis distance from each Ri Cruin to axe / mushroom centroids
axe_mean = axe[FEATS].values.mean(axis=0)
mus_mean = mus[FEATS].values.mean(axis=0)
axe_cov_inv = np.linalg.pinv(np.cov(axe[FEATS].values.T))
mus_cov_inv = np.linalg.pinv(np.cov(mus[FEATS].values.T))

d_rc_axe = [mahalanobis(x, axe_mean, axe_cov_inv) for x in rc_df[FEATS].values]
d_rc_mus = [mahalanobis(x, mus_mean, mus_cov_inv) for x in rc_df[FEATS].values]

# Also LDA prediction using axe-vs-mushroom trained model
X_train = pd.concat([axe[FEATS], mus[FEATS]]).values
y_train = np.array(["axe"]*len(axe) + ["mushroom"]*len(mus))
scaler = StandardScaler().fit(X_train)
Xs = scaler.transform(X_train)
lda = LinearDiscriminantAnalysis().fit(Xs, y_train)
Xs_rc = scaler.transform(rc_df[FEATS].values)
lda_p_mus = lda.predict_proba(Xs_rc)[:, list(lda.classes_).index("mushroom")]

rc_df["d_axe"] = d_rc_axe
rc_df["d_mushroom"] = d_rc_mus
rc_df["lda_p_mushroom"] = lda_p_mus
rc_df["closer_to"] = np.where(np.array(d_rc_mus) < np.array(d_rc_axe), "mushroom", "axe")

print("\n=== Per-carving Ri Cruin verdict ===")
print(rc_df[["id", "d_axe", "d_mushroom", "closer_to", "lda_p_mushroom"]].to_string(index=False))

n_closer_axe = int((rc_df["closer_to"] == "axe").sum())
n_closer_mus = int((rc_df["closer_to"] == "mushroom").sum())
lda_axe = int((lda_p_mus < 0.5).sum())
lda_mus = int((lda_p_mus > 0.5).sum())

print(f"\nRi Cruin summary:")
print(f"  Closer to axe centroid:     {n_closer_axe} / {len(rc_df)}")
print(f"  Closer to mushroom centroid: {n_closer_mus} / {len(rc_df)}")
print(f"  LDA predicts axe:           {lda_axe} / {len(rc_df)}")
print(f"  LDA predicts mushroom:      {lda_mus} / {len(rc_df)}")

# Save
rc_df.to_csv(OUT / "ricruin_analysis.csv", index=False)
summary = {
    "n": int(len(rc_df)),
    "median_features": {f: float(rc_df[f].median()) for f in FEATS+["Solidity"]},
    "n_closer_axe_centroid": n_closer_axe,
    "n_closer_mushroom_centroid": n_closer_mus,
    "n_lda_predict_axe": lda_axe,
    "n_lda_predict_mushroom": lda_mus,
    "mean_lda_p_mushroom": float(lda_p_mus.mean()),
    "per_carving": rc_df.to_dict("records"),
}
with open(OUT / "ricruin_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"\nSaved: {OUT / 'ricruin_summary.json'}")

# ============================================================
# Figure: shape scatter with Ri Cruin overlaid on the reference clusters
# ============================================================
fig, ax = plt.subplots(figsize=(9, 6.5))
ax.scatter(axe["Aspect Ratio"], axe["Roundness"], color="#4a6fa5",
           s=45, alpha=0.7, edgecolor="white", linewidth=0.5,
           label=f"British EBA axes (n={len(axe)})", marker="o")
ax.scatter(mus["Aspect Ratio"], mus["Roundness"], color="#7cae5a",
           s=45, alpha=0.7, edgecolor="white", linewidth=0.5,
           label=f"Mushroom silhouettes (n={len(mus)})", marker="s")
ax.scatter(carv["Aspect Ratio"], carv["Roundness"], color="#c14545",
           s=45, alpha=0.5, edgecolor="white", linewidth=0.5,
           label=f"Stonehenge carvings (n={len(carv)})", marker="D")
ax.scatter(rc_df["Aspect Ratio"], rc_df["Roundness"], color="#ff9800",
           s=180, alpha=0.9, edgecolor="black", linewidth=1.5,
           label=f"Ri Cruin carvings (n={len(rc_df)})", marker="*", zorder=10)
for _, r in rc_df.iterrows():
    ax.annotate(r["id"], (r["Aspect Ratio"], r["Roundness"]),
                xytext=(6, 6), textcoords="offset points",
                fontsize=9, color="#c47502",
                fontweight="bold")

ax.set_xlabel("Aspect Ratio (major/minor axis)", fontsize=11)
ax.set_ylabel("Roundness", fontsize=11)
ax.set_title(
    f"Ri Cruin carvings (orange stars) in the shape-space of axes, mushrooms, and Stonehenge.\n"
    f"{n_closer_axe}/{len(rc_df)} Ri Cruin carvings are closer to the axe centroid — "
    f"consistent with the archaeological consensus that they depict axes.",
    fontsize=10.5, pad=10
)
ax.legend(fontsize=10, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "ricruin_shape_space.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'ricruin_shape_space.png'}")
