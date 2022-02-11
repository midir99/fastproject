from pydantic import constr


Username = constr(
    strip_whitespace=True,
    min_length=4,
    max_length=15,
    regex="[a-zA-Z0-9_]"
)


Password = constr(
    strip_whitespace=True,
    min_length=9,
    max_length=128,
)
