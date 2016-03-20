DELIMITER $$

DROP FUNCTION IF EXISTS isFuzzyMatchString256$$

CREATE DEFINER=`root`@`localhost` FUNCTION `isFuzzyMatchString256`(str1 VARCHAR(255), str2 VARCHAR(255), threshold DOUBLE) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
	DECLARE len1, len2, repLen, levDistance INT;
	DECLARE lenRatio, repRatio, levRatio DOUBLE;
	SET len1 = LENGTH(COALESCE(str1, 0));
	SET len2 = LENGTH(COALESCE(str2, 0));
	
	IF len1 = 0 OR len2 = 0 THEN
		RETURN FALSE;
	END IF;
	
	SET lenRatio = (1.0 * ABS(len2 - len1)) / (1.0 * len1);
	IF lenRatio > threshold THEN
		RETURN FALSE;
	END IF;
	
	IF len1 > len2 THEN
		SET repRatio = (1.0 * LENGTH(REPLACE(str1, str2, ""))) / len1;
	ELSE
		SET repRatio = (1.0 * LENGTH(REPLACE(str2, str1, ""))) / len2;
	END IF;
	IF repRatio > threshold THEN
		RETURN FALSE;
	END IF;
	
	SET levDistance = levenshtein256(str1, str2);
	SET levRatio = (1.0 * levDistance) / (1.0 * len1);
	IF levRatio > threshold THEN
		RETURN FALSE;
	END IF;
	
	RETURN TRUE;
END$$

DELIMITER ;
