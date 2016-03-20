#!/usr/bin/env python
"""
A connector to MediaOcean.
"""

import os, sys, time, gzip, datetime
import subprocess, paramiko
import analyticobjects.util.logger as logger

DEFAULT_ENV = 'DEV'
PROD_ENV = 'PROD'

def get_env():
	return os.getenv('ENV_NAME', DEFAULT_ENV)

def hostname():
	return os.getenv('MEDIAOCEAN_SFTP_HOST', 'mbftp.mbxg.com')

def port():
	return int(os.getenv('MEDIAOCEAN_SFTP_PORT', 22))

def username():
	return os.getenv('MEDIAOCEAN_SFTP_USER')

def password():
	return os.getenv('MEDIAOCEAN_SFTP_PASS')

def connect():
	transport = paramiko.Transport((hostname(), port()))
	transport.connect(username = username(), password = password())
	sftp = paramiko.SFTPClient.from_transport(transport)
	return (transport, sftp)


def download(dryrun = False):
	transport, sftp = connect()
	DL_PATH = '/dataVol/collector/mediaocean'
	if not os.path.exists(DL_PATH):
		os.makedirs(DL_PATH)
	subpaths = ('', 'bulk_api') # Spectra/Offline & Prisma/Online
	for subpath in subpaths:
		filenames = sftp.listdir(subpath)
		try:
			filenames.remove('bulk_api')
		except:
			pass
		for fn in filenames:
			localPath = os.path.join(DL_PATH, fn)
			remotePath = os.path.join(subpath, fn)
			logger.info('Download started: %s' % fn)
			if not dryrun:
				if fn.startswith('extract-status'):
					sftp.remove(remotePath)
				else:
					sftp.get(remotePath, localPath)
					if get_env() == PROD_ENV:
						sftp.remove(remotePath)
			logger.info('Download complete: %s' % fn)
	sftp.close()
	transport.close()


def run(dryrun = False):
	logger.info('MediaOcean download started.')
	try:
		download(dryrun)
	except Exception as ex:
		logger.exception(ex, 'MediaOcean download failed.')
	logger.info('MediaOcean download finished.')


if __name__ == '__main__':
	run()


