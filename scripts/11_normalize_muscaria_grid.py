"""
Fix the muscaria silhouette grid for display.

Each raw mask has the aspect ratio of the source photo (usually 4:3 or 3:4
portrait), producing black bars in a square display. We:
  1. Load each mask
  2. Find the silhouette bounding box
  3. Crop to bbox with 10% padding
  4. Scale so the longer edge is 200 px
  5. Center on a 240x240 white canvas
  6. Save as clean silhouette (black shape on white)

Also produces a "best-of" gallery: pick the largest/most-solid silhouettes
first so the display shows the strongest exemplars.
"""

import numpy as np
from pathlib import Path
from PIL import Image, ImageOps
from skimage import measure

ROOT = Path(__file__).parent.parent
CORPUS = ROOT / "data" / "muscaria_corpus"
IN_MASKS = CORPUS / "masks_v2"
OUT_MASKS = CORPUS / "masks_normalized"
OUT_MASKS.mkdir(exist_ok=True)

CANVAS = 240
TARGET_MAX = 200  # px for the long edge of the silhouette


def normalize(mask_path):
    m = np.asarray(Image.open(mask_path).convert("L"))
    bw = (m > 127).astype(np.uint8)
    if bw.sum() == 0:
        return None, 0.0
    labels = measure.label(bw)
    props = measure.regionprops(labels)
    if not props:
        return None, 0.0
    r = max(props, key=lambda p: p.area)
    minr, minc, maxr, maxc = r.bbox
    # 10% padding
    hh = maxr - minr
    ww = maxc - minc
    padr = max(1, int(hh * 0.10))
    padc = max(1, int(ww * 0.10))
    minr = max(0, minr - padr); maxr = min(bw.shape[0], maxr + padr)
    minc = max(0, minc - padc); maxc = min(bw.shape[1], maxc + padc)
    crop = bw[minr:maxr, minc:maxc]

    # Scale to fit inside TARGET_MAX
    h, w = crop.shape
    scale = TARGET_MAX / max(h, w)
    new_h = max(1, int(round(h * scale)))
    new_w = max(1, int(round(w * scale)))
    im = Image.fromarray((crop * 255).astype(np.uint8)).resize(
        (new_w, new_h), Image.LANCZOS
    )
    # Threshold again after resize
    im = im.point(lambda v: 255 if v > 127 else 0)

    # Center on white canvas — silhouette is currently white-on-black; invert
    im = ImageOps.invert(im.convert("L"))  # now black shape on white
    canvas = Image.new("L", (CANVAS, CANVAS), 255)
    off_x = (CANVAS - new_w) // 2
    off_y = (CANVAS - new_h) // 2
    canvas.paste(im, (off_x, off_y))
    return canvas, float(r.area)


def main():
    masks = sorted(IN_MASKS.glob("*.png"))
    print(f"Loading {len(masks)} masks...")

    results = []
    for mp in masks:
        canvas, area = normalize(mp)
        if canvas is None:
            continue
        out_path = OUT_MASKS / mp.name
        canvas.save(out_path)
        results.append((mp.name, area))

    # Sort by silhouette area descending
    results.sort(key=lambda t: -t[1])

    print(f"Wrote {len(results)} normalized silhouettes.")
    print("Top 12 by area (used for display grid):")
    for name, area in results[:12]:
        print(f"  {name}   area={int(area)} px")

    # Copy the top-24 to a "gallery" subdir the site can use
    gallery = CORPUS / "gallery"
    gallery.mkdir(exist_ok=True)
    for name, _ in results[:24]:
        src = OUT_MASKS / name
        dst = gallery / name
        dst.write_bytes(src.read_bytes())
    print(f"Wrote top-24 gallery to {gallery}")


if __name__ == "__main__":
    main()
