import asyncpg.pool
import pytest

import fastproject.db
from fastproject.db import (get_connection_pool, init_connection_pool,
                            with_connection)


class MockPoolAcquireContext:
    async def __aenter__(self, *args, **kwargs):
        return object()

    async def __aexit__(self, *args, **kwargs):
        pass


class MockConnectionPool:
    def acquire(self):
        return MockPoolAcquireContext()


async def mock_create_pool(**kwargs):
    return MockConnectionPool()


@pytest.mark.asyncio
async def test_init_connection_pool(monkeypatch):
    monkeypatch.setattr(asyncpg.pool, "create_pool", mock_create_pool)
    # Test with use_settings.
    monkeypatch.setattr(fastproject.db.db, "_conn_pool", None)
    assert fastproject.db.db._conn_pool is None
    await init_connection_pool(use_settings=True)
    assert fastproject.db.db._conn_pool is not None
    # Test with connection parameters.
    monkeypatch.setattr(fastproject.db.db, "_conn_pool", None)
    assert fastproject.db.db._conn_pool is None
    await init_connection_pool(
        host="127.0.0.1",
        port=5432,
        dbname="fastprojectdb",
        user="fastprojectusr",
        password="itsasecret",
    )
    assert fastproject.db.db._conn_pool is not None
    # Test with wrong connection parameters.
    monkeypatch.setattr(fastproject.db.db, "_conn_pool", None)
    assert fastproject.db.db._conn_pool is None
    with pytest.raises(ValueError, match="If use_settings is False"):
        await init_connection_pool(
            host=None,
            port=5342,
            dbname="fastprojectdb",
            user="fastprojectusr",
            use_settings=False,
        )


@pytest.mark.asyncio
async def test_get_connection_pool(monkeypatch):
    monkeypatch.setattr(asyncpg.pool, "create_pool", mock_create_pool)
    monkeypatch.setattr(fastproject.db.db, "_conn_pool", None)
    conn_pool = await get_connection_pool()
    other_conn_pool = await get_connection_pool()
    assert conn_pool is other_conn_pool


@pytest.mark.asyncio
async def test_with_connection(monkeypatch):
    monkeypatch.setattr(asyncpg.pool, "create_pool", mock_create_pool)
    monkeypatch.setattr(fastproject.db.db, "_conn_pool", None)

    @with_connection
    async def repository_function(conn):
        assert conn is not None

    await repository_function(conn=MockPoolAcquireContext())
    await repository_function()
