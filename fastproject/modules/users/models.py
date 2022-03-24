import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from . import contypes, password_validators


class UserEntity(BaseModel):
    """Represents user entity in the database."""

    user_id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime
    last_login: Optional[datetime.datetime]


class PublicUserData(BaseModel):
    """Represents user data that is safe to share with the public."""

    user_id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime
    last_login: Optional[datetime.datetime]


class PatchableUserData(BaseModel):
    """
    Represents user data that can be used to partially update a user in the
    database.
    """

    username: Optional[contypes.Username] = Field(None, description="Username")
    email: Optional[EmailStr] = Field(None, description="Email")
    first_name: Optional[contypes.FirstName] = Field(None, description="First name")
    last_name: Optional[contypes.LastName] = Field(None, description="Last name")
    password: Optional[contypes.Password] = Field(None, description="Password")
    is_superuser: Optional[bool] = Field(None, description="Is superuser?")
    is_staff: Optional[bool] = Field(None, description="Is staff?")
    is_active: Optional[bool] = Field(None, description="Is active?")
    date_joined: Optional[datetime.datetime] = Field(None, description="Date joined")
    last_login: Optional[datetime.datetime] = Field(None, description="Last login")


class UserRegistrationData(BaseModel):
    """
    Represents user data that can be used to register a user in the system and
    insert that user in the database.
    """

    username: contypes.Username = Field(None, description="Username")
    email: EmailStr = Field(None, description="Email")
    first_name: contypes.FirstName = Field(None, description="First name")
    last_name: contypes.LastName = Field(None, description="Last name")
    password: contypes.Password = Field(None, description="Password")

    @validator("password")
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
