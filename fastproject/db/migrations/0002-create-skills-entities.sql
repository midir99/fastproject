-- Entity: skill
CREATE TABLE skill (
    PRIMARY KEY (skill_id),
    skill_id UUID DEFAULT gen_random_uuid(),
    name     VARCHAR(50) NOT NULL,
             UNIQUE(name)
);

-- Junction: uuser & skill
CREATE TABLE uuser_skill (
    PRIMARY KEY (uuser_skill_id),
    uuser_skill_id UUID DEFAULT gen_random_uuid(),
    uuser_id       UUID NOT NULL,
                   FOREIGN KEY (uuser_id) REFERENCES uuser (uuser_id) DEFERRABLE INITIALLY DEFERRED,
    skill_id       UUID NOT NULL,
                   FOREIGN KEY (skill_id) REFERENCES skill (skill_id) DEFERRABLE INITIALLY DEFERRED,
    UNIQUE(uuser_id, skill_id)
);
