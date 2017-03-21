"""
A module to connect to MariaDB.
"""
import MySQLdb, os, sys, re, time
import collections
from warnings import filterwarnings

try:
	from aiobj.util import logger
except ImportError:
	pass

try:
	import tabulate
except ImportError:
	pass

try:
	import pandas as pd, pandas
except ImportError:
	pass

try:
	import sqlalchemy
except ImportError:
	pass

filterwarnings('ignore', category = MySQLdb.Warning)

class SQL:
	""" Class to manage SQL connections. """
	DEFAULT_DB = 'ops'
	OPS = 'ops'
	TGOLAP = 'tgolap'
	TGCONF = 'tgconf'

	def __init__(
			self, db = DEFAULT_DB, host = None, port = None, user = None,
			passwd = None, autocommit = False, printsql = False,
			use_unicode = True, charset = 'utf8', managed = True,
			alchemy = False, connect = True, autoretry = True, retryperiod = 240):
		self.db = db
		self.host = host or os.getenv('SQL_HOST', '127.0.0.1')
		self.user = user or os.getenv('SQL_APP_USER', 'notset')
		self.passwd = passwd or os.getenv('SQL_APP_PASS', 'notset')
		self.port = port or int(os.getenv('SQL_PORT', 3306))
		self.printsql = printsql
		self.autocommit = autocommit
		self.autoretry = autoretry
		self.retryperiod = retryperiod
		self.use_unicode = use_unicode
		self.charset = charset
		self.managed = managed
		self.alchemy = alchemy
		self.alchemy_engine = None
		if not connect:
			return
		if not alchemy:
			self.conn = MySQLdb.connect(
				host=self.host, port=self.port, user=self.user,
				passwd=self.passwd, db=self.db, use_unicode = self.use_unicode,
				charset = self.charset)
			self.conn.autocommit(self.autocommit)
			self.conn.set_character_set(self.charset)
			sqlsetup = "SET NAMES utf8; "
			sqlsetup += "SET CHARACTER SET %s; " % self.charset
			sqlsetup += "SET character_set_connection = %s; " % self.charset
			sqlsetup += "SET collation_connection = 'utf8_bin'; "
			self.execute(sqlsetup)
		else:
			constr_base = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s'
			constr = constr_base % (self.user, self.passwd, self.host, self.port, self.db, self.charset)
			ae = sqlalchemy.create_engine(constr, encoding = self.charset)
			self.alchemy_engine = ae


	def __del__(self):
		try:
			if self.managed:
				self.conn.close()
		except:
			pass

	def getconn(self):
		return self.conn

	def close(self):
		self.conn.close()

	def commit(self):
		try:
			self.conn.commit()
		except:
			self.conn.rollback()
			raise
	
	def commitclose(self):
		try:
			self.conn.commit()
		except:
			self.conn.rollback()
			raise
		finally:
			self.close()

	def rollback(self):
		self.conn.rollback()

	def reconnect(self):
		try:
			self.conn.close()
		except:
			pass
		self.conn = MySQLdb.connect(
			host=self.host, port=self.port, user=self.user, passwd=self.passwd,
			db=self.db, use_unicode=self.use_unicode, charset=self.charset)
		self.conn.autocommit(self.autocommit)
		self.execute("SET collation_connection = 'utf8_bin';")

	def ping(self):
		self.conn.ping()

	def __printsql__(self, sqltxt, args = None):
		if self.printsql:
			msg = 'Executing SQL:\n%s' % sqltxt
			if not args is None:
				msg += '\n args = ' + str(args)
			logger.info(msg)

	def insert_id(self, sqltxt, args = None):
		"""
		A method to execute a sql insert statement returning the inserted id.
		"""
		self.__printsql__(sqltxt, args)
		curs = self.conn.cursor()
		curs.execute(sqltxt, args)
		insertid = self.conn.insert_id()
		curs.close()
		return insertid

	def execute(self, sqltxt, args = None):
		"""
		A method to execute a sql statement with no return result set.
		"""
		self.__printsql__(sqltxt, args)
		started = time.time()
		complete = False
		ex0 = Exception('SQL.execute exception')
		while (not complete) and time.time() - started < self.retryperiod:
			try:
				curs = self.conn.cursor()
				curs.execute(sqltxt, args)
				lastrowid = curs.lastrowid
				curs.close()
				complete = True
			except Exception as ex:
				ex0 = ex
				print(ex)
				time.sleep(10)
		if not complete:
			if ex0:
				raise ex0
			else:
				raise TimeoutError('Max query time exceeded. SQL execution was not completed.')
		return lastrowid

	def executemany(self, sqltxt, args = None):
		"""
		A method to execute a sql statement with a parameter array.
		Use this for fast multi-row inserts.
		"""
		self.__printsql__(sqltxt, args)
		started = time.time()
		complete = False
		ex0 = Exception('SQL.executemany exception')
		while (not complete) and time.time() - started < self.retryperiod:
			try:
				curs = self.conn.cursor()
				curs.executemany(sqltxt, args)
				lastrowid = curs.lastrowid
				curs.close()
				complete = True
			except Exception as ex:
				ex0 = ex
				print(ex)
				time.sleep(10)
		if not complete:
			if ex0:
				raise ex0
			else:
				raise TimeoutError('Max query time exceeded. SQL execution was not completed.')
		return lastrowid

	def callproc(self, sqltxt, args = ()):
		"""
		A method to execute a sql procedure 
		"""
		self.__printsql__(sqltxt, args)
		curs = self.conn.cursor()
		curs.callproc(sqltxt, args)
		curs.close()

	def executeall(self, sqltxtlist):
		"""
		A method to execute a list of sql statements with no return result sets.
		"""
		curs = self.conn.cursor()
		for sqltxt in sqltxtlist:
			self.__printsql__(sqltxt)
			curs.execute(sqltxt)
		curs.close()

	def execute_ddl(self, sqltxt, args = None):
		"""
		A method to silently execute ddl.
		"""
		try:
			self.execute(sqltxt, args)
		except (MySQLdb.Error, MySQLdb.Warning) as err:
			logger.debug('Expected DDL Warning:\n' + str(sys.exc_info()))
			logger.debug(err.args[0])
			logger.debug(type(err))
			logger.debug(err)
		except Exception as ex:
			logger.exception(ex, ("Unexpected DDL Warning:\n\n %s\n\n" % sqltxt))

	def executeall_ddl(self, sqltxtlist):
		"""
		A method to silently execute a list of ddl statements.
		"""
		try:
			self.executeall(sqltxtlist)
		except (MySQLdb.Error, MySQLdb.Warning) as err:
			logger.debug('Expected DDL Warning:\n' + str(sys.exc_info()))
			logger.debug(err.args[0])
			logger.debug(type(err))
			logger.debug(err)
		except Exception as ex:
			logger.exception(ex, ("Unexpected DDL Warning:\n" + str(sqltxtlist)))

	def execute_batches(self, sqltxt, iter_params):
		"""
		A method to execute sql over an iteratable parameter source.
		Features:
		Includes tuple wrapping of list elements.
		"""
		if type(iter_params) == list:
				elem0 = iter_params[0]
				if not hasattr(elem0, '__len__'):
					iter_params = list(map(lambda x: (x,), iter_params))
		for params in iter_params:
			self.execute(sqltxt, params)

	def report(self, sqltxt, args = None):
		"""
		A function to return a MySQLdb result set as a formatted string table.
		"""
		self.__printsql__(sqltxt)
		rs = self.fetchall(sqltxt, args, header = True)
		return tabulate.tabulate(rs, headers = 'firstrow')

	def pprint(self, sqltxt, args = None):
		"""
		A function to print sql and return a MySQLdb result set.
		"""
		self.__printsql__(sqltxt)
		rs = self.fetchall(sqltxt, args, header = True)
		print(tabulate.tabulate(rs, headers = 'firstrow'))

	@staticmethod
	def tuples2lists(tx):
		"""Convert a tuple of tuples to a list of lists."""
		return list(map(SQL.tuples2lists, tx)) if isinstance(tx, (list, tuple)) else tx

	@staticmethod
	def nullify(obj):
		"""Convert empty strings to NULL/None."""
		if obj != None and type(obj) != str and isinstance(obj, collections.Iterable):
			return list(map(SQL.nullify, obj))
		if obj != None and type(obj) == str and re.match(r'^\s*$', obj):
			return None
		return obj

	def pandas_dataframe(self, sqltxt, args = None):
		"""
		A function to return a MySQLdb result set in a Pandas DataFrame.
		"""
		self.__printsql__(sqltxt)
		rs = self.fetchall(sqltxt, args, header = True)
		rs = SQL.tuples2lists(rs)
		if len(rs) == 0:
			return pandas.DataFrame(columns = rs[0])
		return pandas.DataFrame(rs[1:], columns = rs[0])

	def _jsonify(self, table_rs):
		"""A function to take tabular result set data with header and jsonify it."""
		jout = []
		header = table_rs[0]
		for row_num in range(1, len(table_rs)):
			jout.append({})
			for col_num in range(len(header)):
				val = table_rs[row_num][col_num]
				try:
					float(val)
				except:
					val = str(val)
				jout[row_num-1][header[col_num]] = val
		return jout

	def fetchall(self, sqltxt, args = None, header = False, jsonify = False):
		"""
		A function to execute sql and return a MySQLdb result set.
		"""
		self.__printsql__(sqltxt, args)
		curs = self.conn.cursor()
		curs.execute(sqltxt, args)
		rs = curs.fetchall()
		curs.close()
		if header or jsonify:
			headr = [col_desc[0] for col_desc in curs.description]
			rs = (tuple(headr),) + rs
			if jsonify:
				rs = self._jsonify(rs)
		return rs

	def fetchone(self, sqltxt, args = None, header = False, jsonify = False):
		"""
		Gets one row from a sql statement.
		"""
		self.__printsql__(sqltxt, args)
		curs = self.conn.cursor()
		curs.execute(sqltxt, args)
		rs = curs.fetchone()
		curs.close()
		if header or jsonify:
			headr = [col_desc[0] for col_desc in curs.description]
			rs = (tuple(headr),) + rs
			if jsonify:
				rs = self._jsonify(rs)
		return rs

	_singletons = {}
	@staticmethod
	def singleton(key = None, db = DEFAULT_DB):
		""" Generate/get a singleton sql connection instance. """
		if key == None:
			conn_key = db
		else:
			conn_key = key
		conn = None
		if not conn_key in SQL._singletons:
			SQL._singletons[conn_key] = SQL(db)
		conn = SQL._singletons[conn_key]
		try:
			conn.ping()
		except:
			conn.reconnect()
		return conn


	@staticmethod
	def generate_insert(table_name, columns, upsert_columns = None):
		""" Generate sql insert/upsert statement. """
		sqltxt = 'INSERT INTO ' + table_name + '\n (' + ','.join(columns) + ')'
		sqltxt += '\nVALUES (' + ('%s,'*len(columns))[:-1] + ')'
		if upsert_columns:
			sqltxt += '\nON DUPLICATE KEY UPDATE\n'
			sqltxt += (''.join([colname + '=VALUES(' + colname + '),' for colname in upsert_columns]))[:-1]
		return sqltxt+';\n'


	@staticmethod
	def generate_select(table_name, columns):
		""" Generate sql select statement. """
		sqltxt = 'SELECT ' + ','.join(columns)
		sqltxt += '\nFROM %s;\n' % table_name
		return sqltxt


	def copy_table(self, src_table, src_columns, dst_table, dst_columns = None, dst_upsertable = None):
		""" Copy a small sql table. """
		if not dst_columns:
			dst_columns = src_columns
		src_data = self.fetchall(SQL.generate_select(src_table, src_columns))
		lastrowid = self.executemany(SQL.generate_insert(dst_table, dst_columns, dst_upsertable), src_data)
		self.commit()
		return lastrowid


