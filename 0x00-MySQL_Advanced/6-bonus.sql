-- script that creates a stored procedure AddBonus that adds a new correction for a student.

DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project INT;
    SELECT id INTO project FROM projects WHERE name = project_name;
    IF project IS NOT NULL
    THEN
        INSERT INTO corrections (user_id, project_id, score)
        VALUES (user_id, project, score);
    ELSEIF project IS NULL
    THEN
        INSERT INTO projects (name) VALUES (project_name);
        SELECT id INTO project FROM projects WHERE name = project_name;
        INSERT INTO corrections (user_id, project_id, score)
        VALUES (user_id, project, score);
    END IF;
END //
DELIMITER ;
