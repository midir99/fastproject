"""Repository module."""

import dataclasses
import datetime
import pathlib
import uuid
from typing import Any, Optional

import aiosql
import asyncpg
import asyncpg.pool

from ... import db
from . import exceptions

_queries = aiosql.from_path(pathlib.Path(__file__).resolve().parent / "sql", "asyncpg")


@dataclasses.dataclass
class User:
    """Represents the entity user in the database."""

    user_id: uuid.UUID
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


@db.with_connection
async def insert_user(conn: asyncpg.pool.PoolAcquireContext, **kwargs: Any) -> User:
    """Inserts a user into the database.

    This function inserts the given values "as-is", so you must make the
    desired transformations to the values before using this function.

    Args:
      conn: A database connection.
      **kwargs: The fields of the user and the value they will have. Example:
        username="snowball99".

    Returns:
      A User representing the inserted user.

    Raises:
      UsernameAlreadyExistsError: If the username already exists.
      EmailAlreadyExistsError: If the email already exists.
    """
    try:
        inserted = await _queries.insert_user(conn, **kwargs)
        inserted["user_id"] = inserted.pop("uuser_id")
        return User(**inserted)
    except asyncpg.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise exceptions.UsernameAlreadyExistsError from e
        if "email" in msg:
            raise exceptions.EmailAlreadyExistsError from e
        raise e from e


@db.with_connection
async def get_user_by_id(
    conn: asyncpg.pool.PoolAcquireContext, user_id: uuid.UUID
) -> Optional[User]:
    """Returns the user with the specified user_id from the database.

    Args:
      user_id: The user_id of the searched user.
      conn: A database connection.

    Returns:
      A User representing the searched user, None if the user was not
      found.
    """
    searched = await _queries.get_user_by_id(conn, uuser_id=user_id)
    if not searched:
        return None
    searched["user_id"] = searched.pop("uuser_id")
    return User(**searched)


@db.with_connection
async def update_user_by_id(
    conn: asyncpg.pool.PoolAcquireContext, user_id: uuid.UUID, **kwargs: Any
) -> Optional[User]:
    """
    Updates the data of a user with the specified user_id in the database. Not
    provided fields won't be updated.

    Args:
      user_id: The user_id of the user that will be updated.
      conn: A database connection.
      **kwargs: The fields of the user and the value they will have. Example:
        username="snowball99".

    Returns:
      A User representing the updated user, None if the user was not
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
    update_data = db.updater_fields(fields, null_fields, **kwargs)
    try:
        updated = await _queries.update_user_by_id(
            conn, uuser_id=user_id, **update_data
        )
        if not updated:
            return None
        updated["user_id"] = updated.pop("uuser_id")
        return User(**updated)
    except asyncpg.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise exceptions.UsernameAlreadyExistsError from e
        if "email" in msg:
            raise exceptions.EmailAlreadyExistsError from e
        raise e from e


@db.with_connection
async def delete_user_by_id(
    conn: asyncpg.pool.PoolAcquireContext, user_id: uuid.UUID
) -> Optional[User]:
    """Deletes the user with the specified user_id from the database.

    Args:
      user_id: The user_id of the user that will be deleted.
      conn: A database connection.

    Returns:
      A User representing the deleted user, None if the user was not
      deleted.
    """
    deleted = await _queries.delete_user_by_id(conn, uuser_id=user_id)
    if not deleted:
        return None
    deleted["user_id"] = deleted.pop("uuser_id")
    return User(**deleted)
