from analyticobjects.util import logger
from analyticobjects.connectors.sql import SQL


def record():
	sql = SQL(autocommit = True)
	hrs_fresh = sql.fetchone('select min(timestampdiff(HOUR, tStamp, now())) from TableSizeHistory;')[0]
	if not hrs_fresh or hrs_fresh > 18:
		logger.info('Started recording TableSizeHistory.')
		sql.execute('CALL RecordTableSizeHistory();')
		logger.info('Finished recording TableSizeHistory.')
