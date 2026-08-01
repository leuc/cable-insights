# Build one continuous cable-by-cable "transmission volume" ledger.
#
# Shared build pipeline for data/derived/transmission_volume.csv. Current
# consumers: questions/dash-counter-meaning (main narrative + code/hourly_accounted.py).
#
# Input: dashfix/<year>.reduced.ndjson lines ({doc, date, dash}), the full-corpus
# re-extraction produced with the fixed src/patterns/dash_counter.py (see
# questions/dash-counter-meaning/results/dash_counter_stats.md). One record in,
# one CSV row out - includes every
# document, not just ones with a usable dash-counter, so downstream consumers can
# see the whole corpus and decide what counts as "accounted for".
#
# Columns:
#   document_number  - e.g. "1977STATE013174"
#   date             - DTG date_iso (falls back to Draft Date), or "" if unknown
#   station          - parsed from document_number, e.g. "STATE", "TOKYO"
#   mrn_serial       - the per-station/per-year sequential number embedded in
#                       document_number (the "MRN" reference-number counter,
#                       see docs/REFTEL.md's MRN format) - null if unparseable
#                       (a small number of document numbers carry stray
#                       characters, e.g. "1973SALVAD0)034" - noise from NARA's
#                       own reproduction process, not OCR; station/mrn_serial
#                       are null for these but the row is still emitted)
#   dash_counter     - the ACP-127 dash-counter line's counter value (the
#                       "state of the counter" at this cable) - null if
#                       missing/unparsed for this document
#
# Usage (looped over years, one continuous CSV with a single header):
#   echo "document_number,date,station,mrn_serial,dash_counter"
#   for y in 1973 1974 1975 1976 1977 1978 1979; do
#     jq -r -f scripts/transmission_volume.jq "dashfix/$y.reduced.ndjson"
#   done
# See scripts/build_transmission_volume.sh for the full runnable pipeline.

select(.doc != null)
| (
    # jq's capture() produces no output at all (not an error, not null) when the
    # regex doesn't match - try/catch can't intercept that, since nothing is
    # thrown. Guard with test() first so every document still emits a row.
    if (.doc | test("^[0-9]{4}[A-Z]+[0-9]+$"))
    then (.doc | capture("^(?<yr>[0-9]{4})(?<station>[A-Z]+)(?<serial>[0-9]+)$"))
    else null
    end
  ) as $cap
| [
    .doc,
    (.date // ""),
    ($cap.station // ""),
    (if $cap.serial then ($cap.serial | tonumber) else null end),
    (.dash.counter // null)
  ]
| @csv
