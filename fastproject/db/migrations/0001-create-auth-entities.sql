/*
 * FAST PROJECT INITIAL DATABASE SCHEMA
 *
 * RULES FOR EDITING:
 * 1) If the table name is a reserved keyword and you can not use another name
 *    as descriptive as the one you chose prepend the name of the table with
 *    the fisrt letter of the table name. For instance:
 *    user  -> uuser
 *    group -> ggroup
 * 2) Do not use "id" as the name of the primary key field. The primary key
 *    name must be "<table name>_id".
 * 3) When creating indexes use the following syntax:
      idx_<table name>_<column name>
 * 4) Use singular form for the table names.
 * 5) When possible, follow as much as possible the following guide:
      https://www.sqlstyle.guide
 */

-- Entity: permission
CREATE TABLE permission (
    PRIMARY KEY (permission_id),
    permission_id SERIAL       NOT NULL,
    name          VARCHAR(255) NOT NULL,
    codename      VARCHAR(100) NOT NULL
);


-- Entity: ggroup
CREATE TABLE ggroup (
    PRIMARY KEY (ggroup_id),
    ggroup_id SERIAL       NOT NULL,
    name      VARCHAR(150) NOT NULL
);
CREATE INDEX idx_ggroup_name ON ggroup USING btree (name varchar_pattern_ops);


-- Entity: uuser
CREATE TABLE uuser (
    PRIMARY KEY (uuser_id),
    uuser_id     SERIAL                   NOT NULL,
    username     VARCHAR(150)             NOT NULL,
                 UNIQUE(username),
    email        VARCHAR(254)             NOT NULL,
    first_name   VARCHAR(150)             NOT NULL,
    last_name    VARCHAR(150)             NOT NULL,
    password     VARCHAR(128)             NOT NULL,
    is_superuser BOOLEAN                  NOT NULL,
    is_staff     BOOLEAN                  NOT NULL,
    is_active    BOOLEAN                  NOT NULL,
    date_joined  TIMESTAMP WITH TIME ZONE NOT NULL,
    last_login   TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_uuser_username ON uuser USING btree (username varchar_pattern_ops);


-- Junction: ggroup & permission
CREATE TABLE ggroup_permission (
    PRIMARY KEY (ggroup_permission_id),
    ggroup_permission_id BIGSERIAL NOT NULL,
    ggroup_id            INTEGER   NOT NULL,
                         FOREIGN KEY (ggroup_id) REFERENCES ggroup (ggroup_id) DEFERRABLE INITIALLY DEFERRED,
    permission_id        INTEGER   NOT NULL,
                         FOREIGN KEY (permission_id) REFERENCES permission (permission_id) DEFERRABLE INITIALLY DEFERRED,
    UNIQUE(ggroup_id, permission_id)
);
CREATE INDEX idx_ggroup_permission_ggroup_id ON ggroup_permission USING btree (ggroup_id);
CREATE INDEX idx_ggroup_permission_permission_id ON ggroup_permission USING btree (permission_id);


-- Junction: uuser & ggroup
CREATE TABLE uuser_ggroup (
    PRIMARY KEY (uuser_ggroup_id),
    uuser_ggroup_id BIGSERIAL NOT NULL,
    uuser_id        INTEGER   NOT NULL,
                    FOREIGN KEY (uuser_id) REFERENCES uuser (uuser_id) DEFERRABLE INITIALLY DEFERRED,
    ggroup_id       INTEGER   NOT NULL,
                    FOREIGN KEY (ggroup_id) REFERENCES ggroup (ggroup_id) DEFERRABLE INITIALLY DEFERRED,
    UNIQUE(uuser_id, ggroup_id)
);
CREATE INDEX idx_uuser_ggroup_uuser_id ON uuser_ggroup USING btree (uuser_id);
CREATE INDEX idx_uuser_ggroup_ggroup_id ON uuser_ggroup USING btree (ggroup_id);


-- Junction: uuser & permission
CREATE TABLE uuser_permission (
    PRIMARY KEY (uuser_permission_id),
    uuser_permission_id BIGSERIAL NOT NULL,
    uuser_id            INTEGER   NOT NULL,
                        FOREIGN KEY (uuser_id) REFERENCES uuser (uuser_id) DEFERRABLE INITIALLY DEFERRED,
    permission_id       INTEGER   NOT NULL,
                        FOREIGN KEY (permission_id) REFERENCES permission (permission_id) DEFERRABLE INITIALLY DEFERRED,
    UNIQUE(uuser_id, permission_id)
);
CREATE INDEX idx_uuser_permission_uuser_id ON uuser_permission USING btree (uuser_id);
CREATE INDEX idx_uuser_permission_permission_id ON uuser_permission USING btree (permission_id);
