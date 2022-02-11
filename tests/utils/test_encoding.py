import datetime

from fastproject.utils.encoding import force_bytes


def test_force_bytes_exception():
    """
    force_bytes knows how to convert to bytes an exception
    containing non-ASCII characters in its args.
    """
    error_msg = "This is an exception, voilà"
    exc = ValueError(error_msg)
    assert force_bytes(exc) == error_msg.encode()
    assert force_bytes(exc, encoding="ascii", errors="ignore") == b"This is an exception, voil"


def test_force_bytes_strings_only():
    today = datetime.date.today()
    assert force_bytes(today, strings_only=True) == today


def test_force_bytes_encoding():
    error_msg = "This is an exception, voilà".encode()
    result = force_bytes(error_msg, encoding="ascii", errors="ignore")
    assert result == b"This is an exception, voil"


def test_force_bytes_memory_view():
    data = b"abc"
    result = force_bytes(memoryview(data))
    # Type check is needed because memoryview(bytes) == bytes.
    assert type(result) is bytes
    assert result == data
