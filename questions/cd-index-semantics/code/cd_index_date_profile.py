#!/usr/bin/env python3
"""Profile cd-index / cd-index-type by cable year, to test whether the
undefined ("nan") rate is dominated by corpus-boundary right-censoring
rather than editorial signal.

The CD-index's forward-citer window (5 years / 1825 days in the patent
literature this measure comes from, and in this codebase's computation --
see HYPOTHESIS.md) is huge relative to a 7-year (1973-1979) corpus. A cable
from 1973 has nearly the whole rest of the corpus available as its forward
window; a cable from late 1979 has almost none, purely because the corpus
ends, not because nothing happened. If that's true, cd-index-type should be
"nan" (undefined, nt=0) at a rate that climbs sharply by cable year.

Usage: cd_index_date_profile.py <graphml_path> [output_csv]
"""
import sys
import os
import igraph as ig
import pandas as pd


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
    sys.stderr.write(f"Vertices: {g.vcount():,}, Edges: {g.ecount():,}\n")

    if "cd-index-type" not in g.vs.attributes():
        sys.stderr.write("No 'cd-index-type' node attribute in this graphml.\n")
        sys.exit(1)

    df = pd.DataFrame(
        {
            "date": g.vs["date"] if "date" in g.vs.attributes() else None,
            "cd_index": g.vs["cd-index"] if "cd-index" in g.vs.attributes() else None,
            "cd_index_type": g.vs["cd-index-type"],
        }
    )
    df["year"] = df["date"].astype(str).str.slice(0, 4)
    df.loc[~df["year"].str.fullmatch(r"\d{4}"), "year"] = pd.NA
    # cd-index-type is a string attribute; missing/NaN cd-index shows up as
    # empty string, literal "nan", or actual NaN depending on the graphml
    # writer -- normalize all of those to "undefined".
    df["type_norm"] = df["cd_index_type"].fillna("undefined").astype(str).str.strip()
    df.loc[df["type_norm"].isin(["", "nan", "NaN"]), "type_norm"] = "undefined"

    sys.stderr.write("\nOverall cd-index-type distribution:\n")
    overall = df["type_norm"].value_counts()
    overall_pct = (overall / len(df) * 100).round(2)
    for k in overall.index:
        sys.stderr.write(f"  {k}: {overall[k]:,} ({overall_pct[k]}%)\n")

    sys.stderr.write("\ncd-index summary (defined values only):\n")
    for t in ("disruptive", "consolidating"):
        vals = df.loc[df["type_norm"] == t, "cd_index"].dropna()
        if len(vals):
            sys.stderr.write(
                f"  {t}: n={len(vals):,} mean={vals.mean():.3f} median={vals.median():.3f} "
                f"min={vals.min():.3f} max={vals.max():.3f}\n"
            )

    sys.stderr.write("\ncd-index-type by year (tests the right-censoring hypothesis):\n")
    by_year = (
        df.dropna(subset=["year"])
        .groupby(["year", "type_norm"])
        .size()
        .unstack(fill_value=0)
    )
    for col in ("disruptive", "consolidating", "undefined"):
        if col not in by_year.columns:
            by_year[col] = 0
    by_year["total"] = by_year[["disruptive", "consolidating", "undefined"]].sum(axis=1)
    by_year["pct_undefined"] = (by_year["undefined"] / by_year["total"] * 100).round(2)
    by_year["pct_disruptive"] = (by_year["disruptive"] / by_year["total"] * 100).round(2)
    by_year["pct_consolidating"] = (by_year["consolidating"] / by_year["total"] * 100).round(2)
    by_year = by_year[["total", "disruptive", "consolidating", "undefined", "pct_undefined", "pct_disruptive", "pct_consolidating"]]
    sys.stderr.write(by_year.to_string() + "\n")

    if output_csv:
        by_year.to_csv(output_csv)
        sys.stderr.write(f"\nWrote {output_csv}\n")


if __name__ == "__main__":
    main()
