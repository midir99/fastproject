from asyncpg.exceptions import UniqueViolationError


class SkillNameAlreadyExistsError(UniqueViolationError):
    """
    Raised when inserting skill objects in the database and the name of the
    skill that will be inserted already exists in the database.
    """
