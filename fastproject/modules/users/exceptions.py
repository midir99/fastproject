from asyncpg.exceptions import UniqueViolationError


class InvalidPasswordError(ValueError):
    """Raised on password validation errors."""


class UsernameAlreadyExistsError(UniqueViolationError):
    """
    Raised when inserting user records in the database and the username of the
    user that will be inserted already exists in the database.
    """


class EmailAlreadyExistsError(UniqueViolationError):
    """
    Raised when inserting user records in the database and the email of the
    user that will be inserted already exists in the database.
    """
