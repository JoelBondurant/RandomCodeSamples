DELIMITER $$

DROP FUNCTION IF EXISTS levenshtein256$$

CREATE DEFINER=`root`@`localhost` FUNCTION `levenshtein256`(str1 VARCHAR(255), str2 VARCHAR(255)) RETURNS int(11)
    DETERMINISTIC
BEGIN
	DECLARE str1Length, str2Length, i, j, c, c_temp, cost INT;
	DECLARE str1_char CHAR;
	DECLARE cv0, cv1 VARBINARY(256);
	SET str1Length = CHAR_LENGTH(str1), str2Length = CHAR_LENGTH(str2), cv1 = 0x00, j = 1, i = 1, c = 0;
	IF str1 = str2 THEN
		RETURN 0;
	ELSEIF str1Length = 0 THEN
		RETURN str2Length;
	ELSEIF str2Length = 0 THEN
		RETURN str1Length;
	ELSE
		WHILE j <= str2Length DO
			SET cv1 = CONCAT(cv1, UNHEX(HEX(j))), j = j + 1;
		END WHILE;
		WHILE i <= str1Length DO
			SET str1_char = SUBSTRING(str1, i, 1), c = i, cv0 = UNHEX(HEX(i)), j = 1;
			WHILE j <= str2Length DO
				SET c = c + 1;
				IF str1_char = SUBSTRING(str2, j, 1) THEN
					SET cost = 0;
				ELSE
					SET cost = 1;
				END IF;
				SET c_temp = CONV(HEX(SUBSTRING(cv1, j, 1)), 16, 10) + cost;
				IF c > c_temp THEN
					SET c = c_temp;
				END IF;
				SET c_temp = CONV(HEX(SUBSTRING(cv1, j+1, 1)), 16, 10) + 1;
				IF c > c_temp THEN
					SET c = c_temp;
				END IF;
				SET cv0 = CONCAT(cv0, UNHEX(HEX(c))), j = j + 1;
			END WHILE;
			SET cv1 = cv0, i = i + 1;
		END WHILE;
	END IF;
	RETURN c;
END$$

DELIMITER ;
