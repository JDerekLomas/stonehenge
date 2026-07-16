"""Figure and paper-ready summary of the multi-class comparison."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent.parent
CORPUS = ROOT / "data" / "multiclass_corpus"
FIGS = ROOT / "figures"

assignments = pd.read_csv(CORPUS / "multiclass_assignments.csv")
counts = assignments["multiclass_nearest"].value_counts()
n = len(assignments)

# =============================================================
# Figure 1: assignment bar chart with class exemplar silhouettes
# =============================================================
class_order = ["mushroom", "tree", "random", "human", "axe", "halberd", "sickle"]
colors = {
    "axe": "#4a6fa5", "mushroom": "#c14545",
    "tree": "#2a9d8f", "human": "#c69950",
    "halberd": "#8f4a8f", "sickle": "#a06a3f",
    "random": "#808080",
}

fig, ax = plt.subplots(figsize=(10, 5.5))
vals = [counts.get(c, 0) for c in class_order]
pcts = [100 * v / n for v in vals]
bars = ax.bar(range(len(class_order)), vals,
              color=[colors[c] for c in class_order],
              edgecolor="white", linewidth=0.8)
for b, v, p in zip(bars, vals, pcts):
    ax.text(b.get_x() + b.get_width()/2, v + 1,
            f"{v}\n({p:.0f}%)", ha="center", fontsize=9)
ax.set_xticks(range(len(class_order)))
ax.set_xticklabels(class_order, fontsize=11)
ax.set_ylabel(f"Carvings assigned (of {n}) by nearest centroid", fontsize=11)
ax.set_title(
    "7-way nearest-centroid classification. Reference classes: axes and mushrooms\n"
    "(real silhouettes), plus halberd, sickle, tree, human, and random prototypes (20 each).\n"
    f"Mushroom is the largest single class; only {counts.get('axe',0)} of {n} carvings assign to axe.",
    fontsize=10.5, pad=10
)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "multiclass_assignments.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'multiclass_assignments.png'}")


# =============================================================
# Figure 2: prototype silhouettes — 3 examples per class
# =============================================================
proto_classes = ["halberd", "sickle", "tree", "human", "random"]
fig, axarr = plt.subplots(len(proto_classes), 3, figsize=(6, 2*len(proto_classes)))
for r, cls in enumerate(proto_classes):
    for c in range(3):
        p = CORPUS / cls / f"{cls}_{c:03d}.png"
        if p.exists():
            arr = np.asarray(Image.open(p).convert("L"))
            # Show black shape on white
            axarr[r, c].imshow(255 - arr, cmap="gray")
        axarr[r, c].set_xticks([]); axarr[r, c].set_yticks([])
        for s in axarr[r, c].spines.values():
            s.set_color("#d6d3d1"); s.set_linewidth(0.6)
        if c == 0:
            axarr[r, c].set_ylabel(cls, fontsize=11, rotation=0,
                                   labelpad=45, ha="right", va="center")

fig.suptitle("Prototype reference silhouettes for the alternative classes",
             fontsize=11, y=0.995)
plt.tight_layout()
plt.savefig(FIGS / "multiclass_prototypes.png", dpi=180,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {FIGS / 'multiclass_prototypes.png'}")
