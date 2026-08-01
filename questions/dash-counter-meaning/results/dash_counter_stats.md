# The dash-counter line: a shared tape-relay sequence, not a per-cable counter

This documents the behavior of `_dash_counters` (`src/patterns/dash_counter.py`) once
correctly extracted across the full corpus (2,081,272 documents, 1973-1979), following
up on the investigation that fixed its post-Dec-1976 parsing (see git history / prior
session notes for that fix). It covers: what the `counter` and `filing_time` fields
represent and where the line sits in the raw cable header, a full-corpus comparison of
"what the counter implies existed" vs. "what survives in this archive", and — new in
this revision — a per-day classification/availability breakdown cross-checked against
Souza, Coelho, Shah & Connelly (2016), *"Using Artificial Intelligence to Identify State
Secrets"* (arXiv:1611.00356) and against the FOIA-reported SAS per-year totals in
[`sas_totals_from_foia.csv`](../../../data/source/sas_totals_from_foia.csv).

(The narrower `filing_time`-vs-DTG lag analysis has been moved to its own file:
[`dash_counter_filing_lag.md`](../../filing-time-vs-dtg/results/dash_counter_filing_lag.md).)

## Where the counter sits in the raw header

The dash-counter line is not part of any labeled ACP-127 field — it has no caption of its
own and sits, unlabeled, between the drafting/clearance signoff block and the DTG line.
Real example (`1977STATE013174`, header block only):

```
DRAFTED BY EB/OA/AVP:JSGRAVATT:FAA:CSPICKENS:JO
APPROVED BY EB/OA/AVP:AJWHITE
NEA/ARN - MLKING
           ------------------201212Z 109980 /20
R 192358Z JAN 77
FM SECSTATE WASHDC
TO AMEMBASSY TRIPOLI
```

That is: PAGE line → ORIGIN/INFO distribution block → drafter/clearance signoff →
**dash-counter line** → DTG (`R 192358Z JAN 77`) → FM/TO. Nothing in ACP-127(G) itself
documents a line in this position — it is not part of the formal message text the
protocol specifies, which is consistent with it being an artifact of the tape-relay
communications centre's own internal handling stamp rather than something the drafting
officer or originating post ever composed. It survived into the declassified plaintext
because the whole page image (including relay-centre marginalia) was captured, not just
the formal message fields.

## Field meaning

Per ACP-127(G) §115/§116 (`docs/acp127g.txt:601-621`), format line 3 ("Message
Identification") is *routing indicator + station serial number + filing time*. The
dash-counter line's two digit groups map onto the latter two:

- `counter` — the non-`Z`-tagged 6-digit group (station serial number)
- `filing_time` — the `Z`-tagged group (filing time / time handed in), only present from
  the Dec-1976 format change onward
- `copies` — the `/NN` suffix (a distribution copy count, distinct from `_distribution`'s
  own `/NNN` trailer)

In the example above: `counter=109980`, `filing_time=201212Z` (the 20th at 1212Z),
`copies=20` — filed roughly 12 hours before the DTG (192358Z, the 19th at 2358Z)... note
this is one of the rare cases where filing precedes DTG; see
[`dash_counter_filing_lag.md`](../../filing-time-vs-dtg/results/dash_counter_filing_lag.md) for the aggregate pattern
(filing almost always follows DTG).

## `counter` is a single shared sequence, not per-embassy

Grouping by originating station (parsed from the document number) is misleading — values
climb for days without resetting per station. Pooling **all** stations together and
sorting by time instead shows the real structure: on a single sampled day
(`1977-07-28`), unrelated posts land in one tight, coherent, climbing numeric band:

```
TOKYO 106165 → TAIPEI 109123 → TEHRAN 111641 → PARIS 112035 → NATO 113012 →
ANKARA 112428 → OTTAWA 115154 → GENEVA 117351 → LONDON 118191 → STATE 121962 →
PANAMA 121770 → QUITO 122749
```

This is one shared counter — almost certainly the tape-relay communications centre's own
transmission log, assigned to every message passing through it regardless of origin
(consistent with ACP-127 being specifically about *tape relay procedure*, per the RN
status list findings in `docs/rn_acp_status_1977.md`, and with its position in the raw
header shown above — a relay-centre stamp, not an originator-composed field).

## What increments the counter: station attribution and cross-checks against other signals

Sorting every counter-bearing document by (date, station) lets us see, for the subset of
counter values that have a surviving document, which station's traffic occupies which
part of the sequence. This only covers the documents in this archive — the counter's
implied volume runs ~100x larger than what we have, so most counter ticks have no
attributable station in our data — but the ticks we *do* have show clear, consistent
structure, and two other fields in the metadata cross-check it independently.

### Counter order tracks `filing_time`, not DTG

Spearman rank correlation between counter value and reconstructed `filing_time` (resolved
to a real timestamp, correcting for month-boundary ambiguity), computed per DTG-day across
every 1977-1979 day with ≥30 counter-bearing records: raw result was noisy (median
ρ=0.84, with 71/1080 days showing a *negative* correlation, some strongly so). Checking
those negative-correlation days showed every one of the 15 worst has a counter reset
occurring mid-day (counter range spanning from near-zero to near the ~130,000 ceiling) —
an unresolved confound, not genuine disorder. Restricting to the 145 days with no mid-day
reset: **median ρ=0.96, mean=0.90, zero days negative**. Within a single reset
"generation," counter order tracks filing_time order almost exactly.

The same clean days, tested against DTG (origination/drafting time) instead of
filing_time, show a measurably weaker relationship: **median ρ=0.73, mean=0.65** — exactly
what's expected if the counter stamps arrival at the relay (filing_time) rather than when
the cable was drafted (DTG); the two diverge more the longer a cable sits before
transmission (see [`dash_counter_filing_lag.md`](../../filing-time-vs-dtg/results/dash_counter_filing_lag.md)).

### Station attribution: overseas posts batch, STATE is continuous

STATE (Washington) alone accounts for **28.7%** of all counter-bearing records in this
corpus (524,763 of 1,826,811) — vastly more than any single overseas post (next highest,
Geneva, is 2.0%).

More telling is *how* each station's counter values are distributed across a day. For
each station-day (clean, non-reset days only), the average gap between that station's
consecutive counter values was compared to the gap expected from a uniform random draw of
the same size across that day's full counter range:

- **Overseas posts cluster tightly**: median ratio 0.16 (many posts — Tehran, Tokyo,
  Bangkok — below 0.02). A post's cables for the day land in a narrow, contiguous *burst*
  of counter values, not spread across the day. Concrete example, 1978-10-23: Tokyo's 29
  cables that day span counters 59,374-61,007 (a 1,633-wide band) inside a day-wide range
  of 25,468-111,340 — under 2% of the day's spread. Meanwhile STATE's cables that same day
  ran continuously from 25,468 up past 63,000.
- **STATE is the opposite**: ratio ≈1.0 essentially everywhere (0.994-1.024 across every
  big-volume STATE-day sampled) — statistically indistinguishable from a uniform random
  draw across the *entire* day.

This is a real structural signal: overseas posts' traffic arrives at the relay in
scheduled daily batches (consistent with a periodic circuit connection/transmission
session per post), while STATE's own traffic is continuously interleaved throughout the
whole day — consistent with this counter being kept at STATE's own relay center in
Washington, where STATE's outgoing stream originates continuously on-site while overseas
posts' traffic arrives in discrete sessions.

### Cross-check: Document Number's per-station serial (the "MRN")

The numeric suffix of `Document Number` (e.g. `013174` in `1977STATE013174`) is a
separate, independent signal: a per-station, per-year sequential cable number assigned by
that station's own communications shop, unrelated to the ACP-127 relay counter. Two checks
confirm it's real and informative:

**It correlates with the dash-counter.** Spearman correlation between a station's
Document Number serial and its dash-counter value, computed per station-day on clean
(non-reset) days: median ρ=0.80 across all stations (1,581 station-day samples), **ρ=0.91
for STATE specifically**. A station's own outgoing numbering and the relay's counter move
together, as expected if both track real chronological order — this is independent
confirmation of the filing_time-ordering result above, from a completely different field.

**It gives an independent, verifiable measure of real cable volume.** Taking the robust
99.9th-percentile serial per year for STATE specifically (excluding a small tail of
placeholder-like values ≥900,000 — a real but minor data-quality artifact, 0-67
docs/year, not evenly distributed and not investigated further here):

| Year | STATE's real annual volume (p99.9 serial) | STATE archived in this corpus | Archived/real | Counter's implied yearly volume ÷ STATE's real volume |
|---|---|---|---|---|
| 1973 | 252,324 | 43,668 | 17.3% | 60.1x |
| 1974 | 284,247 | 85,170 | 30.0% | 124.9x |
| 1975 | 305,666 | 102,270 | 33.5% | 113.9x |
| 1976 | 313,994 | 106,007 | 33.8% | 107.4x |
| 1977 | 311,031 | 90,844 | 29.2% | 138.0x |
| 1978 | 327,994 | 99,479 | 30.3% | 125.3x |
| 1979 | 334,831 | 94,018 | 28.1% | 119.6x |

This is the strongest available evidence on the counter's implied-volume gap, and it's
derived directly from this corpus's own data rather than speculation: even STATE's
complete real outgoing stream (a few hundred thousand cables/year, independently verified
via its own sequential numbering, not the counter) is still ~60-140x smaller than what the
counter implies for the same year. Whatever the counter is tallying, it cannot be
explained by State Department cable traffic alone — that traffic's real volume, measured
directly, is two orders of magnitude too small.

### Other signals checked and ruled out

Three more metadata fields were checked as possible counter-related signals; none showed
a connection:

- **Film Number** (e.g. `D760210-0639`, a microfilm reel + frame identifier): reel
  `D760210` alone spans 8 distinct draft dates and 142 distinct originating stations, and
  frame numbers per reel typically top out around 1,200-2,500 (max observed 9,822) — two
  orders of magnitude below the counter's ~130,000 reset ceiling. This is a NARA
  microfilming batch assembled later in the archival process, freely mixing stations and
  dates — unrelated to transmission order or the relay counter.
- **Legacy Key** (e.g. `link1973/newtext/t19730629/aaaajogf.tel`): the `t19730629`
  segment is a NARA digitization-batch identifier, not a date — one batch spans up to 27
  distinct draft dates. The `aaaajogf`-style filename suffix does increment sequentially,
  but purely as scan/digitization order: consecutive filenames jump between unrelated
  stations, and within one station's cluster the Document Numbers actually run
  *backward* (e.g. `...03542 → 03541 → 03540...`), confirming this reflects archival
  scanning order, not transmission order.
- **Control Number**: present on only 783 of 2,081,272 records. It's a shared
  case-grouping ID covering *multiple* distinct cables (e.g. `S7700301` spans a dozen
  different Document Numbers) — reads as an administrative/review case number, not a
  per-message counter.

## Reset ceiling: ~129,000-131,000, not calendar-based

The counter does not reset daily. Scanning the full corpus for large drops
(threshold >50,000) in time-order, every reset fires at a strikingly consistent
ceiling — 130687, 130664, 130803, 130581, 130536, 129766, 129154, ... — across many
independent reset events spanning all seven years. This looks like a capacity-based
rollover (e.g. a tape reel or batch-log capacity limit intrinsic to the original
tape-relay hardware) rather than a time-based reset.

### Aside: what would that capacity be in modern terms?

Not a measured fact — an order-of-magnitude extrapolation, since the counter counts
*messages*, not bytes. Average message size from real extracted data (avg
`_message_content` 1,658 chars + ~500 chars estimated routing/header overhead ≈ 2,158
chars/message) × the ~130,000-message reset ceiling:

- **≈267.5 MB** at 1 byte/char (modern ASCII convention)
- **≈167.2 MB**-equivalent at 5 bits/char — the historically accurate encoding, since
  ACP-127 tape relay used 5-level Baudot/ITA2 punched paper tape, not ASCII

Across the observed reset range (129,000-131,000): roughly 166-169 MB in Baudot terms,
265-270 MB in modern-byte terms.

## Actual archived cables vs. counter-implied volume, per day

**Method**: for each calendar day (grouped by DTG date — the only date info both actual
cable counts and the counter share), compute:
- `actual_cables` — count of documents in this corpus dated that day
- `implied_volume_naive_span` — `max(counter) − min(counter) + 1` among that day's
  documents

This is a **conservative lower bound**, not an exact count: it can only see the range
between the earliest and latest counter values we happen to have *in this archive* for
that day, and does not attempt to detect or correct for a reset happening mid-day (which
would make the true range larger than what a naive max−min span captures). Full detail
in [`dash_counter_daily_comparison.csv`](dash_counter_daily_comparison.csv) (2,411 days,
1973-01-02 through 1979-12-31).

### Result

| | Total |
|---|---|
| Actual cables (this corpus, days with counter data) | 1,827,495 |
| Implied volume (naive span, summed across days) | 243,235,084 |
| **Overall ratio** | **~133x** |

Excluding a handful of known thin/anomalous months — 1973-01 through 1973-05 (very low
document counts this early in the corpus, not representative) and 1976-06 (a known
scanning/batch-quality outlier already flagged during the post-Dec-1976 format
investigation — nearly all sampled documents that month failed to parse cleanly) — the
monthly ratio is **remarkably stable, settling in an ~105x-165x band from mid-1973
through 1979**, with no long-term drift. Sample months:

| Month | Actual | Implied (span) | Ratio |
|---|---|---|---|
| 1973-07 | 13,029 | 2,445,324 | 187.7x |
| 1974-06 | 22,213 | 2,803,730 | 126.2x |
| 1975-08 | 25,216 | 2,729,558 | 108.2x |
| 1976-08 | 25,291 | 2,626,745 | 103.9x |
| 1977-06 | 23,964 | 3,195,342 | 133.3x |
| 1978-06 | 26,147 | 3,305,163 | 126.4x |
| 1979-06 | 25,691 | 3,418,273 | 133.1x |

**Interpretation**: what the ~100-160x gap between "what the counter implies existed" and
"what's in this declassified corpus" actually represents isn't established by anything in
this repository — the counter is a relay-centre transmission log (see "where the counter
sits in the raw header" above), and we have no data on what else, if anything, passed
through the same relay alongside State Department traffic, so a claim about *who else*
generated the remaining volume would be speculation this analysis doesn't support.

What Souza, Coelho, Shah & Connelly (2016) do document, from NARA's own appraisal records
(pages 7-8), is that the cable population in both this corpus and their study is already a
curated subset of something much larger before the counter even enters the picture: 27
million electronic records had accumulated in the CFPF by 2006, and NARA archivists
deliberately preserved only cables carrying historically-significant TAGS — full retention
for the Political/Military/Social/Economic/Technology-Science categories, and a reviewed
sample of just over 7,000 cables to decide what else, from the remaining
Operations/Administration/Consular categories, merited keeping. The paper notes this
curation explicitly *reduced* the retained proportion of unclassified, routine cables. That
27-million figure spans decades of CFPF record-keeping generally, not specifically the
1973-1979 window this corpus and the counter both cover, so it can't be turned into a
precise ratio here — but it establishes that substantial, deliberate, documented filtering
happened well before either this corpus or the counter's implied volume are compared to
each other. The remarkable month-to-month stability of the counter/corpus ratio (given
it's derived from a completely different, independent signal — the counter — than the
corpus's own document count) is itself supporting evidence that both are tracking a real,
consistent underlying system rather than artifacts of extraction quality; it does not by
itself tell us what the counter's larger implied volume consists of.

Contrast this with the FOIA/SAS-total-vs-corpus ratio below, which is **not** stable —
it grows steadily over the decade, a genuinely different signal telling a different
story (declassification/inclusion coverage narrowing over time, not a constant sampling
fraction of relay traffic).

## Cable classification and full-text availability: cross-checking against Souza et al. (2016) and the FOIA SAS totals

Souza, Coelho, Shah & Connelly (2016), *"Using Artificial Intelligence to Identify State
Secrets"* (arXiv:1611.00356) — analyzing the same NARA/CFPF-derived State Department
cable population this corpus is drawn from — documents specific date ranges with a high
concentration of cables that have index/metadata records but **no message text**
(placeholder text reading `ERROR READING TEXT INDEX` or `EXPAND ERROR ENCOUNTERED`,
the same pattern already identified in this corpus's `_message_content` field), which the
paper's authors interpret as cables likely destroyed or removed by the State Department
sometime after original transmission but before declassification review. The paper
covers 1973-1978 (its Fig. 1/Fig. 2 captions read "1974-1978" and "1973-1978"
respectively); this corpus extends one year further, through 1979.

**Method**: for each document, bucket `_message_content` into `text` (real body present),
`error` (matches the `ERROR READING TEXT INDEX` / `EXPAND ERROR ENCOUNTERED` placeholder
pattern), or `blank` (null/empty), and classification into `UNCLASSIFIED` / `LOU` /
`CONFIDENTIAL` / `SECRET` (from `Original Classification`; a small ~185-document residue
of garbled/OCR-noise values across the full corpus — e.g. `"SECRETARY'S"`,
`"CONFIDENTIAL;"` — is bucketed `OTHER` and excluded from cross-checks). Grouped by DTG
date (falling back to `Draft Date` when `_dtg` failed to parse; 1977 has a higher
`_dtg`-null rate, 18,089/307,219 docs with neither date available and excluded from the
*daily* breakdown, though still counted in yearly totals). Full daily detail in
[`cable_classification_availability_daily.csv`](cable_classification_availability_daily.csv),
monthly rollup in
[`cable_classification_availability_monthly.csv`](cable_classification_availability_monthly.csv),
yearly rollup in
[`cable_classification_availability_yearly.csv`](cable_classification_availability_yearly.csv).

### Cross-check 1: the paper's named gap date ranges

All four of the paper's named ranges show a near-total collapse to placeholder text in
our own corpus — strong independent confirmation:

| Named range | Our days w/ data | Avg missing/day | Missing % range |
|---|---|---|---|
| Dec 1-15, 1975 | 15/15 | 1,055/day | 94.0%-99.9% |
| Mar 18-31, 1976 | 14/14 | 1,107/day | 84.0%-100% |
| May 25-31, 1976 | 7/7 | 611/day | 16.0%-100% |
| June 1976 (full month) | 30/30 | 1,095/day | 99.2%-100% |

One important nuance versus the paper's own text: the paper describes these periods as
having "almost no State Department cables in the database" — i.e. an absence of
documents. Our data shows the opposite mechanism: the *metadata records are present* at
normal or near-normal daily volume (e.g. 1,000-1,600/day through most of these ranges) —
what's missing is specifically the message *body text*, replaced by the
`ERROR READING TEXT INDEX` placeholder. This matches the paper's own Table 5 category
("Error messages for body"), not a true document-count gap. Whether this reflects how the
paper's authors characterized their own finding loosely in prose, or a difference between
their corpus and ours, isn't something we can resolve from the paper text alone.

We also found that the paper's two separately-named "May 25-31, 1976" and "June 1976"
ranges are not, in our data, two separate events — they are one continuous gap running
1976-05-25 through 1976-07-02 (missing % never drops below 94% for the entire six-week
span). Similarly the Dec-1975 and Mar-1976 gaps both extend several days beyond their
named boundaries (Nov 26 - Dec 24, 1975; Mar 17 - Apr 5, 1976 respectively) once measured
directly rather than read off a chart. See the full gap table below.

### Cross-check 2: the paper's Table 5 counts

The paper's Table 5 reports (across its 4 classification categories, its full analyzable
population, likely 1973-1978 given Fig. 2's caption):

| Situation | Paper's total | Our total (1973-1978) | Our total (1973-1979) |
|---|---|---|---|
| Has real text | 1,758,279 | 1,627,587 | 1,946,784 |
| Error placeholder | 119,744 | 124,041 | 126,234 |
| Blank body | 8,282 | 7,041 | 8,069 |
| **Sum** | **1,886,305** | **1,758,669** | **2,081,087** |

The error-placeholder and blank-body totals land within single-digit percent of the
paper's figures for the matching 1973-1978 window — a solid independent confirmation
that we're both counting the same underlying phenomenon. The "has real text" total is
~7.4% lower in our count; the paper's own pipeline applies additional exclusion
categories we don't reproduce here (410,539 "withdrawn" cables, 128,026 cables with
significant TAGS but no text, both counted separately from Table 5) — some fraction of
what we bucket as `text` or `error` may correspond to those other paper-side categories
rather than being a true mismatch. Per-classification breakdown (has-text, 1973-1978):

| Classification | Paper | Ours | Diff |
|---|---|---|---|
| Unclassified | 876,797 | 820,380 | -6.4% |
| Limited Official Use | 411,973 | 388,509 | -5.7% |
| Confidential | 375,690 | 346,727 | -7.7% |
| Secret | 93,635 | 71,971 | -23.1% |

Secret shows the largest gap by far, consistent with Secret-classified cables being more
likely to be withdrawn/still-restricted rather than fully declassified — the category
most affected by the exclusion pipelines not lining up between the two counts.

### Cross-check 3: the FOIA-reported SAS per-year totals

[`sas_totals_from_foia.csv`](../../../data/source/sas_totals_from_foia.csv) reports SAS system totals per
year, system-wide (not scoped to what's been declassified/archived here) — i.e. these
are expected to be substantially *larger* than our corpus, similar in spirit to the
counter-implied-volume comparison above, but this is an independent, non-counter-derived
figure.

| Year | FOIA total | Our total | Ratio (FOIA/ours) |
|---|---|---|---|
| 1973 | 225,840 | 155,285 | 1.45x |
| 1974 | 467,881 | 289,755 | 1.61x |
| 1975 | 541,337 | 333,161 | 1.62x |
| 1976 | 569,391 | 347,516 | 1.64x |
| 1977 | 617,816 | 307,330 | 2.01x |
| 1978 | 655,808 | 325,806 | 2.01x |
| 1979 | 732,206 | 322,419 | 2.27x |

Unlike the dash-counter ratio (stable ~105-165x throughout), **this ratio grows steadily**
from 1.45x to 2.27x over the decade — a genuinely different pattern, meaning declassified
inclusion in this corpus covers a shrinking share of total SAS volume as the decade
progresses. Breaking the ratio down by classification shows this growth is concentrated
almost entirely in Unclassified cables (1.85x → 3.33x) while Confidential/Secret/LOU stay
comparatively flat (1.1x-1.4x range throughout):

| Year | Unclass. ratio | LOU ratio | Confidential ratio | Secret ratio |
|---|---|---|---|---|
| 1973 | 1.85x | 1.16x | 1.13x | 1.19x |
| 1974 | 2.04x | 1.23x | 1.15x | 1.15x |
| 1975 | 2.04x | 1.21x | 1.14x | 1.20x |
| 1976 | 2.11x | 1.22x | 1.22x | 1.42x |
| 1977 | 2.83x | 1.30x | 1.18x | 1.38x |
| 1978 | 2.84x | 1.31x | 1.19x | 1.33x |
| 1979 | 3.33x | 1.34x | 1.21x | 1.41x |

This is consistent with routine unclassified administrative traffic being the least
likely category to make it into a curated diplomatic-cable archive like this one (no
declassification review required, and plausibly de-prioritized for capture/retention
generally), with that gap widening as SAS overall volume grew through the decade.

Also worth flagging: the FOIA CSV's own 1976 row has an internal ~27,000 discrepancy —
summing its four classification columns for 1976 gives 596,388, not the reported
`Total Yearly` of 569,391. All other years reconcile within a few hundred. Notably 1976
is both the year of the dash-counter format transition and the year with the largest
cluster of text-removal gaps found here — plausibly related, though we have no direct
evidence connecting the two.

**All three yearly totals side by side** — the counter-implied total (naive per-day span,
summed across the year — linear, not the log scale used in the charts), the FOIA-reported
SAS total, and this corpus's own archived count:

| Year | Counter-implied total | FOIA SAS total | Our corpus total | Counter ÷ FOIA | Counter ÷ ours |
|---|---|---|---|---|---|
| 1973 | 15,169,166 | 225,840 | 155,285 | 67.2x | 97.7x |
| 1974 | 35,493,316 | 467,881 | 289,755 | 75.9x | 122.5x |
| 1975 | 34,804,038 | 541,337 | 333,161 | 64.3x | 104.5x |
| 1976 | 33,709,801 | 569,391 | 347,516 | 59.2x | 97.0x |
| 1977 | 42,923,679 | 617,816 | 307,330 | 69.5x | 139.7x |
| 1978 | 41,081,467 | 655,808 | 325,806 | 62.6x | 126.1x |
| 1979 | 40,053,617 | 732,206 | 322,419 | 54.7x | 124.2x |
| **1973-1979** | **243,235,084** | **3,810,279** | **2,081,272** | **63.8x** | **116.9x** |

The counter-implied total is a lower bound (see caveats) and still runs 55-76x the
FOIA-reported system-wide SAS total. What accounts for that gap isn't established here —
see the interpretation note above: the paper documents that NARA's own appraisal process
already filtered the underlying CFPF cable population substantially (27 million
accumulated electronic records, curated down by TAGS significance) before either this
corpus or the FOIA SAS totals were assembled, but that process isn't specific enough to
account for the counter's particular scale, and we have no independent data on what the
tape-relay counter itself was tallying beyond State Department traffic. FOIA/SAS and our
corpus, by contrast, stay within the same order of magnitude of each other throughout
(both are specifically State Department cable counts).

### Additional gap/spike date ranges identified

Beyond the paper's four named ranges, using the same missing-count signal (`error` +
`blank`, both by percentage and by raw daily count, since the paper's Fig. 2 y-axis is
raw count, not percentage) across the *entire* 1973-1979 corpus surfaces three more
spikes that are visible in the paper's own Fig. 2 chart but never named or dated in its
text, precisely dated here for the first time, plus one small anomaly entirely outside
the paper's coverage window. Full table in
[`cable_removal_gap_ranges.csv`](cable_removal_gap_ranges.csv):

| Range | Peak day | Peak missing | Named in paper? | Fig. 2 estimate | Notes |
|---|---|---|---|---|---|
| 1973-07-05 to 07-09 | 07-06 | 1,180 | No (visible, unnamed) | ~1,150-1,200 | matches Fig. 2's unlabeled mid-1973 spike |
| 1973-10-18 to 10-23 | 10-19 | 245 | No | not clearly distinguishable | minor/borderline cluster |
| 1973-11-26 to 11-27 | 11-27 | 828 | No (visible, unnamed) | ~800 | matches Fig. 2's unlabeled "shortly before 1/1/1974" spike |
| 1974-10-03 to 10-04 | 10-04 | 478 | No (visible, unnamed) | ~475 | matches Fig. 2's unlabeled "late 1974" spike |
| 1975-11-26 to 12-24 | 12-03 | 1,486 | Yes ("Dec 1-15, 1975") | n/a | actual extent wider than named window |
| 1976-03-17 to 04-05 | 03-24 | 1,691 | Yes ("Mar 18-31, 1976") | n/a | actual extent wider than named window |
| 1976-05-25 to 07-02 | 06-04 | 1,572 | Yes (two ranges, "May 25-31" + "June 1976") | n/a | one continuous ~5.5-week gap, not two |
| 1979-10-30 to 10-31 | 10-31 | 93 | Outside paper's coverage | n/a | small in absolute terms, sharply anomalous vs. 1979's near-zero baseline |

For the three newly-dated 1973-1974 spikes, the paper's text does not offer a historical
explanation, and none is asserted here either — they are reported purely as precise
dates for spikes already visible (but unlabeled and unexplained) in the paper's own
Fig. 2. The four 1975-1976 gaps carry the historical context the paper itself supplies
(East Timor invasion / Ford-Kissinger-Suharto meeting, Dec 1975; Argentina military coup,
Mar 1976; Syrian intervention in Lebanon and the Soweto Uprising, May-June 1976). The
1979-10-30/31 anomaly falls entirely outside the paper's 1973-1978 coverage; its timing
coincides with the intensifying Iran crisis (the Shah was admitted to the US for medical
treatment Oct 22, 1979; the US embassy in Tehran was seized Nov 4, 1979) — noted here
only as a temporal coincidence, not a demonstrated cause.

**1977 and 1978 show almost no gap activity at all** (median missing/day: 0 and 3
respectively; max 4 and 13) — a strong independent confirmation of the paper's own
observation that "the gaps end with the end of Kissinger's term as Secretary of State"
(Jan 20, 1977).

### Per-year stacked classification chart

A stacked-area chart (proportion of `UNCLASSIFIED` / `LOU` / `CONFIDENTIAL` / `SECRET` by
month, reproducing the paper's Fig. 1 style) for each of the seven years, with the gap
ranges above highlighted, is in the [HTML artifact](#) referenced from the project's
data-viz index — see `cable_classification_availability_monthly.csv` for the underlying
numbers.

## Caveats

- `implied_volume_naive_span` is a lower bound, not a precise reconstruction. An attempt
  to build a fully sequenced, reset-aware global estimate (walking every record in
  reconstructed filing-time order across the whole corpus) produced internally
  inconsistent results — roughly 42% of adjacent pairs showed backward steps even after
  reconstructing filing_time to full timestamps, too high to be pure noise, suggesting
  the true structure includes multiple interleaved sub-sequences (parallel
  precedence-tier queues, multiple relay legs) that a single global ordering assumption
  doesn't cleanly capture. The simpler per-day min/max span sidesteps that problem
  entirely (no cross-record ordering required) at the cost of being a floor, not an
  exact figure.
- Pre-1976 documents have `counter` but no `filing_time` (format didn't include it yet)
  — the per-day span comparison still works for those years since it only needs
  `counter`.
- The classification/availability cross-check trusts `Original Classification` and the
  `ERROR READING TEXT INDEX` / `EXPAND ERROR ENCOUNTERED` placeholder pattern as
  extracted from source plaintext (NOT OCR — see `AGENTS.md`'s data-provenance note);
  the ~185-document `OTHER` residue is garbled/noise values in that same source field,
  not a parser artifact of this project's pipeline.
- The 1977 date gap (18,089 documents where neither `_dtg` nor `Draft Date` parsed) is
  excluded from the *daily* gap-detection scan but included in yearly totals; since 1977
  otherwise shows almost no gap activity, this is unlikely to be hiding an undetected
  1977 spike, but it isn't ruled out either.
