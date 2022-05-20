# Stlib
import os
import sqlite3

''' Current Working Directory '''
# cwd = os.getcwd()
# Work Dir. path to crontab
cwd = "/usr/local/bin/web_status"

''' sqlite Database Path'''
db_path = cwd + "/reports.db"


def sqlite_connection(db_file):
	""" Create a database connection to the SQLite
		database specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	try:
		return sqlite3.connect(db_file)
	except Exception as e:
		print(e)


def insert_entry(url, status_code, status):
	""" Insert a URL check infos into the SQLite DB Table reports
	:param url: given url of the report
	:param status_code: given status_code of the report
	:param status: given status of the report
	:return:
	"""
	db_conn = sqlite_connection(db_path)
	cursor = db_conn.cursor()

	cursor.execute("insert into reports (url, code, status) values (?,?,?)", (url, status_code, status))

	db_conn.commit()
	print(f'Inserted sqlite entry: {db_conn.total_changes}')

	db_conn.close()


def select_build_report():
	""" Query s to build the statistics from the URL checks (week)
	returning the formatted summary string with the data collected
	:return: formatted string summary
	"""
	db_conn = sqlite_connection(db_path)
	cursor = db_conn.cursor()

	# TODO: sqlite3 default timezone (UTC). Format timestamp to local timezone
	# SELECT datetime(timestamp, 'localtime') as localtime
	# UTC in email body

	# TODO: get uptime since the last FAILURE if not, since first SUCCESS
	# SELECT *, julianday('now') - julianday(timestamp) as uptime FROM reports
	# WHERE DATE(timestamp) = (
	#     SELECT MIN(DATE(timestamp)) FROM reports
	# )
	# AND url LIKE '%<PATTERN>%' AND status = 'Failure'

	# get oldest
	# SELECT * FROM reports WHERE DATE(timestamp) = (SELECT MIN(DATE(timestamp)) FROM reports)

	# TODO: count checks by url
	# SELECT * FROM reports WHERE DATE(timestamp) >= DATE('now', '-7 days') AND url LIKE '%<PATTERN>%';

	sql_count_lastweek = """SELECT count(*) AS total
	FROM reports
	WHERE DATE(timestamp) >= DATE('now', '-7 days');
	"""
	cursor.execute(sql_count_lastweek)
	total = cursor.fetchone()
	total = total[0]

	sql_count_success = """SELECT count(*) AS Total
	FROM reports
	WHERE DATE(timestamp) >= DATE('now', '-7 days')
	AND Status = 'Success'"""
	cursor.execute(sql_count_success)
	success_count = cursor.fetchone()
	success_count = success_count[0]

	sql_count_failures = """SELECT count(*) AS Total
	FROM reports
	WHERE DATE(timestamp) >= DATE('now', '-7 days')
	AND Status != 'Success'"""
	cursor.execute(sql_count_failures)
	failures_count = cursor.fetchone()
	failures_count = failures_count[0]

	sql_get_failures = """SELECT timestamp, url, code, status FROM reports
	WHERE DATE(timestamp) >= DATE('now', '-7 days')
	AND Status != 'Success'
	ORDER BY timestamp"""
	cursor.execute(sql_get_failures)
	failures_rows = cursor.fetchall()

	failures = []
	for row in failures_rows:
		failure = f'Timestamp UTC: {row[0]}, URL: {row[1]}, Status Code: {row[2]}, Status: {row[3]}\n'
		failures.append(failure)

	summary = f'\nWeek Report Statistics:\n\tTotal Checks: {total}\n\tSuccess Count: {success_count}' \
		f'\n\tFailures Count: {failures_count}\n\nFailures List:\n'

	for fail in failures:
		summary += fail

	''' Write statistics into .CSV file to generate a PLOT w/ gnuplot script '''
	# result, total
	# Failures, 123
	# Success, 1234
	with open(cwd + "/plot/result.csv", "w+") as csv:
		csv.truncate()
		csv.write(f"result, total\nFailures, {failures_count}\nSuccess, {success_count}")

	''' Generate Pie-chart plot - sys call to execute the gnuplot script '''
	# TODO: manage the plot image file - delete, verify if exists, treat errors
	# inside plot script in "filename" line, change the absolute path of the graph_plot.sh script
	plot_script = cwd + "/plot/graph.plot"
	# os.system() - If this command generates any output,
	# it will be sent to the interpreter standard output stream
	''' Execute and then get the exit status ($?) to validate the command '''
	if os.system(plot_script) != 0:
		print("The pie-chart plot generation failed !")

	if not os.path.exists("/tmp/pie_chart.png"):
		print("Pie-chart plot does not exists")

	return summary


if __name__ == "__main__":
	select_build_report()
