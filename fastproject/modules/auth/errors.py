class InvalidPasswordError(ValueError):
    """Raised on password validation errors."""


class UsernameAlreadyExistsError(ValueError):
    """Raised when inserting user objects in the database."""


class EmailAlreadyExistsError(ValueError):
    """Raised when inserting user objects in the database."""
