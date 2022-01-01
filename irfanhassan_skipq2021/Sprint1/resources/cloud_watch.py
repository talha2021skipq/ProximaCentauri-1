import boto3
import constants 


class CloudWatch_PutMetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        
    def put_data(self, Space_Name, Matric_Name, Dimension, Value):
        response = self.client.put_metric_data(
            Namespace = Space_Name,
            MetricData=[{ 'MetricName':Matric_Name, 'Dimensions':Dimension,'Value':Value}]
            )