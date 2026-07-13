"""
Fetch Amanita muscaria observations from iNaturalist (research-grade only),
download medium-size photos, segment silhouettes by color, extract shape
features. Reject any silhouette that fails automated quality filters.

Rationale for the color-threshold approach:
  - Amanita muscaria has a highly distinctive red cap
  - Research-grade iNaturalist photos are generally in-focus and outdoors
  - Color thresholding in HSV space (red hue, high saturation) picks the
    cap out of the background reliably for a large fraction of photos
  - Automated quality filters remove failures (multiple mushrooms, cut-off
    subject, background contamination)

The alternative (using rembg or SAM) is heavier and doesn't improve
substantially on color-based methods for this specific taxon. If we want
to publish, we'll rerun with SAM or manual QA — this is a first pass.
"""

import io
import json
import time
import numpy as np
from pathlib import Path
from PIL import Image
import requests
from skimage import measure, morphology, color, segmentation
from skimage.util import img_as_ubyte

ROOT = Path(__file__).parent.parent
CORPUS = ROOT / "data" / "muscaria_corpus"
IMGS = CORPUS / "images"
MASKS = CORPUS / "masks"
CORPUS.mkdir(exist_ok=True, parents=True)
IMGS.mkdir(exist_ok=True)
MASKS.mkdir(exist_ok=True)

INAT = "https://api.inaturalist.org/v1/observations"
UA = {"User-Agent": "stonehenge-shape-study/0.1 (dereklomas@gmail.com)"}


def fetch_observations(n_pages=6, per_page=100):
    """Pull research-grade A. muscaria observations, sorted by votes."""
    all_obs = []
    for page in range(1, n_pages + 1):
        params = {
            "taxon_name": "Amanita muscaria",
            "quality_grade": "research",
            "photos": "true",
            "per_page": per_page,
            "page": page,
            "order_by": "votes",
            "order": "desc",
        }
        r = requests.get(INAT, params=params, headers=UA, timeout=30)
        r.raise_for_status()
        data = r.json()
        all_obs.extend(data["results"])
        print(f"  page {page}: got {len(data['results'])} obs (total {len(all_obs)})")
        time.sleep(0.5)
    return all_obs


def download_photo(url, dest):
    """Download a photo, upgrading 'square' to 'medium' for full frame."""
    url = url.replace("square", "medium")
    r = requests.get(url, headers=UA, timeout=30, stream=True)
    if r.status_code != 200:
        return False
    dest.write_bytes(r.content)
    return True


def segment_red_cap(img_arr):
    """Extract silhouette using red-hue color thresholding.

    Returns binary mask (H, W) or None if segmentation fails quality checks.
    """
    if img_arr.ndim != 3 or img_arr.shape[2] < 3:
        return None
    rgb = img_arr[:, :, :3]
    hsv = color.rgb2hsv(rgb)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # A. muscaria red cap: hue near 0 or near 1 (both are red in [0,1] HSV)
    red = ((H < 0.05) | (H > 0.94)) & (S > 0.35) & (V > 0.25)

    # Include very orange-ish caps as well (some overripe / brighter)
    red_orange = ((H < 0.08) | (H > 0.94)) & (S > 0.30) & (V > 0.25)

    mask = red_orange
    if mask.sum() < 500:
        return None

    # Clean up: remove small holes, keep largest component
    mask = morphology.remove_small_objects(mask, min_size=800)
    mask = morphology.remove_small_holes(mask, area_threshold=2000)

    labels = measure.label(mask)
    if labels.max() == 0:
        return None
    regions = measure.regionprops(labels)
    largest = max(regions, key=lambda r: r.area)

    # Quality checks
    total_pixels = mask.size
    area_frac = largest.area / total_pixels

    if area_frac < 0.02:  # too small
        return None
    if area_frac > 0.60:  # entire image is red (background contamination)
        return None
    if not (0.35 < largest.solidity < 1.0):  # too concave/fragmented
        return None
    # Must not touch image edges (subject partially cut off)
    minr, minc, maxr, maxc = largest.bbox
    H_img, W_img = mask.shape
    if minr == 0 or minc == 0 or maxr == H_img or maxc == W_img:
        return None

    # Return only the largest component
    final = (labels == largest.label).astype(np.uint8) * 255
    return final


def process_all():
    print("=== Fetching A. muscaria observations from iNaturalist ===")
    obs = fetch_observations(n_pages=6, per_page=100)
    print(f"Got {len(obs)} total observations\n")

    kept = 0
    tried = 0
    manifest = []

    print("=== Downloading + segmenting ===")
    for o in obs:
        photos = o.get("photos", [])
        if not photos:
            continue
        obs_id = o["id"]
        photo_url = photos[0]["url"]

        img_path = IMGS / f"muscaria_{obs_id}.jpg"
        mask_path = MASKS / f"muscaria_{obs_id}.png"

        if img_path.exists() and mask_path.exists():
            kept += 1
            manifest.append({"obs_id": obs_id, "img": str(img_path), "mask": str(mask_path)})
            continue

        tried += 1
        try:
            if not download_photo(photo_url, img_path):
                continue
            img = np.asarray(Image.open(img_path).convert("RGB"))
        except Exception as e:
            print(f"  obs {obs_id}: download error: {e}")
            if img_path.exists():
                img_path.unlink()
            continue

        mask = segment_red_cap(img)
        if mask is None:
            img_path.unlink()
            continue

        Image.fromarray(mask, mode="L").save(mask_path)
        kept += 1
        manifest.append({"obs_id": obs_id, "img": str(img_path), "mask": str(mask_path)})

        if tried % 50 == 0:
            print(f"  processed {tried}, kept {kept} ({100*kept/tried:.0f}%)")

        time.sleep(0.15)  # be polite

    print(f"\nDone. Downloaded and segmented: {kept} of {tried} attempted.")
    with open(CORPUS / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    process_all()
