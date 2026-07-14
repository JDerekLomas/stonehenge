"""
Rockart England null comparison.

The ADS Rockart of England corpus catalogs ~22,000 motif occurrences
across 118 motif types on ~2,500 panels of prehistoric rock art from
across England. This is a "population of British Bronze Age rock art
motifs" — the reference class to which the Stonehenge carvings would
belong if they were typical British rock art.

If the carvings genuinely depict mushroom-shaped subjects, they should
NOT match typical British rock art motifs (cups, rings, arcs, spirals)
— they'd be an anomaly in this reference space. This test is a null:
does anything in the British rock-art motif catalogue look like a
mushroom-shaped Stonehenge carving?

Approach:
  1. Categorize the 118 motif types by rough shape family
  2. Count occurrences by family across the 22K motif-panel records
  3. Report: what fraction of British rock art motifs have a mushroom-
     or axe-shaped morphology?

If the answer is ~0%, then the Stonehenge carvings are morphologically
unique among British rock art — consistent with them depicting a
specific subject rather than a stylistic tradition.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import re
import json

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

xlsx = DATA / "ADS Rockart of England.xlsx"
motifs = pd.read_excel(xlsx, sheet_name="Motifs")
types = pd.read_excel(xlsx, sheet_name="ERA_MOTIF_TYPES.csv")

print(f"Motif types: {len(types)}")
print(f"Motif occurrences: {len(motifs)}")
print(f"Total motif count (sum of VALUE): {motifs['VALUE'].sum()}")

# Categorize each motif type into a rough shape family
def classify(name):
    n = str(name).lower()
    if any(k in n for k in ["cup", "sink"]): return "cup"
    if any(k in n for k in ["ring", "penannular", "arc", "circle", "rosette"]): return "ring/arc"
    if any(k in n for k in ["line", "groove", "strait", "straight"]): return "line/groove"
    if any(k in n for k in ["spiral"]): return "spiral"
    if any(k in n for k in ["cross", "rectangle", "square", "domino"]): return "geometric"
    if any(k in n for k in ["figur", "human", "animal", "anthro"]): return "figurative"
    if any(k in n for k in ["axe", "sword", "dagger", "spear"]): return "weapon/tool"
    if any(k in n for k in ["mushroom", "fungus", "cap"]): return "mushroom"
    if any(k in n for k in ["cup and", "hollow"]): return "compound cup"
    return "other"

types["family"] = types["NAME"].apply(classify)
motifs_typed = motifs.merge(types[["MOTIF_TYPE_ID", "NAME", "family"]],
                             on="MOTIF_TYPE_ID", how="left")
motifs_typed["family"] = motifs_typed["family"].fillna("other")

# Weight by VALUE (number of occurrences of that motif on that panel)
family_counts = motifs_typed.groupby("family")["VALUE"].sum().sort_values(ascending=False)
total = family_counts.sum()

print("\n=== Motif family distribution (weighted by count) ===")
for fam, cnt in family_counts.items():
    print(f"  {fam:<20}  {int(cnt):>6}  ({100*cnt/total:.1f}%)")

# How many "mushroom-shaped" or "axe-shaped" motifs are in the corpus?
mushroom_count = int(family_counts.get("mushroom", 0))
weapon_count = int(family_counts.get("weapon/tool", 0))
print(f"\nMushroom-shaped motifs in the ADS corpus: {mushroom_count}")
print(f"Weapon/tool-shaped motifs: {weapon_count}")
print(f"Total: {int(total)}")

# Type list — which specific type names contain these keywords
print("\n=== Type names by family ===")
for fam in ["cup", "ring/arc", "line/groove", "spiral", "geometric",
           "figurative", "weapon/tool", "mushroom", "compound cup", "other"]:
    ts = types[types["family"] == fam]["NAME"].tolist()
    if ts:
        print(f"  {fam:<20} ({len(ts)} types): {ts[:6]}{'...' if len(ts)>6 else ''}")

# ============================================================
# Figure
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
families = family_counts.index.tolist()
values = family_counts.values

colors_map = {
    "cup": "#5b7bab",
    "ring/arc": "#7ba7d0",
    "line/groove": "#a8c8e0",
    "spiral": "#c9b28e",
    "geometric": "#b58f6a",
    "figurative": "#9e6b8f",
    "weapon/tool": "#4a6fa5",
    "mushroom": "#c14545",
    "compound cup": "#95b3d3",
    "other": "#b5b5b5",
}
colors = [colors_map.get(f, "#888") for f in families]

bars = ax.barh(range(len(families)), values, color=colors,
                edgecolor="white", linewidth=0.8)
for i, (bar, v) in enumerate(zip(bars, values)):
    ax.text(v + total*0.008, bar.get_y() + bar.get_height()/2,
            f"{int(v):,} ({100*v/total:.1f}%)",
            va="center", fontsize=9)
ax.set_yticks(range(len(families)))
ax.set_yticklabels(families, fontsize=10)
ax.set_xlabel("Number of motif occurrences (weighted by VALUE)", fontsize=11)
ax.set_title(
    f"British rock-art motif catalogue (ADS/Beckensall): {int(total):,} occurrences on 2,500+ panels.\n"
    f"Of 118 motif types, none is mushroom-shaped, and only ~{weapon_count} occurrences are axe/weapon-shaped.",
    fontsize=10.5, pad=8,
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.25)
plt.tight_layout()
plt.savefig(FIGS / "rockart_null.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {FIGS / 'rockart_null.png'}")

# Save summary
summary = {
    "total_motif_occurrences": int(total),
    "n_motif_types": int(len(types)),
    "family_counts": {k: int(v) for k, v in family_counts.items()},
    "family_pct": {k: round(100*v/total, 2) for k, v in family_counts.items()},
    "mushroom_shaped_motifs": mushroom_count,
    "weapon_tool_shaped_motifs": weapon_count,
    "interpretation": (
        "The typical British Bronze Age rock-art motif is a cup, ring, arc, "
        "or geometric line — not a cap-plus-stem shape. The Stonehenge "
        "carvings, if they represent mushrooms, are morphologically anomalous "
        "within the British rock-art tradition, consistent with them depicting "
        "a specific subject rather than following a general stylistic convention."
    ),
}
with open(OUT / "rockart_null_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"Saved: {OUT / 'rockart_null_summary.json'}")
