#!/usr/bin/env python3
"""Test: what is the time gap between a cable and the cable(s) it
references, and does this differ by originating station -- particularly
STATE vs. field posts?

Loads data/cable-extract/<year>.reftel.norm.ndjson (document_number -> date,
extracted_references) for all years combined (references cross year
boundaries). For every resolved reference pair, computes
`lag_days = citing.date - cited.date` and breaks the distribution down by
the citing document's station (parsed from document_number via
lib.station.parse_station) -- STATE is ~29% of the corpus and, being the
Department itself rather than a field post, is expected to reference (and
be referenced by) a much wider spread of prior traffic than a field post
mostly citing its own recent reporting stream.

A same-size random-pair null baseline (citing.date - random_other_doc.date)
is reported alongside: since dated documents are scattered across the whole
1973-1979 corpus, a random pair's gap should be far wider and less centered
near zero than a genuine reference.

Usage (from repo root)::

    python3 questions/reference-time-lag/code/reference_time_lag.py
        [--results-dir data/cable-extract] [--years 1973 1974 ...]
        [--sample N] [--seed S] [--top-stations N] [--min-station-n N]
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from lib.station import parse_station

_ALL_YEARS = [1973, 1974, 1975, 1976, 1977, 1978, 1979]


def _parse_iso(s: str | None) -> date | None:
    if not s:
        return None
    try:
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))
    except (ValueError, AttributeError):
        return None


def load_reftel(path: Path) -> dict[str, tuple[date | None, list[str]]]:
    """document_number -> (date, extracted_references)."""
    result: dict[str, tuple[date | None, list[str]]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            doc = d.get("document_number")
            if not doc:
                continue
            result[doc] = (_parse_iso(d.get("date")), d.get("extracted_references") or [])
    return result


class LagStats:
    """Accumulates day-gap (citing.date - cited.date) samples."""

    def __init__(self):
        self.values: list[int] = []
        self.negative = 0

    def add(self, days: int):
        self.values.append(days)
        if days < 0:
            self.negative += 1

    def summary(self) -> dict:
        n = len(self.values)
        if n == 0:
            return {"n": 0}
        vs = sorted(self.values)

        def pct(p):
            return vs[min(n - 1, int(p * n))]

        return {
            "n": n,
            "mean": statistics.mean(vs),
            "median": statistics.median(vs),
            "stdev": statistics.stdev(vs) if n > 1 else 0.0,
            "p10": pct(0.10),
            "p25": pct(0.25),
            "p75": pct(0.75),
            "p90": pct(0.90),
            "negative_pct": self.negative / n * 100,
        }


def _print_summary_row(label: str, s: dict):
    if s["n"] == 0:
        print(f"  {label:28s} no data")
        return
    print(
        f"  {label:28s} n={s['n']:>10,}  mean={s['mean']:>8.1f}d  median={s['median']:>6.1f}d  "
        f"stdev={s['stdev']:>8.1f}  p10={s['p10']:>5.0f}  p25={s['p25']:>5.0f}  "
        f"p75={s['p75']:>6.0f}  p90={s['p90']:>7.0f}  neg%={s['negative_pct']:>5.2f}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Time gap (days) between a citing cable and the cable(s) it references, by station."
    )
    parser.add_argument("--results-dir", default="data/cable-extract", help="Directory with *.reftel.norm.ndjson")
    parser.add_argument("--years", nargs="+", type=int, default=_ALL_YEARS, help="Years to include")
    parser.add_argument("--sample", type=int, default=None, help="Sample this many citing documents; default: use all")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for sampling and the baseline")
    parser.add_argument("--top-stations", type=int, default=25, help="How many stations to show in the per-station table, ranked by pair count")
    parser.add_argument("--min-station-n", type=int, default=200, help="Minimum resolved-pair count for a station to appear in the per-station table")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    results_dir = Path(args.results_dir)

    sys.stderr.write(f"Loading reftel data for years {args.years} ...\n")
    docs: dict[str, tuple[date | None, list[str]]] = {}
    for year in args.years:
        path = results_dir / f"{year}.reftel.norm.ndjson"
        if not path.exists():
            sys.stderr.write(f"  WARNING: {path} not found, skipping\n")
            continue
        year_docs = load_reftel(path)
        sys.stderr.write(f"  {path}: {len(year_docs):,} documents\n")
        docs.update(year_docs)

    sys.stderr.write(f"Total documents: {len(docs):,}\n")

    dated_doc_keys = [d for d, (dt, _) in docs.items() if dt is not None]
    sys.stderr.write(f"Documents with a usable date: {len(dated_doc_keys):,}\n")

    citing_docs = [d for d, (dt, refs) in docs.items() if dt is not None and refs]
    sys.stderr.write(f"Citing documents (dated, with >=1 reference): {len(citing_docs):,}\n")

    if args.sample is not None and args.sample < len(citing_docs):
        citing_docs = rng.sample(citing_docs, args.sample)
        sys.stderr.write(f"Sampled down to {len(citing_docs):,} citing documents\n")

    overall_actual = LagStats()
    overall_random = LagStats()
    state_actual = LagStats()
    nonstate_actual = LagStats()
    unknown_station_actual = LagStats()
    by_station_actual: dict[str, LagStats] = defaultdict(LagStats)

    total_ref_pairs = 0
    resolved_ref_pairs = 0
    citing_docs_with_resolved_ref = 0

    for doc in citing_docs:
        citing_date, refs = docs[doc]
        station = parse_station(doc)
        had_resolved = False
        for ref in refs:
            total_ref_pairs += 1
            cited = docs.get(ref)
            if cited is None or cited[0] is None:
                continue
            resolved_ref_pairs += 1
            had_resolved = True
            lag = (citing_date - cited[0]).days
            overall_actual.add(lag)
            if station == "STATE":
                state_actual.add(lag)
            elif station:
                nonstate_actual.add(lag)
            else:
                unknown_station_actual.add(lag)
            if station:
                by_station_actual[station].add(lag)

            # Random baseline: one random other dated document per resolved
            # reference, compared against the SAME citing document.
            random_doc = rng.choice(dated_doc_keys)
            random_date = docs[random_doc][0]
            overall_random.add((citing_date - random_date).days)
        if had_resolved:
            citing_docs_with_resolved_ref += 1

    print("=== Reference Time-Lag Test (citing.date - cited.date, in days) ===")
    print(f"Years: {args.years}")
    print(f"Citing documents considered: {len(citing_docs):,}")
    if citing_docs:
        print(
            f"Citing documents with >=1 in-corpus resolved reference: "
            f"{citing_docs_with_resolved_ref:,} "
            f"({citing_docs_with_resolved_ref / len(citing_docs) * 100:.2f}%)"
        )
    if total_ref_pairs:
        print(
            f"Reference pairs: {total_ref_pairs:,} total, "
            f"{resolved_ref_pairs:,} resolved to an in-corpus dated document "
            f"({resolved_ref_pairs / total_ref_pairs * 100:.2f}%)"
        )
    print()

    print("--- Overall: actual references vs. random-pair baseline ---")
    _print_summary_row("actual", overall_actual.summary())
    _print_summary_row("random baseline", overall_random.summary())
    print()

    print("--- STATE vs. non-STATE citing documents (actual references only) ---")
    _print_summary_row("STATE", state_actual.summary())
    _print_summary_row("non-STATE", nonstate_actual.summary())
    _print_summary_row("unknown station", unknown_station_actual.summary())
    print()

    print(f"--- Per-station breakdown (top {args.top_stations} by pair count, min {args.min_station_n} pairs) ---")
    rows = [
        (station, stats.summary())
        for station, stats in by_station_actual.items()
        if len(stats.values) >= args.min_station_n
    ]
    rows.sort(key=lambda r: r[1]["n"], reverse=True)
    for station, s in rows[: args.top_stations]:
        _print_summary_row(station, s)
    print()
    print(f"  ({len(rows):,} stations met the {args.min_station_n}-pair threshold out of {len(by_station_actual):,} total stations seen)")


if __name__ == "__main__":
    main()
