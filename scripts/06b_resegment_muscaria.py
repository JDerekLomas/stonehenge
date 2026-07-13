"""
Re-segment A. muscaria photos with proper cap-hole filling.

The pure red-hue threshold in v1 missed the white spots on the cap,
producing donut-shaped masks. This version:
  1. Threshold on red hue (as before)
  2. Also threshold on "warm off-red" pixels (yellows/oranges, browns)
     since some caps are more orange than red, and the spots are cream
  3. Fill all internal holes generously (up to 20% of largest component area)
  4. Take convex hull if solidity is low but shape is otherwise good
  5. Reject if the final silhouette doesn't look like a mushroom shape
     (bad aspect ratio, hollow, edge-touching, etc)
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from skimage import measure, morphology, color, filters
from scipy import ndimage as ndi

ROOT = Path(__file__).parent.parent
CORPUS = ROOT / "data" / "muscaria_corpus"
IMGS = CORPUS / "images"
MASKS = CORPUS / "masks"
MASKS_V2 = CORPUS / "masks_v2"
MASKS_V2.mkdir(exist_ok=True)


def segment_cap_v2(img_arr):
    """Improved segmentation with hole-filling and stem inclusion."""
    if img_arr.ndim != 3 or img_arr.shape[2] < 3:
        return None

    rgb = img_arr[:, :, :3].astype(np.float32) / 255.0
    hsv = color.rgb2hsv(rgb)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # 1. Red/orange cap (broader hue tolerance)
    red_hue = (H < 0.10) | (H > 0.90)
    red_cap = red_hue & (S > 0.30) & (V > 0.25)

    if red_cap.sum() < 500:
        return None

    # Get initial cap region
    red_cap = morphology.remove_small_objects(red_cap, min_size=500)
    labels = measure.label(red_cap)
    if labels.max() == 0:
        return None
    regions = measure.regionprops(labels)
    largest = max(regions, key=lambda r: r.area)
    minr, minc, maxr, maxc = largest.bbox

    # 2. Within the cap bounding box (plus 30% padding), take everything red-ish
    #    OR bright-white/cream (the spots)
    pad = 0.3
    h_bbox = maxr - minr
    w_bbox = maxc - minc
    r0 = max(0, int(minr - pad * h_bbox))
    r1 = min(rgb.shape[0], int(maxr + pad * h_bbox))
    c0 = max(0, int(minc - pad * w_bbox))
    c1 = min(rgb.shape[1], int(maxc + pad * w_bbox))

    # Build the "cap mask" region:
    # take pixels that are either red OR bright-white/cream inside the padded bbox
    inside = np.zeros_like(red_cap)
    inside[r0:r1, c0:c1] = True

    warm_or_cream = (
        red_cap
        | ((V > 0.75) & (S < 0.35))  # white/cream (spots)
        | (((H > 0.05) & (H < 0.12)) & (S > 0.20) & (V > 0.35))  # yellow/orange fringes
    ) & inside

    # 3. Aggressive hole filling — the cap should be solid
    filled = ndi.binary_fill_holes(warm_or_cream)
    filled = morphology.remove_small_holes(filled, area_threshold=50000)

    # Retake largest component
    filled = morphology.remove_small_objects(filled, min_size=1000)
    labels = measure.label(filled)
    if labels.max() == 0:
        return None
    regions = measure.regionprops(labels)
    largest = max(regions, key=lambda r: r.area)

    # 4. If solidity is still low, take convex hull
    if largest.solidity < 0.80:
        hull_img = np.zeros_like(filled)
        hull_img[largest.bbox[0]:largest.bbox[2],
                 largest.bbox[1]:largest.bbox[3]] = largest.convex_image
        labels = measure.label(hull_img)
        regions = measure.regionprops(labels)
        if not regions:
            return None
        largest = max(regions, key=lambda r: r.area)
        filled = hull_img

    # 5. Quality checks
    total = filled.size
    area_frac = largest.area / total
    if area_frac < 0.02 or area_frac > 0.65:
        return None

    minr, minc, maxr, maxc = largest.bbox
    Hi, Wi = filled.shape
    # Reject if silhouette touches any image edge (subject cut off)
    if minr <= 1 or minc <= 1 or maxr >= Hi - 1 or maxc >= Wi - 1:
        return None

    # Reject caps that are extremely elongated horizontally (probably
    # a stem-only view or panorama contamination)
    ar = (maxc - minc) / max(1, (maxr - minr))
    if ar > 4.0:
        return None

    # Return the largest component as final mask
    final = np.zeros_like(filled, dtype=np.uint8)
    final[labels == largest.label] = 255
    return final


def main():
    imgs = sorted(IMGS.glob("*.jpg"))
    if not imgs:
        print("No images found in", IMGS)
        return

    kept = 0
    tried = 0
    for p in imgs:
        tried += 1
        try:
            arr = np.asarray(Image.open(p).convert("RGB"))
        except Exception as e:
            print(f"  {p.name}: error reading: {e}")
            continue
        mask = segment_cap_v2(arr)
        if mask is None:
            continue
        Image.fromarray(mask, mode="L").save(MASKS_V2 / (p.stem + ".png"))
        kept += 1

    print(f"Re-segmented {kept}/{tried} images ({100*kept/tried:.0f}% pass rate)")


if __name__ == "__main__":
    main()
