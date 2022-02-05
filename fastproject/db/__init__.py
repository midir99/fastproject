"""Utils to get database connections based on the application settings."""
import functools
from typing import Callable, TypeVar, Optional
from collections.abc import Awaitable
# TODO: Remove them when switching to Python 3.10
from typing_extensions import ParamSpec, Concatenate

from asyncpg import Pool, create_pool
from asyncpg.pool import PoolAcquireContext

from ..config import settings


P = ParamSpec('P')
T = TypeVar('T')  # pylint: disable=invalid-name


class ConnectionPool:
    """Connection pool container."""
    _conn_pool: Optional[Pool] = None

    def __init__(self):
        raise RuntimeError('Call ConnectionPool.get() instead')

    @classmethod
    async def get(cls) -> Pool:
        """Returns the connection pool.

        Creates the connection pool (in case it had not been created) and
        returns it.

        Returns:
            A connection pool instance.
        """
        if cls._conn_pool is None:
            cls._conn_pool = await create_pool(
                host=settings["DATABASE"]["host"],
                port=settings["DATABASE"]["port"],
                database=settings["DATABASE"]["dbname"],
                user=settings["DATABASE"]["user"],
                password=settings["DATABASE"]["password"],
                min_size=1,
                max_size=5,
            )
        return cls._conn_pool


def with_connection(
    func: Callable[Concatenate[PoolAcquireContext, P], Awaitable[T]]
) -> Callable[P, Awaitable[T]]:
    """Inject a database connection to an async function."""
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Awaitable[T]:
        conn_pool = await ConnectionPool.get()
        async with conn_pool.acquire() as conn:
            return_value = await func(conn, *args, **kwargs)
        return return_value
    return wrapper
