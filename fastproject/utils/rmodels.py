"""Generic Pydantic models."""

import pydantic


class DetailMessage(pydantic.BaseModel):
    detail: str
