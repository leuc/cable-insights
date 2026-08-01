#!/usr/bin/env python3
"""Build ../results/hourly_accounted_contributions.csv from ../../../data/derived/transmission_volume.csv.

For each cable with a real dash-counter value, the `date` column (DTG - Date-Time
Group, e.g. "R 151535Z SEP 76" -> "1976-09-15T15:35:00Z", parsed in
src/patterns/dtg.py) is an exact, minute-resolution timestamp - this is a directly
"accounted for" contribution to the counter, attributable to a specific hour and
station. Between two such cables adjacent in counter order, any counter values in
between are "unaccounted for" (no surviving document), but their timing can still
be bounded: they must have occurred between the two flanking cables' DTGs, so that
span is distributed proportionally across the UTC hours it covers.

DTG is the cable's drafting/origination time, not the dash-counter's own
`filing_time` subfield (when the cable was handed to the relay for transmission) -
the two can diverge by anywhere from minutes to over a day (see
../../filing-time-vs-dtg/results/dash_counter_filing_lag.md), so counter order
tracks DTG order less tightly (median Spearman rho=0.73 on clean days) than it
tracks filing_time order (rho=0.96). This script uses DTG only, since
data/derived/transmission_volume.csv doesn't carry filing_time - the tradeoff
is a noisier per-gap time bound in exchange for
using a field with far broader coverage (DTG exists across the whole corpus;
filing_time only exists post-1976 with a parsed dash-counter line).

Restriction, load-bearing for correctness: only days with no mid-day counter reset
are used (a reset scrambles counter-vs-time ordering and would corrupt the gap
interpolation) - 382 of the corpus's ~2,530 days qualify.

The resulting hourly "unaccounted" figures are a coarser estimate than they might
look: median gap between two counter-adjacent DTGs is 41 minutes, but the
distribution is heavily right-skewed (mean 95 min) - gaps spanning more than an
hour are a minority by count (39.7%) but account for 73.7% of the total
interpolated mass, so most of the "unaccounted" total is smoothed across whichever
multi-hour window it falls in rather than pinned to one hour. Treat "accounted" as
real, directly observed diurnal structure; treat "unaccounted" as directional, not
precise.

Usage (from repo root):
    python3 questions/dash-counter-meaning/code/hourly_accounted.py [data/derived/transmission_volume.csv] [questions/dash-counter-meaning/results/hourly_accounted_contributions.csv]
"""
import csv
import datetime
import sys
from collections import defaultdict

RESET_DROP_THRESHOLD = 50000


def has_reset_signature(counters_in_time_order):
    return any(
        counters_in_time_order[i] - counters_in_time_order[i + 1] > RESET_DROP_THRESHOLD
        for i in range(len(counters_in_time_order) - 1)
    )


def main():
    in_path = sys.argv[1] if len(sys.argv) > 1 else "data/derived/transmission_volume.csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "questions/dash-counter-meaning/results/hourly_accounted_contributions.csv"

    by_day = defaultdict(list)
    with open(in_path, newline="") as f:
        for row in csv.DictReader(f):
            if not row["date"] or not row["dash_counter"]:
                continue
            dtg = datetime.datetime.fromisoformat(row["date"].replace("Z", "+00:00"))
            by_day[row["date"][:10]].append((int(row["dash_counter"]), dtg, row["station"] or None))

    hourly = defaultdict(lambda: {"accounted_state": 0, "accounted_overseas": 0, "unaccounted": 0.0})
    days_used = 0

    for date, pts in by_day.items():
        if len(pts) < 20:
            continue
        pts_by_time = sorted(pts, key=lambda x: x[1])
        if has_reset_signature([c for c, _, _ in pts_by_time]):
            continue
        days_used += 1

        pts_by_counter = sorted(pts, key=lambda x: x[0])

        for c, dtg, station in pts_by_counter:
            bucket = "accounted_state" if station == "STATE" else "accounted_overseas"
            hourly[dtg.hour][bucket] += 1

        for i in range(len(pts_by_counter) - 1):
            c0, t0, _ = pts_by_counter[i]
            c1, t1, _ = pts_by_counter[i + 1]
            gap = c1 - c0 - 1
            if gap <= 0 or t1 <= t0:
                continue
            span_sec = (t1 - t0).total_seconds()
            cur = t0
            while cur < t1:
                next_hour = cur.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
                seg_end = min(next_hour, t1)
                seg_frac = (seg_end - cur).total_seconds() / span_sec
                hourly[cur.hour]["unaccounted"] += gap * seg_frac
                cur = seg_end

    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["hour_utc", "accounted_state", "accounted_overseas", "unaccounted", "total", "unaccounted_share"])
        for h in range(24):
            d = hourly[h]
            total = d["accounted_state"] + d["accounted_overseas"] + d["unaccounted"]
            share = d["unaccounted"] / total if total else 0
            w.writerow([h, d["accounted_state"], d["accounted_overseas"], round(d["unaccounted"], 1), round(total, 1), round(share, 4)])

    print(f"days used (no mid-day reset): {days_used}", file=sys.stderr)
    print(f"wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
