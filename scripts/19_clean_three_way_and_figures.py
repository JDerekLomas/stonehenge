"""
Clean 3-way analysis using proper pre-segmented silhouettes from the
paper's own corpus. Produces:

  - classifier report on the clean data
  - two new atlas figures showing real reference silhouettes:
      atlas_clean_axes.png     — all 41 axe reference silhouettes
      atlas_clean_mushrooms.png — all 22 mushroom reference silhouettes
      atlas_clean_carvings.png  — all 42 carving silhouettes
  - a "canonical trio" figure with a representative axe, mushroom, and
    a range of carvings side by side
  - real_extremes_clean.png: top-6 most-axe and top-6 most-mushroom
    carvings under the clean-corpus classifier
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread
from pathlib import Path
from PIL import Image, ImageOps
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import mahalanobis
from scipy import stats

ROOT = Path(__file__).parent.parent
BASE = ROOT / "data" / "downloads_extracted"
CLEAN = ROOT / "data" / "clean_corpus"
FIGS = ROOT / "figures"
THUMBS = ROOT / "data" / "clean_thumbs"
THUMBS.mkdir(exist_ok=True)

FEATURES = ["Circularity", "Aspect Ratio", "Roundness"]
# Note: solidity now trustworthy (real silhouettes), but keep to 3 for
# consistency with earlier analysis. Report full 4-feature separately.

CORPORA = {
    "axe": BASE / "Axes (Needham 1983, 2012_ burgess)",
    "mushroom": BASE / "Entire Image Corpus" / "mushrooms",
    "carving": BASE / "Entire Image Corpus" / "AllCarvings",
}


def make_thumb(src_path, out_path, size=240):
    """Normalize a silhouette to a square white canvas."""
    img = Image.open(src_path).convert("L")
    arr = np.asarray(img)
    dark = (arr < 128).astype(np.uint8)
    light = (arr >= 128).astype(np.uint8)
    def edge_px(m): return int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    shape = dark if edge_px(dark) < edge_px(light) else light
    if shape.sum() == 0:
        return False
    # bbox
    ys, xs = np.where(shape)
    minr, maxr = ys.min(), ys.max()+1
    minc, maxc = xs.min(), xs.max()+1
    pad = int(0.10 * max(maxr-minr, maxc-minc))
    minr = max(0, minr-pad); maxr = min(shape.shape[0], maxr+pad)
    minc = max(0, minc-pad); maxc = min(shape.shape[1], maxc+pad)
    crop = shape[minr:maxr, minc:maxc]
    h, w = crop.shape
    scale = (size*0.85) / max(h, w)
    new_h = max(1, int(h*scale))
    new_w = max(1, int(w*scale))
    im = Image.fromarray((crop*255).astype(np.uint8), mode="L").resize(
        (new_w, new_h), Image.LANCZOS)
    im = im.point(lambda v: 255 if v>127 else 0)
    im = ImageOps.invert(im.convert("L"))
    canvas = Image.new("L", (size, size), 255)
    canvas.paste(im, ((size-new_w)//2, (size-new_h)//2))
    canvas.save(out_path)
    return True


def build_thumbs():
    for name, directory in CORPORA.items():
        sub = THUMBS / name
        sub.mkdir(exist_ok=True)
        n = 0
        for p in sorted(directory.glob("*")):
            if p.suffix.lower() not in (".tif", ".png", ".jpg", ".jpeg"):
                continue
            if make_thumb(p, sub / (p.stem + ".png")):
                n += 1
        print(f"  {name}: {n} thumbs -> {sub}")


def atlas(name, source_df, thumb_dir, out_path, cols=None, sort_by=None):
    if sort_by:
        source_df = source_df.sort_values(sort_by, ascending=False).reset_index(drop=True)
    n = len(source_df)
    if cols is None:
        cols = min(8, n)
    rows = int(np.ceil(n / cols))
    fig, axarr = plt.subplots(rows, cols, figsize=(cols*1.4, rows*1.5))
    axarr = np.array(axarr).reshape(rows, cols)
    for i in range(rows*cols):
        r, c = i // cols, i % cols
        ax = axarr[r, c]
        if i >= n:
            ax.axis("off"); continue
        row = source_df.iloc[i]
        thumb = thumb_dir / (row["id"] + ".png")
        if thumb.exists():
            ax.imshow(imread(str(thumb)), cmap="gray")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#d6d3d1"); s.set_linewidth(0.8)
        ax.set_title(row["id"][:16], fontsize=6.5, pad=1.5)
    fig.suptitle(name, fontsize=13, y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(out_path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  wrote {out_path}")


def main():
    df = pd.read_csv(CLEAN / "clean_features.csv")

    print("Building thumbnails...")
    build_thumbs()

    print("\n=== Classifier ===\n")
    axe_df = df[df["source"] == "axe"][FEATURES]
    mus_df = df[df["source"] == "mushroom"][FEATURES]
    carv_df = df[df["source"] == "carving"][FEATURES]

    X_train = pd.concat([axe_df, mus_df]).values
    y_train = np.array(["axe"]*len(axe_df) + ["mushroom"]*len(mus_df))
    scaler = StandardScaler().fit(X_train)
    Xs = scaler.transform(X_train)

    for name, clf in [
        ("LDA", LinearDiscriminantAnalysis()),
        ("Random Forest", RandomForestClassifier(n_estimators=300, random_state=42)),
    ]:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(clf, Xs, y_train, cv=cv, scoring="accuracy")
        print(f"  {name}: CV acc = {scores.mean():.3f} ± {scores.std():.3f}")

    # Fit + predict on carvings
    Xs_carv = scaler.transform(carv_df.values)
    lda = LinearDiscriminantAnalysis().fit(Xs, y_train)
    rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xs, y_train)
    mus_idx = list(rf.classes_).index("mushroom")
    lda_p_mus = lda.predict_proba(Xs_carv)[:, list(lda.classes_).index("mushroom")]
    rf_p_mus = rf.predict_proba(Xs_carv)[:, mus_idx]
    lda_pred = lda.predict(Xs_carv)
    rf_pred = rf.predict(Xs_carv)

    print(f"\nCarvings (n={len(carv_df)}):")
    print(f"  LDA predicts mushroom: {(lda_pred=='mushroom').sum()} / {len(carv_df)}"
          f" (mean P(mus) = {lda_p_mus.mean():.3f})")
    print(f"  RF  predicts mushroom: {(rf_pred=='mushroom').sum()} / {len(carv_df)}"
          f" (mean P(mus) = {rf_p_mus.mean():.3f})")

    # Mahalanobis
    axe_mean = axe_df.values.mean(axis=0)
    axe_cov_inv = np.linalg.pinv(np.cov(axe_df.values.T))
    mus_mean = mus_df.values.mean(axis=0)
    mus_cov_inv = np.linalg.pinv(np.cov(mus_df.values.T))
    d_axe = [mahalanobis(x, axe_mean, axe_cov_inv) for x in carv_df.values]
    d_mus = [mahalanobis(x, mus_mean, mus_cov_inv) for x in carv_df.values]
    closer_mus = sum(dm < da for da, dm in zip(d_axe, d_mus))
    print(f"  Carvings closer to mushroom centroid: {closer_mus} / {len(carv_df)}"
          f" ({100*closer_mus/len(carv_df):.1f}%)")

    # Attach predictions
    carv_full = df[df["source"] == "carving"].reset_index(drop=True).copy()
    carv_full["lda_p_mus"] = lda_p_mus
    carv_full["rf_p_mus"] = rf_p_mus
    carv_full["lda_pred"] = lda_pred
    carv_full["rf_pred"] = rf_pred
    carv_full["d_axe"] = d_axe
    carv_full["d_mus"] = d_mus
    carv_full.to_csv(CLEAN / "carving_predictions.csv", index=False)
    print(f"\nSaved: {CLEAN / 'carving_predictions.csv'}")

    print("\n=== Atlas figures ===")
    atlas("All 41 axe reference silhouettes (Needham 1983 + Burgess)",
          df[df["source"]=="axe"], THUMBS/"axe", FIGS/"atlas_clean_axes.png")
    atlas("All 22 mushroom reference silhouettes",
          df[df["source"]=="mushroom"], THUMBS/"mushroom", FIGS/"atlas_clean_mushrooms.png",
          cols=6)
    atlas(f"All 42 Stonehenge carvings, sorted by RF P(mushroom)",
          carv_full, THUMBS/"carving", FIGS/"atlas_clean_carvings.png",
          sort_by="rf_p_mus")

    # =========================================================
    # Composite: canonical trio
    # =========================================================
    canonical_axe = next(p for p in (THUMBS/"axe").glob("2.png"))
    # Amanita Muscaria.tif -> Amanita Muscaria.png
    canonical_mus_files = sorted((THUMBS/"mushroom").glob("Amanita Muscaria*.png"))
    canonical_mus = canonical_mus_files[0] if canonical_mus_files else next((THUMBS/"mushroom").iterdir())

    top_mus = carv_full.sort_values("rf_p_mus", ascending=False).head(6)
    top_axe = carv_full.sort_values("rf_p_mus", ascending=True).head(6)

    fig, axarr = plt.subplots(2, 7, figsize=(15, 4.8),
                              gridspec_kw={"width_ratios":[1.15,1,1,1,1,1,1]})
    # top row: reference axe + 6 most-axe carvings
    axarr[0,0].imshow(imread(str(canonical_axe)), cmap="gray")
    axarr[0,0].set_title("REFERENCE\nBronze axe (Needham 1983)", fontsize=9, pad=3)
    for i,(_,r) in enumerate(top_axe.iterrows()):
        thumb = THUMBS/"carving"/(r["id"]+".png")
        if thumb.exists(): axarr[0,i+1].imshow(imread(str(thumb)), cmap="gray")
        axarr[0,i+1].set_title(f"{r['id']}\nP(mus)={r['rf_p_mus']:.2f}",
                               fontsize=8.5, color="#4a6fa5", pad=3)
    axarr[1,0].imshow(imread(str(canonical_mus)), cmap="gray")
    axarr[1,0].set_title("REFERENCE\nA. muscaria (silhouette)", fontsize=9, pad=3)
    for i,(_,r) in enumerate(top_mus.iterrows()):
        thumb = THUMBS/"carving"/(r["id"]+".png")
        if thumb.exists(): axarr[1,i+1].imshow(imread(str(thumb)), cmap="gray")
        axarr[1,i+1].set_title(f"{r['id']}\nP(mus)={r['rf_p_mus']:.2f}",
                               fontsize=8.5, color="#c14545", pad=3)
    for ax in axarr.ravel():
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#d6d3d1"); s.set_linewidth(1.0)
    # Frame the references specially
    for s in axarr[0,0].spines.values():
        s.set_color("#4a6fa5"); s.set_linewidth(2.5)
    for s in axarr[1,0].spines.values():
        s.set_color("#c14545"); s.set_linewidth(2.5)
    for i in range(1,7):
        for s in axarr[0,i].spines.values():
            s.set_color("#4a6fa5"); s.set_linewidth(1.8)
        for s in axarr[1,i].spines.values():
            s.set_color("#c14545"); s.set_linewidth(1.8)

    fig.text(0.005, 0.75, "6 most axe-like\ncarvings",
             rotation=90, ha="center", va="center", fontsize=9.5,
             fontweight="bold", color="#4a6fa5")
    fig.text(0.005, 0.28, "6 most mushroom-like\ncarvings",
             rotation=90, ha="center", va="center", fontsize=9.5,
             fontweight="bold", color="#c14545")
    fig.suptitle("Real reference silhouettes vs. extremes of the classifier ranking",
                 fontsize=11.5, y=1.02)
    plt.tight_layout(rect=[0.02, 0, 1, 0.98])
    plt.savefig(FIGS/"real_extremes_clean.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  wrote {FIGS/'real_extremes_clean.png'}")


if __name__ == "__main__":
    main()
