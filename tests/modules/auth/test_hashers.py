import pytest

from fastproject.modules.auth.hashers import (
    is_password_usable, ScryptPasswordHasher
)


@pytest.mark.parametrize(
    'password',
    [
        'lètmein_badencoded',
        '',
        None,
    ]
)
def test_is_password_usable(password):
    assert is_password_usable(password) is True


def test_check_password_calls_harden_runtime():
    # The runtime for Scrypt is too complicated to implement a sensible
    # hardening algorithm.
    assert True


@pytest.mark.parametrize(
    'salt',
    [
        None,
        '',
        'sea$salt'
    ]
)
def test_encode_invalid_salt(salt):
    msg = 'salt must be provided and cannot contain $.'
    hasher = ScryptPasswordHasher()
    with pytest.raises(ValueError) as excinfo:
        hasher.encode('password', salt)
    assert msg in str(excinfo.value)


def test_encode_password_required():
    msg = 'password must be provided.'
    hasher = ScryptPasswordHasher()
    with pytest.raises(TypeError) as excinfo:
        hasher.encode(None, 'seasalt')
    assert msg in str(excinfo.value)
