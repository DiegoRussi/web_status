## Website Status Cron Job
Cron jobs to monitor the Websites URLs and report their status via email or webhooks (slack).

This project is built in Python3 and it is meant to run in the linux `crontab`. To know more about `crontab`,
see this documentation in this [link](https://www.linode.com/docs/tools-reference/tools/schedule-tasks-with-cron/).

### SETUP
Setup of the project and configuration of the `crontab`:

1. Access the directory to move the project: `cd /usr/local/bin`
2. Clone this repo.
3. Access project directory: `cd web_status/`
4. Install the requirements of the project:
```
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install -r requirements.txt
```
	* The `crontab` default Working Directory is: `/root`
	* Access the project scripts dir: `cd /usr/local/bin/web_status/web_status/`
	* Get the directory absolute path: `pwd`
 	* Edit the followings scripts path variable `cwd`:
		* e.g: `cwd = "/usr/local/bin/web_status"`
```
hourly_job.py
weekly_job.py
sqlite_database.py
senders.py
```

 * Gnuplot Script:
    * The gnuplot generates the week summary pie-chart via the results retrieved from the statuses.
 	* Access the directory: `cd plot/`
 	* Inside the `graph.plot` script in the "filename" line, change the absolute path of the `result.csv` file:
 		-  `filename = /usr/local/bin/web_status/plot/result.csv`

 * Config Directory Files:
	* In the config directory there are three files which you can configure: 
		* The `email_recipients` to receive the web status reports, eg.:
		`example@live.com`
		* The `urls` that defines which URLs will be tested its statuses, eg.:
		```
		https://www.pudim.com.br
		```
		* The `url_ip` that defines server public IP URL that behaviours differently, eg.:
		`https://8.8.8.8`

#### Crontab config:
 - The `crontab` is meant to run scripts in a cron schedule, in our case, it will
 run a hourly and a weekly scripts.

 * Edit the root user `crontab` file: `sudo crontab -e`
 * Insert the line below with the absolute path to the scripts and the python3 executable:
```
0 * * * * /usr/bin/python3 -u /usr/local/bin/web_status/web_status/hourly_job.py >> /var/log/hourly_status.log 2>&1
0 8 * * 6  /usr/bin/python3 -u /usr/local/bin/web_status/web_status/weekly_job.py >> /var/log/hourly_status.log 2>&1
```

### LOGS
You can reach the logs of the executed scripts in the following files:
```
/var/log/syslog
/var/log/hourly_status.log
/var/log/weekly_status.log
```
