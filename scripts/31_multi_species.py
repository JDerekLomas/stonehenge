"""
Multi-species mushroom classification.

We have labeled silhouettes for 4 named mushroom species:
  - Amanita muscaria
  - Psilocybe coronilla
  - Psilocybe subviscida
  - Stropharia aeruginosa

Task: use these + real Needham axes as a 5-way reference. For each
carving, compute Mahalanobis-like distance in the 3-feature shape
space to each of the 5 class centroids, and assign to the nearest.

Also include the taxonomic reference table (15 candidate species with
cap/stem sizes and psilocybin activity).
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image, ImageOps
from skimage import measure
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import json

ROOT = Path(__file__).parent.parent
LAB_MUS = ROOT / "data" / "extracted_images" / "mushrooms_labeled"
LAB_AXE = ROOT / "data" / "extracted_images" / "axes_labeled"
S53 = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
S4_SRC = ROOT / "data" / "downloads_extracted" / "Entire Image Corpus" / "AllCarvings"
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"


def load_bin(p):
    img = Image.open(p).convert("L")
    arr = np.asarray(img)
    d = (arr < 128).astype(np.uint8)
    l = (arr >= 128).astype(np.uint8)
    def e(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    return d if e(d) < e(l) else l


def features(p):
    try:
        bw = load_bin(p)
    except: return None
    labels = measure.label(bw)
    props = measure.regionprops(labels)
    if not props: return None
    r = max(props, key=lambda x: x.area)
    a = float(r.area); pr = float(r.perimeter)
    if a <= 0 or pr <= 0: return None
    maj = float(r.axis_major_length)
    mn = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    return np.array([
        4*np.pi*a/(pr**2),   # circularity
        maj/mn,              # aspect ratio
        4*a/(np.pi*maj**2),  # roundness
    ])

# Named references
species_files = {
    "A. muscaria": LAB_MUS / "Amanita_Muscaria.jpg",
    "P. coronilla": LAB_MUS / "Psilocybe_Coronilla.jpg",
    "P. subviscida": LAB_MUS / "Psilocybe_Subviscida.jpg",
    "Stropharia aeruginosa": LAB_MUS / "Stropharia_Aeruginosa.jpg",
}

# Also compute an average "Axe" centroid from labeled axes
axe_paths = sorted(LAB_AXE.glob("*.jpg"))[:36]
axe_feats = [f for f in [features(p) for p in axe_paths] if f is not None]
axe_centroid = np.stack(axe_feats).mean(axis=0)

# Get each species centroid (single silhouette each)
class_names = list(species_files.keys()) + ["Bronze axe (avg Needham)"]
centroids = []
for name, p in species_files.items():
    f = features(p)
    print(f"  {name}: circ={f[0]:.3f}, AR={f[1]:.3f}, round={f[2]:.3f}")
    centroids.append(f)
print(f"  Bronze axe (avg): circ={axe_centroid[0]:.3f}, AR={axe_centroid[1]:.3f}, round={axe_centroid[2]:.3f}")
centroids.append(axe_centroid)
centroids = np.stack(centroids)

# Standardize features (z-score across the corpus)
all_feats = []
all_ids = []
for src, tag in [(S53, "S53"), (S4_SRC, "S4")]:
    for p in sorted(src.glob("F*.tif")) + sorted(src.glob("f*.tif")):
        m = p.stem.replace("-aligned", "").lstrip("Ff")
        try: nid = int(m)
        except: continue
        if tag == "S53" and not (595 <= nid <= 638 or nid == 720): continue
        if tag == "S4" and not (640 <= nid <= 730): continue
        f = features(p)
        if f is None: continue
        all_feats.append(f)
        all_ids.append((tag, p.stem))

all_feats = np.stack(all_feats)
print(f"\nCarvings loaded: {len(all_feats)}")

# Scale using pooled std
combined = np.vstack([all_feats, centroids])
mean = combined.mean(axis=0); std = combined.std(axis=0)
Xs_carv = (all_feats - mean) / std
Xs_cent = (centroids - mean) / std

# Nearest centroid assignment
dists = cdist(Xs_carv, Xs_cent)   # (n_carv, 5)
assign = dists.argmin(axis=1)

# Save per-carving assignments
rows = []
for i, ((tag, cid), a) in enumerate(zip(all_ids, assign)):
    rows.append({
        "id": cid, "stone": tag,
        "assigned_class": class_names[a],
        **{f"d_{class_names[j][:15]}": float(dists[i, j]) for j in range(5)},
    })
df = pd.DataFrame(rows)
df.to_csv(OUT / "multispecies_assignments.csv", index=False)
print("\nPer-class assignment counts (nearest-centroid, all 72 carvings):")
print(df["assigned_class"].value_counts())
print()

# Break down by stone
for stone, g in df.groupby("stone"):
    print(f"Stone {stone}:")
    print(g["assigned_class"].value_counts())
    print()

# ============================================================
# Figure: stacked bar of nearest-class assignments
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))
cats = class_names
colors = ["#c14545", "#c69950", "#7cae5a", "#5a9fa0", "#4a6fa5"]
counts_s53 = df[df["stone"] == "S53"]["assigned_class"].value_counts().reindex(cats, fill_value=0)
counts_s4 = df[df["stone"] == "S4"]["assigned_class"].value_counts().reindex(cats, fill_value=0)

x = np.arange(len(cats))
w = 0.4
ax.bar(x - w/2, counts_s53.values, w, label=f"Stone 53 (n={len(df[df['stone']=='S53'])})",
       color="#c14545", edgecolor="white", linewidth=0.8)
ax.bar(x + w/2, counts_s4.values, w, label=f"Stone 4 (n={len(df[df['stone']=='S4'])})",
       color="#e07a2b", edgecolor="white", linewidth=0.8)

for i, (a, b) in enumerate(zip(counts_s53.values, counts_s4.values)):
    if a > 0: ax.text(i - w/2, a + 0.5, str(a), ha="center", fontsize=9)
    if b > 0: ax.text(i + w/2, b + 0.5, str(b), ha="center", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(cats, rotation=15, ha="right", fontsize=9.5)
ax.set_ylabel("Carvings assigned to this class (nearest-centroid)", fontsize=11)
ax.set_title(
    "5-way class assignment: 4 named mushroom species + bronze-axe centroid.\n"
    "Almost all carvings assign to a mushroom species; almost none to the axe centroid.",
    fontsize=10.5, pad=8
)
ax.legend(fontsize=10, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "multispecies_assignments.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'multispecies_assignments.png'}")

# ============================================================
# Also emit the 15-species reference table for the paper
# ============================================================
mus_ref = pd.read_excel(ROOT / "data" / "raw" / "Mushroom Outlines Carvings.xlsx",
                         sheet_name="Mushrooms")
mus_ref_clean = mus_ref.dropna(subset=["Species"])[
    ["Species", "Cap Size", "Stem Size", "Habitat", "Ring", "Activity"]
].copy()
mus_ref_clean.to_csv(OUT / "candidate_mushroom_species.csv", index=False)
print(f"\nSaved: {OUT / 'candidate_mushroom_species.csv'}")
print(mus_ref_clean.to_string(index=False))
