from pydantic import BaseModel

from .fields import PasswordField, UsernameField


class CreateUserDto(BaseModel):
    """DTO for User objects creation."""
    username: UsernameField
    password: PasswordField
