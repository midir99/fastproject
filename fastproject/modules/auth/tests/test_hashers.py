import pytest

from ..hashers import (
    is_password_usable, check_password, make_password, mask_hash
)


@pytest.mark.parametrize(
    'password,is_usable',
    [
        ('lètmein_badencoded', False),
        ('', False),
        (None, False),
    ]
)
def test_is_password_usable(password, is_usable):
    assert is_password_usable(password) == is_usable


def test_check_password():
    hasher = get_hasher('default')
    encoded = make_password('letmein')

    with mock.patch.object(hasher, 'harden_runtime'), \
            mock.patch.object(hasher, 'must_update', return_value=True):
        # Correct password supplied, no hardening needed
        check_password('letmein', encoded)
        self.assertEqual(hasher.harden_runtime.call_count, 0)

        # Wrong password supplied, hardening needed
        check_password('wrong_password', encoded)
        self.assertEqual(hasher.harden_runtime.call_count, 1)


def test_make_password():
    assert True


def test_mask_hash():
    assert False
