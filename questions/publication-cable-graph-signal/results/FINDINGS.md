# Findings: what graph attributes signal a historian's cited cables?

**Status:** answered (exploratory — small-N caveats throughout)

## Headline result

Two signals survive multiple-testing correction and are worth taking
seriously; almost everything else tested (including the community-membership
tests) either doesn't reach significance or turns out to be a methodological
artifact on inspection:

1. **`cd-index-type == "disruptive"` is enriched among cited cables**, and
   this holds both within `morley2019` alone and in the cross-publication
   pooled analysis — the one result in this investigation that's both
   statistically robust *and* consistent across more than one publication.
2. **For `morley2019` specifically, cited cables have *lower* betweenness,
   degree, pagerank, and strength than a same-year background sample** —
   the opposite of the naive "historians cite hub cables" hypothesis.
   `weimer2019` and `szalontai2023` show no comparable centrality signal,
   so this doesn't generalize cleanly across publications.

Before either of those: **most hand-verified citations aren't even in this
graphml.** Only 45 of 191 tiered ground-truth cables (39 of 167
`confirmed`) exist as nodes in the giant component at all. That's the
biggest, most surprising finding of this investigation and shapes how much
weight the rest of the results can bear.

## 1. Coverage gap: most cited cables aren't in this graph

`data/external/reftel-with-tags-and-attr.2026-08-01.giant.graphml` uses a
different MRN convention than `data/source/*/*.md`'s ground truth — ~96% of
its 309,512 nodes are `<2-digit year><FULL station name><unpadded number>`
(e.g. `73SANTIAGO4687`), not the `<4-digit year><6-char truncated
station><zero-padded number>` form the ground truth uses (e.g.
`1973SANTIA04687`). The former turns out to be exactly the canonical form
acp-127's own `src/reftel_normalize.py::_normalize_doc_number()` produces
(2-digit year + canonical station name + `_clean_number()`'s
leading-zero-stripped number) — so `code/build_node_table.py`'s
`match_mrn_to_label()` reproduces that normalization directly: it looks the
ground truth's (possibly truncated/OCR-variant) station code up in the same
`STATIONS` variant table acp-127 uses (copied verbatim into
`code/station_data.py` from `../../../acp-127/src/station_data.py`, per
AGENTS.md's "data snapshot, not a code dependency" convention), strips
leading zeros the same way `_clean_number()` does, and formats the
candidate label exactly as `_format_canonical()` would. All 191 ground-truth
station codes resolve through this table with no unknowns. Even so:

| tier | matched | total |
|---|---|---|
| confirmed | 39 | 167 |
| flagged | 6 | 24 |
| **overall** | **45** | **191** |

| publication | matched (confirmed) | total (confirmed) |
|---|---|---|
| harmer2013 | 1 | 4 |
| hulme2026 | 1 | 9 |
| lee2018 | 0 | 2 |
| morley2019 | 16 | 76 |
| simpson2005 | 2 | 22 |
| szalontai2023 | 4 | 15 |
| weimer2019 | 15 | 39 |

Spot-checks rule out a residual join bug: e.g. no `74BONN2540` node exists
despite 661 other 1974-BONN nodes being present in the giant component
nearby (`74BONN2533`, `74BONN2593`, ...). The giant component here is a
small (309,512-node), very sparse (299,757-edge, mean degree < 1) connected
subset — almost certainly of a much larger full corpus — and cables a
historian cites specifically for their singular content are, it turns out,
often exactly the cables with *no* REF-line connections to anything else,
so they never make it into a giant-component export at all. That asymmetry
is itself informative: a "find cables a historian would cite" tool built
purely on this graph's connectivity would silently miss ~76% of the actual
target population before any attribute even gets a chance to help.

**Practical consequence:** only `morley2019` (20 matched, confirmed+flagged)
and `weimer2019` (15 matched) have enough matched cables for
publication-level statistics. `szalontai2023` (4) is marginal.
`harmer2013`, `hulme2026`, `lee2018`, `simpson2005` (0-2 matched each) only
contribute to the pooled analysis.

## 2. Method A — per-attribute signal ranking

Mann-Whitney U / rank-biserial effect size, `confirmed`-tier cables vs. a
same-year background sample (full-corpus background gave near-identical
results throughout — the date confound doesn't appear to be doing much
work here, probably because the matched set is already so small).
Benjamini-Hochberg FDR applied across the full numeric-test family.

### Generic centrality sweep

| group | attribute | effect size | p | q | n |
|---|---|---|---|---|---|
| morley2019 | betweenness | **-0.352** | 0.0026 | **0.048** | 16 |
| morley2019 | degree | -0.381 | 0.0065 | 0.069 | 16 |
| morley2019 | strength | -0.381 | 0.0065 | 0.069 | 16 |
| morley2019 | pagerank | -0.326 | 0.0148 | 0.121 | 16 |
| ALL_POOLED | betweenness | -0.176 | 0.019 | 0.139 | 39 |
| weimer2019 | (all attrs) | \|effect\| < 0.12 | n.s. | n.s. | 15 |
| szalontai2023 | (all attrs) | \|effect\| < 0.38 | n.s. | n.s. | 4 |

Negative effect size = cited cables score *lower* than background. For
`morley2019`, cited cables are consistently *less* structurally central —
lower betweenness (the only attribute surviving FDR correction on its
own), degree, strength, pagerank — than a random same-year cable. This is
the opposite of "historians cite the hub cables"; it reads more like
"historians cite substantive, often narrowly-addressed analytical cables
(POPPER's 14-paragraph human-rights assessments, verbatim-quote cables)
that aren't necessarily the busiest nodes in the reference network."
`weimer2019` and `szalontai2023` show no comparable effect (all
\|effect size\| < 0.4, none significant) — this is not a general property
of "cables historians cite," at least not one this analysis can detect at
n=15-16 and n=4.

`closeness` was untestable everywhere — the attribute key exists in the
graphml schema but is populated for **0 of 309,512 nodes** in this
particular file.

### cd-index and antichain (dedicated tests)

**cd-index-type enrichment** — the strongest, most cross-publication-robust
result in this investigation:

| group | tier | observed disruptive | expected | p | q |
|---|---|---|---|---|---|
| ALL_POOLED | confirmed+flagged | 25/32 | 17.58 | 0.0057 | **0.0074** |
| morley2019 | confirmed+flagged | 15/18 | 9.89 | 0.0118 | **0.0150** |
| ALL_POOLED | confirmed | 20/27 | 14.83 | 0.033 | 0.040 |
| morley2019 | confirmed | 12/15 | 8.24 | 0.042 | 0.050 |
| szalontai2023 | confirmed | 3/3 | 1.65 | 0.166 | 0.180 |
| weimer2019 | confirmed | 4/7 | 3.85 | 0.607 | 0.607 |

Cited cables skew toward `cd-index-type: disruptive` (successors treat the
cable as superseding/routing around it, rather than building on it
alongside its own predecessors) rather than `consolidating`. This holds up
in the pooled analysis even though it's morley2019-driven, and directionally
recurs in szalontai2023 despite n=3 being far too small to reach
significance on its own. **cd-index *extremeness* (`|cd-index|` vs.
background `|cd-index|`) showed no signal anywhere** — it's specifically
the categorical disruptive/consolidating split that carries signal, not the
magnitude of the continuous score.

**antichain** — the depletion lead reported in an earlier pass of this
analysis (before the MRN-matching fix) does not hold up after correction:
`morley2019` cited cables are numerically depleted in the single
most-populated ("mainstream") antichain layer at every tier/background
combination (e.g. confirmed/same_year: 5 observed vs. 8.58 expected,
p=0.061), but the best q-value is 0.254 — well short of significance, and
other publications don't move in the same direction (`weimer2019`,
`ALL_POOLED_excl_morley2019` show mild *enrichment* instead). Treat this as
a plausible but explicitly unconfirmed lead, not a finding.

### Community membership (leiden / walktrap / infomap)

Nominally "significant" (q → 0 for several morley2019/weimer2019 buckets),
but this turns out to be a **methodological artifact worth flagging, not a
real finding**: this reference graph decomposes into 78,215-84,643
communities across 309,512 nodes, with a *median community size of 1*. When
2-3 of a publication's cited cables happen to directly reference each other
(the same historical episode's cable-and-reply pair), they trivially land
in the same tiny community — that's close to definitional for a
reference-graph community detector, not evidence that "community
membership predicts citation" in any generalizable sense. Reported for
completeness in `results/attribute_signal_categorical.csv`, not treated as
a finding.

## 3. Method B — seed-expansion retrieval test

Leave-one-out personalized PageRank, seeded on a publication's other
`confirmed` matched cables, vs. that cable's own global-pagerank rank and a
random-rank baseline. Only `morley2019` (16 seeds) and `weimer2019` (15
seeds) cleared the n≥10 threshold to run this.

| publication | method | median rank (of 309,512) | MRR | recall@50 |
|---|---|---|---|---|
| morley2019 | personalized PageRank | 90,514 | **0.0071** | **0.19** |
| morley2019 | global pagerank | 80,615 | 0.00002 | 0.00 |
| morley2019 | random | 154,757 | 0.00004 | 0.0002 |
| weimer2019 | personalized PageRank | 205,384 | **0.0057** | **0.13** |
| weimer2019 | global pagerank | 237,114 | 0.00001 | 0.00 |
| weimer2019 | random | 154,757 | 0.00004 | 0.0002 |

Personalized PageRank clearly beats both baselines on MRR and recall@50 for
both publications — network proximity to a publication's *other* known
cables is doing real work that a static global-importance score (pagerank)
doesn't capture at all (global pagerank's recall@50 is exactly 0 in both
cases). But it's a partial win, not a retrieval tool: median rank is still
in the tens-to-hundreds of thousands out of 309,512, and for `morley2019`
the *median* rank under personalized PageRank (90,514) is actually slightly
worse than its own global-pagerank median (80,615) even though personalized
PageRank's MRR/recall are far better — a handful of held-out cables rank
very well under personalization (pulling MRR/recall@50 up) while the bulk
rank no better than a generically-important cable would. `weimer2019` shows
the same pattern more starkly (personalized-PageRank median rank worse than
even the random baseline): its cables span many different, only loosely
cross-referencing stations (Kabul, Geneva, Bonn, Kathmandu, Ottawa), which
plausibly limits how much graph proximity between them personalized
PageRank can exploit.

## Answer to the original question

**Is there a graph-native signal for "cables a historian would cite"?**
Weakly and inconsistently, yes — `cd-index-type: disruptive` is the one
attribute with a real, cross-publication-replicated effect; personalized
PageRank seeded on a partial known set beats a static importance score at
finding the rest. But the dominant finding is that **most of the ground
truth isn't reachable through this graph at all** (giant-component
coverage, not attribute choice, is the binding constraint), and the
generic-centrality effect that does appear is largely specific to
`morley2019` and doesn't replicate in the other publications with enough
matched cables to check (`weimer2019`, `szalontai2023`). The antichain lead
from an earlier pass of this analysis did not survive a corrected MRN join
and should not be cited as a finding.

## Caveats / limitations

- Sample sizes are small even before the coverage gap: `morley2019` (76
  confirmed) and `weimer2019` (39 confirmed) supply nearly all statistical
  power; the other five publications combined contribute 52 confirmed rows
  across the whole project, and only 45 matched cables total survive the
  giant-component join. Every reported effect should be read as "detectable
  at n≈15-40," not as a general property of historian citation behavior.
- Topic/date/station confounds were only partially controlled (same-year
  background); full-corpus background gave near-identical results, which
  is weak evidence the confound isn't dominant here, not proof.
- Ground-truth label noise: `flagged`-tier rows (date offsets, topical-fit-
  only matches) are reported separately from `confirmed` throughout: see
  `results/ground_truth_cables.csv`'s `tier` column and
  `results/attribute_signal_*.csv`'s `tier_scope` column.
- `closeness` is present in the graphml's attribute schema but populated
  for zero nodes — dropped from every test automatically (n=0), not a bug.
- Community-membership "signal" is a known artifact (see above) — don't
  reuse `attribute_signal_categorical.csv`'s community rows as evidence
  without re-deriving a less tautological test (e.g. concentration relative
  to community-size-matched random draws, not a fixed observed-mode
  bucket).
- MRN matching follows acp-127's actual normalization function
  (`code/station_data.py` + `match_mrn_to_label()` in
  `code/build_node_table.py`), not a heuristic reverse-engineered from the
  graph's own labels — this is a hand-copied data snapshot of
  `acp-127/src/station_data.py`'s `STATIONS` table (191/191 ground-truth
  station codes resolve through it), and should be re-synced if acp-127's
  station list changes materially.

## Reproducing

```
python3 questions/publication-cable-graph-signal/code/build_node_table.py
python3 questions/publication-cable-graph-signal/code/attribute_signal.py
python3 questions/publication-cable-graph-signal/code/seed_expansion_retrieval.py
```

Outputs: `results/node_features.csv`, `results/ground_truth_matched.csv`,
`results/attribute_signal_{numeric,categorical,cdindex,antichain}.csv`,
`results/seed_expansion_{details,summary}.csv`.
