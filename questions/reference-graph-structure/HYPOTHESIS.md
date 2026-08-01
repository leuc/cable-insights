# What does the corpus's reference graph look like structurally?

**Status:** open — code built, no write-up yet
**Thread of:** —

## Question

Cables reference other cables via `REF:` lines (reftels), forming a directed
graph (vertices = document numbers, edges = references). What does that
graph's structure look like — is it mostly one connected mass or many
fragments, are there hub documents, do communities form, how robust is
connectivity to removing the biggest hubs?

## Hypothesis

Exploratory — no single claim staked out yet; code exists to compute the
standard structural diagnostics (components, degree distribution,
reciprocity, transitivity, assortativity, k-core, PageRank, community
detection), but no finding has been written up.

## Data used

- External: `results/<year>.reftel.norm.ndjson` and `results/<year>.tags.norm.ndjson`
  from the sibling `acp-127` repo (see `data/external/README.md`)
- Code: `code/reftel2graph.py` (builds the directed GraphML) and
  `code/analyze_graph.py` (computes graph statistics), both
  question-exclusive

## Method summary

- `reftel2graph.py` joins normalized reftel + TAGS NDJSON and builds a
  directed citation-style GraphML (vertices = document numbers, edges =
  references), with XML-sanitization for OCR control-character noise.
- `analyze_graph.py` loads that GraphML and computes: weakly-connected
  components, degree distributions, reciprocity, transitivity,
  assortativity, k-core decomposition, PageRank (top broadcasters/
  authorities), Leiden community detection on the 3-core, and "shattered"
  chain analysis after hub removal.

## Result

Open. Both scripts are implemented and runnable — `analyze_graph.py`
outputs JSON stats to stdout and writes a `.giant.graphml` subgraph — but no
`results/` write-up exists yet interpreting those numbers into a finding.
Next step: run the pipeline end-to-end against current `acp-127` output and
write up what the component/PageRank/community numbers actually show.

## Caveats / limitations

None yet documented — this question hasn't reached the stage of having
caveats worth recording.

## Related questions

- [`tags-reference-similarity`](../tags-reference-similarity/HYPOTHESIS.md) —
  shares the same external reference-data source (`*.reftel.norm.ndjson`),
  but does not share code with this question; that question already answers
  "do referencing cables share TAGS," which is complementary to this
  question's structural focus.
