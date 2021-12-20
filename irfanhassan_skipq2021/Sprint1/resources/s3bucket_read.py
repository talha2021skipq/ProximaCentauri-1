import json
import boto3

s3= boto3.client('s3')

def lambda_handler(event,context):
    buket = "irfanskipq"
    file ="URLS.json"
    response= s3.get_object(Bucket=buket,Key=file)
    contetnt = response['Body']
    json_oject = json.loads(contetnt.read())
    list_url=[json_oject['link1'],json_oject['link2'],json_oject['link3'],json_oject['link4']]
    print(list_url)