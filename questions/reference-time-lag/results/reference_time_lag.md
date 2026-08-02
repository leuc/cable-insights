# Time gap between a cable and the cable(s) it references, by station

**Question:** when one cable references another, how many days elapse
between the cited cable's date and the citing cable's date, and does the gap
differ by the citing document's originating station — in particular,
STATE vs. field posts?

**Answer: the lag is real and tight (median 6 days, vs. 158 for a random
pair), but STATE is not the outlier the hypothesis expected** — its
distribution sits in the same range as most field posts. Station-to-station
variation is real and larger than the STATE/non-STATE split, with some posts
(USUNNEWYORK, GENEVA, CAIRO, TELAVIV) resolving references markedly faster
than others (CARACAS, BRUSSELS, ATHENS).

Script: [`code/reference_time_lag.py`](../code/reference_time_lag.py).

## Method

1. **Join.** `data/cable-extract/<year>.reftel.norm.ndjson`
   (`document_number -> date, extracted_references`) loaded for all 7 years
   combined — the identical join key and reference field used by
   `tags-reference-similarity` and `address-reference-similarity`.
2. **Citing/cited pairs.** For every dated document with >=1 reference
   ("citing"), each reference resolving to an in-corpus dated document
   ("cited") forms one pair; `lag_days = citing.date - cited.date`.
3. **Station.** Parsed from `document_number` via `lib.station.parse_station`
   (2-digit year + station name + serial, e.g. `73BAGHDAD339` -> `BAGHDAD`).
   ~8% of document numbers don't resolve to a recognized station (garbled or
   unusual abbreviations) — these still count in the overall/unknown-station
   rows but are excluded from the per-station table.
4. **Null baseline.** For every resolved actual reference, the same citing
   document is also paired with one random other dated document from the
   whole pool, and the same day-gap computed — an apples-to-apples same-size
   control, same method shape as the other two reference-similarity
   questions' random-pair baseline.

Run: `python3 questions/reference-time-lag/code/reference_time_lag.py --seed 42 --top-stations 30 --min-station-n 500`.

## Full-corpus result (all years 1973-1979, `--seed 42`, no sampling)

- 1,136,509 citing documents (dated, with ≥1 reference).
- 924,094 (81.3%) have at least one reference that resolves to an in-corpus
  dated document — matching the resolution rate found by the other two
  reference-similarity questions, as expected (same reference graph).
- 2,649,583 total reference pairs; 2,055,547 (77.6%) resolved.

### Overall: actual vs. random-pair baseline

| | n | mean | median | stdev | p10 | p25 | p75 | p90 | negative % |
|---|---|---|---|---|---|---|---|---|---|
| actual | 2,055,547 | 14.6d | 6.0d | 53.6 | 1 | 2 | 15 | 40 | 2.73% |
| random baseline | 2,055,547 | 154.4d | 158.0d | 932.6 | -1099 | -498 | 832 | 1398 | 43.45% |

Real references are tight and near-term (three-quarters resolve within 15
days, 90% within 40) with only a small residual (2.7%) of negative-lag pairs
— cables that appear to reference a "future" document, which is a
data-quality floor (bad date or bad reference resolution), not a broken
hypothesis. A random pair of documents shows both a much wider spread
(stdev in the hundreds of days) and a *positive* mean shifted well off zero
(the corpus has more documents in later years, so a random comparison document
skews earlier on average) with a large negative share (43.45%) that would be
meaningless for a real reference — exactly the contrast expected between
"cites recent, live traffic" and "arbitrary pair from a 7-year corpus."

### STATE vs. non-STATE vs. unknown station

| | n | mean | median | stdev | p10 | p25 | p75 | p90 | negative % |
|---|---|---|---|---|---|---|---|---|---|
| STATE | 548,963 | 14.4d | 6.0d | 51.9 | 1 | 2 | 17 | 41 | 2.37% |
| non-STATE | 1,422,483 | 14.8d | 5.0d | 54.0 | 1 | 2 | 15 | 39 | 2.82% |
| unknown station | 84,101 | 12.5d | 4.0d | 58.7 | 1 | 1 | 12 | 32 | 3.52% |

**This does not support the hypothesis's specific STATE-as-outlier
prediction.** STATE's median (6d) and mean (14.4d) are close to non-STATE's
(5d / 14.8d) — a one-day difference in median either way, well within the
noise of station-to-station variation shown below. Being the single
Department-wide hub does not measurably widen or shift STATE's reference
lag relative to the field-post aggregate.

### Per-station breakdown (top 30 by pair count, min 500 pairs; 173 of 208 stations met the threshold)

| station | n | mean | median | stdev | p90 |
|---|---|---|---|---|---|
| STATE | 548,963 | 14.4d | 6.0d | 51.9 | 41 |
| GENEVA | 45,621 | 9.9d | 4.0d | 42.8 | 28 |
| MOSCOW | 45,317 | 16.1d | 6.0d | 53.9 | 39 |
| PARIS | 44,920 | 12.5d | 5.0d | 47.5 | 36 |
| BONN | 43,011 | 17.2d | 6.0d | 70.7 | 44 |
| LONDON | 37,931 | 10.5d | 4.0d | 44.8 | 28 |
| CAIRO | 35,494 | 9.5d | 3.0d | 49.7 | 27 |
| TOKYO | 33,545 | 12.6d | 6.0d | 48.0 | 36 |
| USUNNEWYORK | 30,506 | 6.3d | 3.0d | 41.2 | 21 |
| ROME | 29,190 | 13.0d | 5.0d | 46.1 | 36 |
| MANILA | 24,631 | 15.3d | 6.0d | 54.9 | 40 |
| BANGKOK | 24,376 | 14.8d | 5.0d | 53.3 | 43 |
| BRUSSELS | 23,342 | 22.0d | 7.0d | 65.0 | 60 |
| NEWDELHI | 20,431 | 10.6d | 5.0d | 46.8 | 33 |
| SEOUL | 20,227 | 16.1d | 5.0d | 49.0 | 42 |
| TELAVIV | 19,995 | 10.6d | 3.0d | 42.8 | 28 |
| TEHRAN | 19,975 | 15.2d | 5.0d | 60.1 | 37 |
| MEXICOCITY | 19,505 | 15.8d | 6.0d | 53.6 | 45 |
| LAGOS | 19,212 | 15.1d | 6.0d | 45.2 | 42 |
| ATHENS | 17,944 | 19.6d | 5.0d | 70.0 | 49 |
| ANKARA | 16,291 | 15.8d | 5.0d | 57.1 | 40 |
| BUCHAREST | 16,169 | 16.7d | 7.0d | 53.5 | 43 |
| CARACAS | 16,135 | 21.3d | 7.0d | 67.6 | 58 |
| MADRID | 16,066 | 14.7d | 6.0d | 48.6 | 40 |
| BRASILIA | 15,793 | 17.8d | 7.0d | 57.0 | 48 |
| VIENNA | 15,709 | 17.6d | 7.0d | 60.1 | 51 |
| JEDDAH | 15,689 | 13.2d | 5.0d | 45.2 | 35 |
| WARSAW | 15,540 | 14.9d | 6.0d | 51.9 | 40 |
| LIMA | 15,374 | 16.9d | 6.0d | 55.9 | 42 |
| OTTAWA | 15,046 | 12.6d | 5.0d | 54.4 | 41 |

Full run output (`--seed 42`, `--top-stations 30 --min-station-n 500`, see
script for the complete 173-station table): the fastest-resolving posts by
median are USUNNEWYORK (3d), CAIRO (3d), and TELAVIV (3d); the slowest by
mean are BRUSSELS (22.0d), CARACAS (21.3d), and ATHENS (19.6d, with the
widest stdev of the top 30 at 70.0), suggesting some posts sit on cables
longer before circling back to reference them, or reference older precedent
more often, rather than a uniform corpus-wide tempo.

## Conclusion

The core hypothesis holds: cable references are overwhelmingly to recent,
still-live traffic (median 6 days; p90 = 40 days), a dramatically tighter
and more consistent pattern than a random pair of documents from the 7-year
corpus (median 158 days, 43.5% meaninglessly "negative"). **The specific
STATE-as-outlier prediction does not hold** — STATE's lag distribution is
essentially indistinguishable from the field-post aggregate (6d vs. 5d
median). The more interesting structure is station-to-station: individual
posts vary meaningfully in how quickly they resolve references (3d medians
at USUNNEWYORK/CAIRO/TELAVIV vs. 7d+ means with long tails at
BRUSSELS/CARACAS/ATHENS), which looks like a per-post operational-tempo
signal rather than a Department-vs-field split, and is a plausible target
for a follow-up question.

## Reproducing

```bash
# quick sanity check (single year, small sample)
python3 questions/reference-time-lag/code/reference_time_lag.py --years 1973 --sample 2000 --seed 42

# full corpus, all years, top-30 station table
python3 questions/reference-time-lag/code/reference_time_lag.py --seed 42 --top-stations 30 --min-station-n 500
```
