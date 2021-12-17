import datetime
import urllib3
import constants as constants
from CW_putMetric import CloudWacthPutMetric

def lambda_handler(events, context):
    values=dict()

    #creating an instant our CWPM class
    cw=CloudWacthPutMetric();
    avail=get_availability()
    dimensions=[
                { 'Name':'URL', 'Value':  constants.URL_TO_MONITOR}
            ]

    #put the data to CW using put-metric-data(put_data) method
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME1A,dimensions,avail )
    #get value of latency
    latency=get_latency()
    #put latecny to cloudwatc 
    dimensions=[
                {   'Name':'URL', 'Value':  constants.URL_TO_MONITOR}
            ]

    #put the data to CW using put-metric-data(put_data) method
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME1L,dimensions,latency )
    #to get the values of metrics updated
    values.update({"availability": avail, "Latency": latency})
    return values
def get_availability():
    http=urllib3.PoolManager()
    response=http.request("GET", constants.URL_TO_MONITOR)
    if response.status==200:
        return 1.0
    else: return 0.0
def get_latency():
    http=urllib3.PoolManager()
    start =datetime.datetime.now()
    response=http.request("GET", constants.URL_TO_MONITOR)
    end=datetime.datetime.now()
    dif=end-start
    latency=round(dif.microseconds * 0.000001,6)
    return latency



    