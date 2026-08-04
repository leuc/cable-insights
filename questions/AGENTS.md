# Question-investigation instructions

Each subdirectory is one hypothesis-driven investigation. A question's
`results/` is private to that investigation: do not read another question's
results from code and do not write into it from outside that question.

## Adding a question

1. Create `questions/<slug>/` and write `HYPOTHESIS.md` before analysis code.
   Follow the existing structure: Question, Hypothesis, Data used, Method
   summary, Result, Caveats, and Related questions.
2. Keep `**Status:** open` until a finding exists; change it to `answered`
   once `results/` contains the write-up.
3. Put exclusive code in `questions/<slug>/code/`. Read shared inputs from
   `data/` and shared utilities from `lib/`; do not duplicate either.
4. Write findings and result-only CSVs/artifacts only into that question's
   `results/`.
5. Add the question to `questions/README.md`'s index table.
6. Promote a derived dataset or utility to `data/derived/` or `lib/` only
   when a second question genuinely needs it, and document its consumers.
