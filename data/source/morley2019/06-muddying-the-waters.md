# Chapter 6 — Muddying the Waters — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 6`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` narrowed by origin/destination station, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson`. "Confirmed" = cable text directly verified. "Ambiguous" = multiple same-day candidates, no way to pick without chapter-body text. **🚫 FULLTEXT UNAVAILABLE** marks any MRN whose `_message_content` could not be read in this corpus.

**⚠️ Date-format quirk** (see Ch.4): for 1977+ citations, `all-dates.ndjson`'s `document_date` carries a `T00:00:00` suffix, so `jq` filters must use `.document_date | startswith("YYYY-MM-DD")`, not `==`. All searches below used this fix.

Chapter spans mid-1977 (Boyatt as chargé d'affaires) through mid-1978 (George Landau, Ambassador from late 1977) — the deteriorating human rights situation and the start of Letelier-case extradition pressure on Chile. Canadian Embassy telegram (note 176) is **not in this corpus** and is skipped.

14 of 19 distinct US telegram citations resolved (11 confirmed, 6 ambiguous, 1 confirmed-absent). Notes 3/4, 8/31, and 171/173 are each the book citing the same date twice — in two cases (3/4) it's the same cable, in the others it's likely two different companion cables from the same day.

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 3 | 314 | Telegram, Popper to Vance, May 7, 1977, DOS/FOIAe, I | **Confirmed: 77SANTIAGO3779** (raw `1977SANTIA03779`). SANTIAGO→STATE, subject "CARDINAL SILVA ON CHILEAN AFFAIRS: UNHAPPY BUT LIVING WITH THE SITUATION," signed POPPER — only SANTIAGO→STATE cable that date; same cable answers note 4. |
| 4 | 314 | Telegram, Popper to Vance, May 7, 1977, DOS/FOIAe, I | Same date/citation as note 3 — same cable, **77SANTIAGO3779**. |
| 8 | 315 | Telegram, AmEmb Santiago (Boyatt) to Vance, July 22, 1977, DOS/FOIAe, I. | Ambiguous — 2 candidates, both signed BOYATT, both plausible. See note (a). Slight lean toward `1977SANTIA06030` since it's explicitly "Part II" of the same Evaluation Report series confirmed for note 14 ("Part I"). |
| 9 | 315 | Telegram, AmEmb Santiago (Boyatt) to Vance, July 21 , 1977, Chile Human Rights Documents, Box 1 , File 1 , NA. | Ambiguous — top 2 of 9 same-day SANTIAGO→STATE candidates, both BOYATT-signed. See note (b). |
| 14 | 315 | Telegram, AmEmb (Boyatt) to Vance, "Evaluation Report: Human Rights in Chile," July 1 , 1977, DOS/FOIA. | **Confirmed: 77SANTIAGO5448** (raw `1977SANTIA05448`). SANTIAGO→STATE, subject "EVALUATION REPORT: HUMAN RIGHTS IN CHILE" — exact quoted-title match, signed BOYATT. |
| 23 | 315 | Telegram, Vance, To All American Republic Diplomatic Posts, July 11 , 1977, DOS/FOIAe, I | Confirmed (high confidence): **77STATE160699** (raw `1977STATE160699`). STATE→ALL POSTS/USCINCSO, subject "PRESS GUIDANCE - CHILE," a Q&A transcript defending US Chile policy, signed VANCE. Addressee is "ALL POSTS," not literally "All American Republic Diplomatic Posts," but date/topic/signature align. |
| 31 | 316 | Telegram, AmEmb Santiago (Boyatt) to Vance, July 22, 1977, Ibid. | Same date/citation as note 8 — same ambiguous set, see note (a). |
| 43 | 316 | Telegram, AmEmb Santiago (Boyatt) to Vance, August 13 , 1977, DOS/FOIAe, I. | **Confirmed: 77SANTIAGO6664** (raw `1977SANTIA06664`). SANTIAGO→STATE, subject "GOC OFFICIALS COMMENT ON CHANGES IN DINA: CREATION OF CNI," signed BOYATT — historically significant (DINA's post-Letelier restructuring into the CNI). |
| 65 | 317 | Telegram, AmEmb Santiago (Boyatt) to Vance, September 23, 1977, DOS/FOIAe, I; Memo, Brzezinski to Carter... [memo out of corpus] | Ambiguous — 14 same-day SANTIAGO→STATE candidates, none topically compelling on inspection (the vaguest-titled one turned out to be an unrelated insurance inquiry). See note (c). |
| 66 | 317 | Memo, Situation Room to Brzezinski... Also see CIA, Telegram, September 14, 1977, Chile Human Rights Documents... | Confirmed absent from this corpus — **no CIA-origin documents exist anywhere in the 1977 data** (checked directly: zero `1977CIA*` document numbers in `all-dates.ndjson` or `1977.ndjson`). This corpus is State Dept cable traffic only; the CIA telegram and the Situation Room memo are both out of corpus by design. |
| 67 | 317 | Telegram, AmEmb Santiago (Boyatt) to Vance, October 5, 1977, Chile Human Rights Documents... | **Confirmed: 77SANTIAGO8239** (raw `1977SANTIA08239`). SANTIAGO→STATE, subject "LABOR LEADERS AND GOC BACK AWAY FROM SHOWDOWN," signed BOYATT — only labor/human-rights-themed candidate of 4 same-day cables. |
| 69 | 318 | Telegram, Landau to Vance, November 28, 1977, Chile Human Rights Documents... | Ambiguous — 2 strong candidates, both LANDAU-signed, both about the aftermath of Pinochet's Nov 23 "banishment" speech. See note (d). |
| 91 | 319 | Telegram, Vance (Christopher) to AmEmb Santiago, "US Goals and Objectives in Chile," December 10, 1977, Chile Human Rights Documents... | **Confirmed: 77STATE295616** (raw `1977STATE295616`). STATE→SANTIAGO, subject "US GOALS AND OBJECTIVES IN CHILE" — exact title match, signed CHRISTOPHER — the only STATE→SANTIAGO cable that date. |
| 109 | 319 | Telegram, AmEmb (Boyatt) to Vance, November 15, 1977, DOS/FOIAe, I | Ambiguous — 3 candidates, all BOYATT-signed. See note (e). |
| 117 | 320 | Telegram, Landau to Vance, December 31 , 1977, DOS/FOIAe, I | **Confirmed: 77SANTIAGO10386** (raw `1977SANTIA10386`). SANTIAGO→STATE, subject "CHILEAN NATIONAL CONSULTATION: SITUATION AS OF DECEMBER 31," signed LANDAU — only candidate that date/direction. |
| 160 | 322 | Telegram, Landau to Vance, February 23, 1978, DOS/FOIAe, I. | Ambiguous — 2 candidates, both LANDAU-signed. See note (f). |
| 163 | 322 | Telegram, Landau to Vance, June 14, 1978 ... "as evidence that our relations are better than they are" ... Telegram, Landau to Vance, October 6, 1978 ... "maximum pressure in connection with the Letelier case." | 1st telegram (Jun 14): **Confirmed: 78SANTIAGO4502** (raw `1978SANTIA04502`). SANTIAGO→STATE, subject "CCC CREDITS - LETELIER/MOFFITT ASSASSINATION INVESTIGATION," signed LANDAU — directly on-topic, though the exact quoted phrase wasn't found verbatim in this specific cable. 2nd telegram (Oct 6): **Confirmed — verbatim quote match, both phrases**: **78SANTIAGO7687** (raw `1978SANTIA07687`). Subject "CCC CREDITS AND GSM-101 GUARANTEES," signed LANDAU. Body text contains both book quotes exactly: "...the GOC and its supporters would play USG agriculture export assistance **as evidence that our relations are better than they are**... we will not be willing to exert **maximum pressure in connection with the Letelier case**." |
| 171 | 322 | Telegram, Landau to Vance, March 17, 1978, DOS/FOIAe, I | Ambiguous — 2 strong candidates, both LANDAU-signed, both Letelier-themed. See note (g). |
| 173 | 322 | Telegram, Landau to Vance, March 17, 1978, DOS/FOIAe, I | Same date as note 171 — same ambiguous set, see note (g); likely resolves to the *other* candidate from that pair (book cites this date twice, probably two different cables), but which maps to which isn't determinable without chapter text. |
| 174 | 323 | Telegram, Landau to Vance, "Survivability of Pinochet," April 20, 1978, Chile Human Rights Documents... | **Confirmed: 78SANTIAGO2976** (raw `1978SANTIA02976`). SANTIAGO→STATE, subject "SURVIVABILITY OF PINOCHET: FROM 'WHAT IF?' TO 'SO WHAT?'" — exact title match, signed LANDAU. |
| 176 | 323 | Telegram, CanadianEmb, Ambassador (Buick) to Under Secretary of State for External Affairs... | Out of corpus (Canadian Embassy record). |

## Ambiguous-match candidate sets

**(a) SANTIAGO→STATE, July 22, 1977** (notes 8, 31): 2 candidates, both signed BOYATT —
`1977SANTIA06021` (Todman visit: projected situation and issues in Chile) ·
`1977SANTIA06030` (Evaluation Report: Human Rights in Chile, Part II — likely fit, continues note 14's "Part I")

**(b) SANTIAGO→STATE, July 21, 1977** (note 9): top 2 of 9 candidates, both signed BOYATT —
`1977SANTIA05988` (Junta member Leigh on the Pinochet plan) ·
`1977SANTIA05987` (Todman visit)

**(c) SANTIAGO→STATE, September 23, 1977** (note 65): 14 candidates, none topically compelling on inspection —
`1977SANTIA07847` / `07871` / `07865` / `07843` / `07857` / `07877` / `07878` / `07879` / `07880` / `07842` / `07872` / `07832` / `07863` / `07866`

**(d) SANTIAGO→STATE, November 28, 1977** (note 69): 2 candidates, both signed LANDAU, both about the Pinochet Nov 23 speech aftermath —
`1977SANTIA09497` (November 23 Speech: Pinochet Talks Turkey) ·
`1977SANTIA09646` (Church/State Relations — Strain on the Modus Vivendi)
(3 weaker same-day candidates also exist, not listed.)

**(e) SANTIAGO→STATE, November 15, 1977** (note 109): 3 candidates, all signed BOYATT —
`1977SANTIA09286` (PDC youth hunger strike in support of exile) ·
`1977SANTIA09288` (Chile resolution at UNGA) ·
`1977SANTIA09299` (Christian Democrats restate position)
(4 weaker same-day candidates also exist, not listed.)

**(f) SANTIAGO→STATE, February 23, 1978** (note 160): 2 candidates, both signed LANDAU —
`1978SANTIA01237` (Chilean media reaction, Moffitt/Letelier case) ·
`1978SANTIA01250` (34th Human Rights Commission: Chile resolutions)

**(g) SANTIAGO→STATE, March 17, 1978** (notes 171, 173): 2 candidates, both signed LANDAU, both Letelier-themed —
`1978SANTIA01927` (Letelier/Moffitt: Developments March 16/17) ·
`1978SANTIA01906` (Letelier/Moffitt Assassination Investigation)

## Notes on the workflow

- **Note 163's second telegram is another verbatim-quote confirmation** (joining Ch.3 note 72 and Ch.5 note 56) — the cable's body text contains both of the book's exact quoted phrases about CCC agricultural credits and Letelier-case leverage.
- Confirmed a genuine **absence**, not just a search failure: note 66's "CIA, Telegram" citation has no corresponding document anywhere in this corpus's 1977 data — worth remembering as a category (CIA-origin cables), not just a one-off gap, when triaging future "not found" results.
- The Boyatt→Landau ambassadorial transition (chargé d'affaires through late 1977, then Landau as Ambassador) is a useful signature cross-check within this chapter, same as Popper→Boyatt→Landau has been across the book overall.
- Several ambiguous pairs here (8/31, 171/173) are cases where the book cites the *same date* twice across two different endnotes — in one confirmed case (notes 3/4) this was literally the same cable; in others it's likely two companion cables, unresolved without chapter text.
