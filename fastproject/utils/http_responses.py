"""Generic FastAPI HTTP responses."""

from .rmodels import DetailMessage


NotFoundResponse = {
    "description": "Not Found",
    "model": DetailMessage,
}

ConflictResponse = {
    "description": "Conflict Error",
    "model": DetailMessage
}
