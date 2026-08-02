# Findings: how does the CD-index semantic translate to a telegram reference network?

**Status:** answered. Full grounding, hypothesis, and methodology live in
[`../HYPOTHESIS.md`](../HYPOTHESIS.md) — this file is the detailed
write-up its Result section points to.

## 1. The central finding: "disruptive" is largely a structural artifact, not an editorial signal

This is the direct answer to the question this investigation is named
after. Pulled real cable content for the most extreme disruptive/
consolidating cables (`cd-index` near ±1) from
`reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml` and
checked the formula's behavior against each cable's own predecessor count
(`out_degree` = how many REF: lines the cable itself has):

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
historically significant turning points. Full sample:
`cd_index_content_samples.md`.

**Graph-structure confirmation, at full population scale (not a 24-cable
sample), every numeric node attribute auto-detected and tested, plus two
edge-derived aggregates** — `../code/graph_structure_by_type.py`, run
against both the non-giant (1,637,670 nodes) and giant (379,368 nodes, has
`antichain`) 6-month builds, **and** re-run restricted to the 37.8-61.1%
of disruptive cables that *do* have ≥1 predecessor of their own (the
subset not mechanically forced to `cd-index=1.0`) vs. consolidating, to
check which effects survive controlling for the predecessor-count
degeneracy above. Rank-biserial effect sign: positive = consolidating
scores higher, negative = disruptive scores higher.

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
  not run through the predecessor-count control here, and reasoned to be
  likely mechanical at the time. **Follow-up in
  `../../antichain-semantics/HYPOTHESIS.md` found the opposite**:
  `antichain` group membership is driven by in-degree (citation count),
  not out-degree (predecessor count) — a genuinely different mechanism
  from `cd-index`, that happens to correlate with it for an independent
  reason (both track the same "broadcast hub" cable archetype). Read that
  investigation's Result section before treating this antichain effect as
  either "confirmed" or "purely mechanical" — it's neither, it's a
  separate signal that correlates.
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
hubs draw many citers). Hub score is too entangled with the same
0-predecessor degeneracy to count as independent; coreness shouldn't be
used as evidence at all — it doesn't hold a consistent direction. Full
numbers: `graph_structure_by_type.csv` (non-giant),
`graph_structure_by_type_giant.csv` (giant) — each file has both the
all-disruptive and predecessor-controlled comparisons.

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

## 2. Translation table

| Patent-CD concept | Cable-network analog | Fit |
|---|---|---|
| Focal patent `f` | Focal cable (MRN node) | Direct |
| Predecessor `b` (direct, one-hop) | Cable(s) `f`'s REF: line(s) point to | Structurally direct, but patent "cites prior art" is a broad synthesis relationship; cable REF: is usually a narrow "in reply to / further to" pointer within the same correspondence thread |
| Future citer `i` | Later cable that REF:s `f` and/or its predecessors, in-window | Direct |
| DAG, citations point only to prior work | REF: lines point only to earlier documents | Mostly fine; same-day multi-part cables are a minor edge case |
| 5-year (1825-day) window | ~180-day window recommended and validated (§4) | **Mismatch confirmed, fix validated** |
| Predecessor set can be empty (cable with no REF: of its own) | Common here (see §1) — patents almost always have prior art, so this degeneracy is rare there | **Major, previously-unpredicted mismatch — this is the headline finding** |
| `wit` hardcoded to 1 | Same, unchanged | No difference — same simplification either way |
| Undefined when `nt=0` | Same condition, but likely far more common here (the base reference graph is very sparse — see `publication-cable-graph-signal`'s coverage-gap finding) | Same rule, different base rate |
| University/firm portfolio aggregates (`CDmean5`, `mCDscale5`, `CDtotal±5`) | No cable-domain analog defined yet — a per-station or per-TAGS aggregate is the natural candidate | **Undefined, not yet built** |

## 3. Time-window mismatch — tested, and the finding is more precise than the hypothesis predicted

`reference-time-lag` measured the actual gap between a citing cable and
what it references, full corpus, 2,055,547 resolved pairs: **median 6
days, mean 14.6 days, p90 40 days** (vs. a random-pair baseline median of
158 days). Real REF: resolution is essentially complete within **40 days**
for 90% of pairs. The CD-index window used by this codebase is **1825
days — roughly 45× the p90 lag, ~300× the median.**

The naive prediction from that mismatch: `cd-index-type = "nan"` should
climb steadily across 1973→1979 as more and more of each cable's nominal
5-year window falls outside the 1973-1979 corpus. **That's not what the
year-level data shows** (`cd_index_by_year_giant.csv`,
`cd_index_by_year_nongiant.csv`):

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

## 4. Direct test: the recommended ~180-day window, as actually computed

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

## 5. Overall type distribution, 1825-day window (for context)

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

## 6. Not yet tested

Hypothesis points 2-4 in `../HYPOTHESIS.md` (one-hop-predecessor chain
bias, REF:-extraction noise sensitivity, portfolio aggregates) remain
open — see that file's Caveats and Related questions.

## Reproducing

```
python3 questions/cd-index-semantics/code/cd_index_date_profile.py <graphml_path> [output_csv]
python3 questions/cd-index-semantics/code/graph_structure_by_type.py <graphml_path> [output_csv]
```

Both require the graphml path as their first argument, no default.
Outputs referenced above: `cd_index_by_year_{giant,nongiant,6month_nongiant}.csv`,
`graph_structure_by_type{,_giant}.csv`, `cd_index_content_samples.md`.
