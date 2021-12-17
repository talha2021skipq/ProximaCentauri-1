import boto3
import constants as constants
class CloudWacthPutMetric:
    def __init__(self):
        self.client=boto3.client('cloudwatch')
        
    def put_data(self,namespace, metricname, dimensions, value):
        response = self.client.put_metric_data(
            Namespace= namespace,
            MetricData=
            [
                {
                    'MetricName': metricname ,
                    'Dimensions':dimensions  ,
                    'Value': value
                }
            ]
            )