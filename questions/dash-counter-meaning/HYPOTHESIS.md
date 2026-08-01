# What does the dash-counter line mean?

**Status:** answered
**Thread of:** —

## Question

Every cable header carries an unlabeled line between the drafting/clearance
signoff block and the DTG line — a pair of digit groups with no caption in
ACP-127(G) itself. What does it represent, and what can it tell us about the
corpus as a whole (volume, completeness, gaps)?

## Hypothesis

The dash-counter line is not per-cable or per-station bookkeeping but a
single shared tape-relay transmission sequence — i.e. one continuous counter
that every message passing through the relay increments, regardless of
origin/destination station.

## Data used

- Source: `data/source/sas_totals_from_foia.csv` (FOIA/MuckRock SAS totals,
  cross-check), plus `docs/acp127g.txt` and `docs/faqs.txt` from the sibling
  `acp-127` repo (protocol/field reference — see `data/external/README.md`)
- Derived: `data/derived/transmission_volume.csv` (shared per-cable ledger)
- Code: `lib/build_transmission_volume.sh` + `lib/transmission_volume.jq`
  (shared, builds the ledger) and `code/hourly_accounted.py`
  (question-exclusive)

## Method summary

- Extract and correctly parse the dash-counter's two digit groups (`counter`,
  `filing_time`) across the full 2,081,272-document corpus.
- Sort every counter-bearing document by (date, station) to test whether the
  counter behaves as per-station or shared/global.
- Compare "volume implied by the counter's range" against "documents that
  actually survive in this archive" per day/month/year.
- Cross-check the resulting gap-in-coverage dates against Souza, Coelho,
  Shah & Connelly (2016) (arXiv:1611.00356) and against FOIA-reported SAS
  per-year totals.

## Result

Answered: the counter is a single shared tape-relay sequence, not per-cable
or per-station. STATE accounts for 28.7% of counter-bearing records; the
counter's implied volume is ~60-165x larger than what survives declassified.
Cross-checking against Souza et al. (2016) confirms their four named
text-removal date ranges and surfaces additional undocumented gaps/spikes
with precise dating, plus a FOIA-vs-corpus ratio showing declassification
coverage shrinking over the decade (1.45x → 2.27x). Full write-up:
`results/dash_counter_stats.md`. Published visual summary: [The Shared
Counter — ACP-127 Tape Relay Stats](https://claude.ai/code/artifact/71e5012f-8dcc-4990-ab7c-df727ff41142)
(saved locally as `results/dash_counter_stats.html`).

## Caveats / limitations

What the implied ~100-160x excess volume actually represents (e.g. traffic
beyond State Dept cables passing through the same relay) is explicitly
flagged in the write-up as **not established** — the current analysis
doesn't support a conclusion there, only the volume ratio itself.

## Related questions

- [`filing-time-vs-dtg`](../filing-time-vs-dtg/HYPOTHESIS.md) — split out from
  this investigation as a narrower, secondary finding about the
  `filing_time` subfield specifically.
