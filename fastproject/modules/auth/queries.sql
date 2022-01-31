-- name: get-all-users
-- Get all users
SELECT *
  FROM uuser;


-- name: get-user-by-username^
-- Get 1 user with the given username field
SELECT *
  FROM uuser
 WHERE username = :username;


-- name: get-all-users-with-skill
-- Get all users that have the given skill
SELECT uuser.first_name, skill.name
  FROM uuser
       JOIN uuser_skill
       ON uuser_skill.uuser_id = uuser.uuser_id

       LEFT JOIN skill
       ON uuser_skill.skill_id = skill.skill_id;
 WHERE skill.name IN ('Perseverance', 'Knowledge management', 'Giving clear feedback');
