Googlesheet to JSON -> S3
=========================

This Lambda function opens a Google Sheet using a Google API Service
Account (https://console.developers.google.com/apis/credentials). The
sheet must be shared with the service account.

The program then reads all elements in columns A and B, to create a 
key=>value pair which is encoded into JSON and uploaded to S3.

Example
-------

Google Sheet (with formulas calculating the values):

A | B
------ | ------
wood | 72
rubber | 12
glass | 34


Output:

    {"rubber": "34", "glass": "12", "wood": "72"}


Configuration
-------------
The python script requires two configuration files, config.json and 
credentials.json, as explained below.

config.json
-----------
The config.json file should contain the s3 and sheet parameters of
the Google Sheet you wish to open (...spreadsheets/d/_SHEETID_/edit...)
~~~json
{
  "s3_bucket": "spreadsheet-archive",
  "s3_key": "latest.json",
  "sheet_id": "1SyH5Np4cAAAAtQqMbI9yKylYsdH0AsX2dRaaaav3L4",
  "worksheet_name": "Statistics"
}
~~~

credentials.json
----------------
The credentials.json file should contain the JSON private key 
configuration downloaded for the service account when created in 
Google API Manager (within a certain project). 
See: https://developers.google.com/identity/protocols/OAuth2ServiceAccount
~~~json
{
  "type": "service_account",
  "project_id": "my-really-cool-project",
  "private_key_id": "someprivatekeyid",
  "private_key": "-----BEGIN PRIVATE KEY-----\n my very private key -----END PRIVATE KEY-----\n",
  "client_email": "myserviceaccount@myproject.iam.gserviceaccount.com",
  "client_id": "00000000000000",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lambda%40ft-security-issue-monitor.iam.gserviceaccount.com"
}
~~~


Testing locally
---------------
It is possible to test the script locally by running:
   
    /usr/bin/python2.7 main.py

Deployment onto Lambda
----------------------
The main.py, config.json and credentials.json file should be uploaded
to Lambda in a ZIP file. The environment should be set to Python 2.7 
with a timeout of ~30 seconds. RAM requirements depends on the data 
you are extracting, however 128MB will be plenty for most scenarios.

Other Deployments
-----------------
You can easily adapt the code to output the JSON locally (using file 
write), or upload to S3 when running locally on your machine if required.
