import pymysql
import os
import json
import sys
import time
import datetime

from dateutil import parser

from dotenv import load_dotenv
load_dotenv()
    
# MySQL connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

con = pymysql.connect(host = DB_HOST, user = DB_USER, port = 25060, passwd = DB_PASS, db = DB_NAME)
cursor = con.cursor()

cursor.execute("SELECT uv.user_id, c.id, c.vendor_id, c.published_date, c.link from users_vendors uv left join cves c on uv.vendor_id = c.vendor_id where c.processed <> 1")
res = cursor.fetchall()
print(res)

con.commit()
con.close()

# End script
sys.exit()