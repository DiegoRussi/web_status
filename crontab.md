## CRONTAB the jobs scripts

* Cron to Every Saturday at 8AM
`0 8 * * 6 /usr/bin/python3 -u /path/to/script/weekly_job.py`
* Cron to Every hour at minute 0
` 0 * * * * /usr/bin/python3 -u /path/to/script/hourly_job.py`

* Change the permission of the scripts to be executables
`chmod +x web_status/hourly_job.py`
`chmod +x web_status/weekly_job.py`

* Enter the crontab list:
`sudo crontab -e`
* And configure the scripts like the lines below:
```
0 * * * * /usr/bin/python3 -u /usr/local/bin/ENV[AUTH_TOKEN]_web_status/web_status/hourly_job.py >/dev/null 2>&1
0 8 * * 6  /usr/bin/python3 -u /usr/local/bin/ENV[AUTH_TOKEN]_web_status/web_status/weekly_job.py >/dev/null 2>&1
```
