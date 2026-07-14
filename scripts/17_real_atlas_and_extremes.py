"""
Build two new figures using the real Stone 53 carving silhouettes:

  1. real_carving_atlas.png — all 41 real carvings as a grid, sorted by
     P(mushroom) from high to low, colored by classifier verdict
  2. real_extremes.png — the top-6 most-mushroom and top-6 most-axe-like
     carvings shown as their actual silhouettes, side by side with reference
     mushroom and axe images
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent.parent
THUMBS = ROOT / "data" / "carving_thumbs"
FIGS = ROOT / "figures"
PROCESSED = ROOT / "data" / "processed"


def main():
    # Load per-carving predictions
    preds = pd.read_csv(PROCESSED / "three_way_predictions.csv")
    carv = pd.read_csv(ROOT / "data" / "raw" / "rock_carvings_and_axeheads.csv")
    carv = carv[carv["Stone"] == 53].reset_index(drop=True)
    preds = preds.reset_index(drop=True)
    preds["carving_id"] = carv["Carving#"].astype(int).values

    ranked = preds.sort_values("rf_prob_muscaria", ascending=False).reset_index(drop=True)

    # =========================================================
    # Figure: All 41 real carvings, sorted by P(mushroom)
    # =========================================================
    n = len(ranked)
    cols = 8
    rows = int(np.ceil(n / cols))
    fig, axarr = plt.subplots(rows, cols, figsize=(cols * 1.5, rows * 1.7))
    axarr = np.array(axarr).reshape(rows, cols)
    for i in range(rows * cols):
        r, c = i // cols, i % cols
        ax = axarr[r, c]
        if i >= n:
            ax.axis("off")
            continue
        row = ranked.iloc[i]
        cid = int(row["carving_id"])
        img_path = THUMBS / f"F{cid}.png"
        if img_path.exists():
            ax.imshow(imread(str(img_path)), cmap="gray")
        p = float(row["rf_prob_muscaria"])
        border = "#c14545" if p > 0.5 else "#4a6fa5"
        for s in ax.spines.values():
            s.set_color(border)
            s.set_linewidth(2.0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"F{cid}", fontsize=8, pad=2)
        ax.text(0.5, -0.08, f"P(mus)={p:.2f}",
                transform=ax.transAxes, ha="center", va="top",
                fontsize=7.5,
                color="#c14545" if p > 0.5 else "#4a6fa5")

    fig.suptitle(
        "All 41 Stone 53 carvings, sorted by Random Forest posterior P(mushroom).\n"
        "Red border = classified mushroom; blue border = classified axe.",
        fontsize=12, y=0.995,
    )
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(FIGS / "real_carving_atlas.png", dpi=180,
                bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Wrote: {FIGS / 'real_carving_atlas.png'}")

    # =========================================================
    # Figure: real extremes side by side
    # =========================================================
    top_mus = ranked.head(6)
    top_axe = ranked.tail(6).iloc[::-1]

    fig, axarr = plt.subplots(2, 6, figsize=(13, 4.5))
    for i, (_, r) in enumerate(top_axe.iterrows()):
        ax = axarr[0, i]
        cid = int(r["carving_id"])
        img_path = THUMBS / f"F{cid}.png"
        if img_path.exists():
            ax.imshow(imread(str(img_path)), cmap="gray")
        for s in ax.spines.values():
            s.set_color("#4a6fa5"); s.set_linewidth(2.0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"F{cid}   P(mus)={r['rf_prob_muscaria']:.2f}",
                     fontsize=9.5, color="#4a6fa5", pad=4)

    for i, (_, r) in enumerate(top_mus.iterrows()):
        ax = axarr[1, i]
        cid = int(r["carving_id"])
        img_path = THUMBS / f"F{cid}.png"
        if img_path.exists():
            ax.imshow(imread(str(img_path)), cmap="gray")
        for s in ax.spines.values():
            s.set_color("#c14545"); s.set_linewidth(2.0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"F{cid}   P(mus)={r['rf_prob_muscaria']:.2f}",
                     fontsize=9.5, color="#c14545", pad=4)

    fig.text(0.005, 0.75,
             "Top 6 most\naxe-like carvings",
             rotation=90, ha="center", va="center", fontsize=10,
             fontweight="bold", color="#4a6fa5")
    fig.text(0.005, 0.28,
             "Top 6 most\nmushroom-like carvings",
             rotation=90, ha="center", va="center", fontsize=10,
             fontweight="bold", color="#c14545")

    fig.suptitle(
        "The extremes, as their actual laser-scan silhouettes.",
        fontsize=11.5, y=1.02,
    )
    plt.tight_layout(rect=[0.02, 0, 1, 0.98])
    plt.savefig(FIGS / "real_extremes.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Wrote: {FIGS / 'real_extremes.png'}")


if __name__ == "__main__":
    main()
