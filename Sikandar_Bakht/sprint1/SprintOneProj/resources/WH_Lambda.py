import datetime
import urllib3
import constants as constants
from Cloudwatch_PutMetric import CloudwatchPutMetric
from S3bucket import S3Bucket as sb

def lambda_handler(event,context):
    '''handles period lambda, collects metric data and sends it to cloudwatch'''
    CW = CloudwatchPutMetric()
    URLS_MONITORED = sb('sikandarbakhtskipq').load('urls_dict.json')
    K=list(URLS_MONITORED['URLS'][0].keys())
    values = {"URLS": []}
    
    
    #loop to iterate through list of urls and get metrics corresponding to each URL
    for i in range(len(K)):
        dimensions = [
        {'Name': 'URL', 'Value': URLS_MONITORED['URLS'][0][K[i]]}
        ]
    
        avail = get_availibility(URLS_MONITORED['URLS'][0][K[i]])
        CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
        latency = get_latency(URLS_MONITORED['URLS'][0][K[i]])
        CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
    
        val_dict={
            "availability": avail,
            "latency": latency
            }
        
        values['URLS'].append(val_dict)

    return values

def get_availibility(url):
    '''returns 1 if url is available, 0 if not'''
    
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
def get_latency(url):
    '''returns latency of given url in seconds'''
    
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET", url)
    end = datetime.datetime.now()
    delta = end - start
    latencySec = round(delta.microseconds * 0.000001, 6)
    return latencySec

    
    