from __future__ import print_function
import json
import boto3
print('Loading function')

def lambda_handler(event, context):
    
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']
    #print("From SNS: " + message)
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
    
'''  
    "EventSource": "aws:sns",

2021-12-20T04:05:05.491+05:00	"EventVersion": "1.0",

2021-12-20T04:05:05.491+05:00	"EventSubscriptionArn": "arn:aws:sns:us-east-2:315997497220:SprintOneProjStack-webHealthTopicD88C142D-VXX06M00QSJ6:af079335-16f4-4826-a852-52279bcb22ec",

2021-12-20T04:05:05.491+05:00	"Sns": {

2021-12-20T04:05:05.491+05:00	"Type": "Notification",

2021-12-20T04:05:05.491+05:00	"MessageId": "fd05a49a-10af-5186-9b72-fea3ac4eeae3",

2021-12-20T04:05:05.491+05:00	"TopicArn": "arn:aws:sns:us-east-2:315997497220:SprintOneProjStack-webHealthTopicD88C142D-VXX06M00QSJ6",

2021-12-20T04:05:05.491+05:00	"Subject": "ALARM: \"SprintOneProjStack-LatencyAlarmD644240E-1H4NE9GDB0DI9\" in US East (Ohio)",

2021-12-20T04:05:05.491+05:00	"Message": "{\"AlarmName\":\"SprintOneProjStack-LatencyAlarmD644240E-1H4NE9GDB0DI9\",\"AlarmDescription\":null,\"AWSAccountId\":\"315997497220\",\"NewStateValue\":\"ALARM\",\"NewStateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints [0.337675 (19/12/21 23:01:00)] was greater than the threshold (0.28) (minimum 1 datapoint for OK -> ALARM transition).\",\"StateChangeTime\":\"2021-12-19T23:05:05.304+0000\",\"Region\":\"US East (Ohio)\",\"AlarmArn\":\"arn:aws:cloudwatch:us-east-2:315997497220:alarm:SprintOneProjStack-LatencyAlarmD644240E-1H4NE9GDB0DI9\",\"OldStateValue\":\"OK\",\"Trigger\":{\"MetricName\":\"url_latency\",\"Namespace\":\"SikandarWebHealth\",\"StatisticType\":\"ExtendedStatistic\",\"ExtendedStatistic\":\"Average\",\"Unit\":null,\"Dimensions\":[{\"value\":\"www.skipq.org\",\"name\":\"URL\"}],\"Period\":60,\"EvaluationPeriods\":1,\"ComparisonOperator\":\"GreaterThanThreshold\",\"Threshold\":0.28,\"TreatMissingData\":\"\",\"EvaluateLowSampleCountPercentile\":\"\"}}",

2021-12-20T04:05:05.491+05:00	"Timestamp": "2021-12-19T23:05:05.350Z",

2021-12-20T04:05:05.491+05:00	"SignatureVersion": "1",

2021-12-20T04:05:05.491+05:00	"Signature": "P23xUOErVDastHOALP7UpGFzfXUE1e8QBiCiIkxxMsS3NucPkf2QmcezZaYGj+bs5UnyerxlKZqfzXTFFGwJS68MZiijNGd8OlrKHgJW8gp2ifclqSjjM5Dvut11CHeIrhJoO+HddmC8/e3XalYNkgcxxC8mAZSSckMkdVpLwWZaMBPX30d1k/VJkyZjqRjIiUiJyfPvrk9Qf77B0sMEqqFBtu7qdp+K3nrJp7VdnhPqQKJDgp0dLkOStXfYyxbIkubzodMU3GwA3Uj4COiqBMWNogj9sJfu6Ak4IbFx+qAQ88/QtrIiOovUegfThQdA4/zvp9gmeuzq8BcJIl5D1Q==",

2021-12-20T04:05:05.491+05:00	"SigningCertUrl": "https://sns.us-east-2.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem",

2021-12-20T04:05:05.491+05:00	"UnsubscribeUrl": "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:315997497220:SprintOneProjStack-webHealthTopicD88C142D-VXX06M00QSJ6:af079335-16f4-4826-a852-52279bcb22ec",

2021-12-20T04:05:05.491+05:00	"MessageAttributes": {}'''