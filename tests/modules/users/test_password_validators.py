"""Tests for module modules.users.password_validators."""

import pytest

from fastproject.modules.users import exceptions, password_validators


@pytest.mark.parametrize(
    "password,min_len,max_len,raises",
    [
        ("d4nz4D3G4rd3nI@s", 4, 16, False),
        ("", 0, 1, False),
        ("123456", 6, 6, False),
        ("1234567", 6, 7, False),
        ("12", 6, 7, True),
    ],
)
def test_validate_password_length(password, min_len, max_len, raises):
    if raises:
        with pytest.raises(
            exceptions.InvalidPasswordError, match="Password can not have less than"
        ):
            password_validators.validate_password_length(password, min_len, max_len)
    else:
        password_validators.validate_password_length(password, min_len, max_len)


@pytest.mark.parametrize(
    "password,raises", [("123456", True), ("a12345", False), ("abcded", False)]
)
def test_validate_password_not_numeric(password, raises):
    if raises:
        with pytest.raises(
            exceptions.InvalidPasswordError,
            match="Password can not be entirely numeric.",
        ):
            password_validators.validate_password_not_numeric(password)
    else:
        password_validators.validate_password_not_numeric(password)
