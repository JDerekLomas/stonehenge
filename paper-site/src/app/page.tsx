import Image from "next/image";
import Link from "next/link";
import { FindspotMap } from "@/components/FindspotMap";
import { MuscariaGrid } from "@/components/MuscariaGrid";

export default function Home() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-stone-200 bg-stone-100">
        <div className="max-w-4xl mx-auto px-6 py-16">
          <p className="text-xs uppercase tracking-widest text-stone-500 mb-4">
            Working paper &middot; Preprint &middot; 2026
          </p>
          <h1 className="text-4xl md:text-5xl font-bold leading-tight text-stone-900 mb-6">
            Are the carvings on Stonehenge bronze axeheads &mdash; or mushrooms?
          </h1>
          <p className="text-xl text-stone-700 leading-relaxed mb-6">
            A quantitative shape analysis of 119 prehistoric carvings on
            Stonehenge, compared against 356 British bronze axeheads (Bevan
            corpus, drawn from Needham 1983 and Burgess) and 40 mushroom
            silhouettes, finds that 113 of 119 (95%) carvings are closer to
            the mushroom centroid than to the axe centroid in shape space.
            Linear Discriminant Analysis and Random Forest classifiers,
            cross-validated at 96% accuracy on axes vs. mushrooms, classify
            77% of the carvings as mushroom with mean posterior 0.74. An
            independent ShapeComp perceptual embedding separates axes from
            carvings at 94% cross-validated accuracy. The convergent evidence
            motivates re-examination of the axehead identification that has
            stood since 1953.
          </p>
          <div className="text-sm text-stone-600 space-y-1">
            <p>
              <span className="font-semibold">J. Derek Lomas</span>, TU Delft
            </p>
            <p>Draft &middot; last updated {new Date().toISOString().slice(0, 10)}</p>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-16 prose">
        <section aria-labelledby="abstract" className="mb-16">
          <h2 id="abstract" className="text-2xl font-bold mb-4">Abstract</h2>
          <p className="text-lg leading-relaxed text-stone-800">
            Between 1953 and 2012, laser-scanning revealed 115 prehistoric carvings on the
            sarsen stones of Stonehenge, of which the most conspicuous were interpreted
            as blade-up bronze axeheads dated to 1650&ndash;1400 BC. This identification
            has been repeated in every subsequent treatment of the monument. We test it
            quantitatively for the first time. Using shape descriptors extracted with
            ImageJ, we find that (i) the &ldquo;recurve&rdquo; feature diagnostic of
            certain axe types occurs 5&ndash;6&times; more often on the carvings than on
            real Early Bronze Age axeheads (Fisher exact p = 1.3&times;10<sup>&minus;7</sup>);
            (ii) 68% of Stone 53 carvings are less elongated than the least elongated
            2.5% of real axes (Cohen&rsquo;s d = &minus;1.53, KS p = 2&times;10<sup>&minus;16</sup>);
            (iii) 85% of Stone 53 carvings fall outside the 95% multivariate axe-cluster
            ellipsoid; and (iv) when compared against a corpus of 55{" "}
            <em>Amanita muscaria</em> silhouettes drawn from iNaturalist, 97.6% of Stone 53
            carvings are closer to the mushroom centroid than the axe centroid, and both
            linear and non-linear classifiers (cross-validated at 85&ndash;92% accuracy on
            axes vs. mushrooms) place 73&ndash;76% of the carvings in the mushroom class
            with mean confidence 0.71&ndash;0.76. The convergent evidence motivates
            re-examination of the axehead identification and of the cultural
            interpretation of the carvings.
          </p>
        </section>

        <section className="mb-16">
          <figure className="my-6">
            <Image
              src="/figures/named_species_plate.png"
              alt="Named comparison plate: four psilocybin mushroom species, eight canonical Needham axeheads, and eight Stonehenge carvings, arranged in three rows"
              width={2800}
              height={1200}
              className="rounded-md border border-stone-200 w-full h-auto"
              priority
            />
            <figcaption className="text-sm text-stone-600 mt-3 text-center italic">
              Frontispiece. Top row: four native British psilocybin
              mushroom species. Middle row: eight canonical British Early
              Bronze Age axehead forms (Needham 1983, Class 2A through the
              late-Bronze form). Bottom row: eight Stonehenge carvings
              from Stone 53. Read column-wise: the carvings share their
              cap-plus-stem morphology with the mushrooms, not with the
              bulky wide-shouldered forms of the axes.
            </figcaption>
          </figure>
          <figure className="my-6">
            <Image
              src="/paper_figures/image3.png"
              alt="Side-by-side comparison: mushroom-shaped carvings on Stones 53 and 4 of Stonehenge, next to canonical Southern British bronze axeheads from 2500 to 1600 BC"
              width={2000}
              height={800}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-3 text-center italic">
              The same visual argument, drawn from the paper&rsquo;s own
              working figure: left, the full set of Stone 53 and Stone 4
              carvings; right, the canonical Southern British axehead
              typology 2500&ndash;1600 BC.
            </figcaption>
          </figure>
        </section>

        <section aria-labelledby="intro" className="mb-16">
          <h2 id="intro" className="text-2xl font-bold mb-4">1. Introduction</h2>
          <p>
            In July 1953, archaeologist Richard Atkinson noticed what appeared to be a
            sword and an axehead carved into Stone 53 of Stonehenge&rsquo;s inner
            trilithon. By 2012, laser-scanning by English Heritage had extended the count
            to 118 probable prehistoric carvings on four stones. The identification of the
            carvings as blade-up bronze axeheads &mdash; of the &ldquo;crescentic&rdquo;
            forms manufactured c. 1650&ndash;1400 BC &mdash; has been repeated in every
            subsequent treatment of the site.
          </p>
          <p>
            The identification has, however, never been tested quantitatively. Atkinson
            eyeballed the two most distinctive carvings on Stone 53 in 1953; the
            subsequent 113 carvings were assimilated to his identification. The purpose of
            this paper is to ask, with modern computer vision techniques and a properly
            curated reference corpus, whether the carvings as a population actually match
            the shape distribution of real British Early Bronze Age (EBA) axeheads.
          </p>
          <p>
            The answer, as we show below, is no. Whatever the carvings represent, they do
            not systematically match real axeheads at the level of any of four canonical
            dimensionless shape features, and they match one specific alternative
            reference &mdash; the fly agaric mushroom, <em>Amanita muscaria</em> &mdash;
            remarkably well.
          </p>
        </section>

        <section aria-labelledby="methods" className="mb-16">
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
          <figure className="my-8">
            <Image
              src="/figures/atlas_clean_mushrooms.png"
              alt="Atlas of 22 mushroom reference silhouettes"
              width={2000}
              height={1200}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-8">
            <Image
              src="/paper_figures/needham_reference.png"
              alt="Needham 1983 Class 5D reference figure showing axe subtypes 85 through 89 with anatomical annotations"
              width={2000}
              height={1600}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-8">
            <Image
              src="/paper_figures/hafted_axes.png"
              alt="Reconstruction of two hafted bronze axes with wooden handles"
              width={1600}
              height={1150}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 3b. Reconstruction of hafted bronze axes. Real bronze
              axeheads were used mounted on wooden handles; the &ldquo;axehead
              alone&rdquo; that Atkinson (1953) described the carvings as
              depicting would be an unusual choice of subject &mdash; the
              functional whole is the hafted implement.
            </figcaption>
          </figure>
          <figure className="my-8">
            <Image
              src="/figures/atlas_clean_axes.png"
              alt="Atlas of 41 axe reference silhouettes from Needham 1983 and Burgess"
              width={2000}
              height={1500}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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

        <section aria-labelledby="results" className="mb-16">
          <h2 id="results" className="text-2xl font-bold mb-4">3. Results</h2>

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
          <figure className="my-8">
            <Image
              src="/figures/recurve_comparison.png"
              alt="Bar chart: recurve rate in Stonehenge carvings (Stone 53, Stone 4, all) vs British EBA axes"
              width={1600}
              height={1000}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
            for a handle grip and blade. The 124 Bevan-corpus axes have AR = 2.71 &plusmn;
            0.42 (range 1.65&ndash;4.53). The 41 Stone 53 carvings have AR = 1.76 &plusmn;
            0.76 (range 1.08&ndash;5.37).
          </p>
          <p>
            <span className="font-semibold">
              68% (28 of 41) of Stone 53 carvings are less elongated than the least
              elongated 2.5% of British EBA axes.
            </span>{" "}
            Cohen&rsquo;s d = &minus;1.53 (very large), Kolmogorov&rsquo;s D = 0.73, p =
            2&times;10<sup>&minus;16</sup>. A skilled carver reproducing an axe from
            memory would not systematically flatten it.
          </p>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.3 Carvings sit outside the multivariate axe-cluster
          </h3>
          <p>
            Under Mahalanobis distance in the four-dimensional (Circularity, AR,
            Roundness, Solidity) space, 90.3% of axes fall within their own 95% cluster
            ellipsoid &mdash; validating the model. Only 14.6% of Stone 53 carvings do.
            Mann-Whitney U comparing the two distance distributions gives p = 1.5&times;
            10<sup>&minus;19</sup>. The result is robust across every subset of the four
            features (12&ndash;30% of carvings inside the axe ellipsoid across all
            2&ndash;4-feature Mahalanobis tests), so it is not driven by any single
            feature.
          </p>
          <figure className="my-8">
            <Image
              src="/figures/mahalanobis_histogram.png"
              alt="Histogram: Mahalanobis distance from British EBA axe centroid for axes and carvings"
              width={1600}
              height={900}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-8">
            <Image
              src="/figures/definitive_violin.png"
              alt="Violin plots comparing Circularity, Aspect Ratio, and Roundness across the paper's full labeled corpus of 356 axes, 119 carvings, and 40 mushrooms"
              width={2600}
              height={950}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 4. Distributions of the three dimensionless shape features
              across the paper&rsquo;s definitive corpus. Carvings and
              mushrooms are visually indistinguishable on Aspect Ratio and
              Roundness; axes are systematically different.
            </figcaption>
          </figure>
          <figure className="my-8">
            <Image
              src="/figures/three_way_violin.png"
              alt="Violin plots of Circularity, Aspect Ratio, and Roundness across axes, carvings, and A. muscaria"
              width={2000}
              height={900}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-6">
            <Image
              src="/figures/shapecomp_pca.png"
              alt="PCA scatter of ShapeComp 22-dimensional perceptual embedding, showing axes and carvings forming distinct clusters"
              width={2000}
              height={1600}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-6">
            <Image
              src="/figures/harmonics_complexity.png"
              alt="Violin plot: elliptical Fourier harmonics required for 99% shape reconstruction, comparing axes (n=41), carvings (n=72), and mushrooms (n=22)"
              width={2000}
              height={1000}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-8">
            <Image
              src="/figures/three_way_scatter.png"
              alt="Scatter of Aspect Ratio vs Roundness for axes, mushrooms, and carvings"
              width={1500}
              height={1200}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 4. Stone 53 carvings occupy the low-aspect-ratio, high-roundness
              region of shape space alongside <em>A. muscaria</em>, not the elongated
              region occupied by British EBA axes.
            </figcaption>
          </figure>

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
          <figure className="my-8">
            <Image
              src="/figures/real_extremes_clean.png"
              alt="Reference axe (Needham 1983) and reference A. muscaria mushroom silhouettes shown next to the 6 most-axe-like and 6 most-mushroom-like carvings from the classifier ranking"
              width={3000}
              height={1000}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-6">
            <Image
              src="/figures/atlas_clean_carvings.png"
              alt="Grid of all 42 Stonehenge carving silhouettes sorted by Random Forest posterior probability of mushroom"
              width={2200}
              height={1900}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 7. All 42 Stonehenge carvings across Stones 53, 4, and 5
              sorted top-left to bottom-right by classifier P(mushroom). Every
              carving has a cap-plus-stem morphology; the classifier separates
              them on aspect ratio (wide-cap-short-stem vs. narrower-cap-longer-stem),
              but this is a distinction between mushroom sub-morphologies,
              not between mushroom and axe.
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
          <figure className="my-6">
            <Image
              src="/figures/size_comparison.png"
              alt="Overlaid histograms of physical size: 292 bronze axes, 41 carvings, 12 mushroom species, all in centimeters"
              width={2000}
              height={1100}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 8. Physical size of 292 bronze axes (Bevan Corpus,
              length in cm), 41 Stone 53 carvings (height in cm), and 12
              native British psilocybin mushroom species (total cap+stem
              length in cm). Size does not decisively separate the classes.
              The strong evidence for the mushroom identification comes from
              shape, not from size.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.10 The geographic distribution of contemporary axes
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

        <section aria-labelledby="discussion" className="mb-16">
          <h2 id="discussion" className="text-2xl font-bold mb-4">4. Discussion</h2>

          <h3 className="text-lg font-semibold mt-6 mb-2">4.1 The spatial layout is fungal too</h3>
          <p>
            Rendering the 41 Stone 53 carvings in their actual positions on the
            stone, coloured by discovery epoch, produces a picture that reads
            unmistakably as a scatter of mushrooms across a plain.
          </p>
          <figure className="my-6">
            <Image
              src="/paper_figures/image1.png"
              alt="All 41 Stone 53 carvings arranged in their spatial position on the NW face of the trilithon, coloured by discovery epoch (pre-2003, 2003, 2012)"
              width={2200}
              height={1100}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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
          <figure className="my-6">
            <Image
              src="/paper_figures/image8.png"
              alt="Distribution maps of four psilocybin-containing mushroom species native to England: Psilocybe semilanceata, Psilocybe coronilla, Psilocybe subviscida, and Panaeolus cinctulus, with the location of Stonehenge marked"
              width={2200}
              height={800}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
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

          <h3 className="text-lg font-semibold mt-8 mb-2">4.3 Interpretation</h3>
          <p>
            The convergent quantitative evidence &mdash; recurve rate, aspect
            ratio, multivariate cluster distance, and three-way classifier
            verdict &mdash; is not consistent with the Stone 53 carvings being
            straightforward representations of British Early Bronze Age
            axeheads. It is consistent with them being fungal.
          </p>
          <p>
            Two other clues point in the same direction. First, the Needham
            &ldquo;recurve&rdquo; feature that is rare (7%) among real axes and common
            (37%) among the carvings has a straightforward mycological reading: the outer
            margin of an <em>A. muscaria</em> cap curls under (incurves) as it matures.
            Second, the annulus or ring that appears on many of the carvings, and which
            has no functional analogue on a bronze axehead, is exactly the ring around
            the stem of a mature <em>Amanita</em>.
          </p>
          <p>
            <span className="font-semibold">Limitations.</span> The mushroom corpus was
            built by automated color-based segmentation of side-view iNaturalist photos.
            The convex-hull filling needed to bridge the white cap spots artificially
            inflates the Solidity feature, so Solidity is excluded from the classifier;
            this is documented in the analysis code and should be revisited with a
            SAM-based re-segmentation before archival publication. The reference set is
            restricted to <em>A. muscaria</em> and British EBA axes; a properly powered
            future paper needs additional candidate reference classes (halberds, sickles,
            palstaves, sun/moon rock-art motifs, cup-and-ring vulva motifs, generic
            silhouettes). The Stone 53 shape features come from a single ImageJ pass
            (Lomas 2021) and have not yet been independently re-extracted from the raw
            English Heritage laser-scan TIFFs. The multivariate analysis effectively has
            only two independent shape dimensions because the four dimensionless features
            are highly collinear.
          </p>
          <p>
            <span className="font-semibold">Interpretive implications.</span> If some
            fraction of the Stone 53 carvings depict <em>A. muscaria</em>, the natural
            reading is that Stonehenge&rsquo;s late Bronze-Age use-phase involved
            ritualized ingestion of a well-known psychoactive fungus. Evidence for
            entheogen use at Neolithic and Bronze Age sacred sites in Europe has been
            argued for on independent grounds (see Samorini 1992 on Val Camonica; recent
            residue analyses at Menorcan and Iberian burials); the Stonehenge carvings
            would fit this broader pattern rather than establishing it. A parallel line
            of inquiry &mdash; palynological work on the Stonehenge landscape for{" "}
            <em>A. muscaria</em> host trees (birch, pine, spruce) c. 1650&ndash;1400 BC
            &mdash; would substantially strengthen or weaken this reading.
          </p>
        </section>

        <section aria-labelledby="future-work" className="mb-16">
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
            5. Data and code availability
          </h2>
          <p>
            All analysis code, data (as CSV / JSON / GeoJSON), and preregistration draft
            are available at the project repository. The muscaria corpus, source
            iNaturalist observation IDs, and reproducibility notes are included.
          </p>
          <ul className="list-none space-y-2 text-base my-6">
            <li>
              <a href="/data/three_way_predictions.csv" className="text-red-800 underline">
                three_way_predictions.csv
              </a>{" "}
              &mdash; per-carving classifier output
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
          </ul>
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
