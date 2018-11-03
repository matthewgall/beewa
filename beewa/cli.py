#!/usr/bin/env python3

import os, sys, argparse, logging
from beewa import Beewa

def main():

	parser = argparse.ArgumentParser()

	# hivehome.com credentials
	parser.add_argument("--username", help="hivehome.com username", default=os.getenv("HIVE_USERNAME", ''))
	parser.add_argument("--password", help="hivehome.com password", default=os.getenv("HIVE_PASSWORD", ''))

	# light groups path
	parser.add_argument("--groups", help="file defining light groups", default='groups.json')
	
	# commands
	parser.add_argument("command", nargs="*", help='command to pass to hive')

	# verbose mode
	parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	try:
		assert args.username != ''
		assert args.password != ''
	except AssertionError:
		exit("Missing hivehome.com username or password. Exiting")
	
	if len(args.command) == 0:
		exit(parser.print_help())

	hive = Beewa(args.username, args.password)
	try:
		method = False
		method = getattr(hive, args.command[0])
		try:
			method(args.command[1:], args)
		except SystemError as e:
			exit(e.message)
	except AttributeError:
		exit('{} is not a supported action'.format(args.command[0]))
	if not method:
		exit('{} is not a supported action'.format(args.command[0]))

if __name__ == '__main__':
	main()