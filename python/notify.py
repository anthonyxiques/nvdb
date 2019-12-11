import pymysql
import os
import sys

from datetime import date

from itertools import groupby
from operator import itemgetter

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, From)

from dotenv import load_dotenv
load_dotenv()
    
# MySQL connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

con = pymysql.connect(host = DB_HOST, user = DB_USER, port = 25060, passwd = DB_PASS, db = DB_NAME)
cursor = con.cursor()

# get list of cves published in the last 24 hours
# each cve is only returned if at least one user is subscribed to the related vendor
cursor.execute("SELECT uv.user_id, c.id, v.vendor_name, c.published_date, c.link from users_vendors uv left join cves c on uv.vendor_id = c.vendor_id inner join vendors v on uv.vendor_id = v.id where c.processed <> 1 and c.published_date >= now() - INTERVAL 1 DAY")
res = cursor.fetchall()

# group by user (email address)
cvesByEmail = groupby(res, itemgetter(0))

# print cves grouped by email
# for email, cves in cvesByEmail:
#     print(email)
#     for cve in cves:
#         print(cve)
#         print(cve[3])
#     print('-' * 20)

today = date.today()

# send emails through SendGrid
for email, cves in cvesByEmail:
  html = '<p>Hey there,</p><p>Here\'s the list of CVEs published in the last 24 hours that match the vendors you subscribed to on trynvdb.com:</p><ul>'
  for cve in cves:
    html += '<li>' + cve[1] + ' (' + cve[2] + ') - ' + str(cve[3]) + ' - ' + cve[4] + '</li>'
  html += '</ul><p>Cheers,</p><p>The NVDB team</p>'
  message = Mail(
    from_email=From('notify@trynvdb.com', 'TryNVDB.com'),
    to_emails=email,
    subject=('Notifications for ' + today.strftime("%m/%d/%y") ),
    html_content=html)
  try:
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
  except Exception as e:
    print(str(e))

# set processed = 1 for cves published in the last 24 hours
cursor.execute("UPDATE cves SET processed=1 WHERE processed <> 1 and published_date >= now() - INTERVAL 1 DAY")

con.commit()
con.close()

# End script
sys.exit()