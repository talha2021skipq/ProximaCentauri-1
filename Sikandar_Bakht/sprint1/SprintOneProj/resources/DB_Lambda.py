from __future__ import print_function
import json
import boto3
print('Loading function')

def lambda_handler(event, context):
    '''handles lambda for SNS notification. Performs alarm log update in DynamoDB Table'''
    message = event['Records'][0]['Sns']
    add_log(message, 'MonitorDB')
    return message


def add_log(msg, table_name):
    '''Takes: a dict and table name as input, writes to specified table and returns table relevant data'''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
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
