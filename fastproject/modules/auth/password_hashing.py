"""Functions to hash and verify passwords using Argon2 algorithm."""

import base64
import math
from typing import Any, Optional

import argon2

from ...utils.crypto import RANDOM_STRING_CHARS, get_random_string

SALT_ENTROPY = 128

# This will never be a valid encoded hash
UNUSABLE_PASSWORD_PREFIX = "!"
# Number of random chars to add after UNUSABLE_PASSWORD_PREFIX
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40


_ARGON2_PARAMS = argon2.Parameters(
    type=argon2.low_level.Type.ID,
    version=argon2.low_level.ARGON2_VERSION,
    salt_len=argon2.DEFAULT_RANDOM_SALT_LENGTH,
    hash_len=argon2.DEFAULT_HASH_LENGTH,
    time_cost=2,
    memory_cost=102400,
    parallelism=8
)


def is_password_usable(encoded: Optional[str]) -> bool:
    """
    Return True if this password wasn't generated by make_password(None).
    """
    return encoded is None or not encoded.startswith(UNUSABLE_PASSWORD_PREFIX)


def check_password(password: Optional[str], encoded: str) -> bool:
    """
    Return a boolean of whether the raw password matches the three
    part encoded digest.
    """
    if password is None or not is_password_usable(encoded):
        return False
    try:
        return argon2.PasswordHasher().verify(encoded, password)
    except argon2.exceptions.VerificationError:
        return False


def generate_salt(salt_entropy=SALT_ENTROPY) -> str:
    """
    Generate a cryptographically secure nonce salt in ASCII with an entropy
    of at least `salt_entropy` bits.
    """
    # Each character in the salt provides log_2(len(alphabet)) bits of entropy.
    char_count = math.ceil(salt_entropy / math.log2(len(RANDOM_STRING_CHARS)))
    return get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)


def must_update_salt(salt, expected_entropy: int) -> bool:
    """Returns True is the salt used to hash a password must be updated."""
    # Each character in the salt provides log_2(len(alphabet)) bits of entropy.
    return len(salt) * math.log2(len(RANDOM_STRING_CHARS)) < expected_entropy


def make_password(password: Optional[str], salt: Optional[str] = None) -> str:
    """
    Turn a plain-text password into a hash for database storage.

    If password is None then return a concatenation of UNUSABLE_PASSWORD_PREFIX
    and a random string, which disallows logins. Additional random string
    reduces chances of gaining access to staff or superuser accounts.
    """
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(
            UNUSABLE_PASSWORD_SUFFIX_LENGTH
        )
    if not isinstance(password, str):
        raise TypeError(
            f"Password must be a string, got {type(password).__qualname__}.")
    salt = salt or generate_salt()
    params = _ARGON2_PARAMS
    encoded = argon2.low_level.hash_secret(
        password.encode(),
        salt.encode(),
        time_cost=params.time_cost,
        memory_cost=params.memory_cost,
        parallelism=params.parallelism,
        hash_len=params.hash_len,
        type=params.type,
    )
    return encoded.decode("ascii")


def decode_hash(encoded: str) -> dict[str, Any]:
    """Retunrs the decoded password hash."""
    params = argon2.extract_parameters(encoded)
    variety, *_, b64salt, hash_ = encoded.split("$")
    # Add padding.
    b64salt += "=" * (-len(b64salt) % 4)
    salt = base64.b64decode(b64salt).decode("latin1")
    return {
        "hash": hash_,
        "memory_cost": params.memory_cost,
        "parallelism": params.parallelism,
        "salt": salt,
        "time_cost": params.time_cost,
        "variety": variety,
        "version": params.version,
        "params": params,
    }


def must_update(encoded: str) -> bool:
    """Returns True if the password hash must be updated, False otherwise.

    When the password hashing parameters change, it's also necessary to update
    the hash with this new parameters.
    """
    decoded = decode_hash(encoded)
    current_params = decoded["params"]
    new_params = _ARGON2_PARAMS
    # Set salt_len to the salt_len of the current parameters because salt
    # is explicitly passed to argon2.
    new_params.salt_len = current_params.salt_len
    update_salt = must_update_salt(decoded["salt"], SALT_ENTROPY)
    return (current_params != new_params) or update_salt
