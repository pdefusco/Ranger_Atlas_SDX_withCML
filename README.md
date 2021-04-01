# Data Integration with Machine Learning

This project is an entry level example of Data Matching in Cloudera Machine Learning (CML) and various other components of the Cloudera Data Platform (CDP) including the Shared Data Experience (SDX), Cloudera Operational Database (COD) and Cloudera DataWarehousing (CDW).

## Project Overview

This project showcases CML Sessions to run [Splink](https://github.com/moj-analytical-services/splink), an Open Source Spark library created by the UK MOJ to implement probabilistic record linkage at scale. The Splink libray implements the fastLink R package which is discussed in more detail in [a paper by Harvard and Princeton Researchers](https://imai.fas.harvard.edu/research/files/linkage.pdf)

With probabilistic record linkage, up to millions of records can be compared to identify matches and duplicates across multiple sources. This is a dramatic improvement over past approaches.

CML is a user-friendly Managed Service for Data Scientists and Engineers to develop and deploy Machine Learning models. Among its many benefits, CML makes it easy to run Spark on Kubernetes.

However, a Spark cluster is not enough to reap the benefits at scale. One must work with tools that manage metadata, lineage, security, and datasets at scale. We will implement our workflow in CML but touch on other complimentary services in CDP that are essential to the project's success.


## Project Build 

Notebooks are labeled in numerical order. More notes are contained in each.

Before running the notebooks, don't forget to install the requirements and set environment variables.

#### Installing Requirements

CML Sessions allow you to run code in Python, Scala, Java, and R via your preferred Editor e.g. Jupyter Notebooks. For more on CML Projects and Sessions, please visit [this site](https://docs.cloudera.com/machine-learning/1.1/projects/topics/ml-projects.html)

Launch a CML Session with the "Workbench" editor. Next, open the terminal and issue the following command: "pip3 install -r requirements.txt". This will install all project dependencies.

#### Setting Environment Variables

CML projects allow you to set environment variables for reuse. Navigate to "Project Settings" on the left bar and open the "Advanced" tab.

Add the following environment variables:

* WORKLOAD_USER
* WORKLOAD_PASSWORD
* IMPALA_HOST
* OPDB_ENDPOINT
* ATLAS_ENDPOINT

The workload user and password are your CDP user credentials. As we will see in the notebooks, these can be reused to access multiple services within a single environment with one set of credentials/roles.


To find the Impala host, navigate to the CDP Home Page and open the CDW service. Select an Impala warehouse and click on "Copy JDBC URL" as shown below

![alt_text](https://github.com/pdefusco/myimages_repo/blob/main/Impala_copyurl.png)


To find the OpDB endpoint, naviate to the CDP Home Page and open the COD service. Select the database instance you will connect to, and open the "Phoenix (Thin)" tab.

Copy the url value from the JDBC URL string. You only need to copy starting from "https" and up to and including "avatica"

For example: "https://cod-xxxxx-gatewayxxxx.demo-aws.xxxxx.cloudera.site/cod-xxxxx/cdp-proxy-api/avatica"

![alt_text](https://github.com/pdefusco/myimages_repo/blob/main/COD_screenshot.png)


Finally, to find the Atlas endpoint navigate to the CDP Management Console, select your Cloud Provider environment, go to Data Lake, open the "Endpoints" tab and copy the Atlas endpoint.

Next, replace "/cdp-proxy-api/atlas/api/atlas/" with ":31443/api/atlas/v2/" and save this as your last environment variable.


#### 1 A and B

These notebooks introduce two basic Record Linkage examples with the Python Record Linkage library. Open a new CML Session and select Jupyter Notebooks as editor. A relatively small CPU/Mem value will suffice (e.g. 2 CPU's / 4 GB mem / 0 GPU's)

Simply run the cells in the notebooks by either selecting "Cell" -> Run All". Alternatively, run one cell at a time by pressing "Shift - Enter" on each. 


#### 2 A - Atlas Client Example

Atlas relies on an entity model to track tables, jobs, ML models, and many more assets and workloads across the CDP ecosystem. For example, when a Hive External table is created via Spark SQL, Atlas automatically tracks its metadata, lineage, and more. 

This notebook shows how to create custom Atlas types and instantiate them directly from a CML session via the Python Atlas Client, effectively expanding the default Atlas schema.


#### 2 B - PhoenixDB Client Example

The Cloudera Operational Database experience allows you to create a new operational database with a single click and auto-scales based on your workload.

This notebook shows how to connect to a COD database via the Phoenix client for Python. 

In the notebook you will create a Pheonix table and upsert data held in a local folder in CML.

The data used in this notebook will then be used by the ER algorithm in notebook 3. 


#### 2 C - Hive Client Example

CML allows you to easily run Spark on Kubernetes. When you create a Spark table, this is automatically tracked by Hive as an External table. 

In this notebook you will create a Spark table from a Spark dataframe.

The data used in this notebook will also be used by the ER algorithm in notebook 3 for comparing entities. 


##### 2 D - Impala Clients Example

The Cloudera DataWarehouse Experience allows you to easily provison independent data warehouses and data marts that auto-scale up and down to meet varying workload demands. The Datawarehouse service provides isolated compute instances for each data warehouse/mart, optimization, and enables you to save costs while meeting SLA's. 

In this notebook you will create an Impala table and upsert data directly in it via two Impala clients. The Jaydebeapi library is faster while the Impyla library offers additional options to connect to Hive and other data sources.


##### 3 - End to End Workflow

The Splink library allows you to compare different datasets at scale and find records that are likely matches. A likely match implies the same real-world entity is present in both source datasets.

* First we launch a Spark on Kubernetes Session and load the required Jars.
* We then load the two datasets for the comparison from Phoenix and Hive. These are the same tables we created in the preceding notebooks.
* We run the Linkage algorithm on the two datasets and filter for entities that are likely matches.
* Similar to notebook 2 A, we create custom metadata types and entities in Atlas reflecting this workflow.
* After some brief data cleaning we save the data into Impala via the Jaydebeapi library 
* Finally, we augment our metadata and lineage graph by creating a new process reflecting lineage from Spark to Impala



![alt text](https://github.com/pdefusco/myimages_repo/blob/main/ER_atlas_lineage.png)
