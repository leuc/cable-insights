# Sánchez Nateras (2024), "'A Similar Détente': Mexico's Central American Policy, 1978–1982" — cable findings

Source: *Latin American Research Review* 59(2): 361–376, https://doi.org/10.1017/lar.2023.32 (CC-BY open access). Footnotes at page bottoms; journal page = PDF page + 360 (PDF p5 = jp365 … PDF p13 = jp373).
Sánchez Nateras cites **7 distinct CFPF cables with explicit MRNs** (some with a stray space, e.g. "1979MEXICO 12752"), tagged "NARA"/"Central Foreign Policy Files…Electronic Telegrams". All **7 verified present** in `data/cable-extract/all-dates.ndjson` (matched on `document_number_raw` / `document_number`; date = `dtg.datetime_iso`). One MRN (`1979MEXICO12752`) is reused across three footnotes.

| fn | MRN | p. | Cable / paper date | dtg.datetime_iso |
|---|---|---|---|---|
| 5,20,28 | `1979MEXICO12752` | 365,368,370 | American Embassy Mexico→State · Castañeda conversations on Central America · 30 Jul 1979 | 1979-07-30T16:26Z |
| 8 | `1979MEXICO13864` | 366 | US Embassy Mexico→State · "Mexican Assistance for Nicaragua" · 15 Aug 1979 | 1979-08-15T23:29Z |
| 9 | `1979VIENNA11356` | 366 | Embassy Vienna→State · "Visit of Mexican Foreign Minister Jorge Castañeda" · (n.d.) | 1979-10-19T16:17Z |
| 11 | `1979MEXICO17640` | 366 | Embassy Mexico→State · "Conference of Latin American Political Parties" · 13 Oct 1979 | 1979-10-13T01:09Z |
| 17 | `1979STATE194780` | 367 | State→Managua · OAS special meeting · 26 Jul 1979 | 1979-07-26T23:57Z |
| 19 | `1979MANAGU03651` | 367 | American Embassy Managua→State · "(S) Military Assistance to Nicaragua" · 10 Aug 1979 | 1979-08-10T17:36Z |
| 29 | `1979MEXICO12378` | 370 | US Embassy Mexico→State · "Mexico Continues Nicaragua Assistance Efforts" · 23 Jul 1979 | 1979-07-23T23:03Z |

## Corpus cross-check (`data/cable-extract/all-dates.ndjson`)

- **All 7 MRNs present**, one record each (no duplicates). `_subject` lines match the paper's citations in every case; `dtg.datetime_iso` matches the paper's dates where a date is given.
- **fn 9 `1979VIENNA11356`**: paper prints no date for this Vienna cable; dtg is 1979-10-19 (consistent with the Castañeda late-1979 European tour described in the text). Subject "VISIT OF MEXICAN FOREIGN MINISTER JORGE CASTANEDA" confirms it.
- **Station coding**: the corpus normalizes Mexico City as `MEXICOCITY` (raw MRN keeps `MEXICO`), e.g. `1979MEXICO12752` ↔ `79MEXICOCITY12752`. `1979STATE194780` and `1979MANAGU03651` keep their names in both fields.
- All seven are 1979 (corpus years 1973-79); no coverage gaps, no corpus anomalies.

## Content verification against the cable text

Spot-checked body claims against `_message_content`:
- **fn 5 `1979MEXICO12752`**: Castañeda's "EL SALVADOR IS RENT BY TRUE CLASS HATRED FOCUSSED AGAINST THE LANDOWNING CLASS IN GENERAL," corroborating the paper's "true class hatred…landowning class in general."
- **fn 8 `1979MEXICO13864`**: Lambsdorff visit — "CUBAN INFLUENCE IN JUNTA IS NOT YET OVERWHELMING AND THAT WEST CAN BEST SUPPORT GRN MODERATE ELEMENT BY SUPPLYING AS MUCH AID AS POSSIBLE WITHOUT POLITICAL CONDITIONS," matching the paper's quotation.
- **fn 9 `1979VIENNA11356`**: "LP IS FORTHCOMING, HE BELIEVES THERE IS LITTLE CHANCE THAT NICARAGUA WILL GO THE WAY THAT CUBA HAS GONE…," matching "outside help will determine Nicaragua's fate."
- **fn 20 `1979MEXICO12752`** (same cable as fn 5): "THE CUBANS HAVE A GENUINE REVOLUTIONARY MYSTIQUE…THE SOVIETS HAVE NO MASTER PLAN FOR THE WESTERN HEMISPHERE, BEING TOO PREOCCUPIED WITH SALT" — quoted almost verbatim.
- **fn 19 `1979MANAGU03651`**: content on US/FM military-assistance expectations and the "master plan" trope, supporting the paper's Pezzullo-quote usage.

## Out of scope: CIA-FOIA & other archives (not CFPF cables)

Most footnotes use **Mexican archives** (AH-SRE, AGN/DFS), **CIA-FOIA/CREST records** (fns 10, 12, 26, 33, 34, 35, 39/42 — carrying CIA document numbers like `CIA-RDP80T0…`), **FRUS 1977-80 vols. 15 & 23** (fns 21, 23, 24, 30, 31, 32), **German/Soviet** (TsKhSD) and **FRG/GV** archives. Of these, only the 7 CFPF cables above are State-Department electronic telegrams present in the corpus; the CIA-FOIA items are intelligence assessments (1980-82), the FRUS items are published and mostly 1980+, and the rest are non-US records.