-- creates a stored procedure AddBonus that adds a new correction for a student.
DELIMITER $$
CREATE PROCEDURE AddBonus (
    user_id INT,
    project_name VARCHAR(255),
    score INT
)
BEGIN
    INSERT INTO projects (`name`)
        SELECT project_name
        WHERE NOT EXISTS (
            SELECT `name` FROM projects
            WHERE `name`=project_name
        ) LIMIT 1
    ;
    INSERT INTO corrections (user_id, project_id, score) VALUES (
        user_id,
        (SELECT id FROM projects WHERE `name`=project_name),
        score
    );
END$$
DELIMITER ;
