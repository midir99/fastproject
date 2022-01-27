from fastapi import APIRouter


from .dtos import CreateSkillDto, SkillDto
from . import operations


router = APIRouter(
    prefix='/skills',
    tags=['skills']
)


@router.post("")
async def create_skill(create_skill_dto: CreateSkillDto):
    skill_id = await operations.create_skill(create_skill_dto.name)
    return SkillDto(skill_id, create_skill_dto.name)


@router.get("/{skill_id}")
async def get_skill(skill_id: int):
    return await operations.get_skill(skill_id)
