from collections.abc import Awaitable
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
    conn: Optional[PoolAcquireContext] = None, **kwargs: Any
) -> Awaitable[UserEntity]:
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
      UsernameAlreadyExistsError: If the username already exists.
      EmailAlreadyExistsError: If the email already exists.
    """
    try:
        inserted = await _queries.insert_user(conn, **kwargs)
        return UserEntity(user_id=inserted["uuser_id"], **inserted)
    except asyncpg.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise UsernameAlreadyExistsError from e
        if "email" in msg:
            raise EmailAlreadyExistsError from e
        raise e from e


@with_connection
async def get_user_by_id(
    user_id: UUID,
    conn: Optional[PoolAcquireContext] = None,
) -> Awaitable[Optional[UserEntity]]:
    """Returns the user with the specified user_id from the database.

    Args:
      user_id: The user_id of the searched user.
      conn: A database connection.

    Returns:
      A UserEntity representing the searched user, None if the user was not
      found.
    """
    searched = await _queries.get_user_by_id(conn, uuser_id=user_id)
    if not searched:
        return None
    return UserEntity(user_id=searched["uuser_id"], **searched)


@with_connection
async def update_user_by_id(
    user_id: UUID, conn: Optional[PoolAcquireContext] = None, **kwargs: Any
) -> Awaitable[Optional[UserEntity]]:
    """
    Updates the data of a user with the specified user_id in the database. Not
    provided fields won't be updated.

    Args:
      user_id: The user_id of the user that will be updated.
      conn: A database connection.
      **kwargs: The fields of the user and the value they will have. Example:
        username="snowball99".

    Returns:
      A UserEntity representing the updated user, None if the user was not
      updated.

    Raises:
      UsernameAlreadyExistsError: If the username already exists.
      EmailAlreadyExistsError: If the email already exists.
    """
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "password",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    )
    null_fields = ("last_login",)
    update_data = updater_fields(fields, null_fields, **kwargs)
    try:
        updated = await _queries.update_user_by_id(
            conn, uuser_id=user_id, **update_data
        )
        if not updated:
            return None
        return UserEntity(user_id=updated["uuser_id"], **updated)
    except asyncpg.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise UsernameAlreadyExistsError from e
        if "email" in msg:
            raise EmailAlreadyExistsError from e
        raise e from e


@with_connection
async def delete_user_by_id(
    user_id: UUID, conn: Optional[PoolAcquireContext] = None
) -> Awaitable[Optional[UserEntity]]:
    """Deletes the user with the specified user_id from the database.

    Args:
      user_id: The user_id of the user that will be deleted.
      conn: A database connection.

    Returns:
      A UserEntity representing the deleted user, None if the user was not
      deleted.
    """
    deleted = await _queries.delete_user_by_id(conn, uuser_id=user_id)
    if not deleted:
        return None
    return UserEntity(user_id=deleted["user_id"], **deleted)
