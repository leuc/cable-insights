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
unremarkable single-topic notices. See Result §1.

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
   tendency, a certainty of the formula (see Result §1). Patents almost
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
  coreness / community-sharing tests, §1) — question-exclusive, both load
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

### 1. The central finding: "disruptive" is largely a structural artifact, not an editorial signal

This is the direct answer to the question this file is named after. Pulled
real cable content for the most extreme disruptive/consolidating cables
(`cd-index` near ±1) from `reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml`
and checked the formula's behavior against each cable's own predecessor
count (`out_degree` = how many REF: lines the cable itself has):

**The mechanism:** `bit` (does a later citer also cite one of `f`'s
predecessors) can only ever be 1 if `f` *has* a predecessor. A cable with
zero REF: lines of its own has an empty predecessor set, so `bit=0` for
every possible citer, always — which makes `CDt = nt/nt = 1.0` exactly,
with no exceptions, the instant that cable is cited by anyone. Checked
directly:

| | disruptive cables with ≥1 predecessor | disruptive cables with 0 predecessors |
|---|---|---|
| count | 264,599 (37.8%) | 434,937 (**62.2%**) |
| mean `cd-index` | 0.806 | **1.000, exactly, no exceptions** |

**62% of every cable labeled "disruptive" in this build is disruptive
purely because it never referenced anything else — not because later
traffic chose to cite it instead of its predecessors.** That's the actual
patent-domain meaning of disruptive (Funk & Owen-Smith: "the citer routes
around the focal document's own antecedents") — but routing around
requires antecedents to route around. This degeneracy barely exists in
the patent literature (prior art citation is close to universal there);
it's central here, because REF:-less standalone reports are common in
this corpus.

Content confirms this mechanically, not just statistically. Sampling the
highest-`cd-index`, highest-*degree* disruptive cables returns almost
entirely **broadcast administrative circulars** — "REPORTING REQUIREMENT:
SECTION 36(A)(7) OF ARMS EXPORT CONTROL ACT," "LIST OF DOCTORS," "ADP AND
WORD PROCESSING INVENTORY AT FOREIGN SERVICE POSTS" — STATE-to-all-posts
broadcasts (degree up to 344) that structurally have no reason to REF: a
predecessor themselves, and whose many independent respondents naturally
each cite the circular alone. Sampling **low-degree** (2-5 citers, the
actual median — see below) consolidating cables tells the opposite,
cleaner story: nearly every one carries multiple REF: lines to the *same*
ongoing bilateral or working-group thread — "REF: A) TAIPEI 2095, B)
TAIPEI 1869, C) TAIPEI 1576," "REF A) BANGKOK 10859 B) BANGKOK 12899 C)
BANGKOK 14590" — and gets cited back alongside that same thread. That part
of the original "consolidating = part of a continuing thread" reading
holds up under inspection; the "disruptive = pivotal anchor cable" half
did not — most disruptive cables, even away from the circular-broadcast
extreme, are unremarkable single-topic administrative notices, not
historically significant turning points. Full sample: `results/cd_index_content_samples.md`.

**Graph-structure confirmation, at full population scale (not a 24-cable
sample), every numeric node attribute auto-detected and tested, plus two
edge-derived aggregates** — `code/graph_structure_by_type.py`, run against
both the non-giant (1,637,670 nodes) and giant (379,368 nodes, has
`antichain`) 6-month builds, **and** re-run restricted to the 37.8-61.1%
of disruptive cables that *do* have ≥1 predecessor of their own (the
subset not mechanically forced to `cd-index=1.0`) vs. consolidating, to
check which effects survive controlling for the predecessor-count
degeneracy in Result section 1 above. Rank-biserial effect sign: positive
= consolidating scores higher, negative = disruptive scores higher.

*Survives the predecessor-count control — genuine, independent evidence:*

- **Trussness** — predicted: a consolidating citer, by definition, cites
  both `f` and one of `f`'s own predecessors, so the edges (citer→f),
  (citer→pred), (f→pred) form a triangle, which trussness measures
  directly. **Confirmed in all four comparisons** (both builds, before and
  after the predecessor-count control): non-giant all-disruptive +0.280 →
  with-predecessor-only +0.220; giant all-disruptive +0.155 →
  with-predecessor-only +0.120. Attenuates somewhat under control but
  never disappears or reverses — the single most trustworthy structural
  signal in this analysis.
- **PageRank / authority** — disruptive cables score substantially *higher*
  on both (non-giant: pagerank −0.753, authority −0.440; giant: pagerank
  −0.778, authority −0.041) — both reward being pointed to by many/
  important citers, exactly the broadcast-circular signature (many
  independent posts each citing the circular once). Not run through the
  predecessor-count control, but this is the *disruptive* side of the
  story and isn't the effect that control was checking.
- **Community-sharing** — reverses from "null" to genuinely confirmed once
  controlled: non-giant all-disruptive −0.0001 (n.s., p=0.76) →
  with-predecessor-only **+0.034 (p<10⁻³⁰⁰)**; giant all-disruptive +0.059
  → with-predecessor-only **+0.101**. The uncontrolled "null" in non-giant
  was itself an artifact of the confound — 0-predecessor disruptive cables
  happen to have very high community-sharing themselves (~0.99, diluting
  the comparison), and once excluded the predicted gap shows up clearly in
  both builds.

*Doesn't survive, or wasn't controlled for — likely substantially
mechanical, not independent confirmation:*

- **Antichain** (giant only) — by far the *largest* raw effect measured
  (median layer 0 disruptive vs. 1 consolidating, +0.501, p<10⁻³⁰⁰), but
  not yet run through the predecessor-count control, and very likely
  explained by the same fact: antichain layers by longest path from a
  source, and a 0-predecessor cable *is* a source by definition, so it's
  essentially guaranteed to sit at the base layer regardless of any real
  "broadcast vs. thread" distinction. Suggestive, not independent evidence
  as it stands.
- **Hub score** — consolidating higher in both builds, but the effect size
  swings wildly (non-giant +0.793, giant +0.137) and the mechanism is
  nearly definitional: a 0-predecessor cable has no outgoing edges at all,
  so its hub score (which requires pointing to authorities) is trivially
  ~0 — the same structural fact as trussness/coreness, not new evidence.
- **Coreness** — the one metric that's genuinely **inconsistent**:
  non-giant confirms the original prediction (+0.213) but nearly vanishes
  under the predecessor control (+0.008, practically zero despite
  p<10⁻⁹ at this n); giant *reverses* even before controlling (−0.054)
  and reverses harder after (−0.185, disruptive-with-predecessor cables
  more core-embedded than consolidating). Don't cite this as supporting
  evidence — it doesn't reliably point either direction.
- **Degree / strength / betweenness** — disruptive consistently higher in
  both builds (matches the broadcast-hub picture already established from
  the earlier high-degree text sample), but this is restating what
  drove that sample selection, not new information.

**Net read:** trussness and (once controlled) community-sharing are real,
independent structural confirmation that consolidating cables sit in
denser, triangle-rich thread structure — genuinely new evidence beyond the
text sample, not just a restatement of the predecessor-count mechanism.
PageRank/authority independently confirm the *disruptive* side (broadcast
hubs draw many citers). Antichain and hub score point the same way but are
too entangled with the same 0-predecessor degeneracy to count as
independent; coreness shouldn't be used as evidence at all — it doesn't
hold a consistent direction. Full numbers:
`results/graph_structure_by_type.csv` (non-giant),
`results/graph_structure_by_type_giant.csv` (giant) — each file has both
the all-disruptive and predecessor-controlled comparisons.

**Practical reframing, not "historically pivotal vs. routine":**
"disruptive" ≈ *this cable didn't reply to anything* (an origination
property); "consolidating" ≈ *this cable is visibly part of a multi-cable
thread that later citers keep citing as a unit* (a continuation property).
That's a real, defensible structural distinction — just a different one
than the patent literature's, and not one where "disruptive" implies
anything about historical significance on its own.

**This reframes `publication-cable-graph-signal`'s finding**, not
undermines it: historians disproportionately citing `disruptive` cables is
still real, but a more literal explanation than "historians cite pivotal
cables" is available — historians may simply be more likely to cite
**standalone originating reports** (a cable that's the first, self-contained
account of something) over cables buried in a reply chain, since a
standalone report is what a citation typically points to. That's a
coherent, mechanically-grounded reading; the earlier "anchor cable"
framing was speculation asserted without checking, and turned out to be
only partially right (see above).

### 2. Translation table

| Patent-CD concept | Cable-network analog | Fit |
|---|---|---|
| Focal patent `f` | Focal cable (MRN node) | Direct |
| Predecessor `b` (direct, one-hop) | Cable(s) `f`'s REF: line(s) point to | Structurally direct, but see caveat 2 below — patent "cites prior art" is a broad synthesis relationship; cable REF: is usually a narrow "in reply to / further to" pointer within the same correspondence thread |
| Future citer `i` | Later cable that REF:s `f` and/or its predecessors, in-window | Direct |
| DAG, citations point only to prior work | REF: lines point only to earlier documents | Mostly fine; same-day multi-part cables are a minor edge case |
| 5-year (1825-day) window | ~180-day window recommended and validated (§4) | **Mismatch confirmed, fix validated** |
| Predecessor set can be empty (cable with no REF: of its own) | Common here (see §1) — patents almost always have prior art, so this degeneracy is rare there | **Major, previously-unpredicted mismatch — this is the headline finding** |
| `wit` hardcoded to 1 | Same, unchanged | No difference — same simplification either way |
| Undefined when `nt=0` | Same condition, but likely far more common here (the base reference graph is very sparse — see `publication-cable-graph-signal`'s coverage-gap finding) | Same rule, different base rate |
| University/firm portfolio aggregates (`CDmean5`, `mCDscale5`, `CDtotal±5`) | No cable-domain analog defined yet — a per-station or per-TAGS aggregate is the natural candidate | **Undefined, not yet built** |

### 3. Time-window mismatch — tested, and the finding is more precise than the hypothesis predicted

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

### 4. Direct test: the recommended ~180-day window, as actually computed

The recommendation above got built and run:
`reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml` carries
`cd-index`/`cd-index-type` computed with a ~180-day window instead of
1825. **The predicted right-censoring signature shows up exactly where
predicted, and far more clearly than under the oversized window.**

Year-level undefined rate, 1825-day vs. 180-day (both non-giant — note the
180-day build's underlying graph also has better date coverage from
`all-mrns-tags.estimated.ndjson`, so this isn't a pure ceteris-paribus
window-only comparison; see caveats):

| year | 1825-day % undefined | 180-day % undefined |
|---|---|---|
| 1973 | 47.6% | 38.7% |
| 1974 | 41.3% | 36.8% |
| 1975 | 38.1% | 34.9% |
| 1976 | 38.2% | 35.6% |
| 1977 | 35.2% | 33.9% |
| 1978 | 34.2% | 33.0% |
| 1979 | 36.3% | 33.6% |

Undefined rate is uniformly *lower* under the shorter window at the year
level (confounded by the richer base graph, not a clean isolation of
window length alone). The month-level breakdown within 1979 is the real
test, and it's unambiguous:

| month | 1825-day % undefined | 180-day % undefined |
|---|---|---|
| Jan–Sep 1979 | flat, 18.6–21.8% | flat, 30.3–32.4% |
| Oct 1979 | 20.9% (no jump yet) | 35.4% (climbing) |
| Nov 1979 | 21.7% (no jump yet) | 36.7% (climbing) |
| Dec 1979 | **33.2%** (sharp, isolated spike) | **50.6%** (sharp peak, end of a 3-month climb) |

This is exactly the shape predicted: with a 180-day window, cables dated
from roughly October onward have progressively less than a full window of
runway before the corpus ends (Oct 1979 → ~90 days runway, Nov → ~60,
Dec → ~30 or less), so the undefined rate climbs *starting three months
out*, not just in the final month. Under the old 1825-day window this same
real effect was compressed into a single-month spike, easy to miss
entirely if you weren't looking for it. **The shorter window doesn't
introduce a new problem — it makes an existing, real corpus-boundary
effect legible instead of hiding it inside a nominally-huge window that
was never actually being used for 99%+ of its length.** Practical
implication for anyone consuming `cd-index-type` from this build: treat
cables from roughly the last quarter of the corpus (Oct–Dec 1979) as
increasingly unreliable/undefined-prone, not just December.

Overall type distribution also shifted modestly (again confounded with
the base-graph change): disruptive 39.2%→42.7%, consolidating
22.9%→22.4%, undefined 37.9%→34.9% (non-giant, 1825-day vs. 180-day).
Mean CD-index within each defined bucket moved slightly more extreme
(disruptive mean +0.91→+0.93, consolidating mean −0.19→−0.19 — consolidating
essentially unchanged, disruptive nudged toward the boundary), consistent
with a shorter window giving fewer citers per node overall, which pushes
`CDt` toward its extremes (`±1`) since there's less room for a mixed
`fit`/`bit` signal to average out.

### 5. Overall type distribution, 1825-day window (for context)

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

### 6. Not yet tested

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
- The giant-vs-non-giant type-distribution shift (§5) and the
  1825-day-vs-180-day shift (§4) are both reported as observations,
  not yet decomposed into "which specific cables flip category" — a
  natural follow-up given the tools already exist
  (`code/cd_index_date_profile.py` could be extended to join builds on
  `label` and cross-tabulate the flip).
- **The 180-day-window comparison (§4) is not a clean isolation of
  window length alone**: `reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml`
  is built on `all-mrns-tags.estimated.ndjson` (1,637,670 dated vertices)
  rather than the plain `all-mrns-tags.ndjson` the 1825-day non-giant build
  used (1,419,822 vertices) — better date coverage changes which nodes are
  even eligible for a defined CD-index, independent of window length. The
  year-level undefined-rate table is confounded by this; the month-level
  1979 table is the trustworthy part of that comparison, since the
  within-1979 gradient (flat Jan-Sep, climbing Oct-Dec) is a *shape*
  argument about window length specifically, not a base-rate comparison
  across differently-built graphs.
- The predecessor-count-controlled comparison (§1) only covers trussness,
  coreness, and community-sharing — antichain and hub score are flagged as
  "likely mechanical" by reasoning about the formula, not by actually
  re-running them restricted to the predecessor-having subset. That's a
  real gap: the antichain effect in particular (+0.501, by far the largest
  measured) deserves the same controlled re-test before leaning on it at
  all, even as a suggestive lead.
- This question deliberately does not re-litigate whether `cd-index-type:
  disruptive` enrichment among historian-cited cables (found in
  `publication-cable-graph-signal`) is *real* — that statistical result
  stands on its own. §1's finding gives that result a more literal reading
  than originally guessed (see §1's "reframes" paragraph) but doesn't
  retest it.
- §1's text-content sample is small (12 cables per bucket, 2 buckets, 1
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
