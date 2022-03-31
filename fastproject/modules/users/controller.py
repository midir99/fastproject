"""Controller module."""

import uuid
from typing import Optional

import fastapi

from ...utils import http_responses
from . import exceptions, models, service

controller = fastapi.APIRouter(prefix="/users", tags=["users"])


@controller.post(
    "",
    response_model=models.PublicUser,
    status_code=fastapi.status.HTTP_201_CREATED,
    responses={fastapi.status.HTTP_409_CONFLICT: http_responses.ConflictResponse},
)
async def register_user(
    user_registration_data: models.UserRegistrationData,
) -> models.PublicUser:
    try:
        inserted = await service.insert_user(
            username=user_registration_data.username,
            email=user_registration_data.email,
            first_name=user_registration_data.first_name,
            last_name=user_registration_data.last_name,
            password=user_registration_data.password,
        )
        return models.PublicUser(**inserted.dict())
    except exceptions.UsernameAlreadyExistsError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="Username already taken.",
        ) from e
    except exceptions.EmailAlreadyExistsError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT, detail="Email already taken."
        ) from e


@controller.get(
    "/{user_id}",
    response_model=models.PublicUser,
    status_code=fastapi.status.HTTP_200_OK,
    responses={fastapi.status.HTTP_404_NOT_FOUND: http_responses.NotFoundResponse},
)
async def get_user(user_id: uuid.UUID) -> Optional[models.PublicUser]:
    searched = await service.get_user_by_id(user_id)
    if not searched:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND)
    return models.PublicUser(**searched.dict())


@controller.patch("/{user_id}", response_model=models.PublicUser)
async def patch_user(
    user_id: uuid.UUID, patchable_user_data: models.PatchableUserData
) -> Optional[models.PublicUser]:
    patchable_user_data = patchable_user_data.dict(exclude_unset=True)
    try:
        updated = await service.update_user_by_id(
            user_id=user_id, **patchable_user_data
        )
        if not updated:
            return None
        return models.PublicUser(**updated.dict())
    except exceptions.UsernameAlreadyExistsError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="Username already taken.",
        ) from e
    except exceptions.EmailAlreadyExistsError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT, detail="Email already taken."
        ) from e


@controller.delete("/{user_id}", response_model=models.PublicUser)
async def delete_user(user_id: uuid.UUID) -> Optional[models.PublicUser]:
    deleted = await service.delete_user_by_id(user_id)
    if not deleted:
        return None
    return models.PublicUser(**deleted.dict())
