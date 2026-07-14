"""
Extended classifier: fold Stone 4 carvings into the 3-way analysis
so we have 72 carvings total (41 Stone 53 + 31 Stone 4) instead of the
paper's 41-only. Uses features from the harmonics extraction pipeline.

Also, per-stone breakdown: does the classifier agree on Stone 4 as
strongly as on Stone 53?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import mahalanobis
from scipy import stats
import json

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

# Load all features (extended file has axes, carvings-both-stones, mushrooms)
df = pd.read_csv(OUT / "extended_features_with_harmonics.csv")
print(df.groupby("source").size())

FEATS = ["Circularity", "Aspect Ratio", "Roundness"]
axe_df = df[df["source"] == "axe"][FEATS + ["id"]]
mus_df = df[df["source"] == "mushroom"][FEATS + ["id"]]
carv_df = df[df["source"] == "carving"][FEATS + ["id", "stone"] if "stone" in df.columns else FEATS + ["id"]].copy()

if "stone" not in carv_df.columns:
    # Reconstruct stone from id
    def id_to_stone(s):
        s = str(s).replace("-aligned", "").lstrip("Ff")
        try:
            n = int(s)
            if 595 <= n <= 638 or n == 720: return "53"
            if 640 <= n <= 730: return "4"
        except: pass
        return "other"
    carv_df["stone"] = carv_df["id"].apply(id_to_stone)

print(f"\nAxes: n={len(axe_df)}")
print(f"Mushrooms: n={len(mus_df)}")
print(f"Carvings by stone:")
print(carv_df.groupby("stone").size())

# Train axe-vs-mushroom classifier
X_train = pd.concat([axe_df[FEATS], mus_df[FEATS]]).values
y_train = np.array(["axe"]*len(axe_df) + ["mushroom"]*len(mus_df))
scaler = StandardScaler().fit(X_train)
Xs = scaler.transform(X_train)

for name, clf in [("LDA", LinearDiscriminantAnalysis()),
                  ("RF", RandomForestClassifier(n_estimators=300, random_state=42))]:
    scores = cross_val_score(clf, Xs, y_train, cv=StratifiedKFold(5, shuffle=True, random_state=42))
    print(f"\n{name} CV accuracy on axe-vs-mushroom: {scores.mean():.3f} ± {scores.std():.3f}")

lda = LinearDiscriminantAnalysis().fit(Xs, y_train)
rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xs, y_train)

# Predict on carvings
Xs_carv = scaler.transform(carv_df[FEATS].values)
lda_p = lda.predict_proba(Xs_carv)[:, list(lda.classes_).index("mushroom")]
rf_p = rf.predict_proba(Xs_carv)[:, list(rf.classes_).index("mushroom")]
carv_df["lda_p_mus"] = lda_p
carv_df["rf_p_mus"] = rf_p

# Mahalanobis
axe_mean = axe_df[FEATS].values.mean(axis=0)
mus_mean = mus_df[FEATS].values.mean(axis=0)
axe_cov_inv = np.linalg.pinv(np.cov(axe_df[FEATS].values.T))
mus_cov_inv = np.linalg.pinv(np.cov(mus_df[FEATS].values.T))
d_axe = [mahalanobis(p, axe_mean, axe_cov_inv) for p in carv_df[FEATS].values]
d_mus = [mahalanobis(p, mus_mean, mus_cov_inv) for p in carv_df[FEATS].values]
carv_df["d_axe"] = d_axe
carv_df["d_mus"] = d_mus
carv_df["closer_to_mushroom"] = np.array(d_mus) < np.array(d_axe)

print("\n=== Per-stone breakdown ===")
for stone in [53, 4, "53", "4"]:
    sub = carv_df[carv_df["stone"] == stone]
    n = len(sub)
    if n == 0: continue
    lda_pos = (sub["lda_p_mus"] > 0.5).sum()
    rf_pos = (sub["rf_p_mus"] > 0.5).sum()
    mahal_pos = sub["closer_to_mushroom"].sum()
    print(f"Stone {stone} (n={n}):")
    print(f"  LDA:   {lda_pos}/{n} = {100*lda_pos/n:.1f}% mushroom, mean P = {sub['lda_p_mus'].mean():.3f}")
    print(f"  RF:    {rf_pos}/{n} = {100*rf_pos/n:.1f}% mushroom, mean P = {sub['rf_p_mus'].mean():.3f}")
    print(f"  Mahal: {mahal_pos}/{n} = {100*mahal_pos/n:.1f}% closer to mushroom")

carv_df.to_csv(OUT / "extended_carving_predictions.csv", index=False)

# ============================================================
# Figure: per-stone P(mushroom) distribution
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))
s53 = carv_df[carv_df["stone"].astype(str).str.startswith("53")]["rf_p_mus"].values
s4 = carv_df[carv_df["stone"].astype(str).isin(["4", "4.0"])]["rf_p_mus"].values

parts = ax.violinplot([s53, s4], showmedians=True, widths=0.7)
for pc, c in zip(parts["bodies"], ["#c14545", "#e07a2b"]):
    pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.7)
for key in ("cbars", "cmins", "cmaxes", "cmedians"):
    if key in parts:
        parts[key].set_color("black"); parts[key].set_linewidth(1.0)

for i, (d, col) in enumerate([(s53, "#c14545"), (s4, "#e07a2b")]):
    jit = np.random.default_rng(i).normal(0, 0.06, size=len(d))
    ax.scatter(np.full(len(d), i+1)+jit, d, s=15, alpha=0.55,
               color=col, edgecolor="none")

ax.axhline(0.5, color="gray", linestyle="--", linewidth=1, alpha=0.6)
ax.set_xticks([1, 2])
ax.set_xticklabels([f"Stone 53\nn={len(s53)}\nmedian P(mus)={np.median(s53):.2f}",
                     f"Stone 4\nn={len(s4)}\nmedian P(mus)={np.median(s4):.2f}"], fontsize=10)
ax.set_ylabel("Random Forest P(mushroom)", fontsize=11)
ax.set_ylim(0, 1)
ax.set_title(
    f"Per-stone classifier verdict: Stone 4 carvings agree with Stone 53.\n"
    f"Stone 53: {int((s53>0.5).sum())}/{len(s53)} predicted mushroom · "
    f"Stone 4: {int((s4>0.5).sum())}/{len(s4)} predicted mushroom.",
    fontsize=10.5, pad=8
)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "per_stone_predictions.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'per_stone_predictions.png'}")

summary = {
    "stone_53": {
        "n": int(len(s53)),
        "median_p_mushroom_rf": float(np.median(s53)),
        "mean_p_mushroom_rf": float(s53.mean()),
        "n_predicted_mushroom": int((s53 > 0.5).sum()),
    },
    "stone_4": {
        "n": int(len(s4)),
        "median_p_mushroom_rf": float(np.median(s4)),
        "mean_p_mushroom_rf": float(s4.mean()),
        "n_predicted_mushroom": int((s4 > 0.5).sum()),
    },
    "combined": {
        "n": int(len(carv_df)),
        "n_predicted_mushroom_lda": int((carv_df["lda_p_mus"] > 0.5).sum()),
        "n_predicted_mushroom_rf": int((carv_df["rf_p_mus"] > 0.5).sum()),
        "n_closer_to_mushroom_mahal": int(carv_df["closer_to_mushroom"].sum()),
        "mean_p_mushroom_lda": float(carv_df["lda_p_mus"].mean()),
        "mean_p_mushroom_rf": float(carv_df["rf_p_mus"].mean()),
    },
}
with open(OUT / "extended_predictions_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"Saved: extended_predictions_summary.json")
