"""Tests for module db.utils."""

import datetime

from fastproject import db


def test_updater_fields():
    # Fields and null fields.
    fields = ("username", "email", "first_name")
    null_fields = ("last_name", "last_login")
    new_values = db.updater_fields(
        fields,
        null_fields,
        username="pontiff_sulyvahn",
        email="ps@email.com",
        first_name="Sulyvahn",
        last_login=datetime.datetime(2018, 12, 15),
    )
    assert new_values == {
        "username": "pontiff_sulyvahn",
        "email": "ps@email.com",
        "first_name": "Sulyvahn",
        "last_name": None,
        "update_last_name": False,
        "last_login": datetime.datetime(2018, 12, 15),
        "update_last_login": True,
    }
    # Fields only.
    fields = ("username", "email", "first_name", "last_name")
    new_values = db.updater_fields(
        fields=fields,
        username="pontiff_sulyvahn",
        email="ps@email.com",
        first_name="Sulyvahn",
    )
    assert new_values == {
        "username": "pontiff_sulyvahn",
        "email": "ps@email.com",
        "first_name": "Sulyvahn",
        "last_name": None,
    }
    # Null fields only
    null_fields = ("last_login", "birthday")
    new_values = db.updater_fields(
        null_fields=null_fields,
        updater_flag_preffix="upt_",
        last_login=datetime.datetime(2018, 12, 15),
        birthday=None,
    )
    assert new_values == {
        "last_login": datetime.datetime(2018, 12, 15),
        "upt_last_login": True,
        "birthday": None,
        "upt_birthday": True,
    }
