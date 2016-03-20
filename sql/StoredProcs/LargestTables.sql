DELIMITER $$

DROP PROCEDURE IF EXISTS LargestTables$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `LargestTables`(IN numLimit INT)
BEGIN

IF numLimit IS NULL THEN
	SET numLimit = 10;
END IF;

SET @numLimitInternal = numLimit;

DROP TEMPORARY TABLE IF EXISTS TmpLargestTables;
CREATE TEMPORARY TABLE IF NOT EXISTS TmpLargestTables AS (
SELECT
    database_name AS 'Database',
	table_name AS 'Table',
    LPAD(CONCAT(FORMAT(DAT/POWER(1024,pw1),2),' ',
    SUBSTR(units,pw1*2+1,2)),17,' ') AS 'DataSize',
    LPAD(CONCAT(FORMAT(NDX/POWER(1024,pw2),2),' ',
    SUBSTR(units,pw2*2+1,2)),17,' ') AS 'IndexSize',
    LPAD(CONCAT(FORMAT(TBL/POWER(1024,pw3),2),' ',
    SUBSTR(units,pw3*2+1,2)),17,' ') AS 'TotalSize',
	TBL AS Bytes
FROM
(
    SELECT database_name,table_name,DAT,NDX,TBL,
    IF(px>4,4,px) pw1,IF(py>4,4,py) pw2,IF(pz>4,4,pz) pw3
    FROM 
    (SELECT *,
        FLOOR(LOG(IF(DAT=0,1,DAT))/LOG(1024)) px,
        FLOOR(LOG(IF(NDX=0,1,NDX))/LOG(1024)) py,
        FLOOR(LOG(IF(TBL=0,1,TBL))/LOG(1024)) pz
    FROM
    (SELECT
        database_name,
		table_name,
        SUM(data_length) DAT,
        SUM(index_length) NDX,
        SUM(data_length + index_length) TBL
    FROM
    (
		SELECT table_schema AS database_name, table_name, data_length, index_length
		FROM information_schema.TABLES 
		WHERE table_schema IN ('olap', 'ops')
    ) AAA GROUP BY database_name, table_name WITH ROLLUP
) AAA) AA) A,(SELECT ' BKBMBGBTB' units) B
WHERE table_name IS NOT NULL
);

PREPARE STMT FROM 
"SELECT `Database`, `Table`, `DataSize`, `IndexSize`, `TotalSize`
FROM TmpLargestTables
ORDER BY `Bytes` DESC
LIMIT ?";

EXECUTE STMT USING @numLimitInternal;

END$$

DELIMITER ;
