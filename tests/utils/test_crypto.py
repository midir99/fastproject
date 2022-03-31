"""Tests for module utils.crypto."""

from fastproject.utils import crypto


def test_constant_time_compare():
    # It"s hard to test for constant time, just test the result.
    assert crypto.constant_time_compare(b"spam", b"spam")
    assert not crypto.constant_time_compare(b"spam", b"eggs")
    assert crypto.constant_time_compare("spam", "spam")
    assert not crypto.constant_time_compare("spam", "eggs")


def test_get_random_string():
    allowed_chars = "qwerty012345"
    length = 50
    random_str = crypto.get_random_string(length, allowed_chars)
    assert "a" not in random_str
    assert len(random_str) == length
