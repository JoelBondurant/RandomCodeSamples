import os
import json
import time
import requests
import cachetools
from analyticobjects.util import temporal
from analyticobjects.util import logger
from analyticobjects.util import files


BASE = 'https://api.crimsonhexagon.com/api/'
PASSWORD = os.getenv('CRIMSON_HEXAGON_API_KEY', 'blah')
USER = os.getenv('CRIMSON_HEXAGON_API_USER', 'blah')
AUTH_KEY = {'username':USER, 'password':PASSWORD}
DL_PATH = '/dataVol/collector/crimsonhexagon'


@cachetools.func.ttl_cache(maxsize = 1, ttl = 120)
def token():
	resp = requests.get(BASE + 'authenticate', params = AUTH_KEY)
	return resp.json()['auth']

def key():
	return {'auth': token()}

@cachetools.func.ttl_cache(maxsize = 1, ttl = 120)
def teams():
	resp = requests.get(BASE + 'team/list', params = key())
	return resp.json()['teams']

@cachetools.func.ttl_cache(maxsize = 1, ttl = 120)
def monitors():
	mons = []
	for team in teams():
		resp = requests.get(BASE + 'monitor/list', params = key())
		mons += resp.json()['monitors']
	return mons

def range_call(endpoint, monitor_id, start_date = None, end_date = None, addl_params = {}):
	start_date = start_date or str(temporal.adddays(-1))
	end_date = end_date or str(temporal.adddays(-1))
	params = key()
	params['id'] = monitor_id
	params['start'] = start_date
	params['end'] = end_date
	params.update(addl_params)
	resp = requests.get(BASE + endpoint, params = params)
	jresp = resp.json()
	jresp['monitor_id'] = monitor_id
	return jresp

def history_call(endpoint, monitor_id, days = 1, addl_params = {}):
	start_date = str(temporal.adddays(-days))
	end_date = str(temporal.adddays(-1))
	return range_call(endpoint, monitor_id, start_date = start_date, end_date = end_date, addl_params = addl_params)

def social_monitors():
	return [x for x in monitors() if x['type'] == 'SOCIAL']

def facebook_monitors():
	return [x for x in social_monitors() if x['sources'] == ['Facebook']]

def twitter_monitors():
	return [x for x in social_monitors() if x['sources'] == ['Twitter']]

def instagram_monitors():
	return [x for x in social_monitors() if x['sources'] == ['Instagram']]

def monitor_results(days = 1):
	results = []
	for mon in monitors():
		resp = history_call('monitor/results', mon['id'], days = days)
		results += [resp]
	return results

def monitor_results_by_city(days = 1):
	results = []
	for mon in monitors():
		resp = history_call('monitor/geography/cities', mon['id'], days = days, addl_params = {'country':'USA'})
		results += [resp]
	return results

def monitor_results_by_state(days = 1):
	results = []
	for mon in monitors():
		resp = history_call('monitor/geography/states', mon['id'], days = days, addl_params = {'country':'USA'})
		results += [resp]
	return results

def facebook_admin_posts(days = 1):
	posts = []
	for mon in facebook_monitors():
		resp = history_call('monitor/facebook/adminposts', mon['id'], days = days)
		posts += [resp]
	return posts

def facebook_page_likes(days = 1):
	posts = []
	for mon in facebook_monitors():
		resp = history_call('monitor/facebook/pagelikes', mon['id'], days = days)
		posts += [resp]
	return posts

def facebook_total_activity(days = 1):
	posts = []
	for mon in facebook_monitors():
		resp = history_call('monitor/facebook/totalactivity', mon['id'], days = days)
		posts += [resp]
	return posts

def twitter_engagement_metrics(days = 1):
	rs = []
	for mon in twitter_monitors():
		resp = history_call('monitor/twittermetrics', mon['id'], days = days)
		rs += [resp]
	return rs

def twitter_followers(days = 1):
	rs = []
	for mon in twitter_monitors():
		resp = history_call('monitor/twittersocial/followers', mon['id'], days = days)
		rs += [resp]
	return rs

def twitter_sent_posts(days = 1):
	rs = []
	for mon in twitter_monitors():
		resp = history_call('monitor/twittersocial/sentposts', mon['id'], days = days)
		rs += [resp]
	return rs

def twitter_total_engagement(days = 1):
	rs = []
	for mon in twitter_monitors():
		resp = history_call('monitor/twittersocial/totalengagement', mon['id'], days = days)
		rs += [resp]
	return rs

def instagram_followers(days = 1):
	rs = []
	for mon in instagram_monitors():
		resp = history_call('monitor/instagram/followers', mon['id'], days = days)
		rs += [resp]
	return rs

def instagram_total_activity(days = 1):
	rs = []
	for mon in instagram_monitors():
		resp = history_call('monitor/instagram/totalactivity', mon['id'], days = days)
		rs += [resp]
	return rs

def instagram_sent_media(days = 1):
	rs = []
	for mon in instagram_monitors():
		resp = history_call('monitor/instagram/sentmedia', mon['id'], days = days)
		rs += [resp]
	return rs

def savejson(json_blob):
	fn = 'crimsonhexagon_' + temporal.datetimestamp() + '.json'
	fp = os.path.join(DL_PATH, fn)
	os.makedirs(DL_PATH, exist_ok = True)
	files.savejson(json_blob, fp)
	logger.info('Crimson Hexagon downloaded: %s' % fp)

def download(days = 1):
	logger.info('Crimson Hexagon download started.')
	dat = {}
	dat['is_historical'] = (days > 1)
	started = time.time()
	is_finished = False
	while time.time() - started < 600:
		try:
			dat['monitors'] = monitors()
			logger.info('Crimson Hexagon monitor results...')
			dat['monitor_results'] = monitor_results(days)
			dat['monitor_results_bycity'] = monitor_results_by_city(days)
			dat['monitor_results_bystate'] = monitor_results_by_state(days)
			logger.info('Crimson Hexagon facebook results...')
			dat['facebook_admin_posts'] = facebook_admin_posts(days)
			dat['facebook_page_likes'] = facebook_page_likes(days)
			dat['facebook_total_activity'] = facebook_total_activity(days)
			logger.info('Crimson Hexagon twitter results...')
			dat['twitter_engagement_metrics'] = twitter_engagement_metrics(days)
			dat['twitter_followers'] =  twitter_followers(days)
			dat['twitter_sent_posts'] = twitter_sent_posts(days)
			dat['twitter_total_engagement'] = twitter_total_engagement(days)
			logger.info('Crimson Hexagon instagram results...')
			dat['instagram_followers'] = instagram_followers(days)
			dat['instagram_total_activity'] = instagram_total_activity(days)
			dat['instagram_sent_media'] = instagram_sent_media(days)
			is_finished = True
			break
		except Exception as ex:
			logger.exception(ex, 'Crimson Hexagon API failure, retrying in 10s...')
		finally:
			time.sleep(10)
	if is_finished:
		savejson(dat)
	else:
		logger.warn('Crimson Hexagon download failed!')
	logger.info('Crimson Hexagon download finished.')

def run():
	"""Extra layers of abstraction."""
	download()

