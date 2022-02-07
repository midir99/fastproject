from fastapi import APIRouter


from .dtos import CreateUserDto


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('')
async def create_user(create_user_dto: CreateUserDto) -> str:
    """Endpoint for User objects creation."""
    return 'User successfully created.'
