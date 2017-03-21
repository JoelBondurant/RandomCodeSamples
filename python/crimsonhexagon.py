import os
import json
import time
import datetime
import requests
import cachetools.func
from aiobj.util import temporal
from aiobj.util import logger
from aiobj.util import files


BASE = 'https://api.crimsonhexagon.com/api/'
PASSWORD = os.getenv('CRIMSON_HEXAGON_API_KEY', 'blah')
AUTH_KEY = {'username':'notset', 'password':PASSWORD}
DL_PATH = '/collector/crimsonhexagon'
BEGINNING_OF_TIME = '2014-01-01'
EDIT_PATCHING = True
SINGLE_MONITOR = None

def set_edit_patching(edit_patching):
	"""Set the global module level edit patching flag.
	This determines whether or not start dates of data
	retrieval should be set back to the beginning of time
	for monitors which have been edited."""
	global EDIT_PATCHING
	EDIT_PATCHING = bool(edit_patching)

def set_single_monitor(monitor_id):
	"""Set the global module level single monitor_id
	for all data pulling."""
	global SINGLE_MONITOR
	SINGLE_MONITOR = monitor_id

@cachetools.func.ttl_cache(maxsize = 1, ttl = 7200)
def token():
	"""Get an authentication token for the session."""
	resp = requests.get(BASE + 'authenticate', params = AUTH_KEY)
	return resp.json()['auth']

def key():
	"""Package the auth token."""
	return {'auth': token()}

@cachetools.func.ttl_cache(maxsize = 1, ttl = 7200)
def teams():
	"""Root node of CH data."""
	resp = requests.get(BASE + 'team/list', params = key())
	return resp.json()['teams']

@cachetools.func.ttl_cache(maxsize = 1, ttl = 7200)
def monitors_all():
	"""Get basic info on all monitors."""
	time.sleep(0.6) # API Limit: 2 calls per second.
	resp = requests.get(BASE + 'monitor/list', params = key()).json()
	assert resp['status'] == 'success'
	mons = resp['monitors']
	if SINGLE_MONITOR is not None:
		mons = [x for x in mons if x['id'] == SINGLE_MONITOR]
	return mons

def monitors(start_date = None, end_date = None):
	"""Get basic info on all monitors filtered by date range."""
	start_date = start_date or str(temporal.adddays(-1))
	end_date = end_date or str(temporal.adddays(-1))
	mons = monitors_all()
	fmons = [] # Filter monitors for listening range.
	for mon in mons:
		if mon['resultsStart'] < start_date and mon['resultsEnd'] < start_date:
			continue
		if mon['resultsStart'] > end_date and mon['resultsEnd'] > end_date:
			continue
		fmons += [mon]
	return fmons

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_audit(start_date, end_date):
	"""Monitor audit history."""
	results = []
	params = key()
	for mon in monitors_all():
		monitor_id = mon['id']
		params['id'] = monitor_id
		resp = requests.get(BASE + 'monitor/audit', params = params).json()
		assert resp['status'] == 'success'
		resp.pop('status')
		resp['auditInfo'] = [x for x in resp['auditInfo'][:10] if str(start_date) <= x['eventDate'][:10] <= str(end_date)]
		if len(resp['auditInfo']) == 0:
			continue
		resp['monitor_id'] = monitor_id
		results += [resp]
	return results

def monitor_edits(start_date, end_date):
	"""Set of monitor_ids which have been modified within a date range"""
	ma = monitor_audit(start_date, end_date)
	return set([x['monitor_id'] for x in ma if 'EDITED' in [y['event'] for y in x['auditInfo']]])

def monitor_range(monitor_id, start_date = None, end_date = None):
	"""Monitor date range filtered by date range."""
	start_date = start_date or str(temporal.adddays(-1))
	end_date = end_date or str(temporal.adddays(-1))
	if EDIT_PATCHING and monitor_id in monitor_edits(start_date, end_date):
		logger.warn('Edit patching monitor: %s' % monitor_id)
		start_date = BEGINNING_OF_TIME
	mons = monitors(start_date, end_date)
	mon = None
	for mx in mons:
		if mx['id'] == monitor_id:
			mon = mx
	if mon == None:
		return (None, None)
	sda = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
	eda = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
	sdm = datetime.datetime.strptime(str(mon['resultsStart'][:10]), '%Y-%m-%d').date()
	edm = (datetime.datetime.strptime(str(mon['resultsEnd'][:10]), '%Y-%m-%d') - datetime.timedelta(days = 1)).date()
	sd = sda
	ed = eda
	if sdm > sda:
		sd = sdm
	if edm < eda:
		ed = edm
	return (str(sd), str(ed))

def range_call(endpoint, monitor_id, start_date = None, end_date = None, addl_params = {}):
	"""Call an endpoint with a time range."""
	(start_date, end_date) = monitor_range(monitor_id, start_date, end_date)
	params = key()
	params['id'] = monitor_id
	params['start'] = str(start_date)
	# Shift range to include end date:
	end_date = str((datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days = 1)).date())
	params['end'] = str(end_date)
	params.update(addl_params)
	time.sleep(0.6) # API Limit: 2 calls per second.
	resp = requests.get(BASE + endpoint, params = params).json()
	assert resp['status'] == 'success'
	results = []
	if 'results' in resp:
		results = resp['results']
	elif 'dailyResults' in resp:
		results = resp['dailyResults']
	result = {}
	result['monitor_id'] = monitor_id
	result['results'] = results
	return result

def range_call2(endpoint, monitor_id, start_date = None, end_date = None, addl_params = {}, ignore_errors = False):
	"""Like range_call, but iterates over calls for each day."""
	(start_date, end_date) = monitor_range(monitor_id, start_date, end_date)
	# Shift range to include end date:
	end_date = str((datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days = 1)).date())
	start = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
	end = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
	resps = {'results': []}
	xdate = start
	while xdate < end:
		params = key()
		params['id'] = monitor_id
		datebin = str(xdate)
		params['start'] = str(xdate)
		xdate += datetime.timedelta(days = 1)
		params['end'] = str(xdate)
		params.update(addl_params)
		time.sleep(0.6) # API Limit: 2 calls per second.
		resp = requests.get(BASE + endpoint, params = params).json()
		if ignore_errors and resp['status'] != 'success':
			continue
		assert resp['status'] == 'success'
		resp.pop('status')
		resp['datebin'] = datebin
		resps['results'].append(resp)
	resps['monitor_id'] = monitor_id
	return resps

def social_monitors(start_date = None, end_date = None):
	"""Get basic info on all social Monitors."""
	return [x for x in monitors(start_date, end_date) if x['type'] == 'SOCIAL']

def facebook_monitors(start_date = None, end_date = None):
	"""Get basic info on all Facebook Monitors."""
	return [x for x in social_monitors(start_date, end_date) if x['sources'] == ['Facebook']]

def twitter_monitors(start_date = None, end_date = None):
	"""Get basic info on all Twitter Monitors."""
	return [x for x in social_monitors(start_date, end_date) if x['sources'] == ['Twitter']]

def instagram_monitors(start_date = None, end_date = None):
	"""Get basic info on all Instagram Monitors."""
	return [x for x in social_monitors(start_date, end_date) if x['sources'] == ['Instagram']]


@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_results(start_date, end_date):
	"""Monitor results api endpoint."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call('monitor/results', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_results_by_city(start_date, end_date):
	"""Monitor results api endpoint by city."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/geography/cities', mon['id'], start_date, end_date, addl_params = {'country':'USA'})
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_results_by_state(start_date, end_date):
	"""Monitor results api endpoint by state."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/geography/states', mon['id'], start_date, end_date, addl_params = {'country':'USA'})
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_demographics_age(start_date, end_date):
	"""Monitor age demographic details."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/demographics/age', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_demographics_gender(start_date, end_date):
	"""Monitor gender demographic details."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/demographics/gender', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_topics(start_date, end_date):
	"""Monitor topic clusters."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/topics', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_sources(start_date, end_date):
	"""Monitor sites and sources."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/sources', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_wordclouds(start_date, end_date):
	"""Monitor wordclouds."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/wordcloud', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_affinities(start_date, end_date):
	"""Monitor affinites and interests."""
	results = []
	for mon in twitter_monitors(start_date, end_date):
		resp = range_call2('monitor/interestaffinities', mon['id'], start_date, end_date, ignore_errors = True)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def monitor_posts(start_date, end_date):
	"""Monitor posts."""
	results = []
	for mon in monitors(start_date, end_date):
		resp = range_call2('monitor/posts', mon['id'], start_date, end_date)
		if resp != None:
			results += [resp]
	return results

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def facebook_admin_posts(start_date, end_date):
	"""Facebook admin posts."""
	posts = []
	for mon in facebook_monitors(start_date, end_date):
		resp = range_call('monitor/facebook/adminposts', mon['id'], start_date, end_date)
		if resp != None:
			posts += [resp]
	return posts

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def facebook_page_likes(start_date, end_date):
	"""Facebook page likes."""
	posts = []
	for mon in facebook_monitors(start_date, end_date):
		resp = range_call('monitor/facebook/pagelikes', mon['id'], start_date, end_date)
		if resp != None:
			posts += [resp]
	return posts

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def facebook_total_activity(start_date, end_date):
	"""Facebook total activity."""
	posts = []
	for mon in facebook_monitors(start_date, end_date):
		resp = range_call('monitor/facebook/totalactivity', mon['id'], start_date, end_date)
		if resp != None:
			posts += [resp]
	return posts

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def twitter_engagement_metrics(start_date, end_date):
	"""Twitter engagement metrics."""
	rs = []
	for mon in twitter_monitors(start_date, end_date):
		resp = range_call('monitor/twittermetrics', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def twitter_followers(start_date, end_date):
	"""Twitter followers."""
	rs = []
	for mon in twitter_monitors(start_date, end_date):
		resp = range_call('monitor/twittersocial/followers', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def twitter_sent_posts(start_date, end_date):
	"""Twitter sent posts."""
	rs = []
	for mon in twitter_monitors(start_date, end_date):
		resp = range_call('monitor/twittersocial/sentposts', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def twitter_total_engagement(start_date, end_date):
	"""Twitter total engagement."""
	rs = []
	for mon in twitter_monitors(start_date, end_date):
		resp = range_call('monitor/twittersocial/totalengagement', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def instagram_followers(start_date, end_date):
	"""Instagram Followers"""
	rs = []
	for mon in instagram_monitors(start_date, end_date):
		resp = range_call('monitor/instagram/followers', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def instagram_total_activity(start_date, end_date):
	"""Instagram Total Activity"""
	rs = []
	for mon in instagram_monitors(start_date, end_date):
		resp = range_call('monitor/instagram/totalactivity', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

@cachetools.func.ttl_cache(maxsize = 10000, ttl = 7200)
def instagram_sent_media(start_date, end_date):
	"""Instagram Sent Media"""
	rs = []
	for mon in instagram_monitors(start_date, end_date):
		resp = range_call('monitor/instagram/sentmedia', mon['id'], start_date, end_date)
		if resp != None:
			rs += [resp]
	return rs

def savejson(json_blob):
	"""Save a json blob to disk."""
	fn = 'crimsonhexagon_' + temporal.datetimestamp() + '.json'
	fp = os.path.join(DL_PATH, fn)
	os.makedirs(DL_PATH, exist_ok = True)
	files.savejson(json_blob, fp)
	logger.info('Crimson Hexagon downloaded: %s' % fp)

def download(start_date = None, end_date = None):
	"""Download all the CH data for a time range. Default time range is yesterday."""
	start_date = start_date or str(temporal.adddays(-1))
	end_date = end_date or str(temporal.adddays(-1))
	logger.info('Crimson Hexagon download started. [%s, %s]' % (start_date, end_date))
	params = {''}
	dat = {}
	dat['start_date'] = start_date
	dat['end_date'] = end_date
	dat['started'] = time.time()
	is_finished = False
	while time.time() - dat['started'] < 6*3600:
		try:
			logger.info('Crimson Hexagon metadata...')
			dat['monitors'] = monitors_all()
			dat['monitor_audit'] = monitor_audit(start_date, end_date)
			logger.info('Crimson Hexagon monitor results...')
			dat['monitor_results'] = monitor_results(start_date, end_date)
			dat['monitor_results_bycity'] = monitor_results_by_city(start_date, end_date)
			dat['monitor_results_bystate'] = monitor_results_by_state(start_date, end_date)
			logger.info('Crimson Hexagon monitor demographics...')
			dat['monitor_demographics_age'] = monitor_demographics_age(start_date, end_date)
			dat['monitor_demographics_gender'] = monitor_demographics_gender(start_date, end_date)
			logger.info('Crimson Hexagon monitor topics...')
			dat['monitor_topics'] = monitor_topics(start_date, end_date)
			logger.info('Crimson Hexagon monitor sources...')
			dat['monitor_sources'] = monitor_sources(start_date, end_date)
			logger.info('Crimson Hexagon monitor wordclouds...')
			dat['monitor_wordclouds'] = monitor_wordclouds(start_date, end_date)
			logger.info('Crimson Hexagon monitor affinities...')
			dat['monitor_affinities'] = monitor_affinities(start_date, end_date)
			logger.info('Crimson Hexagon monitor posts...')
			dat['monitor_posts'] = monitor_posts(start_date, end_date)
			logger.info('Crimson Hexagon facebook results...')
			dat['facebook_admin_posts'] = facebook_admin_posts(start_date, end_date)
			dat['facebook_page_likes'] = facebook_page_likes(start_date, end_date)
			dat['facebook_total_activity'] = facebook_total_activity(start_date, end_date)
			logger.info('Crimson Hexagon twitter results...')
			dat['twitter_engagement_metrics'] = twitter_engagement_metrics(start_date, end_date)
			dat['twitter_followers'] =  twitter_followers(start_date, end_date)
			dat['twitter_sent_posts'] = twitter_sent_posts(start_date, end_date)
			dat['twitter_total_engagement'] = twitter_total_engagement(start_date, end_date)
			logger.info('Crimson Hexagon instagram results...')
			dat['instagram_followers'] = instagram_followers(start_date, end_date)
			dat['instagram_total_activity'] = instagram_total_activity(start_date, end_date)
			dat['instagram_sent_media'] = instagram_sent_media(start_date, end_date)
			is_finished = True
			break
		except Exception as ex:
			logger.exception(ex, 'Crimson Hexagon API failure, retrying in 600 sec...')
			time.sleep(600)
	if is_finished:
		dat['finished'] = time.time()
		dat['duration'] = dat['finished'] - dat['started']
		savejson(dat)
	else:
		logger.warn('Crimson Hexagon download failed!')
	logger.info('Crimson Hexagon download finished.')

def history(start_date = None, end_date = None, daysperbatch = 30, monitor_id = None):
	"""Historical loading helper, wrapper to self.download(start_date, end_date).
	Defaults timerange [BEGINNING_OF_TIME, YESTERDAY]."""
	start_date = start_date or BEGINNING_OF_TIME
	end_date = end_date or str(temporal.adddays(-1))
	set_single_monitor(monitor_id)
	set_edit_patching(False)
	start = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
	end = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
	logger.info('Crimson Hexagon history downloading: [%s, %s]' % (start, end))
	sdate = start
	while sdate <= end:
		edate = sdate + datetime.timedelta(days = daysperbatch - 1)
		if edate >= end:
			edate = end
		download(str(sdate), str(edate))
		sdate += datetime.timedelta(days = daysperbatch)
	set_edit_patching(True)
	set_single_monitor(None)

def run():
	"""Extra layers of abstraction."""
	download()

