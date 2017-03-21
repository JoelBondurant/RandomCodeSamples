#!/usr/bin/env python
"""
Module to connect to Google reporting.
"""
import requests
import cachetools.func
import six, six.moves # prime for google
import httplib2, os, sys, io, time, datetime, itertools, random, argparse, json, csv
import googleapiclient, googleapiclient.discovery, googleapiclient.http, googleapiclient.errors
import oauth2client, oauth2client.file, oauth2client.client, oauth2client.tools
from bssp.util import temporal
from bssp.util import logger
from bssp.util import crypto
from bssp.util import files


### Aiobj Creds:
CLIENT_11_SECRETS = './config/google_aiobj1.json'
CLIENT_22_SECRETS = './config/google_aiobj2.json'
PROFILE_ID = '88855571'
### API Targets:
DDM_API_TARGET = 'dfareporting'
DCLK_API_TARGET = 'doubleclicksearch'
ANALYTICS_TARGET = 'analytics'
BID_MANAGER_TARGET = 'doubleclickbidmanager'
### API Versions:
DDM_API_VERSION = 'v2.7'
DCLK_API_VERSION = 'v2'
ANALYTICS_VERSION = 'v3'
BID_MANAGER_VERSION = 'v1'
### API Scopes:
DDM_REPORTING_SCOPE = 'https://www.googleapis.com/auth/dfareporting'
DDM_TRAFFICKING_SCOPE = 'https://www.googleapis.com/auth/dfatrafficking'
DCLK_SEARCH_SCOPE = 'https://www.googleapis.com/auth/doubleclicksearch'
ANALYTICS_SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
BID_MANAGER_SCOPE = 'https://www.googleapis.com/auth/doubleclickbidmanager'
SCOPES = {DDM_REPORTING_SCOPE, DDM_TRAFFICKING_SCOPE, DCLK_SEARCH_SCOPE, ANALYTICS_SCOPE, BID_MANAGER_SCOPE}
### API CREDS:
DDM_REPORTING_CREDS = './config/google_reporting_creds.dat'
DDM_TRAFFICKING_CREDS = './config/google_trafficking_creds.dat'
DCLK_SEARCH_CREDS = './config/google_search_creds.dat'
ANALYTICS_CREDS = './config/google_analytics_creds.dat'
BID_MANAGER_CREDS = './config/google_bidmanager_creds.dat'

### Start Google Auth ###

def profileid():
	"""Return BSSP main profile id."""
	return PROFILE_ID

def download_path():
	"""Where to download report files, and ensures path exists."""
	path = '/collector/google'
	os.makedirs(path, mode = 0o770, exist_ok = True)
	return path

@cachetools.func.ttl_cache(maxsize = 1000, ttl = 600)
def google_service(api_scope):
	"""Connect to Google's DFA Reporting service with 3-leg oauth2 using the discovery service."""
	# For Google Freebie 2 party API access, 3-leg oauth2 is used.
	# Random sleep to allow concurrency, while avoiding freebie api rate limits.
	time.sleep(random.randint(0, 4))
	decrypt_secrets()
	if api_scope == DDM_REPORTING_SCOPE:
		cred_storage = DDM_REPORTING_CREDS
		client_secrets = CLIENT_11_SECRETS
	elif api_scope == DDM_TRAFFICKING_SCOPE:
		cred_storage = DDM_TRAFFICKING_CREDS
		client_secrets = CLIENT_11_SECRETS
	elif api_scope == DCLK_SEARCH_SCOPE:
		cred_storage = DCLK_SEARCH_CREDS
		client_secrets = CLIENT_11_SECRETS
	elif api_scope == ANALYTICS_SCOPE:
		cred_storage = ANALYTICS_CREDS
		client_secrets = CLIENT_22_SECRETS
	elif api_scope == BID_MANAGER_SCOPE:
		cred_storage = BID_MANAGER_CREDS
		client_secrets = CLIENT_11_SECRETS
	storage = oauth2client.file.Storage(cred_storage)
	creds = storage.get()
	oauth_flow = oauth2client.client.flow_from_clientsecrets(client_secrets, scope=api_scope, message=oauth2client.tools.message_if_missing(client_secrets))
	if creds is None or creds.invalid: # This isn't supposed to ever work, must be done manually with a browser (3-leg oauth).
		flags = oauth2client.tools.argparser.parse_args(args=['--noauth_local_webserver'])
		creds = oauth2client.tools.run_flow(oauth_flow, storage, flags)
	http_auth = creds.authorize(http = httplib2.Http())
	if api_scope == DDM_REPORTING_SCOPE or api_scope == DDM_TRAFFICKING_SCOPE:
		serv = googleapiclient.discovery.build(DDM_API_TARGET, DDM_API_VERSION, http = http_auth)
	elif api_scope == DCLK_SEARCH_SCOPE:
		serv = googleapiclient.discovery.build(DCLK_API_TARGET, DCLK_API_VERSION, http = http_auth)
	elif api_scope == ANALYTICS_SCOPE:
		serv = googleapiclient.discovery.build(ANALYTICS_TARGET, ANALYTICS_VERSION, http = http_auth)
	elif api_scope == BID_MANAGER_SCOPE:
		serv = googleapiclient.discovery.build(BID_MANAGER_TARGET, BID_MANAGER_VERSION, http = http_auth)
	return serv


def api_key():
	"""A single encryption key to encrypt all the Google creds."""
	akey = os.getenv('GOOGLE_API_KEY')
	if not akey or akey == '' or akey == 'blah':
		raise PermissionError('$GOOGLE_API_KEY not set.')
	return akey

def encrypt_secret(path2secret):
	"""Encrypt Google API Oauth2 3-leg tokens for source control."""
	crypto.encrypt(path2secret, api_key())

def decrypt_secrets():
	"""Decrypt Google API Oauth2 3-leg tokens for use."""
	if not os.path.exists(CLIENT_11_SECRETS):
		crypto.decrypt(crypto.encrypted_name(CLIENT_11_SECRETS), api_key())
	if not os.path.exists(CLIENT_22_SECRETS):
		crypto.decrypt(crypto.encrypted_name(CLIENT_22_SECRETS), api_key())
	if not os.path.exists(DDM_REPORTING_CREDS):
		crypto.decrypt(crypto.encrypted_name(DDM_REPORTING_CREDS), api_key())
	if not os.path.exists(DDM_TRAFFICKING_CREDS):
		crypto.decrypt(crypto.encrypted_name(DDM_TRAFFICKING_CREDS), api_key())
	if not os.path.exists(DCLK_SEARCH_CREDS):
		crypto.decrypt(crypto.encrypted_name(DCLK_SEARCH_CREDS), api_key())
	if not os.path.exists(ANALYTICS_CREDS):
		crypto.decrypt(crypto.encrypted_name(ANALYTICS_CREDS), api_key())
	if not os.path.exists(BID_MANAGER_CREDS):
		crypto.decrypt(crypto.encrypted_name(BID_MANAGER_CREDS), api_key())


def reporting_service():
	"""Connect to Google's DFA Reporting service with oauth2 using the discovery service."""
	return google_service(DDM_REPORTING_SCOPE)


def trafficking_service():
	"""Connect to Google's DFA Reporting service with oauth2 using the discovery service."""
	return google_service(DDM_TRAFFICKING_SCOPE)


def search_service():
	"""Connect to Google's Search API service with oauth2 using the discovery service."""
	return google_service(DCLK_SEARCH_SCOPE)


def analytics_service():
	"""Connect to Google Analytics API service with oauth2 using the discovery service."""
	return google_service(ANALYTICS_SCOPE)

def bidmanager_service():
	"""Connect to Google Bid Manager API service with oauth2 using the discovery service."""
	return google_service(BID_MANAGER_SCOPE)

### End Google Auth ###


### Begin Google BidManager Reporting ###

def bidmanager_queries():
	return bidmanager_service().queries().listqueries().execute()

def bidmanager_report(query_id = 1482284171934):
	logger.info('Google BidManager report download started.')
	started = time.time()
	while time.time() - started < 1200:
		try:
			rpts = bidmanager_service().reports().listreports(queryId = query_id).execute()
			rpt_url = rpts['reports'][-1]['metadata']['googleCloudStoragePath']
			csvdat = requests.get(rpt_url).text
			fn = 'google_bidmanager_' + temporal.datetimestamp() + '.csv'
			fp = os.path.join(download_path(), fn)
			with open(fp, 'wt') as fout:
				fout.write(csvdat)
			logger.info('Google BidManager report download success: %s' % fn)
			break
		except Exception as ex:
			logger.warn('Google BidManager failure!\n\tEXCEPTION: ' + str(ex))
			time.sleep(60)

def download_bidmanager_reports():
	bidmanager_report()

### End Google BidManager Reporting ###


### Begin Google Analytics Reporting ###

def analytics_page_size():
	"""Get the max Google Analytics pagination page size."""
	return PAGINATION_MAX_RESULTS
	
def analytics_get_client_info():
	"""Get all current analytics target profiles IDs. What are we going to fully process."""
	return ANALYTICS_TARGET_PROFILE_IDS


@cachetools.func.ttl_cache(maxsize = 10**4, ttl = 5000)
def analytics_accounts():
	accts = analytics_service().management().accounts().list().execute()
	return accts['items']

@cachetools.func.ttl_cache(maxsize = 10**4, ttl = 5000)
def analytics_segments():
	segs = analytics_service().management().segments().list().execute()
	return segs['items']

@cachetools.func.ttl_cache(maxsize = 10**4, ttl = 5000)
def analytics_properties(account_id):
	props = analytics_service().management().webproperties().list(accountId = account_id).execute()
	return props['items']

@cachetools.func.ttl_cache(maxsize = 10**4, ttl = 5000)
def analytics_profiles(account_id, property_id):
	profs = analytics_service().management().profiles().list(accountId = account_id, webPropertyId = property_id).execute()
	return profs['items']

@cachetools.func.ttl_cache(maxsize = 10**4, ttl = 5000)
def analytics_goals(account_id, property_id, profile_id):
	goals = analytics_service().management().goals().list(accountId = account_id, webPropertyId = property_id, profileId = profile_id).execute()
	return goals['items']


### End Google Analytics Reporting ###

### Begin Google DoubleClick Search Reporting ###

@cachetools.func.ttl_cache(maxsize = 100, ttl = 3600)
def search_dims(report):
	"""DoubleClick Search Dimensions"""
	with open(os.path.join('./reports/', report), 'r') as fin:
		rpt = json.load(fin)
	serv = search_service()
	req = serv.reports().generate(body = rpt)
	qres = req.execute()
	return qres['rows']

def search_dims_async(report):
	"""Generic helper function to download DS dimensions."""
	with open(os.path.join('./reports/', report), 'r') as fin:
		rpt = json.load(fin)
	serv = search_service()
	req = serv.reports().request(body = rpt)
	rr = req.execute()
	rt = rr['request']['reportType']
	started = time.time()
	timeout_hit = True
	while time.time() - started < 3600:
		time.sleep(10)
		status = serv.reports().get(reportId = rr['id']).execute()
		if not status['isReportReady']:
			pass
		else:
			timeout_hit = False
			break
	if timeout_hit:
		logger.warning('Google %s report timeout hit!' % report)
		return None
	else:
		numchunks = len(status['files'])
		csvtxt = ''
		for chunknum in range(numchunks):
			req = serv.reports().getFile(reportId = rr['id'], reportFragment = chunknum)
			csvdata = req.execute()
			csvtxt += csvdata.decode('utf-8')
		reader = csv.DictReader(io.StringIO(csvtxt), delimiter = '\t')
	return list(reader)

def search_advertisers():
	"""DoubleClick Search Advertisers"""
	return search_dims('search_advertiser.json')

def search_accounts():
	"""DoubleClick Search Accounts"""
	return search_dims('search_account.json')

def search_adgroups():
	"""DoubleClick Search AdGroups"""
	return search_dims_async('search_adgroup.json')

def search_ads():
	"""DoubleClick Search AdGroups"""
	return search_dims_async('search_ad.json')

def search_bidstrategies():
	"""DoubleClick Search BidStrategies"""
	return search_dims_async('search_bidstrategy.json')

def search_campaigns():
	"""DoubleClick Search Campaign"""
	return search_dims_async('search_campaign.json')

def search_activities():
	"""DoubleClick Search Activity"""
	return search_dims_async('search_activity.json')

def download_search_dims():
	"""Download Search Accounts/Advertisers."""
	logger.info('Google search dims download started.')
	sdims = {}
	sdims['search_accounts'] = search_accounts()
	sdims['search_advertisers'] = search_advertisers()
	sdims['search_campaigns'] = search_campaigns()
	sdims['search_adgroups'] = search_adgroups()
	sdims['search_ads'] = search_ads()
	sdims['search_bidstrategies'] = search_bidstrategies()
	sdims['search_activities'] = search_activities()
	dlp = download_path()
	sdims_fn = 'google_searchdims_' + temporal.datetimestamp() + '.json'
	sdims_fp = os.path.join(dlp, sdims_fn)
	files.savejson(sdims, sdims_fp)
	logger.info('Google search dims downloaded: ' + sdims_fp)
	logger.info('Google search dims download finished.')


def search_impressions(start_date = None, end_date = None):
	"""DoubleClick Search Impressions Report"""
	with open('./reports/search_impressions.json', 'r') as fin:
		rpt = json.load(fin)
	rpt['timeRange']['startDate'] = start_date
	rpt['timeRange']['endDate'] = end_date
	serv = search_service()
	req = serv.reports().request(body = rpt)
	rr = req.execute()
	return rr


def search_actions(start_date = None, end_date = None):
	"""DoubleClick Search Actions Report"""
	with open('./reports/search_actions.json', 'r') as fin:
		rpt = json.load(fin)
	rpt['timeRange']['startDate'] = start_date
	rpt['timeRange']['endDate'] = end_date
	serv = search_service()
	req = serv.reports().request(body = rpt)
	rr = req.execute()
	return rr

def search_campaign_impressions(start_date = None, end_date = None):
	"""DoubleClick Search Campaign Impressions Report"""
	with open('./reports/search_campaign_impressions.json', 'r') as fin:
		rpt = json.load(fin)
	rpt['timeRange']['startDate'] = start_date
	rpt['timeRange']['endDate'] = end_date
	serv = search_service()
	req = serv.reports().request(body = rpt)
	rr = req.execute()
	return rr


def search_campaign_actions(start_date = None, end_date = None):
	"""DoubleClick Search Campaign Actions Report"""
	with open('./reports/search_campaign_actions.json', 'r') as fin:
		rpt = json.load(fin)
	rpt['timeRange']['startDate'] = start_date
	rpt['timeRange']['endDate'] = end_date
	serv = search_service()
	req = serv.reports().request(body = rpt)
	rr = req.execute()
	return rr



def search_report_download(report_request, filename_infix):
	"""Generic helper function to download DS reports."""
	rr = report_request
	rt = rr['request']['reportType']
	logger.info('Google search %s %s report download started.' % (rt, filename_infix))
	started = time.time()
	timeout_hit = True
	serv = search_service()
	while time.time() - started < 4*3600:
		time.sleep(10)
		status = serv.reports().get(reportId = rr['id']).execute()
		if not status['isReportReady']:
			logger.info('Report not ready, waiting 10 more sec...')
		else:
			timeout_hit = False
			break
	if timeout_hit:
		logger.warning('Google search %s %s report timeout hit!' % (rt, filename_infix))
	else:
		dlp = download_path()
		fn = 'google_search' + filename_infix + '_' + temporal.datetimestamp() + '.csv'
		fp = os.path.join(dlp, fn)
		numchunks = len(status['files'])
		with open(fp, 'wb') as fout:
			for chunknum in range(numchunks):
				req = serv.reports().getFile(reportId = rr['id'], reportFragment = chunknum)
				csvdata = req.execute()
				fout.write(csvdata)
			logger.info('Google search %s %s report downloaded: %s' % (rt, filename_infix, fp))
		logger.info('Google search %s %s report download finished.' % (rt, filename_infix))
	return status


def download_search_reports(start_date = None, end_date = None):
	"""Download specific DoubleClick search reports."""
	yesterday = temporal.iso_date_format(temporal.adddays(-1))
	if not start_date:
		start_date = yesterday
	if not end_date:
		end_date = yesterday
	start_date = str(start_date)
	end_date = str(end_date)
	download_search_dims()
	simps_rr = search_impressions(start_date, end_date)
	sacts_rr = search_actions(start_date, end_date)
	scampimps_rr = search_campaign_impressions(start_date, end_date)
	scampacts_rr = search_campaign_actions(start_date, end_date)
	simps_status = search_report_download(simps_rr, 'imps')
	sacts_status = search_report_download(sacts_rr, 'acts')
	scampimps_status = search_report_download(scampimps_rr, 'campimps')
	scampacts_status = search_report_download(scampacts_rr, 'campacts')
	status = [simps_status, sacts_status, scampimps_status, scampacts_status]
	return status

### End Google DoubleClick Search Reporting ###


### Start Google DDM Dimensions ###

def api_pager(api_endpoint, endpoint_name, params = {}):
	"""This is to page over DDM API endpoints that support page list operations."""
	params['profileId'] = profileid()
	results = []
	req = api_endpoint.list(**params)
	while True:
		resp = req.execute()
		results += resp[endpoint_name]
		if resp[endpoint_name] and 'nextPageToken' in resp and resp['nextPageToken']:
			req = api_endpoint.list_next(req, resp)
		else:
			break
	return results


def get_advertiser_ids(active = False):
	"""All (active?) advertiser ids from Google.
		We could pull these from Google (get_advertisers), but too many ACTIVE (and really not).
		Ad-ops to inactivate inactivated clients..., hard code for now:"""
	if active:
		return ['5108402','4642908','2347706','2324553','2285349','1885707','1844680']
	else:
		return [adv['id'] for adv in get_advertisers()]


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_advertisers():
	"""Get all advertisers from Google."""
	return api_pager(trafficking_service().advertisers(), 'advertisers')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_sites():
	"""Get all sites from Google."""
	return api_pager(trafficking_service().sites(), 'sites')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_browsers():
	"""Get all browsers from Google."""
	return api_pager(trafficking_service().browsers(), 'browsers')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_platform_types():
	"""Get all platform types from Google."""
	return api_pager(trafficking_service().platformTypes(), 'platformTypes')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_connection_types():
	"""Get all connection types from Google."""
	return api_pager(trafficking_service().connectionTypes(), 'connectionTypes')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_carriers():
	"""Get all carrier types from Google."""
	return api_pager(trafficking_service().mobileCarriers(), 'mobileCarriers')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_campaigns():
	"""Get all campaigns from Google."""
	return api_pager(trafficking_service().campaigns(), 'campaigns')


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_placement_groups(is_historical = False):
	"""Get all placement groups from Google."""
	if is_historical:
		params = {}
	else:
		params = {'minEndDate': str(temporal.adddays(-180))}
	return api_pager(trafficking_service().placementGroups(), 'placementGroups', params)


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_placements(is_historical = False):
	"""Get all placements from Google."""
	if is_historical:
		params = {}
	else:
		params = {'minEndDate': str(temporal.adddays(-180))}
	return api_pager(trafficking_service().placements(), 'placements', params)


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_ads(is_historical = False):
	"""Get all ads from Google."""
	if is_historical:
		params = {}
	else:
		params = {'active': True}
	return api_pager(trafficking_service().ads(), 'ads', params)


@cachetools.func.ttl_cache(maxsize = 2, ttl = 3600)
def get_creatives(is_historical = False):
	"""Get all creatives from Google."""
	if is_historical:
		params = {}
	else:
		params = {'active': True}
	return api_pager(trafficking_service().creatives(), 'creatives', params)


@cachetools.func.ttl_cache(maxsize = 1, ttl = 3600)
def get_sizes():
	"""Get all sizes from Google."""
	return api_pager(trafficking_service().sizes(), 'sizes')


@cachetools.func.ttl_cache(maxsize = 10**4, ttl = 3600)
def get_activities(advertiser_id = None):
	"""Get all Floodlight Activities for an advertiser from Google."""
	if advertiser_id == None:
		acts = []
		for agid in get_advertiser_ids(active = False):
			acts += get_activities(agid)
		return acts
	params = {'advertiserId': advertiser_id}
	return api_pager(trafficking_service().floodlightActivities(), 'floodlightActivities', params)



def download_dimensions(start_date = None, end_date = None):
	"""Download Google DDM Reporting dimension data."""
	logger.info('Google dimensions download started.')
	yesterday = temporal.iso_date_format(temporal.adddays(-1))
	if not start_date or str(start_date) <= yesterday:
		is_historical = True
	dims = {}
	dims['is_historical'] = is_historical
	started = time.time()
	is_finished = False
	while time.time() - started < 3600:
		try:
			logger.info('Google get advertisers...')
			dims['advertisers'] = get_advertisers()
			logger.info('Google advertiser count: %s' % len(dims['advertisers']))
			logger.info('Google get browsers...')
			dims['agents'] = get_browsers()
			logger.info('Google get platform types...')
			dims['platform_types'] = get_platform_types()
			logger.info('Google get connection types...')
			dims['connection_types'] = get_connection_types()
			logger.info('Google get carriers...')
			dims['carriers'] = get_carriers()
			logger.info('Google get sites...')
			dims['sites'] = get_sites()
			logger.info('Google site count: %s' % len(dims['sites']))
			logger.info('Google get activities...')
			dims['activities'] = get_activities()
			logger.info('Google activity count: %s' % len(dims['activities']))
			logger.info('Google get campaigns...')
			dims['campaigns'] = get_campaigns()
			logger.info('Google campaign count: %s' % len(dims['campaigns']))
			logger.info('Google get ads...')
			dims['ads'] = get_ads(is_historical)
			logger.info('Google ad count: %s' % len(dims['ads']))
			logger.info('Google get placement groups...')
			dims['placement_groups'] = get_placement_groups(is_historical)
			logger.info('Google placement group count: %s' % len(dims['placement_groups']))
			logger.info('Google get placements...')
			dims['placements'] = get_placements(is_historical)
			logger.info('Google placement count: %s' % len(dims['placements']))
			logger.info('Google get creatives...')
			dims['creatives'] = get_creatives(is_historical)
			logger.info('Google creative count: %s' % len(dims['creatives']))
			is_finished = True
			break
		except Exception as ex:
			logger.exception(ex, 'Google dimensions failure, trying again in 600s...')
			time.sleep(600)
	if is_finished:
		fp = os.path.join(download_path(), 'google_dims_%s.json' % temporal.datetimestamp())
		files.savejson(dims, fp)
		logger.info('Google dimensions downloaded: %s' % fp)
	else:
		logger.warn('Google dimensions failed!')
	logger.info('Google dimensions download finished.')

### End Google DDM Dimensions ###


### Start Google DDM Report Data ###


def get_report(reportId):
	"""Get a DCM report."""
	serv = reporting_service()
	return serv.reports().get(profileId = profileid(), reportId = reportId).execute()


def download_report(reportId, filename, criteria):
	"""Download a DCM report by reportId to a given filename."""
	logger.info('Google report download started: reportId=%s filename=%s.' % (reportId, filename))
	start = time.time()
	NUM_RETRIES = 6
	MAX_TIME = 6*3600
	# Random sleep to allow concurrency, while avoiding freebie api rate limits.
	time.sleep(random.randint(0, 8))
	fileId = None
	#submit a request to DFA to generate a report using report.run. This object contains a fileId used to download the data
	fail_count = 0
	while True:
		try:
			time.sleep(10)
			serv = reporting_service()
			serv.reports().patch(profileId = profileid(), reportId = reportId, body = criteria).execute()
			logger.info('Google: submiting request for %s with reportId=%s.' % (filename, reportId))
			request = serv.reports().run(profileId = profileid(), reportId = reportId).execute()
			fileId = request['id']
			logger.info('Google: report %s for %s generated fileId %s.' % (reportId, filename, fileId))
			break
		except Exception as ex:
			fail_count += 1
			if (fail_count > NUM_RETRIES) or (time.time() - start) > MAX_TIME:
				logger.exception(ex, 'Google: reportId = %s critical request failure.' % reportId)
				raise
			else:
				logger.exception(ex, 'Google: reportId = %s request failure, retrying in 10 sec...' % reportId)
	#periodically check status of report via reports.files.get (using the fileid from report being run)
	fail_count = 0
	outpath = None
	while True:
		try:
			time.sleep(10)
			serv = reporting_service()
			logger.info('Google: Waiting for file output for %s reportId=%s.' % (filename, reportId))
			status = "PROCESSING"
			while status == "PROCESSING":
				request = serv.reports().files().get(fileId = fileId, profileId = profileid(), reportId = reportId).execute()
				status = request['status']
				logger.info('Google download: status=%s reportId=%s.' % (status, reportId))
				time.sleep(60)
				if (time.time() - start) > MAX_TIME:
					msg = 'Google download timeout: status=%s reportId=%s.' % (status, reportId)
					logger.critical(msg)
					raise TimeoutError(msg)
			# once report status is "report available" download using files().get_media()
			if status == "REPORT_AVAILABLE":
				while True:
					logger.info('Google report=%s fileId=%s download started.' % (reportId, fileId))
					time.sleep(30)
					request = serv.files().get_media(reportId = reportId, fileId = fileId)
					logger.info('Google starting report chunk downloads: reportid=%s' % reportId)
					dlpath = download_path()
					outpath = os.path.join(dlpath, filename)
					hidden_outpath = os.path.join(dlpath, '.'+filename) # Download to hidden file (ignored by lander).
					with io.FileIO(hidden_outpath, mode='wb') as fh:
						downloader = googleapiclient.http.MediaIoBaseDownload(fh, request, chunksize = 10**6)
						done = False
						while not done:
							status, done = downloader.next_chunk(num_retries = 6)
							if (time.time() - start) > MAX_TIME:
								msg = 'Google download timeout: status=%s reportId=%s.' % (status, reportId)
								logger.critical(msg)
								raise TimeoutError(msg)
						if status:
							logger.info('Google download progress: %d%%.' % int(status.progress() * 100))
					logger.info('Validating file integrity on %s...' % hidden_outpath)
					lastline = ''
					with open(hidden_outpath, 'rt') as fh:
						for lastline in fh:
							pass
					if lastline.startswith('Grand Total:'):
						os.rename(hidden_outpath, outpath) # File is complete, make visible to lander.
						logger.info('Google: fileId=%s has been written to %s.' % (fileId, outpath))
						break
					else:
						os.remove(hidden_outpath)
						logger.warn('Google: fileId=%s has failed, retrying...' % fileId)
						logger.warn('Last row: ' + lastline)
				break
		except oauth2client.client.AccessTokenRefreshError as ex:
			logger.exception(ex, 'Google: The credentials have been revoked or expired, please re-run the application to re-authorize.')
			raise
		except googleapiclient.errors.HttpError as ex:
			fail_count += 1
			if fail_count > NUM_RETRIES:
				logger.exception(ex, 'Google: reportId = %s critical download failure.' % reportId)
				raise
			logger.exception(ex, 'Google: An HttpError has occurred when downloading Google reportId=%s.' % reportId)
			time.sleep(600)
		except Exception as ex:
			fail_count += 1
			if fail_count > NUM_RETRIES:
				logger.exception(ex, 'Google: reportId = %s critical request failure.' % reportId)
				raise
			logger.exception(ex, 'Google reportId=%s download failed, retrying...' % reportId)
			time.sleep(600)
	return outpath


def download_floodlight_reports(start_date = None, end_date = None):
	"""Download a batch of floodlight action reports."""
	report_id = 30313117
	yesterday = temporal.iso_date_format(temporal.adddays(-1))
	if not start_date:
		start_date = yesterday
	if not end_date:
		end_date = yesterday
	filename_prefix = 'google_floodlight_30313117'
	criteria_type = 'floodlightCriteria'
	criteria = {}
	criteria[criteria_type] = get_report(report_id)[criteria_type]
	for agid in get_advertiser_ids(active = True):
		filename = filename_prefix + '_' + str(agid) + '_' + temporal.datetimestamp() + '.csv'
		criteria[criteria_type]['dateRange']['startDate'] = str(start_date)
		criteria[criteria_type]['dateRange']['endDate'] = str(end_date)
		criteria[criteria_type]['dateRange']['relativeDateRange'] = None
		criteria[criteria_type]['floodlightConfigId']['value'] = agid
		download_report(report_id, filename, criteria)


def download_display_reports(start_date = None, end_date = None):
	"""Download a batch of display reports."""
	report_ids = (42602257, 19477718, 41940084)
	report_names = ('top', 'geo', 'sys')
	fn_prefix = 'google_display%s_%s'
	fn_suffix = '_%s.csv' % temporal.datetimestamp()
	filenames = [(fn_prefix % x + fn_suffix) for x in zip(report_names, report_ids)]
	yesterday = temporal.iso_date_format(temporal.adddays(-1))
	if not start_date:
		start_date = yesterday
	if not end_date:
		end_date = yesterday
	criteria_type = 'criteria'
	for report_id, filename in zip(report_ids, filenames):
		criteria = {}
		criteria[criteria_type] = get_report(report_id)[criteria_type]
		criteria[criteria_type]['dateRange']['startDate'] = str(start_date)
		criteria[criteria_type]['dateRange']['endDate'] = str(end_date)
		criteria[criteria_type]['dateRange']['relativeDateRange'] = None
		download_report(report_id, filename, criteria)

### End Google DDM Report Data ###

### Start Google User Interface Wrapping ###


def report_type_set():
	"""A way to fragment the bulk data pull."""
	return 'ANALYTICS,BIDMANAGER,DISPLAY,FLOODLIGHT,SEARCH,DIMENSION'


def download_batch(start_date = None, end_date = None, report_filter = None):
	"""Assuming we'll start with a single batch of reports which need to be pulled."""
	report_filter = report_filter or report_type_set()
	if 'ANALYTICS' in report_filter:
		#download_analytics_reports(start_date, end_date)
		print('GA not implemented, skipping.')
	if 'DIMENSION' in report_filter:
		download_dimensions(start_date, end_date)
	if 'DISPLAY' in report_filter:
		download_display_reports(start_date, end_date)
	if 'FLOODLIGHT' in report_filter:
		download_floodlight_reports(start_date, end_date)
	if 'SEARCH' in report_filter:
		download_search_reports(start_date, end_date)
	if 'BIDMANAGER' in report_filter:
		download_bidmanager_reports()


def historical_load(start_date = None, end_date = None, time_block_size = None, report_filter = None):
	"""Load historical data."""
	report_filter = report_filter or report_type_set()
	start_date = start_date or '2014-01-01'
	start_date = str(start_date)
	end_date = end_date or start_date
	end_date = str(end_date)
	time_block_size = time_block_size or 1
	time_block_size = int(float(time_block_size))
	yesterday = temporal.adddays(-1)
	start_date = temporal.str2date(start_date) if type(start_date) == str else start_date
	end_date = temporal.str2date(end_date) if type(end_date) == str else end_date
	params = (start_date, end_date, time_block_size, report_filter)
	print('Google historical load: start_date = %s, end_date = %s, time_block_size = %s, report_filter = %s' % params)
	rstart_date = start_date
	rend_date = temporal.adddays(time_block_size - 1, rstart_date)
	if 'DIMENSION' in report_filter:
		download_batch(rstart_date, rend_date, 'DIMENSION') # Only need a single pull of dimensions.
		report_filter = report_filter.replace('DIMENSION', '')
	while rstart_date <= end_date:
		download_batch(rstart_date, rend_date, report_filter)
		rstart_date = temporal.adddays(1, rend_date)
		rend_date = temporal.adddays(time_block_size - 1, rstart_date)
	if rstart_date < rend_date:
		download_batch(rstart_date, rend_date, report_filter)


def generate_token(api_scope):
	"""Generate a token for an api scope."""
	google_service(api_scope)


def run(report_filter = None):
	"""Wrapper to run the daily download."""
	try:
		logger.info('Google download started.')
		download_batch(report_filter = report_filter)
		logger.info('Google download finished.')
	except Exception as ex:
		logger.exception(ex, 'Google download failed.')


def main():
	desc = """TheGoods-Collector-Google"""
	ap = argparse.ArgumentParser(add_help = True, description = desc)
	dhelp = 'Collect daily Google data.'
	ap.add_argument('-d', '--daily_load', action = 'store_true', default = True, help = dhelp)
	ghelp = 'Generate 3-Leg Oauth2 Tokens For Reporting & Trafficking.'
	ap.add_argument('-g', '--generate_token', action = 'store_true', default = False, help = ghelp)
	lhelp = 'Historical load.'
	ap.add_argument('-l', '--historical_load', action = 'store_true', default = False, help = lhelp)
	shelp = 'Historical load start date.'
	ap.add_argument('-s', '--start_date', help = shelp)
	ehelp = 'Historical load end date.'
	ap.add_argument('-e', '--end_date', help = ehelp)
	thelp = 'Historical load chunk size in days.'
	ap.add_argument('-t', '--time_block_size', help = thelp)
	fhelp = 'Include: %s'%report_type_set()
	ap.add_argument('-f', '--report_filter', help = fhelp)
	ahelp = 'Use with -g. Generate token for this scope. \n\t%s' % SCOPES
	ap.add_argument('-a', '--api_scope', help = ahelp)
	args = ap.parse_args()
	logger.info('TheGoods-Collector-Google started.')
	if args.generate_token:
		generate_token(args.api_scope)
	elif args.historical_load:
		historical_load(start_date = args.start_date, end_date = args.end_date, time_block_size = args.time_block_size, report_filter = args.report_filter)
	elif args.daily_load and not args.historical_load:
		run(report_filter = args.report_filter)
	logger.info('TheGoods-Collector-Google finished.')

if __name__ == '__main__':
	main()

### End Google User Interface Wrapping ###
