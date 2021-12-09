# Machine Learning with the Cloudera Shared Data Experience

This project showcases how to create models in a secure, governed and fully audited manner. 

WIP

CML is not just a Machine Learning platform. It's a ML platform founded on an end to end Data Platform. 

SDX is a fundamental part of Cloudera Data Platform architecture, unlike other vendors’ bolt-on approaches to security and governance. 
Independent from compute and storage layers, SDX delivers an integrated set of security and governance technologies built on metadata and delivers persistent context across all analytics as well as public and private clouds. 
Consistent data context simplifies the delivery of data and analytics with a multi-tenant data access  model that is defined once and seamlessly applied everywhere.
SDX reduces risk and operational costs by delivering consistent data context across deployments. IT can deploy fully secured and governed data lakes faster, giving more users access to more data, without compromise. 

CDP Separates Storage, Comoute and Context. 

* You can track lineage between datasets and models in Atlas, testifying how a model was trained including which features were used, at what time training occurred, and other custom metadata.
* With Ranger Audits, you can trace back to every attempt to access your datasets, wether it succeeded or failed
* Ranger allows you to enforce row and column level masking rules can be applied to datasets used to train/validate/test models. In other words, not only can Data Scientists can be prevented from accessing subsets of the data, but you can prove that they weren't able to do so. 
* In CML, Models are protected by Authentication Constraints. Every response requires authentication.
* Every response issued by a model is tracked by the system and tagged with a unique identifier. Custom metrics can be tracked for each prediction. ML Users can then access the predictions and monitor model inference, subject to permissions.



To learn more on SDX please visit [this page](https://www.cloudera.com/products/sdx.html)

## Project Summary

1. Create a Hive table in CDW. Obrserve the table being automatically tracked in Atlas
2. Read the data into a CML Session using the CML Session Data Connections feature
3. Query the data with a simple select * from CML
4. Go back to Ranger. Enforce column masking on the same table 
5. Come back to the CML session and rerun the same query. Notice the column is now hidden
6. Train a ML model with the table and push the model to a REST Endpoint via CML API V2
7. Observe in Atlas that lineage was created

### Bonus Exercises

1. Customize the yml file by adding feature metadata
2. Use the Python Atlas client to create custom entities and lineage graphs in Atlas
3. Use row level masking in Ranger to train a model with a subset of table rows
4. Test a sample request to your model via authentication





