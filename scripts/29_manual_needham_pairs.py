"""
Paired "each carving next to its manually-assigned Needham axe" figure.

Uses the manual mapping from the Stone 53 Measurements sheet's
"Carvings to axes" tab, which for each carving lists a Needham # (the
axe(s) the original researcher hand-picked as the closest match).

The point: even the researcher's OWN best axe match doesn't look like
the carving. Where the manual mapping picks a specific Needham number
(e.g. "93"), we render that axe next to the carving.
"""

import re
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from matplotlib.image import imread
from skimage import measure

ROOT = Path(__file__).parent.parent
LAB_AX = ROOT / "data" / "extracted_images" / "axes_labeled"
CARV_SRC = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
FIGS = ROOT / "figures"


def load_thumb(src, size=240):
    img = Image.open(src).convert("L")
    arr = np.asarray(img)
    dark = (arr < 128).astype(np.uint8)
    light = (arr >= 128).astype(np.uint8)
    def edge(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    shape = dark if edge(dark) < edge(light) else light
    if shape.sum() == 0: return None
    ys, xs = np.where(shape)
    minr, maxr = ys.min(), ys.max()+1
    minc, maxc = xs.min(), xs.max()+1
    pad = int(0.10 * max(maxr-minr, maxc-minc))
    minr = max(0, minr-pad); maxr = min(shape.shape[0], maxr+pad)
    minc = max(0, minc-pad); maxc = min(shape.shape[1], maxc+pad)
    crop = shape[minr:maxr, minc:maxc]
    h, w = crop.shape
    scale = (size*0.85) / max(h, w)
    im = Image.fromarray((crop*255).astype(np.uint8), "L").resize(
        (max(1,int(w*scale)), max(1,int(h*scale))), Image.LANCZOS)
    im = im.point(lambda v: 255 if v>127 else 0)
    im = ImageOps.invert(im.convert("L"))
    canvas = Image.new("L", (size, size), 255)
    canvas.paste(im, ((size-im.width)//2, (size-im.height)//2))
    return np.asarray(canvas)


# Load mapping
xlsx = ROOT / "data" / "raw" / "Stone 53 Measurements.xlsx"
mapping = pd.read_excel(xlsx, sheet_name="Carvings to axes")

# Parse the Needham # column
def parse_needham(v):
    if pd.isna(v): return None
    s = str(v).strip().rstrip("\n").rstrip(",").strip()
    if not s or s.lower() in ("nan",): return None
    # take first token before comma
    tok = s.split(",")[0].strip()
    return tok

mapping["needham_id"] = mapping["Needham #"].apply(parse_needham)
paired = mapping[mapping["needham_id"].notna()].copy()

# Build filename matching
def find_axe_file(nid):
    if not nid: return None
    # Try axe_{nid}.jpg then axe_{nid}.0.jpg
    for cand in [f"axe_{nid}.jpg", f"axe_{nid}.0.jpg",
                 f"axe_{nid.lower()}.jpg", f"axe_{nid.lower()}.0.jpg"]:
        p = LAB_AX / cand
        if p.exists(): return p
    # fuzzy: any file whose stem contains this
    for p in LAB_AX.glob("*"):
        stem_low = p.stem.lower().replace("axe_", "").rstrip("0").rstrip(".")
        nid_low = nid.lower().rstrip("0").rstrip(".")
        if stem_low == nid_low: return p
    return None

paired["axe_file"] = paired["needham_id"].apply(find_axe_file)
paired["carv_file"] = paired["Carving#"].apply(
    lambda c: CARV_SRC / f"F{int(c)}.tif" if pd.notna(c) and (CARV_SRC / f"F{int(c)}.tif").exists() else None
)

# Keep only rows where BOTH files exist
usable = paired[paired["axe_file"].notna() & paired["carv_file"].notna()].reset_index(drop=True)
print(f"Total mappings: {len(paired)}, usable pairs (both files present): {len(usable)}")
print(usable[["Carving#", "needham_id", "Axe type", "Recurve", "Ring"]].to_string(index=False))

# Pick 12 pairs for the figure — spread across recurve/ring status
if len(usable) < 12:
    pairs = usable
else:
    # spread: 4 with recurve, 4 with ring, 4 without
    recurve = usable[usable["Recurve"] == 1].head(4)
    ring = usable[(usable["Ring"] == 1) & (~usable.index.isin(recurve.index))].head(4)
    rest = usable[~usable.index.isin(recurve.index.union(ring.index))].head(4)
    pairs = pd.concat([recurve, ring, rest]).head(12).reset_index(drop=True)

print(f"\nSelected {len(pairs)} pairs for the figure")

# ============================================================
# Figure: 3 columns x 4 rows of pairs (each pair = 2 cells)
# So 12 pairs = 24 cells arranged 6 wide x 4 rows
# Actually simpler: 12 rows x 2 columns (carving + axe)
# ============================================================
n = len(pairs)
cols = 4  # 4 pairs per row
rows = int(np.ceil(n / cols))
fig, axarr = plt.subplots(rows, cols*2, figsize=(cols*4, rows*2.5),
                          gridspec_kw={"wspace": 0.05, "hspace": 0.4})
if rows == 1:
    axarr = np.array([axarr])

for i, (_, r) in enumerate(pairs.iterrows()):
    row = i // cols
    col_offset = (i % cols) * 2
    ct = load_thumb(r["carv_file"])
    at = load_thumb(r["axe_file"])
    if ct is not None:
        axarr[row, col_offset].imshow(ct, cmap="gray")
    axarr[row, col_offset].set_title(f"Carving F{int(r['Carving#'])}",
                                       fontsize=9, color="#c14545", pad=3)
    if at is not None:
        axarr[row, col_offset+1].imshow(at, cmap="gray")
    axarr[row, col_offset+1].set_title(
        f"manual match: Needham {r['needham_id']}",
        fontsize=9, color="#4a6fa5", pad=3
    )
    # Style spines
    for c in (col_offset, col_offset+1):
        axarr[row, c].set_xticks([]); axarr[row, c].set_yticks([])
        for s in axarr[row, c].spines.values():
            s.set_color("#d6d3d1"); s.set_linewidth(0.8)
    for s in axarr[row, col_offset].spines.values():
        s.set_color("#c14545"); s.set_linewidth(1.8)
    for s in axarr[row, col_offset+1].spines.values():
        s.set_color("#4a6fa5"); s.set_linewidth(1.8)

# Hide any leftover cells
total_cells = rows * cols * 2
used_cells = n * 2
for i in range(used_cells, total_cells):
    row = i // (cols*2)
    col = i % (cols*2)
    if row < axarr.shape[0]:
        axarr[row, col].axis("off")

fig.suptitle(
    "Each Stone 53 carving next to the Needham axe manually picked as its closest match.\n"
    "Even the researcher's own best axe match doesn't visually match the carving.",
    fontsize=11, y=1.0
)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(FIGS / "manual_needham_pairs.png", dpi=180,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nWrote {FIGS / 'manual_needham_pairs.png'}")
