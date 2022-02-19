from pathlib import Path

import aiosql

from ...db import with_connection
from .dtos import PublicSkillDto

_queries = aiosql.from_path(Path(__file__).resolve().parent / "sql", "asyncpg")


@with_connection
async def create_skill(conn, name) -> int:
    """Inserts a skill in the database.

    Args:
        conn: A database connection.
        name: The name of the skill that will be created.

    Returns:
        The skill_id of the skill object created.
    """
    # pylint: disable-next=no-member
    return await _queries.insert_skill(conn, name=name)


@with_connection
async def get_skill(conn, skill_id: str) -> PublicSkillDto:
    """Gets a skill by its skill_id.

    Args:
        conn: A database connection.
        skill_id: The skill_id of the wanted skill.

    Returns:
        A SkillDto containing the skill data.

    Raises:
        SkillDoesNotExist: The skill with the given skill_id does not exist.
    """
    # pylint: disable-next=no-member
    skill_data = await _queries.get_skill(conn, skill_id=skill_id)
    return SkillDto(skill_id=skill_data["skill_id"], name=skill_data["name"])
