import datetime
import urllib3
import constants as constants
from cloudwatch_putMetric import CloudWatchPutMetric

def lambda_handler(events, context):
	values = dict()
	cw = CloudWatchPutMetric()
	
	avail = get_availability()
	
	"""
	We provide the Name Value pair for our dimenions
	to be used as a parameter for put_metric_data to receive a response.
	""" 
	dimensions = [
		{"Name": "URL", "Value": constants.URL_TO_MONITOR}
		]
	
	cw.put_data(constants.URL_MONITOR_NAMESPACE,constants.URL_MONITOR_NAME_Availability, dimensions, avail)
	
	latency = get_latency()
	dimensions = [
		{"Name": "URL", "Value": constants.URL_TO_MONITOR}
		]
	
	cw.put_data(constants.URL_MONITOR_NAMESPACE,constants.URL_MONITOR_NAME_Latency, dimensions, latency)
	
	values.update({"availability":avail,"Latency":latency})
	return values

def get_availability():
	http = urllib3.PoolManager()
	response = http.request("GET", constants.URL_TO_MONITOR)
	if response.status==200:
		return 1.0
	else:
		return 0.0

def get_latency():
	http = urllib3.PoolManager()
	start = datetime.datetime.now()
	response = http.request("GET", constants.URL_TO_MONITOR)
	end = datetime.datetime.now()
	delta = end - start
	latencySec = round(delta.microseconds * .000001, 6)
	return latencySec