"""
Extended shape-feature analysis.

Beyond the four canonical ImageJ features (Circularity, AR, Roundness,
Solidity) we compute three additional feature systems:

  (1) Hu moments — 7 features, invariant to translation/scale/rotation.
      Classical descriptors that separate shapes on their moment
      structure, unrelated to the aspect-ratio family.

  (2) Elliptical Fourier descriptor coefficients — first 8 harmonics
      (32 features). Captures contour form independent of size and
      orientation. We use them as features here (not just complexity
      as in §3.6).

  (3) Skeleton features — extracted from the medial-axis transform.
      Number of endpoints, branch count, width-along-skeleton mean
      and CV. A mushroom shape has bimodal width (wide cap + narrow
      stem); an axe has uniformly-decreasing width from blade to butt.

We then run the same axe-vs-mushroom classifier on:
  - just the 4 canonical features (baseline)
  - just Hu moments
  - just EFD coefficients
  - just skeleton features
  - all combined

If each system independently classifies carvings as mushroom, that's
converging evidence beyond the ImageJ features.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from skimage import measure, morphology
from skimage.morphology import medial_axis
from scipy import ndimage as ndi
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
import cv2  # for Hu moments; if not available fall back to pure numpy

ROOT = Path(__file__).parent.parent

# =============================================================
# Feature extractors
# =============================================================
def largest_component(binary):
    labels = measure.label(binary)
    props = measure.regionprops(labels)
    if not props: return None
    r = max(props, key=lambda p: p.area)
    return (labels == r.label).astype(np.uint8), r


def hu_moments(binary):
    """7 Hu moments, log-scaled for numerical stability."""
    m = cv2.moments((binary * 255).astype(np.uint8))
    h = cv2.HuMoments(m).flatten()
    # log-scale (preserving sign) — Hu moments span many orders of magnitude
    return -np.sign(h) * np.log10(np.abs(h) + 1e-40)


def elliptical_fourier(contour, n_harmonics=8):
    """Compute normalized EFD coefficients for a closed contour.
    Returns 4*n_harmonics real values, invariant to translation, scale,
    rotation, and start point.

    Ref: Kuhl & Giardina (1982); this implementation follows Bonhomme
    et al. Journal of Statistical Software (2014).
    """
    # contour is (N, 2) as (row, col) — treat as (y, x)
    contour = contour[:, ::-1]  # to (x, y)
    dx = np.diff(contour[:, 0])
    dy = np.diff(contour[:, 1])
    dt = np.sqrt(dx**2 + dy**2)
    t = np.concatenate([[0], np.cumsum(dt)])
    T = t[-1]
    if T == 0: return np.zeros(4 * n_harmonics)
    phi = 2 * np.pi * t / T

    coeffs = np.zeros((n_harmonics, 4))
    for n in range(1, n_harmonics + 1):
        c = T / (2 * n**2 * np.pi**2)
        cos_ph = np.cos(n * phi)
        sin_ph = np.sin(n * phi)
        d_cos = np.diff(cos_ph)
        d_sin = np.diff(sin_ph)
        coeffs[n-1, 0] = c * np.sum(dx / dt * d_cos)  # an
        coeffs[n-1, 1] = c * np.sum(dx / dt * d_sin)  # bn
        coeffs[n-1, 2] = c * np.sum(dy / dt * d_cos)  # cn
        coeffs[n-1, 3] = c * np.sum(dy / dt * d_sin)  # dn

    # Normalize to invariance:
    # 1. Rotation invariance — rotate to align with first harmonic principal axis
    a1, b1, c1, d1 = coeffs[0]
    theta = 0.5 * np.arctan2(2 * (a1*b1 + c1*d1), a1**2 - b1**2 + c1**2 - d1**2)
    for n in range(n_harmonics):
        rot = np.array([[np.cos((n+1)*theta), np.sin((n+1)*theta)],
                         [-np.sin((n+1)*theta), np.cos((n+1)*theta)]])
        mat = np.array([[coeffs[n, 0], coeffs[n, 1]],
                        [coeffs[n, 2], coeffs[n, 3]]])
        coeffs[n] = (mat @ rot).flatten()

    # 2. Scale — divide by first harmonic amplitude
    A = np.sqrt(coeffs[0, 0]**2 + coeffs[0, 2]**2)
    if A > 0:
        coeffs = coeffs / A
    return coeffs.flatten()


def skeleton_features(binary):
    """Skeleton-derived shape features."""
    skel, dist = medial_axis(binary.astype(bool), return_distance=True)
    dist_along = dist[skel]
    if len(dist_along) == 0:
        return np.zeros(6)
    return np.array([
        skel.sum(),                                    # skeleton length (pixels)
        dist_along.mean(),                              # mean local width
        dist_along.std() / (dist_along.mean() + 1e-9),  # coefficient of variation
        dist_along.max(),                               # widest point
        dist_along.min(),                               # narrowest point
        # bimodality proxy: proportion of skeleton pixels > 1.5 * median width
        (dist_along > 1.5 * np.median(dist_along)).mean(),
    ])


def load_bin(path):
    img = Image.open(path).convert("L")
    arr = np.asarray(img)
    d = (arr < 128).astype(np.uint8)
    l = (arr >= 128).astype(np.uint8)
    def e(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    return d if e(d) < e(l) else l


def all_features(binary):
    """Extract all four feature systems from one binary mask."""
    lb, r = largest_component(binary)
    if lb is None:
        return None
    # ImageJ features
    a = float(r.area); pr = float(r.perimeter)
    maj = float(r.axis_major_length)
    mn = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    imagej = np.array([
        4 * np.pi * a / (pr**2),
        maj / mn,
        4 * a / (np.pi * maj**2),
        float(r.solidity),
    ])
    # Hu
    hu = hu_moments(lb)
    # EFD
    contours = measure.find_contours(lb.astype(float), 0.5)
    if not contours:
        efd = np.zeros(32)
    else:
        c = max(contours, key=len)
        efd = elliptical_fourier(c, n_harmonics=8)
    # Skeleton
    skel = skeleton_features(lb)
    return imagej, hu, efd, skel


def extract_corpus(paths):
    rows = []
    for p in paths:
        try:
            bw = load_bin(p)
            feats = all_features(bw)
            if feats is None: continue
            imagej, hu, efd, skel = feats
            rows.append({
                "id": p.stem,
                **{f"imagej_{i}": v for i, v in enumerate(imagej)},
                **{f"hu_{i}": v for i, v in enumerate(hu)},
                **{f"efd_{i}": v for i, v in enumerate(efd)},
                **{f"skel_{i}": v for i, v in enumerate(skel)},
            })
        except Exception as e:
            print(f"  {p.name}: {e}")
    return pd.DataFrame(rows)


# =============================================================
# Corpora
# =============================================================
S53_DIR = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
S4_DIR = ROOT / "data" / "stone4_extracted" / "full"
AXE_DIR = ROOT / "data" / "downloads_extracted" / "Axes (Needham 1983, 2012_ burgess)"
MUS_DIR = ROOT / "data" / "downloads_extracted" / "Entire Image Corpus" / "mushrooms"

print("Extracting features …")
axe = extract_corpus(list(AXE_DIR.glob("*.tif")))
mus = extract_corpus(list(MUS_DIR.glob("*.tif")) + list(MUS_DIR.glob("*.jpg")))
s53 = extract_corpus(list(S53_DIR.glob("F*.tif")))
s4 = extract_corpus(list(S4_DIR.glob("*.png")))
print(f"axe: {len(axe)}  mushroom: {len(mus)}  Stone 53: {len(s53)}  Stone 4: {len(s4)}")

carv = pd.concat([s53.assign(stone="53"), s4.assign(stone="4")], ignore_index=True)

def cols_starting(df, pref):
    return [c for c in df.columns if c.startswith(pref)]

# =============================================================
# Classifier on each feature system separately
# =============================================================
systems = {
    "imagej (4)": cols_starting(axe, "imagej_"),
    "hu (7)": cols_starting(axe, "hu_"),
    "efd (32)": cols_starting(axe, "efd_"),
    "skeleton (6)": cols_starting(axe, "skel_"),
    "all (49)": (cols_starting(axe, "imagej_") + cols_starting(axe, "hu_")
                  + cols_starting(axe, "efd_") + cols_starting(axe, "skel_")),
}

print("\n=== Classifier accuracy by feature system ===\n")
print(f"{'System':<15}  {'LDA CV':<14}  {'RF CV':<14}  {'LDA % carv→mus':<16}  {'RF % carv→mus'}")

for name, cols in systems.items():
    X = pd.concat([axe[cols], mus[cols]]).values
    y = np.array(["axe"]*len(axe) + ["mushroom"]*len(mus))
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)

    lda_cv = cross_val_score(LinearDiscriminantAnalysis(), Xs, y,
                              cv=StratifiedKFold(5, shuffle=True, random_state=42))
    rf_cv = cross_val_score(RandomForestClassifier(n_estimators=300, random_state=42),
                             Xs, y, cv=StratifiedKFold(5, shuffle=True, random_state=42))

    lda = LinearDiscriminantAnalysis().fit(Xs, y)
    rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xs, y)
    Xs_c = scaler.transform(carv[cols].values)
    lda_p_mus = lda.predict_proba(Xs_c)[:, list(lda.classes_).index("mushroom")]
    rf_p_mus = rf.predict_proba(Xs_c)[:, list(rf.classes_).index("mushroom")]

    print(f"{name:<15}  {lda_cv.mean():.3f}±{lda_cv.std():.3f}  "
          f"{rf_cv.mean():.3f}±{rf_cv.std():.3f}  "
          f"{100*(lda_p_mus>0.5).mean():>7.1f}%          "
          f"{100*(rf_p_mus>0.5).mean():>6.1f}%  (mean P: {rf_p_mus.mean():.2f})")

carv.to_csv(ROOT / "data" / "processed" / "carvings_extended_features.csv", index=False)
axe.to_csv(ROOT / "data" / "processed" / "axes_extended_features.csv", index=False)
mus.to_csv(ROOT / "data" / "processed" / "mushrooms_extended_features.csv", index=False)
