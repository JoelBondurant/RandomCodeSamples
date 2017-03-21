"""
A connector to communicate with AWS.
"""
import os, time, uuid
import paramiko, json
import boto3
import subprocess as sp
from bssp.util import logger
from bssp.util import files

MOCK = False
SETTING_NAME = 'AWS'
ADVERTISER_CODE = '<<ADVERTISER_SHORT_NAME>>'
DEFAULT_ENV = 'DEV'
PROD_ENV = 'PROD'


def get_env():
	return os.getenv('ENV_NAME', DEFAULT_ENV)

def mock():
	global MOCK
	MOCK = True

if get_env() != PROD_ENV:
	mock()

def zonename():
	return os.getenv('AWS_ZONE_NAME', 'us-west-1')

def accesskey():
	return os.getenv('AWS_ACCESS_KEY_ID', 'notset')

def secretkey():
	return os.getenv('AWS_SECRET_ACCESS_KEY', 'notset')

def keyname():
	return os.getenv('AWS_EC2_KEY_NAME', 'notset')

def sshkeyfile():
	return os.getenv('AWS_SSH_KEY_FILE', 'notset')

def hadoopuser():
	return os.getenv('AWS_HADOOP_USER', 'notset')

def instancetype():
	return os.getenv('AWS_EMR_INSTANCE_TYPE', 'm3.xlarge')

def instancecount():
	return os.getenv('AWS_EMR_INSTANCE_COUNT', 1)

def releaselabel():
	return os.getenv('AWS_EMR_RELEASE_LABEL', 'emr-4.6.0')

def mockpath(bucketname = 'aiobj', keyname = ''):
	fulldir = os.path.join('/datavol/aiobj', bucketname, keyname)
	if os.path.isdir(fulldir):
		if not os.path.exists(fulldir):
			try:
				os.makedirs(fulldir)
			except:
				pass
	else:
		if not os.path.exists(os.path.dirname(fulldir)):
			try:
				os.makedirs(os.path.dirname(fulldir))
			except:
				pass
	return fulldir


def string_upload(strdata, bucketname, keyname):
	"""Upload a string to s3."""
	if MOCK:
		logger.info('MOCK AWS S3 string upload to: ' + bucketname + '/' + keyname)
		with open(mockpath(bucketname, keyname), 'w') as fout:
			fout.write(strdata)
			return
	logger.info('AWS S3 string upload to: ' + bucketname + '/' + keyname)
	boto3.resource('s3').Bucket(bucketname).put_object(Key = keyname, Body = strdata)


def file_upload(filepath, bucketname, keypath):
	"""Upload a file to s3 using boto."""
	filename = os.path.basename(filepath)
	if MOCK:
		logger.info('MOCK AWS S3 file upload: ' + filepath + ' to: ' + bucketname)
		files.copy(filepath, os.path.join(mockpath(bucketname, keypath), filename))
		return
	keyname = os.path.join(keypath, filename)
	logger.info('AWS S3 file upload: ' + filepath + ' to: ' + os.path.join(bucketname, keyname))
	boto3.resource('s3').Bucket(bucketname).upload_file(filepath, keyname)


def emrstatus(jobid):
	"""Get the status of an EMR job."""
	status = boto3.client('emr').describe_cluster(ClusterId = jobid)['Cluster']
	return status

def emrstate(jobid):
	"""Get the state of an EMR job."""
	return emrstatus(jobid)['Status']['State']

def emrmasterdns(jobid):
	"""Get the master node dn of an EMR job."""
	return emrstatus(jobid)['MasterPublicDnsName']

def emrssh(jobid):
	"""SSH connect to master EMR node."""
	hostname = emrmasterdns(jobid)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname = hostname, username = hadoopuser(), key_filename = sshkeyfile(), timeout = 30)
	return ssh

def spark_cluster(instance_count = None, instance_type = None):
	"""Start up an EMR Spark cluster."""
	awscmd = 'aws emr create-cluster --name "SparkCluster" --release-label %s '
	awscmd += '--applications Name=Spark --ec2-attributes KeyName=%s --instance-type %s '
	awscmd += '--instance-count %s --use-default-roles '
	instance_type = instance_type or instancetype()
	instance_count = instance_count or instancecount()
	awscmd = awscmd % (releaselabel(), keyname(), instance_type, instance_count)
	resp = sp.check_output(awscmd, stderr = sp.STDOUT, shell = True)
	jobid = json.loads(resp.decode('utf-8'))['ClusterId']
	return jobid

def spark_execute(sparktxt, jobid):
	"""Execute a Spark script on EMR."""
	scriptname = str(uuid.uuid4()) + '.scala'
	string_upload(sparktxt, 'aiobj-code', scriptname)
	started = time.time()
	while True:
		time.sleep(10)
		state = emrstate(jobid)
		if state == 'WAITING':
			break
		if state == 'FAILED' or (time.time() - started) > 600:
			raise Exception('AWS Spark Job %s Failed!' % jobid)
	ssh = emrssh(jobid)
	ssh.exec_command('sudo nohup shutdown -h 54 &')
	ssh.exec_command('aws s3 cp s3://aiobj-code/%s .' % scriptname)
	ssh.exec_command('spark-shell -i %s' % scriptname)
	ssh.close()

def spark_run(sparktxt):
	"""Run Spark code on EMR"""
	jobid = spark_cluster()
	spark_execute(sparktxt, jobid)
	return jobid


