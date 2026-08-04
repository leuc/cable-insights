# Source-literature instructions

Source folders contain parsed literature that cites or discusses the
1973–1979 ACP-127 cable corpus. Use “reference” or “reftel,” not “citation,”
for the cable reference graph itself.

## Related-literature MRN index

When adding or changing a parsed source folder:

1. Update that folder's `referenced_mrns.json` with every MRN that resolves
   in `data/cable-extract/all-dates.ndjson`.
2. Store the source-printed/full MRN in `mrn_full` and the corpus
   `document_number` in `mrn_normalized`.
3. Set the folder-level source metadata to its DOI (or `null` if none exists),
   a human-readable `citation`, and the exact parsed Markdown files.
4. Validate the result against
   [`referenced_mrns.schema.json`](referenced_mrns.schema.json).

Do not add unresolved or pre-CFPF references to this normalized index; retain
those caveats in the source's own findings file.

## Combining the per-source indexes

The combined view is maintained at
[`related_literature.json`](related_literature.json). Regenerate it with:

```sh
jq -s '
  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    schema_version: 1,
    description: "Deduplicated MRNs found in parsed related literature and resolved in the ACP-127 corpus.",
    normalization: {
      full: "document_number_raw-style four-digit year plus station plus serial",
      normalized: "corpus document_number-style corpus document_number"
    },
    sources: map(.source),
    mrns: (
      map(. as $source | .mrns[] | . + {source_id: $source.source.id})
      | group_by(.mrn_full)
      | map({
          mrn_full: .[0].mrn_full,
          mrn_normalized: .[0].mrn_normalized,
          source_ids: (map(.source_id) | unique)
        })
    )
  }
' data/source/*/referenced_mrns.json > data/source/related_literature.json
```

Validate the combined file against
[`related_literature.schema.json`](related_literature.schema.json).
