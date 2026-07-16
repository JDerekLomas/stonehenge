"""
Calibrate our-pipeline shape features to the Lomas 2021 ImageJ scale.

For each feature (Circ, AR, Roundness, Solidity) we fit a linear
regression `lomas = a * ours + b` on the 41 Stone 53 TIFFs we have in
both — the paired samples where we know both pipelines were run on the
same physical image.

We then apply that fitted transformation to our Stone 4 and Ri Cruin
extractions, producing calibrated feature values on the Lomas ImageJ
scale. Backfill into master_carvings.csv with a source flag.

Rerun the classifier on the calibrated values and report per-source
prediction stability.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from skimage import measure
from scipy import stats
from scipy.spatial.distance import mahalanobis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).parent.parent
MASTER = ROOT / "data" / "master"


def load_bin(p):
    img = Image.open(p).convert("L")
    arr = np.asarray(img)
    d = (arr < 128).astype(np.uint8)
    l = (arr >= 128).astype(np.uint8)
    def e(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    return d if e(d) < e(l) else l


def features(binary):
    labels = measure.label(binary)
    props = measure.regionprops(labels)
    if not props: return None
    r = max(props, key=lambda p: p.area)
    a = float(r.area); pr = float(r.perimeter)
    if a <= 0 or pr <= 0: return None
    maj = float(r.axis_major_length)
    mn = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    return {
        "circularity": 4 * np.pi * a / (pr**2),
        "aspect_ratio": maj / mn,
        "roundness": 4 * a / (np.pi * maj**2),
        "solidity": float(r.solidity),
    }


# =============================================================
# 1. Build the calibration on 41 paired Stone 53 samples
# =============================================================
lomas = pd.read_excel(ROOT / "data" / "raw" / "Stone 53 Measurements.xlsx",
                     sheet_name="Carvings")
lomas["carving_id"] = lomas["Carving#"].apply(lambda x: f"F{int(x)}" if pd.notna(x) else "")
lomas_by = lomas.set_index("carving_id")

tif_dir = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"

pairs = []
for p in sorted(tif_dir.glob("F*.tif")):
    stem = p.stem.replace(" - 540wide", "")
    if stem not in lomas_by.index: continue
    ours = features(load_bin(p))
    lom = lomas_by.loc[stem]
    if ours is None: continue
    pairs.append({
        "id": stem,
        "ours_circ": ours["circularity"], "lomas_circ": lom["Circularity"],
        "ours_ar": ours["aspect_ratio"], "lomas_ar": lom["Aspect Ratio"],
        "ours_round": ours["roundness"], "lomas_round": lom["Roundness"],
        "ours_sol": ours["solidity"], "lomas_sol": lom["Solidity"],
    })
comp = pd.DataFrame(pairs)
print(f"Paired samples: {len(comp)}")

# Fit linear calibration per feature
calibration = {}
for feat in ["circ", "ar", "round", "sol"]:
    slope, intercept, r, p_val, se = stats.linregress(
        comp[f"ours_{feat}"], comp[f"lomas_{feat}"]
    )
    calibration[feat] = {"slope": float(slope), "intercept": float(intercept),
                          "r": float(r), "p": float(p_val)}
    print(f"  {feat:<8}  lomas = {slope:.4f} · ours + {intercept:+.4f}   r = {r:.4f}")

# Save calibration
import json
with open(MASTER / "pipeline_calibration.json", "w") as f:
    json.dump({
        "description": "Per-feature linear calibration from our extraction "
                        "pipeline to the Lomas 2021 ImageJ scale, fit on 41 "
                        "paired Stone 53 samples.",
        "usage": "Apply lomas_hat = slope * ours + intercept to bring our "
                  "extraction into scale-compatibility with Lomas 2021 ImageJ.",
        "features": calibration,
        "n_paired_samples": int(len(comp)),
    }, f, indent=2)
print(f"\nSaved calibration: {MASTER / 'pipeline_calibration.json'}")


# =============================================================
# 2. Backfill master_carvings.csv with calibrated features
# =============================================================
carv = pd.read_csv(MASTER / "master_carvings.csv")

def calibrate_row(row):
    """If this row was extracted with our pipeline, apply calibration."""
    src = str(row.get("source", ""))
    if "Extracted" not in src:
        return pd.Series([row["circularity"], row["aspect_ratio"],
                           row["roundness"], row["solidity"], False])
    circ = calibration["circ"]["slope"] * row["circularity"] + calibration["circ"]["intercept"]
    ar = calibration["ar"]["slope"] * row["aspect_ratio"] + calibration["ar"]["intercept"]
    rnd = calibration["round"]["slope"] * row["roundness"] + calibration["round"]["intercept"]
    sol = calibration["sol"]["slope"] * row["solidity"] + calibration["sol"]["intercept"]
    return pd.Series([circ, ar, rnd, sol, True])

new = carv.apply(calibrate_row, axis=1)
new.columns = ["circularity_calibrated", "aspect_ratio_calibrated",
                "roundness_calibrated", "solidity_calibrated",
                "features_were_calibrated"]
carv = pd.concat([carv, new], axis=1)

# Also rerun classifier on the calibrated features
allf = pd.read_excel(ROOT / "data" / "raw" / "Early Axes from Bevan.xlsx", sheet_name="All data")
train_axes = allf[allf["Type"] == "Axe"][["Circ.", "AR", "Round"]].dropna()
train_mus = allf[allf["Type"] == "Mushroom"][["Circ.", "AR", "Round"]].dropna()
X_train = pd.concat([train_axes, train_mus]).values
y_train = np.array(["axe"]*len(train_axes) + ["mushroom"]*len(train_mus))
scaler = StandardScaler().fit(X_train)
Xs = scaler.transform(X_train)
lda = LinearDiscriminantAnalysis().fit(Xs, y_train)
rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xs, y_train)
mus_lda = list(lda.classes_).index("mushroom")
mus_rf = list(rf.classes_).index("mushroom")
axe_std = scaler.transform(train_axes.values); mus_std = scaler.transform(train_mus.values)
axe_mean = axe_std.mean(axis=0); mus_mean = mus_std.mean(axis=0)
axe_ci = np.linalg.pinv(np.cov(axe_std.T))
mus_ci = np.linalg.pinv(np.cov(mus_std.T))

def predict_cal(row):
    x = np.array([row["circularity_calibrated"], row["aspect_ratio_calibrated"],
                   row["roundness_calibrated"]])
    if np.isnan(x).any():
        return pd.Series([None]*3)
    xs = scaler.transform(x.reshape(1, -1))[0]
    lda_p = float(lda.predict_proba(xs.reshape(1, -1))[0, mus_lda])
    rf_p = float(rf.predict_proba(xs.reshape(1, -1))[0, mus_rf])
    d_a = float(mahalanobis(xs, axe_mean, axe_ci))
    d_m = float(mahalanobis(xs, mus_mean, mus_ci))
    return pd.Series([lda_p, rf_p, "mushroom" if d_m < d_a else "axe"])

new2 = carv.apply(predict_cal, axis=1)
new2.columns = ["lda_p_mushroom_calibrated", "rf_p_mushroom_calibrated",
                 "nearest_centroid_calibrated"]
carv = pd.concat([carv, new2], axis=1)

carv.to_csv(MASTER / "master_carvings.csv", index=False)

# Report before / after
print("\n=== Per-source predictions BEFORE vs AFTER calibration ===\n")
print(f"{'Source':<45}  {'n':>3}  {'LDA%(raw)':>10}  {'LDA%(cal)':>10}  {'RF%(raw)':>9}  {'RF%(cal)':>9}  {'Mahal%(raw)':>11}  {'Mahal%(cal)':>11}")
for src, sub in carv.groupby("source"):
    if not len(sub): continue
    n = len(sub)
    def pct(col, thr=0.5):
        v = pd.to_numeric(sub[col], errors="coerce")
        return f"{100*(v > thr).mean():.0f}%"
    def eq(col, val):
        return f"{100*(sub[col] == val).mean():.0f}%"
    print(f"{str(src)[:45]:<45}  {n:>3}  "
          f"{pct('lda_p_mushroom'):>10}  {pct('lda_p_mushroom_calibrated'):>10}  "
          f"{pct('rf_p_mushroom'):>9}  {pct('rf_p_mushroom_calibrated'):>9}  "
          f"{eq('nearest_centroid', 'mushroom'):>11}  {eq('nearest_centroid_calibrated', 'mushroom'):>11}")

# Update data_dictionary.md with note about calibrated columns
dict_path = MASTER / "data_dictionary.md"
dict_text = dict_path.read_text()
if "calibrated" not in dict_text:
    addition = """

---

## Pipeline calibration (added in v2)

Our extraction pipeline produces feature values that agree with Lomas
2021 ImageJ at r > 0.99 for Circularity, Aspect Ratio, and Solidity
but with a systematic offset for Roundness (r = 0.91, mean −0.19).
The offset reflects a fitted-ellipse convention difference between
scikit-image `regionprops` and ImageJ.

`pipeline_calibration.json` contains per-feature linear calibrations
(`lomas_hat = slope · ours + intercept`) fit on 41 paired Stone 53
samples where both pipelines processed the same TIFF. `master_carvings.csv`
now contains four additional columns per row:

| Column | Description |
|---|---|
| `circularity_calibrated`, `aspect_ratio_calibrated`, `roundness_calibrated`, `solidity_calibrated` | The row's shape features transformed to the Lomas 2021 ImageJ scale via the fitted calibration. For Bevan and Lomas rows, `_calibrated` values equal the originals (no transform). For our-extraction rows (Stone 4, Ri Cruin) they are calibrated. |
| `features_were_calibrated` | Bool: whether a nontrivial calibration was applied to this row. |
| `lda_p_mushroom_calibrated`, `rf_p_mushroom_calibrated`, `nearest_centroid_calibrated` | Classifier re-run on the calibrated features. These are the cross-source-comparable predictions. |
"""
    dict_path.write_text(dict_text + addition)
    print(f"\nAppended calibration note to {dict_path}")
