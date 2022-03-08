from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ...utils.http_responses import NotFoundResponse, ConflictResponse
from . import service
from .models import PublicUser, SignUpUser, PatchUser
from .exceptions import UsernameAlreadyExistsError, EmailAlreadyExistsError

controller = APIRouter(
    prefix="/users",
    tags=["users"]
)


@controller.post(
    "",
    response_model=PublicUser,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: ConflictResponse
    }
)
async def sign_up_user(signup_user: SignUpUser):
    try:
        user = await service.create_user(
            username=signup_user.username,
            email=signup_user.email,
            first_name=signup_user.first_name,
            last_name=signup_user.last_name,
            password=signup_user.password,
        )
        return user
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already taken.") from e
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already taken.") from e


@controller.get(
    "/{user_id}",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundResponse
    },
)
async def get_user(user_id: UUID):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@controller.patch(
    "/{user_id}",
    response_model=PublicUser
)
async def partial_update_user(user_id: UUID, patch_user: PatchUser):
    update_date = patch_user.dict(exclude_defaults=True)
    # TODO
