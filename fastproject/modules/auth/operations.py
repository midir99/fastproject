import zoneinfo
from datetime import datetime
from pathlib import Path

import aiosql

from ...config import settings
from ...db import with_connection  # pylint: disable=relative-beyond-top-level
from ...utils.encoding import normalize_ustring
from .dtos import CreateUserDto, PublicUserDto
from .password_hashing import make_password


_queries = aiosql.from_path(Path(__file__).resolve().parent / "sql", "asyncpg")


@with_connection
async def create_user(conn, create_user_dto: CreateUserDto) -> PublicUserDto:
    """Inserts a user into the database."""
    timezone = zoneinfo.ZoneInfo(settings["APPLICATION"]["timezone"])
    inserted = await _queries.insert_user(
        conn,
        username=normalize_ustring(create_user_dto.username),
        email=create_user_dto.email,
        first_name=normalize_ustring(create_user_dto.first_name),
        last_name=normalize_ustring(create_user_dto.last_name),
        password=make_password(create_user_dto.password),
        is_superuser=False,
        is_staff=False,
        is_active=True,
        date_joined=datetime.now(tz=timezone),
        last_login=None,
    )
    return PublicUserDto(
        user_id=inserted["uuser_id"],
        username=inserted["username"],
        email=inserted["email"],
        first_name=inserted["first_name"],
        last_name=inserted["last_name"],
        is_superuser=inserted["is_superuser"],
        is_staff=inserted["is_staff"],
        is_active=inserted["is_active"],
        date_joined=inserted["date_joined"],
        last_login=inserted["last_login"],
    )


@with_connection
async def get_user_by_id(conn, user_id: int) -> PublicUserDto:
    searched = await _queries.get_user_by_id(conn, uuser_id=user_id)
    return PublicUserDto(
        user_id=searched["uuser_id"],
        username=searched["username"],
        email=searched["email"],
        first_name=searched["first_name"],
        last_name=searched["last_name"],
        is_superuser=searched["is_superuser"],
        is_staff=searched["is_staff"],
        is_active=searched["is_active"],
        date_joined=searched["date_joined"],
        last_login=searched["last_login"],
    )
