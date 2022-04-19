import cml.data_v1 as cmldata

CONNECTION_NAME = "default-hive"
conn = cmldata.get_connection(CONNECTION_NAME)

## Sample Usage to get pandas data frame
EXAMPLE_SQL_QUERY = "show databases"
dataframe = conn.get_pandas_dataframe(EXAMPLE_SQL_QUERY)
print(dataframe)

## Other Usage Notes:

## Alternate Sample Usage to provide different credentials as optional parameters
#conn = cmldata.get_connection(
#    CONNECTION_NAME, {"USERNAME": "someuser", "PASSWORD": "somepassword"}
#)

## Alternate Sample Usage to get DB API Connection interface
#db_conn = conn.get_base_connection()

## Alternate Sample Usage to get DB API Cursor interface
#db_cursor = conn.get_cursor()
#db_cursor.execute(EXAMPLE_SQL_QUERY)
#for row in db_cursor:
#  print(row)