#!/usr/bin/env python3
"""Flatten the enriched giant-component graphml into a per-node feature CSV,
join the hand-transcribed ground truth, and report match diagnostics.

IMPORTANT node-label quirk: this graphml's node labels are NOT the same MRN
convention used in data/source/*/*.md ground truth. ~96% of nodes use
"<2-digit year><FULL station name><unpadded number>" (e.g. "73SANTIAGO4687")
-- which is exactly the canonical form acp-127's own
src/reftel_normalize.py::_normalize_doc_number() produces (2-digit year +
canonical station name + _clean_number()'s leading-zero-stripped number) --
and only ~4% use the older "<4-digit year><6-char-truncated station><zero-
padded number>" form (e.g. "1973MANAGU04838") that the ground truth CSV's
raw MRNs are written in. Ground-truth MRNs are joined by reproducing
acp-127's normalization: look up the truncated station code in the same
STATIONS variant table acp-127 uses (station_data.py here, copied verbatim
from ../../../acp-127/src/station_data.py -- see that file's docstring),
strip leading zeros from the number the same way _clean_number() does, and
try a direct label match first. See match_mrn_to_label() below.

Usage:
    build_node_table.py [graphml_path] [ground_truth_csv] [output_csv]

Defaults assume this script is run from the repo root or the question's
own code/ dir; all three paths can be overridden positionally.
"""
import re
import sys
import os
import igraph as ig
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from station_data import STATIONS

STATIONS_MAPPING = {}
for _canonical, _variants in STATIONS.items():
    STATIONS_MAPPING[_canonical.upper()] = _canonical
    for _variant in _variants:
        STATIONS_MAPPING[_variant.upper()] = _canonical

DEFAULT_GRAPHML = "data/external/reftel-with-tags-and-attr.2026-08-01.giant.graphml"
DEFAULT_GROUND_TRUTH = "questions/publication-cable-graph-signal/results/ground_truth_cables.csv"
DEFAULT_OUTPUT = "questions/publication-cable-graph-signal/results/node_features.csv"
DEFAULT_MATCHED_OUTPUT = "questions/publication-cable-graph-signal/results/ground_truth_matched.csv"

MRN_RE = re.compile(r"^(\d{4})([A-Z]+)(\d+)$")

NODE_ATTRS = [
    "date",
    "missing",
    "antichain",
    "degree",
    "closeness",
    "betweenness",
    "pagerank",
    "cd-index-type",
    "cd-index",
    "coreness",
    "strength",
    "community-leiden",
    "community-walktrap",
    "community-infomap",
]


def _repo_root_relative(path):
    """Resolve a path against the repo root regardless of cwd."""
    if os.path.exists(path):
        return path
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    candidate = os.path.join(root, path)
    return candidate


def build_trussness_aggregates(g):
    """Per-node max/mean trussness over incident edges (trussness is edge-only)."""
    n = g.vcount()
    if "trussness" not in g.es.attributes():
        sys.stderr.write("  No edge 'trussness' attribute found; skipping.\n")
        return np.full(n, np.nan), np.full(n, np.nan)

    trussness = np.array(g.es["trussness"], dtype=float)
    edges = np.array(g.get_edgelist())
    src, tgt = edges[:, 0], edges[:, 1]

    max_t = np.full(n, -np.inf)
    sum_t = np.zeros(n)
    count_t = np.zeros(n)

    for endpoints in (src, tgt):
        np.maximum.at(max_t, endpoints, trussness)
        np.add.at(sum_t, endpoints, trussness)
        np.add.at(count_t, endpoints, 1)

    max_t[count_t == 0] = np.nan
    mean_t = np.divide(sum_t, count_t, out=np.full(n, np.nan), where=count_t > 0)
    return max_t, mean_t


def _clean_number(n):
    """Mirrors acp-127's reftel_normalize.py::_clean_number()."""
    n = n.lstrip("0")
    return n if n else "0"


def match_mrn_to_label(mrn, label_set):
    """Reproduce acp-127's _normalize_doc_number()/_format_canonical(): look
    the raw (possibly truncated) station code up in the authoritative
    STATIONS variant table, then format as 2-digit-year + canonical station
    + leading-zero-stripped number -- the same canonical form this graphml's
    labels turn out to use."""
    if mrn in label_set:
        return mrn
    m = MRN_RE.match(mrn)
    if not m:
        return None
    year4, station_raw, num = m.groups()
    canonical_station = STATIONS_MAPPING.get(station_raw.upper())
    if not canonical_station:
        return None
    candidate = f"{year4[2:]}{canonical_station}{_clean_number(num)}"
    return candidate if candidate in label_set else None


def main():
    graphml_path = _repo_root_relative(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GRAPHML)
    ground_truth_path = _repo_root_relative(
        sys.argv[2] if len(sys.argv) > 2 else DEFAULT_GROUND_TRUTH
    )
    output_path = _repo_root_relative(sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUTPUT)
    matched_output_path = _repo_root_relative(DEFAULT_MATCHED_OUTPUT)

    if not os.path.exists(graphml_path):
        sys.stderr.write(f"GraphML not found: {graphml_path}\n")
        sys.exit(1)

    sys.stderr.write(f"Loading {graphml_path} ...\n")
    g = ig.Graph.Read_GraphML(graphml_path)
    sys.stderr.write(
        f"Vertices: {g.vcount():,}, Edges: {g.ecount():,}, Directed: {g.is_directed()}\n"
    )

    sys.stderr.write("Flattening node attributes ...\n")
    data = {"label": g.vs["label"]}
    for attr in NODE_ATTRS:
        if attr in g.vs.attributes():
            data[attr] = g.vs[attr]
        else:
            sys.stderr.write(f"  Warning: node attribute '{attr}' not found, skipping.\n")

    sys.stderr.write("Aggregating edge trussness onto nodes ...\n")
    max_t, mean_t = build_trussness_aggregates(g)
    data["trussness_max"] = max_t
    data["trussness_mean"] = mean_t

    df = pd.DataFrame(data)
    df["year"] = df["date"].astype(str).str.slice(0, 4)
    df.loc[~df["year"].str.fullmatch(r"\d{4}"), "year"] = pd.NA

    sys.stderr.write(f"Writing node feature table to {output_path} ...\n")
    df.to_csv(output_path, index=False)
    sys.stderr.write(f"  {len(df):,} rows written.\n\n")

    # ── Ground-truth match diagnostics ──
    if not os.path.exists(ground_truth_path):
        sys.stderr.write(f"Ground truth not found: {ground_truth_path}, skipping match report.\n")
        return

    gt = pd.read_csv(ground_truth_path)
    label_set = set(df["label"])

    gt["matched_label"] = gt["mrn"].apply(lambda m: match_mrn_to_label(m, label_set))
    gt["matched"] = gt["matched_label"].notna()
    gt.to_csv(matched_output_path, index=False)
    sys.stderr.write(f"Wrote matched ground truth to {matched_output_path}\n\n")

    sys.stderr.write("Ground-truth match rate against the giant component:\n")
    for tier in sorted(gt["tier"].unique()):
        sub = gt[gt["tier"] == tier]
        sys.stderr.write(f"  {tier}: {sub['matched'].sum()}/{len(sub)} found in giant component\n")
    sys.stderr.write(f"  overall: {gt['matched'].sum()}/{len(gt)} found\n\n")

    sys.stderr.write("Per-publication confirmed-tier match rate:\n")
    confirmed = gt[gt["tier"] == "confirmed"]
    for pub, sub in confirmed.groupby("publication"):
        sys.stderr.write(f"  {pub}: {sub['matched'].sum()}/{len(sub)}\n")

    missing = gt[~gt["matched"]]
    if len(missing):
        sys.stderr.write("\nUnmatched ground-truth MRNs (by publication, count only):\n")
        for pub, sub in missing.groupby("publication"):
            sys.stderr.write(f"  {pub}: {len(sub)} unmatched\n")


if __name__ == "__main__":
    main()
