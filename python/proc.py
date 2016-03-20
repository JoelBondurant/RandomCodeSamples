"""A module to deal with processes."""

import datetime

def uptime(asstr = False):
	"""Get system uptime>"""
	raw = ''
	with open('/proc/uptime','r') as ut:
		raw = ut.read()[:-1]
	uts = list(map(lambda x: int(float(x)), raw.split(' ')))
	if asstr:
		uts = str(datetime.timedelta(seconds = uts[0]))
	return uts
