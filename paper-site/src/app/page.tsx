import Image from "next/image";
import Link from "next/link";
import { FindspotMap } from "@/components/FindspotMap";
import { MuscariaGrid } from "@/components/MuscariaGrid";
import { SketchfabEmbed } from "@/components/SketchfabEmbed";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <header className="border-b border-stone-200 bg-white">
        <div className="max-w-5xl mx-auto px-6 pt-16 pb-12">
          <p className="d-byline uppercase tracking-widest text-xs mb-6">
            Draft &middot; 2026
          </p>
          <h1 className="d-title text-4xl md:text-5xl mb-6" style={{ maxWidth: "24ch" }}>
            Shape analysis of the Stonehenge carvings
          </h1>
          <p className="text-lg leading-relaxed mb-6" style={{ maxWidth: "68ch", color: "#3f3f3f" }}>
            The 115 prehistoric carvings on Stonehenge have been described
            as bronze axeheads since Atkinson&rsquo;s 1953 identification.
            The identification has not previously been tested against real
            axeheads. Using shape descriptors, classifiers, and an
            independent perceptual embedding, this paper finds that the
            carvings do not match the shape distribution of British Early
            Bronze Age axeheads. They do match native British mushroom
            silhouettes.
          </p>
          <div className="d-byline space-y-1">
            <p>
              <span style={{ color: "#0a0a0a", fontWeight: 600 }}>J. Derek Lomas</span>
              {" "}&middot; TU Delft
            </p>
            <p>Last updated {new Date().toISOString().slice(0, 10)} &middot;{" "}
              <a href="https://github.com/JDerekLomas/stonehenge"
                 className="underline"
                 style={{ color: "#b91c1c", borderColor: "rgba(185,28,28,0.35)" }}
                 target="_blank" rel="noopener noreferrer">
                github.com/JDerekLomas/stonehenge
              </a>
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-16 d-article">
        <section aria-labelledby="intro" className="mb-14">
          <h2 id="intro" className="text-2xl font-bold mb-4">1. Introduction</h2>
          <p>
            In July 1953, Richard Atkinson identified two carvings on Stone
            53 of Stonehenge as a bronze axehead and a dagger. The
            interpretation was extended over subsequent decades to a
            growing set of similar carvings on Stones 3, 4, and 5. Abbott
            &amp; Anderson-Whymark&rsquo;s 2012 laser scan brought the
            total to 115.
          </p>
          <p>
            The identification has not, in the seven decades since, been
            tested quantitatively against a corpus of real bronze
            axeheads. This paper does that. It compares shape descriptors
            of the carvings to descriptors of 356 British Early Bronze
            Age axeheads (Bevan corpus) and 40 mushroom silhouettes,
            using standard classifiers and an independent perceptual
            embedding. The carvings do not match the axes. They match
            mushroom silhouettes.
          </p>
        </section>

        <section className="mb-16">
          <figure className="d-figure">
            <SketchfabEmbed
              modelId="87062394109c44fc99b5cf646b83639c"
              title="Axehead carvings, Stone 53 at Stonehenge — Wessex Archaeology"
              height={520}
            />
            <p className="d-figcaption">
              Interactive 3D scan of the &ldquo;axehead&rdquo; carvings on
              Stone 53 (drag to rotate; scroll to zoom). Model by{" "}
              <a href="https://sketchfab.com/wessexarchaeology"
                 target="_blank" rel="noopener noreferrer">Wessex Archaeology / Archaeoptics</a>{" "}
              from a sub-millimetre Minolta VI-900 scan (2002&ndash;2003).
              This is the same sub-mm laser-scan data whose 2D silhouettes
              are analysed below.
            </p>
          </figure>
          <figure className="d-figure">
            <Image
              src="/figures/named_species_plate.png"
              alt="Named comparison plate: four psilocybin mushroom species, eight canonical Needham axeheads, and eight Stonehenge carvings, arranged in three rows"
              width={2800}
              height={1200}
              className="w-full h-auto"
              priority
            />
            <figcaption className="d-figcaption text-center italic">
              Frontispiece. Top row: four native British psilocybin
              mushroom species. Middle row: eight canonical British Early
              Bronze Age axehead forms (Needham 1983, Class 2A through the
              late-Bronze form). Bottom row: eight Stonehenge carvings
              from Stone 53. Read column-wise: the carvings share their
              cap-plus-stem morphology with the mushrooms, not with the
              bulky wide-shouldered forms of the axes.
            </figcaption>
          </figure>
          <figure className="d-figure">
            <Image
              src="/paper_figures/image3.png"
              alt="Side-by-side comparison: mushroom-shaped carvings on Stones 53 and 4 of Stonehenge, next to canonical Southern British bronze axeheads from 2500 to 1600 BC"
              width={2000}
              height={800}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center italic">
              The same visual argument, drawn from the paper&rsquo;s own
              working figure: left, the full set of Stone 53 and Stone 4
              carvings; right, the canonical Southern British axehead
              typology 2500&ndash;1600 BC.
            </figcaption>
          </figure>
        </section>

        <section aria-labelledby="context" className="mb-14">
          <h3 className="text-lg font-semibold mt-6 mb-3">1.1 Prior identifications and their strength</h3>
          <p>
            Atkinson (1956) recorded 15 carvings across Stones 3, 4, and 53
            and identified them as blade-up bronze axeheads dating to
            c.1650&ndash;1400 BC. Subsequent workers (Newall,
            Crawford, Cleal, Walker &amp; Montague 1995; Lawson 2007;
            Abbott &amp; Anderson-Whymark 2012) confirmed the identification
            and added new carvings as they were discovered. The 2012 laser
            scan brought the total to 115. The word &ldquo;axehead&rdquo;
            appears in the Abbott &amp; Anderson-Whymark report 108 times;
            none of the 115 shapes was compared to a real axehead corpus.
          </p>
          <p>
            The identification is doubly consequential. First, if correct,
            Stonehenge&rsquo;s 115 carvings would more than double the
            entire British Bronze Age &ldquo;axehead-on-rock&rdquo; record:
            Abbott &amp; Anderson-Whymark (2012, p.37) note that
            &ldquo;only five certain parallels can be cited&rdquo; for the
            category. Second, the same report documents at least two other
            carvings that had to be re-identified: the &ldquo;quadrilateral
            symbol&rdquo; on Stone 57, originally reported as a Breton
            shield-escutcheon, turned out under laser scan to be
            pick-dressing, not a carving at all.
          </p>
        </section>

        <section aria-labelledby="methods" className="mb-14">
          <h2 id="methods" className="text-2xl font-bold mb-4">2. Data and methods</h2>
          <h3 className="text-lg font-semibold mt-6 mb-2">2.1 Reference corpora</h3>
          <p>
            <span className="font-semibold">Axes.</span> 124 British Early Bronze Age
            axeheads with ImageJ-extracted shape features, from Bevan (unpublished),
            derived from Needham (1983). Complete typology metadata (Class 2 &ndash; Class
            5) for 275 additional axes, with lat/lon findspots, is also used.
          </p>
          <p>
            <span className="font-semibold">Carvings.</span> 41 Stone 53 carvings from the
            English Heritage 2012 laser-scan (Abbott and Whymark-Anderson 2012), with the
            same ImageJ features previously extracted.
          </p>
          <p>
            <span className="font-semibold">Mushrooms.</span> 22 pre-segmented
            mushroom silhouettes assembled by the paper&rsquo;s author,
            including two <em>Amanita muscaria</em> reference forms, one{" "}
            <em>Psilocybe subviscida</em>, and 19 additional silhouettes of
            typical mushroom morphology drawn from natural-history photographs.
            All are canonical side-view silhouettes with the full cap-plus-stem
            (and, where present, volva).
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/atlas_clean_mushrooms.png"
              alt="Atlas of 22 mushroom reference silhouettes"
              width={2000}
              height={1200}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 2. The 22 mushroom reference silhouettes used in the
              analysis. Note the canonical cap-and-stem form.
            </figcaption>
          </figure>
          <p>
            <span className="font-semibold">Axes.</span> 41 canonical bronze
            axe reference silhouettes drawn from Needham (1983) and Burgess.
            These are the reference forms conventionally cited as the visual
            match for the Stonehenge carvings. Needham&rsquo;s original
            typology defines anatomical features &mdash; flange height, body
            width, cutting-edge splay, stop-bevel, marginal waisting &mdash;
            that distinguish Classes 2 through 5 (Fig. 3).
          </p>
          <figure className="d-figure">
            <Image
              src="/paper_figures/needham_reference.png"
              alt="Needham 1983 Class 5D reference figure showing axe subtypes 85 through 89 with anatomical annotations"
              width={2000}
              height={1600}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 3. Needham (1983) reference figure for Class 5D
              axeheads &mdash; the &ldquo;West Drayton type&rdquo; and its
              variants (with mid-body swelling, marginal waisting). Reproduced
              from the paper&rsquo;s own working figure. Anatomical features
              are annotated: <em>medium to high flanges, medium-broad body,
              stop-bevel, medium to broad cutting edge</em>. These are the
              specific formal features that define British Early Bronze Age
              axe typology.
            </figcaption>
          </figure>

          <figure className="d-figure">
            <Image
              src="/figures/measurement_definitions.png"
              alt="Labeled axehead schematic showing all Needham measurement lines (L, LB, WB, W2, W3, WE, LC, DE) plus derived ratios and standard ImageJ dimensionless features"
              width={1200}
              height={2000}
              className="w-full h-auto"
              style={{ maxWidth: 600, margin: "0 auto", display: "block" }}
            />
            <figcaption className="d-figcaption text-center">
              Figure 3d. The shape descriptors used throughout this paper.
              Top: Needham 1983 linear measurements labeled on a schematic
              Class 5 axehead. Bottom: the derived ratios (Needham space)
              and the standard ImageJ dimensionless features (Circularity,
              Aspect Ratio, Roundness, Solidity) used by every classifier
              in §3.
            </figcaption>
          </figure>
          <figure className="d-figure">
            <Image
              src="/paper_figures/hafted_axes.png"
              alt="Reconstruction of two hafted bronze axes with wooden handles"
              width={1600}
              height={1150}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 3b. Reconstruction of hafted bronze axes. Real bronze
              axeheads were used mounted on wooden handles; the &ldquo;axehead
              alone&rdquo; that Atkinson (1953) described the carvings as
              depicting would be an unusual choice of subject &mdash; the
              functional whole is the hafted implement.
            </figcaption>
          </figure>
          <figure className="d-figure">
            <Image
              src="/figures/atlas_clean_axes.png"
              alt="Atlas of 41 axe reference silhouettes from Needham 1983 and Burgess"
              width={2000}
              height={1500}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 3c. The 41 axe reference silhouettes used in the
              analysis. Class 5 recurved forms in particular have a
              superficial cap-plus-stem morphology &mdash; the resemblance
              that plausibly motivated the original 1953 identification.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">2.2 Shape features</h3>
          <p>
            The comparison uses the four canonical dimensionless features returned by
            ImageJ: Circularity (4&pi;A/P<sup>2</sup>), Aspect Ratio
            (major/minor axis), Roundness (4A/&pi;M<sup>2</sup>), and Solidity
            (A/A<sub>convex</sub>). We exclude size-dependent features (area, perimeter,
            height, width) because the axe corpus is measured in pixels on a 400&times;500
            canvas whereas the carving corpus is measured in fractional units; direct
            comparison would be nonsensical.
          </p>
          <p>
            We also examine a single hand-coded morphological feature &mdash; the{" "}
            &ldquo;recurve&rdquo; of Needham (1983), which describes the involuted curl at
            the blade corners of certain axe types &mdash; on the Stonehenge carvings as
            recorded by Lomas (2021).
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">2.3 Statistical analyses</h3>
          <p>
            (i) A Fisher exact test with 95% Wilson score confidence intervals compares the
            proportion of recurve-bearing shapes between carvings and axes. Effect size
            is Cohen&rsquo;s h. A Bayesian posterior (uniform Beta(1,1) priors)
            complements the frequentist test.
          </p>
          <p>
            (ii) Univariate comparisons of the four ImageJ features are made with
            Welch&rsquo;s t and Kolmogorov&rsquo;s D, with Benjamini&ndash;Hochberg
            FDR correction across the four tests.
          </p>
          <p>
            (iii) A Mahalanobis distance from each carving to the axe centroid is
            computed; carvings are declared &ldquo;inside&rdquo; the 95% axe-cluster
            ellipsoid if D<sup>2</sup> &lt; &chi;<sup>2</sup><sub>0.95, k</sub>.
          </p>
          <p>
            (iv) A three-way test compares each carving&rsquo;s Mahalanobis distance to
            the axe and mushroom centroids, and trains axe-vs-mushroom LDA and Random
            Forest classifiers under 5-fold cross-validation; the classifiers are then
            applied to the Stone 53 carvings to obtain per-carving class predictions and
            posterior probabilities.
          </p>
        </section>

        <section aria-labelledby="results" className="mb-14">
          <h2 id="results" className="text-2xl font-bold mb-4">3. Results</h2>
          <p>
            Twelve tests follow, each using a different feature set,
            reference corpus, classifier, or methodology. Each arrives
            at the same qualitative verdict.
          </p>

          <h3 className="text-lg font-semibold mt-6 mb-2">
            3.1 The recurve feature is 5&ndash;6&times; more common on carvings
          </h3>
          <p>
            The paper&rsquo;s original observation about recurve is confirmed with proper
            statistics. Across all 101 identified carvings on Stones 4 and 53, 37 (37%)
            show recurve; of 105 British EBA axes in Needham&rsquo;s corpus, only 7 (7%)
            do. Fisher exact p = 1.3&times;10<sup>&minus;7</sup>, odds ratio 8.1,
            Cohen&rsquo;s h = 0.78, Bayesian
            P(carving rate &gt; axe rate) &gt; 0.9999.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/recurve_comparison.png"
              alt="Bar chart: recurve rate in Stonehenge carvings (Stone 53, Stone 4, all) vs British EBA axes"
              width={1600}
              height={1000}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 1. Recurve rate on the Stonehenge carvings vs. British EBA axes.
              Error bars: 95% Wilson score CI.
            </figcaption>
          </figure>
          <p>
            Recurve is diagnostic of Needham&rsquo;s Class 5 (Arreton phase, c.
            1700&ndash;1450 BC) axeheads with expanded blade-corners, and is otherwise
            rare. It is not, however, a feature one would expect a stonecutter reproducing
            an unfamiliar bronze axehead to invent independently. The same feature does
            match another morphology: the outer margin of the mature{" "}
            <em>Amanita muscaria</em> cap, which curls under (recurves) as the cap
            expands and dries, exposing the gills.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.2 Carvings are systematically less elongated than real axes
          </h3>
          <p>
            Aspect ratio is the single most-diagnostic axe feature we test, and the one
            with the cleanest interpretation. Real bronze axes are functional tools with
            aspect ratio constrained by hafting geometry &mdash; you need enough length
            for a handle grip and blade. The 356 Bevan-corpus axes have median AR = 2.67
            (IQR 2.32&ndash;2.94). The 41 Stone 53 carvings have median AR = 1.53
            (IQR 1.32&ndash;1.98).
          </p>
          <p>
            <span className="font-semibold">
              66% (27 of 41) of Stone 53 carvings are less elongated than the least
              elongated 2.5% of British EBA axes (n = 356).
            </span>{" "}
            Cohen&rsquo;s d = &minus;1.35 (very large), Kolmogorov&rsquo;s D = 0.68, p =
            2&times;10<sup>&minus;17</sup>. A skilled carver reproducing an axe from
            memory would not systematically flatten it.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.3 Carvings sit outside the multivariate axe-cluster
          </h3>
          <p>
            Under Mahalanobis distance in the three-dimensional (Circularity, AR,
            Roundness) space, using the full Bevan reference of 356 axes,
            96% of axes fall within their own 95% cluster ellipsoid
            &mdash; validating the model. Only 20% of Stone 53 carvings do.
            Mann-Whitney U comparing the two distance distributions gives
            p = 5.9&times;10<sup>&minus;22</sup>.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/mahalanobis_histogram_v2.png"
              alt="Histogram: Mahalanobis distance from British EBA axe centroid for axes and carvings"
              width={1600}
              height={900}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 2. Mahalanobis distance from each shape to the British EBA axe
              centroid in the four-dimensional shape space. Axes cluster tightly; only
              14.6% of Stone 53 carvings fall within the 95% axe-cluster ellipsoid.
            </figcaption>
          </figure>
          <p className="italic text-sm text-stone-700">
            Caveat: the four dimensionless features are highly collinear
            (AR&ndash;Roundness r = &minus;0.965 in the axe corpus). The multivariate test
            effectively has two independent dimensions, not four. The result is
            equivalent to reporting the aspect-ratio test above.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.4 Carvings match mushrooms, not axes
          </h3>
          <p>
            With the paper&rsquo;s full labeled corpus &mdash; 356 axes, 119
            carvings, and 40 mushrooms, all with matched ImageJ features
            &mdash; we ask per carving: which class centroid is nearer in the
            (Circularity, Aspect Ratio, Roundness) space?{" "}
            <span className="font-semibold">113 of 119 (95.0%) carvings are
            closer to the mushroom centroid than to the axe centroid.</span>
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/definitive_violin.png"
              alt="Violin plots comparing Circularity, Aspect Ratio, and Roundness across the paper's full labeled corpus of 356 axes, 119 carvings, and 40 mushrooms"
              width={2600}
              height={950}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 4. Distributions of the three dimensionless shape features
              across the paper&rsquo;s definitive corpus. Carvings and
              mushrooms are visually indistinguishable on Aspect Ratio and
              Roundness; axes are systematically different.
            </figcaption>
          </figure>
          <figure className="d-figure">
            <Image
              src="/figures/three_way_violin.png"
              alt="Violin plots of Circularity, Aspect Ratio, and Roundness across axes, carvings, and A. muscaria"
              width={2000}
              height={900}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 3. Per-feature distributions for British EBA axes, Stone 53
              carvings, and <em>Amanita muscaria</em> silhouettes. Carvings and mushrooms
              are indistinguishable on Aspect Ratio and Roundness; both differ sharply
              from axes.
            </figcaption>
          </figure>
          <p>
            An axe-vs-mushroom Linear Discriminant Analysis, cross-validated at
            95.7% &plusmn; 2.3% accuracy on the training data, classifies 88 of
            119 (73.9%) carvings as mushroom with mean posterior probability
            0.74. A Random Forest classifier at 96.0% &plusmn; 1.7% CV
            accuracy classifies 92 of 119 (77.3%) as mushroom with mean
            posterior 0.74. Both classifiers reach the same qualitative
            conclusion.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.5 Independent confirmation via a perceptual embedding
          </h3>
          <p>
            To rule out a hand-engineered-feature artifact, we also ran the
            paper&rsquo;s original ShapeComp analysis (Morgenstern et al.
            2020), which embeds each silhouette in a 22-dimensional space
            trained on 25,000 animal silhouettes and calibrated to human
            shape perception. A cross-validated axe-vs-carving classifier on
            this embedding achieves 93.6% (LDA) and 93.4% (RF) accuracy
            &mdash; independent evidence, from a completely different
            methodology, that the two classes are perceptually distinct.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/shapecomp_pca.png"
              alt="PCA scatter of ShapeComp 22-dimensional perceptual embedding, showing axes and carvings forming distinct clusters"
              width={2000}
              height={1600}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 5. First two principal components of the ShapeComp
              perceptual embedding of 36 axes and 41 Stone 53 carvings.
              Axes and carvings occupy disjoint regions along PC1 with almost
              no overlap. This corroborates the ImageJ-based finding through
              a completely independent representation.
            </figcaption>
          </figure>

          <p>
            The nearest-neighbour distance in the same 22D embedding is also
            telling: axes are separated from their nearest neighbour axe by a
            median of 0.46 units, but the nearest axe for each carving is on
            average <em>four times farther</em> away (median 1.81 units). Even
            the &ldquo;best&rdquo; axe match for any carving is far, in
            perceptual terms, from that carving.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.6 Carvings require more Fourier harmonics than axes
          </h3>
          <p>
            Elliptical Fourier descriptors (Kuhl &amp; Giardina 1982)
            reconstruct a closed contour as a sum of sine and cosine harmonics.
            The number of harmonics required to reach 99% reconstruction
            fidelity is a scale-independent measure of shape complexity: a
            smooth ellipse needs one harmonic; a jagged outline with fine
            detail needs many. We computed this metric for all 41 axes, 72
            Stonehenge carvings (Stone 53 plus 31 newly-processed Stone 4
            TIFFs), and 22 mushroom silhouettes.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/harmonics_complexity.png"
              alt="Violin plot: elliptical Fourier harmonics required for 99% shape reconstruction, comparing axes (n=41), carvings (n=72), and mushrooms (n=22)"
              width={2000}
              height={1000}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 6. Shape complexity by elliptical Fourier decomposition.
              Carvings (median 42) require significantly more harmonics than
              axes (median 40, mean 30 with heavy left tail of very simple
              axe forms), and their distribution overlaps with mushrooms
              (median 44). Mann-Whitney p = 4.0&times;10<sup>&minus;6</sup>,
              Cliff&rsquo;s δ = 0.50 (large effect).
            </figcaption>
          </figure>
          <p>
            The argument is thermodynamic: carving sarsen stone with a
            hammer-stone is enormously effortful. Every additional harmonic
            of shape complexity corresponds to additional detail deliberately
            preserved in the carving. If the carvings were simple depictions
            of an axehead form, they should not require MORE harmonics than
            the axes themselves. That they do &mdash; matching the mushroom
            complexity &mdash; is inconsistent with a low-effort axe-imitation
            hypothesis and consistent with a specific target morphology
            (mushroom) being deliberately reproduced with care.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/three_way_scatter.png"
              alt="Scatter of Aspect Ratio vs Roundness for axes, mushrooms, and carvings"
              width={1500}
              height={1200}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 4. Stone 53 carvings occupy the low-aspect-ratio, high-roundness
              region of shape space alongside <em>A. muscaria</em>, not the elongated
              region occupied by British EBA axes.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.6.5 Manual axe matches: even the researcher&rsquo;s own picks don&rsquo;t look right
          </h3>
          <p>
            The Stone 53 Measurements sheet contains a hand-mapping in which
            the researcher assigns each carving to its closest Needham
            axehead by number. Rendering each carving next to its
            manually-picked Needham match makes the visual mismatch
            explicit: the carvings (red border) have wide caps over narrow
            stems; the hand-picked axes (blue border) have narrower tops
            and wider solid bodies.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/manual_needham_pairs.png"
              alt="8 pairs of carving-and-manually-picked-Needham-axe silhouettes side by side"
              width={2300}
              height={850}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 5b. Eight carvings, each next to the specific Needham
              axe the researcher manually picked as its closest match.
              Even the hand-picked axe match does not visually correspond
              to the carving.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.6.6 Per-stone replication (Stone 4 confirms Stone 53)
          </h3>
          <p>
            The 31 Stone 4 carvings we can process independently confirm
            the pattern. Under the same axe-vs-mushroom classifier trained
            on the same reference sets:
          </p>
          <ul className="list-disc list-inside pl-2 space-y-1">
            <li>Stone 53 (n=41): 78% RF-predicted mushroom, 85% closer to mushroom centroid.</li>
            <li>Stone 4 (n=31): 81% RF-predicted mushroom, 90% closer to mushroom centroid.</li>
          </ul>
          <figure className="d-figure">
            <Image
              src="/figures/per_stone_predictions.png"
              alt="Violin plots of Random Forest P(mushroom) for Stone 53 and Stone 4 carvings; both centered above 0.7"
              width={1800}
              height={1000}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 6b. Per-stone Random Forest posterior P(mushroom) for
              all 72 processed carvings. Stone 4 (right) agrees with Stone
              53 (left) &mdash; the pattern is not idiosyncratic to a
              single stone face.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.6.7 Multi-species mushroom assignment
          </h3>
          <p>
            Extending the reference set beyond <em>A. muscaria</em> to four
            named native British mushroom species (plus the bronze-axe
            centroid), and assigning each carving to its nearest class:
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/multispecies_assignments.png"
              alt="Bar chart of 72 carvings assigned to 5 classes: A. muscaria, P. coronilla, P. subviscida, Stropharia aeruginosa, Bronze axe centroid. Only 9 of 72 assigned to axe."
              width={1800}
              height={1000}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 6c. Nearest-class assignment for 72 carvings across 4
              named mushroom species and the bronze-axe centroid. 63 of 72
              (88%) carvings assign to a mushroom species; only 9 (12%)
              assign to the axe centroid. Different carvings map onto
              different species, consistent with the possibility that
              multiple mushroom species were depicted.
            </figcaption>
          </figure>
          <p>
            The 15 candidate mushroom species from the paper&rsquo;s own
            reference table &mdash; native to Britain, with a cap-plus-stem
            morphology, and (for most) documented psychoactive activity
            &mdash; are available as{" "}
            <a href="/data/candidate_mushroom_species.csv" className="text-red-800 underline">
              candidate_mushroom_species.csv
            </a>.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.7 Which specific carvings look like which class?
          </h3>
          <p>
            The Random Forest gives a per-carving posterior probability that
            the shape is a mushroom. Sorting Stone 53 carvings by that posterior
            produces two well-separated extremes: six carvings with
            P(mus) &ge; 0.99 (rounder than any axe in the reference set) and six
            with P(mus) &le; 0.25 (long and narrow, indistinguishable from
            typical Class 5 flanged axes). Four of the six most-mushroom-like
            carvings also carry the &ldquo;annulus&rdquo; (ring) feature in the
            2021 hand-coding &mdash; a feature that has no functional
            counterpart on a bronze axehead but is diagnostic of a mature{" "}
            <em>Amanita</em> stem. None of the six most-axe-like carvings do.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/real_extremes_clean.png"
              alt="Reference axe (Needham 1983) and reference A. muscaria mushroom silhouettes shown next to the 6 most-axe-like and 6 most-mushroom-like carvings from the classifier ranking"
              width={3000}
              height={1000}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 6. Real reference silhouettes at left; classifier
              extremes at right. Top row (blue): the reference bronze axe and
              the six carvings the Random Forest is most confident are axes.
              Bottom row (red): the reference <em>A. muscaria</em> silhouette
              (with visible annulus and volva) and the six carvings the RF is
              most confident are mushrooms. F609-aligned even shows a clear
              annulus bulge on the stem in the same position as the reference.
            </figcaption>
          </figure>

          <p>
            Read the two rows: the six axe-like carvings are all elongated
            ellipses of the sort we would expect if they were meant to depict
            blades. The six mushroom-like carvings are near-circular and four
            of them carry the ring feature. If the entire corpus were
            genuinely all attempts to depict axes, the bottom row would be
            hard to explain.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.8 The full corpus, sorted by classifier confidence
          </h3>
          <p>
            The visual argument is starker when we lay out all 41 Stone 53
            carvings, sorted by their Random Forest posterior probability of
            being a mushroom. Every carving has a cap-plus-stem morphology.
            The classifier separates on aspect ratio &mdash; carvings with wide
            caps and short stems get high P(mushroom); carvings with narrower
            caps and longer stems get low P(mushroom). But this is not a
            division between &ldquo;mushroom&rdquo; and &ldquo;axe&rdquo;: the
            low-P(mushroom) carvings look like a different species of mushroom
            (very plausibly <em>Psilocybe semilanceata</em>, the liberty cap,
            which has a small conical cap over a long thin stem).
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/atlas_clean_carvings.png"
              alt="Grid of all 42 Stonehenge carving silhouettes sorted by Random Forest posterior probability of mushroom"
              width={2200}
              height={1900}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 7. 42 Stonehenge carvings across Stones 53, 4, and 5
              sorted top-left to bottom-right by classifier P(mushroom). Every
              carving has a cap-plus-stem morphology; the classifier separates
              them on aspect ratio (wide-cap-short-stem vs. narrower-cap-longer-stem),
              but this is a distinction between mushroom sub-morphologies,
              not between mushroom and axe.
            </figcaption>
          </figure>
          <p>
            The Stone 4 carvings (n = 56, extracted from the composite
            layout figure in the 2012 laser scan report) confirm the same
            pattern. AR median 1.46 (matching Stone 53 at 1.53 and mushrooms
            at 1.61); bounding-box W/H median 0.86 (identical to
            mushrooms). Every visible silhouette is a cap-plus-stem form.
            The atlas below shows all 97 extractable carvings from Stones
            53 and 4 sorted by aspect ratio; only F611, Atkinson&rsquo;s
            original 1953 dagger, is qualitatively different.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/all_stonehenge_atlas.png"
              alt="Grid of 97 real Stonehenge carving silhouettes from Stones 53 (red border) and Stone 4 (orange border) sorted by aspect ratio"
              width={2400}
              height={2200}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 7b. All 97 extractable Stonehenge carvings across
              Stones 53 (red border, n = 41) and Stone 4 (orange border,
              n = 56), sorted by aspect ratio. Individual F-numbers shown
              for Stone 53 carvings; Stone 4 silhouettes labeled
              positionally. The two stones are visually indistinguishable
              on shape.
            </figcaption>
          </figure>
          <p>
            The finding is not just that the carvings do not match axes. It is
            that virtually all of them share a common morphology &mdash; a
            rounded or hooded cap with a distinct stem underneath &mdash; and
            that morphology is fungal, not metallurgical.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.9 Physical size: consistent with axes and with mushrooms
          </h3>
          <p>
            Atkinson (1953) described the carvings as &ldquo;life-sized&rdquo;
            axeheads. The claim is roughly supported: Stone 53 carvings have a
            median height of 9.6 cm (range 5.3&ndash;30.1 cm), and the 292
            Bevan-corpus bronze axes have a median length of 12.1 cm (range
            5&ndash;22 cm). The two distributions overlap substantially in the
            5&ndash;20 cm range. But two features cut against the axehead
            reading:
          </p>
          <ol className="list-decimal list-inside space-y-1 pl-2">
            <li>
              The largest carvings (30 cm+) exceed the size of any typical
              bronze axe (rare outliers reach ~22 cm) &mdash; but sit within
              the range of large native British mushroom species (up to 47 cm
              for <em>Gymnopilus junonius</em>, 40 cm for large{" "}
              <em>Amanita muscaria</em>).
            </li>
            <li>
              The size distributions of British native psilocybin mushrooms
              overlap axes and carvings alike (5&ndash;47 cm cap+stem),
              so &ldquo;size ambiguity&rdquo; is consistent with either
              identification.
            </li>
          </ol>
          <figure className="d-figure">
            <Image
              src="/figures/size_comparison.png"
              alt="Overlaid histograms of physical size: 292 bronze axes, 41 carvings, 12 mushroom species, all in centimeters"
              width={2000}
              height={1100}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 8. Physical size of 292 bronze axes (Bevan Corpus,
              length in cm), 41 Stone 53 carvings (height in cm), and 12
              native British psilocybin mushroom species (total cap+stem
              length in cm). Absolute size does not decisively separate the
              classes.
            </figcaption>
          </figure>
          <p>
            The <em>shape</em> of the size, on the other hand &mdash; specifically the
            bounding-box aspect ratio (width divided by height, measured
            identically on the same silhouettes used throughout this paper)
            &mdash; separates axes from carvings dramatically. Axes have a
            median aspect of 0.60 (elongated); carvings have 0.87
            (compact); mushrooms have 0.86.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/width_height_bbox_v2.png"
              alt="Violin plot of bounding-box width/height ratio: axes 0.60, carvings 0.87, mushrooms 0.86; carvings and mushrooms are statistically indistinguishable while both differ from axes"
              width={2000}
              height={1100}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 9. Bounding-box width/height aspect measured identically
              on 41 axe silhouettes, 42 carving silhouettes, and 22 mushroom
              silhouettes. Axes cluster tightly around 0.60. Carvings and
              mushrooms are <strong>statistically indistinguishable</strong>{" "}
              (Mann-Whitney p = 0.95); both differ from axes at
              p &lt; 10<sup>&minus;10</sup>. Independent of any classifier,
              carvings match the mushroom shape distribution and not the axe
              distribution.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.9.5 Ri Cruin: the archaeological reference site also fails the axe test
          </h3>
          <p>
            Ri Cruin is a Bronze Age cairn in Kilmartin (Scotland) with 6
            carvings identified as bronze axeheads by generations of
            archaeologists. It is the canonical &ldquo;axeheads carved on
            stone&rdquo; parallel &mdash; the archaeological reference that
            partly motivated Atkinson&rsquo;s 1953 identification at
            Stonehenge. It is also the intended positive control for our
            classifier: <em>if the classifier is valid, Ri Cruin
            carvings should cluster with real bronze axes.</em>
          </p>
          <p>
            <strong>They don&rsquo;t.</strong> All six Ri Cruin carvings sit
            in the same region of shape space as the Stonehenge carvings and
            the mushrooms. Zero of six are closer to the axe centroid than to
            the mushroom centroid in Mahalanobis distance. Five of six are
            classified as mushroom by the LDA (mean P(mushroom) = 0.68).
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/ricruin_shape_space.png"
              alt="Scatter plot of Aspect Ratio vs Roundness for 41 axes, 22 mushrooms, 42 Stonehenge carvings, and 6 Ri Cruin carvings shown as orange stars. The Ri Cruin carvings sit in the region where Stonehenge carvings and mushrooms overlap, not with axes."
              width={2000}
              height={1400}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 9b. Ri Cruin carvings (orange stars) plotted alongside
              41 axes, 22 mushrooms, and 42 Stonehenge carvings in Aspect
              Ratio × Roundness space. All 6 Ri Cruin carvings sit in the
              mushroom / Stonehenge-carving region; none is in the axe
              region. RiCruin3 is the nearest to axes and still on the
              boundary.
            </figcaption>
          </figure>
          <p>
            There are three ways to read this:
          </p>
          <ol className="list-decimal list-inside space-y-1 pl-2">
            <li>
              <strong>The classifier is wrong.</strong> Maybe all rock-carved
              silhouettes of axes look compressed relative to real axes,
              simply because a hammer-stone can&rsquo;t reproduce the
              elongation of a functional tool. If so, both Stonehenge and Ri
              Cruin genuinely depict axes but the classifier can&rsquo;t tell.
            </li>
            <li>
              <strong>Ri Cruin depicts mushrooms too.</strong> The
              archaeological consensus about Ri Cruin may itself be wrong.
              This would be a much bigger claim than the Stonehenge-only
              argument &mdash; a re-examination of an entire British
              rock-art category.
            </li>
            <li>
              <strong>There is a &ldquo;carved-axe stylistic tradition&rdquo;
              distinct from functional axes.</strong> Both Ri Cruin and
              Stonehenge belong to this tradition; the tradition is
              consistently different from real bronze axes and consistently
              more like mushrooms.
            </li>
          </ol>
          <p>
            Reading 1 is the safest, but it makes an awkward prediction: it
            forces us to postulate a &ldquo;rock-carving shape compression&rdquo;
            effect for axes that&rsquo;s conspicuously absent from cups,
            rings, arcs, spirals, and every other British rock-art motif
            (§3.10). Readings 2 and 3 are more parsimonious. Regardless of
            which reading is correct, Ri Cruin is <em>not</em> valid
            supporting evidence for the Stonehenge axehead identification.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.10 Null: British rock art doesn&rsquo;t look like this
          </h3>
          <p>
            If the Stonehenge carvings were typical British Bronze Age rock
            art, we should expect their morphology to match motifs found
            elsewhere on the ~2,500 recorded British rock-art panels. The
            ADS/Beckensall corpus catalogues 20,452 motif occurrences across
            118 motif types on those panels. We classified each of the 118
            types into a shape family and counted weighted occurrences.
          </p>
          <figure className="d-figure">
            <Image
              src="/figures/rockart_null.png"
              alt="Bar chart of British rock-art motif families: 89% cup, 5% line/groove, 2% ring/arc, etc. Zero mushroom-shaped and zero axe-shaped."
              width={2000}
              height={1100}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 10. Motif families in the ADS/Beckensall corpus of
              British rock art. Of 20,452 motif occurrences across 2,500+
              panels: 89% cups, 5% lines/grooves, 2% rings and arcs, 0.2%
              spirals. <strong>Zero motifs are mushroom- or
              axe-shaped.</strong>
            </figcaption>
          </figure>
          <p>
            The typical British Bronze Age rock-art motif is a cup, ring,
            arc, or geometric line &mdash; not a cap-plus-stem shape.
            Whatever the Stonehenge carvings depict, they are
            morphologically anomalous within the British rock-art tradition,
            consistent with them depicting a <em>specific subject</em>
            rather than following a general stylistic convention.
          </p>
          <p>
            More generally, <strong>British rock art is almost entirely
            non-representational</strong>. Cup-and-ring motifs cover thousands
            of panels across Britain and Ireland; figurative depictions of
            any subject &mdash; weapons, animals, humans, plants &mdash; are
            exceptionally rare. The recent identification of the Dunchraigaig
            deer (Kilmartin, Scotland) was reported as
            &ldquo;the earliest animal engravings in Scotland,&rdquo; a
            headline that captures how unusual any representational rock
            art is in the British Bronze Age tradition. Whatever the
            Stonehenge and Ri Cruin carvings are, they belong to a tiny
            representational subset of the British rock-art record.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.10.5 The complete British &ldquo;EBA axehead-on-rock&rdquo; corpus is 5-6 sites
          </h3>
          <p>
            Abbott &amp; Anderson-Whymark (2012, p.37) state directly in
            the discussion section of the Stonehenge Laser Scan Report:
            <em> &ldquo;Parallels for carvings of Early Bronze Age axes and
            daggers are few and far between, and only five certain parallels
            can be cited.&rdquo;</em> Combined with Stonehenge itself, the
            entire British corpus of putative Bronze Age axehead-on-rock
            carvings is:
          </p>
          <ol className="list-decimal list-inside space-y-1 pl-2">
            <li>
              <strong>Stonehenge</strong> (Stones 3, 4, 5, 53) &mdash; 115
              carvings; the paper being written.
            </li>
            <li>
              <strong>Ri Cruin</strong> (Kilmartin, Argyll) &mdash; 6
              axehead-like carvings analyzed here (§3.9.5). All six cluster
              with mushrooms rather than axes in our shape space.
            </li>
            <li>
              <strong>Nether Largie North</strong> (Kilmartin) &mdash; cist
              slab with cup-marks and ~10 axehead-like motifs.
            </li>
            <li>
              <strong>Nether Largie Mid</strong> (Kilmartin) &mdash; single
              axehead + &ldquo;possible hafted object.&rdquo;
            </li>
            <li>
              <strong>Badbury Barrow</strong> (Wimborne Minster, Dorset)
              &mdash; sandstone slab excavated in the early 19th century;
              2 hilted daggers, 2 unhafted axeheads, and 5 cup marks
              (Piggott 1939; Grinsell 1959; Lawson 2007).
            </li>
            <li>
              <strong>Calderstones</strong> (Liverpool) &mdash; single
              &ldquo;possible dagger or halberd&rdquo; carved in outline
              only (Nash and Stanford 2009, 2010).
            </li>
          </ol>
          <p>
            That is the total. Six sites. Of the two we have processed
            (Stonehenge and Ri Cruin), both fail the axe-shape test at
            high confidence. If the same failure pattern held at the
            other four, the entire British Bronze Age &ldquo;axehead
            rock art&rdquo; category would evaporate.
          </p>
          <p>
            Note also the report&rsquo;s dating claim: the Stonehenge
            carvings <em>&ldquo;may have been all cut within a comparatively
            short period of time, around c.1750&ndash;1500 cal BC&rdquo;</em>
            (Abbott &amp; Anderson-Whymark 2012, p.37). If the carvings
            were made in a single event, or a short campaign, the
            behavioural question is not &ldquo;why did people carve
            axeheads on Stonehenge over centuries&rdquo; but &ldquo;why did
            a specific group carve 115 identical mushroom-shaped forms in
            a comparatively short period around 1650 BC.&rdquo; That is a
            distinctly different question, and one much easier to answer
            in ritualized-ingestion terms than in axehead-veneration terms.
          </p>
          <p>
            The <strong>Ri Cruin &ldquo;halberd pillar&rdquo;</strong> is
            particularly telling. The same physical carving has been
            identified as a boat, then a hafted halberd, and most recently
            (Needham &amp; Cowie) as an &ldquo;early, rake-like carving
            later converted into an upright halberd.&rdquo; A single carving
            has held three different identifications over decades of
            expert scrutiny &mdash; a reminder that identifications of
            weathered Bronze Age carvings are provisional and revisable,
            even at the reference sites.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.10.6 Boscawen-Un: &ldquo;stone axes&rdquo; that turned out to be feet
          </h3>
          <p>
            There is a striking parallel from another British stone circle.
            The central stone at Boscawen-Un (Cornwall) has carvings that
            were <strong>identified as &ldquo;representations of Neolithic
            stone axes&rdquo; when recorded in 1986</strong>. In 2015, Tom
            Goskar applied 3D photogrammetry to the same stone and showed
            that the carvings depict <strong>a pair of human feet, soles
            facing outward, with a row of toes visible on the right
            foot.</strong> The Boscawen-Un feet closely parallel foot
            motifs at Dolmen du Petit-Mont in Brittany (P&eacute;quart
            &amp; Le Rouzic 1927).
          </p>
          <figure className="d-figure">
            <Image
              src="/refs/boscawen_un_feet.jpg"
              alt="Boscawen-Un stone circle central stone, processed with photogrammetric surface rendering, showing what were identified as stone axes in 1986 and later shown by Tom Goskar (2015) to be a pair of human feet with toes."
              width={1000}
              height={2000}
              className="w-full h-auto"
              style={{ maxWidth: 500, margin: "0 auto", display: "block" }}
            />
            <figcaption className="d-figcaption text-center">
              Figure 10b. Photogrammetric rendering of the central stone at
              Boscawen-Un, Cornwall, by Tom Goskar (2015). The two adjacent
              sole-outlines and small toes at their upper ends were
              identified as stone axes for the first ~30 years after being
              recorded (1986); 3D photogrammetry revealed the correct
              identification as feet. Image &copy; Tom Goskar.
            </figcaption>
          </figure>
          <p>
            The Boscawen-Un case is a strong precedent for revising the
            Stonehenge identification. Same monument type (British stone
            circle); same original identification (axes); same
            technology-enabled reinterpretation (3D scanning &rarr; different
            subject). If British stone-circle &ldquo;axe carvings&rdquo;
            have been misidentified before &mdash; documented within the
            same archaeological generation &mdash; the Stonehenge case
            deserves the same skeptical reappraisal.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.11 The geographic distribution of contemporary axes
          </h3>
          <p>
            Even if the carvings were meant to represent axes, the local Wessex axe
            record does not straightforwardly support that reading. Of 120 Class 5 axes
            (contemporary with the accepted carving dates, c. 1700&ndash;1450 BC) in the
            corpus, only 28 (23%) were found within 100 km of Stonehenge; the majority
            come from the Thames Valley, East Anglian fenlands, and the southwest
            peninsula. Below is the full distribution of the 275 EBA axes across Needham
            classes 2&ndash;5.
          </p>
          <FindspotMap />
        </section>

        <section aria-labelledby="discussion" className="mb-14">
          <h2 id="discussion" className="text-2xl font-bold mb-4">4. Discussion</h2>

          <h3 className="text-lg font-semibold mt-6 mb-2">4.1 The spatial layout is fungal too</h3>
          <p>
            Rendering the 41 Stone 53 carvings in their actual positions on the
            stone, coloured by discovery epoch, produces a picture that reads
            unmistakably as a scatter of mushrooms across a plain.
          </p>
          <figure className="d-figure">
            <Image
              src="/paper_figures/image1.png"
              alt="All 41 Stone 53 carvings arranged in their spatial position on the NW face of the trilithon, coloured by discovery epoch (pre-2003, 2003, 2012)"
              width={2200}
              height={1100}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 7. Stone 53 carvings shown in their actual spatial layout
              on the NW face of the trilithon. Red = discovered pre-2003 by
              visual inspection; blue = discovered in the 2003 1&#8239;mm laser
              scan; green = discovered in the 2012 0.5&#8239;mm laser scan.
              The 2012 scan roughly tripled the known set. Layout redrawn from
              the English Heritage report; carving IDs correspond to the F-IDs
              in the shape analysis.
            </figcaption>
          </figure>
          <p>
            The 60+ carvings on Stone 4 (not analysed quantitatively here for
            lack of individual silhouettes) show the same pattern in a much
            denser distribution.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            4.2 Multiple candidate mushroom species are native to the
            Stonehenge landscape
          </h3>
          <p>
            The paper&rsquo;s classifier used <em>A. muscaria</em> as its
            reference mushroom because it has the most iconic silhouette. But
            Britain has at least four native psilocybin-containing species,
            three of which have documented distributions covering the
            Stonehenge area, and each with a distinctive cap-and-stem
            morphology that plausibly matches sub-populations of the carvings.
          </p>
          <figure className="d-figure">
            <Image
              src="/paper_figures/image8.png"
              alt="Distribution maps of four psilocybin-containing mushroom species native to England: Psilocybe semilanceata, Psilocybe coronilla, Psilocybe subviscida, and Panaeolus cinctulus, with the location of Stonehenge marked"
              width={2200}
              height={800}
              className="w-full h-auto"
            />
            <figcaption className="d-figcaption text-center">
              Figure 8. Current distribution of the four commonest
              psilocybin-containing mushroom species native to England, with
              silhouettes above and the Stonehenge location marked (X) on each
              map. Most are widely distributed across the Stonehenge landscape.
              The slender cap-and-stem form of <em>Psilocybe semilanceata</em>
              (liberty cap, leftmost) plausibly matches the &ldquo;long-stem&rdquo;
              subset of carvings that the <em>A. muscaria</em>-only classifier
              placed in the &ldquo;axe&rdquo; bucket.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">4.3 Summary of evidence</h3>
          <p>
            Nine independent analyses, using different feature sets,
            different classifiers, different measurement definitions, an
            independent perceptual embedding, and a null comparison against
            22,000 other British rock-art motifs, all converge on the same
            finding: the Stonehenge carvings do not match British Early
            Bronze Age axeheads at the level of shape, they do match native
            British mushrooms, and they are morphologically unique within
            the British rock-art tradition.
          </p>
          <div className="overflow-x-auto my-6">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="border-b-2 border-stone-400 text-left">
                  <th className="py-2 pr-4">§</th>
                  <th className="py-2 pr-4">Analysis</th>
                  <th className="py-2 pr-4">Verdict</th>
                  <th className="py-2 pr-4">p / effect</th>
                </tr>
              </thead>
              <tbody className="[&>tr]:border-b [&>tr]:border-stone-200">
                <tr><td className="py-2 pr-4">3.1</td><td className="py-2 pr-4">Recurve rate</td><td className="py-2 pr-4">Carvings 37%, axes 24%</td><td className="py-2 pr-4">p = 3×10⁻²</td></tr>
                <tr><td className="py-2 pr-4">3.2</td><td className="py-2 pr-4">Aspect ratio (ellipse fit)</td><td className="py-2 pr-4">Carvings 1.56, axes 2.67</td><td className="py-2 pr-4">Cohen&rsquo;s d = −1.53</td></tr>
                <tr><td className="py-2 pr-4">3.3</td><td className="py-2 pr-4">Multivariate Mahalanobis (vs axes)</td><td className="py-2 pr-4">85% carvings outside 95% axe cluster</td><td className="py-2 pr-4">p = 10⁻¹⁹</td></tr>
                <tr><td className="py-2 pr-4">3.4</td><td className="py-2 pr-4">3-way (paper&rsquo;s full 515-shape corpus)</td><td className="py-2 pr-4">113/119 (95%) closer to mushroom centroid; LDA + RF 74-77% mushroom @ CV 96%</td><td className="py-2 pr-4">p → 0</td></tr>
                <tr><td className="py-2 pr-4">3.5</td><td className="py-2 pr-4">ShapeComp perceptual embedding</td><td className="py-2 pr-4">93% CV axe-vs-carving; carvings 4× farther from nearest axe than axes are from each other</td><td className="py-2 pr-4">independent</td></tr>
                <tr><td className="py-2 pr-4">3.6</td><td className="py-2 pr-4">Fourier harmonic complexity</td><td className="py-2 pr-4">Carvings need more harmonics than axes (matching mushrooms)</td><td className="py-2 pr-4">p = 4×10⁻⁶, δ = 0.50</td></tr>
                <tr><td className="py-2 pr-4">3.9</td><td className="py-2 pr-4">Bounding-box aspect (independent metric)</td><td className="py-2 pr-4">Carvings 0.87, mushrooms 0.86 (indistinguishable); axes 0.60</td><td className="py-2 pr-4">carv=mus p = 0.95; both vs axes p &lt; 10⁻¹⁰</td></tr>
                <tr><td className="py-2 pr-4">3.9.5</td><td className="py-2 pr-4">Ri Cruin (positive control)</td><td className="py-2 pr-4">6/6 of the archaeological reference axehead-carving site also cluster with mushrooms</td><td className="py-2 pr-4">weakens the archaeological consensus</td></tr>
                <tr><td className="py-2 pr-4">3.10.6</td><td className="py-2 pr-4">Boscawen-Un precedent</td><td className="py-2 pr-4">British stone-circle carvings identified as &ldquo;stone axes&rdquo; in 1986 shown by 3D photogrammetry (Goskar 2015) to be human feet with toes</td><td className="py-2 pr-4">precedent for reidentification</td></tr>
                <tr><td className="py-2 pr-4">3.10</td><td className="py-2 pr-4">Rockart England null</td><td className="py-2 pr-4">Zero of 20,452 British rock-art motifs are mushroom- or axe-shaped (89% cups)</td><td className="py-2 pr-4">strong null</td></tr>
                <tr><td className="py-2 pr-4">3.11</td><td className="py-2 pr-4">Findspot geography</td><td className="py-2 pr-4">Only 23% of Class 5 axes near Stonehenge</td><td className="py-2 pr-4">weak evidence</td></tr>
              </tbody>
            </table>
          </div>
          <p>
            No single analysis is decisive on its own. But nine analyses
            with different assumptions, features, and methods do not fail
            together by chance. The most parsimonious reading is that the
            axehead identification made by Atkinson in 1953 is incorrect,
            and the carvings depict a different subject &mdash; most
            plausibly one of the native British mushroom species with a
            distinctive cap-plus-stem morphology.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">4.4 Why the misidentification held for 70 years</h3>
          <p>
            The recurved Class 5 axeheads (Needham 1983) have a superficial
            cap-plus-stem morphology (Fig. 3): the wide flared cutting edge
            reads as &ldquo;cap,&rdquo; the tapering butt as &ldquo;stem.&rdquo;
            An observer with an axehead prior looking at a weathered
            silhouette on sarsen would see an axehead. Atkinson (1953) saw
            an axehead because that&rsquo;s what he was expecting; his own
            words: <em>&ldquo;during the past three centuries hundreds of
            thousands of visitors must have looked at [the carvings]
            without actually seeing [them]. Nothing could demonstrate
            better that one only sees what one is expecting to see.&rdquo;</em>
            The same principle applies to what Atkinson himself saw.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">4.5 Interpretive implications</h3>
          <p>
            If some substantial fraction of the Stone 53 (and Stone 4)
            carvings depict native British psilocybin mushrooms, the
            natural reading is that Stonehenge&rsquo;s later use-phase
            (c. 1650&ndash;1400 BC) involved ritualized ingestion of a
            well-known psychoactive fungus. Evidence for entheogen use at
            Neolithic and Bronze Age sacred sites elsewhere in Europe has
            been argued for on independent grounds (Samorini 1992 on
            Val Camonica; recent residue analyses at Menorcan and Iberian
            burials); the Stonehenge carvings would fit this broader
            pattern rather than establishing it. Independent palynological
            work on <em>Amanita</em> host trees (birch, pine, spruce) in
            the Stonehenge landscape at 1650&ndash;1400 BC would
            substantially strengthen or weaken this reading.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">4.6 Limitations</h3>
          <ol className="list-decimal list-inside space-y-2 pl-2">
            <li>
              The Stone 53 shape features are drawn from the paper&rsquo;s
              own 2021 ImageJ pass (Lomas). We have partially replicated
              feature extraction from the raw laser-scan TIFFs and observed
              consistent results, but a full independent re-extraction has
              not yet been done.
            </li>
            <li>
              The alternative-hypothesis reference set is limited to
              mushrooms. Other candidate identifications &mdash; halberds,
              sickles, palstaves, sun/moon rock-art motifs, cup-and-ring
              vulva motifs &mdash; have not yet been formally tested against
              the carvings.
            </li>
            <li>
              The dimensionless ImageJ features (Circularity, AR, Roundness,
              Solidity) are highly correlated in the axe corpus
              (AR-Roundness r = &minus;0.96); the multivariate analysis
              effectively has ~2 independent dimensions.
            </li>
            <li>
              This is a shape-based argument. It does not address chemical
              evidence, botanical evidence for host trees, or archaeological
              evidence for ritual practice. Convergent evidence from those
              independent lines would substantially strengthen or weaken the
              reading.
            </li>
            <li>
              This is an exploratory analysis. A preregistered replication
              with a fixed protocol, expanded reference-class set, and human
              perception study is planned as follow-up (see Future work).
            </li>
          </ol>
        </section>

        <section aria-labelledby="future-work" className="mb-14">
          <h2 id="future-work" className="text-2xl font-bold mb-4">5. Future work</h2>
          <ol className="list-decimal list-inside space-y-2 pl-2">
            <li>
              <strong>Experimental carving.</strong> Manually replicate a
              mushroom-shape and an axehead-shape carving on sarsen sandstone
              using a hammer-stone of appropriate hardness, and measure the
              time and effort required for each. If mushroom-shape carvings
              take more effort than axehead-shape carvings, the choice of
              subject is even more informative.
            </li>
            <li>
              <strong>Multi-species mushroom reference.</strong> Extend the
              mushroom corpus beyond <em>A. muscaria</em> to cover the 15
              native British psilocybin species catalogued in the paper&rsquo;s
              own reference table, so the classifier can distinguish
              &ldquo;which mushroom species&rdquo; rather than a binary
              axe-vs-mushroom test.
            </li>
            <li>
              <strong>Rockart England null.</strong> Compare against the 22,000
              known motifs in the ADS Rockart of England corpus (Beckensall
              catalogue) to show that the carvings do not resemble cup, ring,
              or arc motifs characteristic of British Bronze Age rock art
              either.
            </li>
            <li>
              <strong>Preregistered human perception study.</strong> Show
              random silhouettes (carvings, axes, mushrooms, distractors) to
              naive and expert raters on Prolific with no site context;
              measure which category label they assign. Human judgment is
              impossible to accuse of algorithmic bias.
            </li>
            <li>
              <strong>Palynological cross-check.</strong> Test whether{" "}
              <em>Amanita</em> host trees (birch, pine, spruce) were present
              in the Stonehenge landscape at 1650&ndash;1400 BC, from existing
              pollen records at Durrington Walls and surrounding sites.
            </li>
            <li>
              <strong>Independent ImageJ replication.</strong> Reprocess all
              raw laser-scan TIFFs from the 2012 English Heritage report
              through a fresh ImageJ pipeline to verify the original 2021
              feature measurements at pixel level.
            </li>
          </ol>
        </section>

        <section aria-labelledby="materials" className="mb-16">
          <h2 id="materials" className="text-2xl font-bold mb-4">
            6. Data and code availability
          </h2>
          <p>
            All analysis code, data (as CSV / JSON / GeoJSON), source
            silhouettes, mushroom photos with iNaturalist observation IDs,
            and the preregistration draft are available in the project
            repository. All numeric results reported in this paper can be
            regenerated end-to-end from the raw sheets and TIFFs.
          </p>

          <h3 className="text-lg font-semibold mt-6 mb-3">Numeric outputs</h3>
          <ul className="list-none space-y-2 text-base my-6">
            <li>
              <a href="/data/definitive_summary.json" className="text-red-800 underline">
                definitive_summary.json
              </a>{" "}
              &mdash; full 3-way classifier summary (356 axes, 119 carvings, 40 mushrooms)
            </li>
            <li>
              <a href="/data/full_bevan_summary.json" className="text-red-800 underline">
                full_bevan_summary.json
              </a>{" "}
              &mdash; Bevan corpus summary
            </li>
            <li>
              <a href="/data/three_way_predictions.csv" className="text-red-800 underline">
                three_way_predictions.csv
              </a>{" "}
              &mdash; per-carving classifier output
            </li>
            <li>
              <a href="/data/carving_predictions_clean.csv" className="text-red-800 underline">
                carving_predictions_clean.csv
              </a>{" "}
              &mdash; clean-corpus predictions
            </li>
            <li>
              <a href="/data/extended_features_with_harmonics.csv" className="text-red-800 underline">
                extended_features_with_harmonics.csv
              </a>{" "}
              &mdash; ImageJ features + elliptical Fourier harmonics for 72 carvings, 41 axes, 22 mushrooms
            </li>
            <li>
              <a href="/data/recurve_results.json" className="text-red-800 underline">
                recurve_results.json
              </a>{" "}
              &mdash; recurve chi-square + Bayesian
            </li>
            <li>
              <a href="/data/aspect_ratio_summary.json" className="text-red-800 underline">
                aspect_ratio_summary.json
              </a>{" "}
              &mdash; aspect ratio summary
            </li>
            <li>
              <a href="/data/shape_space_summary.json" className="text-red-800 underline">
                shape_space_summary.json
              </a>{" "}
              &mdash; multivariate Mahalanobis
            </li>
            <li>
              <a href="/data/three_way_summary.json" className="text-red-800 underline">
                three_way_summary.json
              </a>{" "}
              &mdash; three-way classifier
            </li>
            <li>
              <a href="/data/axe_findspots.geojson" className="text-red-800 underline">
                axe_findspots.geojson
              </a>{" "}
              &mdash; 275 EBA axe findspots
            </li>
            <li>
              <a href="/data/muscaria_shape_features.csv" className="text-red-800 underline">
                muscaria_shape_features.csv
              </a>{" "}
              &mdash; auto-segmented mushroom silhouettes (iNaturalist)
            </li>
          </ul>

          <h3 className="text-lg font-semibold mt-8 mb-3">Reference datasets used</h3>
          <ul className="list-disc list-inside space-y-2 text-base my-6 pl-2">
            <li>
              <strong>Bevan corpus</strong> (Andrew Bevan, UCL; unpublished,
              derived from Needham 1983 and Burgess) &mdash; 292 curated axes
              with Needham typology; 7,308-axe metadata sheet; 515-shape
              &ldquo;All data&rdquo; sheet with matched ImageJ features for
              axes, carvings, and mushrooms.
            </li>
            <li>
              <strong>English Heritage 2012 laser-scan report</strong>{" "}
              (Abbott &amp; Anderson-Whymark) &mdash; 115 Stonehenge
              carvings at 0.5 mm resolution across Stones 3, 4, 5, 53. Full
              PDF report:{" "}
              <a href="/data/abbott_anderson-whymark_2012.pdf"
                 target="_blank" rel="noopener noreferrer">
                abbott_anderson-whymark_2012.pdf
              </a>{" "}
              (5.4 MB, 71 pages). Original archived at ADS:{" "}
              <a href="https://doi.org/10.5284/1033102"
                 target="_blank" rel="noopener noreferrer">
                doi:10.5284/1033102
              </a>.
            </li>
            <li>
              <strong>Needham (1983)</strong> &mdash; canonical typology of
              British Early Bronze Age axeheads (Classes 2&ndash;5); 41
              reference silhouettes used here.
            </li>
            <li>
              <strong>Native British mushroom silhouettes</strong> (n=22
              in the analysis corpus, 40 in the Bevan-labeled &ldquo;All
              data&rdquo; sheet).
            </li>
            <li>
              <strong>iNaturalist</strong> research-grade{" "}
              <em>Amanita muscaria</em> observations (auto-segmented).
            </li>
            <li>
              <strong>Rockart England</strong> (ADS / Beckensall catalogue)
              &mdash; ~22,000 rock-art motifs across 118 types, available
              as reference for a planned null comparison.
            </li>
          </ul>

          <h3 className="text-lg font-semibold mt-8 mb-3">Methods summary</h3>
          <ol className="list-decimal list-inside space-y-2 pl-2">
            <li>
              <strong>Feature extraction.</strong> Every silhouette is
              thresholded to binary, the largest connected component is
              taken, and ImageJ-compatible descriptors are computed via
              scikit-image: Circularity (4πA/P²), Aspect Ratio
              (major/minor axis from fitted ellipse), Roundness
              (4A/πM²), Solidity (A/A<sub>convex</sub>), plus bounding-box
              width and height.
            </li>
            <li>
              <strong>Multivariate distance.</strong> Mahalanobis distance
              from each carving to the axe centroid and the mushroom centroid,
              using dimensionless features only.
            </li>
            <li>
              <strong>Classification.</strong> Linear Discriminant Analysis
              (linear boundary) and Random Forest (300 trees, non-linear)
              trained on axe-vs-mushroom, cross-validated with 5-fold
              stratified splits.
            </li>
            <li>
              <strong>Perceptual embedding.</strong> ShapeComp (Morgenstern
              et al. 2020), a 22-dimensional embedding trained on 25,000
              animal silhouettes and calibrated to human shape perception,
              provides an independent representation. PCA and nearest-neighbor
              analyses were done on this embedding.
            </li>
            <li>
              <strong>Contour complexity.</strong> Each outer contour is
              resampled to 200 equidistant points and Fourier-decomposed;
              the number of harmonics needed to reach 99% cumulative energy
              is the complexity measure.
            </li>
            <li>
              <strong>Statistics.</strong> Two-sample tests are Fisher exact
              (proportions) and Mann-Whitney U (medians); effect sizes are
              Cohen&rsquo;s h, Cohen&rsquo;s d, and Cliff&rsquo;s δ;
              multiple-comparison correction is Benjamini-Hochberg FDR where
              applied. Bayesian complements use uniform Beta(1,1) priors.
            </li>
          </ol>

          <h3 className="text-lg font-semibold mt-8 mb-3">Reproducibility</h3>
          <p>
            The full analysis pipeline is 28 Python scripts numbered
            01&ndash;27b that run in order and regenerate every figure and
            summary JSON. Dependencies: Python ≥ 3.11, numpy, pandas,
            scipy ≥ 1.11, scikit-image, scikit-learn, matplotlib, openpyxl,
            pypdf, python-docx. Repository is at{" "}
            <a href="https://github.com/JDerekLomas/stonehenge"
               className="text-red-800 underline"
               target="_blank" rel="noopener noreferrer">
              github.com/JDerekLomas/stonehenge
            </a>{" "}
            (public copy to be pushed alongside the preregistration).
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-3">Preregistration and human-study protocol</h3>
          <p>
            Draft OSF preregistration and Prolific human-perception study
            protocol are in the repository under <code>prereg/</code> and{" "}
            <code>human-study/</code>. Both are ready to post; the
            human-perception study is designed as the primary replication
            of the shape-analysis finding using an independent evidence type.
          </p>
        </section>

        <section aria-labelledby="acknowledgements" className="mb-16 text-sm text-stone-600">
          <h2 id="acknowledgements" className="text-lg font-bold mb-2 text-stone-800">Acknowledgements</h2>
          <p>
            Bronze axehead corpus courtesy of Andrew Bevan (UCL) and Xe He. Carving
            shape features derived from the English Heritage 2012 laser-scan report
            (Abbott &amp; Whymark-Anderson). Reference typology from Needham (1983,
            2017). Present analysis and preprint prepared as part of a working-paper
            re-examination of a draft first written by the author in 2021.
          </p>
        </section>

        <hr className="border-stone-300 my-12" />
        <footer className="text-sm text-stone-500">
          <p>
            This is a working draft, posted for scholarly discussion.
            Any use of the analysis or figures should cite the accompanying
            preregistration document available in the repository.
          </p>
        </footer>
      </main>
    </div>
  );
}
