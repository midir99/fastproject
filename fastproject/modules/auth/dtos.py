import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from . import password_validators
from .contypes import UserConTypes



class PublicUserDTO(BaseModel):
    """DTO for user objects safe sharing."""
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


class SignUpUserDTO(BaseModel):
    """DTO for user objects creation."""
    username: UserConTypes.Username = Field(None, description="Username")
    email: EmailStr = Field(None, description="Email")
    first_name: UserConTypes.FirstName = Field(None, description="First name")
    last_name: UserConTypes.LastName = Field(None, description="Last name")
    password: UserConTypes.Password = Field(None, description="Password")

    @validator('password')
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
            UserConTypes.Password.min_length,
            UserConTypes.Password.max_length,
            user_attributes
        )
