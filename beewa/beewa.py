#!/usr/bin/env python3

import os, sys, argparse, logging
import requests
from hive import Hive

class Beewa:

	def __init__(self, username, password):
		# instantiation of Hive
		self.hive = Hive(username, password)

		# and login
		self.hive.login()

	def list(self, params=''):
		# now for a list of devices
		data = self.hive.list()
		for device in data:
			if not device['name'].startswith(("http://", "Fake")):
				if self.hive._classify(device) in ['bulb']:
					print("{}: {} (presence: {}, state: {})".format(
						device['id'],
						device['name'],
						device['attributes']['presence']['displayValue'],
						device['attributes']['state']['displayValue']
					))
				else:
					print("{}: {}".format(
						device['id'],
						device['name']
					))

	def info(self, params=''):
		# Now for a list of devices
		try:
			data = self.hive.info(params)

			for value in data:
				if value in ['id', 'name']:
					print("{}: {}".format(value, data[value]))
				elif value in ['attributes']:
					data = data[value]
					for value in data:
						if value in ['state', 'presence', 'brightness']:
							print("{}: {}".format(
								value,
								str(data[value]['displayValue']).lower()
							))
		except:
			exit("Unable to get information about device: {}".format(params[0]))

	def on(self, params=''):
		# Now for a list of devices
		try:
			if self.hive.on(params):
				print("{} is now on".format(params[0]))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def off(self, params=''):
		# Now for a list of devices
		try:
			if self.hive.off(params):
				print("{} is now off".format(params[0]))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def brightness(self, params=''):
		# Now for a list of devices
		try:
			if self.hive.brightness(params):
				print("Set brightness of {} to {}%".format(
					params[0],
					params[1]
				))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

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
		method(args.command[1:])
	except AttributeError:
		exit('{} is not a supported action'.format(args.command[0]))
	if not method:
		exit('{} is not a supported action'.format(args.command[0]))

if __name__ == '__main__':
	main()