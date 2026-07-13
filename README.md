# Stonehenge Carvings — Shape Analysis (Session 2026-07-13)

Companion analysis to Lomas et al., *"Using Computational Similarity Metrics to Gain Insight Into the Origins of Stonehenge Carvings"* (draft, Google Doc `1ydIyGX7T17fp205GipBXMEN12hc8JTP2GEKYquTzJvI`).

This session revisited a pre-tenure paper that had been shelved because the dean advised against publishing it. The paper argues the Stonehenge carvings — traditionally identified as Bronze Age axeheads (Atkinson 1953) — may instead depict *Amanita muscaria* mushrooms. This is the kind of career-defining claim best made from tenure.

Now the goal is to strengthen the methodology and statistics before revival.

## Findings so far (2026-07-13)

### 1. The recurve feature (paper's strongest signal)

Reproduced and tightened the paper's headline count:

| Set | Recurve | n | Rate | 95% CI |
|---|---|---|---|---|
| Stone 53 carvings | 13 | 41 | 31.7% | 19.6% – 47.0% |
| Stone 4 carvings | 24 | 60 | 40.0% | 28.6% – 52.6% |
| All Stonehenge carvings | 37 | 101 | 36.6% | 27.9% – 46.4% |
| British EBA axes | 7 | 105 | 6.7% | 3.3% – 13.1% |

**Combined test:** Fisher exact p = 1.28×10⁻⁷, odds ratio 8.1, Cohen's h = 0.78 (medium), Bayesian P(carving rate > axe rate) > 0.9999.

*A. muscaria* caps recurve/incurve as they mature — outer margin curls inward, exposing the underside. The morphological match is direct.

Files: `scripts/01_recurve_analysis.py`, `data/processed/recurve_results.json`, `figures/recurve_comparison.{png,pdf}`.

### 2. Aspect ratio (single-feature result, cleanest to interpret)

British EBA axes are functional tools with aspect ratio constrained by hafting geometry (grip length + blade length). If the carvings are meant to depict axes, a skilled carver reproducing the form should reproduce the elongation. They do not.

| Set | n | AR mean ± sd | AR range |
|---|---|---|---|
| British EBA axes | 124 | 2.71 ± 0.42 | 1.65 – 4.53 |
| Stone 53 carvings | 41 | 1.76 ± 0.76 | 1.08 – 5.37 |

- Mean difference: −0.95, 95% bootstrap CI [−1.17, −0.68]
- **Cohen's d = −1.53** (very large effect)
- Kolmogorov-Smirnov D = 0.73, p = 2×10⁻¹⁶
- **68% (28/41) of Stone 53 carvings are less elongated than the least elongated 2.5% of real bronze axes.** Only 27% fall inside the axe 95% range at all.

Files: `scripts/05_aspect_ratio_focused.py`, `data/processed/aspect_ratio_summary.json`.

### 3. Shape-space distance (multivariate)

Projected 41 Stone 53 carvings into the same 4-dimensional dimensionless shape space (circularity, aspect ratio, roundness, solidity) as 124 British EBA axes from the Bevan corpus. Used Mahalanobis distance from the axe centroid.

**Caveat: the 4 features carry only ~2 effective dimensions.** Aspect ratio and roundness are correlated at r = −0.965 in the axe corpus (they're near-deterministically related for smooth convex shapes); circularity and solidity at r = 0.94. The multivariate test is more powerful but less interpretable than the single-feature aspect-ratio test above; both give the same qualitative answer.

| Metric | British EBA axes | Stone 53 carvings |
|---|---|---|
| Mean Mahalanobis D | 1.72 | 10.96 |
| Median Mahalanobis D | 1.46 | 9.70 |
| Inside 95% axe ellipsoid | 90.3% (112/124) | **14.6% (6/41)** |
| Inside 99% axe ellipsoid | ≈97% | 14.6% (6/41) |

**Mann-Whitney U:** p = 1.5×10⁻¹⁹ that carvings are farther from the axe centroid than axes are.

**Univariate discrimination (Welch's t, FDR-corrected):**
- Circularity: not different (q = 0.26)
- Aspect ratio: q < 0.001 — axes 2.70 ± 0.42, carvings 1.76 ± 0.76 (carvings are ~35% less elongated)
- Roundness: q < 0.001 — axes 0.38 ± 0.06, carvings 0.64 ± 0.18 (carvings are ~70% rounder)
- Solidity: q < 0.001 — axes 0.79 ± 0.07, carvings 0.70 ± 0.10 (carvings have more concavities)

The model correctly places 90% of real axes inside the 95% ellipsoid — the pipeline works. So the finding that 85% of Stone 53 carvings fall *outside* that ellipsoid is not a modeling artifact. At the level of these four canonical shape descriptors, the carvings do not look like bronze axeheads.

Files: `scripts/03_shape_space_analysis.py`, `scripts/04_shape_space_figure.py`, `data/processed/carvings_axe_distance.csv`, `data/processed/shape_space_summary.json`, `figures/mahalanobis_histogram.{png,pdf}`, `figures/shape_space_scatter.{png,pdf}`.

### 4. Important methodological caveat

The Bevan corpus uses pixel-scale ImageJ measurements on 400×500 silhouettes; the carving spreadsheet appears to use fractionally-normalized measurements. The size-dependent features (area, perimeter, height, width) therefore **cannot** be directly compared — the analyses above use only the four scale-invariant features. This is a real methodological point and should be flagged prominently in any revision. A future step is to re-run ImageJ on the raw Stone 53 laser-scan silhouettes in the F595–F720 TIFFs (the "Stone 53 Carvings" Drive folder) with matched normalization.

## What's in this repo

```
stonehenge/
├── README.md                       ← this file
├── data/
│   ├── raw/                        ← CSVs pulled from Drive
│   │   ├── rock_carvings_and_axeheads.csv     (41 Stone 53 + 6 Ri Cruin)
│   │   ├── early_axes_bevan.csv               (113 axes, ImageJ features)
│   │   └── eba_axeheads_basic_dataset.csv     (108 axes w/ Needham typology)
│   └── processed/
│       ├── recurve_results.json
│       ├── shape_space_summary.json
│       └── carvings_axe_distance.csv          ← per-carving distance
├── figures/
│   ├── recurve_comparison.{png,pdf}
│   ├── mahalanobis_histogram.{png,pdf}
│   └── shape_space_scatter.{png,pdf}
├── scripts/
│   ├── 01_recurve_analysis.py
│   ├── 02_recurve_figure.py
│   ├── 03_shape_space_analysis.py
│   └── 04_shape_space_figure.py
├── prereg/
│   └── preregistration.md          ← OSF-ready draft
├── human-study/
│   └── protocol.md                 ← Prolific + expert study design
└── paper/                          ← empty, for future revision
```

### 5. Three-way shape comparison (added later in the same session)

For the first time, tested the paper's central claim directly: are the carvings closer to mushrooms or to axes in the shape-feature space?

**Reference sets:**
- 124 British EBA axes (Bevan corpus, ImageJ features)
- 55 *Amanita muscaria* silhouettes (iNaturalist research-grade, auto-segmented via color threshold + convex-hull fill; details in `scripts/06_fetch_muscaria.py`, `scripts/06b_resegment_muscaria.py`)
- 41 Stone 53 carvings

**Features:** Circularity, Aspect Ratio, Roundness. Solidity was excluded because the automated color-based segmentation of A. muscaria required convex-hull filling to handle white cap spots, artificially inflating mushroom Solidity to 0.945 vs. real ImageJ silhouettes. A future revision needs SAM-based segmentation to include Solidity honestly.

**Descriptive statistics (means):**

| Feature | Axes | Carvings | *A. muscaria* |
|---|---|---|---|
| Circularity | 0.49 | 0.47 | 0.54 |
| Aspect Ratio | **2.71** | **1.76** | **1.81** |
| Roundness | **0.38** | **0.64** | **0.60** |

Carvings and mushrooms are indistinguishable on these three features. Axes are systematically different.

**Mahalanobis nearest-class:** 40 of 41 (**97.6%**) Stone 53 carvings are closer to the mushroom centroid than the axe centroid. Median distance to axe centroid: 9.57; to mushroom centroid: 1.05.

**Classifier validation and prediction:**

| Classifier | 5-fold CV accuracy on axe-vs-mushroom | Stone 53 predicted mushroom | Mean P(mushroom) |
|---|---|---|---|
| LDA | 0.855 ± 0.047 | 30/41 (73.2%) | 0.709 |
| Random Forest | 0.916 ± 0.039 | 31/41 (75.6%) | 0.763 |

Both classifiers agree with the mushroom hypothesis. The three features contribute roughly equally to the RF classifier (importance ≈ 0.33 each).

Files: `scripts/06_fetch_muscaria.py`, `scripts/06b_resegment_muscaria.py`, `scripts/07_extract_muscaria_features.py`, `scripts/08_three_way_comparison.py`, `scripts/09_three_way_figure.py`, `data/muscaria_corpus/`, `data/processed/three_way_predictions.csv`, `data/processed/three_way_summary.json`, `figures/three_way_violin.{png,pdf}`, `figures/three_way_scatter.{png,pdf}`.

## Where the argument stands right now

The paper's central claim can now be defended with four converging statistical results, in decreasing order of interpretability:

1. **Aspect ratio (cleanest)** — 68% of Stone 53 carvings are less elongated than the *least elongated* 2.5% of British EBA axes. Cohen's d = −1.53 (very large), KS p = 2×10⁻¹⁶. Axes are functional tools with hafting-constrained proportions; a skilled carver reproducing an axe would not systematically flatten it.

2. **Recurve feature** — the paper's original observation, now tested properly. Recurve rate on carvings is 5–6× higher than on real EBA axes (all Stonehenge carvings vs. axes: 37% vs 7%, Fisher exact p = 1.3×10⁻⁷, OR = 8.1). This is exactly the direction expected if the carvings depict *A. muscaria* caps rather than blades.

3. **Multivariate shape space** — 85% of Stone 53 carvings fall outside the 95% axe-cluster ellipsoid (Mann-Whitney p = 10⁻¹⁹). Robust across every subset of the four dimensionless features tested.

4. **Three-way comparison with real mushroom data** — 97.6% of carvings closer to *A. muscaria* centroid than axe centroid. Both LDA and Random Forest classifiers (trained on real axe + real mushroom silhouettes) classify ~75% of Stone 53 carvings as mushroom with mean confidence 0.71–0.76. The test itself is validated by the classifiers' 85–92% CV accuracy on the axe-vs-mushroom training data.

Neither of these results *proves* the mushroom hypothesis. What they do is **shift the burden of proof.** The axehead interpretation was never quantitatively tested — Atkinson eyeballed the two most distinctive carvings on Stone 53 in 1953 and named them axes. Since then, 113 more carvings have been discovered by laser scan and the identification has just been extended. This shape analysis is the first time anyone has actually tested whether the carvings, as a corpus, match the shape distribution of real EBA axes. They do not.

## Next steps (roughly in priority order)

- [ ] **Reprocess the Stone 53 TIFFs** in ImageJ with matched normalization to the Bevan corpus, so size-dependent features are comparable. This is the single most important methodological fix.
- [ ] **Curate the alternative reference sets** — halberds, sickles, palstaves, cup-and-ring vulva motifs, sun/moon symbols, beaker pot cross-sections, generic silhouettes. Extract shape features per the same pipeline.
- [ ] **Curate the *A. muscaria* silhouette corpus** per the protocol in `prereg/preregistration.md` §4.1 (stratified across button/egg/expanded/reflexed stages; iNaturalist research-grade; automated segmentation).
- [ ] **Post the preregistration to OSF** before running the final multi-class analysis.
- [ ] **Launch the Prolific human-perception study** (`human-study/protocol.md`) — cheap (~$500), fast (2 weeks), and independent of any classifier choice.
- [ ] **Build the multi-class classifier** — random forest + gradient-boosted, 5-fold CV, confusion matrix, per-carving prediction + top-3 nearest reference exemplars.
- [ ] **Bring in an archaeologist coauthor** — Andy Bevan (UCL, owns the axe corpus) or someone at the British Museum with rock-art experience. Their name reduces the "outsider claim" risk substantially.
- [ ] **Split the paper in two**: methods paper first (JAS: Reports or similar), interpretive paper second, once the pipeline is peer-accepted.

## Dependencies

Python ≥ 3.10 with: `numpy`, `pandas`, `scipy` (≥ 1.11 for `false_discovery_control`), `matplotlib`.
