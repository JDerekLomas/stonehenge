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
            A quantitative shape analysis of the 115 prehistoric carvings on Stonehenge
            finds they systematically match the silhouette of{" "}
            <em>Amanita muscaria</em> mushrooms, not the British Early Bronze Age
            axeheads to which they have been attributed since 1953.
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
            <span className="font-semibold">Mushrooms.</span> 74 research-grade{" "}
            <em>A. muscaria</em> observations pulled from iNaturalist, sorted by community
            vote. Silhouettes automatically segmented from HSV color threshold on the
            red cap, with convex-hull filling to bridge the white cap spots. After
            automated quality filters, 55 silhouettes retained. This automated pipeline
            biases the <em>Solidity</em> feature toward artificially high values
            (mushroom mean 0.945 vs. axe 0.787); we therefore exclude Solidity from the
            classifier and note the caveat prominently below. A pre-registered SAM-based
            re-segmentation is planned for the archival version.
          </p>

          <MuscariaGrid />

          <p className="italic text-sm text-stone-700 mt-4">
            <strong>Note on imagery.</strong> The original English Heritage
            laser-scan silhouettes for the 41 Stone 53 carvings, and the
            photographic silhouettes for the 124 axes in the Bevan corpus, live
            in Google Drive folders that were not accessible to the automated
            pipeline that generated this draft. The paper site will be updated
            with those images once the folders are indexed.
          </p>

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
            Excluding the biased Solidity feature and using only Circularity, Aspect
            Ratio, and Roundness (each contributing equally, feature importance ~ 0.33 in
            RF), we ask, per carving: which class centroid is nearer &mdash; axe or
            mushroom? <span className="font-semibold">40 of 41 (97.6%) Stone 53
            carvings are closer to the mushroom centroid than the axe centroid.</span>
          </p>
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
            An axe-vs-mushroom Linear Discriminant Analysis, cross-validated at 85.5%
            &plusmn; 4.7% accuracy on its own training data, classifies 30 of 41 (73.2%)
            carvings as mushroom with mean posterior probability 0.71; 24 of 41 (58.5%)
            with probability &gt; 0.8. A Random Forest classifier at 91.6% &plusmn; 3.9%
            CV accuracy classifies 31 of 41 (75.6%) as mushroom with mean posterior 0.76.
            Both classifiers reach the same qualitative conclusion.
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
            3.5 Which specific carvings look like which class?
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
              src="/figures/extremes_composite.png"
              alt="Composite figure: reference axe and reference mushroom schematics next to the six most-axe-like and six most-mushroom-like Stone 53 carvings, shown as shape-ellipse reconstructions"
              width={2800}
              height={1000}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 5. Top row: stylized bronze axehead reference; the six Stone
              53 carvings the Random Forest is most confident are axes. Bottom
              row: stylized <em>A. muscaria</em> mature form (with annulus);
              the six the RF is most confident are mushrooms. Each carving cell
              shows a shape-ellipse reconstruction (major/minor axis fixed to
              the carving&rsquo;s ImageJ measurements). R = the hand-coded
              recurve feature; &#9702; = the annulus/ring feature.
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
            3.6 Corpus-level shape atlas
          </h3>
          <p>
            To make the whole distribution visible at a glance, each shape is
            rendered as an ellipse whose axis ratio matches its ImageJ
            measurements. Sorted by aspect ratio, the Bevan axe corpus is
            dominated by elongated forms (median AR = 2.74), while the Stone 53
            carvings span the full range from near-circular (AR = 1.08) to
            elongated (AR = 5.37). Only 10 of 41 carvings (24%) have AR &gt; 2.0.
          </p>
          <figure className="my-6">
            <Image
              src="/figures/atlas_axes.png"
              alt="Grid of 124 shape-ellipse silhouettes representing every axe in the Bevan corpus"
              width={2000}
              height={900}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 6a. Every axe in the Bevan corpus (n = 124) as a
              shape-ellipse silhouette, sorted by aspect ratio. Almost all
              cluster in the elongated range.
            </figcaption>
          </figure>
          <figure className="my-6">
            <Image
              src="/figures/atlas_carvings.png"
              alt="Grid of 41 shape-ellipse silhouettes representing every Stone 53 carving"
              width={2000}
              height={600}
              className="rounded-md border border-stone-200 w-full h-auto"
            />
            <figcaption className="text-sm text-stone-600 mt-2 text-center">
              Figure 6b. Every Stone 53 carving (n = 41) as a shape-ellipse
              silhouette, sorted by aspect ratio. Only the top-row carvings
              overlap with the axe corpus range; the bottom row does not.
            </figcaption>
          </figure>

          <h3 className="text-lg font-semibold mt-8 mb-2">
            3.7 The geographic distribution of contemporary axes
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
          <p>
            The convergent quantitative evidence &mdash; recurve rate, aspect ratio,
            multivariate cluster distance, and three-way classifier verdict &mdash; is
            not consistent with the Stone 53 carvings being straightforward
            representations of British Early Bronze Age axeheads. It is consistent with
            them being <em>Amanita muscaria</em> mushrooms.
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
