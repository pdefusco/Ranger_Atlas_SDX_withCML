#LOADING SPLINK TABLES INTO PHOENIX#


import pandas as pd

class Db:
    def __init__(self):
        opts = {}
        opts['authentication'] = 'BASIC'
        opts['avatica_user'] = os.environ["WORKLOAD_USER"]
        opts['avatica_password'] = os.environ["WORKLOAD_PASSWORD"]
        database_url = os.environ["OPDB_ENDPOINT_PSE"]
        self.TABLENAME = "test_table_paul"
        self.conn = phoenixdb.connect(database_url, autocommit=True,**opts)
        self.curs = self.conn.cursor()
        
    def create_linkage_table_left(self):
        
        query = """
        CREATE TABLE IF NOT EXISTS "LINKAGE_LEFT" (
        unique_id VARCHAR,
        first_name VARCHAR,
        surname VARCHAR,
        dob VARCHAR,
        city  VARCHAR,
        email VARCHAR,
        groupp VARCHAR CONSTRAINT my_pk PRIMARY KEY (unique_id))
        """
        
        self.curs.execute(query)
        
    def upsert_linkage_left(self, data):

        sql = """upsert into "LINKAGE_LEFT" \
             (unique_id ,first_name,surname,dob,city,email,groupp) \
             values (?,?,?,?,?,?,?)"""
        #print(data)
        self.curs.executemany(sql,data)
        self.conn.commit()

def upsert_data(data, records=100):
        total_records=0
        header = True
        rows = []
        i=1
        model=Db()
        for index, row in data.iterrows():

            rows.append ([f"{row['unique_id']}",\
                      f"{row['first_name']}",f"{row['surname']}",\
                      f"{row['dob']}",f"{row['city']}", \
                      f"{row['email']}", f"{row['group']}"])
            total_records=total_records+1

            if i < records + 1 :   
                i=i+1
            else :
                model.upsert_linkage_left(rows)
                rows = []
                i=1
                print (f"Ingested {total_records} records")

        if len(rows) > 0 :
            model.upsert_linkage_left(rows)

        print (f"Ingested {total_records} records")
        
        
        
df_l= pd.read_parquet("data/fake_df_l.parquet", engine="pyarrow")

import logging
logging.basicConfig( level=logging.DEBUG)

import os
import phoenixdb
model=Db()
model.create_linkage_table_left()
upsert_data(df_l)


