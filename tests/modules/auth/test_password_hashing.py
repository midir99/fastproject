import pytest

from fastproject.modules.auth.password_hashing import (
    check_password,
    generate_salt,
    is_password_usable,
    make_password,
    must_update,
)


@pytest.mark.parametrize(
    "password,is_usable",
    [
        ("lètmein_badencoded", True),
        ("", True),
        (None, True),
        ("!4OKBEajkn5PIt4m6lA9DnmJsGss3n1Emot4vZPbb", False),
        ("!BTwbT9gEta5BLX0MoupCPeNo4NDe9ay7vJNvqeNp", False),
        ("!zyA5BsWm2ygfC3izkKUtse0N0Y3KwYqeN7A7FcrC", False),
    ]
)
def test_is_password_usable(password, is_usable):
    assert is_password_usable(password) is is_usable


def test_argon2_password_hashing():
    encoded = make_password("lètmein")
    assert is_password_usable(encoded)
    assert check_password("lètmein", encoded)
    assert not check_password("lètmeinz", encoded)
    # Blank passwords.
    blank_encoded = make_password("")
    assert is_password_usable(blank_encoded)
    assert check_password("", blank_encoded)
    assert not check_password(" ", blank_encoded)
    # Old hashes without version attribute.
    encoded = (
        "$argon2i$m=8,t=1,p=1$c29tZXNhbHQ$gwQOXSNhxiOxPOA0+PY10P9QFO"
        "4NAYysnqRt1GSQLE55m+2GYDt9FEjPMHhP2Cuf0nOEXXMocVrsJAtNSsKyfg"
    )
    assert check_password("secret", encoded)
    assert not check_password("wrong", encoded)
    # Old hashes with version attribute.
    encoded = "$argon2i$v=19$m=8,t=1,p=1$c2FsdHNhbHQ$YC9+jJCrQhs5R6db7LlN8Q"
    assert check_password("secret", encoded) is True
    assert check_password("wrong", encoded) is False
    # Check salt entropy.
    encoded_weak_salt = make_password("lètmein", "iodizedsalt")
    encoded_strong_salt = make_password("lètmein", generate_salt())
    assert must_update(encoded_weak_salt) is True
    assert must_update(encoded_strong_salt) is False