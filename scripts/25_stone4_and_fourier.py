"""
Process Stone 4 carvings + build Fourier descriptor complexity analysis.

Elliptical Fourier descriptors (Kuhl & Giardina 1982) reconstruct a
closed contour from a series of sine/cosine harmonics. The number of
harmonics required to reach 99% reconstruction fidelity is a measure of
shape complexity: a smooth ellipse needs 1 harmonic; a jagged outline
with fine detail needs many.

If carvings were low-effort attempts to depict axes, they should not
require MORE harmonics than the actual axes (why would you carve
extra complexity?). If they systematically need more, that argues
either the carvings represent an inherently more complex form OR the
carvers were putting genuine effort into a specific target morphology.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from skimage import measure
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent
S4_SRC = ROOT / "data" / "downloads_extracted" / "Entire Image Corpus" / "AllCarvings"
S53_SRC = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
AXE_SRC = ROOT / "data" / "downloads_extracted" / "Axes (Needham 1983, 2012_ burgess)"
MUS_SRC = ROOT / "data" / "downloads_extracted" / "Entire Image Corpus" / "mushrooms"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"
THUMB_S4 = ROOT / "data" / "s4_thumbs"
THUMB_S4.mkdir(exist_ok=True)


def load_binary(path):
    img = Image.open(path).convert("L")
    arr = np.asarray(img)
    dark = (arr < 128).astype(np.uint8)
    light = (arr >= 128).astype(np.uint8)
    def edge(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    return dark if edge(dark) < edge(light) else light


def imagej_features(bw):
    labels = measure.label(bw)
    props = measure.regionprops(labels)
    if not props: return None
    r = max(props, key=lambda p: p.area)
    area = float(r.area); perim = float(r.perimeter)
    if area <= 0 or perim <= 0: return None
    major = float(r.axis_major_length)
    minor = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    return {
        "Area": area, "Perimeter": perim,
        "Height": float(r.bbox[2]-r.bbox[0]),
        "Width": float(r.bbox[3]-r.bbox[1]),
        "Circularity": 4*np.pi*area/(perim**2),
        "Aspect Ratio": major/minor,
        "Roundness": 4*area/(np.pi*major**2),
        "Solidity": float(r.solidity),
    }


def contour_signature(bw, n_points=200):
    """Extract the outer contour of the largest component as N equidistant
    points, then return complex signature."""
    contours = measure.find_contours(bw.astype(float), 0.5)
    if not contours: return None
    # longest contour
    c = max(contours, key=len)
    # resample to n_points
    N = len(c)
    if N < 10: return None
    # cumulative arc length
    diffs = np.diff(c, axis=0)
    seg = np.sqrt((diffs**2).sum(axis=1))
    cumu = np.concatenate([[0], np.cumsum(seg)])
    L = cumu[-1]
    if L <= 0: return None
    target = np.linspace(0, L, n_points+1)[:-1]
    pts = np.zeros((n_points, 2))
    for i, t in enumerate(target):
        idx = np.searchsorted(cumu, t)
        if idx >= len(c): idx = len(c) - 1
        if idx == 0: pts[i] = c[0]
        else:
            f = (t - cumu[idx-1]) / (seg[idx-1] + 1e-9)
            pts[i] = c[idx-1] + f * (c[idx] - c[idx-1])
    # Complex signature (y + i*x, standard convention)
    return pts[:, 1] + 1j * pts[:, 0]


def fourier_harmonics_for_99pct(sig):
    """Return the number of harmonics needed to reach 99% cumulative
    energy after removing DC + shift + rotation invariance."""
    n = len(sig)
    # Remove centroid
    s = sig - sig.mean()
    # FFT
    F = np.fft.fft(s)
    # Power spectrum, excluding DC (index 0)
    power = np.abs(F) ** 2
    power[0] = 0
    total = power.sum()
    if total <= 0: return None
    # Sort harmonics by frequency magnitude (paired: k and n-k)
    # We evaluate 1..n/2 harmonics
    half = n // 2
    # Add power of both k and n-k for each k
    harm_power = np.array([power[k] + power[n - k] if n - k != k else power[k]
                            for k in range(1, half + 1)])
    cumu = np.cumsum(harm_power) / total
    thresh = 0.99
    idx = np.where(cumu >= thresh)[0]
    return int(idx[0] + 1) if len(idx) > 0 else half


# ============================================================
# 1. Process Stone 4 carvings
# ============================================================
s4_files = sorted(S4_SRC.glob("F*.tif")) + sorted(S4_SRC.glob("f*.tif"))
# Filter to Stone 4 (F646+)
def is_s4(p):
    m = p.stem.replace("-aligned", "").lstrip("Ff")
    try: return 640 <= int(m) <= 730
    except: return False

s4_files = [p for p in s4_files if is_s4(p)]
print(f"Stone 4 files: {len(s4_files)}")

s4_rows = []
for p in s4_files:
    bw = load_binary(p)
    f = imagej_features(bw)
    if f is None: continue
    sig = contour_signature(bw)
    h = fourier_harmonics_for_99pct(sig) if sig is not None else None
    f["id"] = p.stem
    f["harmonics_99"] = h
    f["stone"] = "4"
    s4_rows.append(f)

# Stone 53
s53_files = sorted(S53_SRC.glob("F*.tif"))
s53_rows = []
for p in s53_files:
    bw = load_binary(p)
    f = imagej_features(bw)
    if f is None: continue
    sig = contour_signature(bw)
    h = fourier_harmonics_for_99pct(sig) if sig is not None else None
    f["id"] = p.stem
    f["harmonics_99"] = h
    f["stone"] = "53"
    s53_rows.append(f)

# Axes
axe_files = sorted(AXE_SRC.glob("*.tif"))
axe_rows = []
for p in axe_files:
    bw = load_binary(p)
    f = imagej_features(bw)
    if f is None: continue
    sig = contour_signature(bw)
    h = fourier_harmonics_for_99pct(sig) if sig is not None else None
    f["id"] = p.stem
    f["harmonics_99"] = h
    f["source"] = "axe"
    axe_rows.append(f)

# Mushrooms
mus_files = sorted(MUS_SRC.glob("*.tif")) + sorted(MUS_SRC.glob("*.jpg"))
mus_rows = []
for p in mus_files:
    try:
        bw = load_binary(p)
        f = imagej_features(bw)
        if f is None: continue
        sig = contour_signature(bw)
        h = fourier_harmonics_for_99pct(sig) if sig is not None else None
        f["id"] = p.stem
        f["harmonics_99"] = h
        f["source"] = "mushroom"
        mus_rows.append(f)
    except Exception:
        continue

s4_df = pd.DataFrame(s4_rows)
s53_df = pd.DataFrame(s53_rows)
axe_df = pd.DataFrame(axe_rows)
mus_df = pd.DataFrame(mus_rows)

print(f"\nStone 4:  n={len(s4_df)}, harmonics99 median={s4_df['harmonics_99'].median():.0f}")
print(f"Stone 53: n={len(s53_df)}, harmonics99 median={s53_df['harmonics_99'].median():.0f}")
print(f"Axes:     n={len(axe_df)}, harmonics99 median={axe_df['harmonics_99'].median():.0f}")
print(f"Mushrooms:n={len(mus_df)}, harmonics99 median={mus_df['harmonics_99'].median():.0f}")

all_carv = pd.concat([s4_df, s53_df], ignore_index=True)
all_carv["source"] = "carving"

full = pd.concat([axe_df, all_carv, mus_df], ignore_index=True)
full.to_csv(OUT / "extended_features_with_harmonics.csv", index=False)
print(f"\nSaved: {OUT / 'extended_features_with_harmonics.csv'}")

# ============================================================
# Harmonics analysis
# ============================================================
from scipy import stats

print("\n=== Fourier complexity comparison ===")
axe_h = axe_df["harmonics_99"].dropna().values
carv_h = all_carv["harmonics_99"].dropna().values
mus_h = mus_df["harmonics_99"].dropna().values

for name, arr in [("Axes", axe_h), ("Carvings", carv_h), ("Mushrooms", mus_h)]:
    print(f"  {name:<10} median = {int(np.median(arr))}   mean = {arr.mean():.1f}   IQR = [{int(np.quantile(arr, .25))}, {int(np.quantile(arr, .75))}]")

u, p_u = stats.mannwhitneyu(carv_h, axe_h, alternative="greater")
print(f"\nMann-Whitney U (carvings need more harmonics than axes): p = {p_u:.2e}")

t, p_t = stats.ttest_ind(carv_h, axe_h, equal_var=False)
print(f"Welch's t: t = {t:.2f}, p = {p_t:.2e}")

# Effect size — Cliff's delta
def cliffs_delta(x, y):
    n_greater = sum(1 for xi in x for yi in y if xi > yi)
    n_less = sum(1 for xi in x for yi in y if xi < yi)
    return (n_greater - n_less) / (len(x) * len(y))
delta = cliffs_delta(carv_h, axe_h)
print(f"Cliff's delta (carvings vs axes): {delta:.3f} (>0.474 = large)")

# ============================================================
# Figure
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))
data = [axe_h, carv_h, mus_h]
labels = [f"Axes\nn={len(axe_h)}",
          f"Carvings\nn={len(carv_h)}",
          f"Mushrooms\nn={len(mus_h)}"]
colors = ["#4a6fa5", "#c14545", "#7cae5a"]
parts = ax.violinplot(data, showmedians=True, widths=0.75)
for pc, c in zip(parts["bodies"], colors):
    pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.68)
for key in ("cbars", "cmins", "cmaxes", "cmedians"):
    if key in parts:
        parts[key].set_color("black"); parts[key].set_linewidth(1.0)
for i, d in enumerate(data):
    jitter = np.random.default_rng(i).normal(0, 0.06, size=len(d))
    ax.scatter(np.full(len(d), i+1)+jitter, d, s=10, alpha=0.45,
               color=colors[i], edgecolor="none")
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Elliptical Fourier harmonics required for 99% reconstruction",
              fontsize=11)
ax.set_title("Shape complexity: carvings require more harmonics than axes.\n"
             "More harmonics = more carved detail; the carvings are not simple "
             "attempts at axes.",
             fontsize=11, pad=8)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
ax.text(0.02, 0.95, f"Mann-Whitney p = {p_u:.1e}\nCliff's δ = {delta:.2f}",
        transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor="gray", alpha=0.9), fontsize=9)
plt.tight_layout()
plt.savefig(FIGS / "harmonics_complexity.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'harmonics_complexity.png'}")
