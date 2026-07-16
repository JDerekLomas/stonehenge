"""
Fixed extended-features analysis.

Changes from script 38:
  - EFD: use `pyefd` package (validated Kuhl & Giardina 1982 implementation
    with proper normalisation) instead of my hand-rolled version
  - Skeleton: prune spurious short branches; use only 3 features
    (mean width, CV of width, bimodality proxy) instead of 6
  - Report Hu moments unchanged (they validated as a straight cv2 call)

Also produces a fresh visual QA to confirm the fixed EFD reconstruction
actually matches the shapes.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from skimage import measure, morphology
from skimage.morphology import medial_axis, skeletonize
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import mahalanobis
import cv2
import pyefd

ROOT = Path(__file__).parent.parent
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"

N_HARMONICS = 10  # pyefd default recommendation


def load_bin(path):
    img = Image.open(path).convert("L")
    arr = np.asarray(img)
    d = (arr < 128).astype(np.uint8)
    l = (arr >= 128).astype(np.uint8)
    def e(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    return d if e(d) < e(l) else l


def largest_component(binary):
    labels = measure.label(binary)
    props = measure.regionprops(labels)
    if not props: return None, None
    r = max(props, key=lambda p: p.area)
    return (labels == r.label).astype(np.uint8), r


def pruned_skeleton(binary, prune_iters=5):
    """Skeleton with short spurious branches pruned by iterative endpoint removal."""
    skel = skeletonize(binary.astype(bool)).astype(np.uint8)
    for _ in range(prune_iters):
        # Neighbourhood count
        from scipy.signal import convolve2d
        kernel = np.ones((3, 3)); kernel[1, 1] = 0
        n = convolve2d(skel, kernel, mode="same", boundary="fill", fillvalue=0)
        # Endpoints have exactly 1 neighbour
        endpoints = (skel == 1) & (n == 1)
        skel = skel & ~endpoints
    return skel.astype(bool)


def features(binary):
    lb, r = largest_component(binary)
    if lb is None: return None
    a = float(r.area); pr = float(r.perimeter)
    maj = float(r.axis_major_length)
    mn = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6

    # ImageJ 4
    imagej = np.array([
        4*np.pi*a/(pr**2), maj/mn, 4*a/(np.pi*maj**2), float(r.solidity)
    ])

    # Hu 7 (log-scaled for stability)
    m = cv2.moments((lb * 255).astype(np.uint8))
    hu = cv2.HuMoments(m).flatten()
    hu = -np.sign(hu) * np.log10(np.abs(hu) + 1e-40)

    # EFD via pyefd
    contours = measure.find_contours(lb.astype(float), 0.5)
    if not contours:
        efd = np.zeros(N_HARMONICS * 4)
    else:
        c = max(contours, key=len)
        # pyefd expects (N, 2) [x, y]; contour is (row, col)
        cxy = c[:, ::-1]
        coeffs = pyefd.elliptic_fourier_descriptors(
            cxy, order=N_HARMONICS, normalize=True
        )
        efd = coeffs.flatten()

    # Skeleton: only 3 features on pruned skeleton
    _, dist = medial_axis(lb.astype(bool), return_distance=True)
    skel = pruned_skeleton(lb)
    dist_along = dist[skel]
    if len(dist_along) < 5:
        sk = np.array([0.0, 0.0, 0.0])
    else:
        sk = np.array([
            dist_along.mean(),
            dist_along.std() / (dist_along.mean() + 1e-9),
            (dist_along > 1.5 * np.median(dist_along)).mean(),
        ])

    return imagej, hu, efd, sk


def extract_corpus(paths):
    rows = []
    for p in paths:
        try:
            bw = load_bin(p)
            r = features(bw)
            if r is None: continue
            im, hu, efd, sk = r
            rows.append({
                "id": p.stem,
                **{f"imagej_{i}": v for i, v in enumerate(im)},
                **{f"hu_{i}": v for i, v in enumerate(hu)},
                **{f"efd_{i}": v for i, v in enumerate(efd)},
                **{f"skel_{i}": v for i, v in enumerate(sk)},
            })
        except Exception as e:
            print(f"  {p.name}: {e}")
    return pd.DataFrame(rows)


# =========================================================
# Load corpora
# =========================================================
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


systems = {
    "imagej (4)": cols_starting(axe, "imagej_"),
    "hu (7)": cols_starting(axe, "hu_"),
    "efd-pyefd (40)": cols_starting(axe, "efd_"),
    "skeleton (3)": cols_starting(axe, "skel_"),
    "all (54)": (cols_starting(axe, "imagej_") + cols_starting(axe, "hu_")
                  + cols_starting(axe, "efd_") + cols_starting(axe, "skel_")),
}

print("\n=== Classifier accuracy by feature system (fixed pipeline) ===\n")
print(f"{'System':<18}  {'LDA CV':<14}  {'RF CV':<14}  {'LDA %mus':<10}  {'RF %mus':<10}  {'Mahal %closer_mus'}")

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
    lda_p = lda.predict_proba(Xs_c)[:, list(lda.classes_).index("mushroom")]
    rf_p = rf.predict_proba(Xs_c)[:, list(rf.classes_).index("mushroom")]

    # Mahalanobis on standardized features
    axe_std = scaler.transform(axe[cols].values)
    mus_std = scaler.transform(mus[cols].values)
    axe_m = axe_std.mean(axis=0); mus_m = mus_std.mean(axis=0)
    axe_ci = np.linalg.pinv(np.cov(axe_std.T))
    mus_ci = np.linalg.pinv(np.cov(mus_std.T))
    d_a = np.array([mahalanobis(x, axe_m, axe_ci) for x in Xs_c])
    d_m = np.array([mahalanobis(x, mus_m, mus_ci) for x in Xs_c])
    closer_mus = int((d_m < d_a).sum())

    print(f"{name:<18}  {lda_cv.mean():.3f}±{lda_cv.std():.3f}  "
          f"{rf_cv.mean():.3f}±{rf_cv.std():.3f}  "
          f"{100*(lda_p>0.5).mean():>6.1f}%    "
          f"{100*(rf_p>0.5).mean():>6.1f}%    "
          f"{100*closer_mus/len(carv):>6.1f}%")

carv.to_csv(OUT / "carvings_extended_features_v2.csv", index=False)

# =========================================================
# Visual QA: fixed EFD reconstruction on 3 samples
# =========================================================
sample_ids = ["F595", "F607", "F630"]
fig, axarr = plt.subplots(2, 3, figsize=(11, 7))
for col, sid in enumerate(sample_ids):
    p = S53_DIR / f"{sid}.tif"
    if not p.exists(): continue
    bw = load_bin(p)
    lb, _ = largest_component(bw)
    contours = measure.find_contours(lb.astype(float), 0.5)
    c = max(contours, key=len)
    cxy = c[:, ::-1]

    # Original silhouette + contour
    axarr[0, col].imshow(1 - lb, cmap="gray")
    axarr[0, col].plot(cxy[:, 0], cxy[:, 1], "-", color="#2a9d8f", linewidth=1)
    axarr[0, col].set_title(f"{sid} original + contour", fontsize=10)

    # EFD reconstruction via pyefd (10 harmonics, un-normalised for reconstruction)
    coeffs = pyefd.elliptic_fourier_descriptors(cxy, order=10, normalize=False)
    locus = pyefd.calculate_dc_coefficients(cxy)
    recon = pyefd.reconstruct_contour(coeffs, locus=locus, num_points=400)
    axarr[1, col].imshow(1 - lb, cmap="gray")
    axarr[1, col].plot(recon[:, 0], recon[:, 1], "-", color="#c14545", linewidth=1.5)
    axarr[1, col].set_title(f"EFD reconstruction (10 h)", fontsize=10)

    for r_ in [0, 1]:
        axarr[r_, col].set_xticks([]); axarr[r_, col].set_yticks([])

plt.tight_layout()
plt.savefig(FIGS / "validation_efd_fixed.png", dpi=180,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'validation_efd_fixed.png'}")
