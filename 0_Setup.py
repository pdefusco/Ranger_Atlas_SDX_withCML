# ###########################################################################
#
#  CLOUDERA APPLIED MACHINE LEARNING PROTOTYPE (AMP)
#  (C) Cloudera, Inc. 2022
#  All rights reserved.
#
#  Applicable Open Source License: Apache 2.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# ###########################################################################

## Part 0 - Project Setup

## This script creates three datasets and automatically loads them to cloud storage for you.
## No CDP Data Lake based changes are required to this script.
## If you are unable to load the data, you must have a problem with CDP User rights (ID Broker Mappings, etc)


## Installing Project Requirements
!pip3 install -r requirements.txt

## Importing Python Libs
import pandas as pd
import numpy as np
import os
from faker import Faker
import random
import time
import json
import requests
import xml.etree.ElementTree as ET
import datetime

## Loading Base file
camp_conversion_df = pd.read_csv('data/campaign_conversion.csv')

## Number of Fake instances
rg = 1000

## Creating the files

## Fake Score Feature
camp_conversion_df = camp_conversion_df.iloc[:rg]

mu, sigma = 1, .4 # mean and standard deviation
s = np.random.normal(mu, sigma, rg)

camp_conversion_df['score'] = camp_conversion_df['conversion']+s

## Fake Marketing Campaign Features

fake = Faker('en_US')

final = {} 
final['name'] = [fake.name() for i in range(rg)]
final['street_address'] = [fake.street_address() for i in range(rg)]
final['city'] = [fake.city() for i in range(rg)]
final['postcode'] = [fake.postcode() for i in range(rg)]
final['phone_number'] = [fake.phone_number() for i in range(rg)]
final['job'] = [fake.job() for i in range(rg)]

personal_data = pd.DataFrame(final)

marketing_data = pd.concat([personal_data, camp_conversion_df], axis=1)

## Fake Bank Info Features

final = {}
rg = 500
final['name'] = marketing_data['name'].sample(n=rg, replace=False)
final['ABA_routing'] = [fake.aba() for i in range(rg)]
final['bank_country'] = [fake.bank_country() for i in range(rg)]
final['account_number'] = [fake.bban() for i in range(rg)]
final['IBAN'] = [fake.iban() for i in range(rg)]
final['swift11'] = [fake.swift11() for i in range(rg)]
final['random'] = [random.randint(0, 1) for i in range(rg)]

bank_data = pd.DataFrame(final)
bank_data.loc[bank_data['random'] == 1, 'name'] = fake.name()
bank_data = bank_data.drop('random', axis=1)
bank_data = bank_data.drop_duplicates(subset=['name'])
bank_data = pd.merge(bank_data, marketing_data, how="inner", on="name")
bank_data = bank_data.drop(columns=["street_address", "city", "postcode", "phone_number", "job"])

## Fake Credit Card Info Features

final = {}
rg = 200
final['name'] = bank_data['name'].sample(n=rg, replace=False)
final['credit_card_number'] = [fake.credit_card_number() for i in range(rg)]
final['credit_card_provider'] = [fake.credit_card_provider() for i in range(rg)]
final['credit_card_security_code'] = [fake.credit_card_security_code() for i in range(rg)]
final['credit_card_expire'] = [fake.credit_card_expire() for i in range(rg)]

credit_card_data = pd.DataFrame(final)

## Saving files in local CML Project dir

marketing_data.to_csv('data/mkt_campaign_data.csv', index=False)
bank_data.to_csv('data/bank_data.csv', index=False)
credit_card_data.to_csv('data/credit_card_data.csv', index=False)

## Writing files to cloud storage

## Extracting the correct URL from hive-site.xml
tree = ET.parse('/etc/hadoop/conf/hive-site.xml')
root = tree.getroot()

for prop in root.findall('property'):
    if prop.find('name').text == "hive.metastore.warehouse.dir":
        storage = prop.find('value').text.split("/")[0] + "//" + prop.find('value').text.split("/")[2]

print("The correct Cloud Storage URL is:{}".format(storage))

os.environ['STORAGE'] = storage

## Using the HDFS CLI to interact with Cloud Storage

## Creating three different dirs, one for each file
!hdfs dfs -mkdir -p $STORAGE/sdxdemodir/mkt_campaign
!hdfs dfs -mkdir -p $STORAGE/sdxdemodir/bank
!hdfs dfs -mkdir -p $STORAGE/sdxdemodir/creditcard

## Copying files to Cloud Storage
!hdfs dfs -copyFromLocal /home/cdsw/data/mkt_campaign_data.csv $STORAGE/sdxdemodir/mkt_campaign/mkt_campaign_data.csv
!hdfs dfs -copyFromLocal /home/cdsw/data/bank_data.csv $STORAGE/sdxdemodir/bank/bank_data.csv
!hdfs dfs -copyFromLocal /home/cdsw/data/credit_card_data.csv $STORAGE/sdxdemodir/creditcard/credit_card_data.csv

## Validating data has been loaded
!hdfs dfs -ls $STORAGE/sdxdemodir
!hdfs dfs -ls $STORAGE/sdxdemodir/mkt_campaign
!hdfs dfs -ls $STORAGE/sdxdemodir/bank
!hdfs dfs -ls $STORAGE/sdxdemodir/creditcard