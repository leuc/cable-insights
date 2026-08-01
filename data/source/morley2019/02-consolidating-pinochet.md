# Chapter 2 — Consolidating Pinochet — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 2`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` (normalized `document_date`) narrowed by origin-station prefix on `document_number`, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson` for sender signature + subject match against the book's citation. "Confirmed" = cable text directly verified (signature, addressee, and/or topic match the citation). "Likely" = one candidate is a clearly-best topical fit but the match isn't independently verified (e.g. against the book's own secondary FRUS citation). "Ambiguous" = date+station narrows to multiple same-day candidates with no quoted subject in the book to disambiguate — needs the book's chapter-body narrative (not yet consulted) to pick the right one.

29 of 37 distinct telegram citations in this chapter are now resolved (16 confirmed, 1 likely, 12 ambiguous-with-candidates identified, plus out-of-corpus memos).

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 13 | 285 | Telegram, Department of State to Embassy in Chile, September 21, 1973. DOS/OH | Ambiguous — 6 same-day STATE→SANTIAGO candidates, no quoted subject to disambiguate. See note (a). |
| 14 | 285 | Telegram, Kissinger (Rush) to AmEmb Santiago, September 13, 1973, NARA, RG59 CFPF, ET. | Ambiguous — 6 same-day STATE→SANTIAGO candidates; 2 best-fit (both RUSH-signed press-editorial cables). See note (e). |
| 18 | 286 | Telegram, (Rush) to AmEmb Santiago (Davis), September 24, 1973, DOS/OH; Ibid., Doc. 140, pp. 386-389. | Likely (unconfirmed): **73STATE189464** (raw `1973STATE189464`) — STATE→SANTIAGO (sole addressee), signed RUSH, subject "PRESS REPORTS...ALLEGATIONS" — best topical fit (post-coup torture-allegation press reports) among 7 candidates, but not verified against FRUS Doc.140 pp.386-389. See note (f) for the rest. |
| 22 | 286 | Telegram, Davis to Kissinger, "Chilean Request . . . . ," September 28, 1973, DOS released, June 30, 1999, DNSA. | **Confirmed: 73SANTIAGO4687** (raw `1973SANTIA04687`). SANTIAGO→SECSTATE, 281714Z SEP 73, signed DAVIS, subject "CHILEAN REQUEST FOR DETENTION CENTER ADVISOR AND EQUIPMENT" — exact match. |
| 24 | 286 | Memo NSC, Jorden to Kissinger, September 17, 1973, Ibid., Doc.358, pp.925, 926. Also see Telegram, Rush to Davis, September 21 , 1973, Ibid., Doc.363, p.940. | Memo not in this cable corpus (NSC record). Telegram (Rush to Davis, Sep 21 1973): ambiguous, same 6-candidate set as note 13 — see note (a). |
| 26 | 286 | Telegram, Kissinger (Rush) to Santiago Embassy, October 27, 1973, FRUS, South America, 1973-1976, Doc. ISO, pp.404-405. | **Confirmed: 73STATE212600** (raw `1973STATE212600`). STATE→SANTIAGO, subject "REQUEST TO INTERNATIONAL RED CROSS FOR TENTS," refs SANTIAGO 5175 (the note 22 cable's follow-up thread), signed KISSINGER. |
| 27 | 286 | Telegram, Kissinger to AmEmb Santiago, September 24, 1970, NARA, RG59, CFPF,ET. | Out of corpus range — date is 1970 (corpus covers 1973-1979) and inconsistent with the surrounding Sept/Oct-1973 notes; likely a book/OCR typo for "1973." Not searched under either date yet. |
| 32 | 286 | Telegram, Rush to USUN Mission, New York, September 25, 1973, NARA, RG59, CFPF, ET. | **Confirmed: 73STATE190289** (raw `1973STATE190289`). STATE→USUN NY, subject "RELATIONS WITH NEW CHILEAN GOVERNMENT" (repeating SANTIAGO 4550), signed RUSH. |
| 41 | 287 | Telegram, AmEmb Paris (Irwin) to Kissinger for Hennessy, October 3, 1973, NARA, RG59, CFPF, ET. | **Confirmed: 73PARIS25844** (raw `1973PARIS25844`). PARIS→STATE, subject "CHILEAN CONSULTATIONS WITH PARIS CLUB CHAIRMAN," signed IRWIN — only Chile-related candidate of 11 same-day PARIS→STATE cables; ties into the notes 56-58/60/64 Paris Club debt thread. |
| 43 | 287 | Telegram, Kissinger to AmEmb Santiago, November 2, 1973, NARA, RG59, CFPF,ET. | Ambiguous — 3 same-day STATE→SANTIAGO candidates (IBRD/IDB loans to Chile / copper compensation problems / disposition of remains), no quoted subject. See note (b). |
| 49 | 287 | All quotes in Telegram, Popper to Kissinger, February 11 , 1974, NARA, RG59, CFPF, ET. Also see FBIS: DR: LA, February 19, 1974, p.E1. | Ambiguous — narrowed to 3 same-day SANTIAGO→STATE candidates, all signed POPPER, all part of the same Kubisch-Huerta meeting report. See note (g). |
| 54 | 288 | Telegram, Popper to Kissinger, February 27, 1974, DOS/FOIAe, III | Ambiguous — 4 same-day SANTIAGO→STATE candidates, all signed POPPER (Frank Teruggi torture letter, ×3 sequential septels, or ABC TV stringer detention). See note (h). |
| 55 | 288 | Telegram, Kissinger to AmEmb Santiago, January 30, 1974, NARA, RG59 CFPF,ET | Ambiguous — 7 same-day STATE→SANTIAGO candidates (signed KISSINGER), 3 most topically plausible. See note (i). |
| 56 | 288 | Telegram, AmEmb Bonn (Hillenbrand) to Kissinger, February 15, 1974, Ibid. | **Confirmed: 74BONN2540** (raw `1974BONN02540`). BONN→STATE, subject "CHILEAN DEBT RESCHEDULING MEETING" (Paris Club), signed HILLENBRAND. |
| 57 | 288 | Telegram, Kissinger to AmEmb Bonn et al., February 15, 1974, Ibid. | **Confirmed: 74STATE31838** (raw `1974STATE031838`). STATE→BONN MULTIPLE, subject "PARIS CLUB MEETING ON CHILE DEBT RESCHEDULING" — direct reply to note 56. |
| 58 | 288 | Telegram, AmEmb London (Annenberg) to Kissinger, February 19, 1974, Ibid. | **Confirmed: 74LONDON2192** (raw `1974LONDON02192`). LONDON→STATE/PARIS, subject "PARIS CLUB MEETING ON CHILE DEBT," signed ANNENBERG — same debt-rescheduling thread as notes 56-57. |
| 60 | 288 | Memo to UK Secretary of State, "Chilean Debt," June 13 , 1974, Folder: FCO7/2611 , Renegotiation of Foreign Debt of Chile (paris Club), BNA; Telegram, Kissinger to AmEmb Brussels, et al., March 7, 1974, NARA, RG59, CFPF, ET. | Memo not in this cable corpus (British FCO record). Telegram: **Confirmed: 74STATE46469** (raw `1974STATE046469`). STATE→BRUSSELS MULTIPLE, subject "CHILE: DEBT RESCHEDULING," signed KISSINGER — same Paris Club thread (80/20 vs 70/30 formula negotiations). |
| 64 | 288 | Telegram, Popper to Kissinger, March 12, 1974, NARA, RG59, CFPF, ET | **Confirmed: 74SANTIAGO1195** (raw `1974SANTIA01195`). SANTIAGO→STATE, subject "CHILE DEBT RESCHEDULING," signed POPPER — continues the notes 56-58-60 Paris Club thread. |
| 69 | 288 | Telegram, Popper to Kissinger, April 3, 1974, NARA, RG59, CFPF, ET | Ambiguous — 12 same-day SANTIAGO→STATE candidates (incl. Shultz-Pinochet meeting, Letelier arms-deal accusation, Pinochet on natural rights, copper pricing), no quoted subject. See note (c). |
| 85 | 289 | Telegram, AmEmb Santiago (Thompson) to Kissinger, January 28, 1974, NARA, 157, RG 59, CFPF, ET. | Ambiguous — 7 same-day SANTIAGO→STATE candidates, no quoted subject. See note (d). |
| 87 | 289 | Telegram, AmEmb Santiago (Thompson) to Kissinger, January 28, 1974, NARA, RG59, CFPF, 111174- 12/31174, ET.; Telegram, Popper to Kissinger, February 13 , 1974, Ibid. ; Memo, Bowdler, Weiss to Kissinger, March 14, 1974, DOS/FOIAe, II | First telegram: same ambiguous set as note 85, see note (d). Second telegram (Popper to Kissinger, Feb 13 1974): ambiguous — 10 same-day SANTIAGO→STATE candidates. See note (j). Memo not in this cable corpus. |
| 89 | 289 | Telegram, Popper to Kissinger, April 18 , 1974, NARA, RG59, CFPF, ET. | Ambiguous — 10 same-day SANTIAGO→STATE candidates (same set as note 90's first telegram — same date). See note (k). |
| 90 | 289 | Telegram, Popper to Kissinger, April 18, 1974, FRUS, South America, 1973- 1976, Doc.165, pp.448-449 ; Telegram, Popper to Kissinger for Kubisch, April 22, 1974, NARA, RG59, CFPF, ET. | First telegram: same ambiguous set as note 89, see note (k). Second telegram (Apr 22): ambiguous — 6 same-day SANTIAGO→STATE candidates. See note (l). |
| 91 | 289 | Telegram, Kissinger to AmEmb, Santiago, April 25, 1974, Ibid. | **Confirmed: 74STATE84285** (raw `1974STATE084285`). STATE→SANTIAGO, subject "CHILEAN ARMS REQUESTS," signed KISSINGER — only Chile-relevant candidate among 9 same-day STATE→SANTIAGO cables; content conveys a US arms decision to be relayed to Pinochet personally. |
| 92 | 289 | Telegram, Popper to Kissinger, August 2, 1974, Ibid. | **Confirmed: 74SANTIAGO4591** (raw `1974SANTIA04591`). SANTIAGO→STATE, subject "INTERNATIONAL PROTESTS ON CHILEAN DEATH SENTENCES," signed POPPER — only human-rights-relevant candidate among 8 same-day cables. |
| 100 | 290 | Telegram, Kissinger to AmEmb Santiago, March 18 , 1974, NARA, RG59, CFPF,ET. | **Confirmed: 74STATE53384** (raw `1974STATE053384`). STATE→SANTIAGO, subject "INTER-AMERICAN HUMAN RIGHTS CONSIDERATION OF HUMAN RIGHTS SITUATION IN CHILE," signed KISSINGER — only human-rights-relevant candidate among 5 same-day STATE→SANTIAGO cables. |
| 107 | 290 | Telegram, Popper to Kissinger, April 10, 1975, NARA, RG59, CFPF, ET. | Ambiguous — 9 same-day SANTIAGO→STATE candidates; best subject match ("Chile — Human Rights") has no retrievable body text to verify signature. See note (m). |
| 121 | 291 | Telegram, Popper to Kissinger, July 23, 1974, DOS/FOIAe, I | Ambiguous — 6 same-day SANTIAGO→STATE candidates, all signed POPPER, no distinguishing signal. See note (n). |
| 137 | 291 | Telegram, Popper to Kissinger, August 31 , 1974, NARA, RG59, CFPF, ET. | Ambiguous — 3 same-day SANTIAGO→STATE candidates, all signed POPPER, no distinguishing signal. See note (o). |
| 139 | 291 | Telegram, Kissinger to AmEmb Santiago, September 7, 1974, DOS/FOIAe, I. | **Confirmed: 74STATE196836** (raw `1974STATE196836`). STATE→SANTIAGO, subject "HUMAN RIGHTS IN CHILE," signed KISSINGER — the only STATE→SANTIAGO cable that date (of 62 total STATE cables). |
| 140 | 291 | Telegram, Popper to Kissinger, September 9, 1974, NARA, RG59 CFPF, ET. | **Confirmed: 74SANTIAGO5492** (raw `1974SANTIA05492`). SANTIAGO→STATE, subject "HUMAN RIGHTS IN CHILE" — direct reply to note 139's cable (same subject line), signed POPPER; text promises "will communicate further thoughts after Sept 11 address," setting up note 141. |
| 141 | 291 | Telegram, Popper to DOS (Kissinger), September 11 , 1974, in FRUS, South America, 1973-1976, Doc.173, pp,462-466. | Confirmed via narrative chain (not a quoted-subject match — flagged): **74SANTIAGO5559** (raw `1974SANTIA05559`). SANTIAGO→STATE, subject "ONE YEAR OF THE CHILEAN JUNTA," signed POPPER — a substantial 14-paragraph analytical cable, exactly the "further thoughts after Sept 11 address" promised in note 140, long enough to plausibly span FRUS pp.462-466. A same-day shorter alternative (`1974SANTIA05536`, "Sept 11 Anniversary; Letelier Departure") exists but is a brief logistics report, not an analytical piece. |
| 142 | 291 | Memo, Bowdler, Feldman to Sisco, September 3, 1974, DOS/FOIAe, I; Telegram, Kissinger to AmEmb Santiago, September 7, 1974, Ibid. | Memo not in this cable corpus. Telegram: same citation as note 139 (same sender/recipient/date — the book cites this cable twice) → **74STATE196836**. |

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

**(d) SANTIAGO→STATE, January 28, 1974** (notes 85, 87 1st telegram): 7 candidates —
`1974SANTIA00419` (Chilean refugees in Berlin) ·
`1974SANTIA00424` (Meeting with Foreign Minister) ·
`1974SANTIA00421` (Khmer/Chilean relations) ·
`1974SANTIA00425` (Invitation to Secretary to visit Chile) ·
`1974SANTIA00422` (Facilitative assistance: Rector, University of Chile) ·
`1974SANTIA00429` (GOC role at Foreign Ministers' meeting in Mexico) ·
`1974SANTIA00430` (Foreign Minister requests bilateral with Secretary at Mexico)

**(e) STATE→SANTIAGO, September 13, 1973** (note 14): 6 candidates —
`1973STATE181833` (NYT editorial, signed RUSH) ·
`1973STATE182164` (Danish community message) ·
`1973STATE182136` (WaPo editorial, signed RUSH) ·
`1973STATE182343` (Austrian Embassy message) ·
`1973STATE181843` (news briefing transcript) ·
`1973STATE182527` (CODEL IPU, to Santiago + Mexico)
— two RUSH-signed press-editorial cables (181833, 182136) are the best fit; no way to pick between them without chapter text.

**(f) STATE→SANTIAGO, September 24, 1973** (note 18 — other candidates besides the "likely" 73STATE189464): 6 more —
`1973STATE189618` (press guidance) ·
`1973STATE189879` (W/W AmCits) ·
`1973STATE189999` (Dow Chemical meeting) ·
`1973STATE190077` (W/W Charles Horman) ·
`1973STATE190149` (medical supplies) ·
`1973STATE190162` (Protection of Human Rights — multi-addressee, not sole-Santiago)

**(g) SANTIAGO→STATE, February 11, 1974** (note 49): 3 strong candidates (all signed POPPER, same Kubisch-Huerta meeting report) —
`1974SANTIA00678` (Disposition of Horman remains) ·
`1974SANTIA00679` (Horman/Teruggi cases — specific replies requested) ·
`1974SANTIA00680` (Purpose of Kubisch visit; US policy toward Chile)
— plus 3 weaker candidates: `1974SANTIA00671`, `00675`, `00676`.

**(h) SANTIAGO→STATE, February 27, 1974** (note 54): 4 candidates (all signed POPPER) —
`1974SANTIA00951` / `00956` / `00957` (torture of Frank Teruggi — sequential septels, same story) ·
`1974SANTIA00941` (Detention of ABC TV stringer)
— plus weaker candidates: `00952`, `00953`, `00954`, `00958`.

**(i) STATE→SANTIAGO, January 30, 1974** (note 55): 7 candidates (signed KISSINGER where checked), 3 most plausible —
`1974STATE019994` (Leniz/Saez interview in WaPo) ·
`1974STATE020316` (Economy Minister's call on Assistant Secretary) ·
`1974STATE019743` (Refugees)
— plus weaker candidates: `019799`, `019943`, `019938`, `019990`.

**(j) SANTIAGO→STATE, February 13, 1974** (note 87, 2nd telegram): 10 candidates —
`1974SANTIA00722` (Extradition — Torres/Torres Moreno) ·
`1974SANTIA00714` (January cost of living) ·
`1974SANTIA00731` (Guinea-Bissau/UN) ·
`1974SANTIA00726` (Prisoners released from Chacabuco detention camp) ·
`1974SANTIA00727` (Prep for Commission on Narcotic Drugs meeting) ·
`1974SANTIA00729` (ARA monthly narcotics report) ·
`1974SANTIA00724` (US ferrous scrap exports) ·
`1974SANTIA00710` (Kubisch-Huerta meeting: GOC concern about Peru) ·
`1974SANTIA00730` (Situation report: asylees in diplomatic missions) ·
`1974SANTIA00728` (Kubisch-Huerta meeting: St. George's School)
— the Chacabuco detention-camp and asylees-in-missions cables are topically most plausible for the chapter's human-rights thread, but not distinguishable without chapter text.

**(k) SANTIAGO→STATE, April 18, 1974** (notes 89, 90 1st telegram): 10 candidates —
`1974SANTIA02036` (Visit of Chilean naval training ship Esmeralda) ·
`1974SANTIA02051` (Swiss newsman released) ·
`1974SANTIA02048` (Proposed visit of regional scientific attaché) ·
`1974SANTIA02057` (IPU conference — Chile) ·
`1974SANTIA02060` (Consultations on multilateral trade negotiations) ·
`1974SANTIA02062` (Communications in the Americas conference) ·
`1974SANTIA02058` (FY1974 FMS credit — Chile) ·
`1974SANTIA02047` (World Bank loan plans for Chile in 1974) ·
`1974SANTIA02061` (Air Force trial opens) ·
`1974SANTIA02046` (General Rosson's visit and arms from US)
— "Swiss newsman released" (human rights) and "Air Force trial opens" (repression apparatus) stand out topically but aren't distinguishable as *the* match without the book's FRUS Doc.165 cross-reference or chapter text.

**(l) SANTIAGO→STATE, April 22, 1974** (note 90, 2nd telegram, "for Kubisch"): 6 candidates —
`1974SANTIA02135` (Refugees ex-Chile — UNHCR) ·
`1974SANTIA02150` (ITT negotiations) ·
`1974SANTIA02151` (Air Force trial) ·
`1974SANTIA02144` (Status report on Chilean Jewish community) ·
`1974SANTIA02148` (Ambassador Eberle's call on Pinochet/Merino — addressed to Buenos Aires, not STATE; likely excludable) ·
`1974SANTIA02152` (Pinochet appeals for support)
— "for Kubisch" is an internal attention-line, not a routing addressee, so it doesn't narrow the `To:` field.

**(m) SANTIAGO→STATE, April 10, 1975** (note 107): 9 candidates —
`1975SANTIA02160` (Chile — Human Rights; body text not retrievable in this corpus) ·
`1975SANTIA02184` (World Dairy Expo) ·
`1975SANTIA02157` (Gen. Leigh blasts politicians) ·
`1975SANTIA02155` (Chilean cabinet resigns) ·
`1975SANTIA02159` (Council of the Americas study group visit) ·
`1975SANTIA02166` (US Professor Program lectureship) ·
`1975SANTIA02181` (US Professor Program ed. TV) ·
`1975SANTIA02189` (IVP FY75 program) ·
`1975SANTIA02158` (Behind the Chilean cabinet change, signed POPPER, body text readable)
— best subject match (02160, "Chile — Human Rights") can't be verified since its text isn't retrievable in the corpus; the cabinet-change pair (02155/02158) is a plausible political alternative.

**(n) SANTIAGO→STATE, July 23, 1974** (note 121): 6 candidates (all signed POPPER) —
`1974SANTIA04319` (Kennedy Committee hearings) ·
`1974SANTIA04322` (Status of military trials) ·
`1974SANTIA04329` (ITT) ·
`1974SANTIA04351` (Shlaudeman testimony) ·
`1974SANTIA04343` (Shooting of Chilean ambassador to Lebanon) ·
`1974SANTIA04315` (Secretary Callaway's conversations in Santiago, Jul 22)

**(o) SANTIAGO→STATE, August 31, 1974** (note 137): 3 candidates (all signed POPPER) —
`1974SANTIA05306` (Secretary's dinner for Latin Americans at UNGA) ·
`1974SANTIA05308` (Cuba and OAS) ·
`1974SANTIA05307` (Visit of Deputy Assistant Secretary Blake)

## Notes on the workflow

- **Endnote 27**'s date (September 24, **1970**) falls outside this corpus's 1973-1979 coverage and sits awkwardly among the surrounding September/October 1973 notes — flagged as a likely book/OCR typo for 1973, not yet resolved either way.
- Non-telegram citations in a mixed endnote (NSC memos, FCO/British memos) are noted as out-of-corpus rather than searched, since this corpus only contains State Dept cable traffic.
- "Confirmed" matches were verified by reading `_message_content` (body text) and `Message Attributes` (From/To/Subject/signature) directly from `data/cable-extract/<year>.ndjson` — not inferred from date/station alone.
- Several ambiguous clusters (notes 56-58-60-64, Paris Club debt; notes 139-140-141, human rights) turned out to be narrative threads where confirming one cable's content (references, promised follow-ups) helped confirm its neighbors — worth keeping in mind when the remaining ambiguous sets get chapter-text context, since nearby endnotes are often part of the same cable exchange.
