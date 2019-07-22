
* status files - weekly report - Partially done
	* Create file by day, appending every hour the report - DONE
	* Weekly report: append all the week files into one called week.txt - DONE
	* Manage the weekly reports, move to lastweek_xyz.txt maintinaing only the lastweek and current - DONE
	* exclude week files - DONE

* send email - if failure in a daily job and in weekly status - DONE
	- SMTP gmail.com
	- to enable receive SMTP emails:
		https://myaccount.google.com/lesssecureapps

	* SLACK webhook to send status - DONE
		- Send all the reports made to the SLACK CHANNEL - not only failures - DONE
		- Format slack messages - Green/Red color reports - DONE

* Run script as a linux service - systemd - .init - DONE
https://stackoverflow.com/questions/1603109/how-to-make-a-python-script-run-like-a-service-or-daemon-in-linux

Approach - CRONTAB the jobs scripts

every Saturday at 8AM - cron job:
0 8 * * 6 /usr/bin/python3 /path/to/script/weekly_job.py

every hour - cron job:
0 * * * * /usr/bin/python3 /path/to/script/daily_job.py

Extras:
* Validate web page: selenium webdriver test if necessary

* suggestion: https://hund.io/
