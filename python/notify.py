import pymysql
import os
import sys

from datetime import date

from itertools import groupby
from operator import itemgetter

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv
load_dotenv()
    
# MySQL connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

con = pymysql.connect(host = DB_HOST, user = DB_USER, port = 25060, passwd = DB_PASS, db = DB_NAME)
cursor = con.cursor()

cursor.execute("SELECT uv.user_id, c.id, v.vendor_name, c.published_date, c.link from users_vendors uv left join cves c on uv.vendor_id = c.vendor_id inner join vendors v on uv.vendor_id = v.id where c.processed <> 1")
res = cursor.fetchall()

cvesByEmail = groupby(res, itemgetter(0))

# print cves by email
# for email, cves in cvesByEmail:
#     print(email)
#     for cve in cves:
#         print(cve)
#         print(cve[3])
#     print('-' * 20)

today = date.today()

for email, cves in cvesByEmail:
  html = '<p>Hey there,</p><p>Here\'s the list of CVEs published in the last 24 hours that match the vendors you subscribed to on trynvdb.com:</p><ul>'
  for cve in cves:
    html += '<li>' + cve[1] + ' (' + cve[2] + ') - ' + str(cve[3]) + ' - ' + cve[4] + '</li>'
  html += '</ul><p>Cheers,</p><p>The NVDB team</p>'
  message = Mail(
    from_email='notify@trynvdb.com',
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

con.commit()
con.close()

# End script
sys.exit()