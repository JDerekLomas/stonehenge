"""
Combined Stone 4 + Stone 53 atlas — 99 real Stonehenge carving silhouettes
sorted by aspect ratio. This is now most of the 115 carvings that exist
across the whole monument.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIGS = ROOT / "figures"
S53_THUMBS = ROOT / "data" / "carving_thumbs"
S4_THUMBS = ROOT / "data" / "stone4_extracted" / "thumbs"
S4_CSV = ROOT / "data" / "stone4_extracted" / "stone4_features.csv"

# Get all thumbnails with their AR
s53 = pd.read_csv(ROOT / "data" / "raw" / "rock_carvings_and_axeheads.csv")
s53 = s53[s53["Stone"] == 53].dropna(subset=["Aspect Ratio"])
s53_items = [(f"F{int(r['Carving#'])}", r["Aspect Ratio"], "53")
              for _, r in s53.iterrows()]

s4 = pd.read_csv(S4_CSV)
s4_items = [(r["id"], r["Aspect Ratio"], "4") for _, r in s4.iterrows()]

all_items = sorted(s53_items + s4_items, key=lambda x: x[1])
print(f"Total: {len(s53_items)} S53 + {len(s4_items)} S4 = {len(all_items)}")

def thumb_path(id_str, stone):
    if stone == "53":
        return S53_THUMBS / f"{id_str}.png"
    return S4_THUMBS / f"{id_str}.png"

cols = 11
rows = int(np.ceil(len(all_items) / cols))
fig, axarr = plt.subplots(rows, cols, figsize=(cols * 1.3, rows * 1.45))
axarr = np.array(axarr).reshape(rows, cols)

for i in range(rows * cols):
    r_, c_ = i // cols, i % cols
    ax = axarr[r_, c_]
    if i >= len(all_items):
        ax.axis("off"); continue
    id_str, ar, stone = all_items[i]
    p = thumb_path(id_str, stone)
    if p.exists():
        ax.imshow(imread(str(p)), cmap="gray")
    color = "#c14545" if stone == "53" else "#e07a2b"
    for s in ax.spines.values():
        s.set_color(color); s.set_linewidth(1.1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{id_str}   AR {ar:.2f}", fontsize=6.5, pad=2)

fig.suptitle(
    f"All {len(all_items)} extractable Stonehenge carvings, sorted by aspect ratio "
    f"(red = Stone 53, orange = Stone 4)",
    fontsize=12, y=0.998
)
plt.tight_layout(rect=[0, 0, 1, 0.985])
plt.savefig(FIGS / "all_stonehenge_atlas.png", dpi=170,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Wrote {FIGS / 'all_stonehenge_atlas.png'}")
