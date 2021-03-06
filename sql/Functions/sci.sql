DELIMITER $$

DROP FUNCTION IF EXISTS sci$$

CREATE DEFINER=`root`@`localhost` FUNCTION sci (num DOUBLE, digits INT)
RETURNS TEXT DETERMINISTIC

BEGIN

SET @exp = IF(num=0, 0, FLOOR(LOG10(ABS(num))));
RETURN CONCAT(FORMAT(num * POWER(10, -@exp), digits), 'e', @exp);

END$$

DELIMITER ;

