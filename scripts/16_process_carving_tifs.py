"""
Process the 41 Stone 53 carving TIFFs (and 6 Ri Cruin) into web-ready PNGs.

Each TIFF is a 500x400 binary silhouette from the English Heritage 2012
laser scan. We convert to:
  - a clean 500x400 PNG (black shape on white)
  - a normalized square thumbnail (240x240) centered on the shape
"""

import numpy as np
from pathlib import Path
from PIL import Image, ImageOps
from skimage import measure

ROOT = Path(__file__).parent.parent
SRC = ROOT / "data" / "stonehenge_folder" / "Stonehenge Carvings" / "Stone 53 Carvings"
OUT_FULL = ROOT / "data" / "carving_pngs"
OUT_THUMB = ROOT / "data" / "carving_thumbs"
OUT_FULL.mkdir(exist_ok=True, parents=True)
OUT_THUMB.mkdir(exist_ok=True, parents=True)

CANVAS = 240


def process_one(tif_path: Path):
    img = Image.open(tif_path)
    # Convert to L (grayscale). The TIFFs use a palette where the shape is black.
    L = img.convert("L")
    arr = np.asarray(L)

    # Determine polarity — the carving is the dominant contiguous region
    dark = (arr < 128).astype(np.uint8)
    light = (arr >= 128).astype(np.uint8)
    # Whichever has smaller total area *and* touches fewer image edges is the shape
    def edge_pixels(mask):
        return int(mask[0].sum() + mask[-1].sum() + mask[:, 0].sum() + mask[:, -1].sum())
    if edge_pixels(dark) < edge_pixels(light):
        shape = dark
    else:
        shape = light

    labels = measure.label(shape)
    props = measure.regionprops(labels)
    if not props:
        return None, None
    largest = max(props, key=lambda p: p.area)
    shape_mask = (labels == largest.label).astype(np.uint8) * 255

    # Full-size render (500x400): black shape on white
    full = Image.fromarray(255 - shape_mask, mode="L")
    full_out = OUT_FULL / (tif_path.stem + ".png")
    full.save(full_out)

    # Thumbnail: crop to bbox with padding, scale to fit 200 with 240 canvas
    minr, minc, maxr, maxc = largest.bbox
    hh = maxr - minr
    ww = maxc - minc
    pad = int(0.10 * max(hh, ww))
    minr = max(0, minr - pad); maxr = min(shape_mask.shape[0], maxr + pad)
    minc = max(0, minc - pad); maxc = min(shape_mask.shape[1], maxc + pad)
    crop = shape_mask[minr:maxr, minc:maxc]
    h, w = crop.shape
    scale = 200 / max(h, w)
    new_h = max(1, int(round(h * scale)))
    new_w = max(1, int(round(w * scale)))
    im = Image.fromarray(crop, mode="L").resize((new_w, new_h), Image.LANCZOS)
    im = im.point(lambda v: 255 if v > 127 else 0)
    im = ImageOps.invert(im.convert("L"))  # black shape on white

    canvas = Image.new("L", (CANVAS, CANVAS), 255)
    off_x = (CANVAS - new_w) // 2
    off_y = (CANVAS - new_h) // 2
    canvas.paste(im, (off_x, off_y))
    thumb_out = OUT_THUMB / (tif_path.stem + ".png")
    canvas.save(thumb_out)
    return full_out, thumb_out


def main():
    tifs = sorted(SRC.glob("F*.tif"))
    print(f"Processing {len(tifs)} Stone 53 TIFFs...")
    ok = 0
    for tp in tifs:
        f, t = process_one(tp)
        if f is not None:
            ok += 1
    print(f"Saved {ok} full PNGs to {OUT_FULL}")
    print(f"Saved {ok} thumbnails to {OUT_THUMB}")


if __name__ == "__main__":
    main()
