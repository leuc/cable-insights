# Source-literature instructions

Source folders contain parsed literature that cites or discusses the
1973–1979 ACP-127 cable corpus. Use “reference” or “reftel,” not “citation,”
for the cable reference graph itself.

## Related-literature MRN index

When adding or changing a parsed source:

1. Update [`related_literature.json`](related_literature.json) with every MRN
   that resolves in `data/cable-extract/all-dates.ndjson`.
2. Store the source-printed/full MRN in `mrn_full` and the corpus
   `document_number` in `mrn_normalized`.
3. Add or update the source entry with its DOI (or `null` if none exists), a
   human-readable `citation`, and the exact parsed Markdown file.
4. Validate the result against
   [`related_literature.schema.json`](related_literature.schema.json).

Do not add unresolved or pre-CFPF references to this normalized index; retain
those caveats in the source's own findings file.
