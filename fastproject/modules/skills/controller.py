from uuid import UUID

from fastapi import APIRouter

from . import service
from .dtos import CreateSkillDTO, PublicSkillDTO, UpdateSkillNameDTO

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("", response_model=PublicSkillDTO)
async def create_skill(create_skill_dto: CreateSkillDTO):
    return await service.create_skill(create_skill_dto.name)


@router.get("/{skill_id}", response_model=PublicSkillDTO)
async def get_skill_by_id(skill_id: UUID):
    return await service.get_skill_by_id(skill_id)


@router.patch("/{skill_id}/name", response_model=PublicSkillDTO)
async def update_skill_name(skill_id: UUID, update_skill_name_dto: UpdateSkillNameDTO):
    pass
