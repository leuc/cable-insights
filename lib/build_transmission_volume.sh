#!/usr/bin/env bash
# Shared build pipeline for data/derived/transmission_volume.csv. Current
# consumers: questions/dash-counter-meaning (main narrative + code/hourly_accounted.py).
# Kept here as shared/foundational rather than question-exclusive, since it's
# a generic per-cable ledger, not a hypothesis finding in itself.
#
# Build data/derived/transmission_volume.csv: one continuous row per cable,
# 1973-1979, with document number, date, station, MRN-based per-station
# serial, and dash-counter state. See transmission_volume.jq for column docs.
#
# Requires the fixed-parser re-extraction at
# $DASHFIX_DIR/<year>.reduced.ndjson (doc/date/dash only; see
# questions/dash-counter-meaning/results/dash_counter_stats.md for how that
# was produced).
set -euo pipefail

DASHFIX_DIR="${DASHFIX_DIR:-/media/jsm/ShareT19/crawl/cables/rebulk-out/dashfix}"
OUT="${1:-data/derived/transmission_volume.csv}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

{
  echo "document_number,date,station,mrn_serial,dash_counter"
  for y in 1973 1974 1975 1976 1977 1978 1979; do
    jq -r -f "$SCRIPT_DIR/transmission_volume.jq" "$DASHFIX_DIR/$y.reduced.ndjson"
  done
} > "$OUT"

echo "wrote $OUT: $(($(wc -l < "$OUT") - 1)) rows" >&2
