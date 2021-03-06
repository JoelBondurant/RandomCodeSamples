DELIMITER $$

DROP PROCEDURE IF EXISTS DebugLog$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `DebugLog`(IN logMsg VARCHAR(2048))
BEGIN
	SET sql_notes = 0;
	CREATE TEMPORARY TABLE IF NOT EXISTS DebugLog (msg varchar(2048)) ENGINE = MEMORY;
	SET sql_notes = 1;
	INSERT INTO DebugLog (msg) VALUES (logMsg);
END$$

DELIMITER ;
