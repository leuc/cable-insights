# Hulme & Waxman (2026), "Minding the Commitment Gap" — cable/telegram findings

Source: *Security Studies* 35(1): 201-239, https://doi.org/10.1080/09636412.2026.2617892.
All 11 MRNs verified present in `data/cable-extract/all-dates.ndjson` (match on `document_number_raw` and normalized `document_number`; raw `BANGKO` = normalized `BANGKOK`).

| fn | MRN | p. | Direction | Date (paper) | Chapter | Corpus |
|---|---|---|---|---|---|---|
| 76 | — | 223 | Telegram 1377 from Manila | 12 Oct 1959 | NATO/Pactomania | pre-CFPF, no MRN |
| 109 | `1973MANILA09787` | 229 | Manila→State | 27 Aug 1973 | Philippines | ✓ |
| 114 | `1976MANILA11355` | 230 | Manila→Canberra | 2 Aug 1976 | Philippines | ✓ |
| 117 | `1976STATE272078` | 230 | State→Manila | 4 Aug 1976 | Philippines | ✓ (corpus 4 Nov 1976) |
| 119 | `1976STATE268153` | 231 | State→CINCPAC | 9 Nov 1976 | Philippines | ✓ (2 records) |
| 120 | `1976STATE287342` | 231 | State→Manila | 23 Nov 1976 | Philippines | ✓ |
| 121 | `1976STATE287342` | 231 | *Ibid.* (fn 120) | | Philippines | ✓ |
| 122 | `1977MANILA15267` | 231 | Newsom(Manila)→State, No. 15267 | 26 Sep 1977 | Philippines | ✓ (MRN inferred) |
| 124 | `1979STATE004453` | 232 | State→Manila | 6 Jan 1979 | Philippines | ✓ |
| 134 | `1975STATE015015` | 233 | State→CINCPAC | 22 Jan 1975 | Thailand | ✓ |
| 135 | `1975BANGKO12351` | 234 | Bangkok→State | 25 Jun 1975 | Thailand | ✓ |
| 136 | `1975BANGKO18841` | 234 | Bangkok→State | 8 Sep 1975 | Thailand | ✓ |
| 141 | `1977SEOUL06011` | 237 | Seoul→State | 19 Jul 1977 | Conclusion | ✓ |

## Anomalies

- **fn 117** (`1976STATE272078`): paper prints "4 August 1976"; corpus draft date is **4 Nov 1976** — November fits the 1976 cable sequence, so the paper likely mis-printed the month.
- **fn 119** (`1976STATE268153`): two corpus records with the same MRN (both 1976-11-09) — a duplicate; de-duplicate by MRN.
- **fn 122** (`1977MANILA15267`): MRN not printed in source (cited as "No. 15267"); inference confirmed by corpus.
- **fn 76**: 1959 Manila telegram in pre-CFPF Subject Numeric Files — not in the 1973-79 corpus.
