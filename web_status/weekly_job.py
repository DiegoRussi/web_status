#!/usr/bin/env python3

# This script must run as a cron job in CRONTAB
# Run every Saturday at 8AM:
# 0 * * * * /usr/bin/python3 ...ENV[AUTH_TOKEN]-web-status-crontab/web_status/weekly_job.py

# Stdlib
from datetime import datetime
import os

# Local
import sqlite_database
import senders

''' Current Working Directory'''
# cwd = os.getcwd()
cwd = "/Users/diegomatheus/PycharmProjects/ENV[AUTH_TOKEN]-web-status-crontab"
# Work Dir. path to crontab
# cwd = "/usr/local/bin/ENV[AUTH_TOKEN]_web_status"


def weekly_job():
	"""
	This function is a Weekly Job that must be scheduled to run every Saturday 8AM
	to get the current week daily reports and create the weekly report named after the
	current date and send its contents via email and to the slack channel

	It manages the weekly files to maintain only the current week and last week report
	:return:
	"""
	print("Weekly Scheduler working...")
	'''
	Manage Weekly files maintaining only the current last week file for archive.
	This way, we have the current week and last.
	'''
	weekly_files = os.listdir(cwd + "/reports/weekly/")
	for file in weekly_files:
		file_path = os.path.join(cwd + "/reports/weekly", file)
		if file.find("last") >= 0:
			os.remove(file_path)
		else:
			os.rename(file_path, os.path.join(cwd + "/reports/weekly", f"last{file}"))

	''' Append the week files into a new one and remove the daily right after. '''
	file_name = datetime.now().strftime("week_%m-%d-%Y")
	file_path = cwd + "/reports/weekly/" + file_name + ".txt"

	tmp_files = os.listdir(cwd + "/reports/daily/")

	'''
	Loop through files and read its content.
	Write the contents in the output file.
	'''
	with open(file_path, "a+") as out_file:
		for tmp in tmp_files:
			tmp_path = os.path.join(cwd + "/reports/daily", tmp)
			with open(tmp_path) as in_file:
				out_file.write(in_file.read())
				in_file.close()
				''' Removes the file given after read '''
				os.remove(in_file.name)

	''' Search for failure after sending email '''
	with open(file_path) as report:
		rep_content = report.read()
		if "Failure" in rep_content:
			subject = "Web Status Weekly report – with Failure"
		else:
			subject = "Web Status Weekly report – with Success"

	''' Send the weekly report summary built in sqlite3 database file '''
	summary = sqlite_database.select_build_report()
	if summary.find("Failures Count: 0") == -1:
		subject = "Web Status Weekly report – with Failure"
	else:
		subject = "Web Status Weekly report – with Success"

	# Do not send file reports contents, instead you could send the summary from sqlite
	senders.send_email(content=summary, subject=subject, attach_chart=True)
	# Possibility to send via Slack, but keeping it disabled
	# senders.send_status_slackWebhook(content=summary, subject=subject)


if __name__ == "__main__":
	weekly_job()
