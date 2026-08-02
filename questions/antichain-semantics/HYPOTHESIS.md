# What cable and graph properties do nodes on the antichain hold?

**Status:** answered
**Thread of:** —

**Short answer:** `antichain` is a maximum-independent-set membership flag
driven by **in-degree** (how many times a cable is cited), mechanically
unrelated to `cd-index`'s **out-degree**-driven (predecessor-count)
mechanism — yet the two correlate strongly (62% of `antichain=0` cables
are `cd-index-type: disruptive`) because both are downstream of the same
real archetype: a STATE circular that many field posts independently
reply to is simultaneously a broadcast "hub" (high in-degree → excluded
from the antichain, since including it would block all its citers from
the independent set too) and, per `cd-index-semantics`, often
`cd-index-type: disruptive` (frequently has no predecessor of its own).
Content sampling confirms this cleanly: `antichain=1` cables are
terminal, never-cited-back field-post replies; `antichain=0` cables are
STATE requests/circulars cited back by 10-200 different posts. Not
redundant with `cd-index-type` — a genuinely separate structural axis
(who cites vs. who's cited) that happens to point the same way for the
same underlying reason. See Result.

## Question

`antichain` is a precomputed node attribute (giant-component builds only)
that `publication-cable-graph-signal` and `cd-index-semantics` have both
touched without ever characterizing directly. In `cd-index-semantics` it
produced the single largest raw effect size of any attribute tested
(rank-biserial +0.501, consolidating vs. disruptive cd-index-type) but was
flagged as likely substantially mechanical — probably re-deriving the same
"does this cable have a predecessor of its own" fact that drives cd-index,
rather than telling us anything new. This question characterizes
`antichain` on its own terms: what does a node's antichain value actually
represent, mechanically and substantively (graph position, cable content,
station, subject, date), independent of cd-index?

## Hypothesis

**Revised after the first mechanical check (see below) — the original
"longest-path depth layering" guess was wrong, and disproven cheaply
before any further work was built on it, which is exactly what the Method
summary's step 1 was for:**

`antichain` turns out to be **binary** (only values `0.0`/`1.0` occur in
this build, 379,368 of 379,368 nodes, no other value and no `NaN`), not a
multi-level depth layering. A longest-path-layering would require, for
every reference edge `u→v` (u cites v, v is u's predecessor),
`antichain[v] < antichain[u]` — checked directly on all 487,904 edges: the
"violation rate" (predecessor layer ≥ citer layer) is **55.0%**, with
**45.2%** of edges having the *same* value on both ends. A real layering
would show ~0% violations. Disproven.

What actually holds, checked the same direct way: of the 487,904 edges,
**exactly 0** connect two `antichain=1` nodes (the `(1,1)` cell of the
citer×predecessor cross-tab is empty). That's the signature of a genuine
**maximum antichain** in the Dilworth/Mirsky sense — a maximum set of
pairwise-*incomparable* nodes under the DAG's reachability order; two
directly-connected nodes are trivially comparable (one reaches the other
in one hop), so no valid antichain can contain both ends of any edge, and
none do here. `antichain=1` marks membership in that set (~182,778 nodes,
48.2%); `antichain=0` is everyone else.

Revised, testable predictions:

1. **Role asymmetry**: antichain=1 nodes should skew toward *citing only*
   rather than *being cited* — a node that's frequently cited by others is
   more likely to be directly connected to (comparable with) many other
   nodes, making it harder to include in a mutually-incomparable set.
   Already checked directly: antichain=1 mean in-degree 0.26 vs. antichain=0
   mean in-degree 2.24 — a large, real asymmetry, not a subtle one.
2. **Cable-domain reading**: if (1) holds, `antichain=1` cables should read
   as *terminal citing cables* — cables that reference something (a reply,
   a follow-up) but are themselves rarely referenced back — while
   `antichain=0` cables should include the more "referenced" cables:
   predecessors, threads, and broadcast/anchor cables. Predict this
   correlates with TAGS category and station the same way `cd-index`'s
   disruptive/consolidating split did, since both attributes are plausibly
   picking up on related structural roles (citer vs. cited) — worth
   checking directly whether `antichain` and `cd-index-type` overlap
   substantially or capture genuinely different information.
3. **Graph-property profile**: given the in-degree asymmetry already
   found, predict antichain=1 also scores lower on pagerank/authority
   (both reward being cited) and possibly differently on trussness/
   coreness (a node that's rarely cited can still be embedded in a
   triangle as the *citer* corner, so the direction here is less obvious
   than for cd-index-type and worth testing rather than assuming).
4. **Indirect-reachability gap**: the direct-edge check confirms no two
   antichain=1 nodes are *directly* comparable, but a true antichain also
   requires no *indirect* (multi-hop) path between any two members — not
   checked here (would need a transitive-closure computation, expensive at
   this scale) and flagged as an open verification gap, not assumed clean.

## Data used

- External: `reftel-with-tags-estimated-CD-index-6month-2026-08-02.giant.graphml`
  (379,368 nodes) — the same giant build `cd-index-semantics` used, chosen
  for consistency and because it's the only build carrying `antichain`
  alongside the full attribute set (`degree`, `closeness`, `betweenness`,
  `pagerank`, `hub`, `authority`, `strength`, `coreness`, `cd-index`/
  `cd-index-type`, `community-leiden`, edge `trussness`/`edge-betweenness`).
  Filename only, not the full external path — see `data/external/README.md`
  for how this repo documents external data dependencies.
- Code: `code/antichain_profile.py` — question-exclusive, loads a graphml
  directly (path required, no default — same convention established in
  `publication-cable-graph-signal`/`cd-index-semantics`), verifies what
  `antichain` actually is mechanically (done — see Hypothesis) and profiles
  the resulting two groups (`antichain=0` vs. `antichain=1`) by graph
  properties, TAGS, station, year, and overlap with `cd-index-type`.

## Method summary

1. ~~Verify hypothesis 1~~ — done directly in the Hypothesis section above:
   the longest-path-layering guess was checked against all 487,904 edges
   and disproven (55.0% violation rate); the maximum-antichain
   (independent-set) reading was checked the same way and confirmed (0 of
   487,904 edges connect two `antichain=1` nodes).
2. Two-group population-scale comparison (`antichain=0` vs. `antichain=1`),
   same generic auto-detected-attribute + Mann-Whitney/rank-biserial
   approach as `cd-index-semantics`'s `graph_structure_by_type.py`: every
   numeric node attribute, plus edge-derived trussness and
   neighbor-community-sharing.
3. Cross-tabulate against `cd-index-type` directly — does `antichain`
   carry information beyond what `cd-index-type` already captures, or are
   they substantially the same split under two names?
4. TAGS-category, station, and year composition per group.
5. Read a content sample (`message_preview`) of each group to sanity-check
   the "terminal citer vs. cited/thread cable" reading against real cable
   text.

## Result

### 1. Mechanism: in-degree-driven, not out-degree-driven — genuinely different from cd-index

`antichain=0` n=196,590 (51.8%), `antichain=1` n=182,778 (48.2%). Full
numbers: `results/antichain_numeric_comparison.csv`.

| metric | antichain=0 mean | antichain=1 mean | effect | interpretation |
|---|---|---|---|---|
| in_degree | 2.238 | 0.262 | −0.760 (largest of any metric) | antichain=0 = frequently cited |
| out_degree | 1.366 | 1.201 | −0.025 (negligible) | **not** driven by predecessor count |
| pagerank | (higher) | (lower) | −0.829 | tracks in-degree, as expected |
| coreness | 1.834 | 1.295 | −0.423 | antichain=0 more core-embedded |
| trussness_mean | 2.423 | 2.173 | −0.286 | antichain=0 higher — **opposite** of `cd-index`'s consolidating/disruptive trussness direction |

The out-degree near-parity is the key result: unlike `cd-index-type`
(driven by whether the focal cable has a predecessor of its own —
out-degree), `antichain` group membership is essentially unrelated to a
cable's own out-degree and almost entirely explained by in-degree. This
is exactly what maximum-independent-set selection over a graph does
mechanically: a high-in-degree hub conflicts (is directly comparable)
with every one of its citers, so an optimal maximum antichain packs in
many low-in-degree "leaf" nodes instead and excludes hubs. Confirmed
directly (see Hypothesis): 0 of 487,904 edges connect two `antichain=1`
nodes.

### 2. Correlates with cd-index-type, but isn't the same mechanism

| | consolidating | disruptive | undefined |
|---|---|---|---|
| antichain=0 | 25.6% | **62.3%** | 12.1% |
| antichain=1 | **57.5%** | 14.2% | 28.3% |

A real, strong correlation — but §1 already shows *why* it isn't
redundancy: `cd-index-type` is driven by out-degree (predecessor
existence), `antichain` by in-degree (citation count), and the two only
happen to align because the same cable archetype (a STATE circular with
no predecessor of its own, cited by dozens of independent posts) scores
high on both "disruptive" and "excluded from the antichain" for two
different reasons. The trussness direction is the clearest evidence
they're not the same signal: `cd-index-semantics` found *consolidating*
cables have higher trussness than disruptive; here, `antichain=0`
(correlated with disruptive) has *higher* trussness than `antichain=1`
(correlated with consolidating) — the opposite pairing. If `antichain`
were just relabeling `cd-index-type`, the trussness direction would match
its correlated cd-index-type bucket; it doesn't.

### 3. TAGS / station / year: no topical or temporal skew, mild station concentration

Top 15 TAGS codes are nearly identical between groups, same rank order
within noise (US, PFOR, ETRD, PORG, EFIN, ENRG, UR, OVIP, PEPR, EAID,
SREF, GE, BEXP — see `results/antichain_top_tags.csv`) — `antichain`
membership doesn't track subject matter. Year distribution is flat and
proportional across both groups, tracking overall corpus volume per year
(`results/antichain_by_year.csv`) — not a temporal effect either. Station
concentration is mild: STATE is the top station in both groups but a
larger share of `antichain=0` (31.7%) than `antichain=1` (21.9%)
(`results/antichain_top_stations.csv`) — consistent with STATE
disproportionately originating the broadcast circulars that drive
`antichain=0` membership (see §4), not a station-specific pattern beyond
that.

### 4. Content sample confirms the mechanism directly

`results/antichain_content_samples.md`. `antichain=1`, in-degree-0
sample: small field posts (San Salvador, San Jose, New Delhi, Cairo,
Manila, Jeddah), each citing exactly one prior cable, never cited back —
routine, self-contained replies (consular packages, business holidays,
visa issues). `antichain=0`, in-degree≥10 sample: STATE-originated
circulars cited back by 10-197 different posts — "Legal representation
available to Americans arrested abroad," "1978 Country Reports of Human
Rights Practices" (a substantively significant series), "Word processing
policy and procedures" (not one). Same caveat as `cd-index-semantics`
found for "disruptive": `antichain=0` tracks *being a widely-replied-to
hub*, not historical importance — the sample includes both a genuinely
significant recurring report series and purely administrative circulars
side by side.

## Caveats / limitations

- **Indirect-reachability not verified** (Hypothesis point 4): the direct-
  edge check (0 of 487,904 edges connect two `antichain=1` nodes) confirms
  local independent-set validity but not full transitivity — two
  `antichain=1` nodes could in principle still be connected by a 2+ hop
  path through an `antichain=0` intermediary, which would make them
  comparable and violate true antichain membership. Not checked (would
  need a transitive-closure computation, expensive at 379K nodes) — the
  mechanical story here should be read as "strongly supported by the
  direct-edge evidence," not "exhaustively proven."
- Single build tested (the giant 6-month CD-index build) — `antichain` is
  giant-component-only across every build seen in this repo so far, so
  there's no non-giant cross-check available the way `cd-index-semantics`
  had. Whether the in-degree-driven mechanism replicates on a different
  giant build (e.g. the earlier `2026-08-01`/`2026-08-02` `-attr` builds)
  isn't tested here.
- The TAGS/station comparison uses raw code frequency, not
  publication-count-normalized or statistically tested (no Mann-Whitney
  here, just descriptive top-15 tables) — real but small differences
  (e.g. the STATE share gap) aren't formally tested for significance the
  way the numeric graph properties are.
- Content sample is small (7 cables per group, 1 filter each) — enough to
  confirm the mechanism is real and matches the numeric story, not enough
  to characterize edge cases (e.g. what an `antichain=1` cable with
  moderately high out-degree, not just 1-2, looks like).

## Related questions

- [`cd-index-semantics`](../cd-index-semantics/HYPOTHESIS.md) — found the
  largest raw effect of any attribute on `antichain` and suspected it was
  mechanically entangled with predecessor count (out-degree); this
  question tested that directly and found the opposite — `antichain` is
  driven by in-degree, a genuinely different mechanism from `cd-index`'s
  out-degree-driven one, that happens to correlate for a real underlying
  reason (see Result §1-2). `cd-index-semantics`'s own predecessor-count
  control on trussness/coreness should be read alongside this: those
  tests controlled for out-degree, not in-degree, so they remain valid on
  their own terms.
- [`publication-cable-graph-signal`](../publication-cable-graph-signal/HYPOTHESIS.md) —
  first introduced `antichain` to this repo's analyses (as "mainstream vs.
  minor chain" layering) but never characterized what the layers actually
  contain.
- [`reference-graph-structure`](../reference-graph-structure/HYPOTHESIS.md) —
  shares the same base reference graph.
