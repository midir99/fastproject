from pathlib import Path

import aiosql

from ...db import with_connection  # pylint: disable=relative-beyond-top-level


_queries = aiosql.from_path(Path(__file__).resolve().parent / "sql", "asyncpg")
