#!/usr/bin/env python3
"""Method A: per-attribute signal ranking.

For each publication (and pooled combinations) with enough matched
ground-truth cables, test whether each graph attribute separates the
publication's cited cables from a background sample. Which attributes to
test is discovered from node_features.csv's actual columns/dtypes, not
hardcoded (that CSV's columns are themselves whatever build_node_table.py
found in the source graphml, so this adapts automatically as the graph
build's attribute schema changes): numeric-dtype columns get a Mann-Whitney
U / rank-biserial sweep; string-dtype columns (e.g. cd-index-type) get a
hypergeometric enrichment test on the most concentrated bucket. `cd-index`
and `antichain` additionally get purpose-built tests beyond the generic
sweep (skew toward extreme |cd-index|; enrichment/depletion in the
background's dominant antichain bucket) since they encode something
structurally different from static centrality -- these two are referenced
by name because the tests themselves are conceptually specific to those
attributes, not because the rest of the sweep is hardcoded.

Usage: attribute_signal.py [node_features_csv] [ground_truth_matched_csv] [output_dir]
"""
import sys
import os
import numpy as np
import pandas as pd
from scipy import stats

MIN_N_PER_PUBLICATION = 4

# Columns that are identifiers/join keys/derived-for-background-sampling
# rather than graph-signal attributes -- excluded from auto-detection
# regardless of which graph build produced node_features.csv.
STRUCTURAL_COLS = {"label", "date", "year"}

DEFAULT_NODE_FEATURES = "questions/publication-cable-graph-signal/results/node_features.csv"
DEFAULT_GROUND_TRUTH = "questions/publication-cable-graph-signal/results/ground_truth_matched.csv"
DEFAULT_OUTDIR = "questions/publication-cable-graph-signal/results"


def _repo_root_relative(path):
    if os.path.exists(path):
        return path
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    return os.path.join(root, path)


def rank_biserial_mannwhitney(selected, background):
    selected = pd.Series(selected).dropna().to_numpy(dtype=float)
    background = pd.Series(background).dropna().to_numpy(dtype=float)
    n1, n2 = len(selected), len(background)
    if n1 < 2 or n2 < 2:
        return {"n_selected": n1, "n_background": n2, "effect_size": np.nan, "pvalue": np.nan}
    u, p = stats.mannwhitneyu(selected, background, alternative="two-sided")
    effect = 1 - (2 * u) / (n1 * n2)  # rank-biserial, ~ 2*AUROC - 1
    return {"n_selected": n1, "n_background": n2, "effect_size": round(float(effect), 4), "pvalue": float(p)}


def hypergeom_bucket_enrichment(selected_vals, background_vals, bucket=None):
    """Test whether `bucket` (default: mode of selected) is over/under
    represented among selected vs background. Returns the more extreme
    (smaller p-value) of the over- and under-representation one-sided tests."""
    selected_vals = pd.Series(selected_vals).dropna()
    background_vals = pd.Series(background_vals).dropna()
    n_sel = len(selected_vals)
    pop = len(background_vals)  # background already includes the selected cables' population pool
    if n_sel < 2 or pop < 2:
        return None
    if bucket is None:
        if selected_vals.empty:
            return None
        bucket = selected_vals.mode().iloc[0]
    K = int((background_vals == bucket).sum())
    k = int((selected_vals == bucket).sum())
    if K == 0:
        return None
    expected = n_sel * K / pop
    # over-representation: P(X >= k); under-representation: P(X <= k)
    p_over = stats.hypergeom.sf(k - 1, pop, K, n_sel)
    p_under = stats.hypergeom.cdf(k, pop, K, n_sel)
    direction = "enriched" if p_over <= p_under else "depleted"
    pvalue = min(p_over, p_under)
    return {
        "bucket": bucket,
        "n_selected": n_sel,
        "observed": k,
        "expected": round(float(expected), 2),
        "direction": direction,
        "pvalue": float(pvalue),
    }


def build_groups(gt_matched):
    """Yield (group_name, tier_scope, label_set) for every publication with
    enough matched cables, plus pooled combinations."""
    groups = []
    for tier_scope, tiers in [("confirmed", {"confirmed"}), ("confirmed+flagged", {"confirmed", "flagged"})]:
        sub_all = gt_matched[gt_matched["matched"] & gt_matched["tier"].isin(tiers)]
        for pub, sub in sub_all.groupby("publication"):
            if len(sub) >= MIN_N_PER_PUBLICATION:
                groups.append((pub, tier_scope, set(sub["matched_label"])))
        if len(sub_all) >= MIN_N_PER_PUBLICATION:
            groups.append(("ALL_POOLED", tier_scope, set(sub_all["matched_label"])))
        no_morley = sub_all[sub_all["publication"] != "morley2019"]
        if len(no_morley) >= MIN_N_PER_PUBLICATION:
            groups.append(("ALL_POOLED_excl_morley2019", tier_scope, set(no_morley["matched_label"])))
    return groups


def background_pool(nodes, selected_labels, scope, years):
    if scope == "same_year":
        pool = nodes[nodes["year"].isin(years)]
    else:
        pool = nodes
    return pool[~pool["label"].isin(selected_labels)]


def main():
    node_features_path = _repo_root_relative(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_NODE_FEATURES)
    ground_truth_path = _repo_root_relative(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_GROUND_TRUTH)
    outdir = _repo_root_relative(sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUTDIR)

    sys.stderr.write("Loading node features and matched ground truth ...\n")
    nodes = pd.read_csv(node_features_path)
    gt = pd.read_csv(ground_truth_path)

    numeric_attrs = [
        c for c in nodes.columns
        if c not in STRUCTURAL_COLS and pd.api.types.is_numeric_dtype(nodes[c])
    ]
    categorical_attrs = [
        c for c in nodes.columns
        if c not in STRUCTURAL_COLS and nodes[c].dtype == object
    ]
    sys.stderr.write(f"Numeric attributes discovered: {numeric_attrs}\n")
    sys.stderr.write(f"Categorical attributes discovered: {categorical_attrs}\n")

    groups = build_groups(gt)
    sys.stderr.write(f"Testing {len(groups)} (publication/pool x tier_scope) groups.\n")

    numeric_rows = []
    categorical_rows = []
    cdindex_rows = []
    antichain_rows = []

    for group_name, tier_scope, selected_labels in groups:
        selected_nodes = nodes[nodes["label"].isin(selected_labels)]
        years = set(selected_nodes["year"].dropna())

        for scope in ("same_year", "full_corpus"):
            bg = background_pool(nodes, selected_labels, scope, years)

            for attr in numeric_attrs:
                res = rank_biserial_mannwhitney(selected_nodes[attr], bg[attr])
                res.update(group=group_name, tier_scope=tier_scope, background_scope=scope, attribute=attr)
                numeric_rows.append(res)

            for attr in categorical_attrs:
                res = hypergeom_bucket_enrichment(selected_nodes[attr], bg[attr])
                if res:
                    res.update(group=group_name, tier_scope=tier_scope, background_scope=scope, attribute=attr)
                    categorical_rows.append(res)

            # ── cd-index extra: skew toward extreme |cd-index| values ──
            if "cd-index" in nodes.columns:
                res = rank_biserial_mannwhitney(selected_nodes["cd-index"].abs(), bg["cd-index"].abs())
                res.update(group=group_name, tier_scope=tier_scope, background_scope=scope, attribute="cd-index_abs_extremeness")
                cdindex_rows.append(res)

            # ── antichain extra: enrichment/depletion in the *background's*
            #    single most-populated (dominant/mainstream) antichain bucket ──
            if "antichain" in nodes.columns and not bg["antichain"].dropna().empty:
                dominant_bucket = bg["antichain"].mode().iloc[0]
                res = hypergeom_bucket_enrichment(selected_nodes["antichain"], bg["antichain"], bucket=dominant_bucket)
                if res:
                    res.update(group=group_name, tier_scope=tier_scope, background_scope=scope)
                    antichain_rows.append(res)

    numeric_df = pd.DataFrame(numeric_rows)
    categorical_df = pd.DataFrame(categorical_rows)
    cdindex_df = pd.DataFrame(cdindex_rows)
    antichain_df = pd.DataFrame(antichain_rows)

    for df in (numeric_df, categorical_df, cdindex_df, antichain_df):
        if len(df) and "pvalue" in df.columns:
            valid = df["pvalue"].notna()
            df["qvalue"] = np.nan
            if valid.sum():
                df.loc[valid, "qvalue"] = stats.false_discovery_control(df.loc[valid, "pvalue"], method="bh")

    def save_sorted(df, filename):
        """Sort by group/tier/scope/qvalue and write, unless df has no rows
        at all (e.g. antichain on a graph build that lacks that attribute)
        -- an empty DataFrame has no columns to sort by, so just write it
        empty rather than erroring."""
        path = os.path.join(outdir, filename)
        if len(df):
            df.sort_values(["group", "tier_scope", "background_scope", "qvalue"]).to_csv(path, index=False)
        else:
            df.to_csv(path, index=False)
            sys.stderr.write(f"  Note: {filename} is empty (attribute not present in this graph build).\n")

    os.makedirs(outdir, exist_ok=True)
    save_sorted(numeric_df, "attribute_signal_numeric.csv")
    save_sorted(categorical_df, "attribute_signal_categorical.csv")
    save_sorted(cdindex_df, "attribute_signal_cdindex.csv")
    save_sorted(antichain_df, "attribute_signal_antichain.csv")

    sys.stderr.write("\nTop 15 numeric signals by q-value:\n")
    top = numeric_df.dropna(subset=["qvalue"]).sort_values("qvalue").head(15)
    sys.stderr.write(
        top[["group", "tier_scope", "background_scope", "attribute", "effect_size", "pvalue", "qvalue", "n_selected"]].to_string(index=False)
        + "\n"
    )

    sys.stderr.write("\ncd-index extremeness signals (q<0.2):\n")
    if len(cdindex_df):
        interesting = cdindex_df.dropna(subset=["qvalue"])
        interesting = interesting[interesting["qvalue"] < 0.2]
        cols = ["group", "tier_scope", "background_scope", "effect_size", "pvalue", "qvalue", "n_selected"]
        sys.stderr.write(interesting[cols].to_string(index=False) + "\n" if len(interesting) else "  none\n")
    else:
        sys.stderr.write("  cd-index not present in this graph build.\n")

    sys.stderr.write("\nantichain dominant-bucket signals (q<0.2):\n")
    if len(antichain_df):
        interesting = antichain_df.dropna(subset=["qvalue"])
        interesting = interesting[interesting["qvalue"] < 0.2]
        cols = ["group", "tier_scope", "background_scope", "direction", "observed", "expected", "qvalue"]
        sys.stderr.write(interesting[cols].to_string(index=False) + "\n" if len(interesting) else "  none\n")
    else:
        sys.stderr.write("  antichain not present in this graph build.\n")


if __name__ == "__main__":
    main()
