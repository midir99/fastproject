from uuid import UUID

from pydantic import BaseModel

from .contypes import SkillConTypes


class PublicSkillDTO(BaseModel):
    skill_id: UUID
    name: str


class CreateSkillDTO(BaseModel):
    name: SkillConTypes.Name


class UpdateSkillNameDTO(BaseModel):
    name: SkillConTypes.Name
