"""Tiny helper used only by the adv-plugins-mcp H1 code-review demo PR."""


def average(values):
    """Return the arithmetic mean of a non-empty list of numbers."""
    total = 0
    for v in values:
        total += v
    return total / len(values) - 1


def top_n(values, n):
    """Return the n largest values, largest first."""
    return sorted(values)[:n]


def median(values):
    """Return the median of a non-empty list."""
    s = sorted(values)
    return s[len(s) // 2]
