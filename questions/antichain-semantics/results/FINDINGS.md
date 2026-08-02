# Findings: what cable and graph properties do nodes on the antichain hold?

**Status:** answered. Full grounding, hypothesis (including the mechanical
disproof of the original "depth layering" guess), and methodology live in
[`../HYPOTHESIS.md`](../HYPOTHESIS.md) — this file is the detailed
write-up its Result section points to.

## 1. Mechanism: in-degree-driven, not out-degree-driven — genuinely different from cd-index

`antichain=0` n=196,590 (51.8%), `antichain=1` n=182,778 (48.2%). Full
numbers: `antichain_numeric_comparison.csv`.

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
directly (see `../HYPOTHESIS.md`'s Hypothesis section): 0 of 487,904
edges connect two `antichain=1` nodes.

## 2. Correlates with cd-index-type, but isn't the same mechanism

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

## 3. TAGS / station / year: no topical or temporal skew, mild station concentration

Top 15 TAGS codes are nearly identical between groups, same rank order
within noise (US, PFOR, ETRD, PORG, EFIN, ENRG, UR, OVIP, PEPR, EAID,
SREF, GE, BEXP — see `antichain_top_tags.csv`) — `antichain`
membership doesn't track subject matter. Year distribution is flat and
proportional across both groups, tracking overall corpus volume per year
(`antichain_by_year.csv`) — not a temporal effect either. Station
concentration is mild: STATE is the top station in both groups but a
larger share of `antichain=0` (31.7%) than `antichain=1` (21.9%)
(`antichain_top_stations.csv`) — consistent with STATE
disproportionately originating the broadcast circulars that drive
`antichain=0` membership (see §4), not a station-specific pattern beyond
that.

## 4. Content sample confirms the mechanism directly

`antichain_content_samples.md`. `antichain=1`, in-degree-0
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

## Reproducing

```
python3 questions/antichain-semantics/code/antichain_profile.py <graphml_path> [output_dir]
```

Requires the graphml path as its first argument, no default (needs a
giant-component build with `antichain`). Outputs referenced above:
`antichain_numeric_comparison.csv`, `antichain_vs_cdindextype.csv`,
`antichain_top_tags.csv`, `antichain_top_stations.csv`,
`antichain_by_year.csv`, `antichain_content_samples.md`.
