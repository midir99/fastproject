import pytest

from fastproject.utils.text import unicode_ci_compare


@pytest.mark.parametrize(
    "str1,str2",
    [
        ("lucía", "LUCÍA"),
        ("ñandú", "ÑANDÚ"),
        ("На берегу пустынных волн", "На БЕРЕГУ пустынных волн"),
    ]
)
def test_unicode_ci_compare(str1, str2):
    assert unicode_ci_compare(str1, str2) is True
