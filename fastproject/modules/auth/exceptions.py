from asyncpg.exceptions import UniqueViolationError


class InvalidPasswordError(ValueError):
    """Raised on password validation errors."""


class UserUsernameAlreadyExistsError(UniqueViolationError):
    """
    Raised when inserting user records in the database and the username of the
    user that will be inserted already exists in the database.
    """


class UserEmailAlreadyExistsError(UniqueViolationError):
    """
    Raised when inserting user records in the database and the email of the
    user that will be inserted already exists in the database.
    """
