"""
Shape atlas: render every axe (124) and every Stone 53 carving (41) as a
shape-ellipse silhouette from its (Aspect Ratio, Roundness).

This is a visual reprise of the multivariate result: at a glance, the axe
corpus is dominantly elongated and the carving corpus is dominantly
squat/round.

Sort by aspect ratio for readability. Same-scale rendering, small
per-cell axes.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
FIGS = ROOT / "figures"


def draw_ellipse(ax, ar, color):
    major = 0.85
    minor = major / ar
    ell = Ellipse((0.5, 0.5), width=minor, height=major, angle=0,
                  facecolor=color, edgecolor="none")
    ax.add_patch(ell)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def make_grid(values, color, title, out_path, cols=16):
    n = len(values)
    rows = int(np.ceil(n / cols))
    fig, axarr = plt.subplots(rows, cols, figsize=(cols * 0.8, rows * 0.9))
    axarr = np.array(axarr).reshape(rows, cols)
    for i in range(rows * cols):
        r, c = i // cols, i % cols
        ax = axarr[r, c]
        if i >= n:
            ax.set_visible(False)
            continue
        draw_ellipse(ax, values[i], color=color)
    fig.suptitle(title, fontsize=13, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(out_path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


def main():
    axes_ar = pd.read_csv(DATA / "early_axes_bevan.csv")["AR"].dropna().sort_values(ascending=False).values
    carv = pd.read_csv(DATA / "rock_carvings_and_axeheads.csv")
    carv_ar = carv[carv["Stone"] == 53]["Aspect Ratio"].dropna().sort_values(ascending=False).values

    make_grid(
        axes_ar, "#4a6fa5",
        f"All {len(axes_ar)} British EBA axes (Bevan corpus) as shape-ellipse silhouettes, sorted by aspect ratio",
        FIGS / "atlas_axes.png",
    )
    make_grid(
        carv_ar, "#c14545",
        f"All {len(carv_ar)} Stone 53 carvings as shape-ellipse silhouettes, sorted by aspect ratio",
        FIGS / "atlas_carvings.png",
    )
    print(f"Wrote: {FIGS / 'atlas_axes.png'}")
    print(f"Wrote: {FIGS / 'atlas_carvings.png'}")

    # Descriptive summary
    print(f"\nAxes n={len(axes_ar)}: AR min {axes_ar.min():.2f}, median {np.median(axes_ar):.2f}, max {axes_ar.max():.2f}")
    print(f"Carvings n={len(carv_ar)}: AR min {carv_ar.min():.2f}, median {np.median(carv_ar):.2f}, max {carv_ar.max():.2f}")
    over_2 = (carv_ar > 2.0).sum()
    print(f"Carvings with AR > 2.0 (axe-plausible): {over_2}/{len(carv_ar)} ({100*over_2/len(carv_ar):.0f}%)")


if __name__ == "__main__":
    main()
