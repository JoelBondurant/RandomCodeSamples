"""
A time utility module to provide datetime utility functions.
"""

import datetime
try:
	import pytz
except ImportError:
	pass


def to_utc(dt, tz = 'America/Los_Angeles'):
	"""Take a time and convert it to UTC."""
	local = pytz.timezone(tz)
	local_dt = local.localize(dt)
	return local_dt.astimezone(pytz.utc)


def from_utc(dt, tz = 'America/Los_Angeles'):
	"""Take a UTC time and convert it to local timezone."""
	dt_utc = pytz.utc.localize(dt)
	local = pytz.timezone(tz)
	return dt_utc.astimezone(local)


def intervalize_dates(date_list, max_days=100):
	"""
	A function to turn a list of dates into an array of date intervals.
	"""
	date_list.sort()
	intervals = []
	start_date = date_list[0]
	end_date = date_list[0]
	for n in range(1, len(date_list)):
		cur_date = date_list[n]
		if (cur_date - end_date == datetime.timedelta(1) and cur_date - end_date < datetime.timedelta(max_days)):
			end_date = cur_date
		else:
			intervals.append((start_date, end_date))
			start_date = cur_date
			end_date = cur_date
	intervals.append((start_date, end_date))
	return intervals


def datetime_format(datetime_obj, fmtstring = '%Y-%m-%d'):
	"""
	A function to string format a datetime.datetime object.
	"""
	return datetime_obj.strftime(fmtstring)


def iso_date_format(date_obj):
	"""
	A function to ISO 8601 string format a datetime.date object.
	"""
	return date_obj.strftime('%Y-%m-%d')


def iso_datetime_format(datetime_obj):
	"""
	A function to ISO 8601 string format a datetime.datetime object.
	"""
	return datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')


def str2date(date_str, date_format = '%Y-%m-%d'):
	"""
	Create a datetime object from a string with default ISO 8601 format.
	"""
	return datetime.datetime.strptime(date_str, date_format).date()


def str2datetime(datetime_str, datetime_format = '%Y-%m-%dT%H:%M:%S'):
	"""
	Create a datetime object from a string with default ISO 8601 format.
	"""
	return datetime.datetime.strptime(datetime_str, datetime_format)


def iso_date():
	"""
	The current date in ISO 8601 format. e.g. 2068-06-30
	"""
	return datetime.date.today().strftime('%Y-%m-%d')


def iso_datetime():
	"""
	The current datetime in ISO 8601 format. e.g. 2068-06-30T12:31:52
	"""
	return datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S')


def now_date(offset = 0):
	"""
	A function to return a the current date.
	"""
	return adddays(offset, datetime.date.today())


def now_datetime(offset = 0):
	"""
	A function to return the current datetime.
	"""
	return adddays(offset, datetime.datetime.today())


def datestamp():
	"""
	A function to return a YYYYmmdd datestamp. e.g. 20680630
	"""
	return datetime.date.today().strftime('%Y%m%d')


def datetimestamp():
	"""
	A function to return a YYYYmmddHHMMSS datetimestamp. e.g. 20680630123152
	"""
	return datetime.datetime.today().strftime('%Y%m%d%H%M%S')


def seconds(as_string = False, zeropad = False):
	"""
	A function to return the current local time second component.
	"""
	sec_value = datetime.datetime.today().second
	if as_string:
		sec_value = str(sec_value)
		if zeropad:
			if len(sec_value) == 1:
				sec_value = '0' + sec_value
	return sec_value


def minutes(as_string = False, zeropad = False):
	"""
	A function to return the current local time minute component.
	"""
	min_value = datetime.datetime.today().minute
	if as_string:
		min_value = str(min_value)
		if zeropad:
			if len(min_value) == 1:
				min_value = '0' + min_value
	return min_value


def hours(as_string = False, zeropad = False):
	"""
	A function to return the current local time hour component.
	"""
	return datetime.datetime.today().hour
	hrs_value = datetime.datetime.today().hour
	if as_string:
		hrs_value = str(hrs_value)
		if zeropad:
			if len(hrs_value) == 1:
				hrs_value = '0' + hrs_value
	return hrs_value


def day(as_string = False, zeropad = False):
	"""
	A function to return the current local time day component.
	"""
	day_value = datetime.datetime.today().day
	if as_string:
		day_value = str(day_value)
		if zeropad:
			if len(day_value) == 1:
				day_value = '0' + day_value
	return day_value


def month(as_string = False, zeropad = False):
	"""
	A function to return the current local time month component.
	"""
	month_value = datetime.datetime.today().month
	if as_string:
		month_value = str(month_value)
		if zeropad:
			if len(month_value) == 1:
				month_value = '0' + month_value
	return month_value


def year(as_string = False):
	"""
	A function to return the current local time year component.
	"""
	year_value = datetime.datetime.today().year
	if as_string:
		year_value = str(year_value)
	return year_value


def addhours(hrs, dt = None):
	"""
	A function to add hours to a date, with now as a default.
	"""
	dt = dt or datetime.datetime.today()
	return dt + datetime.timedelta(hours = hrs)


def adddays(days, dt = None):
	"""
	A function to add days to a date, with now as a default.
	"""
	dt = dt or datetime.date.today()
	return dt + datetime.timedelta(days = days)


def secondsdiff(datetime1, datetime2 = None):
	"""
	Compute the seconds between two dates, with the present time being one default.
	"""
	datetime2 = datetime2 or datetime.datetime.today()
	delta = datetime1 - datetime2
	secs = delta.seconds
	secs += (delta.days * 24 * 60 * 60)
	return secs


def hoursdiff(datetime1, datetime2 = None):
	"""
	Compute the hours between two dates, with one date defaulting to now.
	"""
	datetime2 = datetime2 or datetime.datetime.today()
	secs = secondsdiff(datetime1, datetime2)
	hrs = secs / 3600.0
	return hrs


def daysdiff(datetime1, datetime2 = None):
	"""
	Compute the days between two dates, with one date defaulting to now.
	"""
	datetime2 = datetime2 or datetime.datetime.today()
	if type(datetime1) == type(''):
		datetime1 = str2date(datetime1)
	hrs = hoursdiff(datetime1, datetime2)
	dys = hrs / 24.0
	return dys


def newdate(yr, mo, dy):
	"""
	Produce a date object from year, month, day tuple
	"""
	return datetime.date(yr, mo, dy)


def newdatetime(yr, mo, dy):
	"""
	Produce a datetime object from year, month, day tuple
	"""
	return datetime.datetime(yr, mo, dy)


def weeknumber(adate, offset = 1):
	"""
	Returns the week number in year for a supplied date.
	"""
	shifted_adate = adate + datetime.timedelta(days = offset)
	return shifted_adate.isocalendar()[1]


def month_name(adate, abbrev = False):
	"""
	Returns a tuple of month name and abbreviated month name per supplied date.
	"""
	monthnm = None
	if abbrev:
		monthnm = adate.strftime('%b')
	else:
		monthnm = adate.strftime('%B')
	return monthnm


def day_in_week(adate, offset = 1):
	"""
	Returns the day of the week as an integer where Sunday = 1, Monday = 2, ..., Saturday = 7
	"""
	return ((adate.weekday() + offset) % 7) + 1


def day_in_year(adate):
	"""
	Returns the day of the year as an integer for the supplied date.
	"""
	dt = datetime.datetime.combine(adate, datetime.min.time())
	return dt.timetuple().tm_yday


def isdate(adate):
	"""Check if argument is of type datetime.date."""
	return type(adate) == datetime.date


def isdatetime(adatetime):
	"""Check if argument is of type datetime.datetime."""
	return type(adatetime) == datetime.datetime


def unix2datetime(unixseconds):
	"""Convert unix timestamp epoch seconds to datetime.datetime"""
	return datetime.datetime.utcfromtimestamp(unixseconds)


def zeropad(anint):
	"""Convert an integer to a two character string."""
	intstr = str(anint)
	if len(intstr) == 1:
		intstr = '0' + intstr
	return intstr


def generate_range(startDate, endDate):
	"""Generate a list of dates [startDate, ..., endDate]"""
	dateList = []
	if type(startDate) == str:
		startDate = str2date(startDate)
	if type(endDate) == str:
		endDate = str2date(endDate)
	step = datetime.timedelta(days = 1)
	dt = startDate
	while dt <= endDate:
		dateList.append(dt)
		dt += step
	if len(dateList) == 0 or dateList[-1:][0] < endDate:
		dateList.append(endDate)
	return dateList



