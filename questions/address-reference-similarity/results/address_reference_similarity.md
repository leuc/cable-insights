# Hypothesis: cables that reference each other share the same office distribution and FM/TO/INFO addresses

**Question:** when one cable references another (a `REF:` line resolving to
another document's MRN), do the two cables tend to carry the same office
distribution selection and values (ACTION/ORIGIN/INFO office codes and copy
counts), and/or the same FM/TO/INFO addresses, more than two unrelated
cables would?

**Answer: yes, on every metric, but the effect size splits cleanly into two
tiers.** Internal State Department routing (office distribution codes) shows
a strong, consistent signal (3.3x-17.5x lift). External addressing (TO/INFO
addressee posts, FM originator) shows a real but much weaker signal for TO,
a much stronger one for INFO, and FM looks confounded in the full corpus —
but that's a STATE artifact: restricted to field-post-to-field-post
references, FM exact-match is the *strongest* signal found (71.6x lift; see
the STATE robustness section below).

Script: [`code/address_reference_similarity.py`](../code/address_reference_similarity.py).

## Method

1. **Join.** `data/cable-extract/<year>.ndjson` (raw per-document extractor
   output — `Message Attributes."Document Number"`, `_distribution`,
   `_from`, `_to`, `_info`) is joined with
   `data/cable-extract/<year>.reftel.norm.ndjson` (`document_number_raw` ->
   `document_number`, plus `extracted_references`) on the raw Document
   Number, giving every document a normalized `document_number` key
   comparable with the reference graph. Both are loaded for all 7 years
   combined (references cross year boundaries), 7 years in parallel.
2. **Citing/cited pairs.** For every document with at least one reference
   and its own routing/addressing data ("citing" doc), each resolved
   reference ("cited" doc, itself present in the addressed corpus) forms
   one pair.
3. **Metrics, per pair:**
   - `action_origin`: Jaccard of ACTION+ORIGIN office-code sets (who is
     tasked to act).
   - `info_office`: Jaccard of INFO office-code sets (which Washington
     bureaus are copied).
   - `office_all`: Jaccard of the full ACTION+ORIGIN+INFO code set.
   - `to_tokens` / `info_tokens`: Jaccard of whitespace-tokenized TO / INFO
     addressee text (the diplomatic posts addressed, e.g. "AMEMBASSY
     LONDON"), distinct from the internal office codes above.
   - **FM exact-match rate**: normalized-string equality between the two
     documents' FM (originating post) line, reported separately rather than
     folded into a Jaccard score, since it is expected to be inflated by a
     cable and the prior cable it references simply sharing an author post.
   - **Office value-match rate**: of the office codes shared by both
     documents (the `office_all` intersection), what fraction also carry an
     identical copy count — testing "same values," not just "same codes."
4. **Null baseline.** For every resolved actual reference, a random other
   document is drawn from the same pool and compared to the same citing
   document with the same metrics — an apples-to-apples same-size control,
   identical in method to
   [`tags-reference-similarity`](../../tags-reference-similarity/code/tags_reference_similarity.py).
5. **STATE robustness check.** The whole comparison runs twice: once over
   the full corpus ("ALL"), once with STATE-originated documents (station
   parsed from `document_number` via `lib.station.parse_station`) excluded
   from both sides of every pair ("EXCLUDING STATE").

Run: `python3 questions/address-reference-similarity/code/address_reference_similarity.py [--sample N] [--seed S]`.

## Full-corpus result (all years 1973-1979, `--seed 42`, no sampling)

- 1,136,872 citing documents (have ≥1 reference and their own address data).
- 924,356 (81.3%) have at least one reference that resolves to an in-corpus
  addressed document — matching the resolution rate found in
  `tags-reference-similarity`, as expected since it's the same reference
  graph.
- 2,650,154 total reference pairs; 2,055,938 (77.6%) resolved.

### Aggregate similarity

| view | n pairs | mean Jaccard (actual) | mean Jaccard (random) | any overlap (actual) | identical (actual) | lift |
|---|---|---|---|---|---|---|
| action_origin | 2,025,211 | 0.774 | 0.044 | 77.4% | 77.4%\* | 17.5x |
| info_office | 2,025,198 | 0.657 | 0.202 | 96.7% | 20.7% | 3.3x |
| office_all | 2,025,211 | 0.685 | 0.192 | 96.7% | 21.4% | 3.6x |
| to_tokens | 2,024,710 | 0.216 | 0.152 | 59.2% | 3.3% | 1.4x |
| info_tokens | 1,350,775 | 0.251 | 0.020 | 58.5% | 5.2% | 12.7x |

\* For `action_origin`, "any overlap" and "identical" coincide because a
cable's ACTION/ORIGIN designation is nearly always a single office code, so
any overlap between two single-code sets is by definition total overlap.

| signal | n | actual match % | random match % | lift |
|---|---|---|---|---|
| FM exact-match | 1,957,957 | 36.4% | 8.5% | 4.3x |
| Office value-match (given shared code) | 20,780,035 | 95.3% | 78.7% | 1.2x |

Full run output:

```
Citing documents considered: 1,136,872
Citing documents with >=1 in-corpus resolved reference: 924,356 (81.31%)
Reference pairs: 2,650,154 total, 2,055,938 resolved to an in-corpus addressed document (77.58%)
```

## Reading the two tiers

**Internal routing (office distribution) is the stronger, cleaner signal.**
`action_origin` shows 17.5x lift and 77% exact-match — referencing cables
overwhelmingly share the same acting bureau/office. This makes sense
structurally: a cable and its reftel are very often part of the same
running correspondence handled by the same desk. `info_office` and
`office_all` show a smaller but still solid 3.3-3.6x lift; the random
baseline here (~19-20% mean Jaccard) is much higher than for `action_origin`
because INFO distribution lists are long and dominated by a handful of very
common bureaus (SS, EUR, IO, PA, etc.) that get copied on nearly everything,
so two *unrelated* cables already share several INFO codes by default — the
same "too-common-to-be-informative" effect the TAGS-similarity write-up
found for codes like `US`.

**External addressing (TO/INFO addressee posts) splits.** `to_tokens` is
the weakest metric in the whole test (1.4x lift, 59% any-overlap actual vs.
53% random) — TO is usually a single primary post (often just "STATE" or
one embassy), so two random cables already collide on it at a high baseline
rate purely because there are few common TO values in the corpus. `info_tokens`
is a much stronger, TAGS-like signal (12.7x lift, near-zero random baseline)
— which posts are copied for awareness turns out to encode real topical/
institutional relationship, unlike the single primary addressee.

**FM confirms the predicted confound.** FM exact-match is real (4.3x lift)
but far weaker than the office-routing signals, and the caveat written into
the hypothesis holds: a meaningful share of that 36.4% is cables replying
to or continuing their own prior traffic from the same post, not a
topical/routing relationship. This should not be read as comparable in
strength to `action_origin` or `info_tokens`.

**Office "same values" (copy counts) adds little beyond "same codes."**
Given two cables already share an office code, the actual/random gap in
whether the copy *count* also matches is small (95.3% vs. 78.7%, 1.2x) —
copy counts for a given office code are fairly stable corpus-wide (an
office's standard copy allocation doesn't vary much cable to cable), so this
is a weak additional discriminator once code-set sharing is already known.

## STATE vs. non-STATE robustness check

STATE is ~29% of the corpus and drafted/routed differently from field posts
(outgoing instructions rather than field reporting), so every run now also
reports a section with STATE-originated documents excluded from both sides
of every pair (station parsed from `document_number` via
`lib.station.parse_station`). Full corpus, `--seed 42`:

| metric | ALL, actual | ALL, random | ALL lift | EXCL-STATE, actual | EXCL-STATE, random | EXCL-STATE lift |
|---|---|---|---|---|---|---|
| action_origin (Jaccard) | 0.774 | 0.044 | 17.5x | 0.788 | 0.056 | 14.0x |
| info_office (Jaccard) | 0.657 | 0.202 | 3.3x | 0.683 | 0.207 | 3.3x |
| office_all (Jaccard) | 0.685 | 0.192 | 3.6x | 0.708 | 0.204 | 3.5x |
| to_tokens (Jaccard) | 0.216 | 0.152 | 1.4x | 0.390 | 0.251 | 1.6x |
| info_tokens (Jaccard) | 0.251 | 0.020 | 12.7x | 0.353 | 0.028 | 12.8x |
| FM exact-match | 36.4% | 8.5% | **4.3x** | 75.4% | 1.1% | **71.6x** |
| office value-match | 95.3% | 78.7% | 1.2x | 95.5% | 77.7% | 1.2x |

Excluding STATE shrinks the citing pool from 1,136,872 to 829,021 and the
resolved-reference rate drops sharply, from 81.3% to 43.6% (STATE cables
reference and are referenced by each other heavily, so removing them cuts
out a large share of resolvable edges). Every Jaccard-based metric stays in
the same range as the full-corpus run — no reversal, no order-of-magnitude
change.

**FM is the exception, and it's a big one.** Once STATE is out of the
picture, FM exact-match jumps from 36.4% to 75.4% while its random baseline
*collapses* from 8.5% to 1.1% — lift goes from 4.3x to **71.6x**, higher
than every office-routing metric. This overturns the write-up's original
framing: FM isn't a weak, merely-confounded signal in general — it's a very
strong signal specifically *among field-post cables citing each other*
(a post continuing its own reporting stream), and it was being diluted in
the full-corpus number by STATE, whose FM value ("STATE") is shared by
nearly a third of the corpus regardless of any citation relationship,
making STATE-involving pairs match on FM at a high *rate* but with almost no
discriminating power (STATE's FM matches practically everything else
tagged STATE, actual or random alike). The original caveat about FM being
"inflated by same-post replies" still holds and explains *why* the
non-STATE FM signal is so strong, but the practical conclusion changes:
for field-post-to-field-post references specifically, sharing an FM value
is the single strongest metric measured in this question.

## Conclusion

The hypothesis holds across the board, but not uniformly: **internal
routing metadata (which office acts, which offices are informed) is a
strong, TAGS-comparable signal**, especially `action_origin` (14-17.5x) and
`info_tokens` (~12.7-12.8x), and both are stable whether or not STATE is
included. **External TO addressing is the weakest signal found** (1.4-1.6x)
because the primary-addressee field has too little variance to discriminate.
**FM's strength depends entirely on whether STATE is in the pool**: diluted
to a modest 4.3x lift across the full corpus by STATE's near-ubiquitous FM
value, but the single strongest signal in the whole test (71.6x) once
restricted to field-post-to-field-post references — a cable overwhelmingly
tends to reference its own post's prior traffic. Relative to
`tags-reference-similarity`'s TAGS overlap (20x-1000x+ depending on type),
routing/addressing metadata overlap is directionally consistent but
generally weaker for the office/TO/INFO metrics — supporting the view that
the TAGS finding reflects a genuine topical relationship, not merely an
artifact of cables sharing a routing/distribution list — though FM among
field posts is now the one address-based metric that rivals TAGS-level
effect sizes.

## Reproducing

```bash
# quick sanity check (single year, small sample)
python3 questions/address-reference-similarity/code/address_reference_similarity.py \
    --years 1973 --sample 500 --workers 1

# full corpus, all years
python3 questions/address-reference-similarity/code/address_reference_similarity.py --seed 42
```
