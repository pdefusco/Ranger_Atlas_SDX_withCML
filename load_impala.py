import os
import pandas
from impala.dbapi import connect
from impala.util import as_pandas




IMPALA_HOST = "coordinator-aws-2-impala-test.env-j2ln9x.dw.ylcu-atmi.cloudera.site"

IMPALA_PORT="443" #443 21050
USERNAME=my_user
PASSWORD=my_pwd
conn = connect(host=IMPALA_HOST,
               port=IMPALA_PORT,
               auth_mechanism="LDAP",
               user=IMPALA_USERNAME,
               password=IMPALA_PASSWORD,
               use_http_transport=True,
               http_path="/cliservice",
               use_ssl=True)
# Execute using SQL
# cursor = conn.cursor()
cursor = conn.cursor()
cursor.execute('show databases')
for row in cursor:
    print(row)