import gzip
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any, ClassVar

from pydantic.validators import str_validator


COMMON_PASSWORDS_PATH = Path(__file__).resolve().parent / 'common-passwords.txt.gz'


class UsernameField(str):
    """Username field (inspired by Twitter usernames)."""

    _field_name: ClassVar[str] = "username"
    _username_allowed_chars: ClassVar[str] = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    _max_length: ClassVar[int] = 15
    _min_length: ClassVar[int] = 4

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield str_validator
        yield cls.validate_length
        yield cls.validate_only_contains_allowed_chars

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type='string', max_length=cls._max_length,
                            min_length=cls._min_length)

    @classmethod
    def validate_length(cls, value: str) -> 'UsernameField':
        """Validates that the username has the correct length."""
        if not cls._min_length <= len(value) <= cls._max_length:
            raise ValueError(f'"{cls._field_name}" can not have less than '
                             f'{cls._min_length} or more than '
                             f'{cls._max_length} characters.')
        return cls(value)

    @classmethod
    def validate_only_contains_allowed_chars(
            cls, value: str) -> 'UsernameField':
        """
        Validates that the username only contains allowed characters.
        """
        if set(value).difference(cls._username_allowed_chars):
            raise ValueError(f'"{cls._field_name}" can only contain '
                             'alphanumeric characters and underscores.')
        return cls(value)


class PasswordField(str):
    """Password field."""

    _field_name: ClassVar[str] = 'password'
    _max_length: ClassVar[int] = 128
    _min_length: ClassVar[int] = 9
    _common_passwords: ClassVar[set[str]] = {}

    @classmethod
    def _load_common_passwords(
            cls, password_list_path: str = COMMON_PASSWORDS_PATH) -> None:
        # pylint: disable=invalid-name
        try:
            with gzip.open(password_list_path, 'rt', encoding='UTF-8') as f:
                cls._common_passwords = {p.strip() for p in f}
        except OSError:
            with open(password_list_path, 'rt', encoding='UTF-8') as f:
                cls._common_passwords = {p.strip() for p in f}

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield str_validator
        yield cls.validate_length
        yield cls.validate_not_numeric
        yield cls.validate_not_common

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type='string', max_length=cls._max_length,
                            min_length=cls._min_length)

    @classmethod
    def validate_length(cls, value: Any) -> 'PasswordField':
        """Validates that the password has the correct length."""
        if not cls._min_length <= len(value) <= cls._max_length:
            raise ValueError(f'"{cls._field_name}" can not have less than '
                             f'{cls._min_length} or more than '
                             f'{cls._max_length} characters.')
        return cls(value)

    @classmethod
    def validate_not_numeric(cls, value: Any) -> 'PasswordField':
        """Validates that the password is not entirely numeric."""
        if value.isdigit():
            raise ValueError(f'"{cls._field_name}" can not be entirely '
                             'numeric.')
        return cls(value)

    @classmethod
    def validate_not_common(cls, value: Any) -> 'PasswordField':
        """
        Validates that the password not occurs in a list of 20,000 common
        passwords.
        """
        if not cls._common_passwords:
            cls._load_common_passwords()
        if value.lower().strip() in cls._common_passwords:
            raise ValueError(f'"{cls._field_name}" is too common.')
        return cls(value)
