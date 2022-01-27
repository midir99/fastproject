from pydantic import BaseModel


class SkillDto(BaseModel):
    skill_id: int
    name: str


class CreateSkillDto(BaseModel):
    name: str
