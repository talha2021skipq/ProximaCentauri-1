import boto3
import constants as constants

class CloudwatchPutMetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        
    def put_data(self, namespace, metricName, dimensions, value):
        response = self.client.put_metric_data(
            Namespace = namespace,
            MetricData=
            [{
                 'MetricName': metricName,
                 'Dimensions': dimensions,
                 'Value': value
            }]
             )
        
    