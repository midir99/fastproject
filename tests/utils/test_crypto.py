from fastproject.utils.crypto import constant_time_compare


def test_constant_time_compare():
    # It"s hard to test for constant time, just test the result.
    assert constant_time_compare(b"spam", b"spam")
    assert not constant_time_compare(b"spam", b"eggs")
    assert constant_time_compare("spam", "spam")
    assert not constant_time_compare("spam", "eggs")
