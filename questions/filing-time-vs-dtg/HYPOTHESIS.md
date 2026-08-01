# How does `filing_time` relate to DTG?

**Status:** answered
**Thread of:** [`dash-counter-meaning`](../dash-counter-meaning/HYPOTHESIS.md)

## Question

The dash-counter line's `filing_time` subfield (present only from the
Dec-1976 format change onward) records when a message was handed to the
relay for transmission — distinct from DTG, when the message was
drafted/dated by the originating post. How do the two relate, and does the
relationship change over time?

## Hypothesis

`filing_time` is always at-or-after DTG (a message can't be filed for
transmission before it's drafted), and any lag between them is not constant
— it plausibly grows as cable volume grows over the corpus's years.

## Data used

- Derived: `../dash-counter-meaning/results/dash_counter_daily_comparison.csv`-adjacent
  counter/filing_time pairs (computed inline from `data/derived/transmission_volume.csv`
  parsing, not a checked-in intermediate CSV)
- Code: none question-exclusive — the analysis was run inline as part of the
  broader dash-counter investigation, not as a separate checked-in script

## Method summary

- Restrict to the 6,805 usable (`counter`, `filing_time`) pairs, 1976-1979
  only (the field doesn't exist pre-Dec-1976).
- Compute the lag distribution (percentiles) per year.
- Track the share of cables filed <1hr before DTG (sanity check: should be
  near zero) and the share filed >24hr after DTG (backlog/refile indicator).

## Result

Answered: filing_time is essentially never earlier than DTG (≤0.4% of pairs
every year). The lag and its tail both grow steadily: cables filed >24hr
after their DTG rose from 5.7% (1977) to 30.3% (1979) — consistent with
either a worsening real transmission backlog as volume grew, or a rising
share of refiled/retransmitted messages (whose filing_time is the refile
event, not the original one). Full write-up: `results/dash_counter_filing_lag.md`.

## Caveats / limitations

Pre-1976 documents have no `filing_time` at all (format didn't include it
yet), so this is a 1976-1979-only analysis — the full 1973-1979 dash-counter
picture is in the parent question.

## Related questions

- [`dash-counter-meaning`](../dash-counter-meaning/HYPOTHESIS.md) — parent
  investigation this was split out from.
