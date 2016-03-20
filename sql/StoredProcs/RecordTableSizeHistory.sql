DELIMITER $$

DROP PROCEDURE IF EXISTS RecordTableSizeHistory$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `RecordTableSizeHistory`()
BEGIN

INSERT INTO TableSizeHistory (tStamp, `Database`, `Table`, DataSize, IndexSize, TotalSize, RowCount)
SELECT
	NOW() AS tStamp,
	COALESCE(DB,'Total') AS `Database`,
	COALESCE(table_name,'Total') AS `Table`,
	SUM(COALESCE(data_length, 0)) AS DataSize,
	SUM(COALESCE(index_length, 0)) AS IndexSize,
	SUM(COALESCE(data_length + index_length, 0)) AS TotalSize,
	SUM(COALESCE(table_rows, 0)) AS RowCount
	FROM
	(
		SELECT table_schema AS DB, table_name, data_length, index_length, table_rows
		FROM information_schema.tables
		WHERE table_schema NOT IN ('information_schema', 'performance_schema', 'mysql')
		AND table_name IS NOT NULL
) AAA GROUP BY DB, table_name WITH ROLLUP;


END$$

DELIMITER ;
