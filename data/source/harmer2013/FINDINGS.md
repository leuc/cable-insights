# Harmer (2013), "Two, Three, Many Revolutions? Cuba and the Prospects for Revolutionary Change in Latin America, 1967–1975" — cable findings

Source: *Journal of Latin American Studies* 45(1): 61-89, https://doi.org/10.1017/S0022216X1200123X.
Harmer cites cables by **sender + date only** (no MRNs), style: "Name, American embassy, City, to secretary of state, Date, DOS/CFP", where DOS/CFP = Electronic Telegrams, Dept. of State, Central Foreign Policy Files, NARA (AAD). Each was resolved by date + station lookup in `data/cable-extract/all-dates.ndjson`, then **validated on full message text** in the per-year `.ndjson` (exact quoted phrase + sender signature + `_from`).

| fn | p. | Citation (sender, embassy, date) | Resolved MRN | Text-content validation |
|---|---|---|---|---|
| 109 & 112 | 83 | McClintock, Caracas → SecState, 13 Jul 1974 | `1974CARACA06501` | SUBJ "CUBA"; "problem of Cuba was uppermost in President's mind… would wreck the inter-American system"; signed MCCLINTOCK |
| 110 | 83 | Moskowitz, San Salvador → SecState, 30 Aug 1974 | `1974SANSA03486` | SUBJ "GOES BACKS LIFTING OF CUBA SANCTIONS"; "facts no longer justified the sanctions… to preserve the OAS as a viable institution"; signed MOSKOWITZ |
| 111 | 83 | Meloy, Guatemala → SecState, 13 Sep 1974 | `1974GUATEM05023` | "Guatemala is prepared to go along with the lifting of sanctions against Cuba"; signed MELOY |
| 111 | 83 | Meloy, Guatemala → SecState, 20 Jun 1975 | `1975GUATEM03218` | SUBJ "FOREIGN MINISTER STATES GUATEMALA WILL ABSTAIN AT SAN JOSE"; "to lift Cuba sanctions would have no effect on Guatemalan policy"; signed MELOY |

## Notes

- 4 distinct cables across 5 footnotes (fn 109 and fn 112 cite the same Caracas cable). All are from the cited embassy on the cited date and contain the sentence Harmer quotes.
- Resolution required date+station disambiguation: 14 Caracas cables exist on 13 Jul 1974 (only `06501` is about Cuba); 3 San Salvador cables on 30 Aug 1974 (only `03486`); 11 Guatemala cables on 13 Sep 1974 (only `05023`).
- fn 108 ("Directorate of Intelligence, Central Intelligence Bulletin, 16 July 1973, CREST") is a CIA product, not a State Dept cable — excluded.
