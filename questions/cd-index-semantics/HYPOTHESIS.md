# How does the CD-index semantic translate to a telegram reference network?

**Status:** answered
**Thread of:** —

**Short answer:** Partially, and not the way it looks. The formula's
mechanics carry over cleanly, and a domain-calibrated window (~180 days,
not the patent literature's 5 years) makes the measure well-behaved. But
**62% of every "disruptive"-labeled cable in this corpus is disruptive
purely because it has zero REF: lines of its own** — a mathematical
certainty of the formula (no predecessor means `bit` can never be 1), not
an editorial signal that later traffic "routed around" it. That degeneracy
is rare in the patent literature (prior art citation is near-universal)
and central here (standalone/administrative cables are common). The
"consolidating = part of a continuing thread" half of the intuitive
reading holds up — confirmed by reading real cable content, and, at full
population scale (1.6M+ nodes, every numeric graph attribute tested, not a
sample), by higher edge trussness and higher neighbor-community-sharing
around consolidating cables in both graph builds, both effects surviving a
control for the predecessor-count degeneracy itself. Disruptive cables
independently confirm as broadcast-hub-shaped via pagerank/authority
(pointed to by many citers). The "disruptive = pivotal anchor cable" half does
not — most disruptive cables, even away from the mechanical extreme, are
unremarkable single-topic notices. See `results/FINDINGS.md` §1.

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
   than the 1825-day window this codebase originally used — **tested
   empirically below, and validated**: a build with the 180-day window
   actually computed shows the corpus-boundary censoring effect as a
   legible 3-month climb (Oct-Dec 1979) instead of the 1825-day window's
   easy-to-miss single-month spike, exactly as predicted.
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

A fifth issue was not predicted in advance — it turned up from reading
actual cable content and checking the formula's behavior directly, and
turned out to be the biggest translation problem of the four-plus-one:

5. **A cable with zero predecessors of its own is mathematically forced to
   `cd-index = +1.0` ("disruptive") the moment it's cited at all** — not a
   tendency, a certainty of the formula (see `results/FINDINGS.md` §1). Patents almost
   always have prior art to cite; a large share of cables in this corpus
   are standalone originating reports or administrative circulars with no
   REF: line of their own. This confounds "disruptive" with "cable that
   happened not to reference anything," which has nothing to do with the
   patent-domain meaning of disruptive (a cable that *did* have
   predecessors but got cited instead of them).

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
- **mCD index**: `mcd_index = CD_index × I_index` (`I_index` = direct
  citers of `f` within the window = the paper's `mt`), matching Eq. 4
  exactly. As of the `reftel-with-tags-estimated-CD-index-6month-
  2026-08-02.graphml` build this **is now exposed** as an `mcd-index` node
  attribute (previously only `cd-index`/`cd-index-type`, the plain `CDt`,
  reached this repo) — not yet analyzed here, a natural next step.
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
  `cd-index`/`cd-index-type` computed with the 1825-day window. Plus two
  fresh builds computed with a **~180-day window** (directly testing this
  question's own recommendation), on top of `all-mrns-tags.estimated.ndjson`
  (better date coverage — see Caveats for why this makes the window
  comparison not perfectly apples-to-apples): `reftel-with-tags-estimated-
  CD-index-6month-2026-08-02.graphml` (1,637,670 nodes, non-giant, no
  `antichain`) and its giant sibling `...6month-2026-08-02.giant.graphml`
  (379,368 nodes, has `antichain`). All four carry `cd-index`/`cd-index-type`;
  the two 6-month builds additionally expose `mcd-index`.
- Related-question evidence (read directly, not via code — see AGENTS.md's
  sharing rule): `reference-time-lag/results/reference_time_lag.md`'s
  measured REF:-resolution lag distribution, used as the empirical
  yardstick for evaluating the window-length translation below.
- Code: `code/cd_index_date_profile.py` (year/month `cd-index-type`
  cross-tabulation) and `code/graph_structure_by_type.py` (trussness /
  coreness / community-sharing tests, see `results/FINDINGS.md` §1) — question-exclusive, both load
  a graphml directly (path required, no default, matching the convention
  established in `publication-cable-graph-signal` after its "no hardcoded
  graph file" fix).

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

See [`results/FINDINGS.md`](results/FINDINGS.md) for the full write-up
(six sections: the central predecessor-count-degeneracy finding and its
population-scale structural confirmation; the patent→cable translation
table; the time-window mismatch analysis; the validated ~180-day-window
recomputation; overall type distributions; what's still untested).
Headline: **62% of every "disruptive"-labeled cable is disruptive purely
because it has zero REF: lines of its own** — a mathematical certainty of
the formula, not an editorial signal — confirmed both by reading real
cable content and, at population scale (1.6M+ nodes), by trussness and
(once controlled for the same degeneracy) community-sharing both
independently confirming the "consolidating = thread-embedded" half of
the reading. The recommended ~180-day window (vs. the codebase's 1825-day
default) was built and validated: it turns an easy-to-miss single-month
undefined-rate spike into a legible 3-month corpus-boundary climb, exactly
as predicted.

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
- The giant-vs-non-giant type-distribution shift (`results/FINDINGS.md`
  §5) and the 1825-day-vs-180-day shift (§4) are both reported as
  observations, not yet decomposed into "which specific cables flip
  category" — a natural follow-up given the tools already exist
  (`code/cd_index_date_profile.py` could be extended to join builds on
  `label` and cross-tabulate the flip).
- **The 180-day-window comparison (`results/FINDINGS.md` §4) is not a
  clean isolation of window length alone**:
  `reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml`
  is built on `all-mrns-tags.estimated.ndjson` (1,637,670 dated vertices)
  rather than the plain `all-mrns-tags.ndjson` the 1825-day non-giant build
  used (1,419,822 vertices) — better date coverage changes which nodes are
  even eligible for a defined CD-index, independent of window length. The
  year-level undefined-rate table is confounded by this; the month-level
  1979 table is the trustworthy part of that comparison, since the
  within-1979 gradient (flat Jan-Sep, climbing Oct-Dec) is a *shape*
  argument about window length specifically, not a base-rate comparison
  across differently-built graphs.
- The predecessor-count-controlled comparison (`results/FINDINGS.md` §1)
  only covers trussness, coreness, and community-sharing — hub score was
  flagged there as "likely mechanical" by reasoning about the formula, not
  by actually re-running it restricted to the predecessor-having subset,
  and remains an open gap. The antichain effect (+0.501, by far the
  largest raw effect measured) was flagged the same speculative way but
  has since been **followed up properly** in
  [`antichain-semantics`](../antichain-semantics/HYPOTHESIS.md): antichain
  turns out to be driven by in-degree, not out-degree/predecessor-count,
  so it's a genuinely different (not "likely mechanical") signal that
  happens to correlate — read that investigation rather than treating the
  original speculation here as the last word.
- This question deliberately does not re-litigate whether `cd-index-type:
  disruptive` enrichment among historian-cited cables (found in
  `publication-cable-graph-signal`) is *real* — that statistical result
  stands on its own. `results/FINDINGS.md` §1's finding gives that result
  a more literal reading than originally guessed (see its "reframes"
  paragraph) but doesn't retest it.
- `results/FINDINGS.md` §1's text-content sample is small (12 cables per bucket, 2 buckets, 1
  random seed) — but it's no longer the primary evidence: the
  predecessor-count mechanism is a mathematical identity (not a pattern in
  a sample), and the trussness/coreness/community-sharing tests run at
  full population scale (1.6M+ nodes, both builds). What the text sample
  alone doesn't cover: the *substantive content* of the 37.8% of
  disruptive cables that do have ≥1 predecessor and therefore aren't
  mechanically forced to `cd-index=1.0` — that "genuinely disruptive in
  something like the patent sense" subset is the one still worth reading
  more of, and isn't distinguished from the 62.2% mechanically-forced
  group by any test run so far (trussness/coreness were computed against
  the whole disruptive bucket, not split by predecessor count).

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
