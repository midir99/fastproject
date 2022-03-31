"""Generic FastAPI HTTP responses."""

from . import rmodels

NotFoundResponse = {
    "description": "Not Found",
    "model": rmodels.DetailMessage,
}

ConflictResponse = {"description": "Conflict Error", "model": rmodels.DetailMessage}
