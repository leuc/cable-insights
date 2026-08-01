# Chapter 4 — A Cooler Embrace — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 4`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` (normalized `document_date`) narrowed by origin/destination-station on `document_number`/`Message Attributes.To`, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson`. "Confirmed" = cable text directly verified. "Likely" = clearly-best topical fit, not fully independently verified (e.g. signature mismatch, or body text unavailable in this corpus). "Ambiguous" = multiple same-day candidates, no way to pick without chapter-body text. **🚫 FULLTEXT UNAVAILABLE** marks any MRN whose `_message_content` could not be read in this corpus (extraction gap) — subject/routing metadata was still usable for matching, but the signature/content itself couldn't be verified.

**⚠️ Data quirk found in this chapter**: for citations dated **1977 or later**, `all-dates.ndjson`'s `document_date` field has a `T00:00:00` suffix (e.g. `"1977-01-18T00:00:00"` vs. 1976's plain `"1976-01-29"`), so a `jq` filter using `==` silently returns zero matches. Use `.document_date | startswith("YYYY-MM-DD")` instead for 1977+ dates. This affects Chapters 5 through 9 going forward (Popper/Boyatt/Landau era through 1980) — carry this fix into every later chapter's search.

British Foreign Office / embassy telegrams cited in several endnotes (LAD, FCO, BritishEmb — e.g. notes 4, 25, 34, 45, 114) are **not in this corpus** (US State Dept only) and are skipped below rather than searched.

18 of ~24 distinct US telegram citations in this chapter are now resolved (13 confirmed, 5 likely, 4 ambiguous).

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 2 | 299 | Telegram, Kissinger to AmEmb, Santiago, January 28, 1976, DOS/FOMe, 1. | **Confirmed: 76STATE21202** (raw `1976STATE021202`). STATE→SANTIAGO, subject "CHILE HUMAN RIGHTS QUESTION AT THE UN HUMAN RIGHTS COMMISSION," signed KISSINGER — only Chile-subject cable of 6 same-day candidates; pairs with note 3. |
| 3 | 299 | Telegram, Popper to Kissinger, January 29, 1976, Ibid. | **Confirmed: 76SANTIAGO745** (raw `1976SANTIA00745`). SANTIAGO→STATE, same subject as note 2, signed POPPER, sent one day after — direct reply. |
| 4 | 299 | Telegram, Popper to Kissinger, February 18, 1976, Ibid. [+ British FCO telegram, out of corpus] | Ambiguous — 10 same-day SANTIAGO→STATE candidates, no quoted subject. See note (s). |
| 6 | 299 | Telegram, Popper to Kissinger, June 28 , 1976, RG59 ... | Ambiguous — 9 same-day SANTIAGO→STATE candidates, no quoted subject. See note (t). |
| 15 | 300 | Telegram, Kissinger to AmEmb Santiago, March 29, 1975, NARA, RG59, CFPF,ET. | **Confirmed: 75STATE71525** (raw `1975STATE071525`). STATE→SANTIAGO, subject "U.S. BANK LOANS TO CHILE," signed KISSINGER — only candidate that date/direction. |
| 23 | 300 | Telegram, AmEmb Santiago (Boyatt) to Kissinger, May 8, 1976, DOS/FOIAe, I. | **Confirmed: 76SANTIAGO4341** (raw `1976SANTIA04341`). SANTIAGO→STATE, subject "TREASURY SECRETARY SIMON'S VISIT TO CHILE: ACCOMPLISHMENTS," signed BOYATT — only candidate that date/direction; ties directly to note 26 (same visit, same day). |
| 25 | 301 | Despatch + Telegram, both British Embassy/FCO | Out of corpus (British Foreign Office records). |
| 26 | 301 | Telegram, AmbEmb Santiago (Bell) to Kissinger, May 8, 1976, DOS/FOIAe, I [+ WP/FBIS press citations, not cables] | Likely: **76SANTIAGO4341** (raw `1976SANTIA04341`) — same cable as note 23 (Simon-visit accomplishments), only STATE-addressed candidate that date. **Flagged**: book attributes this to "(Bell)" but the cable is signed BOYATT — name mismatch unresolved; could be a different companion cable Bell signed, or a book error. |
| 34 | 301 | Telegram, British Embassy Santiago (Haskell) to LAD, FCO | Out of corpus (British Foreign Office record). |
| 40 | 301 | Quotes in Telegram, Kissinger to AmEmb Santiago, March 17, 1976, Public Library of US Diplomacy (Wikileaks). | Likely: **76STATE64984** (raw `1976STATE064984`) — STATE→SANTIAGO, subject "CODEL MOFFETT," "SUBSTANCE OF THEIR REMARKS AT THEIR MARCH 17 PRESS CONFERENCE" (Rep. Tom Harkin's congressional delegation on the Chile visit — Harkin quoted elsewhere in the cluster calling human rights "a disaster"). Part of a 4-cable same-day CODEL Moffett cluster, all STATE→SANTIAGO: `76STATE64826` (press statement, Harkin "disaster" quote), `76STATE64828` (press statement v2, refs SANTIAGO 2107), `76STATE64985` (follow-up). The book's "Quotes in" framing best fits 64984 (a verbatim-remarks cable) but any of the 4 is plausible without chapter text. |
| 45 | 302 | Gerald Ford presidential document + Telegram, British Embassy Washington | Out of corpus (British Foreign Office record; the Ford document isn't a cable either). |
| 52 | 302 | Telegram, Popper to Kissinger, March 23, 1976, DOS/FOIAe, I | Ambiguous — 13 same-day SANTIAGO→STATE candidates; two human-rights-themed, both **🚫 FULLTEXT UNAVAILABLE**: `1976SANTIA02450` ("CHILE: HUMAN RIGHTS -- RELATIONS WITH UN HUMAN RIGHTS COMMISSION WORKING GROUP") and `1976SANTIA02451` ("HUMAN RIGHTS SITUATION IN CHILE") — can't verify signature even if the right one is picked. See note (u). Same cable as note 73 (identical citation). |
| 55 | 302 | Telegram, AmEmb Santiago (Boyatt) to Kissinger, for Rogers, April 21 , 1976, DOS/FOIAe, I. | **Confirmed: 76SANTIAGO3641** (raw `1976SANTIA03641`). SANTIAGO→STATE, subject "REFUGEE AND MIGRATION AFFAIRS: PAROLE OF CHILEAN DETAINEES AND REFUGEES," signed BOYATT — only human-rights-relevant candidate among 9 same-day cables. |
| 56 | 303 | Telegram, AmEmb Santiago (Boyatt) to Kissinger, April 24, 1976, NARA, RG59, CFPF, ET. | **Confirmed: 76SANTIAGO3779** (raw `1976SANTIA03779`). SANTIAGO→STATE, subject "TALKING POINTS FOR SECRETARY'S CALL ON PRESIDENT PINOCHET DURING OASGA," signed BOYATT — the only SANTIAGO→STATE candidate that date. |
| 57 | 303 | See, for instance, Telegram, Kissinger (Robinson) to USUN Mission, York, May 21 , 1976, DOS/FOIAe, I. | **Confirmed: 76STATE125318** (raw `1976STATE125318`). STATE→USUN NEW YORK, subject "CHILE: RELATIONS WITH UN HUMAN RIGHTS COMMISSION WORKING GROUP," text signed "POPPER UNQUOTE ROBINSON" (Robinson relaying Popper's message) — exact match to the book's "(Robinson)" attribution. |
| 59 | 303 | Telegram, Popper to Kissinger, May 29, 1976, Ibid. | Ambiguous — 4 same-day SANTIAGO→STATE candidates; two topically plausible, both **🚫 FULLTEXT UNAVAILABLE**: `1976SANTIA05083` (GOC reaction to non-delivery of F-5 aircraft), `1976SANTIA05128` (Secretary's June 8 lunch with Pinochet). Other 2: `05124` (press opportunities), `05127` (transitional quarter nominations). |
| 73 | 303 | Telegram, Popper to Kissinger, March 23, 1976, DOS/FOIAe, I. | Same date/citation as note 52 — same ambiguous set, see note (u). |
| 81 | 304 | Telegram, Kissinger to AmEmb Santiago, June 19, 1976, Ibid. | Likely: **76STATE151434** (raw `1976STATE151434`) — **🚫 FULLTEXT UNAVAILABLE**. STATE→SANTIAGO, subject "LETTER TO CHILEAN FOREIGN MINISTER CARVAJAL FOR THE AMBASSADOR" — only Chile-diplomacy-relevant candidate of 5 same-day cables, but signature unverified since the body text can't be read. |
| 97 | 305 | Telegram, Kissinger (Robinson) to USDEL Secretary, December 28, 1976, NARA, RG59, CFPF, ET. | Not found — searched Dec 26-29 1976 for STATE-origin cables to any "USDEL SECRETARY" variant, zero matches; likely a routing-address format not caught by this search, or a Draft-Date/DTG mismatch beyond the window tried. Needs a different search approach. |
| 101 | 305 | Telegram, Kissinger to AmEmb Buenos Aires, et al., August 23, 1976, Ibid. Also see Dinges, The Condor Years, pp.6-7. | Likely (high confidence): **76STATE209192** (raw `1976STATE209192`) — **🚫 FULLTEXT UNAVAILABLE**. STATE→BUENOS AIRES/MONTEVIDEO/SANTIAGO/LA PAZ (matches "et al."), subject "OPERATION..." (truncated) — almost certainly the well-known "Operation Condor" warning cable (multi-addressee pattern + exact date match + book's own "see Dinges, *The Condor Years*" gloss immediately after), but not "Confirmed" per this file's own definition since the message text — one of this corpus's known gaps for some high-profile cables — can't be read to verify. |
| 103 | 305 | Telegram, Popper to Kissinger, August 24, 1976, DNSA. | Ambiguous/weak — only 2 SANTIAGO→STATE candidates that date, neither topically compelling (`1976SANTIA08208` FY-1977 IV nominations; `1976SANTIA08209` visa eligibility of MIR-affiliated individuals). Book cites DNSA (National Security Archive) as the release channel, not NARA/AAD — this cable may not be in this corpus's source collection at all. |
| 106 | 305 | Telegram, AmbEmb, Santiago (Popper) to DOS, September 21 , 1976, FRUS, South America, 1973-1976, Doc.247, pp.664-665. | **Confirmed: 76SANTIAGO9212** (raw `1976SANTIA09212`). SANTIAGO→STATE, subject "ASSASSINATION OF ORLANDO LETELIER," signed POPPER — an 82-line analytical assessment (DINA, Southern Cone intelligence services, terrorism abroad) matching the book's 2-page FRUS citation; two shorter same-subject companions that day (`9214`, `9225`, 33/39 lines) are situation reports, not analytical, less likely fit. |
| 110 | 306 | Kathleen Teltsch NYT citation [not a cable]; Telegram, Kissinger to AmEmb Santiago, October 16, 1976, DOS/FOIAe, I | **Confirmed: 76STATE257200** (raw `1976STATE257200`). STATE→SANTIAGO, subject "UN GENERAL ASSEMBLY CONSIDERATION OF HUMAN RIGHTS IN CHILE," signed KISSINGER — exact topical match to the book's companion NYT citation ("U.N. Unit Says Chile Abuses Widen"). |
| 114 | 306 | Telegram, British Embassy Washington (Webb) to LAD, FCO | Out of corpus (British Foreign Office record). |
| 119 | 306 | Telegram, Popper to Kissinger, January 28, 1977, DOS/FOIAe, I; Telegram, Popper to Kissinger, January 18, 1977, Chile Human Rights Documents ... | 2nd telegram (Jan 18, 1977): **Confirmed: 77SANTIAGO487** (raw `1977SANTIA00487`). SANTIAGO→STATE, subject "CHILE: A REVIEW ON HUMAN RIGHTS," signed POPPER — only candidate that date/direction. 1st telegram (Jan 28, 1977): ambiguous — narrowed to 2 candidates, both POPPER, both "missing/disappeared" themed: `1977SANTIA00821`/**77SANTIAGO821** ("Vicariate and Supreme Court fence over missing Chileans") vs `1977SANTIA00834`/**77SANTIAGO834** ("Did missing Chilean communists travel to Argentina?"). See note (v). |

## Ambiguous-match candidate sets

**(s) SANTIAGO→STATE, February 18, 1976** (note 4): 10 candidates —
`1976SANTIA01256` (Navy trial of Luis Corvalán et al.) ·
`1976SANTIA01287` (Refugee/migration affairs: parole of Chilean detainees) ·
`1976SANTIA01264` (Embassy and the Chilean Christian Democrats) ·
`1976SANTIA01254` (Interview with Chilean Air Force General Leigh) ·
plus 6 weaker/unlisted candidates.

**(t) SANTIAGO→STATE, June 28, 1976** (note 6): 9 candidates —
`1976SANTIA06259` (Air Force officers' dissatisfaction with Pinochet) ·
`1976SANTIA06251` / `1976SANTIA06269` (Parole of Chilean Detainees and Refugees) ·
plus 6 weaker/unlisted candidates.

**(u) SANTIAGO→STATE, March 23, 1976** (notes 52, 73): 13 candidates —
`1976SANTIA02450` (Chile: Human Rights — relations with UN Human Rights Commission Working Group — **🚫 FULLTEXT UNAVAILABLE**) ·
`1976SANTIA02451` (Human Rights Situation in Chile — **🚫 FULLTEXT UNAVAILABLE**) ·
`1976SANTIA02398` (AmSpec Mazzocco) · `1976SANTIA02400` (DCM residence furnishing) · `1976SANTIA02411` (Chilean Decision 24 initiative) · `1976SANTIA02449` (Visas Eagle) · `1976SANTIA02412` (narcotics protocol) · `1976SANTIA02460` (USEF report) · `1976SANTIA02468` (narcotics financing) · `1976SANTIA02464` (OPIC insurance) · `1976SANTIA02470` (Radio Balmaceda) · `1976SANTIA02471` (GOC human rights overseers report — **🚫 FULLTEXT UNAVAILABLE**) · `1976SANTIA02469` (women leaders training).

**(v) SANTIAGO→STATE, January 28, 1977** (note 119, 1st telegram): 2 candidates, both signed POPPER —
`1977SANTIA00821` / **77SANTIAGO821** (Vicariate and Supreme Court fence over missing Chileans) ·
`1977SANTIA00834` / **77SANTIAGO834** (Did missing Chilean communists travel to Argentina?)
(4 other same-day candidates ruled out as off-topic.)

## Notes on the workflow

- **Date-format quirk (see warning above)**: 1977+ `document_date` values carry a `T00:00:00` suffix in `all-dates.ndjson`; exact-match `jq` filters must switch to `startswith()` for these years.
- Several notes (52/73, 59, 81, 101) hit a **🚫 FULLTEXT UNAVAILABLE** gap in this corpus even after narrowing to 1-2 strong candidates by subject — a different failure mode than "too many candidates," and worth flagging explicitly (not just in prose) since it means the match is metadata-only, never content-verified. Going forward, every chapter file should mark this explicitly per-candidate whenever `_message_content` can't be read.
- Note 26's signature mismatch (book says "Bell," cable signed "Boyatt") is the first outright discrepancy found between the book's attribution and the matched cable — flagged rather than silently resolved.
- Note 101 is very likely the historically well-known "Operation Condor" warning telegram (Kissinger's aborted August 1976 attempt to caution Condor states) — the multi-addressee pattern (Buenos Aires/Montevideo/Santiago/La Paz) and the book's own Dinges cross-reference both point to it strongly, even without body text.
