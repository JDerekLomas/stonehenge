"""
Rerun the whole shape analysis using the clean pre-segmented reference
silhouettes now available from the paper's original corpus (rather than
my noisy iNaturalist auto-segmentation).

Sources:
  - Axes: 41 already-segmented axe TIFFs from Needham 1983 + Burgess
  - Mushrooms: 22 already-segmented mushroom silhouettes
  - Carvings: 42 carvings across Stones 53/4/5 in AllCarvings

For each shape:
  1. Load, threshold to binary
  2. Compute canonical ImageJ features: Circularity, AR, Roundness, Solidity
  3. Save to CSV

Then run the same 3-way classifier and produce updated figures.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from skimage import measure

ROOT = Path(__file__).parent.parent
BASE = ROOT / "data" / "downloads_extracted"
OUT_DIR = ROOT / "data" / "clean_corpus"
OUT_DIR.mkdir(exist_ok=True, parents=True)

CORPORA = {
    "axe": BASE / "Axes (Needham 1983, 2012_ burgess)",
    "mushroom": BASE / "Entire Image Corpus" / "mushrooms",
    "carving": BASE / "Entire Image Corpus" / "AllCarvings",
}


def features_from_binary(bw):
    labels = measure.label(bw)
    props = measure.regionprops(labels)
    if not props:
        return None
    r = max(props, key=lambda p: p.area)
    area = float(r.area)
    perim = float(r.perimeter)
    if area <= 0 or perim <= 0:
        return None
    major = float(r.axis_major_length)
    minor = float(r.axis_minor_length) if r.axis_minor_length > 0 else 1e-6
    return {
        "Area": area,
        "Perimeter": perim,
        "Height": float(r.bbox[2] - r.bbox[0]),
        "Width": float(r.bbox[3] - r.bbox[1]),
        "Circularity": 4 * np.pi * area / (perim ** 2),
        "Aspect Ratio": major / minor,
        "Roundness": 4 * area / (np.pi * major ** 2),
        "Solidity": float(r.solidity),
    }


def load_and_binarize(path):
    img = Image.open(path).convert("L")
    arr = np.asarray(img)
    # Shape is the darker region; also handle cases where subject is white
    dark = (arr < 128).astype(np.uint8)
    light = (arr >= 128).astype(np.uint8)
    def edge_px(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    if edge_px(dark) < edge_px(light):
        return dark
    return light


def process_corpus(name, directory):
    rows = []
    tifs = sorted(directory.glob("*.tif")) + sorted(directory.glob("*.png")) + \
           sorted(directory.glob("*.jpg"))
    for p in tifs:
        try:
            bw = load_and_binarize(p)
            feats = features_from_binary(bw)
        except Exception as e:
            print(f"  ERR {p.name}: {e}")
            continue
        if feats is None:
            continue
        feats["source"] = name
        feats["id"] = p.stem
        rows.append(feats)
    df = pd.DataFrame(rows)
    print(f"{name}: n = {len(df)}  (of {len(tifs)} files)")
    return df


def main():
    frames = []
    for name, directory in CORPORA.items():
        frames.append(process_corpus(name, directory))
    all_df = pd.concat(frames, ignore_index=True)
    all_df.to_csv(OUT_DIR / "clean_features.csv", index=False)
    print(f"\nWrote {OUT_DIR / 'clean_features.csv'} ({len(all_df)} rows)")

    print("\n=== Descriptive stats (dimensionless) ===\n")
    for name in ["axe", "mushroom", "carving"]:
        sub = all_df[all_df["source"] == name]
        print(f"{name:<10}  n={len(sub):3d}   AR: {sub['Aspect Ratio'].median():.2f}   "
              f"Round: {sub['Roundness'].median():.2f}   Circ: {sub['Circularity'].median():.2f}   "
              f"Solidity: {sub['Solidity'].median():.2f}")


if __name__ == "__main__":
    main()
