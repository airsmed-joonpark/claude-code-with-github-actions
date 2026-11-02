import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from adv_utils import slugify


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_collapses_and_strips():
    assert slugify("  --Foo   Bar--  ") == "foo-bar"


def test_slugify_unicode_accents():
    assert slugify("Café Crème Brûlée") == "cafe-creme-brulee"
    assert slugify("Ñandú à la façon") == "nandu-a-la-facon"


def test_slugify_empty():
    assert slugify("") == ""


def test_slugify_whitespace_only():
    assert slugify("   ") == ""
    assert slugify("\t\n  \r\n") == ""
