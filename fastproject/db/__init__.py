from asyncio import shield
import functools

import asyncpg

from ..config import config


class ConnectionPool:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')

    @classmethod
    async def instance(cls):
        if cls._instance is None:
            cls._instance = await shield(asyncpg.create_pool(
                host=config["DATABASE"]["host"],
                port=config["DATABASE"]["port"],
                database=config["DATABASE"]["dbname"],
                user=config["DATABASE"]["user"],
                password=config["DATABASE"]["password"],
                min_size=1,
                max_size=5,
            ))
        return cls._instance


def with_connection(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        conn_pool = await ConnectionPool.instance()
        async with conn_pool.acquire() as conn:
            rv = await func(conn, *args, **kwargs)
        return rv
    return wrapper
