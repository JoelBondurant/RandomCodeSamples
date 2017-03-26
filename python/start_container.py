#!/usr/bin/env python3
import subprocess, getpass, argparse, os, sys

CONTAINER_NAME = 'replaceme'
container_name = CONTAINER_NAME.lower()

# Start-up Helper functions:
def src_paths(src_path = './src'):
	return [(os.path.abspath(os.path.join(src_path, x)), x) \
				 for x in os.listdir(src_path) \
				 if os.path.isdir(os.path.join(src_path, x))]


# Main Functional Entry Point:
def main():
	desc = """%s service manager.""" % CONTAINER_NAME
	argparser = argparse.ArgumentParser(add_help = True, description = desc)
	argparser.add_argument('-b', '--bash', action = 'store_true', default = False, help = 'Start with bash.')
	argparser.add_argument('-c', '--clean', action = 'store_true', default = False, help = 'Clean process start.')
	argparser.add_argument('-d', '--dev', action = 'store_true', default = False, help = 'Developer mode.')
	argparser.add_argument('-e', '--echo', action = 'store_true', default = False, help = 'Echo start command.')
	argparser.add_argument('-n', '--new', action = 'store_true', default = True, help = 'New process run.')
	argparser.add_argument('-p', '--prompt', action = 'store_true', default = False, help = 'Prompt for secrets.')
	argparser.add_argument('-r', '--restart', action = 'store_true', default = False, help = 'Restart process.')
	argparser.add_argument('-s', '--stop', action = 'store_true', default = False, help = 'Stop process.')
	args = argparser.parse_args()
	# RESTART:
	if args.restart:
		print('%s restarting...' % CONTAINER_NAME)
		subprocess.call(['docker', 'restart', container_name])
		sys.exit(0)
	# CLEAN-UP:
	if args.clean or args.stop:
		print('%s stopping...' % CONTAINER_NAME)
		subprocess.call(['docker', 'stop', container_name])
		if args.clean:
			print('%s process removal...' % CONTAINER_NAME)
			subprocess.call(['docker', 'rm', container_name])
		if args.stop:
			sys.exit(0)
	# DYNAMIC-DATA-INJECTION:

	# START-UP:
	print('%s starting...' % CONTAINER_NAME)
	if args.new:
		startCmd = 'docker run '
		startCmd += '--name=%s ' % container_name
		startCmd += '-h %s ' % container_name
		startCmd += '--restart=always '
		startCmd += '--privileged=true '
		if args.dev:
			for src_path in src_paths():
				if not 'config' in src_path: # Skip config remapping.
					startCmd += '-v %s:/usr/local/'+CONTAINER_NAME+'/%s ' % src_path
		startCmd += '-v /var/log/'+CONTAINER_NAME+':/var/log/'+CONTAINER_NAME
		if args.bash:
			startCmd += '-it '
		else:
			startCmd += '-d '
		startCmd += container_name
		if args.bash:
			startCmd += ' bash'
		else:
			startCmd += ' python '+container_name+'.py'
		if args.echo:
			print('Start cmd:\n' + startCmd)
		subprocess.call(startCmd, shell = True)
		print('%s started.' % CONTAINER_NAME)
	else:
		subprocess.call(['docker','start',container_name])
		print('%s (re)started.' % CONTAINER_NAME)

if __name__ == '__main__':
	main()

