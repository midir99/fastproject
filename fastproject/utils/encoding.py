"""Utilities for encoding types."""

import datetime
import decimal
import unicodedata
from typing import Any

_PROTECTED_TYPES = (
    type(None),
    int,
    float,
    decimal.Decimal,
    datetime.datetime,
    datetime.date,
    datetime.time,
)


def is_protected_type(obj: Any) -> bool:
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_str(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)


def force_bytes(s: Any, encoding="utf-8", strings_only=False, errors="strict") -> bytes:
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    Lazy instances are resolved to strings, rather than kept as lazy objects.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == "utf-8":
            return s
        else:
            return s.decode("utf-8", errors).encode(encoding, errors)
    if strings_only and is_protected_type(s):
        return s
    if isinstance(s, memoryview):
        return bytes(s)
    return str(s).encode(encoding, errors)


def normalize_str(ustring: str) -> str:
    """Returns the normal form NFKC of the unicode string given."""
    return unicodedata.normalize("NFKC", ustring)
