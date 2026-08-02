#!/usr/bin/env python3
"""Test the "disruptive = broadcast circular, consolidating = tight thread"
reading against graph structure directly, at full population scale --
complementary to (and more rigorous than) the small text-content sample in
results/cd_index_content_samples.md.

Every numeric node attribute in the loaded graphml is tested automatically
(degree, closeness, betweenness, pagerank, hub, authority, strength,
coreness, antichain -- whatever the build actually has, auto-detected, not
hardcoded, per the convention established in
publication-cable-graph-signal after its "no hardcoded attributes" fix),
plus two derived edge-based aggregates:

- trussness_mean: a consolidating citer, by definition, cites both `f` and
  one of `f`'s own predecessors -- edges (citer->f), (citer->pred),
  (f->pred) form a triangle. Trussness counts triangle-embeddedness
  directly, so consolidating nodes' incident edges should show higher
  trussness than disruptive nodes'.
- community_share: fraction of a node's edge-neighbors landing in its own
  Leiden community -- citers of a tight thread (consolidating) should
  disproportionately share community with the focal cable; citers of a
  broadcast circular (disruptive) are unrelated posts and should scatter.

A second block splits the disruptive bucket by the focal cable's own
out-degree (predecessor count), since a 0-predecessor cable is
mechanically forced to cd-index=1.0 (see HYPOTHESIS.md Result section 1)
and can't sit in the citer/f/predecessor triangle trussness relies on --
so part of any disruptive-vs-consolidating structural gap could just be
re-deriving that same mechanical fact rather than independently confirming
"broadcast vs. thread". Comparing consolidating against *only* the
disruptive-with->=1-predecessor subset controls for that.

Usage: graph_structure_by_type.py <graphml_path> [output_csv]
"""
import sys
import os
import igraph as ig
import numpy as np
import pandas as pd
from scipy import stats

STRUCTURAL_EXCLUDE = {
    "label", "id", "date", "date_estimated", "message_preview", "TAGS",
    "missing", "cd-index", "cd-index-type", "mcd-index",
}


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


def compare(disr, cons, metric_cols, label_a="disruptive", label_b="consolidating"):
    rows = []
    for metric in metric_cols:
        d_vals, c_vals = disr[metric], cons[metric]
        effect, p, n_d, n_c = rank_biserial(d_vals, c_vals)
        rows.append(
            {
                "metric": metric,
                f"{label_a}_mean": round(float(d_vals.mean()), 4) if len(d_vals.dropna()) else np.nan,
                f"{label_a}_median": round(float(d_vals.median()), 4) if len(d_vals.dropna()) else np.nan,
                f"{label_b}_mean": round(float(c_vals.mean()), 4) if len(c_vals.dropna()) else np.nan,
                f"{label_b}_median": round(float(c_vals.median()), 4) if len(c_vals.dropna()) else np.nan,
                "rank_biserial_effect": effect,
                "pvalue": p,
                f"n_{label_a}": n_d,
                f"n_{label_b}": n_c,
            }
        )
    return pd.DataFrame(rows)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <graphml_path> [output_csv]\n")
        sys.exit(1)
    graphml_path = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(graphml_path):
        sys.stderr.write(f"GraphML not found: {graphml_path}\n")
        sys.exit(1)

    sys.stderr.write(f"Loading {graphml_path} ...\n")
    g = ig.Graph.Read_GraphML(graphml_path)
    n = g.vcount()
    sys.stderr.write(f"Vertices: {n:,}, Edges: {g.ecount():,}\n")

    cd_type = pd.Series(g.vs["cd-index-type"]).fillna("undefined").astype(str)
    out_degree = np.array(g.degree(mode="out"), dtype=float)

    # ---- auto-detect every numeric node attribute worth testing ----
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

    # ---- trussness (edge-only attribute, aggregated onto nodes) ----
    if "trussness" in g.es.attributes():
        sys.stderr.write("Aggregating edge trussness onto nodes ...\n")
        metrics["trussness_mean"] = aggregate_edge_attr(g, n, np.array(g.es["trussness"], dtype=float))

    # ---- community-sharing (derived from community-leiden + edge list) ----
    if "community-leiden" in metrics:
        sys.stderr.write("Computing neighbor community-sharing ...\n")
        community = metrics["community-leiden"]
        edges = np.array(g.get_edgelist())
        src, tgt = edges[:, 0], edges[:, 1]
        same_community = (community[src] == community[tgt]) & ~np.isnan(community[src]) & ~np.isnan(community[tgt])
        same_count = np.zeros(n)
        total_count = np.zeros(n)
        for endpoints in (src, tgt):
            np.add.at(total_count, endpoints, 1)
            np.add.at(same_count, endpoints, same_community.astype(float))
        metrics["community_share"] = np.divide(same_count, total_count, out=np.full(n, np.nan), where=total_count > 0)

    df = pd.DataFrame({"cd_index_type": cd_type, "out_degree": out_degree, **metrics})

    disr = df[df.cd_index_type == "disruptive"]
    cons = df[df.cd_index_type == "consolidating"]
    sys.stderr.write(f"\ndisruptive n={len(disr):,}, consolidating n={len(cons):,}\n")

    metric_cols = [c for c in metrics if c != "community-leiden"]  # raw community id isn't itself a meaningful ordinal metric
    result_df = compare(disr, cons, metric_cols)
    sys.stderr.write("\n=== disruptive (all) vs consolidating ===\n")
    sys.stderr.write(result_df.to_string(index=False) + "\n")

    # ---- predecessor-count-controlled comparison: does the gap survive
    #      once the 0-predecessor mechanical degeneracy is excluded? ----
    disr_with_pred = disr[disr.out_degree > 0]
    sys.stderr.write(
        f"\ndisruptive-with->=1-predecessor n={len(disr_with_pred):,} "
        f"({len(disr_with_pred) / len(disr) * 100:.1f}% of all disruptive)\n"
    )
    controlled_cols = [c for c in ("coreness", "trussness_mean", "community_share") if c in metrics]
    controlled_df = compare(disr_with_pred, cons, controlled_cols, label_a="disruptive_with_pred")
    sys.stderr.write("\n=== disruptive WITH >=1 predecessor vs consolidating (confound-controlled) ===\n")
    sys.stderr.write(controlled_df.to_string(index=False) + "\n")

    if output_csv:
        result_df["comparison"] = "disruptive_all_vs_consolidating"
        controlled_df["comparison"] = "disruptive_with_pred_vs_consolidating"
        combined = pd.concat([result_df, controlled_df], ignore_index=True, sort=False)
        combined.to_csv(output_csv, index=False)
        sys.stderr.write(f"\nWrote {output_csv}\n")


if __name__ == "__main__":
    main()
