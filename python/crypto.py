#!/usr/bin/env python
import os, argparse, getpass
import subprocess as sp

POSTFIX = '.aes256'

def encrypted_name(apath):
	"""Adds .aes256 to the filename."""
	return apath + POSTFIX

def decrypted_name(apath):
	"""Removes .aes256 from the filename."""
	return apath.replace(POSTFIX,'')

def encrypt(apath, akey):
	"""Call openssl to aes-256-cbc a file with the supplied symmetric key."""
	sp.call(['openssl', 'enc', '-aes-256-cbc', '-in', apath, '-out', encrypted_name(apath), '-k', akey])

def decrypt(apath, akey):
	"""Call openssl to un aes-256-cbc a file with the supplied symmetric key."""
	sp.call(['openssl', 'enc', '-d', '-aes-256-cbc', '-in', apath, '-out', decrypted_name(apath), '-k', akey])

def remove(apath):
	"""os.remove(the path and it's encrypted version)"""
	try:
		os.remove(apath)
	except:
		pass
	try:
		os.remove(encrypted_name(apath))
	except:
		pass

def main():
	"""Command line encryption/decryption tool. A thin wrapper to openssl."""
	desc = 'Simple OpenSSL encryption wrapper.'
	argparser = argparse.ArgumentParser(add_help = True, description = desc)
	argparser.add_argument('-e', '--encrypt', type = str, help = 'Encrypt a file.')
	argparser.add_argument('-d', '--decrypt', type = str, help = 'Decrypt a file.')
	args = argparser.parse_args()
	akey = getpass.getpass()
	if args.encrypt and len(args.encrypt) > 0:
		encrypt(args.encrypt, akey)
		print('Encryption complete.')
	elif args.decrypt and len(args.decrypt) > 0:
		decrypt(args.decrypt, akey)
		print('Decryption complete.')
	else:
		print('Please enter a valid filename.')


if __name__ == '__main__':
	main()

