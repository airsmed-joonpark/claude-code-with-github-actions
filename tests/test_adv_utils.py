import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from adv_utils import slugify


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_collapses_and_strips():
    assert slugify("  --Foo   Bar--  ") == "foo-bar"


def test_slugify_empty():
    assert slugify("") == ""
