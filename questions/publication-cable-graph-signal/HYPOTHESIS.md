# What graph attributes signal that a cable is one a historian would cite?

**Status:** answered
**Thread of:** —

## Question

`data/external/reftel-with-tags-and-attr.2026-08-01.giant.graphml` carries a
rich set of precomputed structural attributes on the giant component of the
reference graph — degree, closeness, betweenness, pagerank, coreness,
strength, `cd-index`/`cd-index-type`, `antichain`, three community
labelings, and edge `trussness` — none of it produced by code in this repo.
Separately, `data/source/<publication>/` holds seven historians' hand-built
cable-citation catalogs, each an independent, human-curated selection of
specific cables out of the ~310K-node corpus.

Does any of that precomputed graph structure distinguish a publication's
cited cables from the background corpus? And beyond a single scalar
attribute, could a graph-topological *method* — given a partial known set of
a publication's citations — recover the rest of that publication's cited
cables?

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

Generic centrality (degree/betweenness/pagerank/coreness/strength) and
community membership are tested too, as a baseline against which the above
two are compared.

## Data used

- External: `data/external/reftel-with-tags-and-attr.2026-08-01.giant.graphml`
  (738 MB, 309,512 nodes / 299,757 edges — giant weakly-connected component
  only; see `data/external/README.md` — note this specific enriched file
  isn't documented there, it's an external asset supplied directly).
- Source: `data/source/<publication>/*.md` (seven publications:
  `harmer2013`, `hulme2026`, `lee2018`, `morley2019`, `simpson2005`,
  `szalontai2023`, `weimer2019`) — hand-resolved citation-to-MRN catalogs,
  each with a confidence signal per row (confirmed / flagged-but-matched /
  ambiguous / excluded).
- Code: `code/build_node_table.py`, `code/attribute_signal.py`,
  `code/seed_expansion_retrieval.py` — all question-exclusive.
  `code/station_data.py` is a hand-copied data snapshot of acp-127's
  `src/station_data.py` `STATIONS` table (see AGENTS.md's "External data
  dependency": data snapshot, not a runtime code dependency), used to
  reproduce acp-127's own MRN canonicalization when matching ground truth
  to graph node labels.
- Derived (question-exclusive): `results/ground_truth_cables.csv`, hand
  transcribed from the source `.md` files (not parsed by a script — the
  seven files are inconsistently formatted enough that hand transcription of
  ~100-300 rows was more reliable than throwaway parsing logic).

## Method summary

1. Hand-transcribe every `confirmed`/`flagged` MRN per publication (tiered
   by the source file's own confidence markers) into
   `results/ground_truth_cables.csv`; exclude ambiguous-candidate and
   not-in-corpus rows entirely.
2. `build_node_table.py` loads the graphml once via `igraph` (this repo's
   established convention), flattens all node attributes plus a derived
   per-node `trussness` aggregate (edge-only in the source data) into a
   cached CSV, and matches ground-truth MRNs to node labels by reproducing
   acp-127's own `src/reftel_normalize.py::_normalize_doc_number()`
   canonicalization (station-code lookup via a copy of acp-127's
   `station_data.py`, then leading-zero-stripped number formatting) rather
   than a heuristic — this graphml's labels turn out to already be in that
   canonical form. Reports the ground-truth match rate against the giant
   component.
3. `attribute_signal.py` (Method A): per publication and pooled, Mann-Whitney
   U / rank-biserial effect size for each numeric attribute against a
   same-year background sample (plus full-corpus as a secondary check),
   hypergeometric enrichment for community/antichain bucket concentration,
   BH-FDR correction across tests. `cd-index`/`antichain` get a dedicated
   subsection (skew toward extreme cd-index / disruptive type; enrichment
   in non-dominant antichains) rather than being folded into the generic
   ranking.
4. `seed_expansion_retrieval.py` (Method B): leave-one-out personalized
   PageRank seeded on a publication's other confirmed cables, tested against
   global-pagerank and random baselines (median rank, MRR, recall@k) — does
   network proximity to *other known-cited cables* recover held-out
   citations better than any static attribute threshold?

## Result

See [`results/FINDINGS.md`](results/FINDINGS.md) for the full write-up.
Headline: only 45 of 191 tiered ground-truth cables (39 of 167 `confirmed`)
exist in this giant-component graphml at all — a bigger constraint than any
attribute choice. Of the attributes tested, `cd-index-type: disruptive`
enrichment is the one signal that's both statistically robust and
replicates across the pooled analysis, not just within one publication.
`morley2019`-specific cited cables also show significantly *lower*
betweenness (survives FDR correction on its own) and directionally lower
degree/pagerank/strength than background (not "historians cite hubs"), but
this doesn't replicate in `weimer2019`/`szalontai2023`. The `antichain`
depletion lead from this question's hypothesis did not survive correction
(best q≈0.25) and should be read as unconfirmed, not a finding.
Personalized-PageRank seed-expansion (Method B) beats a static
global-pagerank baseline on MRR/recall@50 for both publications with enough
seeds, without being a reliable retrieval tool outright (median rank still
in the tens-to-hundreds of thousands out of 309,512).

## Caveats / limitations

- **Major, empirically confirmed coverage gap**: this graphml's node labels
  use a different MRN convention than the ground truth (~96% of nodes are
  `<2-digit year><FULL station name><unpadded number>`, e.g.
  `73SANTIAGO4687`, vs. the ground truth's `<4-digit year><6-char truncated
  station><zero-padded number>`, e.g. `1973SANTIA04687`). The former is
  exactly acp-127's own canonical `document_number` form, so matching
  reproduces `src/reftel_normalize.py::_normalize_doc_number()` — a copy of
  acp-127's `station_data.py` station-variant table (`code/station_data.py`;
  191/191 ground-truth station codes resolve through it), plus the same
  leading-zero-stripping. Even joined correctly, only **45 of 191**
  hand-tiered ground-truth cables (39 of 167 `confirmed`) actually exist as
  nodes in this giant component — spot-checks (e.g. no `74BONN2540` node
  despite 661 other 1974 BONN nodes existing) confirm this is real
  sparsity/coverage, not a residual join bug: the giant component is a
  small, well-connected subset of a much larger and much sparser full
  corpus (309,512 nodes / 299,757 edges — average degree well under 1), and
  cables historians cite precisely for their singular content are
  apparently often *not* the ones with reference-graph connections. This
  asymmetry is itself a first-class finding, not just a caveat, and is
  reported prominently in `results/FINDINGS.md`.
- **Practical consequence for sample sizes**: only `morley2019` (20 matched,
  confirmed+flagged) and `weimer2019` (15 matched) have enough matched
  cables for publication-level statistics; `szalontai2023` (4) is marginal;
  `harmer2013`, `hulme2026`, `lee2018`, `simpson2005` (0-2 matched each) are
  usable only in the pooled-across-publications analysis (n=45 total), not
  individually. Method B (seed-expansion retrieval) only runs for
  publications clearing a minimum matched-N threshold.
- Topic/date/station confounds are real: a publication about one country in
  one period will trivially score high on anything correlated with that
  station's traffic volume in that window, independent of any "historians
  prefer structurally important cables" effect. Same-year background
  sampling only partially controls for this.
- Ground truth itself has label noise the source files already flag (date
  offsets, topical-fit-only matches, OCR-reconstructed MRNs) — the
  `confirmed`/`flagged` tier split is meant to bound this, not eliminate it.

## Related questions

- [`reference-graph-structure`](../reference-graph-structure/HYPOTHESIS.md) —
  shares the same reference graph, but is about the graph's own structure
  (components, hubs, communities) rather than whether that structure
  predicts an external, human-curated cable selection.
- [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md) —
  same shape of question ("do X and Y share a graph-native property"),
  applied to TAGS codes instead of publication citations.
