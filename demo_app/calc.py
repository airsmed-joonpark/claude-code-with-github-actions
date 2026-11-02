"""Small functions used by the Step 7 CI auto-fix exercise.

Break one of them on a branch (for example change len(values) to len(values) - 1),
push, and watch Step 7 fix it. See docs/08-ci-autofix.md.
"""


def average(values):
    """Arithmetic mean of a non-empty list of numbers."""
    if not values:
        raise ValueError("average() needs at least one value")
    return sum(values) / len(values)


def clamp(value, low, high):
    """Limit value to the range [low, high]."""
    if low > high:
        raise ValueError("low must be <= high")
    return max(low, min(value, high))


def word_count(text):
    """Number of whitespace-separated words."""
    return len(text.split())
