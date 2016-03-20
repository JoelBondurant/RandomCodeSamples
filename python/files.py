"""
A wrapper module for common file handling.
Created: 2014-03-19
"""
import os, sys, re, shutil, hashlib, fnmatch, zipfile, gzip, uuid, json, csv
import subprocess as sp
from datetime import datetime
from tabulate import tabulate
from analyticobjects.util import temporal


def csv2json(csvfp):
	"""Transform a csv file into json."""
	if not (csvfp.endswith('.csv') or csvfp.endswith('.tsv')):
		raise ValueError('Not a valid csv/tsv path.')
	if csvfp.endswith('.csv'):
		delimiter = ','
	elif csvfp.endswith('.tsv'):
		delimiter = '\t'
	jsonfp = csvfp[:-4] + '.json'
	with open(csvfp, 'r') as csvin:
		rows = []
		csvreader = csv.DictReader(csvin, delimiter = delimiter)
		for row in csvreader:
			if csvreader.line_num == 1:
				continue
			rows.append(row)
	savejson(rows, jsonfp)


def loadjson(fp):
	"""Convenience wrapper to load json data."""
	with open(fp, 'r') as fin:
		dat = json.load(fin)
	return dat


def savejson(obj, fp, **kw):
	"""Convenience wrapper to save json data."""
	skipkeys = kw.get('skipkeys', False)
	ensure_ascii = kw.get('ensure_ascii', True)
	check_circular = kw.get('check_circular', True)
	allow_nan = kw.get('allow_nan', True)
	cls = kw.get('cls', None)
	indent = kw.get('indent', '\t')
	separators = kw.get('separators', (',', ':'))
	default = kw.get('default', None)
	sort_keys = kw.get('sort_keys', True)
	with open(fp, 'w') as fout:
		json.dump(obj, fout, skipkeys = skipkeys, ensure_ascii = ensure_ascii, check_circular = check_circular,
			allow_nan = allow_nan, cls = cls, indent = indent, separators = separators, sort_keys = sort_keys, **kw)


def sizeinbytes(file_path):
	"""Convenience access to os.path.getsize."""
	return os.path.getsize(file_path)


def joinpaths(*paths):
	"""Convenience access to os.path.join."""
	return os.path.join(*paths)


def delete(file_path):
	"""os.remove."""
	os.remove(file_path)


def safedelete(file_path):
	"""os.remove wrapped in minimal exception handling."""
	try:
		os.remove(file_path)
	except Exception as ex:
		print('Exception: ' + str(sys.exc_info()[0]))
		print(ex)


def listdirs(directory = '.', dirname_regex = '.+'):
	"""A utility function to list directories in a directory."""
	dirnames = []
	rawnames = os.listdir(directory)
	for rawname in rawnames:
		matchobj = re.search(dirname_regex, rawname)
		if matchobj is None:
			continue
		fullpath = os.path.join(directory, rawname)
		if os.path.isdir(fullpath):
			dirnames.append(rawname)
	return dirnames


def listfiles(directory = '.', filename_regex = r'.+'):
	"""A utility function to list files in a directory."""
	filenames = []
	rawfilenames = os.listdir(directory)
	for filename in rawfilenames:
		matchobj = re.search(filename_regex, filename)
		if matchobj is None:
			continue
		fullpath = os.path.join(directory, filename)
		if os.path.isfile(fullpath):
			filenames.append(filename)
	return filenames


def safelistfiles(directory = '.', filename_regex = r'.+'):
	"""Same as listfiles, but returns [] rather than throwing an exception."""
	filenames = []
	try:
		filenames = listfiles(directory, filename_regex)
	except Exception as ex:
		print('Exception: ' + str(sys.exc_info()[0]))
		print(ex)
	return filenames


def hexhash(file_path, num_bytes = 32, block_size = 65536):
	"""Compute a hex string hash for a file."""
	hasher = hashlib.sha256()
	hd = ''
	with open(file_path, 'rb') as fs:
		buf = fs.read(block_size)
		while len(buf) > 0:
			hasher.update(buf)
			buf = fs.read(block_size)
		hd = hasher.hexdigest()
	return hd[:num_bytes]


def safehexhash(file_path):
	"""Same as hexhash, but doesn't throw exceptions, but rather returns 'NULL'."""
	hashval = 'NULL'
	try:
		hashval = hexhash(file_path)
	except Exception as ex:
		print('Exception: ' + str(sys.exc_info()[0]))
		print(ex)
	return hashval


def copy(src, dst):
	"""A utility function to copy a file with verification."""
	src_hash = hexhash(src)
	dst_path = os.path.expanduser(dst)
	if os.path.isdir(dst_path):
		dst_path = os.path.join(dst_path, os.path.basename(src))
	makedirs(dst_path)
	print('Copying file %s to %s.' % (src, dst_path))
	shutil.copy2(src, dst_path)
	dst_hash = hexhash(dst_path)	
	if src_hash != dst_hash:
		raise Exception('File move verification failed. Source and destination do not match.')
	else:
		print('File %s copy verified successfully.' % dst_path)


def move(src, dst):
	"""A utility function to move a file with verification."""
	src_hash = hexhash(src)
	dst_path = os.path.expanduser(dst)
	if os.path.isdir(dst_path):
		dst_path = os.path.join(dst_path, os.path.basename(src))
	makedirs(dst_path)
	print('Moving file %s to %s.' % (src, dst_path))
	shutil.copy2(src, dst_path)
	dst_hash = hexhash(dst_path)	
	if src_hash != dst_hash:
		raise Exception('File move verification failed. Source and destination do not match.')
	else:
		os.remove(src)


def copyall(src, dst, filename_regex = r'.+'):
	"""A utility to copy a directory of files with verification."""
	dir_name = os.path.dirname(src)
	src_files = listfiles(src, filename_regex = filename_regex)
	for src_file in src_files:
		copy(os.path.join(dir_name, src_file), dst)


def moveall(src, dst, filename_regex = r'.+'):
	"""A utility to move a directory of files with verification."""
	dir_name = os.path.dirname(src)
	src_files = listfiles(src, filename_regex = filename_regex)
	for src_file in src_files:
		move(os.path.join(dir_name, src_file), dst)


def reverse_moveall(dst, src):
	"""A utility to move a directory of files with verification using reverse order params."""
	moveall(src, dst)


def flattento(src, dst):
	"""A utility to copy all files in a path branch to a single branch."""
	print('Flattening %s to %s.' % (src, dst))
	for root, dirnames, filenames in os.walk(src):
		for fn in filenames:
			src_path = os.path.join(root, fn)
			copy(src_path, dst)


def countfiles(src_path = '.'):
	"""Count the number of files in a path branch recursively."""
	cnt = 0
	for root, dirnames, filenames in os.walk(src_path):
		cnt += len(filenames)
	print('File count = %s in %s.' % (cnt, src_path))
	return cnt


def createdate(file_path):
	"""Returns the create date for the specified file path."""
	return datetime.fromtimestamp(os.path.getctime(file_path))


def unzip(src_path, dst_path = None):
	"""Extracts a zipfile. Defaults extraction to the same path. Returns filename list."""
	dst_pathmod = dst_path
	if dst_path is None:
		dst_pathmod = os.path.dirname(src_path)
	with zipfile.ZipFile(src_path) as zf:
		nmlist = zf.namelist()
		zf.extractall(dst_pathmod)
	return nmlist


def ungz(src_path, keep = True):
	"""Extracts a gzipped file. Defaults extraction to the same path. Returns filename list."""
	cmd = ['gzip', '--decompress']
	if keep:
		cmd.append('--keep')
	cmd.append(src_path)
	sp.call(cmd)
	return os.path.abspath(src_path.replace('.gz', ''))


def compress_gz(src_path, keep = True, fast = True):
	"""Compress to a gzipped file. Defaults extraction to the same path. Returns filename list."""
	cmd = ['gzip', '--no-name']
	if keep:
		cmd.append('--keep')
	if fast:
		cmd.append('--fast')
	cmd.append(src_path)
	sp.call(cmd)
	return os.path.abspath(src_path + '.gz')


def unlz4(src_path, dst_path = None):
	"""Extracts an LZ4 compressed file. Defaults extraction to the same path. Returns filename list."""
	dst_pathmod = dst_path
	if dst_path is None:
		dst_pathmod = src_path.replace('.lz4','')
	sp.call(['lz4', '-d', src_path, dst_pathmod])
	return os.path.abspath(dst_pathmod)


def compress_lz4(src_path, dst_path = None):
	"""LZ4 compress a file. Defaults extraction to the same path. Returns filename list."""
	dst_pathmod = dst_path
	if dst_path is None:
		dst_pathmod = src_path + '.lz4'
	sp.call(['lz4', src_path, dst_pathmod])
	return os.path.abspath(dst_pathmod)


def randhex(nchars = 16):
	"""Utility method to return a string of random hex characters, useful for temporary file names."""
	rhx = ''
	while len(rhx) < nchars:
		rhx += uuid.uuid4().get_hex()
	return rhx[0:nchars]


def pwd():
	"""Returns the current working directory."""
	return os.getcwd()


def cd(directory):
	"""Change the working directory to a specified path."""
	os.chdir(directory)


def count(directory = '.', filename_regex = '.*'):
	"""Count the number of files in a path with regex support"""
	return len(listfiles(directory, filename_regex))


def delete(filename_regex = '.*', directory = '.'):
	"""Utility method to delete all files in a path (default = '.') by filename regex (default = '.*')."""
	fns = listfiles(directory, filename_regex)
	for fn in fns:
		ffp = os.path.join(directory, fn)
		print('deleting file: %s' % ffp)
		os.remove(ffp)
	print('%s files deleted.' % len(fns))

def trimrows(infilename, rows_to_trim):
	"""Trim rows from a text file. Use negative row indexes to trim from end of file.
	
		e.g. 
		trimrows('a.txt', 'b.txt', [1,2,3,7,-1])
		Trims rows 1, 2, 3, 7, and the last row of a.txt into b.txt.

		Keyword arguments:
		infilename -- the input file to trim rows from.
		rows_to_trim -- a list of row numbers to trim, with negatives relative to end of file.
	"""
	outfilename = infilename + '.out'
	with open(infilename, 'rt') as infile:
		nrows = 0
		for inrow in infile:
			nrows += 1
		infile.seek(0)
		for idx in range(len(rows_to_trim)):
			if rows_to_trim[idx] < 0:
				rows_to_trim[idx] += (nrows + 1)
		with open(outfilename, 'wt') as outfile:
			inrownum = 0
			for inrow in infile:
				inrownum += 1
				if not inrownum in rows_to_trim:
					outfile.write(inrow)
	os.remove(infilename)	
	os.rename(outfilename, infilename)

"""
Print files in path.
"""
def ls(apath = '.'):
	fns = os.listdir(apath)
	header = ['Type','FileName','SizeInBytes','Created']
	nf = 0
	nd = 0
	rows = []
	drows = []
	frows = []
	for fn in fns:
		filepath = os.path.join(apath, fn)
		ifile = os.path.isfile(filepath)
		row = []
		if ifile:
			nf += 1
			row.append('/F>')
		else:
			nd += 1
			row.append('/D>')
		row.append(fn)
		row.append(str(sizeinbytes(filepath)))
		row.append(temporal.iso_datetime_format(createdate(filepath)))
		if ifile:
			frows.append(row)
		else:
			drows.append(row)
		rows = drows + frows
	prettyprint(rows, header)
	print('Count: %s\tDirectories: %s\tFiles: %s' % (len(rows), nd, nf))



def prettyprint(rows, header = None, tablefmt = 'grid'):
	"""
	Function for pretty printing lists of tuples to the terminal.
	"""
	if header is None:
		header = ['']*len(rows[0])
	print(tabulate(rows, header, tablefmt))


def read(filepath):
	""" 
	Read the entire text contents from a file into a string.
	"""
	fc = ''
	with open(filepath, 'rt') as fin:
		fc = fin.read()
	return fc


def filter_rows(src_path, regex):
	"""
	Parse a text file line by line, emmitting rows to a new file filename.filter which match a supplied regex.
	"""
	matcher = re.compile(regex, re.IGNORECASE)
	with open(src_path, 'rt') as fin:
		with open(src_path + '.filtered', 'wt') as fout:
			for row in fin:
				if matcher.match(row):
					fout.write(row)


def head(src_path, nrows = 10):
	"""
	Print the first nrows=10 rows of a text file to standard out.
	"""
	mrows = 0
	with open(src_path, 'rt') as fin:
		for row in fin:
			if mrows >= nrows:
				break
			sys.stdout.write(row)
			mrows += 1


def write(astring, filepath):
	"""Write a string to a filepath"""
	with open(filepath, 'wt') as fout:
		fout.write(astring)


def makedirs(filepath):
	"""Make parent directories for a file path if they don't exist."""
	pardir = os.path.dirname(filepath)
	if not os.path.exists(pardir):
		os.makedirs(pardir)



