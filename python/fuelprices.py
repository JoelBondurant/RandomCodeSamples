import os
import json
import requests
import datetime
import xml.etree.ElementTree as ET
from analyticobjects.util import temporal
from analyticobjects.util import logger



def fetch_fuel_data():
	"""Get basic fuel price data."""
	return requests.get('http://www.fueleconomy.gov/ws/rest/fuelprices').text


def parse_fuel_data(xml_response):
	"""Parse XML response into json."""
	root = ET.fromstring(xml_response)
	vals = {'datebin': str(datetime.datetime.now().date())}
	for child in root:
		vals[child.tag] = float(child.text)
	return json.dumps(vals)


def write_fuel_data():
	"""Persist fuel data."""
	fuel_data = fetch_fuel_data()
	fuel_json = parse_fuel_data(fuel_data)
	ts = temporal.datetimestamp()
	base_dir = '/dataVol/collector/json'
	if not os.path.exists(base_dir):
		os.makedirs(base_dir)
	fp = os.path.join(base_dir, 'fuel_data_' + ts + '.json')
	with open(fp, 'w') as fout:
		fout.write(fuel_json)
	logger.info('Fuel prices downloaded: %s' % fp)


def run():
	"""Extra layers of abstraction."""
	write_fuel_data()


