"""Models module."""

import datetime
import uuid
from typing import Any, Optional

import pydantic

from . import contypes, password_validators


class PublicUser(pydantic.BaseModel):
    """Represents user data that can be shared with the public."""

    user_id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime
    last_login: Optional[datetime.datetime]


class PatchableUserData(pydantic.BaseModel):
    """
    Represents user data that can be used to partially update a user in the
    database.
    """

    username: Optional[contypes.Username] = pydantic.Field(None, description="Username")
    email: Optional[pydantic.EmailStr] = pydantic.Field(None, description="Email")
    first_name: Optional[contypes.FirstName] = pydantic.Field(
        None, description="First name"
    )
    last_name: Optional[contypes.LastName] = pydantic.Field(
        None, description="Last name"
    )
    password: Optional[contypes.Password] = pydantic.Field(None, description="Password")
    is_superuser: Optional[bool] = pydantic.Field(None, description="Is superuser?")
    is_staff: Optional[bool] = pydantic.Field(None, description="Is staff?")
    is_active: Optional[bool] = pydantic.Field(None, description="Is active?")
    date_joined: Optional[datetime.datetime] = pydantic.Field(
        None, description="Date joined"
    )
    last_login: Optional[datetime.datetime] = pydantic.Field(
        None, description="Last login"
    )


class UserRegistrationData(pydantic.BaseModel):
    """
    Represents user data that can be used to register a user in the system and
    insert that user in the database.
    """

    username: contypes.Username = pydantic.Field(None, description="Username")
    email: pydantic.EmailStr = pydantic.Field(None, description="Email")
    first_name: contypes.FirstName = pydantic.Field(None, description="First name")
    last_name: contypes.LastName = pydantic.Field(None, description="Last name")
    password: contypes.Password = pydantic.Field(None, description="Password")

    @pydantic.validator("password")
    def validate_password(cls, value: str, values: dict[str, Any]) -> str:
        """Validates the password."""
        user_attributes = {
            "username": values["username"],
            "email": values["email"],
            "first_name": values["first_name"],
            "last_name": values["last_name"],
        }
        return password_validators.validate_password(
            value,
            contypes.Password.min_length,
            contypes.Password.max_length,
            user_attributes,
        )
