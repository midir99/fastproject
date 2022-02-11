from typing import Any

from pydantic import BaseModel, Field, validator

from .contypes import Password, Username
from . import password_validators

class CreateUserDto(BaseModel):
    """DTO for User objects creation."""
    username: Username = Field(None, description="Username")
    password: Password = Field(None, description="Password")

    @validator('password')
    def validate_password(cls, value: str, values: dict[str, Any]) -> str:
        """Validates the password."""
        user_attributes = {
            "username": values["username"]
        }
        return password_validators.validate_password(value, user_attributes)
