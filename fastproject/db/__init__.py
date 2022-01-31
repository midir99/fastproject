from asyncio import shield
import functools

import asyncpg

from ..config import settings


class ConnectionPool:
    _conn_pool = None

    def __init__(self) -> None:
        raise RuntimeError('Call ConnectionPool.get_conn_pool() instead')

    @classmethod
    async def get_conn_pool(cls):
        if cls._conn_pool is None:
            cls._conn_pool = await shield(asyncpg.create_pool(
                host=settings["DATABASE"]["host"],
                port=settings["DATABASE"]["port"],
                database=settings["DATABASE"]["dbname"],
                user=settings["DATABASE"]["user"],
                password=settings["DATABASE"]["password"],
                min_size=1,
                max_size=5,
            ))
        return cls._conn_pool


def with_connection(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        conn_pool = await ConnectionPool.get_conn_pool()
        async with conn_pool.acquire() as conn:
            rv = await func(conn, *args, **kwargs)
        return rv
    return wrapper
