# What graph attributes signal that a cable is one a historian would cite?

**Status:** answered
**Thread of:** —

## Question

An externally-enriched graphml carries a rich set of precomputed structural
attributes on the corpus's reference graph — degree, closeness, betweenness,
pagerank, coreness, `cd-index`/`cd-index-type`, `antichain` (giant-component
build only), community membership, and edge `trussness`/`edge-betweenness`
— none of it produced by code in this repo. Separately, `data/source/<publication>/`
holds seven historians' hand-built cable-citation catalogs, each an
independent, human-curated selection of specific cables out of the corpus.

Does any of that precomputed graph structure distinguish a publication's
cited cables from the background corpus?

## Hypothesis

Exploratory — no attribute is staked out in advance as the answer. Two
candidate mechanisms seem most plausible going in and get first-class
treatment rather than being buried in a generic sweep:

- **`cd-index`** is temporal (built from how later traffic treats a cable
  relative to its own predecessors), not structural — a cable a historian
  cites as a turning point could be low-degree but highly disruptive.
- **`antichain`** separates cables on the single dominant "mainstream"
  broadcast layer from cables on minor, structurally parallel chains — a
  historian tracing one narrow thread may cite disproportionately from
  off-mainstream chains rather than the most heavily populated one.

Generic centrality (degree/betweenness/pagerank/coreness, plus whatever else
a given graph build's schema happens to carry — see Method summary) and
community membership are tested too, as a baseline against which the above
two are compared.

## Data used

- External: enriched graphml builds, both a giant-weakly-connected-component
  variant and its non-giant (full) sibling — filenames only, not full
  filesystem paths, documented here since the files live outside this repo
  and their location/schema has already changed across three builds during
  this question's lifetime (see "Which graph build" in `results/FINDINGS.md`).
  Only the giant-component variant carries `antichain`; the non-giant
  variant covers far more of the corpus (see Result). Passed as a required
  argument to `code/build_node_table.py` — no default path.
- Source: `data/source/<publication>/*.md` (seven publications:
  `harmer2013`, `hulme2026`, `lee2018`, `morley2019`, `simpson2005`,
  `szalontai2023`, `weimer2019`) — hand-resolved citation-to-MRN catalogs,
  each with a confidence signal per row (confirmed / flagged-but-matched /
  ambiguous / excluded).
- Code: `code/build_node_table.py`, `code/attribute_signal.py` —
  question-exclusive. `code/station_data.py` is a hand-copied data snapshot
  of acp-127's `src/station_data.py` `STATIONS` table (see AGENTS.md's
  "External data dependency": data snapshot, not a runtime code
  dependency), used to reproduce acp-127's own MRN canonicalization when
  matching ground truth to graph node labels.
- Derived (question-exclusive): `results/ground_truth_cables.csv`, hand
  transcribed from the source `.md` files (not parsed by a script — the
  seven files are inconsistently formatted enough that hand transcription of
  ~100-300 rows was more reliable than throwaway parsing logic).

## Method summary

1. Hand-transcribe every `confirmed`/`flagged` MRN per publication (tiered
   by the source file's own confidence markers) into
   `results/ground_truth_cables.csv`; exclude ambiguous-candidate and
   not-in-corpus rows entirely.
2. `build_node_table.py` (graphml path required, no default) loads the
   graphml via `igraph`, **discovers** node/edge attributes from whatever
   file is passed rather than a hardcoded list (excluding only structural
   columns: `label`/`id`/`message_preview`/`TAGS`/`date`), aggregates every
   edge-only attribute (e.g. `trussness`, `edge-betweenness`) onto nodes as
   max/mean, and matches ground-truth MRNs to node labels by reproducing
   acp-127's own `src/reftel_normalize.py::_normalize_doc_number()`
   canonicalization (station-code lookup via a copy of acp-127's
   `station_data.py`, then leading-zero-stripped number formatting) rather
   than a heuristic. Reports the ground-truth match rate. Attribute
   auto-discovery matters in practice: this graph's enrichment schema has
   already changed across builds (attributes added and removed), and
   hardcoded attribute lists needed hand-editing every time until this was
   made generic; it also means the same script runs unmodified against the
   non-giant build even though that one lacks `antichain` entirely.
3. `attribute_signal.py`: per publication and pooled, Mann-Whitney U /
   rank-biserial effect size for every numeric-dtype column in
   `node_features.csv` against a same-year background sample (plus
   full-corpus as a secondary check), hypergeometric enrichment for every
   string-dtype column (currently just `cd-index-type`) — both sets
   auto-detected from the CSV's dtypes, not a hardcoded attribute list.
   `cd-index`/`antichain` additionally get a dedicated subsection (skew
   toward extreme cd-index; enrichment in the dominant antichain layer)
   beyond the generic sweep, since those two tests are conceptually
   specific to those attributes; both degrade gracefully (empty output, no
   error) when the loaded graph lacks the attribute. BH-FDR correction is
   applied **separately per test family** (numeric / categorical / cd-index
   / antichain) — an earlier pass of this analysis pooled `community-leiden`
   into the same categorical family as `cd-index-type`, and
   `community-leiden`'s many tautologically-significant tiny-community
   matches were inflating `cd-index-type`'s apparent significance by
   sharing that correction; keeping families separate (and routing
   `community-leiden` to the numeric sweep, where it's an ID column with no
   real signal) fixed that.
4. Both steps are run twice — once against a giant-component-only build
   (has `antichain`, much lower ground-truth coverage) and once against
   the full non-giant build (no `antichain`, far higher coverage) — to see
   whether findings hold up once statistical power isn't as constrained by
   the giant-component coverage gap. See Result.

## Result

See [`results/FINDINGS.md`](results/FINDINGS.md) for the full write-up.
Headline: ground-truth coverage is the dominant constraint, and it differs
drastically between the two builds — only 52 of 191 tiered ground-truth
cables (46 of 167 `confirmed`) exist in the giant-component build, vs. 151
of 191 (130 of 167 `confirmed`) in the non-giant build. With that much more
statistical power, the non-giant run gives a substantially more confident
answer: **`degree`, `betweenness`, `pagerank`, and `coreness` are all
significantly *lower* for cited cables than background** (not "historians
cite hubs") across the pooled analysis and individually within
`morley2019` and `weimer2019`, and **`cd-index-type: disruptive`
enrichment is genuinely significant** (not just directionally suggestive)
in the pooled analysis and in `morley2019`/`szalontai2023` individually.
The giant-component run's weaker, noisier version of these same findings
was mostly an artifact of being underpowered at n≈46-52, not a different
underlying effect. `antichain` (giant-only, since non-giant lacks it)
still shows no stable signal.

## Caveats / limitations

- **Major, empirically confirmed coverage gap between graph builds**: both
  graphml builds' node labels use a different MRN convention than the
  ground truth (the large majority of nodes are `<2-digit year><FULL
  station name><unpadded number>`, e.g. `73SANTIAGO4687`, vs. the ground
  truth's `<4-digit year><6-char truncated station><zero-padded number>`,
  e.g. `1973SANTIA04687`). The former is exactly acp-127's own canonical
  `document_number` form, so matching reproduces
  `src/reftel_normalize.py::_normalize_doc_number()` — a copy of acp-127's
  `station_data.py` station-variant table (`code/station_data.py`;
  191/191 ground-truth station codes resolve through it), plus the same
  leading-zero-stripping. Even joined correctly, the **giant-component**
  build only contains 52/191 (46/167 confirmed) ground-truth cables — the
  **non-giant** build contains 151/191 (130/167 confirmed). Spot-checks in
  earlier passes (e.g. no `74BONN2540` node in the giant build despite 661
  other 1974 BONN nodes existing there) confirmed the giant-component gap
  is real sparsity/coverage, not a join bug: cables historians cite
  precisely for their singular content are apparently often exactly the
  cables with no REF-line connections to anything else, so they never
  survive a giant-weakly-connected-component filter.
- **Practical consequence for sample sizes**: in the giant-component build,
  only `morley2019` and `weimer2019` have enough matched cables for
  individual-publication statistics, and even pooled n is only 52. In the
  non-giant build, `harmer2013` also reaches full coverage (4/4) and every
  publication except `lee2018`/`hulme2026` has a reasonably large matched
  set — see `results/FINDINGS.md` for the full breakdown.
- Topic/date/station confounds are only partially controlled (same-year
  background); full-corpus background gives near-identical results in
  every configuration tested — in the pooled/large-n groups this is partly
  because the ground truth spans nearly the graph's entire year range, so
  "same-year" background converges to "full corpus" background by
  construction, not because the confound was actually ruled out.
- Ground truth itself has label noise the source files already flag (date
  offsets, topical-fit-only matches, OCR-reconstructed MRNs) — the
  `confirmed`/`flagged` tier split is meant to bound this, not eliminate it.
- Results are sensitive to which graph build is used, but in the direction
  of "the non-giant build recovers stronger, more general versions of the
  giant build's own findings," not different findings — see
  `results/FINDINGS.md`'s "Which graph build" section for specifics.

## Related questions

- [`reference-graph-structure`](../reference-graph-structure/HYPOTHESIS.md) —
  shares the same reference graph, but is about the graph's own structure
  (components, hubs, communities) rather than whether that structure
  predicts an external, human-curated cable selection.
- [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md) —
  same shape of question ("do X and Y share a graph-native property"),
  applied to TAGS codes instead of publication citations.
