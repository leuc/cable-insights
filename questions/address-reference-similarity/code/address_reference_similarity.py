#!/usr/bin/env python3
"""Test the hypothesis: cables that reference each other share the same
office distribution (ACTION/ORIGIN/INFO office codes and copy counts) and/or
the same FM/TO/INFO addresses.

Joins data/cable-extract/<year>.ndjson (raw per-document extractor output:
Message Attributes.Document Number, _distribution, _from, _to, _info) with
data/cable-extract/<year>.reftel.norm.ndjson (document_number_raw ->
document_number mapping, plus extracted_references, from
src.reftel_normalize) on the raw Document Number, then compares each citing
document's routing/addressing metadata against each of its referenced
documents', against a random-pair baseline drawn from the same document
pool -- same method shape as
questions/tags-reference-similarity/code/tags_reference_similarity.py.

Reports, per pair:
  - office code-set Jaccard, three views: action (+origin), info, and the
    union of all three ("office_all")
  - office "same values": of the office codes shared by both documents, what
    fraction also carry the identical copy count
  - FM exact-match rate (reported separately -- expected to be inflated by
    a cable and the prior cable it cites sharing an author post)
  - TO / INFO addressee token-set Jaccard

Every run reports two sections: ALL (including STATE) and EXCLUDING STATE
(station parsed from document_number via lib.station.parse_station, dropped
on either side of the pair) -- STATE is ~29% of the corpus and drafted/routed
differently from field posts (outgoing instructions vs. field reporting), so
its inclusion can dominate an aggregate that's meant to describe how field
cables reference each other.

    Usage (from repo root)::

        python3 questions/address-reference-similarity/code/address_reference_similarity.py
            [--results-dir data/cable-extract] [--years 1973 1974 ...]
            [--sample N] [--seed S] [--workers 7]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from lib.station import parse_station

_ALL_YEARS = [1973, 1974, 1975, 1976, 1977, 1978, 1979]

_SET_VIEWS = ["action_origin", "info_office", "office_all", "to_tokens", "info_tokens"]


def _normalize_text(s: str | None) -> str:
    if not s:
        return ""
    return " ".join(s.upper().split())


def _load_reftel(path: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    """raw Document Number -> document_number, and document_number -> extracted_references."""
    raw2norm: dict[str, str] = {}
    refs_by_doc: dict[str, list[str]] = {}
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
            raw = d.get("document_number_raw")
            if doc and raw:
                raw2norm[raw] = doc
            refs = d.get("extracted_references")
            if doc and refs:
                refs_by_doc[doc] = refs
    return raw2norm, refs_by_doc


def _load_addresses(path: Path, raw2norm: dict[str, str]) -> dict[str, dict]:
    """document_number -> routing/addressing entry, keyed via raw2norm."""
    result: dict[str, dict] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            attrs = d.get("Message Attributes") or {}
            raw_doc = attrs.get("Document Number")
            if not raw_doc:
                continue
            doc = raw2norm.get(raw_doc)
            if not doc:
                continue

            dist = d.get("_distribution") or {}
            action = set((dist.get("ACTION") or {}).keys())
            origin = set((dist.get("ORIGIN") or {}).keys())
            info_office = set((dist.get("INFO") or {}).keys())
            values: dict[str, int] = {}
            for section in ("ACTION", "ORIGIN", "INFO"):
                for code, count in (dist.get(section) or {}).items():
                    values[code] = count

            result[doc] = {
                "action_origin": action | origin,
                "info_office": info_office,
                "office_all": action | origin | info_office,
                "office_values": values,
                "from": _normalize_text(d.get("_from")),
                "to_tokens": set(_normalize_text(d.get("_to")).split()),
                "info_tokens": set(_normalize_text(d.get("_info")).split()),
            }
    return result


def _load_year(year: int, results_dir: str) -> tuple[int, dict[str, dict], dict[str, list[str]]]:
    """Worker: load one year's reftel + address data. Returns (year, addresses, refs_by_doc)."""
    rdir = Path(results_dir)
    raw2norm, refs_by_doc = _load_reftel(rdir / f"{year}.reftel.norm.ndjson")
    addresses = _load_addresses(rdir / f"{year}.ndjson", raw2norm)
    return year, addresses, refs_by_doc


def jaccard(a: set, b: set) -> float | None:
    if not a and not b:
        return None
    union = a | b
    if not union:
        return None
    return len(a & b) / len(union)


class PairStats:
    """Accumulates Jaccard scores for one set-valued view."""

    def __init__(self):
        self.scores: list[float] = []
        self.any_overlap = 0
        self.majority_overlap = 0
        self.identical = 0
        self.both_empty = 0

    def add(self, a: set, b: set):
        score = jaccard(a, b)
        if score is None:
            self.both_empty += 1
            return
        self.scores.append(score)
        if score > 0:
            self.any_overlap += 1
        if score >= 0.5:
            self.majority_overlap += 1
        if score == 1.0:
            self.identical += 1

    def summary(self) -> dict:
        n = len(self.scores)
        if n == 0:
            return {"n": 0}
        return {
            "n": n,
            "both_empty": self.both_empty,
            "mean": statistics.mean(self.scores),
            "median": statistics.median(self.scores),
            "stdev": statistics.stdev(self.scores) if n > 1 else 0.0,
            "any_overlap_pct": self.any_overlap / n * 100,
            "majority_overlap_pct": self.majority_overlap / n * 100,
            "identical_pct": self.identical / n * 100,
        }


class MatchStats:
    """Tracks an exact-match rate over items where both sides have a value."""

    def __init__(self):
        self.n = 0
        self.matches = 0

    def add(self, matched: bool):
        self.n += 1
        if matched:
            self.matches += 1

    def summary(self) -> dict:
        if self.n == 0:
            return {"n": 0}
        return {"n": self.n, "match_pct": self.matches / self.n * 100}


def run_report(
    label: str,
    citing_docs_pool: list[str],
    addresses_by_doc: dict[str, dict],
    refs_by_doc: dict[str, list[str]],
    doc_keys_pool: list[str],
    rng: random.Random,
    args,
    exclude_station: str | None = None,
):
    """Run the full actual-vs-random comparison over one document pool and print it.

    `exclude_station`, when set, additionally drops any reference whose cited
    document has that station (citing side is already filtered into
    `citing_docs_pool`/`doc_keys_pool` by the caller).
    """
    citing_docs = list(citing_docs_pool)
    if args.sample is not None and args.sample < len(citing_docs):
        citing_docs = rng.sample(citing_docs, args.sample)
        sys.stderr.write(f"  [{label}] sampled down to {len(citing_docs):,} citing documents\n")

    actual = {v: PairStats() for v in _SET_VIEWS}
    random_baseline = {v: PairStats() for v in _SET_VIEWS}
    actual_fm = MatchStats()
    random_fm = MatchStats()
    actual_office_value = MatchStats()
    random_office_value = MatchStats()

    resolved_ref_pairs = 0
    total_ref_pairs = 0
    citing_docs_with_resolved_ref = 0

    for doc in citing_docs:
        entry = addresses_by_doc[doc]
        refs = refs_by_doc[doc]
        had_resolved = False
        for ref in refs:
            if exclude_station and parse_station(ref) == exclude_station:
                continue
            total_ref_pairs += 1
            ref_entry = addresses_by_doc.get(ref)
            if ref_entry is None:
                continue
            resolved_ref_pairs += 1
            had_resolved = True

            for view in _SET_VIEWS:
                actual[view].add(entry[view], ref_entry[view])

            if entry["from"] and ref_entry["from"]:
                actual_fm.add(entry["from"] == ref_entry["from"])

            shared_codes = entry["office_all"] & ref_entry["office_all"]
            for code in shared_codes:
                actual_office_value.add(entry["office_values"].get(code) == ref_entry["office_values"].get(code))

            # Random baseline: one random other document per resolved reference,
            # compared against the SAME citing document.
            random_doc = rng.choice(doc_keys_pool)
            random_entry = addresses_by_doc[random_doc]
            for view in _SET_VIEWS:
                random_baseline[view].add(entry[view], random_entry[view])
            if entry["from"] and random_entry["from"]:
                random_fm.add(entry["from"] == random_entry["from"])
            shared_random_codes = entry["office_all"] & random_entry["office_all"]
            for code in shared_random_codes:
                random_office_value.add(entry["office_values"].get(code) == random_entry["office_values"].get(code))

        if had_resolved:
            citing_docs_with_resolved_ref += 1

    print(f"=== Office Distribution / FM/TO/INFO Address Reference-Similarity Test -- {label} ===")
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
            f"{resolved_ref_pairs:,} resolved to an in-corpus addressed document "
            f"({resolved_ref_pairs / total_ref_pairs * 100:.2f}%)"
        )
    print()

    for view in _SET_VIEWS:
        a = actual[view].summary()
        r = random_baseline[view].summary()
        print(f"--- {view} ---")
        if a["n"] == 0:
            print("  no data")
            continue
        print(f"  {'':20s} {'actual references':>20s} {'random baseline':>20s}")
        print(f"  {'n pairs':20s} {a['n']:>20,} {r['n']:>20,}")
        print(f"  {'mean Jaccard':20s} {a['mean']:>20.4f} {r['mean']:>20.4f}")
        print(f"  {'median Jaccard':20s} {a['median']:>20.4f} {r['median']:>20.4f}")
        print(f"  {'stdev':20s} {a['stdev']:>20.4f} {r['stdev']:>20.4f}")
        print(f"  {'any overlap %':20s} {a['any_overlap_pct']:>19.2f}% {r['any_overlap_pct']:>19.2f}%")
        print(f"  {'>=50% overlap %':20s} {a['majority_overlap_pct']:>19.2f}% {r['majority_overlap_pct']:>19.2f}%")
        print(f"  {'identical %':20s} {a['identical_pct']:>19.2f}% {r['identical_pct']:>19.2f}%")
        lift = (a["mean"] / r["mean"]) if r["mean"] > 0 else float("inf")
        print(f"  mean Jaccard lift (actual / random): {lift:.2f}x")
        print()

    af = actual_fm.summary()
    rf = random_fm.summary()
    print("--- FM exact-match rate (both sides non-empty; expect inflation from same-post replies) ---")
    if af["n"]:
        print(f"  actual:  n={af['n']:,}  match={af['match_pct']:.2f}%")
        print(f"  random:  n={rf['n']:,}  match={rf['match_pct']:.2f}%")
        lift = (af["match_pct"] / rf["match_pct"]) if rf.get("match_pct") else float("inf")
        print(f"  lift (actual / random): {lift:.2f}x")
    else:
        print("  no data")
    print()

    aov = actual_office_value.summary()
    rov = random_office_value.summary()
    print("--- Office code VALUE match rate (given both sides share the code, do copy counts match too?) ---")
    if aov["n"]:
        print(f"  actual:  n={aov['n']:,}  match={aov['match_pct']:.2f}%")
        print(f"  random:  n={rov['n']:,}  match={rov['match_pct']:.2f}%")
        lift = (aov["match_pct"] / rov["match_pct"]) if rov.get("match_pct") else float("inf")
        print(f"  lift (actual / random): {lift:.2f}x")
    else:
        print("  no data")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Test whether referencing cables share office distribution and FM/TO/INFO addresses."
    )
    parser.add_argument("--results-dir", default="data/cable-extract", help="Directory with *.ndjson and *.reftel.norm.ndjson")
    parser.add_argument("--years", nargs="+", type=int, default=_ALL_YEARS, help="Years to include")
    parser.add_argument("--sample", type=int, default=None, help="Sample this many citing documents; default: use all")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for sampling and the baseline")
    parser.add_argument("--workers", type=int, default=min(len(_ALL_YEARS), 7), help="Parallel year-loading workers")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    sys.stderr.write(f"Loading addresses + references for years {args.years} (parallel, {args.workers} workers) ...\n")
    addresses_by_doc: dict[str, dict] = {}
    refs_by_doc: dict[str, list[str]] = {}
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(_load_year, year, args.results_dir): year for year in args.years}
        for fut in concurrent.futures.as_completed(futures):
            year = futures[fut]
            try:
                y, year_addresses, year_refs = fut.result()
            except FileNotFoundError as e:
                sys.stderr.write(f"  WARNING: {year}: {e}, skipping\n")
                continue
            sys.stderr.write(
                f"  {y}: {len(year_addresses):,} documents with addresses, "
                f"{len(year_refs):,} documents with references\n"
            )
            addresses_by_doc.update(year_addresses)
            refs_by_doc.update(year_refs)

    sys.stderr.write(f"Total documents with addresses: {len(addresses_by_doc):,}\n")
    sys.stderr.write(f"Total documents with references: {len(refs_by_doc):,}\n")

    citing_docs = [d for d in refs_by_doc if d in addresses_by_doc]
    sys.stderr.write(f"Citing documents with own address data: {len(citing_docs):,}\n")

    all_doc_keys = list(addresses_by_doc.keys())

    run_report("ALL (including STATE)", citing_docs, addresses_by_doc, refs_by_doc, all_doc_keys, rng, args)

    non_state_citing = [d for d in citing_docs if parse_station(d) != "STATE"]
    non_state_doc_keys = [d for d in all_doc_keys if parse_station(d) != "STATE"]
    sys.stderr.write(
        f"Non-STATE citing documents: {len(non_state_citing):,} / {len(citing_docs):,}\n"
    )
    run_report(
        "EXCLUDING STATE (station != STATE on both sides)",
        non_state_citing,
        addresses_by_doc,
        refs_by_doc,
        non_state_doc_keys,
        rng,
        args,
        exclude_station="STATE",
    )


if __name__ == "__main__":
    main()
