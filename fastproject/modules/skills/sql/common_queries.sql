-- name: insert-skill<!
-- Insert a single skill
INSERT INTO skill (name) VALUES (:name) RETURNING skill_id;


-- name: get-skill^
-- Get a single skill
SELECT * FROM skill WHERE skill_id = :skill_id;


-- name: get-all-skill
SELECT * FROM skill;
