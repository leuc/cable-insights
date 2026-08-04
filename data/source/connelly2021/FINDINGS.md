# Connelly et al. (2021), “New evidence and new methods for analyzing the Iranian revolution as an intelligence failure” — cable findings

**Source:** Matthew Connelly, Raymond Hicks, Robert Jervis, and Arthur
Spirling, “New evidence and new methods for analyzing the Iranian revolution
as an intelligence failure,” *Intelligence and National Security* 36(6):
781–806. DOI: [10.1080/02684527.2021.1946959](https://doi.org/10.1080/02684527.2021.1946959).

**Zotero:** item `PX6PI7SP`, PDF `6BB2EG5V`.

The article explicitly names **15 distinct CFPF cables** by MRN. All 15 are
present in `data/cable-extract/1978.ndjson`; subjects match the article's
references.

| Fn | MRN | Corpus date | Subject |
|---:|---|---|---|
| 38 | `1978TEHRAN00389` | 1978-01-11 | SERIOUS RELIGIOUS DISSIDENCE IN QOM |
| 38 | `1978TEHRAN00665` | 1978-01-18 | MORE REACTION TO QOM DEMONSTRATIONS |
| 38 | `1978TABRIZ00004` | 1978-01-22 | DEMONSTRATIONS IN TABRIZ |
| 38 | `1978TEHRAN00961` | 1978-01-26 | RELIGION AND POLITICS: QOM AND ITS AFTERMATH |
| 45 | `1978TEHRAN07242` | 1978-08-01 | MORE ON RECENT RIOTS |
| 45 | `1978TEHRAN07882` | 1978-08-17 | IRAN: WHERE ARE WE NOW AND WHERE ARE WE GOING? |
| 56 | `1978TEHRAN03892` | 1978-04-25 | GOI DISCOURAGEMENT OF DISSIDENT POLITICAL ACTION |
| 56 | `1978STATE110017` | 1978-04-29 | GOI DISCOURAGEMENT OF DISSIDENT POLITICAL ACTION |
| 57 | `1978TEHRAN04582` | 1978-05-14 | GOI DISCOURAGEMENT OF DISSIDENT POLITICAL ACTION |
| 57 | `1978TEHRAN05390` | 1978-06-06 | DISCUSSION WITH SHAH ON IRAN'S DOMESTIC PROBLEMS |
| 58 | `1978TEHRAN08217` | 1978-08-29 | RECOMMENDATION FOR PRESIDENT TO SHAH LETTER |
| 60 | `1978TEHRAN09431` | 1978-09-28 | IRANIAN PERMREP TO UNITED NATIONS URGES USG |
| 61 | `1978STATE231682` | 1978-09-13 | SAVAK |
| 67 | `1978STATE283811` | 1978-11-07 | MESSAGE TO FOREIGN MINISTER |
| 68 | `1978TEHRAN10962` | 1978-11-08 | MESSAGE TO FOREIGN MINISTER GENSCHER |

## Method and caveats

- Extracted explicit MRNs from the PDF text, including MRNs in the body,
  footnotes, and the references section.
- Deduplicated repeated MRNs; footnote numbers above preserve where each
  reference appears.
- Dates and subjects come from the local extracted corpus, not from an
  assumption based on the article's prose.
- The article also analyzes thousands of cables in aggregate. Those corpus
  mentions are not individually listed here unless the article gives an
  explicit MRN.
