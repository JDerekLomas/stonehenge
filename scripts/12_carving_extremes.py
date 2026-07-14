"""
Rank Stone 53 carvings by classifier confidence and render:
  - top-5 most-mushroom carvings and top-5 most-axe carvings
  - as schematic silhouettes (ellipses stretched to the carving's AR + roundness)

Also render:
  - the "median axe" silhouette (median AR, median roundness across Bevan corpus)
  - the "median mushroom" silhouette (median AR, median roundness across A. muscaria corpus)

This gives a visual side-by-side that doesn't depend on us having access to
the original carving TIFFs — the shapes shown are reconstructions of the
same shape features the classifier uses to reach its verdict.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGS = ROOT / "figures"
OUT = PROCESSED / "extremes"
OUT.mkdir(exist_ok=True)


def draw_silhouette_from_features(ar, roundness, size=240, color=(0, 0, 0)):
    """Reconstruct a rough silhouette from Aspect Ratio + Roundness.

    AR = major/minor axis. Roundness = 4*Area / (pi * MajorAxis^2).
    Given AR and Roundness we can back out the ellipse-equivalent shape:
      major = 1
      minor = 1/AR
      area = roundness * pi * major^2 / 4
    We construct a stylized shape by starting with the equivalent ellipse
    and then modulating radius by a small periodic function so shapes with
    lower solidity look less convex. Since we don't have solidity in the
    extreme sets, keep it simple: pure ellipse.
    """
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    # Scale so major axis is 80% of canvas
    major_px = size * 0.85
    # If AR > 1 the shape is taller than wide; orient with major = vertical
    if ar >= 1:
        h = major_px
        w = major_px / ar
    else:
        w = major_px
        h = major_px * ar

    # Roundness constrains: area = roundness * pi * major^2 / 4
    # For an ellipse of major=a, minor=b: area = pi*a*b/4 ... no, that's diameter form.
    # Actually image "Roundness" (ImageJ) = 4*A / (pi * D_max^2) where D_max is the
    # major axis LENGTH. For an ellipse with semi-axes a,b (a>=b):
    #   A = pi * a * b
    #   D_max = 2a
    #   Roundness = 4 * pi * a * b / (pi * 4 * a^2) = b/a = 1/AR
    # Which is what the correlation plot showed. So a pure ellipse has
    # Roundness = 1/AR exactly. For our reconstruction, using an ellipse
    # of the given AR gives the right Roundness "for free."

    x0 = (size - w) / 2
    y0 = (size - h) / 2
    d.ellipse([x0, y0, x0 + w, y0 + h], fill=color + (255,))
    return img


def draw_axe_schematic(size=240, ar=2.7, blade_flare=0.35):
    """A schematic bronze axehead: elongated with flared blade end."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    # Vertical orientation, blade at top (as in the "blade up" convention)
    h = size * 0.85
    w = h / ar
    x_cx = size / 2
    y_top = (size - h) / 2

    butt_w = w * 0.55
    mid_w = w * 0.85
    blade_w = w * (1.0 + blade_flare)

    # Approximate axe outline with 8 points
    pts = [
        (x_cx - butt_w / 2, y_top + h),                # bottom left (butt)
        (x_cx - mid_w / 2, y_top + h * 0.55),          # mid left
        (x_cx - blade_w / 2, y_top + h * 0.15),        # blade left
        (x_cx - blade_w / 2 * 0.9, y_top),             # top left corner
        (x_cx + blade_w / 2 * 0.9, y_top),             # top right corner
        (x_cx + blade_w / 2, y_top + h * 0.15),        # blade right
        (x_cx + mid_w / 2, y_top + h * 0.55),          # mid right
        (x_cx + butt_w / 2, y_top + h),                # bottom right (butt)
    ]
    d.polygon(pts, fill=(0, 0, 0, 255))
    return img


def draw_mushroom_schematic(size=240, ar=1.7, ring=False):
    """A schematic A. muscaria: dome cap over shorter stem."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    h = size * 0.85
    w = h / ar
    x_cx = size / 2
    y_top = (size - h) / 2

    # Cap: wide elliptical dome (top 65% of shape)
    cap_h = h * 0.65
    cap_w = w * 1.05
    d.chord(
        [x_cx - cap_w / 2, y_top,
         x_cx + cap_w / 2, y_top + cap_h * 1.5],
        180, 360, fill=(0, 0, 0, 255)
    )
    d.rectangle(
        [x_cx - cap_w / 2, y_top + cap_h * 0.75,
         x_cx + cap_w / 2, y_top + cap_h],
        fill=(0, 0, 0, 255)
    )

    # Stem: narrower rectangle
    stem_w = w * 0.35
    d.rectangle(
        [x_cx - stem_w / 2, y_top + cap_h,
         x_cx + stem_w / 2, y_top + h],
        fill=(0, 0, 0, 255)
    )

    # Optional annulus (ring) at the top of the stem
    if ring:
        ring_w = stem_w * 1.6
        ring_h = 4
        d.ellipse(
            [x_cx - ring_w / 2, y_top + cap_h + h * 0.08,
             x_cx + ring_w / 2, y_top + cap_h + h * 0.08 + ring_h * 3],
            fill=(0, 0, 0, 255)
        )
    return img


def main():
    predictions = pd.read_csv(PROCESSED / "three_way_predictions.csv")
    carv_source = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
    carv_source = carv_source[carv_source["Stone"] == 53][
        ["Carving#", "Circularity", "Aspect Ratio", "Roundness", "Solidity", "Recurve", "Ring"]
    ].dropna(subset=["Aspect Ratio", "Roundness"]).reset_index(drop=True)

    # Merge shape features back in
    predictions = predictions.reset_index(drop=True)
    predictions["carving_id"] = carv_source["Carving#"].values
    predictions["Aspect Ratio"] = carv_source["Aspect Ratio"].values
    predictions["Roundness"] = carv_source["Roundness"].values
    predictions["Recurve"] = carv_source["Recurve"].fillna(0).astype(int).values
    predictions["Ring"] = carv_source["Ring"].fillna(0).astype(int).values

    ranked = predictions.sort_values("rf_prob_muscaria", ascending=False)

    top_mushroom = ranked.head(6)
    top_axe = ranked.tail(6).iloc[::-1]

    print("=== Top 6 most-mushroom-like carvings ===")
    print(top_mushroom[["carving_id", "Aspect Ratio", "Roundness", "Recurve",
                        "Ring", "rf_prob_muscaria"]].to_string(index=False))
    print("\n=== Top 6 most-axe-like carvings ===")
    print(top_axe[["carving_id", "Aspect Ratio", "Roundness", "Recurve",
                   "Ring", "rf_prob_muscaria"]].to_string(index=False))

    # =====================================================
    # Render schematics
    # =====================================================
    axe_med_ar = 2.71
    mus_med_ar = 1.6

    # Save schematic references
    draw_axe_schematic(ar=axe_med_ar).save(OUT / "ref_axe_median.png")
    draw_mushroom_schematic(ar=mus_med_ar, ring=True).save(OUT / "ref_mushroom_median.png")

    # Render each of the top 6 most-mushroom carvings as their shape-feature ellipse
    for _, r in top_mushroom.iterrows():
        img = draw_silhouette_from_features(r["Aspect Ratio"], r["Roundness"])
        img.save(OUT / f"most_mushroom_F{int(r['carving_id']):03d}.png")
    for _, r in top_axe.iterrows():
        img = draw_silhouette_from_features(r["Aspect Ratio"], r["Roundness"])
        img.save(OUT / f"most_axe_F{int(r['carving_id']):03d}.png")

    # Save the ranking to JSON for the paper site
    output = {
        "median_axe_ar": axe_med_ar,
        "median_mushroom_ar": mus_med_ar,
        "top_mushroom": [
            {
                "carving_id": int(r["carving_id"]),
                "aspect_ratio": round(float(r["Aspect Ratio"]), 3),
                "roundness": round(float(r["Roundness"]), 3),
                "recurve": bool(r["Recurve"]),
                "ring": bool(r["Ring"]),
                "prob_mushroom": round(float(r["rf_prob_muscaria"]), 3),
            }
            for _, r in top_mushroom.iterrows()
        ],
        "top_axe": [
            {
                "carving_id": int(r["carving_id"]),
                "aspect_ratio": round(float(r["Aspect Ratio"]), 3),
                "roundness": round(float(r["Roundness"]), 3),
                "recurve": bool(r["Recurve"]),
                "ring": bool(r["Ring"]),
                "prob_mushroom": round(float(r["rf_prob_muscaria"]), 3),
            }
            for _, r in top_axe.iterrows()
        ],
    }
    with open(PROCESSED / "carving_extremes.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nSaved schematics to", OUT)
    print("Saved ranking to", PROCESSED / "carving_extremes.json")


if __name__ == "__main__":
    main()
