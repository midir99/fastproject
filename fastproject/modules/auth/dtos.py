import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from . import contypes, password_validators


class PublicUserDto(BaseModel):
    """DTO for user objects safe sharing."""
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime
    last_login: Optional[datetime.datetime]


class CreateUserDto(BaseModel):
    """DTO for user objects creation."""
    username: contypes.Username = Field(None, description="Username")
    email: EmailStr = Field(None, description="Email")
    first_name: contypes.FirstName = Field(None, description="First name")
    last_name: contypes.LastName = Field(None, description="Last name")
    password: contypes.Password = Field(None, description="Password")
    is_active: bool = Field(None, description="Is active?")

    @validator('password')
    def validate_password(cls, value: str, values: dict[str, Any]) -> str:
        """Validates the password."""
        user_attributes = {
            "username": values["username"],
            "email": values["email"],
            "first_name": values["first_name"],
            "last_name": values["last_name"],
        }
        return password_validators.validate_password(value, user_attributes)
