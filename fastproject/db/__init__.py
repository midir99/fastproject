"""Utils to get database connections based on the application settings."""
import functools
from collections.abc import Awaitable
from typing import Callable, Optional, TypeVar

from asyncpg import Pool, create_pool
from asyncpg.pool import PoolAcquireContext
# TODO: Remove them when switching to Python 3.10
from typing_extensions import Concatenate, ParamSpec

from ..config import settings

P = ParamSpec("P")
T = TypeVar("T")

_CONN_POOL: Optional[Pool] = None


async def init_connection_pool(
    host: Optional[str] = None,
    port: Optional[int] = None,
    dbname: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    min_connections=10,
    max_connections=10,
    use_settings=False
) -> None:
    """Initializates the database connection pool.

    If use_settings is True, the connection parameters are taken from the
    configuration file ".env".
    """
    global _CONN_POOL  # pylint: disable=global-statement
    if use_settings:
        host = settings["DATABASE"]["host"]
        port = int(settings["DATABASE"]["port"])
        dbname = settings["DATABASE"]["dbname"]
        user = settings["DATABASE"]["user"]
        password = settings["DATABASE"]["password"]
        min_connections = int(settings["DATABASE"]["min_connections"])
        max_connections = int(settings["DATABASE"]["max_connections"])
    else:
        params = (host, port, dbname, user, password, min_connections,
                  max_connections)
        if None in params:
            raise ValueError("If use_settings is False, you must specify "
                             "host, port, dbname and password.")
    _CONN_POOL = await create_pool(
        host=host,
        port=port,
        database=dbname,
        user=user,
        password=password,
        min_size=min_connections,
        max_size=max_connections,
    )


async def get_connection_pool() -> Pool:
    """Returns the database connection pool."""
    if _CONN_POOL is None:
        await init_connection_pool(use_settings=True)
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
