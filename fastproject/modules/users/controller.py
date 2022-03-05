from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ...utils.http_responses import NotFoundResponse, ConflictResponse
from . import service
from .models import PublicUser, SignUpUser
from .exceptions import UsernameAlreadyExistsError, EmailAlreadyExistsError

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "",
    response_model=PublicUser,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: ConflictResponse
    }
)
async def sign_up_user(signup_user_dto: SignUpUser):
    try:
        user = await service.create_user(
            username=signup_user_dto.username,
            email=signup_user_dto.email,
            first_name=signup_user_dto.first_name,
            last_name=signup_user_dto.last_name,
            password=signup_user_dto.password,
        )
        return user
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already taken.") from e
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already taken.") from e


@router.get(
    "/{user_id}",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundResponse
    },
)
async def get_user_by_id(user_id: UUID):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
