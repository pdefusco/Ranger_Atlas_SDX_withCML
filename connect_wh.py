import os
try:
  import cmldata
except ImportError as error:
  raise ImportError("Could not import cmldata, please fork project or create a new one to use the library functionality " + str(error))

CONNECTION_NAME = "default-hive"

# You can change the following lines to update your credentials
USERNAME = os.getenv('HADOOP_USER_NAME')
PASSWORD = os.getenv('WORKLOAD_PASSWORD')

conn = cmldata.getConnection({
         'CONNECTION_NAME': CONNECTION_NAME,
         'USERNAME': USERNAME,
         'PASSWORD': PASSWORD
       })

dbCursor = conn.getCursor()

# Uncomment following lines to run an example query
#EXAMPLE_SQL_QUERY = "show databases"
#dbCursor.execute(EXAMPLE_SQL_QUERY)
#for row in dbCursor:
#  print(row)


try:
  import cmldata
except ImportError as error:
  raise ImportError("Could not import cmldata, please fork project or create a new one to use the library functionality " + str(error))

CONNECTION_NAME = "go02-aw-dl"
conn = cmldata.getConnection({
         'CONNECTION_NAME': CONNECTION_NAME,
       })
handle = conn.getHandle()

# Uncomment following lines to run an example query
#EXAMPLE_SQL_QUERY = "show databases"
#handle.sql(EXAMPLE_SQL_QUERY).show()
