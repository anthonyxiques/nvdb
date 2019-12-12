# nvdb

## ISM6218 @ USF - Group 2 (Dec 2019)
- Gomez, Pedro
- Phillips, Eddie
- Sanchez, Sasha
- Xiques, Anthony

## MySQL

### View recently imported cves

`select * from nvdb.cves order by created_at desc limit 1000;`

##  Python

cd python

### How to activate venv

From https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

"Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH."

source env/bin/activate

### Install dependencies from requirements.txt

pip install -r requirements.txt

### Run import script

python3 import.py

### Install a new package

Example: installing requests package

pip install requests

### Update requirements.txt

pip freeze > requirements.txt

### Deactivate venv

deactivate

## Cron

### Set up cron job to run import.sh hourly
`0 * * * * sh ~/import.sh 2>&1 | /usr/bin/logger -t import_recent_cves`
`0 17 * * * sh ~/notify.sh 2>&1 | /usr/bin/logger -t notify`

## Logging
Cron log is set up through papertrailapp.com