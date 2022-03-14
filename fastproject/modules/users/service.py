import datetime
import zoneinfo
from collections.abc import Awaitable
from typing import Optional
from uuid import UUID

from ...config import settings
from ...utils.encoding import normalize_str
from . import repository
from .models import UserEntity
from .password_hashing import make_password


async def insert_user(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    date_joined: Optional[datetime.datetime] = None,
    is_superuser=False,
    is_staff=False,
    is_active=True,
    last_login: Optional[datetime.datetime] = None
) -> Awaitable[UserEntity]:
    """Inserts a user into the database.

    Args:
      username: The username of the user.
      email: The email of the user.
      first_name: The first name of the user.
      last_name: The last name of the user.
      password: The password (not hashed) of the user.
      date_joined: The datetime the user joined the system.
      is_superuser: A flag that indicates if this user is super user.
      is_staff: A flag that indicated if this user can is staff.
      is_active: A flag that indicates if this user is active.
      last_login: The datetime the user last logged in.

    Returns:
      A UserEntity representing the created user.

    Raises:
      UsernameAlreadyExistsError: If the username already exists.
      EmailAlreadyExistsError: If the email already exists.
    """
    username = normalize_str(username)
    email = normalize_str(email)
    first_name = normalize_str(first_name)
    last_name = normalize_str(last_name)
    if date_joined is None:
        tzinfo = zoneinfo.ZoneInfo(settings["APPLICATION"]["timezone"])
        date_joined = datetime.datetime.now(tz=tzinfo)
    password_hash = make_password(password)
    return await repository.insert_user(
        username=username, email=email, first_name=first_name,
        last_name=last_name, password=password_hash, date_joined=date_joined,
        is_superuser=is_superuser, is_staff=is_staff, is_active=is_active,
        last_login=last_login)


async def get_user_by_id(user_id: UUID) -> Awaitable[Optional[UserEntity]]:
    """Returns the user with the specified user_id from the database.

    Args:
      user_id: The user_id of the searched user.

    Returns:
      A UserEntity representing the searched user, None if the user was not
      found.
    """
    return await repository.get_user_by_id(user_id)


async def update_user_by_id(
    user_id: UUID,
    username: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    password: Optional[str] = None,
    is_superuser: Optional[bool] = None,
    is_staff: Optional[bool] = None,
    is_active: Optional[bool] = None,
    date_joined: Optional[datetime.datetime] = None,
    last_login: Optional[datetime.datetime] = None,
) -> Awaitable[Optional[UserEntity]]:
    """Updates the data of the user with the specified user_id in the database.

    Args:
      username: The username of the user.
      email: The email of the user.
      first_name: The first name of the user.
      last_name: The last name of the user.
      password: The password (not hashed) of the user.
      is_superuser: A flag that indicates if this user is super user.
      is_staff: A flag that indicated if this user can is staff.
      is_active: A flag that indicates if this user is active.
      date_joined: The datetime the user joined the system.
      last_login: The datetime the user last logged in.

    Returns:
      A UserEntity representing the updated user, None if the user was not
      updated.

    Raises:
      UsernameAlreadyExistsError: If the username already exists.
      EmailAlreadyExistsError: If the email already exists.
    """
    username = normalize_str(username)
    email = normalize_str(email)
    first_name = normalize_str(first_name)
    last_name = normalize_str(last_name)
    password_hash = make_password(password)
    return await repository.update_user_by_id(
        user_id, username=username, email=email, first_name=first_name,
        last_name=last_name, password=password_hash, is_superuser=is_superuser,
        is_staff=is_staff, is_active=is_active, date_joined=date_joined,
        last_login=last_login)


async def delete_user_by_id(user_id: UUID) -> Awaitable[Optional[UserEntity]]:
    """Deletes the user with the specified user_id from the database.

    Args:
      user_id: The user_id of the user that will be deleted.

    Returns:
      A UserEntity representing the deleted user, None if the user was not
      deleted.
    """
    return await repository.delete_user_by_id(user_id)
