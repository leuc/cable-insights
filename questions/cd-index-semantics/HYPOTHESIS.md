# How does the CD-index semantic translate to a telegram reference network?

**Status:** open
**Thread of:** —

## Question

`publication-cable-graph-signal` and `reference-graph-structure` both
consume `cd-index`/`cd-index-type` off the externally-enriched graphml as
if "disruptive" and "consolidating" were self-evidently meaningful labels
for a diplomatic cable. They aren't self-evident — the CD-index is a
measure imported wholesale from the patent-citation literature (Funk &
Owen-Smith), built around patents' curated legal bibliography, multi-year
technology-diffusion citation dynamics, and firm/university portfolio
analysis. None of that is obviously true of a 7-year, REF:-line-extracted
telegram network. This question interrogates the translation directly,
rather than taking the label at face value the way the other two questions
do.

## Hypothesis

The core CD-index mechanic (does later traffic treat this document as a
standalone reference point that supersedes what it built on, or as one
link in a continuing chain) should carry over structurally — patents and
cables both form directed, (mostly) acyclic citation-like graphs. But
several of the measure's *parameter choices*, tuned for patents, are
predicted to translate poorly:

1. **The 5-year (1825-day) forward-citation window** is patent-domain
   scale (citation is a slow, multi-year diffusion process there). A
   domain-appropriate window derived from `reference-time-lag`'s measured
   REF: reply distribution (mean 14.6d, stdev 53.6d) is **~180 days (6
   months)** — mean + 3σ ≈ 175d, rounded up, and still 3× the slowest
   observed station's p90 (BRUSSELS, 60d) for margin. That's ~10× shorter
   than the 1825-day window this codebase actually uses — **tested
   empirically below**.
2. **`bit` counts only direct, one-hop predecessors**, not the full
   transitive ancestor set — a known patent-literature simplification that
   should bite harder here, since REF: chains are frequently literal
   multi-hop reply threads (C3 refs C2 refs C1 refs C0), and a later cable
   that refs C0 or C3 directly (skipping C1/C2) won't register as
   "consolidating" C2 under a one-hop rule, even though it's obviously the
   same continuing correspondence — **not yet tested**.
3. **REF:-line extraction noise** (OCR errors, ambiguous same-day
   candidates, unmatched station abbreviations — see
   `acp-127/src/reftel_normalize.py`'s documented failure modes) directly
   corrupts `fit`/`bit`, unlike patents' clean, examiner-reviewed
   bibliography — **not yet tested**.
4. **The university/firm portfolio aggregates** (`CDmean5`, `mCDscale5`,
   `CDtotal±5`) have no cable-domain analog defined yet; a per-station or
   per-TAGS "portfolio" aggregate is a plausible cable-domain equivalent —
   **not yet defined or tested**.

## Grounding: the CDt / mCDt index (patent-citation literature)

**Setup.** A tripartite citation graph `G(V1, V2, V3, E)`: `V1` = focal
patent `f`, `V2` = predecessors `b` (patents `f` cites, **direct one-hop
only**), `V3` = future patents `i` that eventually cite `f` and/or its
predecessors within a time window. Edges are directed, acyclic.

**Per-citer indicators**, for each future citer `i`:
- `fit = 1` if `i` cites `f` directly, else 0
- `bit = 1` if `i` cites any of `f`'s direct predecessors, else 0

**CDt index:**

```
CDt = (1/nt) · Σ (−2·fit·bit + fit) / wit
```

`nt` = total forward citations of `f` and/or its predecessors in the
window; `wit` = optional per-citer weight. `+1` per citer that cites `f`
alone (destabilizing/disruptive — displaces the predecessors); `−1` per
citer that cites both `f` and a predecessor (consolidating — reinforces
them); `0` per citer that only cites a predecessor. Range `[−1, +1]`.

**mCDt index:** `mCDt = (mt/nt) · Σ(...) = mt · CDt`, where `mt` = citations
of the focal patent *only*, a magnitude/impact weight on the directional
CDt signal.

**Undefined:** when `nt = 0`, both indexes are undefined — 2.8% of patents
at the patent literature's 5-year mark.

**Parameter choices actually used in the source paper:** `wit = 1`
throughout ("for simplicity" — the weighted variant is presented but never
run); **5-year window** as the headline measure (chosen because "annual
citations of most patents reach their peak within this time frame");
undefined patents excluded from primary models (a robustness check imputes
0 instead — "nearly identical" results either way).

## Exact computation used by this codebase

Cross-checked `/home/jsm/Code/igraph-vlk/src/graph/wrappers_centrality.c`
against `igraph_cd_index` directly (full paper text also cross-referenced,
archived at
`/tmp/claude-1001/-home-jsm-Code-igraph-vlk/677ab825-1c1e-4ad3-9ee7-821bcb218285/scratchpad/cd_index_paper_fulltext.txt`
for this session):

- **Formula**: `Σ (fbit − 2·fbit·bbit) / |C|` — algebraically identical to
  the paper's `(−2·fit·bit + fit)/nt`.
- **`wit`**: hardcoded to 1 — an exact match to what the paper actually ran
  in every reported result, not a simplification relative to it.
- **Time window**: `CD_INDEX_TIME_WINDOW_DAYS = 1825`
  (`wrappers_centrality.c:414`) — exactly `5 × 365`, i.e. this codebase
  computes precisely the paper's headline `CD5`/`mCD5`.
- **mCD index**: exposed internally as `mcd_index = CD_index × I_index`
  (`I_index` = direct citers of `f` within the window = the paper's `mt`),
  matching Eq. 4 exactly — but the current wrapper only surfaces the plain
  CD index (`igraph_cd_index(..., NULL, NULL, ...)`, dropping the
  `i_index`/`mcd_index` output pointers), so **`mCDt` is computed
  internally but never exposed** to the graphml this repo consumes. Only
  `cd-index`/`cd-index-type` (the plain `CDt`) reach us.
- **Undefined handling**: returns `NaN` for empty `C`; the enrichment
  pipeline preserves that as `cd-index-type = "nan"` rather than silently
  coercing to 0 — the paper's *preferred* (exclusion) treatment, not its
  robustness-check imputation.
- **Predecessor scope**: `bit`/`C` is direct, one-hop predecessors only —
  not the transitive ancestor set, in both the paper and this
  implementation (see Hypothesis point 2).
- Requires a self-loop-free input graph (a non-issue here — cables can't
  cite themselves) and parallelizes across vertices via OpenMP — an
  implementation detail, not a definitional one.

## Data used

- External: the same enriched graphml builds used by
  `publication-cable-graph-signal` — a giant-component build (347,203
  nodes) and its non-giant sibling (1,419,822 nodes), both carrying
  `cd-index`/`cd-index-type`.
- Related-question evidence (read directly, not via code — see AGENTS.md's
  sharing rule): `reference-time-lag/results/reference_time_lag.md`'s
  measured REF:-resolution lag distribution, used as the empirical
  yardstick for evaluating the window-length translation below.
- Code: `code/cd_index_date_profile.py` — question-exclusive, loads a
  graphml directly (path required, no default, matching the convention
  established in `publication-cable-graph-signal` after its "no hardcoded
  graph file" fix) and cross-tabulates `cd-index-type` by cable year/month.

## Method summary

1. Document the patent-CD-index → cable-network translation systematically
   (table below) rather than assuming it.
2. Pick the most concretely falsifiable translation claim — the 5-year
   window is oversized for a domain where references resolve in days — and
   test it: if the window is oversized relative to corpus length, the
   `cd-index-type = "nan"` (undefined, `nt=0`) rate should climb sharply
   for cables near the corpus's end (1979), since their forward window
   gets truncated by the corpus boundary rather than genuinely lacking
   forward traffic.
3. Cross-reference the result against `reference-time-lag`'s independently
   measured REF: resolution-lag distribution to explain *why* the result
   comes out the way it does, rather than stopping at "undefined rate by
   year."

## Result

### 1. Translation table

| Patent-CD concept | Cable-network analog | Fit |
|---|---|---|
| Focal patent `f` | Focal cable (MRN node) | Direct |
| Predecessor `b` (direct, one-hop) | Cable(s) `f`'s REF: line(s) point to | Structurally direct, but see caveat 2 below — patent "cites prior art" is a broad synthesis relationship; cable REF: is usually a narrow "in reply to / further to" pointer within the same correspondence thread |
| Future citer `i` | Later cable that REF:s `f` and/or its predecessors, in-window | Direct |
| DAG, citations point only to prior work | REF: lines point only to earlier documents | Mostly fine; same-day multi-part cables are a minor edge case |
| 5-year (1825-day) window | — | **Major mismatch, tested below** |
| `wit` hardcoded to 1 | Same, unchanged | No difference — same simplification either way |
| Undefined when `nt=0` | Same condition, but likely far more common here (the base reference graph is very sparse — see `publication-cable-graph-signal`'s coverage-gap finding) | Same rule, different base rate |
| University/firm portfolio aggregates (`CDmean5`, `mCDscale5`, `CDtotal±5`) | No cable-domain analog defined yet — a per-station or per-TAGS aggregate is the natural candidate | **Undefined, not yet built** |

### 2. Time-window mismatch — tested, and the finding is more precise than the hypothesis predicted

`reference-time-lag` measured the actual gap between a citing cable and
what it references, full corpus, 2,055,547 resolved pairs: **median 6
days, mean 14.6 days, p90 40 days** (vs. a random-pair baseline median of
158 days). Real REF: resolution is essentially complete within **40 days**
for 90% of pairs. The CD-index window used by this codebase is **1825
days — roughly 45× the p90 lag, ~300× the median.**

The naive prediction from that mismatch: `cd-index-type = "nan"` should
climb steadily across 1973→1979 as more and more of each cable's nominal
5-year window falls outside the 1973-1979 corpus. **That's not what the
year-level data shows** (`results/cd_index_by_year_giant.csv`,
`results/cd_index_by_year_nongiant.csv`):

| year | giant: % undefined | non-giant: % undefined |
|---|---|---|
| 1973 | 30.4% | 47.6% |
| 1974 | 20.9% | 41.3% |
| 1975 | 19.9% | 38.1% |
| 1976 | 20.7% | 38.2% |
| 1977 | 19.1% | 35.2% |
| 1978 | 18.5% | 34.2% |
| 1979 | 21.2% | 36.3% |

1974 (which gets its *entire* nominal 5-year window inside the corpus,
since 1974+5=1979) and 1979 (which gets almost none) have **nearly
identical** undefined rates in both builds. The window's specific length
barely matters at the year level — because, per `reference-time-lag`,
essentially all of the "action" a forward-citer window could ever capture
happens in the first ~40 days regardless of how much runway is nominally
available afterward.

Month-level granularity within 1979 (giant build) confirms this precisely
rather than contradicting it — the censoring effect is real, just far
narrower than a naive year-level reading would suggest:

| month | % undefined |
|---|---|
| 1979-01 through 1979-11 | 18.6% – 21.8% (flat, no trend) |
| **1979-12** | **33.2%** |

Only the corpus's literal final month — where a cable has close to zero
days of forward runway, well under the 40-day p90 resolution window —
shows a clear jump. Everything from January through November 1979 still
has enough runway (≥30 days, usually much more) to capture nearly all of
its real forward citations, so the mismatch between a 1825-day nominal
window and a ~40-day real one turns out **not to matter** for the vast
majority of the corpus. It only matters at the literal edge.

**Recommended cable-domain window: ~180 days (6 months)**, not 1825. That
figure comes directly from `reference-time-lag`'s measured distribution:
mean (14.6d) + 3 stdev (53.6d) ≈ 175d, rounded to 180 for a clean 6-month
figure, and independently checked against the slowest individual station
in that dataset (BRUSSELS, p90 = 60d) — 180 days is 3× that station's own
90th-percentile lag, so it comfortably covers even the slowest-resolving
posts, not just the corpus-wide average. A cable with ≥180 days of runway
before 1979-12-31 (i.e. dated before ~1979-07-05) should see essentially
identical `cd-index-type` classification whether computed with a 180-day
or an 1825-day window, per the year/month evidence above; only cables
dated after that point would classify differently under the shorter,
more domain-appropriate window — and for those, a shorter window is *more*
correct, not less, since the extra ~4.5 years the 1825-day window nominally
grants them don't exist in this corpus regardless. The 1973 elevated
undefined rate (30-48%, both builds) is a separate effect, not explained
by forward-window truncation at all — 1973 has roughly half the cable
volume of other years (partial-year corpus ramp-up), so the reference
graph is intrinsically sparser there independent of any window-length
question.

### 3. Overall type distribution (for context)

| | giant | non-giant |
|---|---|---|
| disruptive | 38.4% (mean CD +0.79) | 39.2% (mean CD +0.91) |
| consolidating | 41.7% (mean CD −0.12) | 22.9% (mean CD −0.19) |
| undefined | 19.9% | 37.9% |

The consolidating share drops sharply from giant to non-giant (41.7% →
22.9%) while disruptive stays roughly flat — consistent with
`publication-cable-graph-signal`'s finding that giant-component membership
already selects for well-connected, multiply-referenced cables (which
should skew consolidating almost by construction, since a well-embedded
cable is more likely to be cited *alongside* its own predecessors).

### 4. Not yet tested

Hypothesis points 2-4 (one-hop-predecessor chain bias, REF:-extraction
noise sensitivity, portfolio aggregates) remain open — see Caveats and
Related questions.

## Caveats / limitations

- The "not yet tested" items above are real gaps, not just hedges: the
  one-hop-predecessor issue in particular could matter a lot for this
  domain's long reply-chain cables and deserves its own pass (e.g.
  comparing CD-index computed on direct predecessors only vs. the full
  transitive reference closure, for a sample of known long threads).
- `nt` (the raw forward-citer count) isn't itself exposed as a graphml
  attribute — the undefined-rate analysis here uses `cd-index-type ==
  "nan"` as a proxy for `nt=0`, which is exactly what the paper's own
  definition says it means, but there's no way from this codebase's output
  alone to distinguish "nt=0 because genuinely nothing cited this" from
  "nt=0 because REF:-extraction failed to resolve a real citation" — see
  hypothesis point 3.
- The giant-vs-non-giant type-distribution shift (section 3) is reported
  as an observation, not yet decomposed into "which specific cables flip
  category" — a natural follow-up given the tools already exist
  (`code/cd_index_date_profile.py` could be extended to join both builds
  on `label` and cross-tabulate the flip).
- This question deliberately does not re-litigate whether `cd-index-type:
  disruptive` enrichment among historian-cited cables (found in
  `publication-cable-graph-signal`) is *real* — that statistical result
  stands on its own. What's open here is *interpretive*: given everything
  above, what does "disruptive" mean substantively for a cable, and is
  that reading defensible. Provisional reading, not yet validated against
  actual cable content: a "disruptive" cable is one that becomes the
  citable anchor point for a topic (a major assessment, a NIACT event
  report) such that later cables cite *it* without needing to also cite
  what it built on; a "consolidating" cable is one that reads as part of a
  continuing thread, cited alongside its own predecessors (e.g. routine
  periodic reporting, sequential debt-negotiation cables).

## Related questions

- [`reference-time-lag`](../reference-time-lag/HYPOTHESIS.md) — its
  measured REF: resolution-lag distribution (median 6d, p90 40d) is the
  empirical basis for this question's time-window analysis; that question
  didn't set out to inform CD-index parameter choice, but its result
  turned out to be exactly what this question needed.
- [`publication-cable-graph-signal`](../publication-cable-graph-signal/HYPOTHESIS.md) —
  consumes `cd-index-type` downstream (found `disruptive` enrichment among
  historian-cited cables); this question interrogates what that attribute
  actually means rather than re-testing whether the enrichment is real.
- [`reference-graph-structure`](../reference-graph-structure/HYPOTHESIS.md) —
  shares the same base reference graph this measure is computed over.
