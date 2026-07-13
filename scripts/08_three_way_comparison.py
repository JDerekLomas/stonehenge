"""
Three-way shape comparison:  axes vs carvings vs mushrooms.

The paper's central claim is that Stone 53 carvings look more like
Amanita muscaria mushrooms than like British EBA axes. This script
tests that claim quantitatively for the first time using real data
from all three classes.

For each of the 4 dimensionless shape features (Circularity, Aspect
Ratio, Roundness, Solidity), we compute:
  1. Per-class distributions with descriptive stats
  2. Which class's centroid each carving is closest to (Mahalanobis)
  3. Cross-validated LDA classifier: axe vs mushroom, then predict carvings

Success criterion for the mushroom hypothesis: a majority of Stone 53
carvings are classified as mushroom, and the axe-vs-mushroom classifier
achieves reasonable CV accuracy on its training data.
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import mahalanobis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import json

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

FEATURES = ["Circularity", "Aspect Ratio", "Roundness"]  # Excluded Solidity — see note
# NOTE ON SOLIDITY:
#   Excluded because our automated color-based segmentation of A. muscaria
#   photos required convex-hull filling to handle the white cap spots. This
#   artificially inflates mushroom Solidity (mean 0.945) vs real ImageJ
#   measurements on clean silhouettes. Including Solidity would let a
#   classifier trivially separate axes and mushrooms on a segmentation
#   artifact rather than a real shape difference. See prereg §4.1 for the
#   planned SAM-based segmentation that would let us include this feature.


def load_axes():
    df = pd.read_csv(DATA / "early_axes_bevan.csv")[["Circ.", "AR", "Round"]].dropna()
    df.columns = FEATURES
    df["source"] = "axe"
    return df


def load_carvings():
    df = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
    df = df[df["Stone"] == 53][["Circularity", "Aspect Ratio", "Roundness"]].dropna()
    df.columns = FEATURES
    df["source"] = "carving"
    return df


def load_muscaria():
    p = PROCESSED / "muscaria_shape_features.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p)[FEATURES + ["id"]]
    df["source"] = "muscaria"
    return df


def describe(name, df):
    print(f"\n=== {name} (n = {len(df)}) ===")
    for f in FEATURES:
        col = df[f]
        print(f"  {f:<15}  mean = {col.mean():.3f} ± {col.std():.3f}  "
              f"median = {col.median():.3f}")


def mahalanobis_class_assignment(carvings, axe_centroid, axe_cov_inv,
                                  mus_centroid, mus_cov_inv):
    """For each carving, return distance to axe and mushroom centroids."""
    d_axe = np.array([mahalanobis(p, axe_centroid, axe_cov_inv) for p in carvings])
    d_mus = np.array([mahalanobis(p, mus_centroid, mus_cov_inv) for p in carvings])
    assigned = np.where(d_axe < d_mus, "axe", "muscaria")
    return d_axe, d_mus, assigned


def main():
    axes = load_axes()
    carvings = load_carvings()
    muscaria = load_muscaria()

    describe("British EBA axes (Bevan)", axes)
    describe("Stone 53 carvings", carvings)
    if muscaria is None:
        print("\n*** No muscaria features yet. Run 07_extract_muscaria_features.py first. ***")
        return
    describe("Amanita muscaria (iNaturalist, auto-segmented)", muscaria)

    # === 1. Per-carving Mahalanobis distance to axe and mushroom centroids ===
    print("\n=== Per-carving nearest class (Mahalanobis) ===\n")

    axe_X = axes[FEATURES].values
    mus_X = muscaria[FEATURES].values
    car_X = carvings[FEATURES].values

    axe_mean = axe_X.mean(axis=0)
    mus_mean = mus_X.mean(axis=0)
    axe_cov_inv = np.linalg.pinv(np.cov(axe_X.T))
    mus_cov_inv = np.linalg.pinv(np.cov(mus_X.T))

    d_axe, d_mus, assigned = mahalanobis_class_assignment(
        car_X, axe_mean, axe_cov_inv, mus_mean, mus_cov_inv
    )

    n_muscaria = int((assigned == "muscaria").sum())
    n_axe = int((assigned == "axe").sum())
    print(f"  Carvings closer to mushroom centroid than axe centroid: "
          f"{n_muscaria}/{len(carvings)} ({100*n_muscaria/len(carvings):.1f}%)")
    print(f"  Carvings closer to axe centroid: "
          f"{n_axe}/{len(carvings)} ({100*n_axe/len(carvings):.1f}%)")
    print(f"  Median D to axe centroid:     {np.median(d_axe):.2f}")
    print(f"  Median D to mushroom centroid: {np.median(d_mus):.2f}")

    # === 2. Cross-validated axe-vs-mushroom classifier ===
    print("\n=== CV accuracy: axe vs mushroom classifier (validation) ===\n")

    X_train = np.vstack([axe_X, mus_X])
    y_train = np.array(["axe"] * len(axe_X) + ["muscaria"] * len(mus_X))

    scaler = StandardScaler().fit(X_train)
    X_train_s = scaler.transform(X_train)

    for name, clf in [
        ("LDA", LinearDiscriminantAnalysis()),
        ("Random Forest", RandomForestClassifier(n_estimators=300, random_state=42)),
    ]:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(clf, X_train_s, y_train, cv=cv, scoring="accuracy")
        print(f"  {name:<15}  5-fold CV accuracy = {scores.mean():.3f} ± {scores.std():.3f}")

    # === 3. Fit final classifier on all axe+mushroom data, predict carvings ===
    print("\n=== Predicting carvings using axe-vs-mushroom classifier ===\n")

    X_carv_s = scaler.transform(car_X)

    clf = LinearDiscriminantAnalysis().fit(X_train_s, y_train)
    proba = clf.predict_proba(X_carv_s)
    preds = clf.predict(X_carv_s)
    mus_idx = list(clf.classes_).index("muscaria")

    n_mus_pred = int((preds == "muscaria").sum())
    conf_high = int((proba[:, mus_idx] > 0.8).sum())
    print(f"LDA predictions on {len(carvings)} Stone 53 carvings:")
    print(f"  Classified as 'muscaria': {n_mus_pred}/{len(carvings)} "
          f"({100*n_mus_pred/len(carvings):.1f}%)")
    print(f"  Classified as 'axe':      {len(carvings)-n_mus_pred}/{len(carvings)}")
    print(f"  With mushroom probability > 0.8: {conf_high}/{len(carvings)} "
          f"({100*conf_high/len(carvings):.1f}%)")
    print(f"  Mean P(mushroom): {proba[:, mus_idx].mean():.3f}")

    # Random Forest for comparison
    clf_rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(X_train_s, y_train)
    proba_rf = clf_rf.predict_proba(X_carv_s)
    preds_rf = clf_rf.predict(X_carv_s)
    mus_idx_rf = list(clf_rf.classes_).index("muscaria")
    n_mus_pred_rf = int((preds_rf == "muscaria").sum())
    print(f"\nRandom Forest predictions on {len(carvings)} Stone 53 carvings:")
    print(f"  Classified as 'muscaria': {n_mus_pred_rf}/{len(carvings)} "
          f"({100*n_mus_pred_rf/len(carvings):.1f}%)")
    print(f"  Mean P(mushroom): {proba_rf[:, mus_idx_rf].mean():.3f}")

    # === 4. Feature importance from Random Forest ===
    importances = pd.Series(clf_rf.feature_importances_, index=FEATURES).sort_values(ascending=False)
    print("\n=== Which features drive the axe-vs-mushroom distinction? ===")
    for feat, imp in importances.items():
        print(f"  {feat:<15}  {imp:.3f}")

    # Save all per-carving predictions
    df_out = carvings.copy().reset_index(drop=True)
    df_out["d_to_axe"] = d_axe
    df_out["d_to_mushroom"] = d_mus
    df_out["nearest_by_mahal"] = assigned
    df_out["lda_prob_muscaria"] = proba[:, mus_idx]
    df_out["lda_prediction"] = preds
    df_out["rf_prob_muscaria"] = proba_rf[:, mus_idx_rf]
    df_out["rf_prediction"] = preds_rf
    df_out.to_csv(PROCESSED / "three_way_predictions.csv", index=False)

    summary = {
        "n_axes": int(len(axes)),
        "n_carvings": int(len(carvings)),
        "n_muscaria": int(len(muscaria)),
        "carvings_closer_to_muscaria_mahal": n_muscaria,
        "carvings_lda_predict_muscaria": n_mus_pred,
        "carvings_lda_high_confidence_muscaria": conf_high,
        "carvings_rf_predict_muscaria": n_mus_pred_rf,
        "lda_mean_p_muscaria": float(proba[:, mus_idx].mean()),
        "rf_mean_p_muscaria": float(proba_rf[:, mus_idx_rf].mean()),
        "feature_importance_rf": importances.to_dict(),
    }
    with open(PROCESSED / "three_way_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved:")
    print(f"  {PROCESSED / 'three_way_predictions.csv'}")
    print(f"  {PROCESSED / 'three_way_summary.json'}")


if __name__ == "__main__":
    main()
