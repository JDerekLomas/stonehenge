# Handoff — Stonehenge paper fixes (2026-07-16)

## Done (committed f2360e1, pushed, live at https://stonehenge-carvings.vercel.app)
Tier-1 mechanical fixes to `paper-site/src/app/page.tsx` + `README.md`:
- Reconciled all headline stats to `data/processed/*.json` (body prose was stale vs figures):
  - §3.1 recurve: axes 7% / p=1.3e-7 (was 24% / 3e-2)
  - §3.2 AR: d=-1.53, 68% (28/41), n=124 (was -1.35, 66%, 356)
  - §3.3 Mahalanobis: 90% axes / 15% carvings / p=1.5e-19 / 4D / n=124 (was 96/20/5.9e-22/3D/356)
- Figures renumbered sequentially 1-26 (were duplicated); in-text (Fig. 3)->(Fig. 2)
- Duplicate §1.1 -> §1.2; dropped hard "twelve tests" count
- Author name Whymark-Anderson -> Anderson-Whymark
- Added §7 References; added 115/119/222/124/356 count-reconciliation note
- tsc clean.

## Open — Tier-2 reframing (authorial call, NOT done)
Offered to Derek; he said gnite before deciding. Pick up here:
1. **Title/entheogen framing outruns the 7-way result** (§4.6.1: axe 2%, but tree 24% vs mushroom 57%).
   Recommend splitting top-line claim: (a) strong = not-axes; (b) softer = of organic cap-stem forms, mushroom fits best.
2. **Rock-carving-compression confound** (§3.9.5 reading 1) is the real threat — elevate it to a named alternative
   hypothesis up front, with the §3.10 null as the rebuttal.
3. **Tone**: results say "decisively/definitive"; §4.6 admits exploratory/~2D/curated. Match results prose to §4.6's register.

Ground-truth stats live in data/processed/{recurve_results,aspect_ratio_summary,shape_space_summary}.json.
