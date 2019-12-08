#!/bin/bash

cd ~/nvdb/python/data
wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz
gunzip nvdcve-1.1-recent.json.gz
mv nvdcve-1.1-recent.json recent.json

cd ~/nvdb/python
source env/bin/activate
python3 import.py
deactivate