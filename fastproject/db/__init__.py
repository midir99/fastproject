"""Utils to get database connections based on the application settings."""
import functools
from typing import Callable, TypeVar, Optional
from collections.abc import Awaitable
from configparser import ConfigParser

# TODO: Remove them when switching to Python 3.10
from typing_extensions import ParamSpec, Concatenate
from asyncpg import Pool, create_pool
from asyncpg.pool import PoolAcquireContext

from ..config import settings


P = ParamSpec("P")
T = TypeVar("T")  # pylint: disable=invalid-name

_CONN_POOL: Optional[Pool] = None


async def init_connection_pool(app_settings: ConfigParser = settings) -> None:
    """Initializates the connection pool with the given settings."""
    global _CONN_POOL  # pylint: disable=global-statement
    _CONN_POOL = await create_pool(
        host=app_settings["DATABASE"]["host"],
        port=app_settings["DATABASE"]["port"],
        database=app_settings["DATABASE"]["dbname"],
        user=app_settings["DATABASE"]["user"],
        password=app_settings["DATABASE"]["password"],
        min_size=1,
        max_size=5,
    )


async def get_connection_pool() -> Pool:
    """Returns the connection pool."""
    if _CONN_POOL is None:
        await init_connection_pool()
    return _CONN_POOL


def with_connection(
    func: Callable[Concatenate[PoolAcquireContext, P], Awaitable[T]]
) -> Callable[P, Awaitable[T]]:
    """
    Injects a database connection into an async function as the first
    parameter.
    """
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Awaitable[T]:
        conn_pool = await get_connection_pool()
        async with conn_pool.acquire() as conn:
            return_value = await func(conn, *args, **kwargs)
        return return_value
    return wrapper
