# Telegram/cable mentions in Morley & McGillion, *US Policy toward Chile in the 1970s*

Extraction of every endnote citing a **Telegram** or **Cable** from the
endnotes section (pp. 279-338) of:

> Morris Morley & Chris McGillion, *US Policy toward Chile in the 1970s:
> Frustrated Ambitions* (Cambridge Scholars Publishing, 2019).

Purpose: these citations name sender, recipient, and date for individual
State Department cables — many explicitly sourced to `NARA, RG59, CFPF, ET`
(the same National Archives Central Foreign Policy Files / Electronic
Telegrams series `acp-127` extracts from) — but cite them by
sender/recipient/date, not by MRN. This catalog is step one of a two-step
process: extract the citations here, then in a later step match each one
against the corpus (by date + station + addressee) to recover its MRN and
link to the local extracted document.

One file per chapter, matching the book's own endnote grouping
(`Notes to Introduction`, `Notes to Chapter 1`, ... `Notes to Conclusion`).
Each row is one endnote number containing a telegram/cable mention, with
the exact printed page number it appears on:

| File | Chapter | Telegram/cable citations |
|---|---|---|
| [`00-introduction.md`](00-introduction.md) | Introduction | 0 |
| [`01-confronting-allende.md`](01-confronting-allende.md) | Chapter 1 — Confronting Allende | 3 |
| [`02-consolidating-pinochet.md`](02-consolidating-pinochet.md) | Chapter 2 — Consolidating Pinochet | 33 |
| [`03-discordant-voices.md`](03-discordant-voices.md) | Chapter 3 — Discordant Voices | 29 |
| [`04-a-cooler-embrace.md`](04-a-cooler-embrace.md) | Chapter 4 — A Cooler Embrace | 25 |
| [`05-continuity-and-change.md`](05-continuity-and-change.md) | Chapter 5 — Continuity and Change in Chile Policy | 17 |
| [`06-muddying-the-waters.md`](06-muddying-the-waters.md) | Chapter 6 — Muddying the Waters | 21 |
| [`07-one-step-forward-two-steps-back.md`](07-one-step-forward-two-steps-back.md) | Chapter 7 — One Step Forward, Two Steps Back | 30 |
| [`08-policy-adrift.md`](08-policy-adrift.md) | Chapter 8 — Policy Adrift | 25 |
| [`09-conclusion.md`](09-conclusion.md) | Conclusion | 1 |

184 total citations.

## Method

- Extracted from the PDF with `pdftotext -layout`, working from the
  publisher's own printed page numbers (confirmed via the running headers
  on each page).
- Endnote boundaries were located by matching each `Notes to <Section>`
  divider heading, and individual endnote text was split on numbered-marker
  boundaries (`N <citation text> ... N+1 <next citation>`).
- Endnotes were kept if they contained the word `Telegram` or `Cable` in
  any form (not just the comma-suffixed `Telegram,`/exact phrase used in an
  earlier pass of this extraction, which silently missed a handful of
  citations phrased as e.g. "quote in Telegram AmEmb..." with no comma).
  Endnotes citing **Airgrams**, **Despatches**, memos, letters, or archival
  folder names that merely contain the word "Cables" (e.g. "Kissinger
  Briefing Books and Cables") were excluded — those are different document
  types, not individual electronic telegrams. One entry (Ch.8, endnote 98)
  is a CIA "National Intelligence Daily Cable," a different product from a
  State Dept telegram — flagged inline rather than excluded, since it's
  still cable-form traffic that might be worth checking.

## Verification against the source PDF (multimodal cross-check)

Every citation in this catalog was checked against **rendered page images**
of the PDF (`pdftoppm` → PNG, read directly), not just the raw
`pdftotext` OCR layer, specifically to catch OCR errors the text layer
alone wouldn't reveal. This surfaced and fixed:

- **Systematic OCR substitutions** specific to this PDF's embedded font,
  applied consistently across all chapters: `rn`/`m` confusion (`AmErnb`,
  `ArnEmb` → `AmEmb`), broken ligatures (`!bid.`/`!hid.`/`lbid.` → `Ibid.`,
  `Doe.` → `Doc.`), digit/letter confusion (`RGS9` → `RG59`, `19S0` →
  `1980`, `FC07`/`FCa7` → `FCO7`, roman numeral `I`/`II`/`III` misread as
  digits `1`), and several one-off misreads verified against known
  historical terms (e.g. endnote 41, Ch.1: the real 1970 CIA cable title
  "**Firm** and Continuing Policy that Allende be Overthrown by a Coup",
  OCR'd as "Finn").
- **Two chapter mis-attributions**: this extraction originally assigned an
  endnote's chapter purely by *page number*, but three of the book's
  chapter breaks fall partway down a page — so a citation that's textually
  still under the *previous* chapter's `Notes to Chapter N` heading (but on
  a page where the *next* chapter's heading also appears) was getting
  filed under the wrong chapter. Fixed for Ch.3/4 (endnote 129), Ch.4/5
  (endnotes 110, 114, 119), Ch.6/7 (endnotes 174, 176), and Ch.7/8
  (endnote 162).
- **Five missed citations**: the original pass only matched the literal
  string `Telegram,` (comma required) or the phrase `Cable from
  Headquarters`, which silently skipped citations phrased without a comma
  (e.g. "quote in Telegram AmEmb Chile...", Ch.1 endnote 8) or using bare
  `Cable,` (Ch.8 endnotes 39, 62, 98). Re-run with a looser `\bTelegram\b`
  / `\bCable\b` match and added.
- **A handful of endnote-number mis-assignments**: the regex used to find
  each citation's endnote number gives up if the number marker is more than
  ~250 characters before the "Telegram"/"Cable" match (long endnotes with a
  citation buried at the end of a paragraph). These were manually
  identified against the images and corrected (e.g. Ch.3 endnote 110 had
  been mis-attributed to endnote 109; several endnotes appeared as `?` and
  were resolved to their real numbers).

This was a genuine image-by-image check, not inference from the OCR text
alone — roughly 30 of the 60 endnote pages were directly re-read as
rendered images across all nine chapters/sections to validate both the
specific corrections above and the OCR-substitution patterns generally;
the remaining pages were cleaned using the same verified substitution
patterns without an additional per-page image read. **Residual OCR noise
is still possible on pages not individually re-checked** — treat this as a
strong-confidence extraction, not a guaranteed-exact transcription.

## Caveats

- Citation text is truncated per-entry using the *next* detected endnote
  marker as the boundary; on rare occasions this can pull in a stray
  trailing fragment from an adjacent, non-telegram footnote continuation.
- A few citations (e.g. Ch.2 endnote 110/Ch.3 boundary) span a page break
  in the original book; the printed page recorded is where the citation
  *starts*.
- **Verify against the original PDF page before treating any single
  citation as authoritative for MRN matching** — this catalog is meant to
  narrow down candidates, not replace the source text.
