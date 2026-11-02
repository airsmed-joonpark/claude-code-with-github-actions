import pytest

from demo_app.calc import average, clamp, word_count


def test_average():
    assert average([2, 4, 6]) == 4
    assert average([5]) == 5


def test_average_empty():
    with pytest.raises(ValueError):
        average([])


def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-3, 0, 10) == 0
    assert clamp(42, 0, 10) == 10


def test_word_count():
    assert word_count("hello  world  again") == 3
    assert word_count("") == 0
