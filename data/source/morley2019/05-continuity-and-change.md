# Chapter 5 — Continuity and Change in Chile Policy — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 5`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` narrowed by origin/destination station, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson`. "Confirmed" = cable text directly verified. "Likely" = clearly-best topical fit, not fully independently verified. "Ambiguous" = multiple same-day candidates, no way to pick without chapter-body text. **🚫 FULLTEXT UNAVAILABLE** marks any MRN whose `_message_content` could not be read in this corpus.

**⚠️ Date-format quirk** (see Ch.4): for 1977+ citations, `all-dates.ndjson`'s `document_date` carries a `T00:00:00` suffix, so `jq` filters must use `.document_date | startswith("YYYY-MM-DD")`, not `==`. All 1977 searches below used this fix.

British Foreign Office and Canadian Embassy telegrams cited in this chapter (notes 15, 48, 140) are **not in this corpus** (US State Dept only) and are skipped.

11 of 15 distinct US telegram citations in this chapter are now resolved (8 confirmed, 2 likely, 5 ambiguous). Two notes (9, 59) cite "Kissinger" as recipient for dates in March/May 1977 — Cyrus Vance was Secretary of State by then (Kissinger left office Jan 20, 1977); flagged as a likely book naming-convention holdover rather than a search error.

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 9 | 307 | Telegram, Popper to Kissinger, March 30, 1977, RG59, Office of the Secretary, Subject Files of Amb David H. Popper, Folder: Chrons, Out-going Telegrams, 1977, Box 1 , NA . | Ambiguous — 4 same-day SANTIAGO→STATE candidates, none human-rights-themed. See note (a). Book's "Kissinger" attribution is anachronistic (Vance was Secretary by this date). |
| 15 | 307 | Telegram, BritishEmb, Santiago (Webb) to LAD, FCO (Davies), November 5, 1976, Folder: FCO7/308l, Relations between Chile and the USA, BNA. | Out of corpus (British Foreign Office record). |
| 16 | 307 | Telegram, AmEmb Santiago (Boyatt) to Kissinger, October 27, 1976, DOS/FOIAe, I. | Likely: **76SANTIAGO10335** (raw `1976SANTIA10335`) — SANTIAGO→STATE, subject "VICARIATE OF SOLIDARITY VIEWS ON HUMAN RIGHTS SITUATION AND CHURCH/STATE RELATIONS," signed BOYATT — strong topical fit. Alternate not ruled out: `76SANTIAGO10362` (raw `1976SANTIA10362`, "Chilean government provides mechanism for return of those who fled country," also signed BOYATT). |
| 17 | 307 | Telegram, Popper to Kissinger, January 28, 1977, Ibid. | Ambiguous — 6 same-day SANTIAGO→STATE candidates, all signed POPPER. See note (b). Cited the same date as note 19 — the book is likely citing two *different* cables from this set, most plausibly the two human-rights-specific ones (`1977SANTIA00821`, `1977SANTIA00834`), but which note maps to which can't be determined without chapter text. |
| 18 | 307 | Telegram, AmEmb (Boyatt) to Kissinger, February 14, 1977, Ibid. | **Confirmed: 77SANTIAGO1273** (raw `1977SANTIA01273`). SANTIAGO→STATE, subject "HUMAN RIGHTS COMMISSION (HRC) - 33RD SESSION: CHILE QUESTION," signed BOYATT — only human-rights-relevant candidate of 7 same-day cables. |
| 19 | 307 | Telegram, Popper to Kissinger, January 28, 1977, DOS/FOIAe, I. | Same ambiguous set as note 17, see note (b). |
| 26 | 308 | Telegram, Popper to Kissinger, April 11 , 1977, DOS/FOIAe, I. | Ambiguous/weak — only 2 same-day SANTIAGO→STATE candidates, neither topically compelling. See note (c). |
| 48 | 308 | Telegram, CanadianEmb, Santiago, Ambassador to Under Secretary of State for External Affairs, March 26, 1979, Ottawa, RG25, Interim Container 121 , File: 20-Chile-1-4, Part 14, CNA. | Out of corpus (Canadian Embassy record). |
| 52 | 309 | Telegram, Popper to Vance, March 7, 1977, DOS/FOIAe, I. | **Confirmed: 77SANTIAGO1800** (raw `1977SANTIA01800`). SANTIAGO→STATE, subject "HUMAN RIGHTS COMMISSION: AGENDA ITEM 5, CHILE," signed POPPER — explicitly urges the Department to withdraw co-sponsorship of a Chile resolution; only Chile-relevant candidate of 4 same-day cables. |
| 53 | 309 | Telegram, Vance to AmEmb Santiago, March 8, 1977, Ibid. | Ambiguous/weak — 4 same-day STATE→SANTIAGO candidates, none topically compelling. See note (d). |
| 54 | 309 | Telegram, Vance to AmEmb, Santiago, March 15, 1977, Ibid. | **Confirmed: 77STATE57032** (raw `1977STATE057032`). STATE→SANTIAGO, subject "CHILE -- HUMAN RIGHTS," signed VANCE, refs SANTIAGO 1664 — brief personal note ("Yes, by all means I would appreciate your thoughts on the next stage in our human rights dialogue with the GOC"). |
| 56 | 309 | Telegram, Vance to Emb Santiago, et al., March 9, 1977, DOS/FOIAe, I. Tyson's remarks were immediately disavowed... | **Confirmed — verbatim quote match**: **77STATE51957** (raw `1977STATE051957`). STATE→SANTIAGO/BRASILIA/MULTIPLE, subject "HUMAN RIGHTS COMMISSION: AGENDA ITEM 5, CHILE," contains Brady Tyson's full Geneva statement text including the book's exact quoted passage ("...candid, and untrue to ourselves and to our people... played in the subversion of the previous, democratically-[elected]..."), signed "CATTO UNQUOTE VANCE." |
| 59 | 309 | Telegram, Popper to Kissinger, May 10, 1977, RG59, Office of the Secretary, Subject Files of Amb. David H. Popper, Folder: Chrons, Out-Going Telegrams 1977, Box 1 , NA. | Likely: **77SANTIAGO3835** (raw `1977SANTIA03835`) — SANTIAGO→STATE, subject "GOC DEPRIVES THREE CHILEAN EXILE LABOR LEADERS OF NATIONALITY," signed POPPER — best topical fit of 5 same-day candidates. Book's "Kissinger" attribution is anachronistic (Vance was Secretary by this date); not independently confirmable beyond topical fit. |
| 111 | 312 | Telegram, AmEmb (Boyatt) to Vance, for Christopher and Luers, May 25, 1977, Ibid. Cardinal Silva had been invited to the US to receive an award from Georgetown University. | **Confirmed: 77SANTIAGO4319** (raw `1977SANTIA04319`). SANTIAGO→STATE, opens "FOR DEPUTY SECRETARY CHRISTOPHER AND LUERS FROM CHARGE" (exact attention-line match), body discusses the reception of Cardinal Silva by Deputy Secretary Christopher. |
| 125 | 313 | Memo of Conversation, DOD ... ; Briefing Memo, Devine to Christopher ... Also see Telegram, Vance to AmEmb Santiago, May 28, 1977, Chile Human Rights Documents ... | Both memos out of corpus (DOD/DOS internal records). Telegram: **Confirmed: 77STATE123807** (raw `1977STATE123807`). STATE→SANTIAGO, subject "THE DEPUTY SECRETARY'S MEETING WITH AMBASSADOR CAUAS," signed VANCE — direct readout continuing note 111's Christopher-Cauas thread. |
| 128 | 313 | Telegram, AmEmb (Boyatt) to Vance, June 3, 1977 DOS/FOIAe, I. The Embassy also reported that DINA was "taking the lead in [a] new wave of repression..." Telegram, Popper to Vance, May 18 , 1977, Ibid. | 1st telegram: **Confirmed: 77SANTIAGO4564** (raw `1977SANTIA04564`). SANTIAGO→STATE, subject "USG POLICY REGARDING DISAPPEARANCES IN CHILE," signed BOYATT — topic matches (disappearances), though the book's exact DINA quote wasn't found verbatim in the visible text. 2nd telegram: **Confirmed: 77SANTIAGO4103** (raw `1977SANTIA04103`). SANTIAGO→STATE, subject "HUMAN RIGHTS IN CHILE: SIGNS OF RECIDIVISM," signed POPPER, closes "abuses of basic human rights are again occurring in Chile" — strong match, predates telegram 1 by ~2 weeks matching the book's citation order. |
| 140 | 313 | Telegram, CanadianEmb, Santiago to Under Secretary of State for External Affairs, Ottawa, "Basis of Chilean Foreign Policy 1977," June 20, 1977, RG25, Interim Container 121 , File: 20-Chile-1 -4, Part 7, CNA. | Out of corpus (Canadian Embassy record). |

## Ambiguous-match candidate sets

**(a) SANTIAGO→STATE, March 30, 1977** (note 9): 4 candidates, none human-rights-themed —
`1977SANTIA02579` (Portland Symphony String Quartet touring) ·
`1977SANTIA02580` (Multi-regional energy project) ·
`1977SANTIA02595` (Santiago Voice Radio Net) ·
`1977SANTIA02582` (PARM annual policy/resource assessment)

**(b) SANTIAGO→STATE, January 28, 1977** (notes 17, 19): 6 candidates, all signed POPPER —
`1977SANTIA00821` (Vicariate and Supreme Court fence over missing Chileans) ·
`1977SANTIA00834` (Did missing Chilean communists travel to Argentina?) ·
`1977SANTIA00804` (Chile — Overview) ·
`1977SANTIA00820` (LOS meeting) ·
`1977SANTIA00835` (Antarctica visit) ·
`1977SANTIA00809` (Commander Jaime Lavin)
— the two "missing Chileans" cables (00821, 00834) are the best fits for notes 17/19, but which is which isn't determinable without chapter text.

**(c) SANTIAGO→STATE, April 11, 1977** (note 26): 2 candidates, neither compelling —
`1977SANTIA02891` (International Drug Enforcement Association conference) ·
`1977SANTIA02904` (GOC approves foreign investment, Quebrada Blanca orebody)

**(d) STATE→SANTIAGO, March 8, 1977** (note 53): 4 candidates, none compelling —
`1977STATE050688` (Eximbank/ENDESA credit insurance) ·
`1977STATE051024` (ECLA 17th Session) ·
`1977STATE051090` (Fulbright Commission records) ·
`1977STATE051154` (US v. O'Brian legal case)

## Notes on the workflow

- **Note 56 is another verbatim-quote confirmation** (alongside Ch.3 note 72) — the cable's body text contains the book's exact quoted passage from Brady Tyson's UN statement, not just a topical/date/signature match.
- Notes 17/19 illustrate a re-verification catch: Chapter 4 (note 119, same date) had found only 2 candidates for this exact date+station; re-running the search independently here surfaced 6 — the earlier search was under-inclusive. Worth treating any single-pass candidate count as a lower bound, not definitive, especially for high-volume station/dates.
- Two notes (9, 59) cite "Kissinger" as the addressee for dates when Cyrus Vance was actually Secretary of State — likely a naming-convention holdover in the book's prose (referring to "the Department"/"the Secretary's office" generically) rather than evidence the wrong cable was found.
