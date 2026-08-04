# Data instructions

`data/` contains shared inputs and derived datasets. Any question may read
these files; question-specific outputs belong under that question's own
`results/` directory instead.

## Layout

- `source/` contains raw or manually parsed external literature and source
  catalogs. Its MRN index rules are in `data/source/AGENTS.md`.
- `derived/` contains computed datasets reused by at least two questions.
  Keep question-exclusive outputs in the question directory until a second
  consumer genuinely exists.
- `external/` documents the on-disk data contract produced by the sibling
  `acp-127` repo. This repo has no code dependency on that repo; do not
  symlink or copy its code here.

Do not overwrite raw source material. New derived files must document their
inputs and current consumers when they are promoted for sharing.
