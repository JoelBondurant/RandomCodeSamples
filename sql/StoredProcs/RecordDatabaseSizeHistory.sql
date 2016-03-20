DELIMITER $$

DROP PROCEDURE IF EXISTS RecordDatabaseSizeHistory$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `RecordDatabaseSizeHistory`()
BEGIN

INSERT INTO DatabaseSizeHistory (tStamp, `Database`, StorageEngine, DataSize, IndexSize, TotalSize)
SELECT
	NOW() AS tStamp,
	COALESCE(DB,'Total') AS `Database`,
	COALESCE(ENGINE,'Total') AS StorageEngine,
	SUM(data_length) AS DataSize,
	SUM(index_length) AS IndexSize,
	SUM(data_length+index_length) AS TotalSize
FROM
(
	SELECT table_schema AS DB, ENGINE, data_length, index_length
	FROM information_schema.tables
	WHERE table_schema NOT IN ('information_schema', 'performance_schema', 'mysql')
	AND ENGINE IS NOT NULL
) AAA GROUP BY DB, ENGINE WITH ROLLUP;

END$$

DELIMITER ;
