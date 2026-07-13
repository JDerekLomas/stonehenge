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

### 2. Shape-space distance (new — not in the paper)

Projected 41 Stone 53 carvings into the same 4-dimensional dimensionless shape space (circularity, aspect ratio, roundness, solidity) as 124 British EBA axes from the Bevan corpus. Used Mahalanobis distance from the axe centroid.

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

### 3. Important methodological caveat

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

## Where the argument stands right now

The paper's central claim can now be defended with two independent statistical results:

1. **Feature-level** — the recurve rate on the carvings is 5-6× higher than on real EBA axes (p = 10⁻⁷). The single most diagnostic axe-shape feature is systematically overrepresented on carvings in a direction that matches mushroom morphology.

2. **Shape-space level** — 85% of Stone 53 carvings fall outside the 95% axe-cluster ellipsoid, with p = 10⁻¹⁹. They are systematically rounder, less elongated, and less solid than actual axes.

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
