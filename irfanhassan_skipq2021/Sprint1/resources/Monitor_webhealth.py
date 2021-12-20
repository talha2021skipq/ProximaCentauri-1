import datetime
import urllib3
import constants as constant_
from cloud_watch import CloudWatch_PutMetric


def lambda_handler(event,context):
    value = dict()
    cloudwatch = CloudWatch_PutMetric();
    avail = availabilty_value()
    Dimensions=[
        {'Name': 'URL', 'Value': constant_.URL}
    ]
    cloudwatch.put_data(constant_.URL_NameSpace, constant_.URL_Aailibilty,Dimensions,avail)
    
    latency = latency_value()
    cloudwatch.put_data(constant_.URL_NameSpace, constant_.URL_Latency,Dimensions,latency)
    value.update({"availibility":avail,"latency":latency})
    return value
    
def availabilty_value():
    http = urllib3.PoolManager()
    response = http.request("GET", constant_.URL)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    

def latency_value():
    http = urllib3.PoolManager()
    begin = datetime.datetime.now()
    response = http.request("GET",constant_.URL)
    end = datetime.datetime.now()
    duration = end - begin
    latency_sec = round(duration.microseconds * 0.000001,6)
    return latency_sec
    