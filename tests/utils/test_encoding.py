import datetime
from decimal import Decimal
from unicodedata import is_normalized

import pytest

from fastproject.utils.encoding import (force_bytes, is_protected_type,
                                        normalize_str)


@pytest.mark.parametrize(
    "protected_type,is_protected_type_",
    [
        (None, True),
        (5, True),
        (3.14, True),
        (Decimal(9.3), True),
        (datetime.datetime.now(), True),
        (datetime.date.today(), True),
        (datetime.time.min, True),
        (False, True),
        ("Shanalotte", False),
        (b"Twin Princess", False),
        ([], False),
    ],
)
def test_is_protected_type(protected_type, is_protected_type_):
    assert is_protected_type(protected_type) is is_protected_type_


def test_force_bytes_exception():
    """
    force_bytes knows how to convert to bytes an exception
    containing non-ASCII characters in its args.
    """
    error_msg = "This is an exception, voilà"
    exc = ValueError(error_msg)
    assert force_bytes(exc) == error_msg.encode()
    assert (
        force_bytes(exc, encoding="ascii", errors="ignore")
        == b"This is an exception, voil"
    )


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


def test_normalize_str():
    string = "María de todos los Ángeles"
    norm_str = normalize_str(string)
    assert is_normalized("NFKC", norm_str)
