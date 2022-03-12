from pathlib import Path
from typing import Any, Optional
from uuid import UUID

import aiosql
import asyncpg
from asyncpg.pool import PoolAcquireContext

from ...db import updater_fields, with_connection
from .exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from .models import UserEntity

_queries = aiosql.from_path(Path(__file__).resolve().parent / "sql", "asyncpg")


@with_connection
async def insert_user(
        conn: PoolAcquireContext, **kwargs: Any) -> Optional[UserEntity]:
    """Inserts a user into the database.

    This function inserts the given values "as-is", so you must make the
    desired transformations to the values before using this function.

    Args:
      conn: A database connection.
      **kwargs: The fields of the user and the value they will have. Example:
        username="snowball99".

    Returns:
      A UserEntity representing the inserted user.

    Raises:
      UserUsernameAlreadyExistsError: If the username already exists.
      UserEmailAlreadyExistsError: If the email already exists.
    """
    try:
        inserted = await _queries.insert_user(conn, **kwargs)
        return UserEntity(user_id=inserted["uuser_id"], **inserted)
    except asyncpg.exceptions.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise UsernameAlreadyExistsError from e
        if "email" in msg:
            raise EmailAlreadyExistsError from e
        raise e from e


@with_connection
async def get_user_by_id(
        conn: PoolAcquireContext, user_id: UUID) -> Optional[UserEntity]:
    """Returns a user from the database with the given user_id.

    Args:
      conn: A database connection.
      user_id: The user_id of the searched user.

    Returns:
      A UserEntity representing the searched user, None if the user was not
      found.
    """
    searched = await _queries.get_user_by_id(conn, uuser_id=user_id)
    if searched:
        return UserEntity(user_id=searched["uuser_id"], **searched)
    return None


@with_connection
async def update_user_by_id(
    conn: PoolAcquireContext, user_id: UUID, **kwargs: Any
) -> Optional[UserEntity]:
    """
    Updates the data of an existing user in the database with the given user_id
    and returns it. Not provided fields won't be updated.

    Args:
      conn: A database connection.
      user_id: The user_id of the user that will be updated.
      **kwargs: The fields of the user and the value they will have. Example:
        username="snowball99".

    Returns:
      A UserEntity representing the updated user, None if the user was not
      updated.

    Raises:
      UserUsernameAlreadyExistsError: If the username already exists.
      UserEmailAlreadyExistsError: If the email already exists.
    """
    fields = ("username", "email", "first_name", "last_name", "password",
              "is_superuser", "is_staff", "is_active", "date_joined",)
    null_fields = ("last_login",)
    update_data = updater_fields(fields, null_fields)
    try:
        updated = await _queries.update_user_by_id(
            conn, uuser_id=user_id, **update_data)
        if not updated:
            return None
        return UserEntity(user_id=updated["uuser_id"], **updated)
    except asyncpg.exceptions.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise UsernameAlreadyExistsError from e
        if "email" in msg:
            raise EmailAlreadyExistsError from e
        raise e from e


@with_connection
async def delete_user_by_id(
        conn: PoolAcquireContext, user_id: UUID) -> Optional[UserEntity]:
    """Deletes a user from the database with the given user_id.

    Args:
      conn: A database connection.
      user_id: The user_id of the user that will be deleted.

    Returns:
      A UserEntity representing the deleted user, None if the user was not
      deleted.
    """
    deleted = await _queries.delete_user_by_id(conn, uuser_id=user_id)
    if deleted:
        return UserEntity(user_id=deleted["user_id"], **deleted)
    return None
