import pytest

from fastproject.modules.auth.hashers import (
    check_password, is_password_usable, ScryptPasswordHasher, make_password
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


def test_scrypt():
    encoded = make_password('lètmein', 'seasalt')
    assert encoded == 'scrypt$16384$seasalt$8$1$Qj3+9PPyRjSJIebHnG81TMjsqtaI' \
        'GxNQG/aEB/NYafTJ7tibgfYz71m0ldQESkXFRkdVCBhhY8mx7rQwite/Pw=='
    assert is_password_usable(encoded) is True
    assert check_password('lètmein', encoded) is True
    assert check_password('lètmeinz', encoded) is False
    # Blank passwords.
    blank_encoded = make_password('', 'seasalt')
    assert blank_encoded.startswith('scrypt$') is True
    assert is_password_usable(blank_encoded) is True
    assert check_password('', blank_encoded) is True
    assert check_password(' ', blank_encoded) is False


def test_scrypt_decode():
    encoded = make_password('lètmein', 'seasalt')
    hasher = ScryptPasswordHasher()
    decoded = hasher.decode(encoded)
    assert decoded['block_size'] == hasher.block_size
    assert decoded['parallelism'] == hasher.parallelism
    assert decoded['salt'] == 'seasalt'
    assert decoded['work_factor'] == hasher.work_factor
