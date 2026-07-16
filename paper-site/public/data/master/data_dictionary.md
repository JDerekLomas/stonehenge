# Data dictionary

This document defines every column in every master dataset published with
this paper. Values traced back to the source they were originally
measured in.

## Sources cited
- **Bevan All data** — sheet "All data" of `Early Axes from Bevan.xlsx`. ImageJ
  measurements produced by A. Bevan (UCL, unpublished) on canonical
  400-pixel-tall silhouettes of axes, carvings, and mushrooms. Units are
  pixels for size features; dimensionless for shape features.
- **Bevan ea metadata** — sheet "ea" of the same workbook. 7,308-row
  metadata table from PAS/museum records: findspots, physical
  measurements in mm, catalogue IDs, typology.
- **Bevan Corpus** — sheet "Corpus" of the same workbook. 292-row curated
  subset with hand-coded flags (Recurve, Flair, Flat, Round, pointed)
  and Needham type numbers.
- **Lomas 2021 ImageJ** — sheet "Carvings" of `Stone 53 Measurements.xlsx`,
  produced during the author's 2021 analysis pass using ImageJ. Units
  are cm for size features.
- **Extracted this study** — feature values computed by scripts in this
  repository (see `scripts/35_extract_stone4.py`, `scripts/32_ricruin_validation.py`,
  and `scripts/38_extended_features.py`). Uses scikit-image regionprops
  and, where noted, pyefd or cv2. Pipeline validated against Lomas 2021:
  Circularity, Aspect Ratio, Solidity match at r > 0.99; Roundness
  shows a systematic offset (mean -0.19, r = 0.91) reflecting a
  fitted-ellipse convention difference.
- **English Heritage 2012** — Abbott & Anderson-Whymark's *Stonehenge
  Laser Scan: Archaeological Analysis Report*, Historic England Research
  Report 32-2012. Source of F-numbers, per-stone counts, dating claims.

---

## `master_axes.csv` (n = 340)

One row per axe. Joined on `artefact_id` across three Bevan sheets.

| Column | Type | Source | Description |
|---|---|---|---|
| `artefact_id` | int | Bevan All data (Label) | Unique axe ID. Also the join key for the Bevan ea and Corpus sheets. |
| `image` | str | Bevan All data | Original image filename (e.g. `1002.tif`). |
| `area_px`, `perim_px` | float | Bevan All data | Area (px²) and perimeter (px) on the 400-pixel-tall canonical silhouette. |
| `width_px`, `height_px` | float | Bevan All data | Bounding-box dimensions in pixels. |
| `circularity` | float [0,1] | Bevan All data | 4π · Area / Perimeter². 1.0 = perfect circle. |
| `aspect_ratio` | float ≥ 1 | Bevan All data | Major axis / minor axis of the fitted ellipse. 1.0 = circle. |
| `roundness` | float [0,1] | Bevan All data | 4 · Area / (π · MajorAxis²). 1.0 = circle. |
| `solidity` | float [0,1] | Bevan All data | Area / ConvexHullArea. 1.0 = convex shape. |
| `needham_L`, `needham_LB`, `needham_WB`, `needham_W2`, `needham_W3`, `needham_WE`, `needham_LC`, `needham_DE`, `needham_MO` | float | Bevan All data | Needham 1983 linear measurements. See paper §2.2 and figure 3d for definitions. |
| `object` | str | Bevan ea | Object description ("Flat Axe", "Flanged Axe", etc). |
| `material` | str | Bevan ea | Metal composition where recorded. |
| `basic_type` | str | Bevan ea | Needham class (`Class 2`, `Class 3`, `Class 4`, `Class 5`, or transitional). |
| `suggested_type`, `published_types` | str | Bevan ea | Typology metadata from published catalogues. |
| `site_name`, `admin_region`, `country` | str | Bevan ea | Findspot location description. |
| `longitude`, `latitude` | float | Bevan ea | Findspot decimal-degrees coordinates where recorded. |
| `length_mm`, `blade_width_mm`, `butt_width_mm`, `weight_g` | float | Bevan ea | Real-world physical measurements. |
| `discovery_year` | int | Bevan ea | Year of discovery/report. |
| `hc_recurve`, `hc_flair`, `hc_flat`, `hc_round`, `hc_pointed` | 0/1 | Bevan Corpus | Hand-coded morphological flags (blade shows recurve; flair; etc). |
| `needham_number` | int | Bevan Corpus | Needham 1983 catalogue number for this axe. |

---

## `master_carvings.csv` (n = 222)

One row per carving. Four sources; every row tagged with `stone` and
`source` so subsets can be filtered.

| Column | Type | Source | Description |
|---|---|---|---|
| `carving_id` | str | source-specific | Stable identifier (`F595`, `s4_001`, `RiCruin1`, or Bevan Label). |
| `stone` | str | derived | Stone number (`53`, `4`, `RiCruin`, or `unknown` for Bevan All data rows where stone is not tagged). |
| `source` | str | derived | Provenance tag: `Lomas 2021 ImageJ`, `Extracted (this study, from Stone4.tiff)`, `Extracted (this study)` (Ri Cruin), or `Bevan All data (ImageJ)`. |
| `hc_recurve`, `hc_ring` | 0/1 | Lomas 2021 | Hand-coded flags (only for Stone 53 rows). |
| `hc_axe_note` | str | Lomas 2021 | Free-text note about the axe interpretation (Stone 53 rows only). |
| `area_px`, `perim_px`, `width_px`, `height_px` | float | Extracted or Bevan | Pixel-unit size measurements (for our extractions and Bevan). |
| `area_rel`, `perim_cm`, `width_cm`, `height_cm` | float | Lomas 2021 | Real-unit size measurements from Lomas 2021 (Stone 53 only). |
| `circularity`, `aspect_ratio`, `roundness`, `solidity` | float | source-specific | Dimensionless shape features. Definitions as for master_axes. |
| `lda_p_mushroom` | float [0,1] | Backfilled | LDA posterior P(mushroom) using axe-vs-mushroom classifier trained on Bevan All data (356 axes + 40 mushrooms), 95.7% CV accuracy. |
| `rf_p_mushroom` | float [0,1] | Backfilled | Random Forest posterior P(mushroom), same classifier, 96.0% CV accuracy. |
| `mahal_dist_to_axe_centroid` | float | Backfilled | Mahalanobis distance in standardized (Circ, AR, Roundness) space to the axe centroid. |
| `mahal_dist_to_mushroom_centroid` | float | Backfilled | Mahalanobis distance to the mushroom centroid. |
| `nearest_centroid` | str | Backfilled | `"mushroom"` if `mahal_dist_to_mushroom_centroid < mahal_dist_to_axe_centroid`, else `"axe"`. |

**Caveat on cross-source features**: LDA and RF predictions apply the
same classifier to features measured with different pipelines (Lomas
2021 ImageJ vs our-pipeline extraction). Where the pipelines differ
systematically (Roundness in particular), predictions may be biased.
See paper §3.6.pipeline_validation.

---

## `master_mushrooms.csv` (n = 62)

One row per mushroom silhouette.

| Column | Type | Source | Description |
|---|---|---|---|
| `mushroom_id` | str | source-specific | Stable identifier (Bevan Label, or filename). |
| `source` | str | derived | `Bevan All data (ImageJ)` or `Curated pre-segmented silhouettes`. |
| `area_px`, `perim_px`, `width_px`, `height_px` | float | source | Pixel-unit size measurements. |
| `circularity`, `aspect_ratio`, `roundness`, `solidity` | float | source | Dimensionless shape features. |

---

## `master_mushroom_species_reference.csv` (n = 15)

Reference table of candidate native British psilocybin-bearing mushroom
species. Source: sheet `Mushrooms` of `Mushroom Outlines Carvings.xlsx`.

| Column | Type | Description |
|---|---|---|
| `species` | str | Latin binomial. |
| `cap_size_cm` | float | Typical cap width in cm (from mycology references). |
| `stem_size_cm` | float | Typical stem length in cm. |
| `habitat` | str | Where this species is typically found in Britain (e.g. "pasture land", "cow/horse dung", "under old trees"). |
| `has_ring` | 0/1 | Whether the mature form has a stem annulus (ring) — a distinctive feature that could be reproduced in a carving. |
| `psilocybin_activity` | str | Reported psilocybin activity level (e.g. "Strong", "Moderately Active", "Mild", "Unknown"). |

---

## Coverage summary

| Field | # rows with value | Notes |
|---|---|---|
| **master_axes**: `basic_type` | 319 / 340 | Needham class label |
| **master_axes**: `length_mm` | 307 / 340 | Physical measurement |
| **master_axes**: `hc_recurve` | 216 / 340 | Hand-coded flag from Bevan Corpus |
| **master_axes**: `longitude` | 275 / 340 | Findspot coordinates |
| **master_carvings**: `hc_recurve` | 41 / 222 | Only Stone 53 has hand-coded flags |
| **master_carvings**: `height_cm` | 41 / 222 | Only Lomas 2021 has cm-scale |
| **master_carvings**: `lda_p_mushroom` | ~222 | All rows with shape features backfilled |
