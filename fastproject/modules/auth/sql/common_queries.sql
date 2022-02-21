-- name: get-all-users
-- Get all users
SELECT *
  FROM uuser;


-- name: insert-user<!
-- Inserts a single user
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
) RETURNING
    uuser_id,
    username,
    email,
    first_name,
    last_name,
    password,
    is_superuser,
    is_staff,
    is_active,
    date_joined,
    last_login;


-- name: get-user-by-username^
-- Get 1 user with the given username field
SELECT *
  FROM uuser
 WHERE username = :username;


-- name: get-user-by-id^
-- Get a single user with the given user_id
SELECT *
  FROM uuser
 WHERE uuser_id = :uuser_id;


-- name: get-all-users-with-skill
-- Get all users that have the given skill
SELECT uuser.first_name, skill.name
  FROM uuser
       JOIN uuser_skill
       ON uuser_skill.uuser_id = uuser.uuser_id

       LEFT JOIN skill
       ON uuser_skill.skill_id = skill.skill_id
 WHERE skill.name IN ('Perseverance', 'Knowledge management', 'Giving clear feedback');
