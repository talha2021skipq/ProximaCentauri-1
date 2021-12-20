from __future__ import print_function
import json
import boto3
print('Loading function')

def lambda_handler(event, context):
    
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']
    add_log(message)
    return message


def add_log(msg):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MonitorDB')
    data = json.loads(msg['Message'])
    response = table.put_item(Item = {'Timestamp': msg['Timestamp'], 
                                    'Alarm Name':data['AlarmName'],
                                    'Alarm Description':data['AlarmDescription'],
                                    'AWS Account Id':data['AWSAccountId'],
                                    'URL':data['Trigger']['Dimensions'][0]['value'],
                                    'Metric Name':data['Trigger']['MetricName'],
                                    'Namespace':data['Trigger']['Namespace'],
                                    'OldStateValue':data['OldStateValue'],
                                    'NewStateValue':data['NewStateValue'],
                                    'NewStateReason':data['NewStateReason'],
                                    'Region':data['Region'],
                                    'Statistic':data['Trigger']['ExtendedStatistic'],
                                    'Threshold':str(data['Trigger']['Threshold'])
                                    }
                                 )
    return response
