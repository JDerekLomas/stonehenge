"""
Build a multi-class alternative-reference corpus and rerun the
classifier as multi-way instead of binary axe-vs-mushroom.

Classes (target: 20 silhouettes each):

  1. Axes           — Needham + Burgess canonical silhouettes (real)
  2. Mushrooms      — pre-segmented silhouettes (real)
  3. Halberds       — synthetic prototypes with variation
                      (long haft + crescentic blade at right angle)
  4. Sickles        — synthetic prototypes
                      (crescentic blade + handle)
  5. Trees          — synthetic prototypes
                      (round crown + trunk; several crown/trunk ratios)
  6. Human figures  — synthetic schematic figures
                      (head + torso + legs)
  7. Random null    — random blob silhouettes (Gaussian random field
                      thresholded)

Then compute (Circ, AR, Roundness) for every silhouette and ask, per
Stonehenge carving, which class centroid is nearest.

This addresses critique §4.6.1 as an initial pass. Real museum
silhouettes for halberds/sickles would strengthen it further; these
synthetics establish the multi-class methodology.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from skimage import measure, morphology
from scipy.spatial.distance import cdist
from scipy import ndimage

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "multiclass_corpus"
OUT.mkdir(exist_ok=True)
for sub in ("halberd", "sickle", "tree", "human", "random"):
    (OUT / sub).mkdir(exist_ok=True)

rng = np.random.default_rng(20260716)
CANVAS = 400

# =============================================================
# Prototype generators
# =============================================================
def render_halberd(i, canvas=CANVAS):
    """Long thin haft + crescentic blade at ~90° to haft near the top."""
    img = Image.new("L", (canvas, canvas), 0)
    d = ImageDraw.Draw(img)
    haft_w = rng.integers(8, 14)
    haft_h = int(canvas * rng.uniform(0.75, 0.9))
    haft_x = canvas // 2 - haft_w // 2
    haft_y = canvas - haft_h
    d.rectangle([haft_x, haft_y, haft_x + haft_w, canvas], fill=255)
    # Blade: curved (chord of ellipse) attached at the top
    blade_w = rng.integers(60, 110)
    blade_h = rng.integers(30, 55)
    cx = canvas // 2 + rng.integers(-5, 5)
    cy = haft_y + blade_h // 2 + 4
    d.chord([cx - blade_w//2, cy - blade_h//2 - blade_h,
             cx + blade_w//2, cy + blade_h//2], 0, 180, fill=255)
    # Optional spike opposite the blade
    if rng.random() < 0.5:
        spike_len = rng.integers(15, 40)
        d.polygon([(cx + blade_w//2, cy), (cx + blade_w//2 + spike_len, cy),
                   (cx + blade_w//2, cy - 8)], fill=255)
    return np.asarray(img)


def render_sickle(i, canvas=CANVAS):
    """Crescentic blade + short handle."""
    img = Image.new("L", (canvas, canvas), 0)
    d = ImageDraw.Draw(img)
    # Handle
    handle_w = rng.integers(20, 32)
    handle_h = rng.integers(90, 130)
    hx = canvas // 2 - handle_w // 2
    hy = canvas - handle_h
    d.rounded_rectangle([hx, hy, hx + handle_w, canvas], radius=8, fill=255)
    # Crescent blade at top of handle
    r_outer = rng.integers(75, 130)
    r_inner = int(r_outer * rng.uniform(0.55, 0.75))
    cx = canvas // 2
    cy = hy - 10
    outer = Image.new("L", (canvas, canvas), 0)
    ImageDraw.Draw(outer).chord(
        [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
        200, 340, fill=255
    )
    inner = Image.new("L", (canvas, canvas), 0)
    ImageDraw.Draw(inner).chord(
        [cx - r_inner, cy - r_inner + 15, cx + r_inner, cy + r_inner + 15],
        200, 340, fill=255
    )
    arr = np.asarray(outer).copy()
    arr[np.asarray(inner) > 128] = 0
    img_arr = np.maximum(np.asarray(img), arr)
    return img_arr


def render_tree(i, canvas=CANVAS):
    """Round crown on top of a straight trunk."""
    img = Image.new("L", (canvas, canvas), 0)
    d = ImageDraw.Draw(img)
    trunk_w = rng.integers(20, 45)
    trunk_h = rng.integers(80, 160)
    trunk_x = canvas // 2 - trunk_w // 2
    trunk_y = canvas - trunk_h
    d.rectangle([trunk_x, trunk_y, trunk_x + trunk_w, canvas], fill=255)
    # Crown: elliptical or circular
    crown_rx = rng.integers(70, 130)
    crown_ry = rng.integers(60, 120)
    cx = canvas // 2
    cy = trunk_y - crown_ry // 2 + 10
    d.ellipse([cx - crown_rx, cy - crown_ry, cx + crown_rx, cy + crown_ry],
              fill=255)
    return np.asarray(img)


def render_human(i, canvas=CANVAS):
    """Schematic human: head + torso + legs, arms optional."""
    img = Image.new("L", (canvas, canvas), 0)
    d = ImageDraw.Draw(img)
    head_r = rng.integers(20, 35)
    torso_w = rng.integers(45, 70)
    torso_h = rng.integers(80, 120)
    leg_w = rng.integers(15, 25)
    leg_h = rng.integers(90, 140)
    cx = canvas // 2
    total_h = 2*head_r + torso_h + leg_h + 20
    top_y = (canvas - total_h) // 2
    # Head
    d.ellipse([cx - head_r, top_y, cx + head_r, top_y + 2*head_r], fill=255)
    # Torso
    torso_y = top_y + 2*head_r + 5
    d.rounded_rectangle([cx - torso_w//2, torso_y,
                          cx + torso_w//2, torso_y + torso_h],
                         radius=8, fill=255)
    # Legs — two rectangles
    leg_y = torso_y + torso_h + 3
    d.rectangle([cx - torso_w//2 + 5, leg_y, cx - torso_w//2 + 5 + leg_w,
                 leg_y + leg_h], fill=255)
    d.rectangle([cx + torso_w//2 - 5 - leg_w, leg_y,
                 cx + torso_w//2 - 5, leg_y + leg_h], fill=255)
    # Arms (optional)
    if rng.random() < 0.6:
        arm_len = rng.integers(50, 90)
        arm_w = rng.integers(12, 20)
        d.rectangle([cx - torso_w//2 - arm_len, torso_y + 5,
                     cx - torso_w//2, torso_y + 5 + arm_w], fill=255)
        d.rectangle([cx + torso_w//2, torso_y + 5,
                     cx + torso_w//2 + arm_len, torso_y + 5 + arm_w], fill=255)
    return np.asarray(img)


def render_random_blob(i, canvas=CANVAS):
    """Gaussian random field thresholded to a single connected blob."""
    field = rng.standard_normal((canvas, canvas))
    sigma = rng.uniform(15, 30)
    field = ndimage.gaussian_filter(field, sigma=sigma)
    # Threshold near median so about 15% is above
    thr = np.quantile(field, 0.85)
    mask = (field > thr).astype(np.uint8) * 255
    # Keep only largest component
    labels = measure.label(mask)
    props = measure.regionprops(labels)
    if not props:
        return render_random_blob(i, canvas)
    r = max(props, key=lambda p: p.area)
    if r.area < 500:
        return render_random_blob(i, canvas)
    keep = (labels == r.label).astype(np.uint8) * 255
    return keep


# =============================================================
# Generate 20 per class
# =============================================================
GENERATORS = {
    "halberd": render_halberd,
    "sickle": render_sickle,
    "tree": render_tree,
    "human": render_human,
    "random": render_random_blob,
}
N_PER_CLASS = 20

for cls, gen in GENERATORS.items():
    for i in range(N_PER_CLASS):
        arr = gen(i)
        Image.fromarray(arr, mode="L").save(OUT / cls / f"{cls}_{i:03d}.png")
    print(f"  {cls}: {N_PER_CLASS} silhouettes")


# =============================================================
# Feature extraction (matches script 35 / 38)
# =============================================================
def features(binary):
    labels = measure.label(binary > 128)
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


rows = []
for cls in GENERATORS:
    for p in sorted((OUT / cls).glob("*.png")):
        arr = np.asarray(Image.open(p).convert("L"))
        f = features(arr)
        if f is None: continue
        rows.append({"class": cls, "id": p.stem, **f})

# Also add axes and mushrooms from existing sources
BEVAN = ROOT / "data" / "raw" / "Early Axes from Bevan.xlsx"
allf = pd.read_excel(BEVAN, sheet_name="All data")
for _, r in allf[allf["Type"] == "Axe"][["Label", "Circ.", "AR", "Round", "Solidity"]].dropna().iterrows():
    rows.append({"class": "axe", "id": str(r["Label"]),
                  "circularity": r["Circ."], "aspect_ratio": r["AR"],
                  "roundness": r["Round"], "solidity": r["Solidity"]})
for _, r in allf[allf["Type"] == "Mushroom"][["Label", "Circ.", "AR", "Round", "Solidity"]].dropna().iterrows():
    rows.append({"class": "mushroom", "id": str(r["Label"]),
                  "circularity": r["Circ."], "aspect_ratio": r["AR"],
                  "roundness": r["Round"], "solidity": r["Solidity"]})

ref_df = pd.DataFrame(rows)
print("\nReference sample sizes:")
print(ref_df["class"].value_counts())
ref_df.to_csv(OUT / "multiclass_reference_features.csv", index=False)


# =============================================================
# Classifier — nearest centroid, 7-way
# =============================================================
FEATS = ["circularity", "aspect_ratio", "roundness"]
# Standardize
X_all = ref_df[FEATS].values
mean = X_all.mean(axis=0); std = X_all.std(axis=0)
X_std = (X_all - mean) / std
ref_df["_std"] = list(X_std)

centroids = ref_df.groupby("class")[FEATS].mean()
centroids_std = (centroids.values - mean) / std
class_names = centroids.index.tolist()
print("\n=== Per-class centroids (raw features) ===")
print(centroids.round(3).to_string())

# Load carvings (Bevan All-data 119, plus our own Stone 4 calibrated)
carv = pd.read_csv(ROOT / "data" / "master" / "master_carvings.csv")
# Use calibrated features where available, raw otherwise
carv["cf_circ"] = carv["circularity_calibrated"].fillna(carv["circularity"])
carv["cf_ar"] = carv["aspect_ratio_calibrated"].fillna(carv["aspect_ratio"])
carv["cf_round"] = carv["roundness_calibrated"].fillna(carv["roundness"])
carv_valid = carv.dropna(subset=["cf_circ", "cf_ar", "cf_round"])
print(f"\nCarvings ready for multi-class assignment: {len(carv_valid)}")

X_carv = carv_valid[["cf_circ", "cf_ar", "cf_round"]].values
X_carv_std = (X_carv - mean) / std
dists = cdist(X_carv_std, centroids_std)
assign_idx = dists.argmin(axis=1)
carv_valid = carv_valid.copy()
carv_valid["multiclass_nearest"] = [class_names[i] for i in assign_idx]

print("\n=== Multi-class assignment counts (all carving rows) ===")
print(carv_valid["multiclass_nearest"].value_counts())

print("\n=== Per source ===")
for src, sub in carv_valid.groupby("source"):
    counts = sub["multiclass_nearest"].value_counts()
    print(f"\n{src[:60]}  (n={len(sub)})")
    for cls in class_names:
        n = counts.get(cls, 0)
        if n:
            print(f"  {cls:<12}  {n}")

# Save
carv_valid[["carving_id", "stone", "source", "multiclass_nearest"]].to_csv(
    OUT / "multiclass_assignments.csv", index=False
)
print(f"\nSaved: {OUT / 'multiclass_assignments.csv'}")
