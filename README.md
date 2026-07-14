# Stonehenge Carvings — Shape Analysis

Companion analysis to the working paper *"Mushroom-Shaped Carvings on Stonehenge May Be Early Evidence for Bronze Age Entheogen Use"* (J. Derek Lomas, TU Delft, 2021 / revised 2026).

**Live paper:** https://stonehenge-carvings.vercel.app

## What this repository contains

Eight independent shape-analysis pipelines that test the 1953 identification of the Stonehenge carvings as bronze axeheads. All eight converge on the same finding: the carvings do not match British Early Bronze Age axeheads at the level of shape, and they do match native British mushrooms.

## Repository layout

```
stonehenge/
├── README.md                          ← this file
├── paper-site/                        ← Next.js site, deployed to Vercel
│   ├── src/app/page.tsx               ← the full paper
│   ├── src/components/                ← FindspotMap, MuscariaGrid
│   └── public/                        ← figures, data downloads
├── scripts/                           ← 28 Python analysis scripts, ordered
│   ├── 01_recurve_analysis.py         ← §3.1
│   ├── 05_aspect_ratio_focused.py     ← §3.2
│   ├── 03_shape_space_analysis.py     ← §3.3
│   ├── 23_definitive_analysis.py      ← §3.4 (full 515-shape corpus)
│   ├── 20_shapecomp_analysis.py       ← §3.5 (perceptual embedding)
│   ├── 25_stone4_and_fourier.py       ← §3.6 (Fourier harmonics + Stone 4)
│   ├── 26_size_comparison.py          ← §3.9 (physical size)
│   ├── 27b_width_length_comparable.py ← §3.9 (bbox aspect)
│   ├── 10_findspot_map.py             ← §3.10 (geographic)
│   └── ...                            ← 20 more, all reproducible
├── data/
│   ├── raw/                           ← input XLSX/CSV from the paper's corpus
│   ├── processed/                     ← JSON summaries + CSV outputs
│   ├── clean_corpus/                  ← curated clean feature CSVs
│   ├── carving_thumbs/                ← normalized carving silhouettes
│   ├── clean_thumbs/{axe,carving,mushroom}/ ← normalized reference silhouettes
│   └── crawford_images/               ← historical Crawford 1954 plates
├── figures/                           ← all figures (PNG + PDF)
├── prereg/preregistration.md          ← OSF-ready draft
└── human-study/protocol.md            ← Prolific + expert-panel study design
```

## Key findings

| § | Analysis | Verdict |
|---|---|---|
| 3.1 | Recurve rate | Carvings 37%, axes 24%, p = 3×10⁻² |
| 3.2 | Aspect ratio (ellipse) | Carvings 1.56, axes 2.67, d = −1.53 |
| 3.3 | Multivariate Mahalanobis vs axes | 85% carvings outside 95% axe cluster |
| 3.4 | 3-way LDA/RF classifier (n=515) | 74–77% carvings predicted mushroom, 96% CV accuracy |
| 3.4 | 3-way Mahalanobis (n=515) | **113/119 (95%) closer to mushroom centroid** |
| 3.5 | ShapeComp perceptual embedding | 93% CV axe-vs-carving accuracy, carvings 4× farther from nearest axe |
| 3.6 | Fourier harmonic complexity | Carvings need more harmonics than axes (p = 4×10⁻⁶) |
| 3.9 | Bounding-box aspect | **Carvings 0.87 = mushrooms 0.86** (p = 0.95); axes 0.60 (p = 10⁻¹⁰) |
| 3.10 | Findspot geography | Only 23% of contemporary axes near Stonehenge |

## Reference datasets

- **Bevan corpus** (A. Bevan, UCL): 292 curated axes, 7308-axe metadata sheet, 515-shape "All data" with matched ImageJ features for axes, carvings, and mushrooms.
- **English Heritage 2012 laser scan** (Abbott & Whymark-Anderson): 118 Stonehenge carvings at 0.5 mm resolution; 41 Stone 53 + 31 Stone 4 TIFFs available locally.
- **Needham (1983)** typology: 41 canonical axe silhouettes across Classes 2–5.
- **British mushroom silhouettes**: 22 curated in the shape analysis; 15 candidate species catalogued with cap/stem sizes and psilocybin activity.
- **iNaturalist**: research-grade *A. muscaria* photos (auto-segmented).
- **Rockart England** (ADS / Beckensall): 22,000 rock-art motifs, 118 types — reserved for a planned null comparison.

## How to reproduce

```bash
python3 -m venv .venv
.venv/bin/pip install numpy pandas scipy scikit-image scikit-learn matplotlib pillow openpyxl pypdf python-docx requests
for i in $(seq -w 01 27); do
    .venv/bin/python scripts/${i}*.py
done
```

Every figure and every summary JSON in `data/processed/` is regenerated end-to-end.

## Deploying the paper site

```bash
cd paper-site && npm install && npm run build && vercel --prod
```

## Preregistration and human-perception study

Draft OSF preregistration (`prereg/preregistration.md`) and Prolific/expert-panel human-perception study protocol (`human-study/protocol.md`) are ready to post. The human study is the strongest planned replication — it uses independent evidence (perceptual judgment) that cannot be dismissed as algorithmic bias.

## Dependencies

Python ≥ 3.11 with `numpy pandas scipy scikit-image scikit-learn matplotlib pillow openpyxl pypdf python-docx requests`. Next.js 16 with Tailwind 4 for the site.
