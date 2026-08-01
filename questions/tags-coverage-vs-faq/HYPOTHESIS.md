# How much of the real TAGS data does the FAQ-derived mapping cover?

**Status:** answered
**Thread of:** —

## Question

The Subject TAGS classification used elsewhere in this repo
(`src/tags_mapping.py` in the sibling `acp-127` repo) was transcribed from
`docs/faqs.txt` Appendix I/II, which only documents Subject TAGS codes — not
Geographic or Organization codes. How much of the TAGS data actually present
across the corpus does that mapping explain, and what's in the "unknown"
residue?

## Hypothesis

Exploratory — no single falsifiable claim; this is a coverage-measurement
snapshot rather than a hypothesis test.

## Data used

- External: `results/*.ndjson` (all 7 years) from the sibling `acp-127` repo
  (see `data/external/README.md`), plus `docs/faqs.txt` and
  `docs/rg59_state_dept_tags_74.pdf/.txt` (protocol/reference documents,
  outside this repo)
- Code: none checked in — this was an ad-hoc measurement run directly
  against the external NDJSON, not a maintained script

## Method summary

- Compare two independently-extracted TAGS sources per document
  (`Message Attributes.TAGS` vs. body-line `_tags`), analyzed separately
  since they can and do differ.
- Tokenize, normalize, and filter to 4-letter subject-code-shaped tokens.
- Measure what fraction of real occurrences the FAQ-derived Subject TAGS
  mapping (permanent + temporary + `E`/`M`/`P`/`S`/`T` wildcard rule)
  classifies vs. leaves "unknown."
- Characterize the "unknown" residue to check whether it's mapping gaps or
  simply out-of-scope code categories (Geographic/Organization) the FAQ
  never covered.

## Result

Answered: ~93% of occurrences are covered once the wildcard field rule is
included. The "unknown" residue is mostly legitimate Organization TAGS
(NATO, UNGA, OECD, etc.) that the FAQ never documented in the first place,
not a mapping defect. Full write-up: `results/tags_coverage.md`.

## Caveats / limitations

This is a snapshot analysis at one point in the underlying extraction
pipeline's evolution — see the write-up's "independent research, not part
of `docs/faqs.txt`" section for scope boundaries.

## Related questions

- [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md) —
  shares the same TAGS-classification foundation, different question
  (coverage vs. co-occurrence).
