import os
import cx_Oracle
from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def index():
    connection = cx_Oracle.connect("admin/DemoATP12345678@demoatp_high")
    cur = connection.cursor()
    cur.execute("SELECT channel_desc, TO_CHAR(SUM(amount_sold),'9,999,999,999') SALES$,RANK() OVER (ORDER BY SUM \
        (amount_sold)) AS default_rank,RANK() OVER (ORDER BY SUM(amount_sold) DESC NULLS LAST) AS custom_rank \
        FROM sh.sales, sh.products, sh.customers, sh.times, sh.channels, sh.countries \
        WHERE sales.prod_id=products.prod_id AND sales.cust_id=customers.cust_id AND customers.country_id = countries.country_id AND sales.time_id=times.time_id AND sales.channel_id=channels.channel_id \
        AND times.calendar_month_desc IN ('2000-09', '2000-10') \
        AND country_iso_code='US' \
        GROUP BY channel_desc")
    # col = cur.fetchone()
    list = []
    for result in cur:
        list.append(result)
        print (result)
    list_json = json.dumps(list)
    cur.close()
    connection.close()
    return list_json

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)