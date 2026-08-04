# Agent instructions for cable-insights

This repo investigates the 1973-1979 ACP-127 diplomatic cable corpus,
organized as one hypothesis-driven `questions/<slug>/` per investigation. See
`README.md` for the high-level structure and `questions/README.md` for the
current list.

## The sharing rule

- `data/` (source + derived datasets) may be read by any question's code.
- `lib/` (shared code — build pipelines, reusable utilities) may be used by
  any question.
- A question's `results/` belongs to that question exclusively. Never read
  another question's `results/` from code, and never write into it from
  outside that question's own investigation.
- Default new code to a question's own `code/`. Only promote something to
  `lib/` once a second question genuinely needs it — don't pre-emptively
  share.

## Terminology

This is a **reference graph** — cables reference other cables via `REF:`
lines that resolve to another document's MRN (a "reftel"). It is not a
citation graph in the academic sense; use "reference"/"reftel" consistently,
not "citation," when describing this structure or naming files/folders.

## Adding a new question

1. `mkdir -p questions/<slug>`, then write `HYPOTHESIS.md` first — before
   writing analysis code. Copy the structure from any existing
   `questions/*/HYPOTHESIS.md` (Question / Hypothesis / Data used / Method
   summary / Result / Caveats / Related questions).
2. Mark `**Status:** open` until there's a finding; flip to `answered` once
   `results/` has a write-up.
3. Put question-exclusive code under `questions/<slug>/code/`. Reach into
   `data/` for shared inputs and `lib/` for shared code; don't duplicate
   either.
4. Write findings only into `questions/<slug>/results/` — the write-up
   markdown plus any result-only CSVs/artifacts.
5. Add a row to `questions/README.md`'s index table.
6. If the new question's derived data or code turns out to be useful to an
   existing or future question, promote it into `data/derived/` or `lib/`
   at that point (not before), and note the current consumers in a header
   comment — see `lib/build_transmission_volume.sh` for the pattern.

## External data dependency

This repo has no code dependency on the sibling `acp-127` repo — only a data
contract (NDJSON/CSV it produces on disk). See `data/external/README.md` for
exactly what's expected and how to regenerate it; that dependency is
documented there only, nothing is symlinked or copied into this repo.

## Related-literature MRN index

- When adding or changing a parsed source under `data/source/`, update
  `data/source/related_literature.json` with each MRN that resolves in
  `data/cable-extract/all-dates.ndjson`.
- Store the source-printed/full MRN in `mrn_full`, the corpus
  `document_number` in `mrn_normalized`, and point `source_ids` at a source
  entry whose metadata includes the DOI (or `null` when none exists), a
  human-readable `citation`, and the exact parsed Markdown file.
- Validate the index against
  `data/source/related_literature.schema.json`; do not add unresolved or
  pre-CFPF references to this normalized index.

## Git

Do not run `git` commands in this repo (status, add, commit, mv, or
otherwise) — the user handles all git operations themselves.
