#!/usr/bin/env python3
"""Profile the two antichain groups (antichain=0 vs antichain=1) by graph
properties, cd-index-type overlap, TAGS category, station, and year.

`antichain` in this graphml turns out to be a *binary* maximum-antichain
(independent-set) membership indicator, not a multi-level depth layering
-- verified directly against the edge list before writing this script (see
HYPOTHESIS.md): a longest-path-layering would show ~0% of edges with
predecessor-layer >= citer-layer, but 55.0% do; the independent-set
reading instead predicts 0 edges connect two antichain=1 nodes, and
that's exactly what's observed (0 of 487,904). So antichain=1 marks
membership in a large (~48%) set of pairwise-incomparable nodes -- no two
of them are ever directly connected by a reference edge.

Usage: antichain_profile.py <graphml_path> [output_dir]
"""
import sys
import os
import re
from collections import Counter

import igraph as ig
import numpy as np
import pandas as pd
from scipy import stats

STRUCTURAL_EXCLUDE = {
    "label", "id", "date", "date_estimated", "message_preview", "TAGS",
    "missing", "cd-index-type", "antichain",
}

TAGS_CODE_RE = re.compile(r"\(([^()]+)\)\s*$")
STATION_RE = re.compile(r"^\d{2}([A-Z]+)\d+$")


def rank_biserial(a, b):
    a = pd.Series(a).dropna().to_numpy(dtype=float)
    b = pd.Series(b).dropna().to_numpy(dtype=float)
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan, len(a), len(b)
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    effect = 1 - (2 * u) / (len(a) * len(b))
    return round(float(effect), 4), float(p), len(a), len(b)


def aggregate_edge_attr(g, n, values):
    edges = np.array(g.get_edgelist())
    src, tgt = edges[:, 0], edges[:, 1]
    sum_v = np.zeros(n)
    count_v = np.zeros(n)
    for endpoints in (src, tgt):
        np.add.at(sum_v, endpoints, values)
        np.add.at(count_v, endpoints, 1)
    return np.divide(sum_v, count_v, out=np.full(n, np.nan), where=count_v > 0)


def parse_tag_codes(tags_str):
    if not tags_str:
        return []
    codes = []
    for line in str(tags_str).strip().split("\n"):
        m = TAGS_CODE_RE.search(line.strip())
        if m:
            codes.append(m.group(1))
    return codes


def parse_station(label):
    m = STATION_RE.match(str(label))
    return m.group(1) if m else None


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <graphml_path> [output_dir]\n")
        sys.exit(1)
    graphml_path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."

    if not os.path.exists(graphml_path):
        sys.stderr.write(f"GraphML not found: {graphml_path}\n")
        sys.exit(1)

    sys.stderr.write(f"Loading {graphml_path} ...\n")
    g = ig.Graph.Read_GraphML(graphml_path)
    n = g.vcount()
    sys.stderr.write(f"Vertices: {n:,}, Edges: {g.ecount():,}\n")

    if "antichain" not in g.vs.attributes():
        sys.stderr.write("No 'antichain' node attribute in this graphml.\n")
        sys.exit(1)

    antichain = np.array(g.vs["antichain"], dtype=float)
    sys.stderr.write(f"antichain value counts: {pd.Series(antichain).value_counts().to_dict()}\n")

    # ---- mechanical verification (see module docstring) ----
    edges = np.array(g.get_edgelist())
    src, tgt = edges[:, 0], edges[:, 1]
    layering_violation_rate = (antichain[tgt] >= antichain[src]).mean()
    both_one_rate = ((antichain[src] == 1.0) & (antichain[tgt] == 1.0)).mean()
    sys.stderr.write(
        f"Layering-hypothesis violation rate: {layering_violation_rate:.4f} (expect ~0 if valid layering)\n"
        f"Both-endpoints-antichain=1 rate: {both_one_rate:.6f} (expect exactly 0 if valid independent set)\n"
    )

    # ---- auto-detect numeric node attributes ----
    metrics = {}
    for attr in g.vs.attributes():
        if attr in STRUCTURAL_EXCLUDE:
            continue
        try:
            arr = np.array(g.vs[attr], dtype=float)
        except (ValueError, TypeError):
            continue
        metrics[attr] = arr
    sys.stderr.write(f"Auto-detected node metrics: {sorted(metrics)}\n")

    if "trussness" in g.es.attributes():
        sys.stderr.write("Aggregating edge trussness onto nodes ...\n")
        metrics["trussness_mean"] = aggregate_edge_attr(g, n, np.array(g.es["trussness"], dtype=float))

    if "community-leiden" in metrics:
        sys.stderr.write("Computing neighbor community-sharing ...\n")
        community = metrics["community-leiden"]
        same_community = (community[src] == community[tgt]) & ~np.isnan(community[src]) & ~np.isnan(community[tgt])
        same_count = np.zeros(n)
        total_count = np.zeros(n)
        for endpoints in (src, tgt):
            np.add.at(total_count, endpoints, 1)
            np.add.at(same_count, endpoints, same_community.astype(float))
        metrics["community_share"] = np.divide(same_count, total_count, out=np.full(n, np.nan), where=total_count > 0)

    out_degree = np.array(g.degree(mode="out"), dtype=float)
    in_degree = np.array(g.degree(mode="in"), dtype=float)
    metrics.setdefault("out_degree", out_degree)
    metrics.setdefault("in_degree", in_degree)

    cd_type = pd.Series(g.vs["cd-index-type"]).fillna("undefined").astype(str) if "cd-index-type" in g.vs.attributes() else None
    dates = g.vs["date"] if "date" in g.vs.attributes() else [""] * n
    tags_raw = g.vs["TAGS"] if "TAGS" in g.vs.attributes() else [""] * n
    labels = g.vs["label"]

    df = pd.DataFrame({"antichain": antichain, "label": labels, "date": dates, "tags_raw": tags_raw, **metrics})
    if cd_type is not None:
        df["cd_index_type"] = cd_type.to_numpy()

    grp0 = df[df.antichain == 0.0]
    grp1 = df[df.antichain == 1.0]
    sys.stderr.write(f"\nantichain=0 n={len(grp0):,}, antichain=1 n={len(grp1):,}\n")

    # ---- numeric comparison ----
    metric_cols = [c for c in metrics if c != "community-leiden"]
    rows = []
    for metric in metric_cols:
        a, b = grp0[metric], grp1[metric]
        effect, p, n0, n1 = rank_biserial(a, b)
        rows.append(
            {
                "metric": metric,
                "antichain0_mean": round(float(a.mean()), 4) if len(a.dropna()) else np.nan,
                "antichain0_median": round(float(a.median()), 4) if len(a.dropna()) else np.nan,
                "antichain1_mean": round(float(b.mean()), 4) if len(b.dropna()) else np.nan,
                "antichain1_median": round(float(b.median()), 4) if len(b.dropna()) else np.nan,
                "rank_biserial_effect": effect,
                "pvalue": p,
                "n_antichain0": n0,
                "n_antichain1": n1,
            }
        )
    numeric_df = pd.DataFrame(rows).sort_values("pvalue")
    sys.stderr.write("\n=== antichain=0 vs antichain=1, numeric graph properties ===\n")
    sys.stderr.write(numeric_df.to_string(index=False) + "\n")

    # ---- cd-index-type cross-tab ----
    if cd_type is not None:
        sys.stderr.write("\n=== cd-index-type composition by antichain group ===\n")
        crosstab = pd.crosstab(df.antichain, df.cd_index_type, normalize="index").round(4)
        sys.stderr.write(crosstab.to_string() + "\n")
        crosstab.to_csv(os.path.join(outdir, "antichain_vs_cdindextype.csv"))

    # ---- TAGS category breakdown ----
    sys.stderr.write("\n=== top 15 TAGS codes per antichain group ===\n")
    tags_rows = []
    for val, sub in df.groupby("antichain"):
        counter = Counter()
        for t in sub.tags_raw:
            counter.update(parse_tag_codes(t))
        total = sum(counter.values())
        for code, count in counter.most_common(15):
            tags_rows.append({"antichain": val, "tag_code": code, "count": count, "pct_of_tag_mentions": round(count / total * 100, 2) if total else 0})
    tags_df = pd.DataFrame(tags_rows)
    sys.stderr.write(tags_df.to_string(index=False) + "\n")
    tags_df.to_csv(os.path.join(outdir, "antichain_top_tags.csv"), index=False)

    # ---- station breakdown ----
    df["station"] = df.label.apply(parse_station)
    sys.stderr.write("\n=== top 10 stations per antichain group ===\n")
    station_rows = []
    for val, sub in df.groupby("antichain"):
        vc = sub.station.value_counts(normalize=True).head(10)
        for station, frac in vc.items():
            station_rows.append({"antichain": val, "station": station, "fraction": round(float(frac), 4)})
    station_df = pd.DataFrame(station_rows)
    sys.stderr.write(station_df.to_string(index=False) + "\n")
    station_df.to_csv(os.path.join(outdir, "antichain_top_stations.csv"), index=False)

    # ---- year distribution ----
    df["year"] = df.date.astype(str).str.slice(0, 4)
    df.loc[~df.year.str.fullmatch(r"\d{4}"), "year"] = pd.NA
    sys.stderr.write("\n=== year distribution by antichain group (% within group) ===\n")
    year_tab = pd.crosstab(df.year, df.antichain, normalize="columns").round(4)
    sys.stderr.write(year_tab.to_string() + "\n")
    year_tab.to_csv(os.path.join(outdir, "antichain_by_year.csv"))

    numeric_df.to_csv(os.path.join(outdir, "antichain_numeric_comparison.csv"), index=False)
    sys.stderr.write(f"\nWrote CSVs to {outdir}\n")


if __name__ == "__main__":
    main()
