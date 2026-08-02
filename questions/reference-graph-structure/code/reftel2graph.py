#!/usr/bin/env python3
import sys
import json
import os
import re
import igraph

# XML 1.0 forbids these control characters outright (tab/LF/CR are fine);
# OCR'd cable text occasionally contains raw form-feed (0x0C) etc, which
# crashes igraph's graphml writer if left in string attribute values.
_XML_FORBIDDEN_RE = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _xml_safe(s):
    return _XML_FORBIDDEN_RE.sub("", s) if s else s


def _format_tags(tags):
    """TAGS list -> multi-line "type: name (code)\n" string."""
    lines = [
        f"{t.get('type')}: {t.get('name') or t.get('code')} ({t.get('code')})"
        for t in tags
        if t.get("code")
    ]
    return _xml_safe("\n".join(lines) + "\n") if lines else None


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} ref.json output.graphml\n")
        sys.exit(1)

    src = sys.argv[1]
    dest = sys.argv[2]

    if not os.path.exists(src):
        sys.stderr.write(f"Error: Input file not found: {src}\n")
        sys.exit(1)
    if os.path.exists(dest):
        sys.stderr.write(f"Error: Output file already exists: {dest}\n")
        sys.exit(1)

    vertices = set()
    primary_docs = set()  # Track IDs that exist as a document_number
    edges = set()
    node_dates = {}
    node_previews = {}
    node_tags = {}
    count = 0

    with open(src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            row = json.loads(line)
            doc = row.get("document_number")

            if not doc:
                continue

            # Every document with a document_number becomes a vertex with
            # full detail (date/preview/tags), whether or not it has
            # outgoing references -- reference-less and/or unreferenced
            # (isolated) nodes are pruned from the finished graph at the
            # end, not excluded from attribute extraction up front.
            primary_docs.add(doc)
            vertices.add(doc)

            doc_date = row.get("date")
            if doc_date:
                node_dates[doc] = doc_date

            doc_preview = row.get("message_preview")
            if doc_preview:
                node_previews[doc] = _xml_safe(doc_preview)

            doc_tags = row.get("tags")
            if doc_tags:
                formatted = _format_tags(doc_tags)
                if formatted:
                    node_tags[doc] = formatted

            refs = row.get("extracted_references")
            if refs:
                for r in refs:
                    edges.add((doc, r))
                    vertices.add(r)

            count += 1
            if count % 500000 == 0:
                sys.stderr.write(f"  {count} lines...\n")

    sys.stderr.write(
        f"\nVertices: {len(vertices)} (Primary: {len(primary_docs)}), Edges: {len(edges)}\n"
    )

    ids = sorted(vertices)
    idx = {v: i for i, v in enumerate(ids)}

    edge_list = [(idx[f], idx[t]) for f, t in sorted(edges)]

    sys.stderr.write("Building graph...\n")
    # n=len(ids) is required now that some vertices can be genuinely
    # edge-less before pruning (a document with no refs, not cited by
    # anyone else) -- without it, igraph.Graph() infers vertex count from
    # the edge list alone and would silently drop/misalign any vertex
    # whose index isn't reached by an edge.
    g = igraph.Graph(n=len(ids), edges=edge_list, directed=True)

    # Map node properties
    g.vs["label"] = ids
    g.vs["date"] = [node_dates.get(vid, "") for vid in ids]
    g.vs["message_preview"] = [node_previews.get(vid, "") for vid in ids]
    g.vs["TAGS"] = [node_tags.get(vid, "") for vid in ids]

    # Flag missing documents: True if it ONLY appeared as a reference
    g.vs["missing"] = [vid not in primary_docs for vid in ids]

    sys.stderr.write("Pruning isolated nodes (degree 0)...\n")
    degrees = g.degree(mode="all")
    non_isolated = [i for i, d in enumerate(degrees) if d > 0]
    isolated_count = g.vcount() - len(non_isolated)
    g = g.induced_subgraph(non_isolated)
    sys.stderr.write(
        f"  Removed {isolated_count:,} isolated nodes; "
        f"final: {g.vcount():,} vertices, {g.ecount():,} edges\n"
    )

    sys.stderr.write(f"Saving {dest}...\n")
    g.write_graphml(dest)


if __name__ == "__main__":
    main()
