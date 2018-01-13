#!/usr/bin/env python3

import os, sys, argparse, logging
import requests

class Beewa:

	def __init__(self, username, password):
		self.baseURI = 'https://api-prod.bgchprod.info/omnia'
		self.headers = {
			'Content-Type': 'application/vnd.alertme.zoo-6.1+json',
			'Accept': 'application/vnd.alertme.zoo-6.1+json',
			'X-Omnia-Client': 'Hive Web Dashboard'
		}

		# Set a temporary store for username and password data
		self.username = username
		self.password = password

		# And attempt a login
		self.login()

	def _classify(self, data):
		if 'motion.sensor.json' in data['nodeType']:
			return "motion_sensor"
		if 'node.class.light.json' in data['nodeType']:
			return 'bulb'
		if 'node.class.hub.json' in data['nodeType']:
			return 'hub'
		return None

	def login(self, params=''):
		# Now we attempt a login
		payload = {
			"sessions": [{
				"username": self.username,
				"password": self.password,
				"caller": "WEB"
			}]
		}
		try:
			data = requests.post(
				"{}/auth/sessions".format(self.baseURI),
				headers=self.headers,
				json=payload
			).json()
			# Now we save the session id
			self.session_id = data['sessions'][0]['id']
			# And append the needed header to self.headers
			self.headers['X-Omnia-Access-Token'] = self.session_id
			# Blank the username and password
			self.username = ''
			self.password = ''

			return True
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def list(self, params=''):
		# Now for a list of devices
		data = requests.get(
			"{}/nodes".format(self.baseURI),
			headers=self.headers
		).json()['nodes']
		
		try:
			for device in data:
				if not device['name'].startswith(("http://", "Fake")):
					if self._classify(device) in ['bulb']:
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
		except:
			exit("We encountered an error listing your devices")

	def info(self, params=''):
		# Now for a list of devices
		try:
			data = requests.get(
				"{}/nodes/{}".format(self.baseURI, params[0]),
				headers=self.headers
			).json()['nodes'][0]

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
			exit("Unable to login to Hive at this time. Exiting.")

	def on(self, params=''):
		# Now for a list of devices
		try:
			payload = {
				"nodes":[{
					"attributes": {
						"state": {"targetValue": "ON"},
						"brightness": { "targetValue":100 }
					}
				}]
			}

			data = requests.put(
				"{}/nodes/{}".format(self.baseURI, params[0]),
				headers=self.headers,
				json=payload
			).json()['nodes'][0]
			print("{} is now on".format(data['name']))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def off(self, params=''):
		# Now for a list of devices
		try:
			payload = {
				"nodes":[{
					"attributes": {
						"state": {"targetValue": "OFF"},
						"brightness": { "targetValue": 0 }
					}
				}]
			}

			data = requests.put(
				"{}/nodes/{}".format(self.baseURI, params[0]),
				headers=self.headers,
				json=payload
			).json()['nodes'][0]
			print("{} is now off".format(data['name']))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def brightness(self, params=''):
		# Now for a list of devices
		try:
			payload = {
				"nodes":[{
					"attributes": {
						"state": {"targetValue": "ON"},
						"brightness": { "targetValue": params[1] }
					}
				}]
			}

			data = requests.put(
				"{}/nodes/{}".format(self.baseURI, params[0]),
				headers=self.headers,
				json=payload
			).json()['nodes'][0]
			print("Set brightness of {} to {}%".format(data['name'], params[1]))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

def main():

	parser = argparse.ArgumentParser()

	# hivehome.com credentials
	parser.add_argument("--username", help="hivehome.com username", default=os.getenv("HIVE_USERNAME", ''))
	parser.add_argument("--password", help="hivehome.com password", default=os.getenv("HIVE_PASSWORD", ''))

	# Actions
	parser.add_argument("command", nargs="*", help='command to pass to hive')

	# Verbose mode
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
	
	if len(args.command) < 1:
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