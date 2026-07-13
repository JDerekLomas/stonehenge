# Preregistration: Shape analysis of Stonehenge carvings

**Authors:** J. Derek Lomas (TU Delft) [+ archaeology coauthor TBD]
**Date drafted:** 2026-07-13
**Registration platform:** OSF (target)
**Status:** Draft — not yet posted

---

## 1. Research question

What class of real-world object best explains the shape of the ~115 prehistoric carvings on Stonehenge (Stones 3, 4, 5, and 53)?

The canonical identification since Atkinson (1953) has been **British Early Bronze Age (EBA) bronze axeheads, blade-up, c. 1650–1400 BC.** This preregistered study tests that identification quantitatively against alternative shape references — including the null hypothesis that the carvings do not resemble EBA axeheads more than they resemble other candidate referents.

## 2. Hypotheses (registered before final analysis)

**H1 (canonical):** Each Stonehenge carving is closer, in a multidimensional shape space, to the centroid of British EBA axeheads (Needham 1983 corpus) than to any other reference class.

**H2 (feature-level canonical):** The distribution of hand-coded shape features (recurve, ring/annulus, flared bottom, flat bottom, rounded edge, sharp bottom) in the carvings is statistically indistinguishable from the same distribution in the British EBA axe corpus.

**H3 (alternative — mushroom):** The carvings are closer, in shape space, to the centroid of *Amanita muscaria* silhouettes than to any other reference class, including EBA axeheads.

**H4 (alternative — other):** The carvings are closer to at least one other reference class (halberds, sickles, palstaves, cup-and-ring motifs, sun/moon symbols, beaker pottery cross-sections, or random silhouettes) than to EBA axeheads.

**H5 (recurve subhypothesis):** The proportion of carvings with the "recurve" feature is higher than the proportion of British EBA axeheads with recurve.

## 3. Data sources

- **Carvings:** English Heritage 2012 laser-scan corpus (Abbott & Whymark-Anderson 2012). All 115 identified carvings on Stones 3, 4, 5, 53.
- **Axeheads:** Xe et al. (2021) Early Bronze Age Axe Corpus, drawn from Needham (1983) and Bevan (unpublished). n = 292 photographic silhouettes.
- **Mushrooms:** A curated corpus of *Amanita muscaria* silhouettes. Details below; **this dataset must be constructed to a documented protocol before final analysis.**
- **Other reference classes:** Curated silhouettes of British Bronze Age halberds, sickles, palstaves; cup-and-ring rock art from Northumberland/Kilmartin/Rombalds Moor; simplified Neolithic sun and moon symbols; beaker pottery cross-sections; random silhouettes from an animal-shape database (as null).

## 4. Reference-set construction protocols

### 4.1 Mushroom corpus (highest-risk decision)

To prevent reviewer accusations of biased corpus curation, the mushroom set will follow these rules:

- **Species:** *Amanita muscaria* only. Not other Amanitas, not other psychoactive mushrooms.
- **Source:** iNaturalist "research grade" observations only, filtered to photographs where the mushroom is (a) photographed from the side, (b) upright, (c) fully in-frame, (d) with a clear silhouette against a distinguishable background.
- **Growth stage sampling:** Stratified across the four canonical development stages — button, egg-emerging, expanded, reflexed — with equal representation from each. This prevents cherry-picking stages that happen to look like carvings.
- **Silhouette extraction:** Automated segmentation with `rembg` or Segment Anything, followed by manual quality inspection. Any silhouette with segmentation artifacts is discarded and replaced.
- **Target n:** 200 silhouettes total (50 per growth stage).

### 4.2 Alternative reference classes

Each alternative reference class will follow an equivalent protocol, with the *type* and *source* documented in a supplementary spreadsheet. Any exclusions are logged with a reason.

## 5. Shape features (registered)

All shapes converted to normalized 400×500 binary silhouettes at fixed area (top-hat area-preserving rescaling). Features computed via ImageJ + Python:

**Generalized:**
- Length, width, area, perimeter
- Circularity (4π·A / P²)
- Aspect ratio (H/W)
- Roundness, solidity
- Elliptical Fourier descriptors (18 harmonics, capturing 99.9% of harmonic power)

**Axe/carving-specific:**
- Blade width, butt width, edge blade height
- Min/max blade height and ratios
- Recurve ratio (Needham 1983 definition)

**Perceptual embedding:**
- DINOv2 ViT-L/14 image embedding (registered *ex ante* as the perceptual similarity space, to prevent post-hoc model selection).

## 6. Analyses (registered)

### 6.1 Recurve chi-squared test (primary H5 test)
Two-sample proportion test with Fisher's exact + Wilson 95% CI + Cohen's h effect size, comparing recurve rate in carvings vs. axes. **Threshold:** two-sided Fisher p < 0.005 AND |h| ≥ 0.3 to reject H2 with respect to recurve.

### 6.2 Multi-class classifier (primary H1 vs. H3/H4 test)
Random forest and gradient-boosted classifier trained on labeled reference classes with 5-fold CV. Report:
- Cross-validated accuracy on the reference sets alone (validates the classifier)
- Confusion matrix
- Predicted class + confidence for each carving
- Top-3 nearest-reference-exemplars per carving

**Threshold to reject the axe interpretation:** ≥ 60% of carvings are classified as a non-axe class with mean confidence > 0.5.

### 6.3 Bayesian model comparison (secondary)
For each carving, compute the log-likelihood under generative shape models fit to each reference class (Gaussian in first 22 shape-feature PCA dimensions). Report per-carving Bayes factors and corpus-level log-Bayes-factor sum. **Threshold:** log-BF sum > 10 in favor of the non-axe class to declare it the better explanation.

### 6.4 Human-perception study (see `human-study/protocol.md`)
Registered to run in parallel. Preregistered analysis: mixed-effects logistic regression on category selection, with rater as random effect, class as fixed effect.

## 7. Stopping rules

Data collection is complete (carving set is fixed by the Abbott scan). No sequential analysis is planned. All reference-set expansion is completed before the primary classifier is trained.

## 8. Deviations

Any deviation from this protocol will be reported in a Deviations section of the final paper with a justification.

## 9. Authors' commitments

- Analysis code and reference-set silhouettes will be released on GitHub at time of preprint.
- The paper will report the multi-class classifier result even if it favors the axe interpretation (i.e., no dependence on H3 being confirmed).
