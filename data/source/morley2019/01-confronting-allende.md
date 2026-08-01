# Chapter 1 — Confronting Allende — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 1`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson`, cross-checked against `data/cable-extract/<year>.ndjson`.

**⚠️ Corpus date boundary**: `data/cable-extract/` only contains years **1973 through 1979**. All three of this chapter's telegram/cable citations are dated **1970** (the Allende-election/Track-II period, three years before the corpus's coverage begins) — every one of them is **categorically out of range**, the mirror image of Chapter 8's problem at the other end of the timeline.

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 8 | 281 | Kerry quote in Telegram AmEmb Chile to Department of State, 5 September 1970, DOS/OH; CIA assessment in Memorandum for Dr. Kissinger/Chile-40 Committee Meeting, September 14, 1970, DNSA. | **Out of corpus date range** (1970; corpus begins 1973-01-01). The CIA memo is also out of corpus by type (not State Dept cable traffic). |
| 41 | 282 | CIA, Cable from Headquarters [Firm and Continuing Policy that Allende be Overthrown by a Coup !] October 16, 1970, DNSA. | **Out of corpus** on two independent grounds: 1970 date (pre-corpus) **and** CIA origin (not State Dept traffic). This is the well-known "It is firm and continuing policy..." Track II cable — historically significant, but not in this collection regardless of date. |
| 45 | 282 | Telegram, Under Secretary of State Irwin to All ARA Diplomatic Posts, October 22, 1970, DOS/OH; Memo, CIA, "Special Report," October 21 , 1970, CIA. | **Out of corpus date range** (1970). The CIA memo is also out of corpus by type. |

## Notes on the workflow

- No searches were run for this chapter — every citation is dated 1970, three years before this corpus's earliest coverage (1973-01-01), so a search would be guaranteed to return nothing. This is the same failure mode as Chapter 8 (1980 citations, after the corpus's latest date) but at the opposite boundary.
- Between Chapters 1 and 8, this project has now identified both edges of the corpus's usable date range for matching this book's citations: **1973-01-01 to 1979-12-31**. Any citation outside that window is unmatchable in principle, not a search failure.
