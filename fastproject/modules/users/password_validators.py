"""Utilities to validate passwords."""

import difflib
import gzip
import pathlib
import re
from typing import Optional

from . import exceptions

_PASSWORD_LIST_PATH = (
    pathlib.Path(__file__).resolve().parent / "common-passwords.txt.gz"
)
_PASSWORD_LIST = set()


def _load_password_list(password_list_path=_PASSWORD_LIST_PATH) -> None:
    """Loads the password list."""
    global _PASSWORD_LIST
    try:
        with gzip.open(password_list_path, "rt", encoding="utf-8") as file:
            _PASSWORD_LIST = {p.strip() for p in file}
    except OSError:
        with open(password_list_path, "rt", encoding="utf-8") as file:
            _PASSWORD_LIST = {p.strip() for p in file}


def validate_password_length(password: str, min_length: int, max_length: int) -> str:
    """Validates that the password has the correct length."""
    if not min_length <= len(password) <= max_length:
        raise exceptions.InvalidPasswordError(
            f"Password can not have less than {min_length} or more "
            f"than {max_length} characters."
        )
    return password


def validate_password_not_numeric(password: str) -> str:
    """Validates that the password is not entirely numeric."""
    if password.isdigit():
        raise exceptions.InvalidPasswordError("Password can not be entirely numeric.")
    return password


def exceeds_maximum_length_ratio(
    password: str, max_similarity: float, value: str
) -> float:
    """
    Test that value is within a reasonable range of password.

    The following ratio calculations are based on testing difflib.SequenceMatcher like
    this:

    for i in range(0,6):
      print(10**i, difflib.SequenceMatcher(a='A', b='A'*(10**i)).quick_ratio())

    which yields:

    1 1.0
    10 0.18181818181818182
    100 0.019801980198019802
    1000 0.001998001998001998
    10000 0.00019998000199980003
    100000 1.999980000199998e-05

    This means a length_ratio of 10 should never yield a similarity higher than
    0.2, for 100 this is down to 0.02 and for 1000 it is 0.002. This can be
    calculated via 2 / length_ratio. As a result we avoid the potentially
    expensive sequence matching.
    """
    pwd_len = len(password)
    length_bound_similarity = max_similarity / 2 * pwd_len
    value_len = len(value)
    return pwd_len >= 10 * value_len and value_len < length_bound_similarity


def validate_password_not_similar_to_user_attributes(
    password: str, user_attrs: Optional[dict[str, str]]
) -> str:
    """
    Validate that the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """
    max_similarity = 0.7  # max_similarity must be at least 0.1
    password_lower = password.lower()
    for attr in user_attrs:
        attr_value = user_attrs[attr]
        if not attr_value or not isinstance(attr_value, str):
            continue
        attr_value_lower = attr_value.lower()
        parts = re.split(r"\W+", attr_value_lower) + [attr_value_lower]
        for part in parts:
            if exceeds_maximum_length_ratio(password_lower, max_similarity, part):
                continue
            if (
                difflib.SequenceMatcher(a=password_lower, b=part).quick_ratio()
                >= max_similarity
            ):
                raise exceptions.InvalidPasswordError(
                    "The password is very similar to " f"the {attr}"
                )
    return password


def validate_password_not_common(password: str) -> None:
    """
    Validates that the password not occurs in a list of 20,000 common
    passwords.
    """
    if not _PASSWORD_LIST:
        _load_password_list()
    if password.lower().strip() in _PASSWORD_LIST:
        raise exceptions.InvalidPasswordError("Password is too common.")
    return password


def validate_password(
    password: str,
    min_length: int,
    max_length: int,
    user_attrs: Optional[list[str]] = None,
) -> None:
    """
    Validates the password with all the password validation related
    functions in this module.
    """
    password = validate_password_length(password, min_length, max_length)
    password = validate_password_not_numeric(password)
    password = validate_password_not_similar_to_user_attributes(password, user_attrs)
    password = validate_password_not_common(password)
    return password
