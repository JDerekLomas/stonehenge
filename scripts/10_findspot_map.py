"""
Map of EBA axe findspots colored by Needham class, with Stonehenge marked.

Directly visualizes the paper's argument: of ~88 Class 5 axes (the only
axes contemporary with the carving date range), very few were found near
Stonehenge — most come from the Thames Valley, East Anglia, and the SW
peninsula. If the carvers had been reproducing local axes, we'd expect
the distribution of nearby axes to match the carvings.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
FIGS = ROOT / "figures"

STONEHENGE_LAT = 51.1789
STONEHENGE_LON = -1.8262

# Rough "near Stonehenge" radius: 100 km
NEAR_KM = 100.0


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = np.radians(lat1); phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1); dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlam / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


df = pd.read_csv(DATA / "eba_axeheads_basic_dataset.csv")
df["dist_km"] = haversine_km(STONEHENGE_LAT, STONEHENGE_LON, df["Lat"], df["Lon"])
df["near_stonehenge"] = df["dist_km"] <= NEAR_KM

print("=== Axe findspots by Needham class ===\n")
print(df["BasicType"].value_counts().sort_index())
print()
print(f"Within {NEAR_KM} km of Stonehenge:")
print(df[df["near_stonehenge"]]["BasicType"].value_counts().sort_index())
print()

# Percentage per class within Stonehenge radius
print(f"=== % within {NEAR_KM} km by class ===")
for cls in ["Class 2", "Class 3", "Class 4", "Class 5"]:
    sub = df[df["BasicType"] == cls]
    if len(sub) == 0:
        continue
    n_near = int(sub["near_stonehenge"].sum())
    print(f"  {cls}: {n_near}/{len(sub)} = {100*n_near/len(sub):.1f}% near Stonehenge")

# ============================================================
# Map figure
# ============================================================
class_colors = {
    "Class 2": "#2c7fb8",   # blue
    "Class 3": "#41b6c4",   # teal
    "Class 4": "#a1dab4",   # green
    "Class 5": "#fdae61",   # orange
}
class_labels = {
    "Class 2": "Class 2 (Flat, ~2200-1900 BC)",
    "Class 3": "Class 3 (Flat, ~2000-1750 BC)",
    "Class 4": "Class 4 (Low-flanged, ~1800-1600 BC)",
    "Class 5": "Class 5 (Flanged, ~1700-1450 BC)",
}

fig, ax = plt.subplots(figsize=(9, 10))

# Rough Britain outline via lat/lon bounds
ax.set_xlim(-6.5, 2.0)
ax.set_ylim(49.5, 55.5)
ax.set_facecolor("#f4f4f4")

# Approximate coastline from world-borders isn't available; instead
# draw simple rectangles for context
ax.plot([], [])  # placeholder

# Plot axes by class
for cls in ["Class 2", "Class 3", "Class 4", "Class 5"]:
    sub = df[df["BasicType"] == cls]
    ax.scatter(sub["Lon"], sub["Lat"],
               c=class_colors[cls], s=45, alpha=0.75,
               edgecolor="white", linewidth=0.5,
               label=f"{class_labels[cls]} (n={len(sub)})")

# Stonehenge marker
ax.plot(STONEHENGE_LON, STONEHENGE_LAT, marker="*",
        color="#c14545", markersize=22, markeredgecolor="black",
        markeredgewidth=1, label="Stonehenge", zorder=10)
ax.annotate("STONEHENGE", (STONEHENGE_LON, STONEHENGE_LAT),
            xytext=(-1.7, 51.6), fontsize=10, fontweight="bold",
            color="#c14545", ha="left")

# 100 km radius circle
theta = np.linspace(0, 2 * np.pi, 100)
km_per_deg_lat = 111.0
km_per_deg_lon = 111.0 * np.cos(np.radians(STONEHENGE_LAT))
circle_lon = STONEHENGE_LON + (NEAR_KM / km_per_deg_lon) * np.cos(theta)
circle_lat = STONEHENGE_LAT + (NEAR_KM / km_per_deg_lat) * np.sin(theta)
ax.plot(circle_lon, circle_lat, color="#c14545", linestyle="--",
        linewidth=1.2, alpha=0.7, label=f"{int(NEAR_KM)} km radius")

ax.set_xlabel("Longitude (°E)", fontsize=11)
ax.set_ylabel("Latitude (°N)", fontsize=11)
ax.set_title("Distribution of British EBA axe findspots by Needham class\n"
             "Few Class 5 axes (contemporary with carvings) were found near Stonehenge",
             fontsize=11.5, pad=12)
ax.legend(loc="upper left", fontsize=8.5, frameon=True, facecolor="white",
          edgecolor="#dddddd")
ax.set_aspect("auto")
ax.grid(alpha=0.25)

plt.tight_layout()
plt.savefig(FIGS / "findspot_map.png", dpi=200, bbox_inches="tight")
plt.savefig(FIGS / "findspot_map.pdf", bbox_inches="tight")
plt.close()

# ============================================================
# Also emit GeoJSON for the web version
# ============================================================
features = []
for _, r in df.iterrows():
    features.append({
        "type": "Feature",
        "properties": {
            "artefact_id": int(r["ArtefactID"]),
            "object": str(r["Object"]),
            "class": str(r["BasicType"]),
            "site": str(r["SiteNameFull"]),
            "county": str(r["County"]),
            "region": str(r["Region"]),
            "dist_km_from_stonehenge": round(float(r["dist_km"]), 1),
            "near_stonehenge": bool(r["near_stonehenge"]),
        },
        "geometry": {
            "type": "Point",
            "coordinates": [float(r["Lon"]), float(r["Lat"])],
        },
    })

geojson = {
    "type": "FeatureCollection",
    "features": features,
    "stonehenge": {"lat": STONEHENGE_LAT, "lon": STONEHENGE_LON},
    "near_radius_km": NEAR_KM,
}

with open(OUT / "axe_findspots.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print(f"\nSaved: {FIGS / 'findspot_map.png'}")
print(f"Saved: {OUT / 'axe_findspots.geojson'}")
