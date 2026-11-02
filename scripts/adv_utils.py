"""Small utility helpers."""

import re
import unicodedata


def slugify(text):
    """Convert text to a lowercase, hyphen-separated ASCII slug.

    Unicode accents are stripped (e.g. "Café" -> "cafe").
    """
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
