# cable-insights

Derived research and analysis over the ACP-127 diplomatic telegram corpus
(1973-1979) extracted by the sibling [`acp-127`](../acp-127) repo. That repo
does extraction only — raw cable text to structured NDJSON, plus reference
(reftel)/TAGS normalization. This repo does everything downstream of that:
reference-graph construction and analysis, statistical cross-checks against
external sources (a 2016 academic paper, a FOIA-obtained dataset), and
investigative write-ups about patterns found in the corpus.

For the `acp-127` data contract (what NDJSON this repo expects and how to
regenerate it), see [`data/external/README.md`](data/external/README.md).
Nothing here imports `acp-127`'s code — only its output files, on disk.

## Workflow

This repo is organized around one hypothesis/question per investigation, in
the spirit of a lab notebook: each question in
[`questions/`](questions/README.md) states what's being asked before it's
answered, and owns its findings exclusively. Code and data that multiple
questions can legitimately share live at the top level; a question's own
results never do.

```
cable-insights/
├── data/
│   ├── source/     # raw, unmodified external inputs (e.g. FOIA data)
│   ├── external/   # documents the acp-127 dependency — no data checked in
│   └── derived/    # shared computed datasets, reused by 2+ questions
├── lib/            # shared code: build pipelines + reusable utilities
└── questions/
    └── <slug>/
        ├── HYPOTHESIS.md   # the question, hypothesis, status, result
        ├── code/           # question-exclusive code only
        └── results/        # question-exclusive output — never shared
```

See [`questions/README.md`](questions/README.md) for the current list of
investigations and their status, and [`AGENTS.md`](AGENTS.md) for the rules
to follow when adding a new one.
