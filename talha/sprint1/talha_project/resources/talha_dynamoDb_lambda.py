import json
from db_putdata import dynamoTablePutData

def lambda_handler(events, context):
    db = dynamoTablePutData();#creating an instance of my putdata class
    message = events['Records'][0]['Sns']['Message']
    message = json.loads(message)
    parsed_message =  message['AlarmName']
    createdDate = message['StateChangeTime']
   # reason=message['ReasonforStateChange']
    db.dynamo_data("TalhaAlarmTable", parsed_message, createdDate)
