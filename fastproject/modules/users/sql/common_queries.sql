-- name: insert-user<!
-- Insert a user
INSERT INTO uuser (
    username,
    email,
    first_name,
    last_name,
    password,
    is_superuser,
    is_staff,
    is_active,
    date_joined,
    last_login
) VALUES (
    :username,
    :email,
    :first_name,
    :last_name,
    :password,
    :is_superuser,
    :is_staff,
    :is_active,
    :date_joined,
    :last_login
) RETURNING uuser.*;


-- name: get-all-users
-- Get all users
SELECT *
  FROM uuser;


-- name: get-user-by-username^
-- Get a user with the given username field
SELECT *
  FROM uuser
 WHERE username = :username;


-- name: get-user-by-id^
-- Get a user with the given uuser_id
SELECT *
  FROM uuser
 WHERE uuser_id = :uuser_id;


-- name: update-user-by-id^
-- Update a user with the given uuser_id. The "coalesced" fields that were not
-- provided will be updated with their current value (their value won't change).
   UPDATE uuser
      SET username = COALESCE(:username, username),
          email = COALESCE(:email, email),
          first_name = COALESCE(:first_name, first_name),
          last_name = COALESCE(:last_name, last_name),
          password = COALESCE(:password, password),
          is_superuser = COALESCE(:is_superuser, is_superuser),
          is_staff = COALESCE(:is_staff, is_staff),
          is_active = COALESCE(:is_active, is_active),
          date_joined = COALESCE(:date_joined, date_joined),
          last_login = :last_login
    WHERE uuser_id = :uuser_id
RETURNING uuser.*;


-- name: delete-user-by-id^
-- Delete a user with the given uuser_id
DELETE FROM uuser
      WHERE uuser_id = :uuser_id
  RETURNING uuser.*;
