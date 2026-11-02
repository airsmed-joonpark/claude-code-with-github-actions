"""Small utility helpers."""

import re


def slugify(text):
    """Convert text to a lowercase, hyphen-separated slug."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
