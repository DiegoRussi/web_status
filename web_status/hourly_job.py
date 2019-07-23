#!/usr/bin/env python3

# This script must run as a cron job in CRONTAB
# Run at every hour
# 0 * * * * /usr/bin/python3 .../web_status/hourly_job.py

# Stdlib
from datetime import datetime
import os
import warnings

# Third-party
import urllib3 as urllib3requests
import requests

# Local
import sqlite_database
import senders

''' Current Working Directory'''
cwd = os.getcwd()
# Work Dir. path to crontab
# cwd = "/usr/local/bin/ENV[AUTH_TOKEN]_web_status"


def hourly_job():
	"""
	This function is a Daily Job that must be scheduled to run every hour
	to check the web pages status and report the status

	The Job is to make requests to the ENV[AUTH_TOKEN] Website and ENV[AUTH_TOKEN] Cloud URLs to get the
	status of that page and store in tmp files named after the day of the request

	In case of FAILURE STATUS it must send the current failure report via email
	and to slack incoming webhook app

	:return:
	"""
	print("Daily Scheduler working...")
	print(os.getcwd())
	''' Get the List of URLs to make the requests '''
	with open(cwd + "/config/urls", "r") as conf:
		urls = conf.read().splitlines()

	''' Create file path by day to append the hourly reports '''
	file_name = datetime.now().strftime("%m-%d-%Y")
	file_path = cwd + "/reports/daily/" + file_name + ".txt"

	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0',
		'content-type': 'application/json',
		'Accept-Charset': 'UTF-8'
	}

	''' Loop for urls to make the request. '''
	for url in urls:
		status_code = None
		try:
			req = requests.get(url, headers=headers, verify=True)  # verify (SSL cred)
			status_code = req.status_code
		except Exception as e:
			print(e)

		status_code = req.status_code
		if not status_code:
			status_code = "unreachable"
			# TODO: if a failure happen, make a new request again to confirm that error

		url_status = "Success" if status_code == 200 else "Failure"

		''' Report status line. '''
		report = f'{datetime.now().strftime("%m-%d-%Y %H:%M:%S")} ' \
			f'{url} {status_code} {url_status}'
		print(report)

		sqlite_database.insert_entry(url, status_code, url_status)
		'''
		In case of failure: Send the report via email
		and to the slack incoming webhook channel.
		'''
		if url_status == "Failure":
			senders.send_email(report, subject="Web Status Daily report – Failure")
			senders.send_status_slackWebhook(report, subject="Web Status Daily report - Failure")

		with open(file_path, "a+") as tmp:
			tmp.write(f'{report}\n')

	''' Check ENV[AUTH_TOKEN] server IP address - status code 403 Forbidden - disable verify SSL '''
	with open(cwd + "/config/url_svn", "r") as conf:
		url_svn = conf.read()
	status_code = None
	''' Disable Insecure SSL exception/warning to request the ENV[AUTH_TOKEN] server'''
	urllib3requests.disable_warnings(urllib3requests.exceptions.InsecureRequestWarning)
	try:
		req = requests.get(url_svn, headers=headers, verify=False)  # verify (SSL)
		status_code = req.status_code
	except Exception as e:
		print(e)

	''' Re-enable warnings disabled previously '''
	warnings.resetwarnings()

	if not status_code:
		status_code = "unreachable"
		# TODO: if a failure happen, make a new request again to confirm that error

	''' ENV[AUTH_TOKEN] address must return 403 - Forbidden, due to its web access '''
	url_status = "Success" if status_code == 403 else "Failure"

	report = f'{datetime.now().strftime("%m-%d-%Y %H:%M:%S")} ' \
		f'{url_svn} {status_code} {url_status}'
	print(report)
	''' Insert request data in sqlite database '''
	sqlite_database.insert_entry(url_svn, status_code, url_status)

	if url_status == "Failure":
		senders.send_email(report, subject="Web Status Daily report – Failure")
		senders.send_status_slackWebhook(report, subject="Web Status Daily report - Failure")

	''' Append the hourly report in the day file. '''
	with open(file_path, "a+") as tmp:
		tmp.write(report)


if __name__ == "__main__":
	hourly_job()
