#!/usr/bin/env python3
"""Flatten the enriched giant-component graphml into a per-node feature CSV,
join the hand-transcribed ground truth, and report match diagnostics.

IMPORTANT node-label quirk: this graphml's node labels are NOT the same MRN
convention used in data/source/*/*.md ground truth. The large majority of
nodes use "<2-digit year><FULL station name><unpadded number>" (e.g.
"73SANTIAGO4687") -- which is exactly the canonical form acp-127's own
src/reftel_normalize.py::_normalize_doc_number() produces (2-digit year +
canonical station name + _clean_number()'s leading-zero-stripped number) --
and a small minority use the older "<4-digit year><6-char-truncated
station><zero-padded number>" form (e.g. "1973MANAGU04838") that the ground
truth CSV's raw MRNs are written in. Ground-truth MRNs are joined by
reproducing
acp-127's normalization: look up the truncated station code in the same
STATIONS variant table acp-127 uses (station_data.py here, copied verbatim
from ../../../acp-127/src/station_data.py -- see that file's docstring),
strip leading zeros from the number the same way _clean_number() does, and
try a direct label match first. See match_mrn_to_label() below.

Usage:
    build_node_table.py <graphml_path> [ground_truth_csv] [output_csv]

graphml_path is required -- no default, since this repo's enriched graphml
builds live outside the repo and their filename/schema changes over time
(see the "Which graph build" changelog in results/FINDINGS.md for examples:
attributes have been added/removed/renamed across builds already). Node and
edge attributes to extract are discovered from whatever file is passed, not
hardcoded, so this script adapts automatically to schema changes -- see
STRUCTURAL_NODE_ATTRS below for the only attributes it deliberately skips.

ground_truth_csv/output_csv default to this question's own results/ paths
(stable, in-repo) and can still be overridden positionally.
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

DEFAULT_GROUND_TRUTH = "questions/publication-cable-graph-signal/results/ground_truth_cables.csv"
DEFAULT_OUTPUT = "questions/publication-cable-graph-signal/results/node_features.csv"

MRN_RE = re.compile(r"^(\d{4})([A-Z]+)(\d+)$")

# Node attributes that are identifiers/bulk text rather than graph-signal
# attributes -- excluded from the auto-detected feature set regardless of
# which graphml build is loaded. "date" is kept out of the flattened
# attribute loop but read separately below (needed for year derivation).
STRUCTURAL_NODE_ATTRS = {"label", "id", "message_preview", "TAGS", "date"}


def _repo_root_relative(path):
    """Resolve a path against the repo root regardless of cwd."""
    if os.path.exists(path):
        return path
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    candidate = os.path.join(root, path)
    return candidate


def build_edge_attr_aggregates(g, edge_attr):
    """Per-node max/mean of an edge-only attribute over incident edges."""
    n = g.vcount()
    if edge_attr not in g.es.attributes():
        sys.stderr.write(f"  No edge '{edge_attr}' attribute found; skipping.\n")
        return np.full(n, np.nan), np.full(n, np.nan)

    values = np.array(g.es[edge_attr], dtype=float)
    edges = np.array(g.get_edgelist())
    src, tgt = edges[:, 0], edges[:, 1]

    max_v = np.full(n, -np.inf)
    sum_v = np.zeros(n)
    count_v = np.zeros(n)

    for endpoints in (src, tgt):
        np.maximum.at(max_v, endpoints, values)
        np.add.at(sum_v, endpoints, values)
        np.add.at(count_v, endpoints, 1)

    max_v[count_v == 0] = np.nan
    mean_v = np.divide(sum_v, count_v, out=np.full(n, np.nan), where=count_v > 0)
    return max_v, mean_v


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
    if len(sys.argv) < 2:
        sys.stderr.write(
            f"Usage: {sys.argv[0]} <graphml_path> [ground_truth_csv] [output_csv]\n"
        )
        sys.exit(1)

    graphml_path = sys.argv[1]
    ground_truth_path = _repo_root_relative(
        sys.argv[2] if len(sys.argv) > 2 else DEFAULT_GROUND_TRUTH
    )
    output_path = _repo_root_relative(sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUTPUT)
    # Written next to output_path rather than a fixed repo path, so pointing
    # output_csv at a different directory (e.g. a non-giant-build run) keeps
    # that run's matched ground truth alongside it instead of overwriting
    # the canonical results/ground_truth_matched.csv.
    matched_output_path = os.path.join(os.path.dirname(output_path), "ground_truth_matched.csv")

    if not os.path.exists(graphml_path):
        sys.stderr.write(f"GraphML not found: {graphml_path}\n")
        sys.exit(1)

    sys.stderr.write(f"Loading {graphml_path} ...\n")
    g = ig.Graph.Read_GraphML(graphml_path)
    sys.stderr.write(
        f"Vertices: {g.vcount():,}, Edges: {g.ecount():,}, Directed: {g.is_directed()}\n"
    )

    node_attrs = [a for a in g.vs.attributes() if a not in STRUCTURAL_NODE_ATTRS]
    edge_attrs = list(g.es.attributes())
    sys.stderr.write(f"Discovered node attributes: {node_attrs}\n")
    sys.stderr.write(f"Discovered edge attributes: {edge_attrs}\n")

    sys.stderr.write("Flattening node attributes ...\n")
    data = {"label": g.vs["label"]}
    if "date" in g.vs.attributes():
        data["date"] = g.vs["date"]
    for attr in node_attrs:
        data[attr] = g.vs[attr]

    for edge_attr in edge_attrs:
        col_prefix = edge_attr.replace("-", "_")
        sys.stderr.write(f"Aggregating edge '{edge_attr}' onto nodes ...\n")
        max_v, mean_v = build_edge_attr_aggregates(g, edge_attr)
        data[f"{col_prefix}_max"] = max_v
        data[f"{col_prefix}_mean"] = mean_v

    df = pd.DataFrame(data)
    if "date" in df.columns:
        df["year"] = df["date"].astype(str).str.slice(0, 4)
        df.loc[~df["year"].str.fullmatch(r"\d{4}"), "year"] = pd.NA
    else:
        df["year"] = pd.NA

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
