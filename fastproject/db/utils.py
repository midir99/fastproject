"""Utils to be used in repository modules."""

from collections.abc import Iterable
from typing import Any, Optional


def updater_fields(
    fields: Optional[Iterable[str]] = None,
    null_fields: Optional[Iterable[str]] = None,
    updater_flag_preffix="update_",
    **kwargs: Any
) -> dict[str, Any]:
    """
    Prepares the specified fields in **kwargs to be used in an "update"
    repository function.

    This function is intended to be used inside update functions in repository
    modules, because it returns the neccesary values that SQL update queries
    need.

    Args:
      fields: This is a list containing the NON-NULLABLE fields of the entity
        that will be updated in the database.
      null_fields: This is a list containig the NULLABLE fields of the entity
        that will be updated in the database.
      updater_flag_preffix: This is a preffix added to the flags that indicate
        that a NULLABLE field must be updated or not.

    Returns:
      A dictionary containing the names and the values of the fields that will
      be updated in the database, it also includes the updater flags (used to
      indicate which NULLABLE fields will be updated). For example:

      fields = ("username", "email", "first_name")
      null_fields = ("last_login", "last_name")
      new_values = updater_fields(fields, null_fields, username="snowball99",
                                  email="snowball@example.com",
                                  last_login="1999-01-22")
      new_values' content:
      {
          "username": "snowball99",
          "email": "snowball@example.com",
          "first_name": None,
          "last_name": None,
          "update_last_name": False,
          "last_login": "1999-01-22",
          "update_last_login": True
      }

      Now imagine you send this arguments to the following SQL update query
      (the query from below is the standard way in this project to implement
      update queries):

      UPDATE student
      SET username = COALESCE(:username, username),
          email = COALESCE(:email, email),
          first_name = COALESCE(:first_name, first_name),
          last_name = CASE WHEN :update_last_name THEN :last_name ELSE last_name END,
          last_login = CASE WHEN :update_last_login THEN :last_login ELSE last_login END
      WHERE student_id = :student_id;

      The way the arguments and the SQL query are written allows you to use
      partial updates on database records.

      For those fields that are non-nullable, sending a NULL (None) for the
      update query is enough, because COALESCE will not update them if they are
      NULL. But for nullable fields an extra flag that indicates if the
      field must be updated must be provided, since NULL is a valid value for
      that field.
    """
    if fields is None:
        fields = ()
    if null_fields is None:
        null_fields = ()
    return {
        **{field: kwargs.get(field) for field in fields + null_fields},
        **{f"{updater_flag_preffix}{field}": True for field in null_fields
            if field in kwargs}
    }
