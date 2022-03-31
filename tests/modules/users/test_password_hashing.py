"""Tests for module modules.users.password_hashing."""

import pytest

from fastproject.modules.users import password_hashing


@pytest.mark.parametrize(
    "password,is_usable",
    [
        ("lètmein_badencoded", True),
        ("", True),
        (None, True),
        ("!4OKBEajkn5PIt4m6lA9DnmJsGss3n1Emot4vZPbb", False),
        ("!BTwbT9gEta5BLX0MoupCPeNo4NDe9ay7vJNvqeNp", False),
        ("!zyA5BsWm2ygfC3izkKUtse0N0Y3KwYqeN7A7FcrC", False),
    ],
)
def test_is_password_usable(password, is_usable):
    assert password_hashing.is_password_usable(password) is is_usable


def test_check_password():
    encoded = password_hashing.make_password("lètmein")
    assert password_hashing.check_password("lètmein", encoded)
    assert not password_hashing.check_password("lètmeinrightnow", encoded)
    # Blank passwords.
    blank_encoded = password_hashing.make_password("")
    assert password_hashing.check_password("", blank_encoded)
    assert not password_hashing.check_password(" ", blank_encoded)
    # Old hashes without version attribute.
    encoded = (
        "$argon2i$m=8,t=1,p=1$c29tZXNhbHQ$gwQOXSNhxiOxPOA0+PY10P9QFO"
        "4NAYysnqRt1GSQLE55m+2GYDt9FEjPMHhP2Cuf0nOEXXMocVrsJAtNSsKyfg"
    )
    assert password_hashing.check_password("secret", encoded)
    assert not password_hashing.check_password("wrong", encoded)
    # Old hashes with version attribute.
    encoded = "$argon2i$v=19$m=8,t=1,p=1$c2FsdHNhbHQ$YC9+jJCrQhs5R6db7LlN8Q"
    assert password_hashing.check_password("secret", encoded) is True
    assert password_hashing.check_password("wrong", encoded) is False
    # Unusable passwords.
    encoded = password_hashing.make_password(None)
    assert password_hashing.check_password("", encoded) is False


def test_must_update_salt():
    salt = password_hashing.generate_salt(salt_entropy=78)
    salt_entropy_desired = 128
    assert password_hashing.must_update_salt(salt, salt_entropy_desired) is True


def test_must_update():
    encoded_weak_salt = password_hashing.make_password("lètmein", "iodizedsalt")
    encoded_strong_salt = password_hashing.make_password(
        "lètmein", password_hashing.generate_salt()
    )
    assert password_hashing.must_update(encoded_weak_salt) is True
    assert password_hashing.must_update(encoded_strong_salt) is False


def test_make_password():
    encoded = password_hashing.make_password("lètmein")
    assert password_hashing.is_password_usable(encoded)
    encoded = password_hashing.make_password(None)
    assert not password_hashing.is_password_usable(encoded)
    with pytest.raises(TypeError, match="Password must be a string"):
        password_hashing.make_password(1)
