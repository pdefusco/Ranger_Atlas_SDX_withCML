# Machine Learning with the Cloudera Shared Data Experience

CML is not just a Machine Learning platform. It's a ML platform powered by an end to end Data Platform. 

SDX is a fundamental part of Cloudera Data Platform architecture, unlike other vendors’ bolt-on approaches to security and governance. 
Independent from compute and storage layers, SDX delivers an integrated set of security and governance technologies built on metadata and delivers persistent context across all analytics as well as public and private clouds. 
Consistent data context simplifies the delivery of data and analytics with a multi-tenant data access  model that is defined once and seamlessly applied everywhere.
SDX reduces risk and operational costs by delivering consistent data context across deployments. IT can deploy fully secured and governed data lakes faster, giving more users access to more data, without compromise. 

In the context of ML and MLOps, SDX provides the following key benefits:

* You can track ML metadata in Atlas. For example, ML Models are assigned a lineage graph mapping them to datasets and projects.
* You can enforce data access constraints on the entire Model Lifecycle in Ranger. Datasets are assigned row and column level masking rules that govern how a Data Scientist creates models. 
* You can profile and audit users in the CDP Data Catalog. For example, you can determine not only who accessed the data, but also if they did so  
* In CML, Models are protected by Security Constraints. Every prediction request reaching a Model Endpoint optionally requires authentication.

To learn more on SDX please visit [this page](https://www.cloudera.com/products/sdx.html)


## Project Summary

In this project you will explore real world examples of how SDX increases ML Governance and overall compliance with ML Ops Best Practices. 

The project is divided in the following steps:

1. CML Project Setup
2. Create Hive Managed Tables from Cloud Storage in the CDW Virtual Warehouse
3. Validate the Data in the Atlas UI
4. Access the Data in the CML Project via CML Data Connections
5. Restrict user access in the Ranger UI and observe changes in the CML Project
6. Train a ML model with the Hive data and deploy the model to a REST Endpoint via CML API V2. Observe the changes in Atlas


## Prerequisites

This project requires access to a CML Workspace, a CDW Virtual Warehouse, and rights to access the Data Catalog, Ranger and Atlas (SDX) in CDP Public or Private Cloud. 

Familiarity with Python, SQL, and Jupyter Notebooks is recommended. However, no coding is required beyond executing the provided scripts. 

If you are completely new to CML and would like a quick intro to creating Projects, Sessions, using Spark and more, please start with [this repository](https://github.com/pdefusco/CML_CrashCourse)


## Part 1: CML Project Setup

Log into your CML Workspace. Create a new CML Project.

![alt text](images/sdx2cml01.png)

To create the CML Project, clone it from this GitHub repository by pasting this link as shown below. You can leave default runtime settings as they are. 

![alt text](images/sdx2cml02.png)

Start a CML Session with the following settings.

![alt text](images/sdx2cml03.png)

* Session Name: "WB Session" or anything you would like to use
* Editor: "Workbench"
* Enable Spark: Not required  
* Resource Profile: 1 or 2 vCPU / 2 or 4 GiB Memory is fine. Make sure to select 0 GPUs
* Other settings such as Kernel, Edition, Version, can be left to default values

Open script "0_Setup.py" and run all the code at once as shown below. 

![alt text](images/sdx2cml04.png)

At the end, enter the following code into the prompt. The prompt is located at the bottom right of your screen.

<code>os.environ['STORAGE']</code> 

Take note of the output. This is your Cloud Storage location. You will need this in Part 2. 

![alt text](images/sdx2cml05.png)


## Part 2: Create Hive Managed Tables from Cloud Storage in the CDW Virtual Warehouse

Navigate out of the CML Project and open the CDW Service. 

Open the Hue editor to run queries in your Hive CDW Virtual Warehouse as shown below.

![alt text](images/sdx2cml06.png)

Enter the following queries and execute. 

Notice we are creating a temporary table from each of the three files, and then three Hive Managed Tables correspondingly.

You will proabably have to modify the S3 bucket value. 

To do so, replace the string "s3a://demo-aws-go02" below with value you copied to your clipboard in the CML Session earlier.

#### DDL for Marketing Campaign Table

<code> 
DROP TABLE IF EXISTS marketing_campaign_tbl;

CREATE EXTERNAL TABLE marketing_campaign_tbl(
  name STRING,
  street_address STRING,
  city STRING,
  postcode STRING,
  phone_number STRING, 
  job STRING
  )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION "s3a://demo-aws-go02/sdxdemodir/mkt_campaign";
  
SELECT * FROM marketing_campaign_tbl;

DROP TABLE IF EXISTS marketing_campaign_table;

CREATE TABLE IF NOT EXISTS marketing_campaign_table(
  name STRING,
  street_address STRING,
  city STRING,
  postcode STRING,
  phone_number STRING, 
  job STRING
  )
COMMENT 'Marketing Campaign';

INSERT OVERWRITE TABLE marketing_campaign_table SELECT * FROM marketing_campaign_tbl;

SELECT * from marketing_campaign_table; 
DROP TABLE marketing_campaign_tbl;
</code>

#### DDL for Bank Info Table

<code> 
DROP TABLE IF EXISTS bank_info_tbl;

CREATE EXTERNAL TABLE bank_info_tbl(
  name STRING,
  ABA_routing STRING,
  bank_country STRING,
  account_number STRING,
  IBAN STRING, 
  swift11 STRING, 
  Recency STRING, 
  History STRING, 
  used_discount STRING, 
  used_bogo STRING,
  zip_code STRING, 
  is_referral STRING, 
  channel STRING, 
  offer STRING, 
  conversion STRING, 
  score STRING 
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION "s3a://demo-aws-go02/sdxdemodir/bank";

SELECT * FROM bank_info_tbl;

DROP TABLE IF EXISTS bank_info_table;

CREATE TABLE IF NOT EXISTS bank_info_table(
  name STRING,
  ABA_routing STRING,
  bank_country STRING,
  account_number STRING,
  IBAN STRING, 
  swift11 STRING, 
  Recency STRING, 
  History STRING, 
  used_discount STRING, 
  used_bogo STRING,
  zip_code STRING, 
  is_referral STRING, 
  channel STRING, 
  offer STRING, 
  conversion STRING, 
  score STRING 
  )
COMMENT 'Bank Info';

INSERT OVERWRITE TABLE bank_info_table SELECT * FROM bank_info_tbl;

SELECT * FROM bank_info_table; 
DROP TABLE bank_info_tbl;
</code>

#### DDL for Bank Info Table

<code> 
DROP TABLE IF EXISTS cc_info_tbl;

CREATE EXTERNAL TABLE cc_info_tbl(
  name STRING,
  credit_card_number STRING,
  credit_card_provider STRING,
  credit_card_security_code STRING,
  credit_card_expire STRING
  )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION "s3a://demo-aws-go02/sdxdemodir/creditcard”;
  
SELECT * FROM cc_info_tbl;

DROP TABLE IF EXISTS cc_info_table;

CREATE EXTERNAL TABLE cc_info_table(
  name STRING,
  credit_card_number STRING,
  credit_card_provider STRING,
  credit_card_security_code STRING,
  credit_card_expire STRING
  )
COMMENT 'Credit Card Info';
  
INSERT OVERWRITE TABLE cc_info_table SELECT * FROM cc_info_tbl;

SELECT * FROM cc_info_table; 
DROP TABLE cc_info_tbl;
</code>

For more on creating Hive Managed Tables please visit [the documentation](https://docs.cloudera.com/cdp-private-cloud-base/7.1.6/using-hiveql/topics/hive_create_an_external_table.html)


## Part 3: Create Hive Managed Tables from Cloud Storage in the CDW Virtual Warehouse

Exit Hue and navigate back to the CDW Database Catalog. 

Open the Atlas UI corresponding to the Virtual Warehouse where you executed the above queries.

![alt text](images/sdx2cml07.png)

Atlas has a lot of useful Data Governance features but those are beyond the scope of this demo. 

To access table metadata, simply enter their names in the bar at the top of the page and select the relevant result of type “Hive Table”.

![alt text](images/sdx2cml5.png)

The properties tab is opened by default. A lot of table metadata is stored here including table attributes, row counts, database information and more. 

![alt text](images/sdx2cml6.png)

Expand the “User-defined properties”, “Labels” and “Business Metadata” sections. You can use these to further categorize and then easily search your assets. 

![alt text](images/sdx2cml7.png)

The Lineage tab allows you to visualize your data as it is created, transformed, and persisted. Notice that all the below is created for you by default, without any user actions. 

Data, transformations and user actions are tracked by means of “Atlas Hooks”, powered by Kafka. CDP SDX manages this for you at the infrastructure level. 

![alt text](images/sdx2cml8.png)

![alt text](images/sdx2cml9.png)

![alt text](images/sdx2cml10.png)

Then create a custom classification for this Machine Learning Project by clicking on the “plus sign” icon. 
Notice existing classifications are shown by default. Pick a random classification and observe that Atlas model instances of different types are returned in the main screen.  

![alt text](images/sdx2cml11.png)

We will create a custom classification and apply it to our tables. 

![alt text](images/sdx2cml12.png)

Navigate back to the Atlas entity for each of the three tables. Open the classifications tab and apply the new classification. 

![alt text](images/sdx2cml13.png)

You can leave default options such as validity period to their default value. 

![alt text](images/sdx2cml14.png)

Repeat the same steps for “cc_info_table” and “bank_info_table”. 

Then navigate back to the Classifications tab and browse for all entities carrying it.


## Part 4: Access the Data in the CML Project via CML Data Connections


Navigate back to CML and create a new session using Jupyter Notebooks. Make sure to launch it with the following options (you can leave the rest to their defaults):

* Editor: JupyterLab
* Kernel: Python 3.7 or above
* Enable Spark: Optional
* Resource Profile: 2 vCPU / 4 GiB Mem

![alt text](images/sdx2cml15.png)

Once the session has started, the “Data Connections” page will immediately open. 
This window contains sample code to connect to any of your Hive or Impala Datawarehouses via Spark Hive Warehouse Connector or the Impyla Python library.

These are not just examples though. This is the code you need with the values you need to access your data, all prefilled for you. You can just copy and paste it into your notebook and execute it. 

Select the “Hive” option reflecting the Hive CDW Virtual Warehouse that you created your three tables with earlier. Copy the code to your clipboard and then close the window. 

![alt text](images/sdx2cml16.png)

Open the “1_Data_Access.ipynb” notebook and paste the code in the first open cell. Notice an old stub has already been entered for you, but the values are likely not the same needed for your Data Lake. 

![alt text](images/sdx2cml17.png)

Highlight the cell and execute the code. There are multiple ways to do so, but the fastest is to press “Shift” + “Enter” on your keyboard. 
You can also click on the “play” button or “Run” -> “Run Selected Cells” on the top pane. 

Notice the output in the cell is the output of the “SHOW DATABASES” query. 

![alt text](images/sdx2cml18.png)

You can modify the SQL syntax at will to execute more advanced queries. For example, you can use the same template to load data from Hive into a Pandas Dataframe. 

Scroll down in your notebook and execute the next cells. Notice that you are just updating the SQL syntax. The connection to the Hive Virtual Warehouse is the same. 

![alt text](images/sdx2cml19.png)

Before moving on, notice the Pandas dataframe shape is 1001 rows x 6 columns. This is the original data contained in the CSV file we loaded from Cloud Storage.


## Part 5: Restrict user access in the Ranger UI and observe changes in the CML Project

















