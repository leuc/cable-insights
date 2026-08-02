# External dependency: the `acp-127` sibling repo

Nothing in this repo imports `acp-127`'s Python code. Everything here reads
NDJSON/CSV that `acp-127`'s pipeline produces on disk. To regenerate the
inputs these scripts expect, run `acp-127`'s pipeline first:

```bash
# In ../acp-127
python3 -m src.extractor <paths...>                              # raw text -> NDJSON
python3 -m src.reftel_normalize *.reftel.ndjson > all-mrns.ndjson  # reference normalization
python3 -m src.tags_normalize *.new5.ndjson > all-tags.ndjson      # TAGS normalization
```

See `../acp-127/README.md` and `../acp-127/AGENTS.md` for the full extraction
pipeline and NDJSON schema.

## What this repo expects, and from where

- `results/<year>.reftel.norm.ndjson` and `results/<year>.tags.norm.ndjson`
  (per year, 1973-1979) — normalized reference and TAGS records, consumed by
  `questions/reference-graph-structure/code/reftel2graph.py` and
  `questions/tags-reference-similarity/code/tags_reference_similarity.py`.
- `results/<year>.ndjson` (per year, 1973-1979) — raw per-document extractor
  output (`Message Attributes."Document Number"`, `_distribution`, `_from`,
  `_to`, `_info`, among other fields not yet consumed by any question here).
  Consumed by
  `questions/address-reference-similarity/code/address_reference_similarity.py`,
  joined to `results/<year>.reftel.norm.ndjson` via the raw Document Number
  (`document_number_raw`). Exposed to this repo at `data/cable-extract/`
  (symlinked to the same underlying directory as `acp-127/results`).
- `$DASHFIX_DIR/<year>.reduced.ndjson` — a separate fixed-parser
  re-extraction (doc/date/dash only), consumed by
  `lib/build_transmission_volume.sh` to build
  `data/derived/transmission_volume.csv`. Defaults to
  `/media/jsm/ShareT19/crawl/cables/rebulk-out/dashfix` if `$DASHFIX_DIR`
  isn't set — override it to point at your own re-extraction.

None of this NDJSON is checked into this repo (it's large, regenerable, and
owned by `acp-127`). If a script here can't find its input, regenerate it
from `acp-127` first using the commands above.
