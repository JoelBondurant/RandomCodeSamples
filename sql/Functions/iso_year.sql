DELIMITER $$

DROP FUNCTION IF EXISTS iso_year$$

CREATE DEFINER=`root`@`localhost` FUNCTION iso_year (adate DATE)
RETURNS INT DETERMINISTIC

BEGIN

RETURN date_format(adate, "%x");

END$$

DELIMITER ;

