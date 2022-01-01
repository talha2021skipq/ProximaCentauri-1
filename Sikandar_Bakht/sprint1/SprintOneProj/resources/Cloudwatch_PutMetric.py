import boto3
import constants as constants

class CloudwatchPutMetric:
    '''A wrapper class to access cloudwatch and store metric data'''

    def __init__(self):
        '''initialized cloudwatch boto3 client'''   
        self.client = boto3.client('cloudwatch')
        
    def put_data(self, namespace, metricName, dimensions, value):
        '''takes 2 strings: namespace, metric name
           one array containing atleast one dict: dimensions
        '''
        response = self.client.put_metric_data(
            Namespace = namespace,
            MetricData=
            [{
                 'MetricName': metricName,
                 'Dimensions': dimensions,
                 'Value': value
            }]
             )
        
    