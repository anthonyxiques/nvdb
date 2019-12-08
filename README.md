# nvdb

## ISM6218 @ USF - Group 2 (Dec 2019)
- Gomez, Pedro
- Phillips, Eddie
- Sanchez, Sasha
- Xiques, Anthony

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