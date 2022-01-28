from ..crypto import constant_time_compare, get_random_string


def test_constant_time_compare():
    # It's hard to test for constant time, just test the result.
    assert constant_time_compare(b'spam', b'spam')
    assert not constant_time_compare(b'spam', b'eggs')
    assert constant_time_compare('spam', 'spam')
    assert not constant_time_compare('spam', 'eggs')


def test_get_random_string():
    assert False
