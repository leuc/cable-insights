# Cable content samples: does "disruptive"/"consolidating" read as meaningful?

Pulled from `reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml`.
Referenced by `HYPOTHESIS.md` §1. Median `degree` among defined-type nodes
in this build is **2** (mean 2.19, 75th pct 3) — the high-degree sample
below is the extreme tail, not typical; the low-degree sample is closer to
the modal case.

## High-degree disruptive (top by `degree`, `cd-index` > 0.95)

Dominated by STATE-to-all-posts broadcast circulars — administrative, not
substantive/event-driven:

| MRN | date | degree | cd | subject |
|---|---|---|---|---|
| 78STATE287307 | 1978-12-09 | 344 | 1.000 | US GOALS, OBJECTIVES, AND RESOURCE MANAGEMENT (GORM) FOR FY 81 |
| 76STATE279635 | 1976-12-10 | 327 | 1.000 | REPORTING REQUIREMENT: SECTION 36(A)(7) OF ARMS EXPORT CONTROL ACT |
| 77STATE96600 | 1977-04-28 | 272 | 1.000 | SY TRACKING AND LOCATOR SYSTEM |
| 75STATE194199 | 1975-08-15 | 267 | 0.996 | CONGRESSIONAL HEARINGS ON AMERICAN PRISONERS |
| 79STATE317171 | 1979-12-08 | 229 | 1.000 | PROTECTION OF POST RECORDS |
| 78STATE254951 | 1978-10-06 | 229 | 1.000 | ASSISTANCE TO RELATIVES OF U.S. CITIZENS WHO DIE ABROAD |
| 77STATE38356 | 1977-03-16 | 221 | 0.968 | ANNUAL POLICY AND RESOURCE ASSESSMENTS |
| 78STATE162948 | 1978-06-27 | 220 | 1.000 | LIST OF DOCTORS |
| 75STATE210312 | 1975-09-04 | 216 | 1.000 | SECURITY PROTECTION AFFORDED PUBLIC ACCESS AREAS AT OVERSEAS POSTS |
| 79STATE169825 | 1979-06-30 | 215 | 1.000 | ADP AND WORD PROCESSING INVENTORY AT FOREIGN SERVICE POSTS |
| 78STATE63477 | 1978-03-22 | 209 | 0.955 | FY 1980 GOALS/OBJECTIVES AND RESOURCE MANAGEMENT (GORM) PROCESS |

## Low-degree disruptive (degree 3-5, `cd-index` > 0.95, random sample)

Mixed — some substantive (China trade contacts, Namibia diplomacy,
nuclear-fuel storage), several routine (CODEL logistics, scholarship
admin, travel funding):

| MRN | date | degree | cd | subject |
|---|---|---|---|---|
| 79STATE273037 | 1979-10-18 | 3 | 1.000 | RONG YIREN (CITIC) DISCUSSIONS WITH USG |
| 78USUNNEWYORK1732 | 1978-05-01 | 5 | 1.000 | NAMIBIA: SECRETARY'S MEETING WITH TANZANIAN FOREIGN MINISTER MKAPA (EXDIS) |
| 79PORTMORESBY927 | 1979-06-30 | 3 | 1.000 | Papua New Guinea spent nuclear fuel storage follow-up |
| 74STATE255228 | 1974-11-19 | 3 | 1.000 | POST EVALUATIONS OF PTRS (routine) |
| 76STATE244103 | 1976-10-01 | 4 | 1.000 | CODEL BELL travel notice |
| 76SANAA20 | 1976-01-05 | 5 | 1.000 | Scholarship administration |
| 78STATE247146 | 1978-09-28 | 5 | 1.000 | RSO/TSO travel funding |

## Low-degree consolidating (degree 3-5, `cd-index` < -0.95, random sample)

Consistent pattern: every single one carries multiple REF: lines to the
same ongoing bilateral/topical thread, and gets cited back alongside that
thread:

| MRN | date | degree | cd | subject | own REF:s |
|---|---|---|---|---|---|
| 77STATE86058 | 1977-04-16 | 5 | -1.000 | Alleged ROC discrimination against US vessels | Taipei 2095, 1869, 1576 |
| 76ATHENS7120 | 1976-07-14 | 4 | -1.000 | Aegean continental shelf dispute follow-up | Athens 6985, State 170846/166435, Athens 6706 |
| 75BELGRADE4158 | 1975-08-08 | 4 | -1.000 | Pan Am schedule change, Yugoslav approval | State 185903, Budapest 2521/2553 |
| 79BANGKOK17291 | 1979-05-21 | 4 | -1.000 | Helicopter procurement cost estimate | Bangkok 10859, 12899, 14590 |
| 78OTTAWA3720 | 1978-06-26 | 3 | -1.000 | Foothills pipeline procurement | Ottawa 3718 |
| 79STATE141696 | 1979-06-02 | 4 | -1.000 | US-Japan union nuclear-industry discussions | State 118642, Tokyo 8006/7666/7196 |
| 75STATE145369 | 1975-06-20 | 12 | -1.000 | Parole of Indochina refugees | 8 sequential Bangkok reftels |

## Mechanical check: predecessor count vs. type

```
disruptive with >=1 predecessor: 264,599 (37.8%), mean cd=0.806
disruptive with 0 predecessors:  434,937 (62.2%), mean cd=1.000 (exactly, no exceptions)
```

A cable with zero REF: lines of its own cannot have `bit=1` for any citer
(there is no predecessor to cite), so `CDt` collapses to `nt/nt = 1.0`
deterministically the moment it's cited at all — not a statistical
tendency, a mathematical identity of the formula. See `HYPOTHESIS.md` §1.

## Reproducing

Ad hoc, not scripted (small one-off samples) — see the query pattern in
this session; loads `reftel-with-tags-estimated-CD-index-6month-2026-08-02.graphml`
via igraph, builds a DataFrame from `label`/`date`/`degree`/`cd-index`/
`cd-index-type`/`TAGS`/`message_preview`, filters by type + cd-index
threshold + degree range, and prints `message_preview`.
