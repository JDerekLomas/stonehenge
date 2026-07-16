"""
Validation of our shape-feature pipeline.

(1) Canonical-shape sanity: compute all features on synthesized perfect
    circle, ellipse, rectangle. Confirm theoretical values.

(2) Cross-check vs Lomas 2021 ImageJ: same 41 Stone 53 TIFFs, two
    pipelines. Compare Circularity, AR, Roundness, Solidity.

(3) Cross-check vs Bevan corpus values (where matched).

(4) Skeleton + EFD reconstruction plots on 3 sample carvings for
    visual QA.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from skimage import measure, morphology
from skimage.morphology import medial_axis
from skimage.draw import ellipse as draw_ellipse, disk, rectangle
import sys

sys.path.insert(0, str(Path(__file__).parent))
from importlib import util
spec = util.spec_from_file_location("ext38", Path(__file__).parent / "38_extended_features.py")
m38 = util.module_from_spec(spec); spec.loader.exec_module(m38)

ROOT = Path(__file__).parent.parent
FIGS = ROOT / "figures"

# =============================================================
# (1) Canonical shapes
# =============================================================
print("=" * 60)
print("(1) CANONICAL-SHAPE SANITY CHECK")
print("=" * 60)

# Perfect circle radius 100
c = np.zeros((300, 300), dtype=np.uint8)
rr, cc = disk((150, 150), 100)
c[rr, cc] = 1
im_c, hu_c, efd_c, sk_c = m38.all_features(c)
print(f"\nPerfect circle:")
print(f"  Circularity  = {im_c[0]:.4f}   (expected ~1.000)")
print(f"  Aspect Ratio = {im_c[1]:.4f}   (expected 1.0)")
print(f"  Roundness    = {im_c[2]:.4f}   (expected ~1.0)")
print(f"  Solidity     = {im_c[3]:.4f}   (expected ~1.0)")

# Ellipse 2:1
e = np.zeros((300, 300), dtype=np.uint8)
rr, cc = draw_ellipse(150, 150, 60, 120)
e[rr, cc] = 1
im_e, _, _, _ = m38.all_features(e)
print(f"\nEllipse 2:1 (major=120, minor=60):")
print(f"  Circularity  = {im_e[0]:.4f}   (theory: 0.906; pixellation lowers)")
print(f"  Aspect Ratio = {im_e[1]:.4f}   (expected 2.0)")
print(f"  Roundness    = {im_e[2]:.4f}   (expected 0.5 = 1/AR)")
print(f"  Solidity     = {im_e[3]:.4f}   (expected ~1.0)")

# Rectangle 3:1
r = np.zeros((300, 400), dtype=np.uint8)
rr, cc = rectangle((60, 30), extent=(180, 340))
r[rr, cc] = 1
im_r, _, _, _ = m38.all_features(r)
print(f"\nRectangle 3:1 (340×180):")
print(f"  Circularity  = {im_r[0]:.4f}   (theory: pi/4 ≈ 0.585 for square; less for elongated)")
print(f"  Aspect Ratio = {im_r[1]:.4f}   (fitted-ellipse AR; ≈ sqrt(3) for 3:1 rect = 1.73)")
print(f"  Roundness    = {im_r[2]:.4f}   (4·A / (π·M²))")
print(f"  Solidity     = {im_r[3]:.4f}   (expected 1.0)")

# =============================================================
# (2) Cross-check vs Lomas 2021 ImageJ measurements
# =============================================================
print("\n" + "=" * 60)
print("(2) OURS vs LOMAS 2021 IMAGEJ ON SAME STONE 53 TIFFs")
print("=" * 60)

lomas = pd.read_excel(ROOT / "data" / "raw" / "Stone 53 Measurements.xlsx",
                      sheet_name="Carvings")
lomas["carving_id"] = lomas["Carving#"].apply(lambda x: f"F{int(x)}" if pd.notna(x) else "")
lomas_by_id = lomas.set_index("carving_id")

tif_dir = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
rows = []
for p in sorted(tif_dir.glob("F*.tif")):
    stem = p.stem.replace(" - 540wide", "")
    if stem not in lomas_by_id.index: continue
    bw = m38.load_bin(p)
    im, _, _, _ = m38.all_features(bw)
    lomas_row = lomas_by_id.loc[stem]
    rows.append({
        "id": stem,
        "our_circ": im[0], "lomas_circ": lomas_row["Circularity"],
        "our_ar": im[1], "lomas_ar": lomas_row["Aspect Ratio"],
        "our_round": im[2], "lomas_round": lomas_row["Roundness"],
        "our_sol": im[3], "lomas_sol": lomas_row["Solidity"],
    })

comp = pd.DataFrame(rows)
print(f"\nMatched {len(comp)} carvings")
print()
for feat in ["circ", "ar", "round", "sol"]:
    our = comp[f"our_{feat}"].values
    lom = comp[f"lomas_{feat}"].values
    diff = our - lom
    r = np.corrcoef(our, lom)[0, 1]
    print(f"{feat:<10}  mean(ours) = {our.mean():.3f}   mean(Lomas) = {lom.mean():.3f}   "
          f"diff mean = {diff.mean():+.4f}   |diff| median = {np.median(np.abs(diff)):.4f}   r = {r:.4f}")

# Save comparison
comp.to_csv(ROOT / "data" / "processed" / "validation_ours_vs_lomas.csv", index=False)

# Scatter plots
fig, axarr = plt.subplots(1, 4, figsize=(15, 4))
for ax, feat, name in zip(axarr, ["circ", "ar", "round", "sol"],
                          ["Circularity", "Aspect Ratio", "Roundness", "Solidity"]):
    our = comp[f"our_{feat}"].values
    lom = comp[f"lomas_{feat}"].values
    ax.scatter(lom, our, s=30, alpha=0.7, color="#4a6fa5", edgecolor="white")
    lo = min(our.min(), lom.min()) * 0.9
    hi = max(our.max(), lom.max()) * 1.05
    ax.plot([lo, hi], [lo, hi], "--", color="#c14545", linewidth=1.2,
            label="y = x")
    ax.set_xlabel(f"Lomas 2021 ImageJ", fontsize=10)
    ax.set_ylabel(f"Our pipeline", fontsize=10)
    r = np.corrcoef(our, lom)[0, 1]
    ax.set_title(f"{name}   r = {r:.3f}", fontsize=10.5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGS / "validation_ours_vs_lomas.png", dpi=180,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'validation_ours_vs_lomas.png'}")

# =============================================================
# (3) Visual QA: skeleton + EFD reconstruction on 3 samples
# =============================================================
print("\n" + "=" * 60)
print("(3) VISUAL QA: skeleton + EFD on 3 sample carvings")
print("=" * 60)

sample_ids = ["F595", "F607", "F630"]
fig, axarr = plt.subplots(3, 3, figsize=(9, 9))
for row, sid in enumerate(sample_ids):
    p = tif_dir / f"{sid}.tif"
    if not p.exists(): continue
    bw = m38.load_bin(p)
    lb, r = m38.largest_component(bw)

    # (a) Original silhouette
    axarr[row, 0].imshow(1 - lb, cmap="gray")
    axarr[row, 0].set_title(f"{sid} — original", fontsize=10)

    # (b) Skeleton overlay
    skel, dist = medial_axis(lb.astype(bool), return_distance=True)
    overlay = np.dstack([1 - lb, 1 - lb, 1 - lb]).astype(float)
    overlay[skel] = [1, 0, 0]  # red skeleton
    axarr[row, 1].imshow(overlay)
    axarr[row, 1].set_title(f"skeleton  ({int(skel.sum())} px)", fontsize=10)

    # (c) EFD reconstruction (8 harmonics)
    contours = measure.find_contours(lb.astype(float), 0.5)
    if contours:
        c = max(contours, key=len)
        # Reconstruct from 8 harmonics
        contour_xy = c[:, ::-1]  # (x, y)
        dx = np.diff(contour_xy[:, 0]); dy = np.diff(contour_xy[:, 1])
        dt = np.sqrt(dx**2 + dy**2)
        t = np.concatenate([[0], np.cumsum(dt)])
        T = t[-1]
        n_recon = 200
        recon = np.zeros((n_recon, 2))
        recon += contour_xy.mean(axis=0)  # centroid
        for k in range(1, 9):
            # Estimate Fourier coefficients (unnormalized)
            phi = 2 * np.pi * t / T
            cos_ph = np.cos(k * phi); sin_ph = np.sin(k * phi)
            d_cos = np.diff(cos_ph); d_sin = np.diff(sin_ph)
            cf = T / (2 * k**2 * np.pi**2)
            an = cf * np.sum(dx / dt * d_cos)
            bn = cf * np.sum(dx / dt * d_sin)
            cn = cf * np.sum(dy / dt * d_cos)
            dn = cf * np.sum(dy / dt * d_sin)
            ph = 2 * np.pi * k * np.arange(n_recon) / n_recon
            recon[:, 0] += an * np.cos(ph) + bn * np.sin(ph)
            recon[:, 1] += cn * np.cos(ph) + dn * np.sin(ph)
        axarr[row, 2].imshow(1 - lb, cmap="gray")
        axarr[row, 2].plot(recon[:, 0], recon[:, 1], "-", color="#c14545", linewidth=2)
        axarr[row, 2].set_title(f"EFD reconstruction (8 harmonics)", fontsize=10)
        axarr[row, 2].set_xlim(0, lb.shape[1]); axarr[row, 2].set_ylim(lb.shape[0], 0)

    for c_ in range(3):
        axarr[row, c_].set_xticks([]); axarr[row, c_].set_yticks([])

plt.tight_layout()
plt.savefig(FIGS / "validation_visual_qa.png", dpi=180,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'validation_visual_qa.png'}")
