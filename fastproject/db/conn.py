"""Utilities to get database connections based on the application settings."""

import functools
from collections.abc import Awaitable
from typing import Callable, Optional, TypeVar

import asyncpg.pool
# TODO: Remove them when switching to Python 3.10
from typing_extensions import Concatenate, ParamSpec

from .. import config

P = ParamSpec("P")
T = TypeVar("T")

_conn_pool: Optional[asyncpg.pool.Pool] = None


async def init_connection_pool(
    host: Optional[str] = None,
    port: Optional[int] = None,
    dbname: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    min_connections=10,
    max_connections=10,
    use_settings=False,
) -> None:
    """Initializates the database connection pool.

    If use_settings is True, the connection parameters are taken from the
    configuration file ".env".
    """
    global _conn_pool
    if use_settings:
        host = config.settings["DATABASE"]["host"]
        port = int(config.settings["DATABASE"]["port"])
        dbname = config.settings["DATABASE"]["dbname"]
        user = config.settings["DATABASE"]["user"]
        password = config.settings["DATABASE"]["password"]
        min_connections = int(config.settings["DATABASE"]["min_connections"])
        max_connections = int(config.settings["DATABASE"]["max_connections"])
    else:
        params = (host, port, dbname, user, password, min_connections, max_connections)
        if None in params:
            raise ValueError(
                "If use_settings is False, you must specify "
                "host, port, dbname and password."
            )
    _conn_pool = await asyncpg.pool.create_pool(
        host=host,
        port=port,
        database=dbname,
        user=user,
        password=password,
        min_size=min_connections,
        max_size=max_connections,
    )


async def get_connection_pool() -> asyncpg.pool.Pool:
    """Returns the database connection pool."""
    if _conn_pool is None:
        await init_connection_pool(use_settings=True)
    return _conn_pool


def with_connection(
    func: Callable[Concatenate[asyncpg.pool.PoolAcquireContext, P], Awaitable[T]]
) -> Callable[P, Awaitable[T]]:
    """
    Injects a database connection into an async function as the first
    parameter.

    Args:
      **conn (asyncpg.pool.PoolAcquireContext): A database connection, if None,
      a new connection is opened and closed. If the connection is provided, the
      responsibility of closing it is leveraged to the user of the function.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        conn = kwargs.pop("conn", None)
        if conn is not None:
            return await func(conn, *args, **kwargs)
        conn_pool = await get_connection_pool()
        async with conn_pool.acquire() as conn:
            return await func(conn, *args, **kwargs)

    return wrapper
