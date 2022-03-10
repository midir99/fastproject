import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID

import aiosql
import asyncpg
from asyncpg.pool import PoolAcquireContext

from ...db import with_connection
from .models import PublicUser
from .exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError

_queries = aiosql.from_path(Path(__file__).resolve().parent / "sql", "asyncpg")


@with_connection
async def insert_user(
    conn: PoolAcquireContext,
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    date_joined: datetime.datetime,
    is_superuser=False,
    is_staff=False,
    is_active=True,
    last_login: Optional[datetime.datetime] = None
) -> Optional[PublicUser]:
    """Inserts a user into the database.

    This function inserts the given values "as-is", so you must make the
    desired transformations to the values before using this function.

    Args:
      conn: A database connection.
      username: The value for the "username" field of the user table.
      email: The value for the "email" field of the user table.
      first_name: The value for the "first_name" field of the user table.
      last_name: The value for the "last_name" field of the user table.
      password: The value for the "password" field of the user table.
      date_joined: The value for the "date_joined" field of the user table.
      is_superuser: The value for the "is_superuser" field of the user table.
      is_staff: The value for the "is_staff" field of the user table.
      last_login: The value for the "last_login" field of the user table.

    Returns:
      A PublicUser representing the inserted user.

    Raises:
      UserUsernameAlreadyExistsError: If the username already exists.
      UserEmailAlreadyExistsError: If the email already exists.
    """
    try:
        inserted = await _queries.insert_user(
            conn, username=username, email=email, first_name=first_name,
            last_name=last_name, password=password, is_superuser=is_superuser,
            is_staff=is_staff, is_active=is_active, date_joined=date_joined,
            last_login=last_login)
        return PublicUser(user_id=inserted["uuser_id"], **inserted)
    except asyncpg.exceptions.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise UsernameAlreadyExistsError from e
        if "email" in msg:
            raise EmailAlreadyExistsError from e
        raise e from e


@with_connection
async def get_user_by_id(
        conn: PoolAcquireContext, user_id: UUID) -> Optional[PublicUser]:
    """Returns a user from the database with the given user_id.

    Args:
      conn: A database connection.
      user_id: The user_id of the searched user.

    Returns:
      A PublicUser representing the searched user, None if the user was not
      found.
    """
    searched = await _queries.get_user_by_id(conn, uuser_id=user_id)
    if searched:
        return PublicUser(user_id=searched["uuser_id"], **searched)
    return None


@with_connection
async def update_user_by_id(
    conn: PoolAcquireContext,
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
) -> Optional[PublicUser]:
    """
    Updates the data of an existing user in the database with the given user_id
    and returns it.

    Not provided fields won't be updated

    Args:
      conn: A database connection.
      user_id: The user_id of the user that will be updated.
      username: The value for the "username" field of the user table.
      email: The value for the "email" field of the user table.
      first_name: The value for the "first_name" field of the user table.
      last_name: The value for the "last_name" field of the user table.
      password: The value for the "password" field of the user table.
      is_superuser: The value for the "is_superuser" field of the user table.
      is_staff: The value for the "is_staff" field of the user table.
      is_active: The value for the "is_active" field of the user table.
      date_joined: The value for the "date_joined" field of the user table.
      last_login: The value for the "last_login" field of the user table.

    Returns:
      A PublicUser representing the updated user, None if the user was not
      updated.

    Raises:
      UserUsernameAlreadyExistsError: If the username already exists.
      UserEmailAlreadyExistsError: If the email already exists.
    """
    # TODO: test if exceptions can really happen.
    try:
        updated = await _queries.update_user_by_id(
            conn, uuser_id=user_id, username=username, email=email,
            first_name=first_name, last_name=last_name, password=password,
            is_superuser=is_superuser, is_staff=is_staff, is_active=is_active,
            date_joined=date_joined, last_login=last_login)
        if updated:
            return PublicUser(user_id=updated["user_id"], **updated)
        return None
    except asyncpg.exceptions.UniqueViolationError as e:
        msg = str(e)
        if "username" in msg:
            raise UsernameAlreadyExistsError from e
        if "email" in msg:
            raise EmailAlreadyExistsError from e
        raise e from e


@with_connection
async def delete_user_by_id(
        conn: PoolAcquireContext, user_id: UUID) -> Optional[PublicUser]:
    """Deletes a user from the database with the given user_id.

    Args:
      conn: A database connection.
      user_id: The user_id of the user that will be deleted.

    Returns:
      A PublicUser representing the deleted user, None if the user was not
      deleted.
    """
    deleted = await _queries.delete_user_by_id(conn, uuser_id=user_id)
    if deleted:
        return PublicUser(user_id=deleted["user_id"], **deleted)
    return None
