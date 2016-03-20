DELIMITER $$

DROP FUNCTION IF EXISTS iso_week$$

CREATE DEFINER=`root`@`localhost` FUNCTION iso_week (adate DATE)
RETURNS INT DETERMINISTIC

BEGIN

RETURN date_format(adate, '%v');

END$$

DELIMITER ;

