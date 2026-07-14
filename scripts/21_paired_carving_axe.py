"""
Paired figure: for each of 8 representative Stone 53 carvings, show it
side by side with its nearest neighbor axe in the ShapeComp perceptual
embedding.

If the axehead identification were correct, the "nearest axe" for each
carving should look at least somewhat like the carving. In practice they
don't — the shape difference is objectively visible.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIGS = ROOT / "figures"
OUT = ROOT / "data" / "processed"

# Load the mapping
pairs = pd.read_csv(OUT / "shapecomp_carving_nearest_axe.csv")

# Carving thumbnails come from data/clean_thumbs/carving/
CARV_THUMB = ROOT / "data" / "clean_thumbs" / "carving"
AXE_THUMB = ROOT / "data" / "clean_thumbs" / "axe"

# Sort by nearest-axe-distance ascending — start with the "easiest" pairs
# and end with the hardest
pairs = pairs.sort_values("nearest_axe_dist").reset_index(drop=True)

# Pick 4 with smallest distances (best axe match) and 4 with largest (worst)
best = pairs.head(4)
worst = pairs.tail(4).iloc[::-1]

def find_thumb(directory, base):
    """Some IDs have variants; find the closest match."""
    for suffix in [".png"]:
        p = directory / (base + suffix)
        if p.exists(): return p
    # Try substring match
    for p in directory.glob("*.png"):
        if base.lower() in p.stem.lower() or p.stem.lower() in base.lower():
            return p
    return None

fig, axarr = plt.subplots(4, 4, figsize=(11, 11.5))

def render_pair(row_idx_top, row_data, ax_col_offset, label_color):
    for i, (_, r) in enumerate(row_data.iterrows()):
        row = row_idx_top + i // 2
        col = ax_col_offset + (i % 2) * 2
        # carving
        ct = find_thumb(CARV_THUMB, r["short_id"])
        if ct: axarr[row, col].imshow(imread(str(ct)), cmap="gray")
        axarr[row, col].set_title(f"Carving {r['short_id']}",
                                    fontsize=9, color="#c14545", pad=4)
        # axe
        at = find_thumb(AXE_THUMB, r["nearest_axe_id"])
        if at: axarr[row, col+1].imshow(imread(str(at)), cmap="gray")
        axarr[row, col+1].set_title(f"nearest axe: {r['nearest_axe_id']}",
                                      fontsize=9, color="#4a6fa5", pad=4)
        for j in (col, col+1):
            axarr[row, j].set_xticks([]); axarr[row, j].set_yticks([])
            for s in axarr[row, j].spines.values():
                s.set_color("#d6d3d1"); s.set_linewidth(0.8)
        # add distance label under the pair
        axarr[row, col].text(1.0, -0.11, f"ShapeComp distance: {r['nearest_axe_dist']:.2f}",
                              transform=axarr[row, col].transAxes,
                              ha="center", va="top", fontsize=8, color="#57534e")

# Grid: 4 rows × 4 cols
# Rows 0-1: best (2 pairs per row)
# Rows 2-3: worst (2 pairs per row)
render_pair(0, best, 0, "#4a6fa5")
render_pair(2, worst, 0, "#4a6fa5")

# Row labels
fig.text(0.005, 0.75, "Best carving-to-axe matches\n(smallest distance)",
         rotation=90, ha="center", va="center", fontsize=10.5,
         fontweight="bold", color="#0f5132")
fig.text(0.005, 0.28, "Worst carving-to-axe matches\n(largest distance)",
         rotation=90, ha="center", va="center", fontsize=10.5,
         fontweight="bold", color="#712f2f")

fig.suptitle(
    "Each Stone 53 carving next to its nearest-neighbour axe in the ShapeComp "
    "perceptual embedding.\nEven the best matches are not close.",
    fontsize=11.5, y=1.005,
)
plt.tight_layout(rect=[0.03, 0, 1, 0.98])
plt.savefig(FIGS / "paired_carving_nearest_axe.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Wrote {FIGS / 'paired_carving_nearest_axe.png'}")
