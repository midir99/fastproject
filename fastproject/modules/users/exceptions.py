"""Exceptions module."""

from asyncpg import exceptions


class InvalidPasswordError(ValueError):
    """Raised on password validation errors."""


class UsernameAlreadyExistsError(exceptions.UniqueViolationError):
    """
    Raised when inserting user records in the database and the username of the
    user that will be inserted already exists in the database.
    """


class EmailAlreadyExistsError(exceptions.UniqueViolationError):
    """
    Raised when inserting user records in the database and the email of the
    user that will be inserted already exists in the database.
    """
