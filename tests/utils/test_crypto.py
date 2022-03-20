from fastproject.utils.crypto import constant_time_compare, get_random_string


def test_constant_time_compare():
    # It"s hard to test for constant time, just test the result.
    assert constant_time_compare(b"spam", b"spam")
    assert not constant_time_compare(b"spam", b"eggs")
    assert constant_time_compare("spam", "spam")
    assert not constant_time_compare("spam", "eggs")


def test_get_random_string():
    allowed_chars = "qwerty012345"
    length = 50
    random_str = get_random_string(length, allowed_chars)
    assert "a" not in random_str
    assert len(random_str) == length
