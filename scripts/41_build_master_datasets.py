"""
Build three integrated master datasets:

  master_axes.csv       — every axe used anywhere in the analysis,
                          with every attribute we have for it, joined
                          on ArtefactID.
  master_carvings.csv   — every carving from Stones 53, 4, Ri Cruin,
                          Bevan carving corpus, plus our-pipeline
                          feature extractions and classifier predictions.
  master_mushrooms.csv  — every mushroom silhouette, joined with
                          the 15-species reference table where possible.

Also outputs a top-level dataset manifest describing each column.
"""

import json
import numpy as np
import pandas as pd
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
BEVAN = ROOT / "data" / "raw" / "Early Axes from Bevan.xlsx"
OUT = ROOT / "data" / "master"
OUT.mkdir(exist_ok=True)


def id_from_label(lbl):
    m = re.match(r"(\d+)", str(lbl))
    return int(m.group(1)) if m else None


# =============================================================
# MASTER AXES
# =============================================================
print("=== Building master_axes.csv ===")

# Base: All-data sheet — 356 axes with ImageJ features
allf = pd.read_excel(BEVAN, sheet_name="All data")
axes_all = allf[allf["Type"] == "Axe"].copy()
axes_all["ArtefactID"] = axes_all["Label"].apply(id_from_label)
axes_all = axes_all.dropna(subset=["ArtefactID"])
axes_all["ArtefactID"] = axes_all["ArtefactID"].astype(int)

# Rename to canonical
axes_master = axes_all[[
    "ArtefactID", "Label", "Area", "Perim.", "Width", "Height",
    "Circ.", "AR", "Round", "Solidity",
    "L", "DE", "LB", "WB", "W2", "W3", "WE", "LC", "MO",
]].copy()
axes_master.columns = [
    "artefact_id", "image", "area_px", "perim_px", "width_px", "height_px",
    "circularity", "aspect_ratio", "roundness", "solidity",
    "needham_L", "needham_DE", "needham_LB", "needham_WB",
    "needham_W2", "needham_W3", "needham_WE", "needham_LC", "needham_MO",
]

# Join ea metadata (typology, findspot, physical measurements)
ea = pd.read_excel(BEVAN, sheet_name="ea")
ea_slim = ea[[
    "ArtefactID", "Object", "Material", "BasicType", "SuggestedType",
    "PublishedTypes", "SiteNameFull", "AdminRegion", "Country",
    "Lon", "Lat", "Length", "BladeWidth", "ButtWidth", "Weight",
    "DiscoveryYear",
]].copy()
ea_slim.columns = [
    "artefact_id", "object", "material", "basic_type", "suggested_type",
    "published_types", "site_name", "admin_region", "country",
    "longitude", "latitude", "length_mm", "blade_width_mm",
    "butt_width_mm", "weight_g", "discovery_year",
]
axes_master = axes_master.merge(ea_slim, on="artefact_id", how="left")

# Also join Corpus sheet for hand-coded flags (Recurve, Flair, Flat, Round, pointed)
corp = pd.read_excel(BEVAN, sheet_name="Corpus")
corp_slim = corp[["ArtefactID", "Recurve", "Flair", "Flat", "Round",
                    "pointed", "Needham#"]].copy()
corp_slim.columns = ["artefact_id", "hc_recurve", "hc_flair", "hc_flat",
                      "hc_round", "hc_pointed", "needham_number"]
axes_master = axes_master.merge(corp_slim, on="artefact_id", how="left")

axes_master.to_csv(OUT / "master_axes.csv", index=False)
print(f"  Rows: {len(axes_master)}")
print(f"  Cols: {len(axes_master.columns)}")
print(f"  With basic_type: {axes_master['basic_type'].notna().sum()}")
print(f"  With length_mm:  {axes_master['length_mm'].notna().sum()}")
print(f"  With hc_recurve: {axes_master['hc_recurve'].notna().sum()}")
print(f"  Saved: {OUT / 'master_axes.csv'}")


# =============================================================
# MASTER CARVINGS
# =============================================================
print("\n=== Building master_carvings.csv ===")

carvings_rows = []

# Stone 53 (41): use Lomas 2021 ImageJ measurements
s53 = pd.read_excel(ROOT / "data" / "raw" / "Stone 53 Measurements.xlsx",
                     sheet_name="Carvings")
for _, r in s53.iterrows():
    cid = int(r["Carving#"]) if pd.notna(r["Carving#"]) else None
    if cid is None: continue
    carvings_rows.append({
        "carving_id": f"F{cid}",
        "stone": "53",
        "source": "Lomas 2021 ImageJ",
        "hc_recurve": int(r["Recurve"]) if pd.notna(r["Recurve"]) else 0,
        "hc_ring": int(r["Ring"]) if pd.notna(r["Ring"]) else 0,
        "hc_axe_note": r.get("Axe Note") if pd.notna(r.get("Axe Note")) else None,
        "area_rel": r["Area"] if pd.notna(r["Area"]) else None,
        "perim_cm": r["Perimeter"] if pd.notna(r["Perimeter"]) else None,
        "width_cm": r["Width"] if pd.notna(r["Width"]) else None,
        "height_cm": r["Height"] if pd.notna(r["Height"]) else None,
        "circularity": r["Circularity"] if pd.notna(r["Circularity"]) else None,
        "aspect_ratio": r["Aspect Ratio"] if pd.notna(r["Aspect Ratio"]) else None,
        "roundness": r["Roundness"] if pd.notna(r["Roundness"]) else None,
        "solidity": r["Solidity"] if pd.notna(r["Solidity"]) else None,
    })

# Stone 4 (56): our own extraction
s4 = pd.read_csv(ROOT / "data" / "stone4_extracted" / "stone4_features.csv")
for _, r in s4.iterrows():
    carvings_rows.append({
        "carving_id": r["id"],
        "stone": "4",
        "source": "Extracted (this study, from Stone4.tiff)",
        "area_px": r["Area"],
        "perim_px": r["Perimeter"],
        "width_px": r["Width"],
        "height_px": r["Height"],
        "circularity": r["Circularity"],
        "aspect_ratio": r["Aspect Ratio"],
        "roundness": r["Roundness"],
        "solidity": r["Solidity"],
    })

# Ri Cruin (6): our extraction
ric_summary = json.load(open(ROOT / "data" / "processed" / "ricruin_summary.json"))
for r in ric_summary["per_carving"]:
    carvings_rows.append({
        "carving_id": r["id"],
        "stone": "RiCruin (Kilmartin cairn, comparison site)",
        "source": "Extracted (this study)",
        "circularity": r["Circularity"],
        "aspect_ratio": r["Aspect Ratio"],
        "roundness": r["Roundness"],
        "solidity": r["Solidity"],
        "mahal_d_axe": r["d_axe"],
        "mahal_d_mushroom": r["d_mushroom"],
        "lda_p_mushroom": r["lda_p_mushroom"],
        "closer_to": r["closer_to"],
    })

# Bevan All-data carvings (119): to give a machine-readable full-corpus record
bevan_carv = allf[allf["Type"] == "Carving"].copy()
bevan_carv["ArtefactID"] = bevan_carv["Label"].apply(id_from_label)
for _, r in bevan_carv.iterrows():
    carvings_rows.append({
        "carving_id": r["Label"],
        "stone": "unknown (Bevan All data — stone not tagged)",
        "source": "Bevan All data (ImageJ)",
        "area_px": r["Area"],
        "perim_px": r["Perim."],
        "width_px": r["Width"],
        "height_px": r["Height"],
        "circularity": r["Circ."],
        "aspect_ratio": r["AR"],
        "roundness": r["Round"],
        "solidity": r["Solidity"],
    })

carvings_master = pd.DataFrame(carvings_rows)
# Reorder columns for readability
col_order = [
    "carving_id", "stone", "source",
    "hc_recurve", "hc_ring", "hc_axe_note",
    "area_px", "perim_px", "width_px", "height_px",
    "area_rel", "perim_cm", "width_cm", "height_cm",
    "circularity", "aspect_ratio", "roundness", "solidity",
    "mahal_d_axe", "mahal_d_mushroom", "lda_p_mushroom", "closer_to",
]
carvings_master = carvings_master.reindex(columns=col_order)
carvings_master.to_csv(OUT / "master_carvings.csv", index=False)
print(f"  Rows: {len(carvings_master)}")
by_stone = carvings_master["stone"].value_counts()
for st, ct in by_stone.items():
    print(f"    Stone {st}: {ct}")
print(f"  Saved: {OUT / 'master_carvings.csv'}")


# =============================================================
# MASTER MUSHROOMS
# =============================================================
print("\n=== Building master_mushrooms.csv ===")

mus_rows = []

# Bevan All-data mushrooms (40)
bevan_mus = allf[allf["Type"] == "Mushroom"].copy()
for _, r in bevan_mus.iterrows():
    mus_rows.append({
        "mushroom_id": r["Label"],
        "source": "Bevan All data (ImageJ)",
        "area_px": r["Area"],
        "perim_px": r["Perim."],
        "width_px": r["Width"],
        "height_px": r["Height"],
        "circularity": r["Circ."],
        "aspect_ratio": r["AR"],
        "roundness": r["Round"],
        "solidity": r["Solidity"],
    })

# Curated pre-segmented silhouettes (22) — read the clean_features CSV
clean_mus = pd.read_csv(ROOT / "data" / "clean_corpus" / "clean_features.csv")
clean_mus = clean_mus[clean_mus["source"] == "mushroom"]
for _, r in clean_mus.iterrows():
    mus_rows.append({
        "mushroom_id": r["id"],
        "source": "Curated pre-segmented silhouettes",
        "area_px": r["Area"],
        "perim_px": r["Perimeter"],
        "width_px": r["Width"],
        "height_px": r["Height"],
        "circularity": r["Circularity"],
        "aspect_ratio": r["Aspect Ratio"],
        "roundness": r["Roundness"],
        "solidity": r["Solidity"],
    })

mushrooms_master = pd.DataFrame(mus_rows)
mushrooms_master.to_csv(OUT / "master_mushrooms.csv", index=False)
print(f"  Rows: {len(mushrooms_master)}")
print(f"  Saved: {OUT / 'master_mushrooms.csv'}")

# Also copy the species reference table (15 species with sizes/habitat/activity)
species_ref = pd.read_excel(
    ROOT / "data" / "raw" / "Mushroom Outlines Carvings.xlsx",
    sheet_name="Mushrooms"
).dropna(subset=["Species"])
species_ref = species_ref[["Species", "Cap Size", "Stem Size", "Habitat",
                            "Ring", "Activity"]]
species_ref.columns = ["species", "cap_size_cm", "stem_size_cm",
                        "habitat", "has_ring", "psilocybin_activity"]
species_ref.to_csv(OUT / "master_mushroom_species_reference.csv", index=False)
print(f"  Species reference table: {len(species_ref)} rows")
print(f"  Saved: {OUT / 'master_mushroom_species_reference.csv'}")


# =============================================================
# DATASET MANIFEST
# =============================================================
print("\n=== Writing dataset manifest ===")

manifest = {
    "datasets": {
        "master_axes.csv": {
            "description": "Every British Early Bronze Age axehead with ImageJ shape features, Needham typology labels, physical measurements, and findspot coordinates where available.",
            "n_rows": len(axes_master),
            "columns_grouped": {
                "id": ["artefact_id", "image"],
                "shape_pixel_units": ["area_px", "perim_px", "width_px", "height_px"],
                "shape_dimensionless": ["circularity", "aspect_ratio", "roundness", "solidity"],
                "needham_measurements": ["needham_L", "needham_LB", "needham_WB", "needham_W2", "needham_W3", "needham_WE", "needham_LC", "needham_DE", "needham_MO"],
                "typology": ["object", "basic_type", "suggested_type", "published_types", "needham_number"],
                "findspot": ["site_name", "admin_region", "country", "longitude", "latitude"],
                "physical_measurements_mm": ["length_mm", "blade_width_mm", "butt_width_mm", "weight_g"],
                "metadata": ["material", "discovery_year"],
                "hand_coded_flags": ["hc_recurve", "hc_flair", "hc_flat", "hc_round", "hc_pointed"],
            },
        },
        "master_carvings.csv": {
            "description": "Every Stonehenge (and Ri Cruin) carving analyzed, from all four data sources, with source and stone attribution.",
            "n_rows": len(carvings_master),
            "sources": {
                "Stone 53 (Lomas 2021 ImageJ)": int((carvings_master["source"] == "Lomas 2021 ImageJ").sum()),
                "Stone 4 (extracted this study)": int((carvings_master["source"] == "Extracted (this study, from Stone4.tiff)").sum()),
                "Ri Cruin (extracted this study)": int((carvings_master["source"] == "Extracted (this study)").sum()),
                "Bevan All data (ImageJ)": int((carvings_master["source"] == "Bevan All data (ImageJ)").sum()),
            },
        },
        "master_mushrooms.csv": {
            "description": "Mushroom silhouettes with shape features. Two sources: Bevan ImageJ measurements (40) and curated pre-segmented silhouettes (22).",
            "n_rows": len(mushrooms_master),
        },
        "master_mushroom_species_reference.csv": {
            "description": "Reference table of 15 native British psilocybin-bearing mushroom species with cap/stem sizes, habitat, ring presence, and psilocybin activity level.",
            "n_rows": len(species_ref),
        },
    },
}
with open(OUT / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"  Saved: {OUT / 'manifest.json'}")

print("\nAll master datasets built.")
