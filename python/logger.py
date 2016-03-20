"""
A module to centralize logging settings.
"""

import os, sys, logging, datetime, inspect, traceback

LOGGING_ROOT = '/var/log/analyticobjects'

class TermColor:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class Logger:
	
	@staticmethod
	def introspect_caller():
		"""Climb up the call stack looking for what module is calling this."""
		caller = 'console'
		stack = inspect.stack()
		try:
			for frame in stack:
				module = inspect.getmodule(frame[0])
				if hasattr(module, '__name__'):
					module_name = module.__name__
					if len(module_name) > 1:
						caller = module_name
		except:
			pass
		if caller == '__main__':
			caller = os.path.basename(sys.argv[0]).replace('.py','')
		return caller

	def __init__(self, level = None):
		#print(TermColor.BOLD+'NOTICE:'+TermColor.WARNING+' analyticobjects.util.logger.init called.'+TermColor.ENDC)
		self.datestamp = datetime.datetime.today().date()
		caller = Logger.introspect_caller()
		logr = logging.getLogger(caller)
		logr.handlers = []
		level = level or logging.INFO
		logr.setLevel(level)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		filepath = os.path.join(LOGGING_ROOT, caller)
		datestr = datetime.datetime.strftime(self.datestamp, '%Y%m%d')
		filename = caller + '_' + datestr + '.log'
		try:
			os.makedirs(filepath)
		except:
			pass
		logpath = os.path.join(filepath, filename)
		filehandler = logging.FileHandler(logpath)
		filehandler.setFormatter(formatter)
		logr.addHandler(filehandler)
		consolehandler = logging.StreamHandler()
		consolehandler.setLevel(level)
		consolehandler.setFormatter(formatter)
		logr.addHandler(consolehandler)
		self.logr = logr

	def info(self, msg):
		self.logr.info(str(msg))

	def debug(self, msg):
		self.logr.debug(TermColor.OKBLUE+str(msg)+TermColor.ENDC)

	def warn(self, msg):
		self.logr.warn(TermColor.WARNING+str(msg)+TermColor.ENDC)

	def error(self, msg):
		self.logr.error(TermColor.FAIL+str(msg)+TermColor.ENDC)

	def critical(self, msg):
		self.logr.critical(TermColor.FAIL+str(msg)+TermColor.ENDC)

	def exception(self, ex, msg = 'EXCEPTION:'):
		self.logr.critical(TermColor.BOLD+TermColor.FAIL+'\n!************EXCEPTION-BEGIN***************!\n'+TermColor.ENDC)
		self.logr.critical(TermColor.WARNING+'ExceptionMessage: '+str(msg)+TermColor.ENDC)
		self.logr.critical(TermColor.WARNING+'ExceptionType: '+str(type(ex))+TermColor.ENDC)
		self.logr.critical(TermColor.WARNING+'Exception: '+str(ex)+TermColor.ENDC)
		self.logr.critical(TermColor.BOLD+TermColor.OKGREEN+'Exception Details:'+TermColor.ENDC)
		self.logr.critical(TermColor.BOLD+TermColor.OKGREEN+traceback.format_exc()+TermColor.ENDC)
		self.logr.critical(TermColor.OKBLUE+'Stack Traceback:'+TermColor.ENDC)
		for stackframe in traceback.format_stack():
			self.logr.critical(TermColor.OKBLUE+stackframe.replace('\n','')+TermColor.ENDC)
		local_vars = inspect.trace()[-1][0].f_locals
		self.logr.critical(TermColor.WARNING+'Local variables:'+TermColor.ENDC)
		for lvar in local_vars:
			self.logr.critical(TermColor.WARNING+'%s:\n\t%s' % (str(lvar), str(local_vars[lvar]))+TermColor.ENDC)
		self.logr.critical(TermColor.BOLD+TermColor.FAIL+'\n!************EXCEPTION-END*****************!\n'+TermColor.ENDC)


_logr = Logger()

def rollover():
	global _logr
	today = datetime.datetime.today().date()
	if today != _logr.datestamp:
		_logr = Logger()

def pre():
	rollover()
	env_level = os.getenv('LOGGING_LEVEL')
	if env_level:
		if env_level == 'CRITICAL':
			_logr.logr.setLevel(logging.CRITICAL)
		elif env_level == 'ERROR':
			_logr.logr.setLevel(logging.ERROR)
		elif env_level == 'WARNING':
			_logr.logr.setLevel(logging.WARNING)
		elif env_level == 'INFO':
			_logr.logr.setLevel(logging.INFO)
		elif env_level == 'DEBUG':
			_logr.logr.setLevel(logging.DEBUG)
		elif env_level == 'NOTSET':
			_logr.logr.setLevel(logging.NOTSET)

def info(msg):
	pre()
	_logr.info(msg)

def debug(msg):
	pre()
	_logr.debug(msg)

def warn(msg):
	pre()
	_logr.warn(msg)

def error(msg):
	pre()
	_logr.error(msg)

def critical(msg):
	pre()
	_logr.critical(msg)

def exception(ex, msg = 'EXCEPTION:'):
	pre()
	_logr.exception(ex, msg)

