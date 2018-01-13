#!/usr/bin/env python3

import os, sys, logging, json
import requests
from hive import Hive

class Beewa:

	def __init__(self, username, password):
		# instantiation of Hive
		self.hive = Hive(username, password)

		# and login
		self.hive.login()

	def list(self, params='', args=''):
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

	def info(self, params='', args=''):
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

	def on(self, params='', args=''):
		# Now for a list of devices
		try:
			if self.hive.on(params):
				print("{} is now on".format(params[0]))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def off(self, params='', args=''):
		# Now for a list of devices
		try:
			if self.hive.off(params):
				print("{} is now off".format(params[0]))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def brightness(self, params='', args=''):
		# Now for a list of devices
		try:
			if self.hive.brightness(params):
				print("Set brightness of {} to {}%".format(
					params[0],
					params[1]
				))
		except:
			exit("Unable to login to Hive at this time. Exiting.")

	def groups(self, params='', args=''):
		try:
			with open(args.groups) as f:
				data = json.loads(f.read())
		except IOError:
			exit("Unable to locate {} file".format(args.groups))

		# if they haven't submitted a subcommand
		if len(params) == 0:
			exit(self.groups_list(args.command[1:], data))

		try:
			method = False
			method = getattr(self, "groups_{}".format(params[0]))
			method(args.command[1:], data)
		except AttributeError:
			exit('groups {} is not a supported action'.format(params[0]))
		if not method:
			exit('groups {} is not a supported action'.format(params[0]))

	def groups_list(self, params='', data=''):
		# print a list of groups
		for group in data['groups']:
			print("===========\n{}\n===========".format(group))
			for device in data['groups'][group]:
				print(device)

	def groups_on(self, params='', data=''):
		# now we iterate through the devices and switch them on
		try:
			for device in data['groups'][params[1]]:
				if self.hive.on([device]):
					print("{} is now on".format(device))
		except KeyError:
			exit("Unable to find group: {}".format(params[1]))

	def groups_off(self, params='', data=''):
		# now we iterate through the devices and switch them on
		try:
			for device in data['groups'][params[1]]:
				if self.hive.off([device]):
					print("{} is now off".format(device))
		except KeyError:
			exit("Unable to find group: {}".format(params[1]))