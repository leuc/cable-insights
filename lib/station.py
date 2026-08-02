"""Parse the originating station embedded in a normalized document_number.

Shared by questions that need a per-document station/office breakdown (most
notably separating STATE-originated cables, which behave structurally
differently from field-post cables, from the rest of the corpus). Current
consumers: questions/tags-reference-similarity,
questions/address-reference-similarity, questions/reference-time-lag.

document_number format (from acp-127's src.reftel_normalize): 2-digit year +
station name + serial number, e.g. "73BAGHDAD339", "73STATE93410". Station
names are letters only, with exactly one known exception that contains an
embedded space ("KUALA LUMPUR"). About 8% of document numbers fail to
normalize to a recognized station (an unresolved abbreviation, e.g.
"BIENH"/"FORTL"/"JECPA") and are left in raw 4-digit-year form by
reftel_normalize.py -- parse_station() correctly returns None for these
rather than guessing; callers should treat None as "station unknown", not
an error.
"""

from __future__ import annotations

import re

_DOC_NUMBER_RE = re.compile(r"^\d{2}(?P<station>[A-Z]+(?: [A-Z]+)*)\d+$")


def parse_station(document_number: str | None) -> str | None:
    """Return the station name from a normalized document_number, or None."""
    if not document_number:
        return None
    m = _DOC_NUMBER_RE.match(document_number)
    return m.group("station") if m else None
