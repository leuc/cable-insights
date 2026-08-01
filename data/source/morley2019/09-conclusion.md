# Conclusion — telegram/cable mentions in endnotes

Source: Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s: Frustrated Ambitions* (Cambridge Scholars Publishing, 2019), endnotes section (`Notes to Conclusion`).

MRN matching method: `jq` date-range filter on `data/cable-extract/all-dates.ndjson` narrowed by origin/destination station, cross-checked by reading `_message_content`/`Message Attributes` in `data/cable-extract/<year>.ndjson`.

Only one telegram/cable citation appears in this chapter's endnotes (`Notes to Conclusion`, p.338) — the chapter is mostly a retrospective essay citing books, interviews, and one 1987 declassified memo (out of corpus; the corpus covers 1973-1979 State Dept cable traffic only, not later intelligence-community records).

| Endnote # | Page | Citation (as printed, OCR-extracted) | MRN match |
|---|---|---|---|
| 2 | 338 | Telegram, Landau to Vance, March 17, 1978, DOS/FOIAe, I. | Ambiguous — same date/direction as [Ch.6 notes 171/173](06-muddying-the-waters.md), set (g): 2 candidates, both signed LANDAU, both Letelier-themed — `78SANTIAGO1927` (raw `1978SANTIA01927`, "Letelier/Moffitt: Developments March 16/17") vs `78SANTIAGO1906` (raw `1978SANTIA01906`, "Letelier/Moffitt Assassination Investigation"). This may be a *third* citation of the same date as Ch.6's pair (following the notes-63/68/72 pattern in Ch.7, where one date served multiple endnotes) — worth checking whether the book is citing the same underlying cable across chapters once chapter-body text resolves which is which. |

## Notes on the workflow

- This chapter has essentially no cable-matching work of its own — its one telegram citation reuses a candidate pair already fully identified while resolving Chapter 6. No new search infrastructure or agents were needed.
- The chapter's other endnote (note 1, not a telegram) cites a 1987 memo from Secretary of State George Shultz to President Reagan analyzing a CIA report on Pinochet's role in the Letelier assassination — a good example of the book's endnotes reaching well past this corpus's 1973-1979 coverage even in a chapter with almost no cable citations at all.
