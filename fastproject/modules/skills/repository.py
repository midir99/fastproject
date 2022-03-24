from pathlib import Path
from typing import Optional

import aiosql
import asyncpg
from asyncpg.pool import PoolAcquireContext

from ...db import with_connection
from .dtos import PublicSkillDTO
from .exceptions import SkillNameAlreadyExistsError

_queries = aiosql.from_path(Path(__file__).resolve().parent / "sql", "asyncpg")


@with_connection
async def insert_skill(conn: PoolAcquireContext, name: str) -> Optional[PublicSkillDTO]:
    """Inserts a skill into the database.

    This function inserts the given values "as-is", so you must make the
    desired transformations to the values before using this function.

    Args:
      conn: A database connection.
      name: The value for the "name" field of the skill table.

    Returns:
      A PublicSkillDto representing the inserted skill.

    Raises:
      SkillNameAlreadyExistsError: If the name already exists.
    """
    try:
        inserted = await _queries.insert_skill(conn, name=name)
        return PublicSkillDTO(**inserted)
    except asyncpg.UniqueViolationError as e:
        msg = str(e)
        if "name" in msg:
            raise SkillNameAlreadyExistsError from e
        raise e from e


@with_connection
async def get_skill_by_id(
    conn: PoolAcquireContext, skill_id: str
) -> Optional[PublicSkillDTO]:
    """Returns a skill from the database with the given skill_id.

    Args:
      conn: A database connection.
      skill_id: The skill_id of the searched skill.

    Returns:
      A PublicSkillDTO representing the searched skill, None if the skill was
      not found.
    """
    searched = await _queries.get_skill_by_id(conn, skill_id=skill_id)
    if searched:
        return PublicSkillDTO(**searched)
    return None
