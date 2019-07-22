## ENV[AUTH_TOKEN] WEB STATUS CRONTAB
Cron jobs to monitor the ENV[AUTH_TOKEN] and ENV[AUTH_TOKEN] Cloud websites and report their status.

This project is built in Python3 and it is meant to run in `crontab`.

### SETUP
Setup of the project and configuration of the `crontab`:

1. Access the directory to move the project: `cd /usr/local/bin`
2. Disable the SSL verification to clone the repository: `git config --global http.sslverify "false"`
3. Clone the repo.: `git clone https://gitlab.ENV[AUTH_TOKEN].com/diego.russi/ENV[AUTH_TOKEN]_web_status.git`
4. Access project directory: `cd ENV[AUTH_TOKEN]-web-status-crontab/`
5. Install the requirements of the project:
```
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install -r requirements.txt
```
6. Modify the Current Working Directory (cwd) inside the scripts:
	* The `crontab` default Working Directory is: `/root`
	* Access the project scripts dir: `cd /usr/local/bin/ENV[AUTH_TOKEN]_web_status/web_status/`
	* Get the directory absolute path: `pwd`
 	* Edit the followings scripts path variable `cwd`:
		* e.g: `cwd = "/usr/local/bin/ENV[AUTH_TOKEN]-web-status-crontab"`
```
hourly_job.py
weekly_job.py
sqlite_database.py
senders.py
```

 * Gnuplot Script:
 	* Access the directory: `cd plot/`
 	* Inside the `graph.plot` script in the "filename" line, change the absolute path of the `result.csv` file:
 		-  `filename = /usr/local/bin/ENV[AUTH_TOKEN]_web_status/ENV[AUTH_TOKEN]-web-status-crontab/plot/result.csv`

#### Crontab config:
 - The `crontab` is meant to run scripts in a cron schedule, in our case, it will
 run a hourly and a weekly scripts. To get more info about `crontab`,
 see `crontab man` and documentation in this [link](https://www.linode.com/docs/tools-reference/tools/schedule-tasks-with-cron/).

 * Edit the root user `crontab` file: `sudo crontab -e`
 * Insert the line below with the absolute path to the scripts:
```
0 * * * * /usr/bin/python3 -u /usr/local/bin/ENV[AUTH_TOKEN]-web-status-crontab/web_status/hourly_job.py >> /var/log/hourly_status.log 2>&1
0 8 * * 6  /usr/bin/python3 -u /usr/local/bin/ENV[AUTH_TOKEN]-web-status-crontab/web_status/weekly_job.py >> /var/log/weekly_status.log 2>&1
```

### LOGS
You can reach the logs of the executed scripts in the following files:
```
/var/log/hourly_status.log
/var/log/weekly_status.log
```
