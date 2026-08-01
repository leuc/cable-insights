# Chapter 8 — Policy Adrift — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 8`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` narrowed by origin/destination station, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson`. "Confirmed" = cable text directly verified. "Likely" = clearly-best topical fit, not fully independently verified. "Ambiguous" = multiple same-day candidates, no way to pick without chapter-body text.

**⚠️ Corpus date boundary — this is the key fact about this chapter**: `data/cable-extract/` only contains years **1973 through 1979** (confirmed: `all-dates.ndjson`'s latest `document_date` is `1979-12-31`, and no `198*` year files exist at all). This chapter, "Policy Adrift," covers the second half of the Carter term and is overwhelmingly dated **1980** — so the large majority of its telegram citations are **categorically out of range**, not failed searches. Only citations dated 1979 or earlier could possibly match.

Of 22 distinct US telegram citations in this chapter, only **3 fall within the corpus's date range** (notes 19, 20, 85 — all late 1979); the other **19 are out of range** (1980). Of the 3 in-range: 2 confirmed, 1 likely.

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 14 | 332 | Telegram, Landau to Vance, July 22, 1980, DOS/FOIAe, III | **Out of corpus date range** (1980; corpus ends 1979-12-31). |
| 19 | 332 | Telegram, USUN Mission, New York (McHenry) to Vance, December 4, 1979, DOS/FOIAe, III. | **Confirmed: 79USUNNEWYORK5828** (raw `1979USUNN05828`). USUN→STATE, subject "34TH UNGA: THIRD COMMITTEE - ECOSOC REPORT - CHILE RESOLUTION," signed MCHENRY (Donald McHenry, US Ambassador to the UN) — exact match. |
| 20 | 332 | Telegram, Vance to USUN Mission, New York, December 5, 1979, Ibid. | **Confirmed: 79STATE313565** (raw `1979STATE313565`). STATE→USUN NEW YORK/SANTIAGO, subject "34TH UNGA -- RESOLUTIONS ON HUMAN RIGHTS IN CHILE," signed VANCE — direct reply to note 19's cable, one day later. |
| 22 | 332 | Telegram, Landau to Vance, January 18, 1980, DOS/FOIAe, III | **Out of corpus date range** (1980). |
| 23 | 332 | Telegram, Landau to Vance, January 23, 1980, Ibid. | **Out of corpus date range** (1980). |
| 24 | 332 | Telegram, Landau to Vance, January 18, 1980, Ibid. | **Out of corpus date range** (1980); same date as note 22. |
| 25 | 332 | Telegram, Landau to Vance, February 4, 1980, Ibid. | **Out of corpus date range** (1980). |
| 39 | 333 | Cable, Landau to Vance, April 16, 1980, NSA, Staff Material, North/South, Folder: 1-10/80, Box 3-9, JCPL. | **Out of corpus date range** (1980). |
| 43 | 333 | Telegram, Vance to AmEmb, Ottawa et al., April 15, 1980, NSA, Staff Material, North/South, Folder: 1 - 10/80, Box 3-9, JCPL. | **Out of corpus date range** (1980). |
| 47 | 334 | See for instance Telegram, AmEmb Paris (Hartman) to Vance, April 17, 1980... Telegram, AmEmb London (Streator) to Vance, April 17, 1980, Ibid. | **Out of corpus date range** (1980), both telegrams. |
| 53 | 334 | Memo, Flood to Derian, February 18, 1980... Telegram, Vance to US Mission Geneva, February 23, 1980, NSA... | Memo out of corpus (DOS internal record). Telegram: **out of corpus date range** (1980). |
| 61 | 334 | Telegram, Landau to Vance, March 18 , 1980, NSA, Staff material, North-South... | **Out of corpus date range** (1980). |
| 62 | 334 | Telegram Landau to DOD (Joint Chiefs of Staff), March 4, 1980, DNSA. | **Out of corpus date range** (1980); also DOD-addressed rather than State Dept routing, likely a different distribution channel from this corpus regardless. |
| 64 | 334 | Telegram, Christopher to AmEmb Santiago, "Naval Exercise UNITAS XXI," April l l , 1980, NSA... | **Out of corpus date range** (1980). |
| 71 | 335 | Telegram, Landau to Vance, "US/Bilateral Relations," April 24, 1980, DOS/FOIAe, III. | **Out of corpus date range** (1980). |
| 73 | 335 | Telegram, Landau to Vance, "US/Bilateral Relations," April 24, 1980. | **Out of corpus date range** (1980); same date/title as note 71. |
| 76 | 335 | Quoted in Telegram, The Situation Room, To Denend for Brzezinski, "Secretary's Morning Summary," June 21 , 1980... | **Out of corpus date range** (1980). |
| 81 | 335 | Telegram, Situation Room, to Denend for Brzezinski, "Secretary's Morning Summary," June 21 , 1980. | **Out of corpus date range** (1980); same date/citation as note 76. |
| 85 | 335 | Telegram, Landau to Vance, September 2S, 1979. | Likely: **79SANTIAGO6822** (raw `1979SANTIA06822`) — SANTIAGO→STATE/ROME, subject "THE DAY THE CARDINAL BLINKED," signed LANDAU — Cardinal Silva's censored/uncensored Independence Day homily and its criticism of the regime, a strong topical fit for a chapter about eroding church-state relations. Read `"September 2S"` as `"September 28"` per this project's established `S`→`8` OCR-substitution pattern. 5 other same-day SANTIAGO→STATE candidates exist but are all off-topic (Merino/Valenzuela travel, IMCO candidacy, LAN Chile fares, Beagle Channel mediation). |
| 95 | 335 | Telegram, Landau to Muskie, August 20, 1980, DOS/FOIAe, III. | **Out of corpus date range** (1980); also notes the Secretary of State transition (Muskie succeeded Vance in May 1980). |
| 96 | 336 | Telegram, CanadianEmb, Santiago... | Out of corpus (Canadian Embassy record) **and** out of date range (1980) regardless. |
| 98 | 336 | National Intelligence Daily Cable... [CIA product, not a State Dept telegram] | Out of corpus (CIA product, not State Dept traffic) **and** out of date range (1980) regardless. |
| 103 | 336 | Telegram, Landau to Muskie, September 10, 1980, DOS/FOIAe, III | **Out of corpus date range** (1980). |
| 112 | 336 | Telegram, Landau to Muskie, September 8, 1980, DOS/FOIAe, III | **Out of corpus date range** (1980). |
| 113 | 336 | Telegram, Muskie to AmEmb, Santiago, September 12, 1980, Ibid. | **Out of corpus date range** (1980). |

## Notes on the workflow

- This is the first chapter where the corpus's date boundary (1973-1979) becomes the dominant constraint rather than OCR quality or candidate ambiguity — worth remembering for the Conclusion chapter too, since its endnotes reach even later (into the 1980s/1990s, based on earlier extraction passes).
- The two confirmed cables (notes 19-20) form a clean one-day-turnaround exchange at the UN over the annual Chile human-rights resolution — a recurring pattern (UNGA Third Committee Chile resolutions) also seen resolved in Chapters 3 and 6.
- No parallel agents were used for this chapter — with only 3 potentially in-range citations, direct sequential search was faster than the coordination overhead of spawning forks.
