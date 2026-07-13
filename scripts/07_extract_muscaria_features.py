"""
Extract shape features from A. muscaria silhouette masks, matching the
ImageJ features used by the Bevan axe corpus.

Features computed:
  - Area (pixel count)
  - Perimeter
  - Height, Width (from bounding box)
  - Circularity = 4pi * Area / Perimeter^2
  - AR (aspect ratio) = MajorAxis / MinorAxis (from fitted ellipse)
  - Round (roundness) = 4 * Area / (pi * MajorAxis^2)
  - Solidity = Area / ConvexArea

These match the ImageJ definitions used in the Bevan corpus so the
resulting numbers are directly comparable.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from skimage import measure

ROOT = Path(__file__).parent.parent
CORPUS = ROOT / "data" / "muscaria_corpus"
MASKS = CORPUS / "masks_v2"
OUT = ROOT / "data" / "processed"


def features_from_mask(mask_arr):
    """Return dict of ImageJ-compatible shape features."""
    # Ensure binary
    bw = (mask_arr > 127).astype(np.uint8)
    labels = measure.label(bw)
    props = measure.regionprops(labels)
    if not props:
        return None
    # Take largest connected component
    r = max(props, key=lambda p: p.area)

    area = float(r.area)
    perim = float(r.perimeter)
    if perim <= 0 or area <= 0:
        return None

    minr, minc, maxr, maxc = r.bbox
    height = float(maxr - minr)
    width = float(maxc - minc)

    major = float(r.major_axis_length)
    minor = float(r.minor_axis_length) if r.minor_axis_length > 0 else 1e-6

    circularity = 4 * np.pi * area / (perim ** 2)
    ar = major / minor
    roundness = 4 * area / (np.pi * major ** 2)
    solidity = float(r.solidity)

    return {
        "Area": area,
        "Perimeter": perim,
        "Height": height,
        "Width": width,
        "Circularity": circularity,
        "Aspect Ratio": ar,
        "Roundness": roundness,
        "Solidity": solidity,
    }


def main():
    mask_paths = sorted(MASKS.glob("*.png"))
    if not mask_paths:
        print("No masks found. Run 06_fetch_muscaria.py first.")
        return

    rows = []
    skipped = 0
    for mp in mask_paths:
        try:
            arr = np.asarray(Image.open(mp).convert("L"))
        except Exception:
            skipped += 1
            continue
        feats = features_from_mask(arr)
        if feats is None:
            skipped += 1
            continue
        feats["source"] = "muscaria"
        feats["id"] = mp.stem
        rows.append(feats)

    df = pd.DataFrame(rows)
    df = df[["id", "source", "Area", "Perimeter", "Height", "Width",
             "Circularity", "Aspect Ratio", "Roundness", "Solidity"]]
    df.to_csv(OUT / "muscaria_shape_features.csv", index=False)

    print(f"Extracted features from {len(df)} silhouettes ({skipped} skipped)")
    print()
    print("Feature distributions:")
    for feat in ["Circularity", "Aspect Ratio", "Roundness", "Solidity"]:
        col = df[feat]
        print(f"  {feat:<15} mean = {col.mean():.3f}, sd = {col.std():.3f}, "
              f"median = {col.median():.3f}, IQR = [{col.quantile(0.25):.3f}, {col.quantile(0.75):.3f}]")
    print()
    print(f"Saved: {OUT / 'muscaria_shape_features.csv'}")


if __name__ == "__main__":
    main()
