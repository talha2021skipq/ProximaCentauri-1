# ProximaCentauri Sprint1
# WebHealth Monitor(Latency & Availability)

## Table of contents
* [Project Description](#Project-Description)
* [Technologies](#technologies)
* [Setup](#setup)


## Project Description
This aim of this project to to measure availability and latency of custom list (a json file placed in s3 bucket) using AWS CDK. It will update latency and availability after each 1 minu and will write metrics for latency and availability on cloudwatch using cloudwatch's API. Also set alarm to notify the subscriber when threshold for latency and avaialabilty is preached. Push SNS notification to subscriber using email address and also triger lambda and store alarm data into dynamodb when alarm generated. 
## Technologies 
Project is created with 
* Lambda
* CloudWatch
* DynamoDB
* SNS
* Cloud9
* S3

## SetUp
To run this project, follow these steps 
### Environment creation on AWS
First of all login in aws.amazon and create a virtual machine. 
### Update Python and AWS 
check version of python and if it is old version check new version is available then make new version as default version using these commands.
 ```
 $ python --version
 $ python3 --version
 $ source ~/.bashrc
 ```
 then add this line in bashrc file
```
$alis python='/usr/bin/python3' (press ESC on keybaord)
$:w! (press Enter on keybaord)
$:q! (press Enter on keybaord) 
```
check version of aws and then update it to new version using these commands.
````
$ aws --version 
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
````
### Create CDK project 
create directory of your choice and change directory to new created and then create cdk project using these commands. 
```
$ mkdir IrfanskipQ_Project1
$ cd IrfanskipQ_Project1
$ cdk init app --language python
```

### install requirements 
copy the files and update file in CDK project file. 
