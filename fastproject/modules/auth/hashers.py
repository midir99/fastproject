import base64
import hashlib
import importlib
import math
import warnings

# from ..utils.crypto import (
from fastproject.modules.utils.crypto import (
# from modules.utils.crypto import (
    RANDOM_STRING_CHARS, constant_time_compare, get_random_string
)


def mask_hash(hash, show=6, char="*"):
    """
    Return the given hash, with only the first ``show`` number shown. The
    rest are masked with ``char`` for security reasons.
    """
    masked = hash[:show]
    masked += char * len(hash[show:])
    return masked


class BasePasswordHasher:
    """
    Abstract base class for password hashers
    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().
    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None
    salt_entropy = 128

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError as e:
                raise ValueError("Couldn't load %r algorithm library: %s" %
                                 (self.__class__.__name__, e))
            return module
        raise ValueError("Hasher %r doesn't specify a library attribute" %
                         self.__class__.__name__)

    def salt(self):
        """
        Generate a cryptographically secure nonce salt in ASCII with an entropy
        of at least `salt_entropy` bits.
        """
        # Each character in the salt provides
        # log_2(len(alphabet)) bits of entropy.
        char_count = math.ceil(self.salt_entropy / math.log2(len(RANDOM_STRING_CHARS)))
        return get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)

    def verify(self, password, encoded):
        """Check if the given password is correct."""
        raise NotImplementedError('subclasses of BasePasswordHasher must provide a verify() method')

    def _check_encode_args(self, password, salt):
        if password is None:
            raise TypeError('password must be provided.')
        if not salt or '$' in salt:
            raise ValueError('salt must be provided and cannot contain $.')

    def encode(self, password, salt):
        """
        Create an encoded database value.
        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError('subclasses of BasePasswordHasher must provide an encode() method')

    def decode(self, encoded):
        """
        Return a decoded database value.
        The result is a dictionary and should contain `algorithm`, `hash`, and
        `salt`. Extra keys can be algorithm specific like `iterations` or
        `work_factor`.
        """
        raise NotImplementedError(
            'subclasses of BasePasswordHasher must provide a decode() method.'
        )

    def safe_summary(self, encoded):
        """
        Return a summary of safe values.
        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError('subclasses of BasePasswordHasher must provide a safe_summary() method')

    def must_update(self, encoded):
        return False

    def harden_runtime(self, password, encoded):
        """
        Bridge the runtime gap between the work factor supplied in `encoded`
        and the work factor suggested by this hasher.
        Taking PBKDF2 as an example, if `encoded` contains 20000 iterations and
        `self.iterations` is 30000, this method should run password through
        another 10000 iterations of PBKDF2. Similar approaches should exist
        for any hasher that has a work factor. If not, this method should be
        defined as a no-op to silence the warning.
        """
        warnings.warn('subclasses of BasePasswordHasher should provide a harden_runtime() method')


class ScryptPasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the Scrypt algorithm.
    """
    algorithm = 'scrypt'
    block_size = 8
    maxmem = 0
    parallelism = 1
    work_factor = 2 ** 14

    def encode(self, password, salt, n=None, r=None, p=None):
        self._check_encode_args(password, salt)
        n = n or self.work_factor
        r = r or self.block_size
        p = p or self.parallelism
        hash_ = hashlib.scrypt(
            password.encode(),
            salt=salt.encode(),
            n=n,
            r=r,
            p=p,
            maxmem=self.maxmem,
            dklen=64,
        )
        hash_ = base64.b64encode(hash_).decode('ascii').strip()
        return '%s$%d$%s$%d$%d$%s' % (self.algorithm, n, salt, r, p, hash_)

    def decode(self, encoded):
        algorithm, work_factor, salt, block_size, parallelism, hash_ = encoded.split('$', 6)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'work_factor': int(work_factor),
            'salt': salt,
            'block_size': int(block_size),
            'parallelism': int(parallelism),
            'hash': hash_,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(
            password,
            decoded['salt'],
            decoded['work_factor'],
            decoded['block_size'],
            decoded['parallelism'],
        )
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('work factor'): decoded['work_factor'],
            _('block size'): decoded['block_size'],
            _('parallelism'): decoded['parallelism'],
            _('salt'): mask_hash(decoded['salt']),
            _('hash'): mask_hash(decoded['hash']),
        }

    def must_update(self, encoded):
        decoded = self.decode(encoded)
        return (
            decoded['work_factor'] != self.work_factor or
            decoded['block_size'] != self.block_size or
            decoded['parallelism'] != self.parallelism
        )

    def harden_runtime(self, password, encoded):
        # The runtime for Scrypt is too complicated to implement a sensible
        # hardening algorithm.
        pass