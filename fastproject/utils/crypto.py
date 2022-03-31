"""Utilities for cryptography."""

import secrets
from typing import AnyStr

from . import encoding

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def constant_time_compare(val1: AnyStr, val2: AnyStr) -> bool:
    """Return True if the two strings are equal, False otherwise."""
    return secrets.compare_digest(
        encoding.force_bytes(val1), encoding.force_bytes(val2)
    )


def get_random_string(length: int, allowed_chars=RANDOM_STRING_CHARS) -> str:
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return "".join(secrets.choice(allowed_chars) for _ in range(length))
