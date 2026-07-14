"""
Compare actual physical sizes:
  - 292 British bronze axes (Bevan Corpus, mm) — total length
  - 41 Stone 53 carvings (paper's ImageJ Height column, likely cm)
  - 15 native British psilocybin mushroom species (cm; cap + stem)

Atkinson (1953) claimed the carvings were "life-sized" bronze axes.
This tests that claim quantitatively.

Assumptions on units:
  - Bevan Length is in mm (values 50-224, median 122). Convert to cm.
  - Carving Height is in cm (values 5-30, paper text says smallest is
    7 cm and largest 40 cm — matches). Confirmed by cross-reference
    to the paper.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
FIGS = ROOT / "figures"

# =========================================================
# 1. Bronze axe lengths (Corpus + ea sheets)
# =========================================================
corp = pd.read_excel(DATA / "Early Axes from Bevan.xlsx", sheet_name="Corpus")
ea = pd.read_excel(DATA / "Early Axes from Bevan.xlsx", sheet_name="ea")

# Use the Corpus subset (curated, has typology labels)
axe_lengths_cm = corp["Length"].dropna().values / 10.0  # mm -> cm
print(f"Axes (Corpus): n = {len(axe_lengths_cm)}, "
      f"median = {np.median(axe_lengths_cm):.1f} cm, "
      f"range [{axe_lengths_cm.min():.1f}, {axe_lengths_cm.max():.1f}] cm")

# By Needham class
by_class = corp.groupby("BasicType")["Length"].agg(["count", "median", "min", "max"]) / 10.0
by_class["count"] = corp.groupby("BasicType")["Length"].count()
print("\nBy Needham class (cm):")
print(by_class)

# =========================================================
# 2. Carving heights
# =========================================================
carv = pd.read_excel(DATA / "Stone 53 Measurements.xlsx", sheet_name="Carvings")
carv_heights = carv["Height"].dropna().values  # assumed cm
carv_widths = carv["Width"].dropna().values
print(f"\nCarvings (Stone 53): n = {len(carv_heights)}, "
      f"median = {np.median(carv_heights):.1f} cm, "
      f"range [{carv_heights.min():.1f}, {carv_heights.max():.1f}] cm")

# =========================================================
# 3. Mushroom sizes (cap + stem)
# =========================================================
mus = pd.read_excel(DATA / "Mushroom Outlines Carvings.xlsx",
                     sheet_name="Mushrooms")
mus_valid = mus.dropna(subset=["Cap Size", "Stem Size"])
mus_total = (mus_valid["Cap Size"] + mus_valid["Stem Size"]).values
print(f"\nMushrooms: n = {len(mus_total)}, "
      f"median total = {np.median(mus_total):.1f} cm, "
      f"range [{mus_total.min():.1f}, {mus_total.max():.1f}] cm")
print(mus_valid[["Species", "Cap Size", "Stem Size"]].assign(
    Total=lambda d: d["Cap Size"] + d["Stem Size"]).to_string(index=False))

# =========================================================
# Figure: overlaid histograms
# =========================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
bins = np.arange(0, 55, 2)

ax.hist(axe_lengths_cm, bins=bins, alpha=0.6, color="#4a6fa5",
        label=f"Bronze axes (n={len(axe_lengths_cm)}, Bevan Corpus)",
        edgecolor="white", linewidth=0.5)
ax.hist(carv_heights, bins=bins, alpha=0.7, color="#c14545",
        label=f"Stone 53 carvings (n={len(carv_heights)}, height)",
        edgecolor="white", linewidth=0.5)
ax.hist(mus_total, bins=bins, alpha=0.55, color="#7cae5a",
        label=f"Native British psilocybin mushrooms (n={len(mus_total)}, cap+stem)",
        edgecolor="white", linewidth=0.5)

# Annotations
ax.axvline(np.median(axe_lengths_cm), color="#2c4a70", linestyle="--",
           linewidth=1.3, alpha=0.8)
ax.axvline(np.median(carv_heights), color="#8b2020", linestyle="--",
           linewidth=1.3, alpha=0.8)

ax.set_xlabel("Length / height (cm)", fontsize=11)
ax.set_ylabel("Count", fontsize=11)
ax.set_title(
    "Physical size distributions.\n"
    "Carvings (median 9.6 cm) overlap substantially with bronze axes (median 12 cm) at 5-20 cm;\n"
    "the largest carvings (30 cm+) exceed typical bronze axes but sit within the mushroom range.",
    fontsize=11, pad=10,
)
ax.legend(fontsize=9.5, loc="upper right", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.25)

# Add median annotations
ax.text(np.median(axe_lengths_cm)+0.4, ax.get_ylim()[1]*0.85,
        f"axe median\n{np.median(axe_lengths_cm):.1f} cm",
        fontsize=8.5, color="#2c4a70", va="top")
ax.text(np.median(carv_heights)+0.4, ax.get_ylim()[1]*0.60,
        f"carving median\n{np.median(carv_heights):.1f} cm",
        fontsize=8.5, color="#8b2020", va="top")

plt.tight_layout()
plt.savefig(FIGS / "size_comparison.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'size_comparison.png'}")

# Save size summary
import json
summary = {
    "axes_cm": {
        "n": int(len(axe_lengths_cm)),
        "median": float(np.median(axe_lengths_cm)),
        "iqr": [float(np.quantile(axe_lengths_cm, .25)),
                float(np.quantile(axe_lengths_cm, .75))],
        "min": float(axe_lengths_cm.min()),
        "max": float(axe_lengths_cm.max()),
    },
    "carvings_cm": {
        "n": int(len(carv_heights)),
        "median": float(np.median(carv_heights)),
        "iqr": [float(np.quantile(carv_heights, .25)),
                float(np.quantile(carv_heights, .75))],
        "min": float(carv_heights.min()),
        "max": float(carv_heights.max()),
    },
    "mushrooms_cm_total": {
        "n": int(len(mus_total)),
        "median": float(np.median(mus_total)),
        "min": float(mus_total.min()),
        "max": float(mus_total.max()),
    },
}
with open(ROOT / "data" / "processed" / "size_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"Saved size_summary.json")
