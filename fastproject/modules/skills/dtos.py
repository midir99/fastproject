import uuid

from pydantic import BaseModel


class PublicSkillDto(BaseModel):
    skill_id: uuid.UUID
    name: str


class CreateSkillDto(BaseModel):
    name: str
