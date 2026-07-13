# Human perception study: what do the Stonehenge carvings look like?

**Purpose.** The paper's shape-statistics argument depends on which reference class the algorithm was given. A skeptic can always say "your classifier is biased" or "your mushroom corpus was cherry-picked." Human judgment is much harder to argue against — if naive human raters shown the shapes in isolation say "mushroom" more often than "axe," the argument becomes robust in a way pure algorithm output cannot.

## Design

**2 (rater expertise: naive / archaeologist) × 3 (task) between-subjects.**

Both rater populations do the same three tasks in randomized order.

### Task 1 — Free description (open-ended)
Present each shape (silhouette, black on white, canonical orientation) with the prompt:
> "In one word, what does this shape look like most?"

Coded post-hoc into categories: axe/hatchet, mushroom, tree, sun/moon, tool (other), body part, animal, geometric, other/nothing.

### Task 2 — Forced choice
Present each shape with 10 candidate labels in randomized order:
- Bronze axe (blade up)
- Mushroom
- Halberd
- Sickle
- Sun/moon symbol
- Bell-beaker pot (cross-section)
- Human vulva (cup-and-ring motif)
- Boat
- Tree
- I don't know / none of these

### Task 3 — Similarity rating
Present the shape alongside 4 exemplars (axe, mushroom, sun, geometric null) in randomized position. Rate similarity of each pair on 1–7 Likert scale.

## Stimulus set

- **60 Stonehenge carvings** — random subset of the 115, stratified across Stones 3, 4, 5, 53.
- **20 real EBA axeheads** — random subset of the Bevan corpus, silhouetted identically.
- **20 real *Amanita muscaria*** — mixed growth stages.
- **20 distractor silhouettes** — halberds, sickles, sun symbols, random shapes (validity check: raters should call these what they are).

All stimuli normalized to identical size/rotation and presented in randomized order. Rater sees no site context, no framing about Stonehenge or archaeology.

## Sample size

- **Naive raters:** n = 200 via Prolific. UK+US, English fluent, no archaeology background (screened via prescreen questionnaire). Est. cost: ~$500 at $6/hr for 5 min task.
- **Expert raters:** n = 25 via targeted recruitment (Bronze-Age archaeologists, rock-art specialists, museum curators). Est. cost: honorarium $50 each = $1,250, plus recruitment time.

Power analysis: n = 200 gives >0.99 power to detect a 15-percentage-point difference in category selection at α = 0.005.

## Primary analysis (preregistered)

Mixed-effects logistic regression on category selection:
- DV: Was the shape called "axe" (vs. anything else)? Was it called "mushroom" (vs. anything else)?
- Fixed effect: stimulus class (carving / axe / mushroom / distractor).
- Random effect: rater.

**Success criterion for the mushroom hypothesis:** Carvings are called "mushroom" at a rate significantly higher than the base rate (from distractors) AND at a rate not statistically different from the mushroom-stimulus rate — while being called "axe" at a rate significantly lower than the axe-stimulus rate.

**Success criterion for the axe hypothesis:** Reverse.

**No result:** Carvings are called something else (sun, sickle, vulva, "I don't know") more often than either axe or mushroom.

## Validity checks

- Real axe silhouettes must be called "axe" by ≥ 70% of naive raters, or the task is invalid.
- Real *A. muscaria* silhouettes must be called "mushroom" by ≥ 70% of naive raters.
- Random shapes must be called "I don't know / none" at above chance rate.
- Inter-rater agreement (Fleiss' κ) reported for both rater populations.

## Ethics

- IRB submission required (TU Delft HREC — should be exempt/minimal-risk).
- No deception, no identifiable data, no sensitive personal info collected.
- Prolific standard consent + debrief.

## Timeline

- Week 1: Stimulus preparation, Qualtrics/Prolific pilot with n=10.
- Week 2: Launch Prolific study, collect data.
- Week 3: Expert rater recruitment + data collection.
- Week 4: Analysis + write-up.

## What this study defends against

- "You cherry-picked your mushroom corpus" → naive humans use their own mushroom prototypes, not ours.
- "Your classifier is biased" → humans are not our classifier.
- "You're comparing 2D projections of 3D objects" → humans don't care; they see 2D silhouettes and match them to mental categories.
- "You're an outsider making an outsider claim" → converging evidence from naive + expert humans is the highest-status form of evidence in perception research.
