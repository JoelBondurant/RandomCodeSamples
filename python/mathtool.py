"""
Starting collection of needed math utils.
"""

def pct(a, b, percent = True, asstr = False, ndigits = 4):
	""" Percent difference function: Calculate the percent difference from a to b. """
	result = 1.0 * (b - a) / a
	if percent:
		result *= 100.0
	result = round(result, ndigits)
	if asstr:
		result = str(result) + '%'
	return result

def isNumber(x):
	""" Is the argument a python numeric type. """
	return ( (type(x) == float) or (type(x) == int) )


