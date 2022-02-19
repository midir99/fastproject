from fastapi import APIRouter

from . import operations
from .dtos import CreateSkillDto, PublicSkillDto

router = APIRouter(
    prefix="/skills",
    tags=["skills"]
)


@router.post("")
async def create_skill(create_skill_dto: CreateSkillDto):
    skill_id = await operations.create_skill(create_skill_dto.name)
    return PublicSkillDto(skill_id=skill_id, name=create_skill_dto.name)


@router.get("/{skill_id}")
async def get_skill(skill_id: str):
    return await operations.get_skill(skill_id)
