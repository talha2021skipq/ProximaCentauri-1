import datetime
import urllib3
import constants as constants
from Cloudwatch_PutMetric import CloudwatchPutMetric


def lambda_handler(event,context):
   
    values = dict()
    CW = CloudwatchPutMetric()
    
    dimensions=[
        {'Name': 'URL', 'Value': constants.URL_TO_MONITOR}
        ]
    
    avail = get_availibility()
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
    latency = get_latency()
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
                 
    values.update({
        "availability": avail,
        "latency": latency
        })
    return values

def get_availibility():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
def get_latency():
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET", constants.URL_TO_MONITOR)
    end = datetime.datetime.now()
    delta = end - start
    latencySec = round(delta.microseconds * 0.000001, 6)
    return latencySec

    
    