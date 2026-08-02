# What is the time gap between a cable and the cable(s) it references, and does it differ by station?

**Status:** answered
**Thread of:** —

## Question

When one cable references another (a `REF:` line resolving to another
document's MRN), how many days elapse between the cited cable's date and the
citing cable's date? Does that gap differ by the citing document's
originating station — in particular, does STATE (the Department itself,
~29% of the corpus, sending outgoing instructions rather than field
reporting) behave differently from field posts?

## Hypothesis

Most references are to recent, still-live traffic (a post replying to or
following up on a cable from the last few days/weeks), so the lag
distribution should be tight and right-skewed (a short median, a long tail
for pulling up older precedent), and dramatically shorter than the gap
between two randomly paired documents drawn from the whole 7-year corpus.
STATE was expected to behave differently from field posts, plausibly with a
wider spread, since it is a single desk-driven hub referencing/being
referenced across a much broader range of traffic than a single embassy's
own reporting stream.

## Data used

- External: `data/cable-extract/<year>.reftel.norm.ndjson` (`document_number`
  -> `date`, `extracted_references`) from the sibling `acp-127` repo (see
  `data/external/README.md`) — no local copy checked into this repo.
- Shared: `lib/station.py` (`parse_station`), parses the originating station
  from `document_number` — also used by
  [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md)
  and [`address-reference-similarity`](../address-reference-similarity/HYPOTHESIS.md)
  for their STATE/non-STATE breakdowns.
- Code: `code/reference_time_lag.py` (question-exclusive).

## Method summary

- Load `document_number -> (date, extracted_references)` for all 7 years
  combined (references cross year boundaries) — the same join key and
  reference field used by the other two reference-similarity questions.
- For every citing document with a date and >=1 reference, and each
  reference that resolves to an in-corpus document with its own date,
  compute `lag_days = citing.date - cited.date`.
- Report the distribution (mean, median, stdev, p10/p25/p75/p90, % negative
  — a data-quality flag, since a cable referencing a "future" cable
  indicates a bad date or a bad reference resolution) three ways:
  overall, STATE vs. non-STATE vs. unknown-station, and a full per-station
  table (stations meeting a minimum pair-count threshold, ranked by volume).
- Null baseline: for every resolved actual reference, pair the same citing
  document with one random other dated document from the whole pool instead,
  and compute the same gap — same method shape as the other two
  reference-similarity questions' random-pair baseline, adapted to a
  continuous day-gap instead of a Jaccard score.

## Result

Answered — yes, the lag is real and tight. Overall median lag is 6 days
(mean 14.6d, heavily right-skewed: p90 = 40 days), versus a random-pair
baseline with median 158 days and enormous spread (stdev 933, 43.5%
*negative* — i.e., a random "citing" doc's date often falls before the
random "cited" doc's, which is meaningless for a real reference and exactly
what should happen for an arbitrary pair). Only 2.7% of actual reference
pairs show a negative lag, a small residual of bad dates/reference
resolution rather than a broken hypothesis.

**STATE does not behave dramatically differently from field posts as a
whole** — contrary to the hypothesis, STATE's median (6d) and non-STATE's
median (5d) are close, and STATE's mean (14.4d) sits right in the same range
as most individual field posts. What *does* vary substantially is
station-to-station: some posts (USUNNEWYORK: 3d median, GENEVA/CAIRO/TELAVIV:
~3-4d) resolve references much faster than others (CARACAS: 7d/21.3d mean,
BRUSSELS: 7d/22.0d mean, ATHENS: 19.6d mean with a notably long tail/high
stdev). This is more consistent with per-post operational tempo and
recordkeeping style (a subject for further investigation) than with a
"STATE hub vs. everyone else" split. Full write-up:
`results/reference_time_lag.md`.

## Caveats / limitations

- `date` in `reftel.norm.ndjson` falls back from DTG to Draft Date when DTG
  is unavailable (`date_source`); a small share of dates are therefore
  drafted rather than transmitted dates, which could shift lag by a few days
  in either direction for that subset.
- Station is parsed from `document_number` (see `lib/station.py`); ~8% of
  document numbers don't resolve to a recognized station (garbled/unusual
  abbreviations) and are excluded from the per-station table (they still
  count in the overall and "unknown station" rows).
- The 2.7% negative-lag rate is a floor on the combined error rate of dating
  and reference resolution, not necessarily attributable to either alone.

## Related questions

- [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md) —
  same reference-edge join and citing/cited pair construction, applied to
  TAGS overlap instead of time.
- [`address-reference-similarity`](../address-reference-similarity/HYPOTHESIS.md) —
  same reference-edge join, applied to routing/addressing metadata; also
  uses `lib/station.py` for its own STATE/non-STATE breakdown.
- [`filing-time-vs-dtg`](../filing-time-vs-dtg/HYPOTHESIS.md) — a different
  time-lag question (filing_time vs. DTG within a single cable, 1976-1979
  only), not to be confused with this one (citing cable vs. cited cable,
  full corpus).
