DELIMITER $$

DROP FUNCTION IF EXISTS percentDifference$$

CREATE DEFINER=`root`@`localhost` FUNCTION `percentDifference`
	(arg1 DOUBLE, arg2 DOUBLE) RETURNS double DETERMINISTIC
BEGIN
	IF arg2 = 0.0 THEN
		IF arg1 = 0.0 THEN
			RETURN 0.0;
		ELSE
			RETURN NULL;
		END IF;
	END IF;
	RETURN 100.0 * ((arg2 - arg1) / arg1);
END$$

DELIMITER ;
