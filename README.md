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
### Insatll requirements
Then install new version of python (python 3.7) and console (2.1).
### Create CDK project 
create directory of your choice and change directory to new created and then create cdk project using these commands. 
```
$ mkdir IrfanskipQ_Project1
$ cd IrfanskipQ_Project1
$ cdk init app --language python
```
copy the files and update file in CDK project file. 
