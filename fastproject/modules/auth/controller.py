from fastapi import APIRouter

from . import service
from .dtos import PublicUserDTO, SignUpUserDTO

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("", response_model=PublicUserDTO)
async def sign_up_user(signup_user_dto: SignUpUserDTO):
    return await service.create_user(
        username=signup_user_dto.username,
        email=signup_user_dto.email,
        first_name=signup_user_dto.first_name,
        last_name=signup_user_dto.last_name,
        password=signup_user_dto.password,
    )


@router.get("/{user_id}", response_model=PublicUserDTO)
async def get_user_by_id(user_id: str):
    return await service.get_user_by_id(user_id)
