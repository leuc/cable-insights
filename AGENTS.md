# Agent instructions for cable-insights

This repo investigates the 1973-1979 ACP-127 diplomatic cable corpus,
organized as one hypothesis-driven `questions/<slug>/` per investigation. See
`README.md` for the high-level structure and `questions/README.md` for the
current list.

## Terminology

This is a **reference graph** — cables reference other cables via `REF:`
lines that resolve to another document's MRN (a "reftel"). It is not a
citation graph in the academic sense; use "reference"/"reftel" consistently,
not "citation," when describing this structure or naming files/folders.

## Git

Do not run `git` commands in this repo (status, add, commit, mv, or
otherwise) — the user handles all git operations themselves.
