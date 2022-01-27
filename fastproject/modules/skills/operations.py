from pathlib import Path

import aiosql

from ...db import with_connection
from .dtos import SkillDto


_queries = aiosql.from_path(Path(__file__).resolve().parent / 'queries.sql',
                            'asyncpg')


@with_connection
async def create_skill(conn, name) -> int:
    return await _queries.insert_skill(conn, name=name)


@with_connection
async def get_skill(conn, skill_id) -> SkillDto:
    skill_data = await _queries.get_skill(conn, skill_id=skill_id)
    return SkillDto(skill_id=skill_data['skill_id'], name=skill_data['name'])
