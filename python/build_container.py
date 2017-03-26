#!/usr/bin/env python3

import subprocess as sp
import argparse
import random


CONTAINER_NAME = 'replaceme'
container_name = CONTAINER_NAME.lower()


desc = """%s Build Application:  
Builds %s docker container.""" % (CONTAINER_NAME, container_name)
argparser = argparse.ArgumentParser(description = desc, add_help = True)
argparser.add_argument('-c', '--clean', action = 'store_true', default = False, help = 'Clean build.')
argparser.add_argument('-b', '--break_cache', action = 'store_true', default = False, help = 'Break cache.')
argparser.add_argument('-n', '--no_cache', action = 'store_true', default = False, help = 'No cache.')
args = argparser.parse_args()


print('%s build started.' % CONTAINER_NAME)
if args.clean:
	print('%s clean-up...' % CONTAINER_NAME)
	sp.call(['docker', 'stop', container_name])
	sp.call(['docker', 'rm', container_name])
	sp.call(['docker', 'rmi', container_name])
if args.break_cache:
	with open('src/.breakcache', 'w') as fout:
		fout.write(str(random.randint(0, 10**10)))
else:
	sp.call(['touch', '.breakcache'])
build_args = ['docker', 'build', '--tag=%s' % container_name]
if args.no_cache:
	build_args += ['--no-cache=true']
sp.call(build_args + ['.'])
print('%s complete.' % CONTAINER_NAME)

