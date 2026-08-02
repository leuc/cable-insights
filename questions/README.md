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
| | TODO Main path analysis: search path count (SPC), search path link count (SPLC), search path node pair (SPNP), SPLC: really good at finding "long" running discussions? | new |
| | Can we predict links between cables that don't have any? (based on subject, TAGS, office distribution and address similarity, with measured time lag fall off by station) | new |
| [`dash-counter-meaning`](dash-counter-meaning/HYPOTHESIS.md) | What does the unlabeled dash-counter header line represent? | answered |
| [`filing-time-vs-dtg`](filing-time-vs-dtg/HYPOTHESIS.md) | How does the counter's `filing_time` subfield relate to DTG, and does the lag change over time? | answered |
| [`tags-reference-similarity`](tags-reference-similarity/HYPOTHESIS.md) | Do cables that reference each other share similar TAGS codes? | answered |
| [`tags-coverage-vs-faq`](tags-coverage-vs-faq/HYPOTHESIS.md) | How much of the real TAGS data does the FAQ-derived Subject TAGS mapping explain? | answered |
| [`reference-graph-structure`](reference-graph-structure/HYPOTHESIS.md) | What does the corpus's reference graph look like structurally (components, hubs, communities)? | open |
| [`publication-cable-graph-signal`](publication-cable-graph-signal/HYPOTHESIS.md) | What graph attributes signal that a cable is one a historian would cite? | answered |
| [`address-reference-similarity`](address-reference-similarity/HYPOTHESIS.md) | Do cables that reference each other share the same office distribution selection/values and/or the same FM/TO/INFO addresses? | answered |
| [`reference-time-lag`](reference-time-lag/HYPOTHESIS.md) | What is the time gap between a cable and the cable(s) it references, and does it differ by station (STATE vs. field posts)? | answered |
| [`cd-index-semantics`](cd-index-semantics/HYPOTHESIS.md) | How does the CD-index semantic (imported from patent-citation literature) translate to a telegram reference network? | answered |
| [`antichain-semantics`](antichain-semantics/HYPOTHESIS.md) | What cable and graph properties do nodes on the antichain hold? | answered |
