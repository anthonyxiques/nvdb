#!/bin/bash

cd ~/nvdb/python/data
wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz
gunzip ~/nvdb/python/data/nvdcve-1.1-recent.json.gz
mv ~/nvdb/python/data/nvdcve-1.1-recent.json ~/nvdb/python/data/recent.json

cd ~/nvdb/python
. ~/nvdb/python/env/bin/activate
python3 ~/nvdb/python/import.py