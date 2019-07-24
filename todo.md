Email Recipients:
	After monitoring system confirmed/stable, add Arnaldo, Nestor and Rene N. to week summary email targets
	* ENV[AUTH_TOKEN].zimmermann@ENV[AUTH_TOKEN].com,ENV[AUTH_TOKEN].melo@ENV[AUTH_TOKEN].com,rene.neumann@ENV[AUTH_TOKEN].com

hourly_job.py - lines 67 & 105:
	TODO: if a failure happen, make a new request again to confirm that error

sqlite_database.py - lines 52 and on:
	TODO: sqlite3 default timezone (UTC). Format timestamp to local timezone
 	TODO: get uptime since the last FAILURE if not, since first SUCCESS
	TODO: count checks by url

Extras:
* Validate web pages using selenium webdriver test if necessary
* Tool suggestion to manage web page statuses and statistics: https://hund.io/
