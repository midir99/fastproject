import datetime
import zoneinfo
from typing import Optional
from uuid import UUID

from ...config import settings
from ...utils.encoding import normalize_ustring
from . import repository
from .models import PublicUser
from .password_hashing import make_password


async def _create_user(
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
) -> PublicUser:
    username = normalize_ustring(username)
    email = normalize_ustring(email)
    first_name = normalize_ustring(first_name)
    last_name = normalize_ustring(last_name)
    if date_joined is None:
        tzinfo = zoneinfo.ZoneInfo(settings["APPLICATION"]["timezone"])
        date_joined = datetime.datetime.now(tz=tzinfo)
    password_hash = make_password(password)
    return await repository.insert_user(
        username, email, first_name, last_name, password_hash, date_joined,
        is_superuser, is_staff, is_active, last_login)


async def create_user(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    date_joined: Optional[datetime.datetime] = None
) -> PublicUser:
    return await _create_user(
        username, email, first_name, last_name, password, date_joined,
        is_superuser=False, is_staff=False, is_active=True)


async def create_staff_user(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    date_joined: Optional[datetime.datetime] = None
) -> PublicUser:
    return await _create_user(
        username, email, first_name, last_name, password, date_joined,
        is_superuser=False, is_staff=True, is_active=True)


async def create_super_user(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    date_joined: Optional[datetime.datetime] = None
) -> PublicUser:
    return await _create_user(
        username, email, first_name, last_name, password, date_joined,
        is_superuser=True, is_staff=True, is_active=True)


async def get_user_by_id(user_id: UUID) -> Optional[PublicUser]:
    return await repository.get_user_by_id(user_id)
