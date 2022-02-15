from fastapi import APIRouter, Query


from .dtos import CreateUserDto, PublicUserDto
from . import operations
from .password_hashing import make_password


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("", response_model=PublicUserDto)
async def create_user(create_user_dto: CreateUserDto):
    return await operations.create_user(create_user_dto)


@router.get("/unusable_password")
async def generate_unusable_password():
    return make_password(None)


@router.get("/{user_id}", response_model=PublicUserDto)
async def get_user(user_id: int):
    return await operations.get_user_by_id(user_id)



