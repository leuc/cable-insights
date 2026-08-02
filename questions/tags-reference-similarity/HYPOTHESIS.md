# Do cables that reference each other share similar TAGS?

**Status:** answered
**Thread of:** —

## Question

When one cable references another (a `REF:` line resolving to another
document's MRN), do the two cables tend to carry the same or similar TAGS
codes, more than two unrelated cables would?

## Hypothesis

Cables citing/referencing each other are topically related, so their TAGS
code sets should overlap well above what random chance would produce — and
this should hold across TAGS types (subject, geographic, organization,
person), not just one.

## Data used

- External: `results/<year>.tags.norm.ndjson` and
  `results/<year>.reftel.norm.ndjson` from the sibling `acp-127` repo (see
  `data/external/README.md`) — no local copy checked into this repo
- Shared: `lib/station.py` (`parse_station`), for the STATE/non-STATE
  breakdown
- Code: `code/tags_reference_similarity.py` (question-exclusive)

## Method summary

- Join TAGS records with reference (`extracted_references`) records on
  `document_number`, across all 7 years combined (references cross year
  boundaries).
- For every citing/cited pair, compute Jaccard similarity of TAGS code sets,
  both on the full set and on 7 type-restricted subsets (subject, geo,
  organization, person, annotation, unknown, other).
- Build a same-size random-pair null baseline per citing document, so
  actual-vs-random is apples-to-apples.
- Compute per-code lift for high-frequency codes:
  `P(cited doc has code X | citing doc has code X)`.
- Run the whole comparison twice: once over the full corpus, once with
  STATE-originated documents (station parsed from `document_number`)
  excluded from both sides of every pair, to check the finding isn't an
  artifact of STATE's ~29% share of the corpus.

## Result

Answered — yes, strongly and consistently, across the full corpus and every
TAGS type. Subject-code overlap (topical "aboutness") is if anything the
*strongest* signal (91.8% any-overlap, 61.8% identical-set), not an artifact
of shared dateline geography; effects range 20x-1000x+ above the random
baseline depending on type. Confirmed robust to STATE's ~29% share of the
corpus: every run now reports both ALL (including STATE) and EXCLUDING
STATE (station parsed from `document_number`, dropped on both sides of the
pair); mean Jaccard and lift stay in the same range either way, with no
reversal of sign or order-of-magnitude change. Full write-up: `results/tags_reference_similarity.md`.
Published visual summary: [TAGS Reference Similarity — ACP-127](https://claude.ai/code/artifact/d0f24b09-043b-480e-abe2-2a21892d938f)
(saved locally as `results/tags_reference_similarity.html`).

## Caveats / limitations

See the full write-up's method section for the null-baseline construction
and per-code minimum-n thresholds used for the lift analysis.

## Related questions

- [`tags-coverage-vs-faq`](../tags-coverage-vs-faq/HYPOTHESIS.md) — shares
  the same TAGS-classification foundation, different question (coverage vs.
  co-occurrence).
- [`reference-graph-structure`](../reference-graph-structure/HYPOTHESIS.md) —
  shares the same external reference-data source (`*.reftel.norm.ndjson`),
  but does not share code with this question.
- [`address-reference-similarity`](../address-reference-similarity/HYPOTHESIS.md) —
  follow-up: do cables that reference each other share the same office
  distribution selection/values and/or the same FM/TO/INFO addresses? Tests
  whether the TAGS overlap found here is distinct from, or largely
  explained by, shared routing/distribution metadata.
- [`reference-time-lag`](../reference-time-lag/HYPOTHESIS.md) — same
  reference-edge join, applied to the time gap between citing and cited
  cables instead of TAGS.
