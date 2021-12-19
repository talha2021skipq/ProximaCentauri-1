# ProximaCentauri sprint1
## WebHealth Monitor(Latency & Availability)

This aim of this project to to measure availability and latency of custom list (a json file placed in s3 bucket) using AWS CDK. It will update latency and availability after each 1 minu and will write metrics for latency and availability on cloudwatch using cloudwatch's API. Also set alarm to notify the subscriber when threshold for latency and avaialabilty is preached. Push SNS notification to subscriber using email address and also triger lambda and store alarm data into dynamodb when alarm generated. 
### Technologies for this application
#####Lambda
#####CloudWatch
#####DynamoDB
#####SNS
#####Cloud9
#####S3

