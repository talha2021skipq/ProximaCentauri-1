import datetime
import urllib3
import constants as constants
from Cloudwatch_PutMetric import CloudwatchPutMetric
from S3bucket import S3Bucket as sb

def lambda_handler(event,context):
   
    CW = CloudwatchPutMetric()
    URLS_MONITORED = sb('sikandarbakhtskipq').load('urls_dict.json')
    K=list(URLS_MONITORED['URLS'][0].keys())
    values = {"URLS": []}
    
    #######################################################################################
    ##                              ALARM TRIGGER FOR URL # 1                            ##
    #######################################################################################
    dimensions=[
        {'Name': 'URL', 'Value': URLS_MONITORED['URLS'][0][K[0]]}
        ]
    
    avail = get_availibility(URLS_MONITORED['URLS'][0][K[0]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
    latency = get_latency(URLS_MONITORED['URLS'][0][K[0]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
                 
    val_dict={
        "availability": avail,
        "latency": latency
        }
    values['URLS'].append(val_dict)
    
    #######################################################################################
    ##                              ALARM TRIGGER FOR URL # 2                            ##
    #######################################################################################
    dimensions=[
        {'Name': 'URL', 'Value': URLS_MONITORED['URLS'][0][K[1]]}
        ]
    
    avail = get_availibility(URLS_MONITORED['URLS'][0][K[1]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
    latency = get_latency(URLS_MONITORED['URLS'][0][K[1]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
                 
    val_dict={
        "availability": avail,
        "latency": latency
        }
    values['URLS'].append(val_dict)
    
    #######################################################################################
    ##                              ALARM TRIGGER FOR URL # 3                            ##
    #######################################################################################
    dimensions=[
        {'Name': 'URL', 'Value': URLS_MONITORED['URLS'][0][K[2]]}
        ]
    
    avail = get_availibility(URLS_MONITORED['URLS'][0][K[2]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
    latency = get_latency(URLS_MONITORED['URLS'][0][K[2]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
                 
    val_dict={
        "availability": avail,
        "latency": latency
        }
    values['URLS'].append(val_dict)
    
    #######################################################################################
    ##                              ALARM TRIGGER FOR URL # 4                            ##
    #######################################################################################
    dimensions=[
        {'Name': 'URL', 'Value': URLS_MONITORED['URLS'][0][K[3]]}
        ]
    
    avail = get_availibility(URLS_MONITORED['URLS'][0][K[3]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
    latency = get_latency(URLS_MONITORED['URLS'][0][K[3]])
    CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
                 
    val_dict={
        "availability": avail,
        "latency": latency
        }
    values['URLS'].append(val_dict)
    
    return values

def get_availibility(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
def get_latency(url):
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET", url)
    end = datetime.datetime.now()
    delta = end - start
    latencySec = round(delta.microseconds * 0.000001, 6)
    return latencySec

    
    