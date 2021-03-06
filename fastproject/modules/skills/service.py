from typing import Optional

from ...utils.encoding import normalize_str
from . import repository
from .dtos import PublicSkillDTO


async def create_skill(name: str) -> PublicSkillDTO:
    name = normalize_str(name)
    return await repository.insert_skill(name)


async def get_skill_by_id(skill_id: str) -> Optional[PublicSkillDTO]:
    return await repository.get_skill_by_id(skill_id)
