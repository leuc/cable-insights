# Auffant (2022), "Oil for Atoms: The 1970s Energy Crisis and Nuclear Proliferation in the Persian Gulf" — cable findings

Source: *Texas National Security Review* 5(3): 59–82, https://doi.org/10.26153/TSW/42079. Footnotes at page bottoms. Journal page = PDF page + 58.
Auffant cites **26 distinct CFPF cables with explicit MRNs**, all "Central Foreign Policy Files, 1973-79/Electronic Telegrams, RG 59" (most with AAD `createpdf` URLs). All **26 MRNs verified present** in `data/cable-extract/all-dates.ndjson` (matched on `document_number_raw` / `document_number`; date = `dtg.datetime_iso`). All 26 are 1974 except two 1975.

| fn | MRN | p. | Direction / title (paper) | dtg.datetime_iso |
|---|---|---|---|---|
| 8 | `1974PARIS01654` | 62 | Paris→State · "France Floats the Franc" · 19 Jan 1974 | 1974-01-19T21:56Z |
| 58 | `1974BONN01326` | 70 | Bonn→State · "Energy: FRG Flirting with Bilateralism" · 24 Jan 1974 | 1974-01-24T18:52Z |
| 61 | `1974BONN04098` | 70 | Bonn→State · "Iranian Prime Minister's Visit to Bonn" · 14 Mar 1974 | 1974-03-14T17:07Z |
| 62 | `1974TOKYO01127` | 71 | Tokyo→State · "GOJ Views on Bilateral Deals and the Energy Conference" · 25 Jan 1974 | 1974-01-25T09:49Z |
| 63 | `1974TOKYO01784` | 71 | Tokyo→State · "Kosaka Trip to North Africa and Middle East" · ⚠ "Jan. 30" 1974 | **1974-02-07**T09:15Z (paper date off) |
| 63 | `1974TOKYO01337` | 71 | Tokyo→State · "Energy: Yamani in Tokyo" · 30 Jan 1974 | 1974-01-30T09:00Z |
| 64 | `1974TOKYO02473` | 71 | Tokyo→State · "Japanese Negotiations with Iraq on Bilateral Oil Deal" · 25 Feb 1974 | 1974-02-25T09:08Z |
| 65 | `1974TOKYO03150` | 71 | Tokyo→State · "Iranian Export Refinery" · 8 Mar 1974 | 1974-03-08T10:35Z |
| 67 | `1974STATE045027` | 71 | State→Manila · "Joint US-Saudi Economic Commissions" · 7 Mar 1974 | 1974-03-07T19:28Z |
| 68 | `1974JIDDA01123` | 71 | Jeddah→State · "Joint US-Saudi Economic Commissions" · 8 Mar 1974 | 1974-03-08T09:40Z |
| 69 | `1974JIDDA01192` | 71 | Jeddah→State · "Joint US-Saudi Economic Commissions: Saudi Enthusiasm" · 11 Mar 1974 | 1974-03-11T11:53Z |
| 79 | `1974BONN07347` | 74 | Bonn→State · "FRG/Iran Economic Relations" · 7 May 1974 | 1974-05-07T17:14Z |
| 80 | `1974NEWDE06431` | 74 | New Delhi→State · "Indians See Mrs. Gandhi's Iran Visit as Great Success" · 15 May 1974 | 1974-05-15T08:15Z |
| 80 | `1974TEHRAN03593` | 74 | Tehran→State · "Mrs. Gandhi's Visit to Iran" · 6 May 1974 | 1974-05-06T08:15Z |
| 82 | `1974NEWDE06785` | 75 | New Delhi→State · "India's Nuclear Explosion: Swaran Singh Statement" · 22 May 1974 | 1974-05-22T15:30Z |
| 88 | `1974PARIS15305` | 75 | Paris→State · "Interview with Shah" · 24 Jun 1974 | 1974-06-24T15:10Z |
| 89 | `1974TEHRAN05192` | 76 | Tehran→State · "Shah's Alleged Statement on Nuclear Weapons" · 25 Jun 1974 | 1974-06-25T11:38Z |
| 90 | `1974PARIS15445` | 76 | Paris→State · "Further Remarks by Shah on Nuclear Weapons" · 25 Jun 1974 | 1974-06-25T15:37Z |
| 101 | `1974JIDDA03609` | 77 | Jeddah→State · "Saudi Interest Expressed in US-Saudi Nuclear Agreement" · 24 Jun 1974 | 1974-06-24T07:30Z |
| 102 | `1974STATE220253` | 77 | State→Tehran · "US-Iran Cooperation" · ⚠ "May 28" 1974 | **1974-10-06**T22:41Z (paper date off) |
| 102 | `1974KUWAIT03297` | 77 | Kuwait→State · "Kuwaiti Interest in Atomic Energy and Conversion of Sea Water" · 6 Aug 1974 | 1974-08-06T12:48Z |
| 103 | `1974STATE138121` | 78 | State→Jeddah · "Saudi Interest in Nuclear Agreement" · 27 Jun 1974 | 1974-06-27T00:15Z |
| 115 | `1974PARIS29667` | 80 | Paris→State · "Prime Minister Chirac's Visit to Iraq" · 10 Dec 1974 | 1974-12-10T18:30Z |
| 118 | `1974PARIS28641` | 80 | Paris→State · "French Views on Coordination of Nuclear Export Policy" · 29 Nov 1974 | 1974-11-29T17:43Z |
| 123 | `1975PARIS01944` | 80 | Paris→State · "Iraqi Interest in Buying French Natural Uranium Power Reactor" · 23 Jan 1975 | 1975-01-23T15:57Z |
| 125 | `1975PARIS23731` | 81 | Paris→State · "Saddam Hussein Visit to France" · 15 Sep 1975 | 1975-09-15T18:36Z |

## Corpus cross-check (`data/cable-extract/all-dates.ndjson`)

- **All 26 MRNs present**, one record each (no duplicates). `_subject` lines in `1974.ndjson`/`1975.ndjson` match the footnote titles in all 26 cases; `dtg.datetime_iso` matches the paper's dates in all but two cases.
- **fn 63 `1974TOKYO01784`**: dtg is 1974-**02-07** (cable's own DTG `R 070915Z FEB 74`), paper prints "Jan. 30, 1974" — off by 8 days. The other cable in the same footnote (`1974TOKYO01337`, "Yamani in Tokyo") is correctly Jan. 30.
- **fn 102 `1974STATE220253`**: dtg is 1974-**10-06** (DTG `R 062241Z OCT 74`), paper prints "May 28, 1974" — off by ~4.5 months. Subject "US-IRAN COOPERATION" matches the footnote title, and the body context ("within a few months, Iran, Saudi Arabia, and Kuwait all approached the United States seeking reactors") fits October, not May.
- Date field note: 1974 records carry `dtg.datetime_iso` (used here) plus `dates.draft_date`; all 26 have a real dtg (no `sent_date`/`filing_datetime_iso`, consistent with the 1973-76 cohort).

## Content verification against the cable text

Spot-checked the body claims' key phrases against `_message_content` in the per-year files — all present:
- **fn 88 `1974PARIS15305`**: shah's "CERTAINLY, AND SOONER THAN IS BELIEVED" reply (Les Informations, June 23) and the Iranian Embassy's June 24 "TOTALLY INVENTED" denial — both in this cable.
- **fn 62 `1974TOKYO01127`**: "NOT DISHARMONIZING OR DESTABILIZING TO THE WORLD'S ECONOMY."
- **fn 68 `1974JIDDA01123`**: "WE HAD NEVER DISCUSSED ANYTHING REMOTELY COMPARABLE OR AS IMPORTANT WITH ANY OTHER COUNTRY IN THE MIDDLE EAST AND RARELY WITH ANY COUNTRY ANYPLACE."
- **fn 125/130 `1975PARIS23731`**: "SPEND MANY HOURS IN THE BOSOM OF PM CHIRAC'S FAMILY" (red-carpet treatment, Château/restaurant visit).

## Out of scope: FRUS-document references, not CFPF cables

Several body claims about the US-Saudi confrontation are sourced to FRUS 1969–1976, vol. XXXVI ("Energy Crisis, 1969-1974") *documents*, not the CFPF electronic-telegram corpus: fn 46 (Doc 302), fn 48 (Docs 275, 283), fn 49/51 (Doc 303, Akins backchannel — a backchannel message, not a regular cable), fn 66 (Doc 330), fn 71 (Doc 279), fn 72 (Doc 293), fn 74-76 (Doc 345), fn 77 (Doc 353). These are not in `all-dates.ndjson` and are excluded from the table above. The rest of the notes cite French archives (Minutier du délégué général à l'énergie, ANF), CIA CREST/FOIA, and the National Security Archive — none are CFPF cables.
