from pydantic import constr


class SkillConTypes:
    Name = constr(min_length=1, max_length=50, strip_whitespace=True)
