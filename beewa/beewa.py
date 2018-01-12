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
		self.login(None)

	def login(self, device):
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

	def list(self, device):
		# Now for a list of devices
		try:
			data = requests.get(
				"{}/nodes".format(self.baseURI),
				headers=self.headers
			).json()
			
			for device in data['nodes']:
				if not device['name'].startswith(("http://", "Fake")):
					print("{}: {}".format(
						device['id'],
						device['name']
					))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def info(self, device):
		# Now for a list of devices
		try:
			data = requests.get(
				"{}/nodes/{}".format(self.baseURI, device),
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

def main():

	parser = argparse.ArgumentParser()

	# hivehome.com credentials
	parser.add_argument("--username", help="hivehome.com username", default=os.getenv("HIVE_USERNAME", ''))
	parser.add_argument("--password", help="hivehome.com password", default=os.getenv("HIVE_PASSWORD", ''))

	# Actions
	parser.add_argument("action", help="the action to perform")
	parser.add_argument("device", nargs="?", default='', help='the device to perform the action')

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
	
	hive = Beewa(args.username, args.password)
	try:
		method = False
		method = getattr(hive, args.action)
		method(args.device)
	except AttributeError:
		exit('{} is not a supported action'.format(args.action))
	if not method:
		exit('{} is not a supported action'.format(args.action))

if __name__ == '__main__':
	main()