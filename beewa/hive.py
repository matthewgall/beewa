#!/usr/bin/env python3

import os, sys, argparse, logging
import requests

class Hive:

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
			return False

	def list(self, params=''):
		# Now for a list of devices
		data = requests.get(
			"{}/nodes".format(self.baseURI),
			headers=self.headers
		).json()['nodes']
		return data

	def info(self, params=''):
		# Now for a list of devices
		try:
			return requests.get(
				"{}/nodes/{}".format(self.baseURI, params[0]),
				headers=self.headers
			).json()['nodes'][0]
		except:
			return None

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
			return True
		except:
			return False

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
			return True
		except:
			return False

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
			return True
		except:
			return False