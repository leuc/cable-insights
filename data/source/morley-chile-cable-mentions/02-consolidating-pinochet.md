# Chapter 2 — Consolidating Pinochet — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 2`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` (normalized `document_date`) narrowed by origin-station prefix on `document_number`, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson` for sender signature + subject match against the book's citation. "Confirmed" = cable text directly verified (signature, addressee, and/or topic match the citation). "Ambiguous" = date+station narrows to multiple same-day candidates with no quoted subject in the book to disambiguate — needs the book's chapter-body narrative (not yet consulted) to pick the right one. "Not yet searched" = no lookup attempted yet.

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 13 | 285 | Telegram, Department of State to Embassy in Chile, September 21, 1973. DOS/OH | Ambiguous — 6 same-day STATE→SANTIAGO candidates, no quoted subject to disambiguate. See note (a) below. |
| 14 | 285 | Telegram, Kissinger (Rush) to AmEmb Santiago, September 13, 1973, NARA, RG59 CFPF, ET. | Not yet searched |
| 18 | 286 | Telegram, (Rush) to AmEmb Santiago (Davis), September 24, 1973, DOS/OH; Ibid., Doc. 140, pp. 386-389. | Not yet searched |
| 22 | 286 | Telegram, Davis to Kissinger, "Chilean Request . . . . ," September 28, 1973, DOS released, June 30, 1999, DNSA. | **Confirmed: 73SANTIAGO4687** (raw `1973SANTIA04687`). SANTIAGO→SECSTATE, 281714Z SEP 73, signed DAVIS, subject "CHILEAN REQUEST FOR DETENTION CENTER ADVISOR AND EQUIPMENT" — exact match. |
| 24 | 286 | Memo NSC, Jorden to Kissinger, September 17, 1973, Ibid., Doc.358, pp.925, 926. Also see Telegram, Rush to Davis, September 21 , 1973, Ibid., Doc.363, p.940. | Memo not in this cable corpus (NSC record). Telegram (Rush to Davis, Sep 21 1973): ambiguous, same 6-candidate set as note 13 — see note (a). |
| 26 | 286 | Telegram, Kissinger (Rush) to Santiago Embassy, October 27, 1973, FRUS, South America, 1973-1976, Doc. ISO, pp.404-405. | **Confirmed: 73STATE212600** (raw `1973STATE212600`). STATE→SANTIAGO, subject "REQUEST TO INTERNATIONAL RED CROSS FOR TENTS," refs SANTIAGO 5175 (the note 22 cable's follow-up thread), signed KISSINGER. |
| 27 | 286 | Telegram, Kissinger to AmEmb Santiago, September 24, 1970, NARA, RG59, CFPF,ET. | Out of corpus range — date is 1970 (corpus covers 1973-1979) and inconsistent with the surrounding Sept/Oct-1973 notes; likely a book/OCR typo for "1973." Not searched under either date yet. |
| 32 | 286 | Telegram, Rush to USUN Mission, New York, September 25, 1973, NARA, RG59, CFPF, ET. | **Confirmed: 73STATE190289** (raw `1973STATE190289`). STATE→USUN NY, subject "RELATIONS WITH NEW CHILEAN GOVERNMENT" (repeating SANTIAGO 4550), signed RUSH. |
| 41 | 287 | Telegram, AmEmb Paris (Irwin) to Kissinger for Hennessy, October 3, 1973, NARA, RG59, CFPF, ET. | Not yet searched |
| 43 | 287 | Telegram, Kissinger to AmEmb Santiago, November 2, 1973, NARA, RG59, CFPF,ET. | Ambiguous — 3 same-day STATE→SANTIAGO candidates (IBRD/IDB loans to Chile / copper compensation problems / disposition of remains), no quoted subject. See note (b) below. |
| 49 | 287 | All quotes in Telegram, Popper to Kissinger, February 11 , 1974, NARA, RG59, CFPF, ET. Also see FBIS: DR: LA, February 19, 1974, p.E1. | Not yet searched |
| 54 | 288 | Telegram, Popper to Kissinger, February 27, 1974, DOS/FOIAe, III | Not yet searched |
| 55 | 288 | Telegram, Kissinger to AmEmb Santiago, January 30, 1974, NARA, RG59 CFPF,ET | Not yet searched |
| 56 | 288 | Telegram, AmEmb Bonn (Hillenbrand) to Kissinger, February 15, 1974, Ibid. | **Confirmed: 74BONN2540** (raw `1974BONN02540`). BONN→STATE, subject "CHILEAN DEBT RESCHEDULING MEETING" (Paris Club), signed HILLENBRAND. |
| 57 | 288 | Telegram, Kissinger to AmEmb Bonn et al., February 15, 1974, Ibid. | **Confirmed: 74STATE31838** (raw `1974STATE031838`). STATE→BONN MULTIPLE, subject "PARIS CLUB MEETING ON CHILE DEBT RESCHEDULING" — direct reply to note 56. |
| 58 | 288 | Telegram, AmEmb London (Annenberg) to Kissinger, February 19, 1974, Ibid. | **Confirmed: 74LONDON2192** (raw `1974LONDON02192`). LONDON→STATE/PARIS, subject "PARIS CLUB MEETING ON CHILE DEBT," signed ANNENBERG — same debt-rescheduling thread as notes 56-57. |
| 60 | 288 | Memo to UK Secretary of State, "Chilean Debt," June 13 , 1974, Folder: FCO7/2611 , Renegotiation of Foreign Debt of Chile (paris Club), BNA; Telegram, Kissinger to AmEmb Brussels, et al., March 7, 1974, NARA, RG59, CFPF, ET. | Memo not in this cable corpus (British FCO record). Telegram (Kissinger to Brussels et al., Mar 7 1974): not yet searched. |
| 64 | 288 | Telegram, Popper to Kissinger, March 12, 1974, NARA, RG59, CFPF, ET | **Confirmed: 74SANTIAGO1195** (raw `1974SANTIA01195`). SANTIAGO→STATE, subject "CHILE DEBT RESCHEDULING," signed POPPER — continues the notes 56-58 Paris Club thread. |
| 69 | 288 | Telegram, Popper to Kissinger, April 3, 1974, NARA, RG59, CFPF, ET | Ambiguous — 12 same-day SANTIAGO→STATE candidates (incl. Shultz-Pinochet meeting, Letelier arms-deal accusation, Pinochet on natural rights, copper pricing), no quoted subject. See note (c) below. |
| 85 | 289 | Telegram, AmEmb Santiago (Thompson) to Kissinger, January 28, 1974, NARA, 157, RG 59, CFPF, ET. | Ambiguous — 7 same-day SANTIAGO→STATE candidates, no quoted subject. See note (d) below. |
| 87 | 289 | Telegram, AmEmb Santiago (Thompson) to Kissinger, January 28, 1974, NARA, RG59, CFPF, 111174- 12/31174, ET.; Telegram, Popper to Kissinger, February 13 , 1974, Ibid. ; Memo, Bowdler, Weiss to Kissinger, March 14, 1974, DOS/FOIAe, II | First telegram: same ambiguous set as note 85, see note (d). Second telegram (Popper to Kissinger, Feb 13 1974): not yet searched. Memo not in this cable corpus. |
| 89 | 289 | Telegram, Popper to Kissinger, April 18 , 1974, NARA, RG59, CFPF, ET. | Not yet searched |
| 90 | 289 | Telegram, Popper to Kissinger, April 18, 1974, FRUS, South America, 1973- 1976, Doc.165, pp.448-449 ; Telegram, Popper to Kissinger for Kubisch, April 22, 1974, NARA, RG59, CFPF, ET. | Not yet searched (both telegrams; first is same date as note 89 — likely the same cable). |
| 91 | 289 | Telegram, Kissinger to AmEmb, Santiago, April 25, 1974, Ibid. | Not yet searched |
| 92 | 289 | Telegram, Popper to Kissinger, August 2, 1974, Ibid. | Not yet searched |
| 100 | 290 | Telegram, Kissinger to AmEmb Santiago, March 18 , 1974, NARA, RG59, CFPF,ET. | Not yet searched |
| 107 | 290 | Telegram, Popper to Kissinger, April 10, 1975, NARA, RG59, CFPF, ET. | Not yet searched |
| 121 | 291 | Telegram, Popper to Kissinger, July 23, 1974, DOS/FOIAe, I | Not yet searched |
| 137 | 291 | Telegram, Popper to Kissinger, August 31 , 1974, NARA, RG59, CFPF, ET. | Not yet searched |
| 139 | 291 | Telegram, Kissinger to AmEmb Santiago, September 7, 1974, DOS/FOIAe, I. | Not yet searched |
| 140 | 291 | Telegram, Popper to Kissinger, September 9, 1974, NARA, RG59 CFPF, ET. | Not yet searched |
| 141 | 291 | Telegram, Popper to DOS (Kissinger), September 11 , 1974, in FRUS, South America, 1973-1976, Doc.173, pp,462-466. | Not yet searched |
| 142 | 291 | Memo, Bowdler, Feldman to Sisco, September 3, 1974, DOS/FOIAe, I; Telegram, Kissinger to AmEmb Santiago, September 7, 1974, Ibid. | Memo not in this cable corpus. Telegram (Kissinger to AmEmb Santiago, Sep 7 1974): not yet searched — same date as note 139, possibly the same cable. |

## Ambiguous-match candidate sets

Full candidate lists for the "ambiguous" rows above, from `jq` date+station filtering. Picking the right one requires reading the book's chapter-body narrative (pp. 41-74) around each endnote marker, which hasn't been done yet.

**(a) STATE→SANTIAGO, September 21, 1973** (notes 13, 24): 6 candidates —
`1973STATE188028` (W/W Carol Rich Andreas) ·
`1973STATE188201` (Consultation with Secretary-Designate Kissinger) ·
`1973STATE188497` / `1973STATE188508` (W/W AmCits in Chile) ·
`1973STATE188709` (Copper — meeting with Kennecott rep.) ·
`1973STATE188845` (State Dept news transcript re. Chile)

**(b) STATE→SANTIAGO, November 2, 1973** (note 43): 3 candidates —
`1973STATE216172` (Prospects for IBRD and IDB loans to Chile) ·
`1973STATE216697` (Copper compensation problems) ·
`1973STATE216765` (Disposition of remains)

**(c) SANTIAGO→STATE, April 3, 1974** (note 69): 12 candidates —
`1974SANTIA01690` (IVP grantees Canessa/Montero) ·
`1974SANTIA01679` (IDB loan to Chilean agricultural sector) ·
`1974SANTIA01692` (National intelligence assessment: Chile-Peru conflict potential) ·
`1974SANTIA01691` (1974 IVP grantee Vicente Perez) ·
`1974SANTIA01696` / `1974SANTIA01687` (Shultz-Pinochet meeting, Panama) ·
`1974SANTIA01709` (W/W repatriation of AmCit Marietta Parrish) ·
`1974SANTIA01693` (Orlando Letelier accused in press of arms deal for Allende) ·
`1974SANTIA01700` (ECLA director Iglesias on energy crisis) ·
`1974SANTIA01697` (Pinochet on natural rights) ·
`1974SANTIA01702` (Minister of Mines Yavone: "Arab system" for copper pricing) ·
`1974SANTIA01708` (Discussion with Chileans on US economic assistance, Panama)

**(d) SANTIAGO→STATE, January 28, 1974** (notes 85, 87): 7 candidates —
`1974SANTIA00419` (Chilean refugees in Berlin) ·
`1974SANTIA00424` (Meeting with Foreign Minister) ·
`1974SANTIA00421` (Khmer/Chilean relations) ·
`1974SANTIA00425` (Invitation to Secretary to visit Chile) ·
`1974SANTIA00422` (Facilitative assistance: Rector, University of Chile) ·
`1974SANTIA00429` (GOC role at Foreign Ministers' meeting in Mexico) ·
`1974SANTIA00430` (Foreign Minister requests bilateral with Secretary at Mexico)

## Notes on the workflow

- **Endnote 27**'s date (September 24, **1970**) falls outside this corpus's 1973-1979 coverage and sits awkwardly among the surrounding September/October 1973 notes — flagged as a likely book/OCR typo for 1973, not yet resolved either way.
- Non-telegram citations in a mixed endnote (NSC memos, FCO/British memos) are noted as out-of-corpus rather than searched, since this corpus only contains State Dept cable traffic.
- "Confirmed" matches were verified by reading `_message_content` (body text) and `Message Attributes` (From/To/Subject/signature) directly from `data/cable-extract/<year>.ndjson` — not inferred from date/station alone.
