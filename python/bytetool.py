"""
Module for byte operations.
"""
import hashlib
import datetime

def sizeof_fmt(num, dec = 3, kibibyte = False):
	"""Byte size formatting utility function."""
	prefixes = None
	factor = None
	if kibibyte:
		factor = 1024.0
		prefix = ['bytes','KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB']
	else:
		factor = 1000.0
		prefix = ['bytes','KB','MB','GB','TB','PB','EB','ZB','YB']
	for x in prefix:
		if num < factor:
			return ("%3."+str(dec)+"f %s") % (num, x)
		num /= factor


def to_ascii(text):
	"""Convert text to ascii."""
	asciiText = ''.join([ch if ord(ch) < 128 else ' ' for ch in text])
	return asciiText


def hex_hash(astring, length = 6):
	"""Compute a hex string hash for a string."""
	hasher = hashlib.md5()
	hasher.update(astring.encode('utf-8'))
	hash_raw = hasher.hexdigest()
	return hash_raw[:length].upper()


def string_shorten(astring, preserve_header = 6, max_length = 35):
	"""Long string shortener."""
	if len(astring) <= max_length:
		return astring
	astring_lower = astring.lower()
	astring2 = astring[:preserve_header] + '_DX' + hex_hash(astring)
	astring2 += '_' + datetime.datetime.now().date().strftime('%Y%m%d')
	if len(astring2) > max_length:
		raise Exception('Illegal string length in %s.' % astring2)
	return astring2

