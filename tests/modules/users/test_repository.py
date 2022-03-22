import datetime
from uuid import UUID

import asyncpg
import pytest
from fastproject.modules.users import repository
from fastproject.modules.users.exceptions import (EmailAlreadyExistsError,
                                                  UsernameAlreadyExistsError)


@pytest.mark.asyncio
async def test_insert_user(monkeypatch):
    async def mock_queries_insert_user(conn, **kwargs):
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
            "last_login": kwargs["last_login"]
        }

    monkeypatch.setattr(repository._queries, "insert_user",
                        mock_queries_insert_user)
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
    )
    assert inserted.user_id == UUID("de623351-1398-4a83-98c5-91a34f5919ee")
    assert inserted.username == "soulofcinder"
    assert inserted.email == "soc@kotff.com"
    assert inserted.first_name == "Soul"
    assert inserted.last_name == "Of Cinder"
    assert inserted.password == "averysecrethash"
    assert inserted.is_superuser is True
    assert inserted.is_staff is True
    assert inserted.is_active is True
    assert inserted.date_joined == datetime.datetime(1999, 1, 22)
    assert inserted.last_login == datetime.datetime(2002, 11, 26)

    async def mock_queries_insert_user(conn, **kwargs):
        raise asyncpg.UniqueViolationError("username")

    monkeypatch.setattr(repository._queries, "insert_user",
                        mock_queries_insert_user)
    with pytest.raises(UsernameAlreadyExistsError):
        await repository.insert_user()

    async def mock_queries_insert_user(conn, **kwargs):
        raise asyncpg.UniqueViolationError("email")

    monkeypatch.setattr(repository._queries, "insert_user",
                        mock_queries_insert_user)
    with pytest.raises(EmailAlreadyExistsError):
        await repository.insert_user()
