import datetime
from uuid import UUID

import asyncpg
import pytest

from fastproject.modules.users import repository
from fastproject.modules.users.exceptions import (EmailAlreadyExistsError,
                                                  UsernameAlreadyExistsError)
from fastproject.modules.users.models import UserEntity


class MockPoolAcquireContext:
    pass


@pytest.mark.asyncio
async def test_insert_user(monkeypatch):
    async def mock_insert_user(conn, **kwargs):
        return {
            "uuser_id": UUID("de623351-1398-4a83-98c5-91a34f5919ee"),
            "username": kwargs["username"],
            "email": kwargs["email"],
            "first_name": kwargs["first_name"],
            "last_name": kwargs["last_name"],
            "password": kwargs["password"],
            "is_superuser": kwargs["is_superuser"],
            "is_staff": kwargs["is_staff"],
            "is_active": kwargs["is_active"],
            "date_joined": kwargs["date_joined"],
            "last_login": kwargs["last_login"],
        }

    monkeypatch.setattr(repository._queries, "insert_user", mock_insert_user)
    inserted = await repository.insert_user(
        username="soulofcinder",
        email="soc@kotff.com",
        first_name="Soul",
        last_name="Of Cinder",
        password="averysecrethash",
        is_superuser=True,
        is_staff=True,
        is_active=True,
        date_joined=datetime.datetime(1999, 1, 22),
        last_login=datetime.datetime(2002, 11, 26),
        conn=MockPoolAcquireContext(),
    )
    assert type(inserted) is UserEntity

    async def mock_insert_user(conn, **kwargs):
        raise asyncpg.UniqueViolationError("username")

    monkeypatch.setattr(repository._queries, "insert_user", mock_insert_user)
    with pytest.raises(UsernameAlreadyExistsError):
        await repository.insert_user(conn=MockPoolAcquireContext())

    async def mock_insert_user(conn, **kwargs):
        raise asyncpg.UniqueViolationError("email")

    monkeypatch.setattr(repository._queries, "insert_user", mock_insert_user)
    with pytest.raises(EmailAlreadyExistsError):
        await repository.insert_user(conn=MockPoolAcquireContext())


@pytest.mark.asyncio
async def test_get_user_by_id(monkeypatch):
    async def mock_get_user_by_id(conn, uuser_id):
        if uuser_id == UUID("de623351-1398-4a83-98c5-91a34f5919ee"):
            return {
                "uuser_id": UUID("de623351-1398-4a83-98c5-91a34f5919ee"),
                "username": "soulofcinder",
                "email": "soc@kotff.com",
                "first_name": "Soul",
                "last_name": "Of Cinder",
                "password": "averysecrethash",
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
                "date_joined": datetime.datetime(1999, 1, 22),
                "last_login": datetime.datetime(2002, 11, 26),
            }
        return None

    monkeypatch.setattr(repository._queries, "get_user_by_id", mock_get_user_by_id)
    searched = await repository.get_user_by_id(
        UUID("de623351-1398-4a83-98c5-91a34f5919ee"), conn=MockPoolAcquireContext()
    )
    assert type(searched) is UserEntity
    searched = await repository.get_user_by_id(
        UUID("de623351-1398-4a83-98c5-91a34f5919aE"), conn=MockPoolAcquireContext()
    )
    assert searched is None


@pytest.mark.asyncio
async def test_update_user_by_id(monkeypatch):
    async def mock_update_user_by_id(conn, uuser_id, **kwargs):
        if uuser_id == UUID("de623351-1398-4a83-98c5-91a34f5919ee"):
            return {
                "uuser_id": UUID("de623351-1398-4a83-98c5-91a34f5919ee"),
                "username": "soulofcinder",
                "email": "soc@kotff.com",
                "first_name": "Soul",
                "last_name": "Of Cinder",
                "password": "averysecrethash",
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
                "date_joined": datetime.datetime(1999, 1, 22),
                "last_login": datetime.datetime(2002, 11, 26),
            }
        return None

    monkeypatch.setattr(
        repository._queries, "update_user_by_id", mock_update_user_by_id
    )
    updated = await repository.update_user_by_id(
        UUID("de623351-1398-4a83-98c5-91a34f5919ee")
    )
    assert type(updated) is UserEntity
    updated = await repository.update_user_by_id(
        UUID("de623351-1398-4a83-98c5-91a34f5919AA")
    )
    assert updated is None

    async def mock_update_user_by_id(conn, uuser_id, **kwargs):
        raise asyncpg.UniqueViolationError("username")

    monkeypatch.setattr(
        repository._queries, "update_user_by_id", mock_update_user_by_id
    )
    with pytest.raises(UsernameAlreadyExistsError):
        await repository.update_user_by_id(UUID("de623351-1398-4a83-98c5-91a34f5919ee"))

    async def mock_update_user_by_id(conn, uuser_id, **kwargs):
        raise asyncpg.UniqueViolationError("email")

    monkeypatch.setattr(
        repository._queries, "update_user_by_id", mock_update_user_by_id
    )
    with pytest.raises(EmailAlreadyExistsError):
        await repository.update_user_by_id(UUID("de623351-1398-4a83-98c5-91a34f5919ee"))


@pytest.mark.asyncio
async def test_delete_user_by_id(monkeypatch):
    async def mock_delete_user_by_id(conn, uuser_id):
        if uuser_id == UUID("de623351-1398-4a83-98c5-91a34f5919ee"):
            return {
                "uuser_id": UUID("de623351-1398-4a83-98c5-91a34f5919ee"),
                "username": "soulofcinder",
                "email": "soc@kotff.com",
                "first_name": "Soul",
                "last_name": "Of Cinder",
                "password": "averysecrethash",
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
                "date_joined": datetime.datetime(1999, 1, 22),
                "last_login": datetime.datetime(2002, 11, 26),
            }
        return None

    monkeypatch.setattr(
        repository._queries, "delete_user_by_id", mock_delete_user_by_id
    )
    deleted = await repository.delete_user_by_id(
        UUID("de623351-1398-4a83-98c5-91a34f5919ee"), conn=MockPoolAcquireContext()
    )
    assert type(deleted) is UserEntity
    deleted = await repository.delete_user_by_id(
        UUID("de623351-1398-4a83-98c5-91a34f5919aE"), conn=MockPoolAcquireContext()
    )
    assert deleted is None
