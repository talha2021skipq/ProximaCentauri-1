import boto3
import json

def lambda_handler(event, context):
    #write to database
    #resource = boto3.resource('dynamodb') 
    client_ = boto3.client('dynamodb')
    info = event['Records'][0]['Sns']['Message']
    info = json.loads(info)
    item = {
        'AlarmDetails': {'S': info}
            }
    client_.put_item(TableName="AbdullahTable", Item=item)