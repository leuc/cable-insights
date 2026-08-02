# Do cables that reference each other share the same office distribution and FM/TO/INFO addresses?

**Status:** answered
**Thread of:** —

## Question

When one cable references another (a `REF:` line resolving to another
document's MRN), do the two cables tend to carry the same office
distribution selection and values (ACTION/ORIGIN/INFO office codes and copy
counts), and/or the same FM/TO/INFO addressee lines, more than two unrelated
cables would?

## Hypothesis

Referencing cables are drafted in the same institutional context — same
desks, same routing lists — so their distribution (ACTION/ORIGIN/INFO office
codes) and TO/INFO addressee sets should overlap well above random chance.
The FM (originating post) comparison is expected to be a weaker or
near-tautological signal on its own — a cable and the prior cable it cites
are disproportionately likely to share an author post regardless of topic —
so the more interesting test is whether office-distribution and INFO-breadth
overlap holds even after accounting for that. This is a companion test to
[`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md):
that question found strong TAGS (topical) overlap between referencing
cables; this one asks whether that overlap is distinct from, or largely
explained by, shared routing/addressing metadata.

## Data used

- External: `results/<year>.ndjson` (raw per-document extractor output —
  `_distribution` {ACTION/ORIGIN/INFO office code: copy count}, `_from`,
  `_to`, `_info`, and `Message Attributes.Document Number`) and
  `results/<year>.reftel.norm.ndjson` (`document_number_raw` ->
  `document_number` mapping, plus `extracted_references`) from the sibling
  `acp-127` repo (see `data/external/README.md`) — no local copy checked
  into this repo; read directly from `data/cable-extract/`.
- Shared: `lib/station.py` (`parse_station`), for the STATE/non-STATE
  breakdown.
- Code: `code/address_reference_similarity.py` (question-exclusive).

## Method summary

- Build a raw-Document-Number -> normalized-`document_number` map from
  `reftel.norm.ndjson`'s `document_number_raw`/`document_number` pair (same
  join key used by `tags-reference-similarity`).
- Load `_distribution`, `_from`, `_to`, `_info` per document from
  `results/<year>.ndjson`, keyed by raw Document Number, remapped to
  normalized `document_number`.
- Join with citing -> cited reference edges from `reftel.norm.ndjson`
  (identical join to `tags-reference-similarity`).
- For each citing/cited pair, compare:
  - office-distribution code sets (Jaccard on ACTION+INFO+ORIGIN codes;
    separately, a count-weighted overlap using the copy-count values, since
    "same codes, same values" is the stronger claim in the question);
  - FM text (exact/normalized match rate);
  - TO and INFO addressee text (token-set Jaccard).
- Reuse the same-size random-pair null baseline construction from
  `tags-reference-similarity` so actual-vs-random is apples-to-apples.
- Explicitly separate the FM (near-tautological "same post") signal from the
  office-distribution and INFO-breadth signal, since conflating them would
  overstate the finding.
- Run the whole comparison twice: once over the full corpus, once with
  STATE-originated documents (station parsed from `document_number`)
  excluded from both sides of every pair, to check the finding isn't an
  artifact of STATE's ~29% share of the corpus.

## Result

Answered — yes, but the effect splits into two tiers. Internal State
Department routing (office distribution codes) shows a strong, consistent
signal: `action_origin` (which office is tasked to act) 17.5x lift, 77.4%
exact-match; `info_office`/`office_all` (which bureaus are copied) 3.3x-3.6x
lift. External addressing splits further: `to_tokens` (primary addressee) is
the weakest metric found, 1.4x lift, because TO has too little variance
corpus-wide to discriminate; `info_tokens` (which posts are copied) is a
much stronger, TAGS-like signal at 12.7x lift. Office "same values" (copy
counts), conditioned on already sharing a code, adds little (95.3% vs 78.7%
random, 1.2x lift). FM exact-match looked weak/confounded in the full
corpus (4.3x lift) but that turned out to be a STATE artifact: excluding
STATE (station parsed from `document_number`) from both sides of every
pair, FM lift jumps to **71.6x** — the strongest metric in the whole
question — because STATE's near-ubiquitous FM value was diluting an
otherwise very strong "same field post" signal. Full write-up:
`results/address_reference_similarity.md`.

## Caveats / limitations

- FM overlap is expected to be inflated by cables replying to/continuing
  their own prior traffic; report it separately from office-distribution
  overlap rather than folding it into one score.
- `results/<year>.ndjson` is raw extractor output, not a normalized/validated
  product like `*.reftel.norm.ndjson` or `*.tags.norm.ndjson` — document_number
  matching relies on the raw `Document Number` attribute string matching
  exactly what `reftel_normalize.py` captured as `document_number_raw`.

## Related questions

- [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md) —
  same shape of question ("do referencing cables share property X") and the
  same reference-edge join, applied to routing/addressing metadata instead
  of TAGS; this question exists to check whether that TAGS finding is
  distinct from shared routing/distribution metadata.
- [`reference-graph-structure`](../reference-graph-structure/HYPOTHESIS.md) —
  shares the same external reference-data source
  (`*.reftel.norm.ndjson`), but does not share code with this question.
- [`reference-time-lag`](../reference-time-lag/HYPOTHESIS.md) — same
  reference-edge join, applied to the time gap between citing and cited
  cables instead of routing/addressing metadata; also uses
  `lib/station.py`.
