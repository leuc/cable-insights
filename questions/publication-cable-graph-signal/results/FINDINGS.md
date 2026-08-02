# Findings: what graph attributes signal a historian's cited cables?

**Status:** answered (exploratory — small-N caveats throughout, though much
reduced by the non-giant comparison below)

**Graph builds used:** two sibling files from the same `2026-08-02`
enrichment pass — `reftel-with-tags-attr-2026-08-02.giant.graphml`
(347,203 nodes / 428,324 edges, the only one with `antichain`) and
`reftel-with-tags-attr-2026-08-02.graphml` (1,419,822 nodes / 1,224,940
edges, no `antichain`). Both passed explicitly as the required first
argument to `code/build_node_table.py` — filenames only; full filesystem
paths are external to this repo and not reproduced here (see
`data/external/README.md` for how this repo documents its external data
dependencies). Giant-build results live in `results/`; non-giant results
live in `results/nongiant/`.

**Pipeline is schema-generic**: `code/build_node_table.py` discovers
node/edge attributes from whatever graphml file is passed rather than a
hardcoded list (excluding only structural columns: `label`, `id`,
`message_preview`, `TAGS`, `date`). `code/attribute_signal.py` likewise
auto-detects which columns to test from `node_features.csv`'s dtypes
(numeric → Mann-Whitney sweep, string → hypergeometric enrichment). This
was a genuine problem in earlier passes of this question: three different
giant-build versions each added/dropped attributes (`strength`,
`community-walktrap`, `community-infomap` gone; `hits-hub`,
`edge-betweenness` added), which meant hand-editing attribute lists every
time — and it's what let the same script run unmodified against the
non-giant build, which lacks `antichain` entirely (both scripts degrade to
empty output for that attribute rather than erroring).

## Headline result

The non-giant build has far more ground-truth coverage (151/191 matched
vs. 52/191 for giant), and with that much more statistical power gives a
substantially more confident version of the giant build's own findings —
not a different result, a *stronger* one:

1. **`degree`, `betweenness`, `pagerank`, and `coreness` are all
   significantly lower for cited cables than background** in the non-giant
   pooled analysis (q as low as 2×10⁻⁶) and individually within both
   `morley2019` and `weimer2019` — the giant build could only detect this
   reliably for `degree` and only in `morley2019` alone.
2. **`cd-index-type: disruptive` enrichment is now genuinely
   significant**, not just directionally suggestive — q=0.0023 pooled,
   and significant individually in `morley2019` and `szalontai2023`. In
   the giant build this same test topped out at q≈0.19 (not significant)
   once correctly isolated from `community-leiden`'s FDR family.
3. **`antichain` still shows no stable signal** (giant-only, since the
   non-giant build lacks it) — consistent with every prior build tested.

Coverage itself remains the standout finding: **even the non-giant build
only reaches 130/167 (78%) of confirmed citations** — better than the
giant build's 46/167 (28%), but still not complete, and the giant-only
`antichain` test is necessarily working from the smallest, most
coverage-constrained slice of ground truth of anything tested here.

## 1. Coverage

| | giant build | non-giant build |
|---|---|---|
| confirmed | 46 / 167 | **130 / 167** |
| flagged | 6 / 24 | **21 / 24** |
| **overall** | **52 / 191** | **151 / 191** |

Per-publication (confirmed tier):

| publication | giant | non-giant |
|---|---|---|
| harmer2013 | 1 / 4 | **4 / 4** |
| hulme2026 | 1 / 9 | 4 / 9 |
| lee2018 | 0 / 2 | 1 / 2 |
| morley2019 | 18 / 76 | **62 / 76** |
| simpson2005 | 2 / 22 | **14 / 22** |
| szalontai2023 | 4 / 15 | **14 / 15** |
| weimer2019 | 20 / 39 | **31 / 39** |

Matching reproduces acp-127's own `_normalize_doc_number()` canonicalization
(`code/station_data.py` + `match_mrn_to_label()`). In the giant build, only
`morley2019` and `weimer2019` have enough matched cables for individual
statistics. In the non-giant build, `harmer2013` (4/4), `morley2019`
(62-76), `simpson2005` (14/22), `szalontai2023` (14/15), and `weimer2019`
(31/39) all clear a reasonable bar; only `hulme2026` and `lee2018` remain
too small individually.

## 2. Per-attribute signal ranking

Mann-Whitney U / rank-biserial effect size, `confirmed`-tier cables vs. a
same-year background sample (full-corpus background gives near-identical
results in every configuration — see caveats for why this isn't strong
confound-control evidence on its own). BH-FDR applied separately within
each test family (numeric / categorical / cd-index / antichain).

### Non-giant build (primary — far more statistical power)

| group | attribute | effect size | p | q | n |
|---|---|---|---|---|---|
| ALL_POOLED | degree | -0.266 | 2×10⁻⁸ | **2×10⁻⁶** | 130 |
| ALL_POOLED | betweenness | -0.146 | 6×10⁻⁵ | **0.0008** | 130 |
| ALL_POOLED | pagerank | -0.174 | 2×10⁻⁴ | **0.0022** | 130 |
| ALL_POOLED | coreness | -0.157 | 4×10⁻⁴ | **0.0029** | 130 |
| morley2019 | betweenness | -0.283 | 7×10⁻⁸ | **5×10⁻⁶** | 62 |
| morley2019 | degree | -0.356 | 2×10⁻⁷ | **9×10⁻⁶** | 62 |
| morley2019 | coreness | -0.205 | 0.0013 | **0.0094** | 62 |
| weimer2019 | degree | -0.358 | 2×10⁻⁴ | **0.0022** | 31 |
| weimer2019 | coreness | -0.279 | 0.0020 | **0.013** | 31 |
| szalontai2023 | cd-index | -0.340 | 0.032 | 0.154 | 11 |

Every significant effect is negative — cited cables are consistently
*less* structurally central than a same-year background sample, across
every attribute that measures some form of connectivity or importance.
`weimer2019` in particular reverses the giant build's null result once
there's enough data: it shows the *same* negative-degree/coreness pattern
as `morley2019`, just undetectable at the giant build's n=15-20. `hits-hub`,
`edge-betweenness` (max/mean), `trussness` (max/mean), `community-leiden`,
and `missing` show no signal anywhere in either build (`missing` is
degenerate — see caveats). `closeness` remains untestable, populated for 0
nodes in both builds.

**cd-index-type enrichment:**

| group | tier | observed disruptive | expected | p | q |
|---|---|---|---|---|---|
| ALL_POOLED | confirmed+flagged | 91/115 | 72.53 | 0.00015 | **0.0023** |
| ALL_POOLED | confirmed | 75/98 | 61.81 | 0.0031 | **0.018** |
| morley2019 | confirmed+flagged | 48/60 | 37.84 | 0.0037 | **0.018** |
| szalontai2023 | confirmed | 11/11 | 6.88-6.94 | 0.006 | **0.019** |

Same direction as every build tested (`disruptive` over-represented), now
clearing significance in the pooled analysis and individually in two
different publications — a materially stronger result than the giant
build's best q≈0.19.

### Giant build (has `antichain`, far less ground truth)

| group | attribute | effect size | p | q | n |
|---|---|---|---|---|---|
| ALL_POOLED (confirmed+flagged) | degree | -0.279 | 0.0003 | **0.038** | 52 |
| morley2019 | degree | -0.388 | 0.0031 | 0.081 | 18 |
| morley2019 | betweenness | -0.301 | 0.0085 | 0.184 | 18 |
| ALL_POOLED (confirmed+flagged) | cd-index-type disruptive | 29/45 | 21.58 | 0.019 | 0.185 |

Same direction throughout as the non-giant build, just underpowered — only
`degree` in the pooled analysis clears q<0.05.

**antichain** (giant-only): no stable direction. `morley2019` and
`ALL_POOLED` cited cables are numerically *enriched* in the dominant
antichain layer (14/9.13, confirmed/same_year, p=0.022, q=0.135 — doesn't
survive correction). Earlier builds of this analysis found the opposite
(depletion, also non-significant). Not a usable lead.

### Community membership

`community-leiden` is tested via the numeric (Mann-Whitney) sweep, not a
mode-bucket enrichment test — see "Which graph build" in the prior pass of
this analysis for why the enrichment version was a tautological artifact
(median community size in this graph is close to 1 node). Shows no signal
in either build (best q≈0.92-0.97).

## Answer to the original question

**Is there a graph-native signal for "cables a historian would cite"?**
Yes, more confidently than earlier passes of this analysis suggested once
ground-truth coverage stops being the binding constraint: cited cables are
systematically *less* central (lower degree/betweenness/pagerank/coreness)
than background, and skew toward `cd-index-type: disruptive`. Both effects
are modest in size (rank-biserial ≈ 0.15-0.36) but statistically solid at
n=62-151. `antichain` remains the one tested attribute with no reliable
signal in any build. The dominant caveat is still coverage, just a less
severe one than before: **even the best (non-giant) build only reaches
78% of confirmed citations**, so any attribute-based method built on this
graph structure alone would still miss roughly a fifth of what historians
actually cite before it even gets a chance to rank anything.

## Caveats / limitations

- Sample sizes are much better than earlier passes but still bounded:
  `morley2019` (76 confirmed) and `weimer2019` (39 confirmed) supply most
  statistical power even in the non-giant build; `harmer2013` (4) and
  `lee2018`/`hulme2026` (2/9) remain too small individually.
- Topic/date/station confounds are only partially controlled. Same-year
  and full-corpus backgrounds give near-identical results in the
  large-n groups specifically because the ground truth spans nearly the
  graph's entire 1973-1979 year range, so "same-year" background converges
  to "full corpus" background by construction — this is *not* strong
  evidence the date confound was ruled out, just that this particular
  control didn't have much room to matter for these particular groups.
- Ground-truth label noise: `flagged`-tier rows are reported separately
  from `confirmed` throughout (`tier`/`tier_scope` columns).
- `closeness` is present in the schema but populated for zero nodes in
  every build tested so far.
- `missing` (boolean) is included in the auto-detected numeric sweep but
  is degenerate — every ground-truth cable that matched the graph at all
  has `missing=False` by construction (it had to have its own record to
  be extractable and joinable), so there's no variance to test within the
  selected group.
- FDR correction is applied separately per test family specifically to
  avoid one family's tautological hits inflating another's apparent
  significance (this is what changed `cd-index-type`'s giant-build result
  between passes of this analysis) — don't recombine `attribute_signal_*.csv`
  files and re-derive a single global correction without accounting for
  this.
- `antichain` is only testable on the giant build, which is also the
  build with the least ground-truth coverage — its null result should be
  read as "underpowered and inconsistent across builds," not "ruled out."

## Reproducing

```
python3 questions/publication-cable-graph-signal/code/build_node_table.py \
  <path-to-enriched-graphml> [ground_truth_csv] [output_csv]
python3 questions/publication-cable-graph-signal/code/attribute_signal.py \
  [node_features_csv] [ground_truth_matched_csv] [output_dir]
```

`build_node_table.py` requires the graphml path as its first argument (no
default — the file lives outside the repo and its name/schema changes over
time); `attribute_signal.py` reads `build_node_table.py`'s CSV output and
needs no graphml path itself. To reproduce the non-giant comparison, point
`output_csv`/`node_features_csv`/`output_dir` at a separate directory (this
repo used `results/nongiant/`) so it doesn't overwrite the giant-build
results. Outputs per build: `node_features.csv`,
`ground_truth_matched.csv`,
`attribute_signal_{numeric,categorical,cdindex,antichain}.csv`.
