#!/usr/bin/env python3
"""Method B: leave-one-out seed-expansion retrieval test.

For publications with enough matched confirmed cables, seed a personalized
PageRank on all-but-one of a publication's cables and see where the held-out
cable ranks among all 309K giant-component nodes. Compared against two
baselines per held-out cable: the node's own global-pagerank rank (does
personalization beat "this is just a generically important cable"?) and a
random-rank expectation. This tests whether network proximity to *other
known-cited cables* recovers held-out citations, which is a different claim
than Method A's "is any single static attribute elevated."

Usage: seed_expansion_retrieval.py [graphml_path] [ground_truth_matched_csv] [node_features_csv] [output_dir]
"""
import sys
import os
import igraph as ig
import numpy as np
import pandas as pd

MIN_SEEDS = 10
RECALL_KS = (10, 50, 100, 1000)

DEFAULT_GRAPHML = "data/external/reftel-with-tags-and-attr.2026-08-01.giant.graphml"
DEFAULT_GROUND_TRUTH = "questions/publication-cable-graph-signal/results/ground_truth_matched.csv"
DEFAULT_NODE_FEATURES = "questions/publication-cable-graph-signal/results/node_features.csv"
DEFAULT_OUTDIR = "questions/publication-cable-graph-signal/results"


def _repo_root_relative(path):
    if os.path.exists(path):
        return path
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    return os.path.join(root, path)


def ranks_desc(scores):
    """1-indexed rank, 1 = highest score, ties broken by min-rank."""
    order = np.argsort(-np.asarray(scores), kind="stable")
    rank = np.empty(len(scores), dtype=int)
    rank[order] = np.arange(1, len(scores) + 1)
    return rank


def main():
    graphml_path = _repo_root_relative(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GRAPHML)
    ground_truth_path = _repo_root_relative(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_GROUND_TRUTH)
    node_features_path = _repo_root_relative(sys.argv[3] if len(sys.argv) > 3 else DEFAULT_NODE_FEATURES)
    outdir = _repo_root_relative(sys.argv[4] if len(sys.argv) > 4 else DEFAULT_OUTDIR)

    sys.stderr.write(f"Loading {graphml_path} ...\n")
    g = ig.Graph.Read_GraphML(graphml_path)
    n = g.vcount()
    sys.stderr.write(f"Vertices: {n:,}, Edges: {g.ecount():,}\n")

    labels = g.vs["label"]
    label_to_idx = {lbl: i for i, lbl in enumerate(labels)}

    node_features = pd.read_csv(node_features_path)
    global_pagerank = np.full(n, np.nan)
    label_to_row = {lbl: i for i, lbl in enumerate(node_features["label"])}
    pr_col = node_features["pagerank"].to_numpy()
    for i, lbl in enumerate(labels):
        row = label_to_row.get(lbl)
        if row is not None:
            global_pagerank[i] = pr_col[row]
    global_pagerank = np.nan_to_num(global_pagerank, nan=0.0)
    global_rank = ranks_desc(global_pagerank)

    gt = pd.read_csv(ground_truth_path)
    confirmed = gt[(gt["matched"]) & (gt["tier"] == "confirmed")]

    detail_rows = []
    summary_rows = []

    for pub, sub in confirmed.groupby("publication"):
        seed_labels = sub["matched_label"].tolist()
        seed_idx = [label_to_idx[l] for l in seed_labels if l in label_to_idx]
        if len(seed_idx) < MIN_SEEDS:
            sys.stderr.write(f"Skipping {pub}: only {len(seed_idx)} matched confirmed cables (< {MIN_SEEDS}).\n")
            continue

        sys.stderr.write(f"{pub}: leave-one-out over {len(seed_idx)} seeds ...\n")
        ppr_ranks, global_ranks_held = [], []

        for held_out in seed_idx:
            other_seeds = [s for s in seed_idx if s != held_out]
            ppr = g.personalized_pagerank(directed=True, reset_vertices=other_seeds)
            rank = ranks_desc(ppr)[held_out]
            ppr_ranks.append(rank)
            global_ranks_held.append(int(global_rank[held_out]))
            detail_rows.append(
                {
                    "publication": pub,
                    "held_out_label": labels[held_out],
                    "ppr_rank": int(rank),
                    "global_pagerank_rank": int(global_rank[held_out]),
                    "n_nodes": n,
                }
            )

        ppr_ranks = np.array(ppr_ranks)
        global_ranks_held = np.array(global_ranks_held)
        random_expected_rank = (n + 1) / 2

        def summarize(ranks, method):
            row = {
                "publication": pub,
                "method": method,
                "n_seeds": len(seed_idx),
                "median_rank": float(np.median(ranks)),
                "mrr": float(np.mean(1.0 / ranks)),
            }
            for k in RECALL_KS:
                row[f"recall@{k}"] = float(np.mean(ranks <= k))
            return row

        summary_rows.append(summarize(ppr_ranks, "personalized_pagerank"))
        summary_rows.append(summarize(global_ranks_held, "global_pagerank"))
        summary_rows.append(
            {
                "publication": pub,
                "method": "random",
                "n_seeds": len(seed_idx),
                "median_rank": random_expected_rank,
                "mrr": float(np.log(n) / n),  # approx E[1/rank] for uniform random rank in [1,n]
                **{f"recall@{k}": k / n for k in RECALL_KS},
            }
        )

    os.makedirs(outdir, exist_ok=True)
    detail_df = pd.DataFrame(detail_rows)
    summary_df = pd.DataFrame(summary_rows)
    detail_df.to_csv(os.path.join(outdir, "seed_expansion_details.csv"), index=False)
    summary_df.to_csv(os.path.join(outdir, "seed_expansion_summary.csv"), index=False)

    sys.stderr.write("\nSummary (lower rank = better, higher recall/MRR = better):\n")
    if len(summary_df):
        sys.stderr.write(summary_df.to_string(index=False) + "\n")
    else:
        sys.stderr.write("  No publication had enough matched confirmed cables to run Method B.\n")


if __name__ == "__main__":
    main()
