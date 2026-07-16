"""
Extract individual carving silhouettes from Stone4.tiff.

The image is a spatial layout of ~60 carvings on Stone 4, each rendered
as a filled shape in either red (discovered pre-2003) or green
(discovered in 2012), on white background. Each has an F-number label
nearby.

We segment each connected coloured component and extract it as an
individual binary silhouette. Also compute ImageJ-equivalent features.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image, ImageOps
from skimage import measure, morphology

Image.MAX_IMAGE_PIXELS = 500_000_000

ROOT = Path(__file__).parent.parent
SRC = Path("/Users/dereklomas/Downloads/Stone4.tiff")
OUT = ROOT / "data" / "stone4_extracted"
OUT_THUMBS = OUT / "thumbs"
OUT_FULL = OUT / "full"
OUT.mkdir(exist_ok=True)
OUT_THUMBS.mkdir(exist_ok=True)
OUT_FULL.mkdir(exist_ok=True)

# Load
img = Image.open(SRC).convert("RGB")
arr = np.asarray(img)
print(f"Loaded {SRC.name}: {arr.shape}")

# Detect coloured pixels (anything NOT close to white or grey text)
R, G, B = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)
brightness = (R + G + B) / 3

# Red carvings: high R, low G, low B — the brownish red
red = (R > 100) & (G < 100) & (B < 100)

# Green carvings: high G, moderate R, low B — the sage green
green = (G > 100) & (R < 200) & (B < 150) & (G > R)

# Coloured mask
coloured = red | green
print(f"Coloured pixels: {coloured.sum():,} ({100*coloured.mean():.2f}%)")

# Clean up — remove small noise, close small gaps within shapes
mask = morphology.remove_small_objects(coloured, min_size=800)
mask = morphology.remove_small_holes(mask, area_threshold=200)

# Label connected components
labels = measure.label(mask)
props = measure.regionprops(labels)
print(f"Connected components: {len(props)}")

# Filter to likely-carving components: area between ~1000 and ~200000 px
valid = [r for r in props if 1000 <= r.area <= 500000]
print(f"Valid carvings after size filter: {len(valid)}")

# Filter out the two legend-box artifacts (perfect squares with solidity ~1.0)
def is_legend_swatch(r):
    minr, minc, maxr, maxc = r.bbox
    h = maxr - minr; w = maxc - minc
    return r.solidity > 0.99 and abs(h - w) < 5

valid = [r for r in valid if not is_legend_swatch(r)]
print(f"After legend-swatch filter: {len(valid)}")

# Extract each
rows = []
for i, r in enumerate(sorted(valid, key=lambda p: (-p.centroid[0], p.centroid[1])), 1):
    minr, minc, maxr, maxc = r.bbox
    pad = int(0.10 * max(maxr-minr, maxc-minc))
    minr = max(0, minr-pad); maxr = min(arr.shape[0], maxr+pad)
    minc = max(0, minc-pad); maxc = min(arr.shape[1], maxc+pad)

    # Crop the coloured mask for this component only
    lbl_crop = labels[minr:maxr, minc:maxc]
    binary = (lbl_crop == r.label).astype(np.uint8) * 255

    # Full-size silhouette (black shape on white)
    full = Image.fromarray(255 - binary, mode="L")
    full.save(OUT_FULL / f"s4_{i:03d}.png")

    # Thumbnail — normalize to 240x240
    h, w = binary.shape
    scale = 200 / max(h, w)
    im = Image.fromarray(binary, mode="L").resize(
        (max(1, int(w*scale)), max(1, int(h*scale))), Image.LANCZOS)
    im = im.point(lambda v: 255 if v > 127 else 0)
    im = ImageOps.invert(im.convert("L"))
    canvas = Image.new("L", (240, 240), 255)
    canvas.paste(im, ((240-im.width)//2, (240-im.height)//2))
    canvas.save(OUT_THUMBS / f"s4_{i:03d}.png")

    # Compute ImageJ-equivalent features on the binary mask
    area = float(r.area)
    perim = float(r.perimeter)
    maj = float(r.axis_major_length)
    mn = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    rows.append({
        "id": f"s4_{i:03d}",
        "centroid_y": float(r.centroid[0]),
        "centroid_x": float(r.centroid[1]),
        "Area": area,
        "Perimeter": perim,
        "Height": float(r.bbox[2] - r.bbox[0]),
        "Width": float(r.bbox[3] - r.bbox[1]),
        "Circularity": 4 * np.pi * area / (perim**2),
        "Aspect Ratio": maj / mn,
        "Roundness": 4 * area / (np.pi * maj**2),
        "Solidity": float(r.solidity),
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "stone4_features.csv", index=False)
print(f"\nSaved {len(df)} silhouettes with features to {OUT}")
print(f"AR median: {df['Aspect Ratio'].median():.2f}, IQR "
      f"[{df['Aspect Ratio'].quantile(0.25):.2f}, {df['Aspect Ratio'].quantile(0.75):.2f}]")
print(f"Roundness median: {df['Roundness'].median():.2f}")
print(f"Bounding-box W/H median: {(df['Width']/df['Height']).median():.2f}")
