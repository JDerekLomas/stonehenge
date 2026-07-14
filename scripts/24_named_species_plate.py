"""
Definitive comparison plate using LABELED silhouettes:
  - 4 named psilocybin mushroom species (A. muscaria, Psilocybe coronilla,
    P. subviscida, Stropharia aeruginosa)
  - 8 named Needham axe references (spanning Class 2-5 forms)
  - 8 representative Stonehenge carvings (sorted by cap-shape prominence)

The named labels let a reader identify which specific mushroom or axe
form each visual reference corresponds to. Ideal for the paper's key figure.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from pathlib import Path
from PIL import Image, ImageOps
from skimage import measure

ROOT = Path(__file__).parent.parent
LAB_AX = ROOT / "data" / "extracted_images" / "axes_labeled"
LAB_MUS = ROOT / "data" / "extracted_images" / "mushrooms_labeled"
CARV_SRC = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
FIGS = ROOT / "figures"


def load_thumb(src, size=240):
    """Load an image, extract silhouette, center on white canvas."""
    img = Image.open(src).convert("L")
    arr = np.asarray(img)
    dark = (arr < 128).astype(np.uint8)
    light = (arr >= 128).astype(np.uint8)
    def edge(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    shape = dark if edge(dark) < edge(light) else light
    if shape.sum() == 0:
        return None
    ys, xs = np.where(shape)
    minr, maxr = ys.min(), ys.max()+1
    minc, maxc = xs.min(), xs.max()+1
    pad = int(0.10 * max(maxr-minr, maxc-minc))
    minr = max(0, minr-pad); maxr = min(shape.shape[0], maxr+pad)
    minc = max(0, minc-pad); maxc = min(shape.shape[1], maxc+pad)
    crop = shape[minr:maxr, minc:maxc]
    h, w = crop.shape
    scale = (size*0.85) / max(h, w)
    im = Image.fromarray((crop*255).astype(np.uint8), mode="L").resize(
        (max(1,int(w*scale)), max(1,int(h*scale))), Image.LANCZOS)
    im = im.point(lambda v: 255 if v>127 else 0)
    im = ImageOps.invert(im.convert("L"))
    canvas = Image.new("L", (size, size), 255)
    canvas.paste(im, ((size-im.width)//2, (size-im.height)//2))
    return np.asarray(canvas)


# Named mushrooms
mushrooms = [
    ("Amanita muscaria", "Amanita_Muscaria.jpg"),
    ("Psilocybe coronilla", "Psilocybe_Coronilla.jpg"),
    ("Psilocybe subviscida", "Psilocybe_Subviscida.jpg"),
    ("Stropharia aeruginosa", "Stropharia_Aeruginosa.jpg"),
]

# Named Needham axes — pick a range from Class 2-5
axes_named = [
    ("Needham 2\n(Class 2A)", "axe_2.0.jpg"),
    ("Needham 21\n(Class 2B)", "axe_21.0.jpg"),
    ("Needham 42\n(Class 3)", "axe_42.0.jpg"),
    ("Needham 77\n(Class 4)", "axe_77.0.jpg"),
    ("Needham 85\n(Class 5A)", "axe_85.0.jpg"),
    ("Needham 91\n(Class 5C)", "axe_91.0.jpg"),
    ("Needham 96\n(Class 5D)", "axe_96.0.jpg"),
    ("Needham 109\n(Late)", "axe_109.0.jpg"),
]

# Representative carvings — pick a range across the classifier posterior
carvings = [
    ("F630", "F630.tif"),
    ("F601", "F601.tif"),
    ("F596", "F596.tif"),
    ("F597", "F597.tif"),
    ("F595", "F595.tif"),
    ("F614", "F614.tif"),
    ("F607", "F607.tif"),
    ("F634", "F634.tif"),
]

fig, axarr = plt.subplots(3, 8, figsize=(15, 6.5),
                          gridspec_kw={"hspace": 0.35, "wspace": 0.15})

# Row 1: mushrooms (only 4 named species; pad with empty)
for i, (label, fname) in enumerate(mushrooms):
    ax = axarr[0, i*2]  # spread across positions 0,2,4,6
    src = LAB_MUS / fname
    if src.exists():
        thumb = load_thumb(src)
        if thumb is not None: ax.imshow(thumb, cmap="gray")
    ax.set_title(label, fontsize=9, color="#7cae5a", pad=4)
for i in range(1, 8, 2):
    axarr[0, i].axis("off")
axarr[0, 0].set_ylabel("Native British\npsilocybin mushrooms",
                       fontsize=10, color="#5a8035", fontweight="bold",
                       rotation=0, labelpad=90, ha="center", va="center")

# Row 2: axes
for i, (label, fname) in enumerate(axes_named):
    ax = axarr[1, i]
    src = LAB_AX / fname
    if src.exists():
        thumb = load_thumb(src)
        if thumb is not None: ax.imshow(thumb, cmap="gray")
    ax.set_title(label, fontsize=8.5, color="#4a6fa5", pad=4)
axarr[1, 0].set_ylabel("British Early Bronze Age\naxeheads (Needham 1983)",
                       fontsize=10, color="#3b5678", fontweight="bold",
                       rotation=0, labelpad=90, ha="center", va="center")

# Row 3: carvings
for i, (label, fname) in enumerate(carvings):
    ax = axarr[2, i]
    src = CARV_SRC / fname
    if src.exists():
        thumb = load_thumb(src)
        if thumb is not None: ax.imshow(thumb, cmap="gray")
    ax.set_title(label, fontsize=9, color="#c14545", pad=4)
axarr[2, 0].set_ylabel("Stonehenge\ncarvings (Stone 53)",
                       fontsize=10, color="#8f2b2b", fontweight="bold",
                       rotation=0, labelpad=90, ha="center", va="center")

for ax in axarr.ravel():
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#d6d3d1"); s.set_linewidth(0.8)

# Color-code the row spines
for r, color in enumerate(["#7cae5a", "#4a6fa5", "#c14545"]):
    for c in range(8):
        for s in axarr[r, c].spines.values():
            s.set_color(color); s.set_linewidth(1.6)

fig.suptitle(
    "Named comparison: native British psilocybin mushrooms, canonical Needham axeheads, "
    "and Stonehenge carvings",
    fontsize=12, y=0.99
)
plt.tight_layout(rect=[0.06, 0, 1, 0.97])
plt.savefig(FIGS / "named_species_plate.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"Wrote {FIGS / 'named_species_plate.png'}")
