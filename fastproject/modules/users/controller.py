from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ...utils.http_responses import ConflictResponse, NotFoundResponse
from . import service
from .exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from .models import PatchableUserData, PublicUserData, UserRegistrationData

controller = APIRouter(prefix="/users", tags=["users"])


@controller.post(
    "",
    response_model=PublicUserData,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: ConflictResponse},
)
async def register_user(
    user_registration_data: UserRegistrationData,
) -> PublicUserData:
    try:
        inserted = await service.insert_user(
            username=user_registration_data.username,
            email=user_registration_data.email,
            first_name=user_registration_data.first_name,
            last_name=user_registration_data.last_name,
            password=user_registration_data.password,
        )
        return PublicUserData(**inserted.dict())
    except UsernameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken."
        ) from e
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already taken."
        ) from e


@controller.get(
    "/{user_id}",
    response_model=PublicUserData,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: NotFoundResponse},
)
async def get_user(user_id: UUID) -> Optional[PublicUserData]:
    searched = await service.get_user_by_id(user_id)
    if not searched:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return PublicUserData(**searched.dict())


@controller.patch("/{user_id}", response_model=PublicUserData)
async def patch_user(
    user_id: UUID, patchable_user_data: PatchableUserData
) -> Optional[PublicUserData]:
    patchable_user_data = patchable_user_data.dict(exclude_unset=True)
    try:
        updated = await service.update_user_by_id(
            user_id=user_id, **patchable_user_data
        )
        if not updated:
            return None
        return PublicUserData(**updated.dict())
    except UsernameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken."
        ) from e
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already taken."
        ) from e


@controller.delete("/{user_id}", response_model=PublicUserData)
async def delete_user(user_id: UUID) -> Optional[PublicUserData]:
    deleted = await service.delete_user_by_id(user_id)
    if not deleted:
        return None
    return PublicUserData(**deleted.dict())
