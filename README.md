# nvdb

## About

Dec 2019
ISM6218 - Group 2
Gomez, Pedro
Phillips, Eddie
Sanchez, Sasha
Xiques, Anthony

##  Python

### How to activate venv

From https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

"Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH."

source python/env/bin/activate

### Install dependencies from requirements.txt

cd python

pip install -r requirements.txt

### Install package

Example: installing requests package

pip install requests

### Update requirements.txt

pip freeze > requirements.txt

### Deactivate venv

deactivate