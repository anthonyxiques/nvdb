import pymysql
import os
import json
import sys
import time
import datetime

from dateutil import parser

from dotenv import load_dotenv
load_dotenv()

# Read JSON file
file = os.path.relpath('.') + "/data/sample.json"
json_data = open(file).read()
json_data_obj = json.loads(json_data)
cves = json_data_obj['CVE_Items']

# do validation and checks before insert
def validate_string(val):
  if val != None:
    if type(val) is int: #for x in val: #print(x)
      return str(val).encode('utf-8')
    else :
      return val

# return id of row if it already exists, create if it doesn't exist
def first_or_create_vendor(connection, curs, vendor_name):
  curs.execute("SELECT * from vendors where vendor_name = %s", (vendor_name))
  res = curs.fetchone()
  if (res is None):
    curs.execute("INSERT INTO vendors SET vendor_name = %s ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)", (vendor_name))
    connection.commit()
    curs.execute("SELECT LAST_INSERT_ID()")
    res = curs.fetchone()
    return res[0]   
  else:
    return res[0]
    
# MySQL connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

con = pymysql.connect(host = DB_HOST, user = DB_USER, port = 25060, passwd = DB_PASS, db = DB_NAME)
cursor = con.cursor()

# Parse json data to SQL insert
for i, item in enumerate(cves):
  try:
    id = validate_string(item.get("cve", {}).get('CVE_data_meta', {}).get('ID'))

    published_date_str = validate_string(item.get("publishedDate"))
    published_date = parser.parse(published_date_str)

    last_modified_date_str = validate_string(item.get("lastModifiedDate"))
    last_modified_date = parser.parse(published_date_str)

    description = validate_string(item.get("cve", {}).get('description', {}).get('description_data', {})[0].get('value'))
    reference_data = item.get("cve", {}).get('references', {}).get('reference_data')

    if isinstance(reference_data, list) and(len(reference_data) > 0):
      link = reference_data[0].get('url')
    else:
      link = ''

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    nodes = item.get('configurations', {}).get('nodes')

    if isinstance(nodes, list) and(len(nodes) > 0):
      node = nodes[0]

      if 'cpe_match' in node:
        cpe_string = validate_string(node.get('cpe_match', {})[0].get('cpe23Uri'))
      else:
        cpe_string = validate_string(node.get('children', {})[0].get('cpe_match', {})[0].get('cpe23Uri'))

      cpe = cpe_string.split(':')

      vendor = cpe[3]
      product = cpe[4]

      vendor_id = first_or_create_vendor(con, cursor, vendor)
    else:
      vendor = ''
      product = ''

    score = item.get("impact", {}).get('baseMetricV3', {}).get('cvssV3', {}).get('baseScore')

    cursor.execute("INSERT IGNORE INTO cves (id, published_date, last_modified_date, created_at, description, link, vendor_id, product, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, published_date, last_modified_date, timestamp, description, link, vendor_id, product, score))
  except:
    print("Unexpected error:", sys.exc_info())
    cursor.execute("INSERT IGNORE INTO failed_imports (id, failed__created_at) VALUES (%s, %s)", (id, timestamp))
    continue
con.commit()
con.close()

# End script
sys.exit()