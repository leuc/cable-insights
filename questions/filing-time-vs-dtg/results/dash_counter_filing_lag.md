# `filing_time` vs. DTG: always at-or-after, with a growing lag over the years

Split out from [`dash_counter_stats.md`](../../dash-counter-meaning/results/dash_counter_stats.md) — this is a narrower,
secondary finding about the `filing_time` field specifically (present only from the
Dec-1976 format change onward), not part of the core counter/gap-analysis story.

Per ACP-127(G) §115/§116 (`docs/acp127g.txt:601-621`), format line 3 ("Message
Identification") is *routing indicator + station serial number + filing time*.
`filing_time` is the `Z`-tagged group in the dash-counter line — the date/time a message
was received by the communications centre for transmission (§115 "FILING TIME/TIME
HANDED IN"), as opposed to the DTG, which is when the message was drafted/dated by the
originating post.

## Result

Computed across 6,805 usable pairs (1976-1979; `filing_time` doesn't exist before the
Dec-1976 format change):

| Year | n | p5 | p25 | median | p75 | p95 | filed <1hr before DTG | >24hr lag |
|---|---|---|---|---|---|---|---|---|
| 1976 | 38 | 8 | 43 | 95 | 674 | 7,582 | 2.6% | 5.3% |
| 1977 | 2,154 | 14 | 59 | 200 | 595 | 1,421 | 0.4% | 5.7% |
| 1978 | 2,322 | 11 | 53 | 266 | 978 | 2,566 | 0.2% | 16.6% |
| 1979 | 2,290 | 11 | 55 | 316 | 2,156 | 4,282 | 0.2% | 30.3% |

(minutes; "filed before DTG" is ≤0.4% every year — filing_time is essentially never
earlier than the DTG, exactly as expected for "time handed in for transmission.")

The lag and its tail both grow steadily year over year — the share of cables filed more
than a day after their DTG nearly triples (5.7% → 30.3%) from 1977 to 1979. Consistent
with either a worsening real transmission backlog as volume grew, or (per ACP-127 §115)
an increasing share of refiled/retransmitted messages, whose filing_time is the refile
event, not the original one.

## Caveat

Pre-1976 documents have `counter` but no `filing_time` (format didn't include it yet), so
this analysis is 1976-1979 only — see `dash_counter_stats.md` for the counter-only
analysis that covers the full 1973-1979 range.
