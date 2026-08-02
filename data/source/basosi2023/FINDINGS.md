# FINDINGS — Basosi 2023, "Something that apparently troubles the Cubans significantly"

**Slug:** basosi2023
**Reference:** Duccio Basosi, "‘Something that apparently troubles the Cubans significantly’: Jimmy Carter’s attempt to pressure Cuba ‘out of Africa’ through the Non-Aligned Movement, 1977–78," *Cold War History* 24, no. 3 (2023): 359–377. DOI: 10.1080/14682745.2023.2269869.
**Zotero:** item `Q5AFRJWD`, PDF `9XPU6KNS`. Journal page 359 at PDF page 2 → **jp = PDF + 357**.
**Corpus:** resolved against `data/cable-extract/1978.ndjson`, cross-checked with `data/cable-extract/all-dates.ndjson`.

## Summary

Basosi examines Carter's 1977–78 effort to pressure Cuba "out of Africa" through the Non-Aligned Movement. The State Department cables it cites come from **NARA "Access to Archival Databases" (AAD) Electronic Telegrams** — the same CFPF "Electronic Telegrams" set this repo holds. Consequently every cable citation carries **no MRN**, only station + subject + date, and each had to be resolved against the corpus by station and day, then vetted on subject/body. ("AAD" is the archival source tag, not a signal in the corpus.) **24 distinct references were resolved** to corpus MRNs; four (fn 83/86/89/91) could not be located.

## Cable table

All dates are the cable DTG (`dtg.datetime_iso`).

| fn | station (paper) | subject (paper) | date (paper) | resolved MRN | dtg.datetime_iso | corpus subject | match |
|----|-----------------|-----------------|--------------|--------------|------------------|----------------|-------|
| 38a | USINT Havana → State | Ethiopian Somali Hostilities | 25 Jan 1978 | `1978HAVANA00219` | 1978-01-25 | ETHIOPIAN-SOMALI HOSTILITIES: HAVANA UPDATE | exact |
| 38b | US Embassy Belgrade → State | USA Yugoslav consultation | 1 Feb 1978 | `1978BELGRA00759` | 1978-02-01 | USA YUGOSLAV CONSULTATIONS ON SSOD OTHER UN MATTERS | exact |
| 39 | USINT → State | Cuban Participation in Ethiopian-Somali Conflict | 27 Jan 1978 | `1978HAVANA00236` | 1978-01-27 | CUBAN PARTICIPATION IN ETHIOPIAN-SOMALI CONFLICT | exact |
| 59 | Christopher → NMC | Multilateral Affairs | 15 Apr 1978 | `1978STATE097545` | 1978-04-15 | MULTILATERAL AFFAIRS: NON-ALIGNED COORDINATING | exact |
| 64 | US Embassy Abu Dhabi → State | Multilateral Affairs | 9 May 1978 | `1978ABUDH01313` | 1978-05-09 | MULTILATERAL AFFAIRS: NON-ALIGNED COORDINATING COMMITTEE | exact |
| 68 | USINT → State | Cuba to Host NACC Meeting | 5 May 1978 | `1978HAVANA01176` | 1978-05-05 | CUBA TO HOST NACC MEETING | exact |
| 69 | USUN → USINT | NACB Havana Meeting | 16 May 1978 | `1978USUNN01966` | 1978-05-16 | NON-ALIGNED COORDINATING BUREAU (NACB) HAVANA | exact |
| 70 | USINT → State | Non-Aligned Conference | 17 May 1978 | `1978HAVANA01299` | 1978-05-17 | NON-ALIGNED CONFERENCE: ACCESS TO PRESS BRIEFINGS | approx* |
| 72a | US Embassy Colombo → State | Sri Lanka FM Hameed's Statement | 23 May 1978 | `1978COLOMB02392` | 1978-05-23 | SRI LANKA FOREIGN MINISTER A.C.S. HAMEED'S STATEMENT | exact |
| 72b | USUN → State | Tanzania PERMREP's Views | 24 May 1978 | `1978USUNN02099` | 1978-05-24 | ERITREA: VIEWS OF TANZANIAN PERM REP | exact |
| 72c | USUN → State | Indian Diplomats' Views | 30 May 1978 | `1978USUNN02178` | 1978-05-30 | NON-ALIGNED MEETING IN HAVANA: INDIAN DIPLOMAT'S | exact |
| 73a | USINT → State | Non-Aligned Conference Closes | 23 May 1978 | `1978HAVANA01379` | 1978-05-23 | NON-ALIGNED CONFERENCE CLOSES | exact |
| 73b | USINT → State | Non-Aligned Conference | 24 May 1978 | `1978HAVANA01400` | 1978-05-24 | NON-ALIGNED CONFERENCE: FINAL COMMUNIQUE ON AFRICA | approx* |
| 73c | USINT → State | Non-Aligned Conference | 26 May 1978 | `1978HAVANA01430` | 1978-05-26 | NON-ALIGNED CONFERENCE: REMAINING ISSUES | approx* |
| 74 | USINT → State | Non-Aligned Conference Closes | 23 May 1978 | `1978HAVANA01379` | 1978-05-23 | NON-ALIGNED CONFERENCE CLOSES | exact |
| 76 | Vance → All Diplomatic Posts | Multilateral Affairs | 6 Jun 1978 | `1978STATE142045` | 1978-06-06 | MULTILATERAL AFFAIRS: MAY 15-20 MEETING OF THE ... | exact |
| 80a | USUN → State | Non-Aligned Movement | 21 Jun 1978 | `1978USUNN02593` | 1978-06-21 | NON-ALIGNED MOVEMENT: CENTRAL AFRICAN ISSUES | exact |
| 80b | State → All Diplomatic Posts | Multilateral Affairs | 28 Jun 1978 | `1978STATE164031` | 1978-06-28 | MULTILATERAL AFFAIRS: N.Y. TIMES ARTICLE CITED | exact |
| 92 | State → USBEL (msg to Vrhovec) | — | 24 Jul 1978 | `1978BELGRA05405` | 1978-07-24 | PRESIDENTIAL MESSAGE TO NAM | exact |
| 93a | Khartoum → State | OAU Summit | 24 Jul 1978 | `1978KHARTO03325` | 1978-07-24 | OAU SUMMIT: ETHIOPIA/SOMALIA GOOD OFFICES RECS | approx (set) |
| 93b | State → OAU Collective | OAU Summit | 24 Jul 1978 | `1978STATE186342` | 1978-07-24 | OAU SUMMIT: FOREIGN MILITARY PRESENCE IN AFRICA | approx (set) |
| 94 | USBEL → State | Havana-Belgrade NAM Conferences | 20 Jun 1978 (paper prints "20 Jul") | `1978BELGRA04620` | 1978-06-20 | HAVANA-BELGRADE NAM CONFERENCES | date note |
| 95 | USBEL → State | Belgrade Non-Aligned Conference | 26 Jul 1978 | `1978BELGRA05466` | 1978-07-26 | BELGRADE NON-ALIGNED CONFERENCE: THE CUBAN ISSUE | exact |
| 97 | USBEL → State | Non-Aligned Conference | 30 Jul 1978 | `1978BELGRA05563` | 1978-07-30 | BELGRADE NON-ALIGNED CONFERENCE: DAY V - GENERAL | exact |
| 108 | Christopher → ARA Posts | ARA Weekly Highlights | 9 Sep 1978 | `1978STATE229147` | 1978-09-09 | ARA WEEKLY HIGHLIGHTS AUGUST 31 - SEPT. 7 | exact |

`* fn 70/73b/73c:` the paper gives the generic subject "Non-Aligned Conference (…)"; multiple HAVANA telegrams on those days bear more specific corpus subjects. The listed MRN is the closest on the day, verified against the surrounding narrative.

## Unresolved / not in corpus

- **fnn 83, 86, 89, 91 — Christopher → NMC, "Multilateral Affairs", 14 July 1978** (cited in four places): **not re-located** in the corpus. Comprehensive subject/date/`_to` scans of State Department July cables found no "MULTILATERAL AFFAIRS" or NMC-addressed circular dated 14 July. (The closest that exists is `1978STATE176826`, "MULTILATERAL AFFAIRS: ZIONISM-…" on 13 Jul, but it is a Libreville cable, not an NMC-wide circular, and does not fit the content.) Likely outside the released CFPF set or a transcription/date issue.

## Corpus cross-check notes

- Dates are from **`dtg.datetime_iso`** (authoritative). Station norm:
  **HAVANA** = Interests Section (USINT), **USUNN** = USUN Delegation New York, **ABUDH** = Abu Dhabi, **COLOMB** = Colombo, **KHARTO** = Khartoum, **BELGRA** = Belgrade, **STATE** = Department of State circulars.
- **fn 94**: paper prints the "Havana–Belgrade NAM Conferences" cable as **20 July**, but the only subject-exact match `1978BELGRA04620` is DTG **20 June 1978** — a likely month misprint in the paper.
- **fn 93 (a,b)**: the generic subject "OAU Summit" matches a family of Khartoum (`…0322/…0323/…0325/…030…`) and State (`186190/186191/186259/186342`) cables all dated 24 Jul; the specific intended one cannot be definitively pinned. `1978KHARTO03325` and `1978STATE186342` are the primary choices.
- **Content verification**: the fn 74 quotation, "the Non-Aligned Movement is a weak reed on which to lean if we wish to place international political pressure on Cuba", is **present verbatim** in `1978HAVANA01379`.

## Out-of-scope sources cited by this paper (not CFPF telegrams)

FRUS volumes (Vol. I 2014; III 2013; XIII 2013; XVII/1 2016; XIX 2019; XX; XXIII 2016; XXIV); Jimmy Carter Library NSA ("The NLC- …" RAC locations); CIA Records Search Tool (CREST); UN Digital Library (A_33_118-ES, A_33_206-EN); French AMAE Série Europe; Cuban government speeches (cuba.cu); contemporary press (NYT, Associated Press, Globe and Mail). These are left as "outside scope; not CFPF."