# Questions

Each subfolder is one hypothesis-driven investigation over the corpus. Every
question owns its `results/` exclusively — no other question reads or writes
into it. Shared inputs live in `../data/` and shared code lives in `../lib/`;
a question only keeps `code/` for scripts that are genuinely exclusive to it.

To add a new question: create `questions/<slug>/`, write `HYPOTHESIS.md`
first (see any existing one for the template), then add code/results as the
investigation proceeds, then add a row below.

| Slug | Question | Status |
|---|---|---|
| [`dash-counter-meaning`](dash-counter-meaning/HYPOTHESIS.md) | What does the unlabeled dash-counter header line represent? | answered |
| [`filing-time-vs-dtg`](filing-time-vs-dtg/HYPOTHESIS.md) | How does the counter's `filing_time` subfield relate to DTG, and does the lag change over time? | answered |
| [`tags-reference-similarity`](tags-reference-similarity/HYPOTHESIS.md) | Do cables that reference each other share similar TAGS codes? | answered |
| [`tags-coverage-vs-faq`](tags-coverage-vs-faq/HYPOTHESIS.md) | How much of the real TAGS data does the FAQ-derived Subject TAGS mapping explain? | answered |
| [`reference-graph-structure`](reference-graph-structure/HYPOTHESIS.md) | What does the corpus's reference graph look like structurally (components, hubs, communities)? | open |
