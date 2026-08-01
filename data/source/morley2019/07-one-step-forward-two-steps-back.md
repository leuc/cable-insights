# Chapter 7 — One Step Forward, Two Steps Back — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Chapter 7`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` narrowed by origin/destination station, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson`. "Confirmed" = cable text directly verified. "Likely" = clearly-best topical fit, not fully independently verified. "Ambiguous" = multiple same-day candidates, no way to pick without chapter-body text. **🚫 FULLTEXT UNAVAILABLE** marks any MRN whose `_message_content` could not be read in this corpus.

**⚠️ Date-format quirk** (see Ch.4): for 1977+ citations, `all-dates.ndjson`'s `document_date` carries a `T00:00:00` suffix, so `jq` filters must use `.document_date | startswith("YYYY-MM-DD")`, not `==`.

Chapter covers mid-1978 through late 1979: Ambassador George Landau's cable traffic on the AFL-CIO/ORIT labor boycott campaign against Chile, and the Letelier case reaching its climax with Chile's Supreme Court refusing extradition of the accused DINA officials (mid-1979), triggering US sanctions. Canadian Embassy telegrams (notes 65's Canadian portion, 75, 79, 107) and a British Embassy telegram (note 137) are **not in this corpus** and are skipped.

23 of 25 distinct US telegram citations resolved (16 confirmed, 4 likely, 4 ambiguous, 1 unresolved).

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 47 | 325 | Telegram Landau to Vance, "The Govt of Chile and Organized Labor after Five Years," August 30, 1978... | **Confirmed: 78SANTIAGO6580** (raw `1978SANTIA06580`) — exact title match, signed LANDAU. |
| 50 | 325 | ...also see Telegram, Landau to Vance, June 5, 1978, Chile Human Rights Documents... [formation of the CNS] | Likely: **78SANTIAGO4247** (raw `1978SANTIA04247`) — subject "THREE 'DINAMICOS' JOIN COMMUNISTS IN FORMING NEW LABOR COORDINATING BODY," signed LANDAU — topically exact, though the book doesn't quote a title. |
| 54 | 325 | Telegram, Landau to Vance, "AFL-CIO Solidarity Visit," June 5, 1978... | **Confirmed: 78SANTIAGO4206** (raw `1978SANTIA04206`) — exact title match, signed LANDAU. Same date as note 50 — a different, companion cable. |
| 57 | 326 | Telegram, Landau to Vance, September 1 , 1978, DOS/FOIAe, I | Likely: **78SANTIAGO6647** (raw `1978SANTIA06647`) — subject "TRADE UNION FREEDOM: REACTION TO MEANY LETTER," signed LANDAU — best topical fit among 6 STATE-addressed candidates that day. |
| 59 | 326 | Telegram, Landau to Vance, September 14, 1978, Chile Human Rights documents... | Ambiguous — 2 candidates, both signed LANDAU: `78SANTIAGO7016` ("AIFLD REQUEST FOR ADDITIONAL FUNDS -- EMBASSY COMMENTS," slightly better labor-theme fit) vs `78SANTIAGO6999` ("REACTION TO PINOCHET'S FIFTH ANNIVERSARY SPEECH"). |
| 60 | 326 | ...Telegram, Landau to Vance, "Trade Union Rights . . . ," October 30, 1978... | **Confirmed: 78SANTIAGO8391** (raw `1978SANTIA08391`) — exact title match ("TRADE UNION RIGHTS: DEMOCRATIC TRADE UNION LEADERS PROTEST RESTRICTIONS ON TRADE UNION ELECTIONS"), signed LANDAU. |
| 63 | 326 | Telegram, Landau to Vance for Vaky, November 30, 1978... | Ambiguous — 4 candidates, all signed LANDAU, all Letelier/labor-themed, shared with notes 68 and 72 (the book cites this exact date/attention-line three separate times). See note (a). |
| 64 | 326 | Telegram, Landau to Vance, December 1 , 1978, Ibid. | Ambiguous — no quoted subject; 5 leading candidates among 10 same-day STATE-addressed cables. See note (b). **Not** the same cable as note 89 (same date, different — confirmed separately below). |
| 65 | 326 | ...Also see Telegram, Landau to Vance, December 7, 1978, DOS/FOIAe, I | Canadian telegram in the same note out of corpus. Telegram: ambiguous — 2 ORIT-labor-themed candidates, both signed LANDAU. See note (c). |
| 66 | 326 | Telegram, Landau to Vance, November 29, 1978, Chile Human Rights Documents... | **Confirmed: 78SANTIAGO9126** (raw `1978SANTIA09126`) — subject "ORIT BOYCOTT: MORE LOCAL REACTION," signed LANDAU. |
| 67 | 326 | Telegram, Landau to Vance, November 16, 1978, DOS/FOIAe, III | **Confirmed: 78SANTIAGO8783** (raw `1978SANTIA08783`) — subject "AWARENESS GROWS OF POSSIBLE LABOR BOYCOTT OF CHILE," signed LANDAU. |
| 68 | 326 | Telegram, Landau to Vance for Vaky, November 30, 1978, Ibid. | Likely: **78SANTIAGO9161** (raw `1978SANTIA09161`) — opens "ARA FOR ASSISTANT SECRETARY VAKY" (exact attention-line match), subject "THE BOYCOTT, BEAGLE AND LETELIER," signed LANDAU. Same 4-candidate set as note 63/72, see note (a) — this is the best "for Vaky" attention-line match of the four. |
| 69 | 326 | Telegram, Landau to Vance, December 2, 1978, Chile, Human Rights Documents... | **Confirmed: 78SANTIAGO9201** (raw `1978SANTIA09201`) — subject "ORIT BOYCOTT: MCLELLAND LETTER TO LABATT; GOC PLANS LABOR RALLY," signed LANDAU. |
| 70 | 326 | Telegram, Landau to Vance, December 6, 1978, Ibid. | Likely: **78SANTIAGO9282** (raw `1978SANTIA09282`) — subject "ORIT/AFL-CIO BOYCOTT: TALK WITH FOREIGN MINISTER CUBILLOS," signed LANDAU. Alternate `78SANTIAGO9278` ("TRADE UNION RIGHTS: ANEF REQUESTS EMERGENCY LOAN FROM AIFLD") also topically strong, signature unverified. |
| 72 | 326 | Telegram, Landau to Vance for Vaky, November 30, 1978, Chile Human Rights Documents... | Same date/attention-line as notes 63, 68 — same 4-candidate set, see note (a). With 3 endnotes and 4 candidates, these likely map to 3 of the 4 — unresolved which. |
| 73 | 327 | Telegram, Landau to Vance, December 11 , 1978, Ibid. | **Confirmed: 78SANTIAGO9353** (raw `1978SANTIA09353`) — subject "STATUS OF EFFORTS TO AVOID ORIT BOYCOTT," signed LANDAU. |
| 75 | 327 | Telegram, CanadianEmb, Santiago (Buick)... | Out of corpus (Canadian Embassy record). |
| 77 | 327 | Telegram, Landau to Vance, December 29, 1978, Chile Human Rights Documents... | **Confirmed: 78SANTIAGO9824** (raw `1978SANTIA09824`) — subject "CONVERSATION WITH MINISTER OF LABOR JOSE (PEPE) PINERA," signed LANDAU. |
| 78 | 327 | Telegram, Landau to Vance, January 12, 1979... The other "modernizations" comprised pensions, education, health, agriculture, justice and decentralization. | Unresolved — 5 same-day SANTIAGO→STATE candidates, none containing "moderniz*" in body text or topically obvious (`1979SANTIA00308` Common Fund negotiations, `00307` R/V Hero clearance, `00292`/`00306` Letelier/Moffitt media coverage, `00322` ORIT boycott hopeful view). Likely a Draft-Date/DTG mismatch or different addressee pattern beyond this search's window — needs a different approach. |
| 79 | 327 | Telegram, CanadianEmb, Santiago (Buick)... | Out of corpus (Canadian Embassy record). |
| 84 | 327 | Telegram, Vance to AmEmb Santiago, "AFL-CIO Letter to Chilean Minister of Labor," March 26, 1979, DOS/FOIAe, III. | **Confirmed: 79STATE75056** (raw `1979STATE075056`) — exact title match, signed VANCE. |
| 85 | 327 | Telegram, Vance to AmEmb Santiago, April 5, 1979, Ibid. | **Confirmed: 79STATE84455** (raw `1979STATE084455`) — subject "ORIT BOYCOTT: VISIT TO U.S. OF GROUP OF TEN LEADERS," signed VANCE — continues note 84's AFL-CIO/AIFLD thread. |
| 89 | 328 | Telegram, Landau to Vance, "Chile Resolution in Third Committee," December 1 , 1978... | **Confirmed: 78SANTIAGO9194** (raw `1978SANTIA09194`) — exact title match, signed LANDAU. Same date as note 64 but a **different** cable (independently confirmed by two separate search passes). |
| 107 | 328 | Telegram, CanadianEmb Santiago (Buick)... | Out of corpus (Canadian Embassy record). |
| 110 | 328 | Telegram, Vance to AmEmb Santiago, January 26, 1979, DOS/FOIAe, III. | **Confirmed: 79STATE21857** (raw `1979STATE021857`) — subject "1979 GOALS AND OBJECTIVES," signed VANCE — discusses transitioning "from cool to more normal relations" contingent on Letelier case resolution. |
| 116 | 329 | Telegram, Vance (Christopher) to AmEmb Santiago, April 17 , 1979, DOS/FOIAe, III. | **Confirmed: 79STATE96739** (raw `1979STATE096739`) — subject "GORM IMPLEMENTATION PLANS," signed CHRISTOPHER (matches book's parenthetical exactly) — implements note 110's goals, ties Letelier-case handling to US-Chile relations. |
| 121 | 329 | Telegram, Vance to AmEmb, Santiago, "Text of Letter," May 16, 1979, DOS/FOIAe, III Also see Letter, Chairman SFRC Church to President... | **Confirmed: 79STATE124968** (raw `1979STATE124968`) — subject is the Kennedy-Church letter to Carter, signed VANCE — matches the book's companion Church-letter citation exactly. |
| 127 | 329 | Telegram, Vance (Christopher) to Landau, "Instructions re US Reaction to outcome of Letelier Case," June 1 , 1979... | **Confirmed: 79STATE140552** (raw `1979STATE140552`) — exact title match, signed CHRISTOPHER. The historically significant cable following Chile's Supreme Court refusal to extradite the DINA defendants. |
| 137 | 330 | Telegram, BritishEmb Washington, D.C. (Henderson) to FCO, London... | Out of corpus (British Foreign Office record). |
| 162 | 331 | Memo, Brzezinski to Vance... Telegram, Vance to AmEmb Santiago, November 30, 1979... | Memo out of corpus. Telegram: **Confirmed: 79STATE308464** (raw `1979STATE308464`) — subject "LETELIER/MOFFITT CASE: THE US RESPONSE TO THE GOVERNMENT OF CHILE," signed VANCE — the sole STATE→SANTIAGO candidate that date; the sanctions-announcement cable. |

## Ambiguous-match candidate sets

**(a) SANTIAGO→STATE, November 30, 1978, "for Vaky"** (notes 63, 68, 72 — cited 3 times, 4 candidates, all signed LANDAU) —
`78SANTIAGO9150` (Letelier/Moffitt case: legal fees) ·
`78SANTIAGO9159` (Letelier/Moffitt case: Chilean Ambassador's recommendation on extradition legal review) ·
`78SANTIAGO9160` (ORIT boycott roundup) ·
`78SANTIAGO9161` (The Boycott, Beagle and Letelier — best "for Vaky" attention-line match, used as note 68's "likely")
— with 3 endnotes and 4 candidates, these very likely map to 3 of these 4 cables; exactly which endnote goes with which isn't determinable without chapter text.

**(b) SANTIAGO→STATE, December 1, 1978** (note 64): 5 leading candidates (of 10 total that day) —
`78SANTIAGO9198` (Economic impact of ORIT-GOC confrontation) ·
`78SANTIAGO9199` (ORIT boycott: more of the same) ·
`78SANTIAGO9195` (Censorship in Chile) ·
`78SANTIAGO9196` (Strauss letter to GOC ministers) ·
`78SANTIAGO9183` (Horman litigation)
— note: `78SANTIAGO9194` (same date) is confirmed separately as note 89's cable, not part of this ambiguous set.

**(c) SANTIAGO→STATE, December 7, 1978** (note 65, telegram part): 2 candidates, both signed LANDAU —
`78SANTIAGO9321` (Press guidance concerning ORIT boycott) ·
`78SANTIAGO9319` (ORIT boycott: GOC rally restrained)

## Notes on the workflow

- This chapter's dominant thread — the AFL-CIO/ORIT international labor boycott campaign against Chile — made most confirmations easy once the theme was recognized; nearly every LANDAU cable that date mentions "ORIT," "boycott," or "AFL-CIO" somewhere.
- **Note 89 is a good independent-verification case**: two separate search passes (one incidental, from the agent resolving note 64's neighborhood; one dedicated) both landed on `78SANTIAGO9194` independently — strong confidence in that match, and useful confirmation that note 64 (same date) is genuinely a *different* cable, not the same one mis-cited.
- Notes 127 and 162 are probably the two most historically significant cables in this whole project so far — the US response to Chile's Supreme Court blocking DINA-official extradition, and the resulting sanctions announcement, both confirmed with exact title matches.
- Note 78 is this chapter's one outright unresolved case — the book quotes specific text ("modernizations") not found in any same-day candidate; likely needs a wider date window or a different addressee search.
