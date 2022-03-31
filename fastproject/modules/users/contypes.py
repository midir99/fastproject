"""User specific constrained types."""

import pydantic

Username = pydantic.constr(
    strip_whitespace=True, min_length=4, max_length=15, regex="[a-zA-Z0-9_]"
)
Password = pydantic.constr(
    strip_whitespace=True,
    min_length=9,
    max_length=128,
)
FirstName = pydantic.constr(strip_whitespace=True, max_length=150, regex="[a-zA-Z]")
LastName = pydantic.constr(
    strip_whitespace=True,
    max_length=150,
    regex="[a-zA-Z]",
)
