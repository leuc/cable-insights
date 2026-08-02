# Content samples: antichain=1 (independent set) vs antichain=0 (excluded)

From `reftel-with-tags-estimated-CD-index-6month-2026-08-02.giant.graphml`.
Referenced by `HYPOTHESIS.md` Result section.

## antichain=1, in-degree=0, out-degree 1-3 (random sample)

Small field posts, cited by no one, each referencing exactly one prior
cable — routine, self-contained replies/reports:

| MRN | date | in | out | cd-type | subject |
|---|---|---|---|---|---|
| 78SANSALVADOR852 | 1978-02-21 | 0 | 1 | consolidating | FY 1980 consular package - El Salvador |
| 78SANJOSE4854 | 1978-11-14 | 0 | 1 | consolidating | Annual listing of business holidays |
| 77NEWDELHI11494 | 1977-08-16 | 0 | 1 | consolidating | DOD elements under ambassadorial authority |
| 79BRUSSELS7207 | 1979-04-18 | 0 | 1 | undefined | Judicial assistance: service of subpoena |
| 76CAIRO12518 | 1976-09-16 | 0 | 1 | undefined | Libyan visas for Egyptians |
| 78MANILA15034 | 1978-08-28 | 0 | 1 | consolidating | Second fisheries development (Pakistan) |
| 79JEDDAH7116 | 1979-10-10 | 0 | 2 | consolidating | Illicit payments - International Systems and Control Corp |

## antichain=0, in-degree ≥10 (random sample)

STATE-originated policy circulars / requests-for-information, each cited
back by 10-197 different field posts:

| MRN | date | in | out | cd-type | subject |
|---|---|---|---|---|---|
| 77STATE207984 | 1977-08-31 | 103 | 0 | disruptive | (preview unavailable) |
| 77STATE147704 | 1977-06-24 | 197 | 0 | disruptive | Legal representation available to Americans arrested abroad |
| 75STATE58837 | 1975-03-15 | 22 | 0 | disruptive | Host government positions for a consumer/producer conference |
| 78STATE212848 | 1978-09-07 | 13 | 1 | disruptive | 1978 Country Reports of Human Rights Practices |
| 78STATE287683 | 1978-11-13 | 136 | 1 | disruptive | Word processing policy and procedures |
| 77STATE186657 | 1977-08-08 | 11 | 0 | disruptive | PRM-10 review as it regards US-NATO strategy |

## Reading

The two groups read exactly as the in-degree numbers predict: `antichain=1`
cables are terminal, self-contained field-post replies that never get
cited back; `antichain=0` cables are STATE circulars/requests-for-input
that many different posts each independently reply to or reference —
which is also *why* they can't be in the maximum antichain: including a
77-citer hub would block all 77 of its citers from also being in the
independent set, so an optimal maximum-antichain selection naturally
excludes high-in-degree hubs in favor of packing in more low-degree
leaves. Note this includes at least one substantively important series
(78STATE212848, the annual Country Reports on Human Rights Practices
process) alongside purely administrative ones (word processing policy) —
`antichain=0` membership tracks *being a widely-replied-to hub*, not
historical significance one way or the other, same caveat as
`cd-index-semantics` found for `cd-index-type: disruptive`.

## Reproducing

Ad hoc, not scripted — loads the graphml via igraph, builds a DataFrame
from `label`/`date`/`antichain`/in-out degree/`cd-index-type`/
`message_preview`, filters by antichain value + degree range, prints
`message_preview`.
