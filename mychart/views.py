from django.shortcuts import render
from datetime import datetime,timedelta

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpRequest, response, request
from django.shortcuts import render
import requests
from django.views import View
import decimal
# Create your tests here.
class queryRange():
    def __init__(self,metric,timeRange,step):
        self.timeRange = timeRange 
        self.metric = metric
        self.step = step
    def getTime(self):
        timeList = []
        utc_now = (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        utc_range = (datetime.utcnow() - timedelta(minutes=self.timeRange) ).strftime("%Y-%m-%dT%H:%M:%SZ")     
        rangeList = round(int(self.timeRange)*60/int(self.step) + 1) 
        metricQuery = requests.get(f'http://localhost:9090/api/v1/query_range?query={self.metric}&start={utc_range}&end={utc_now}&step={self.step}').json()
        for x in range(rangeList):
            timeList.append(datetime.fromtimestamp(metricQuery['data']['result'][0]['values'][x][0]).strftime("%H:%M:%S"))
        return timeList
    def getMetric(self):
        metricList = []
        utc_now = (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        utc_range = (datetime.utcnow() - timedelta(minutes=self.timeRange) ).strftime("%Y-%m-%dT%H:%M:%SZ")     
        rangeList = round(int(self.timeRange)*60/int(self.step) + 1) 
        metricQuery = requests.get(f'http://localhost:9090/api/v1/query_range?query={self.metric}&start={utc_range}&end={utc_now}&step={self.step}').json()
        for x in range(rangeList):
            metricList.append(round(int(metricQuery['data']['result'][0]['values'][x][1]),3))   
        return metricList

class queryInstant():
    def __init__(self,metric):
        self.metric = metric
    def getMetric(self):
        metric = requests.get(f'http://localhost:9090/api/v1/query?query={self.metric}').json()
        metricValue = round(float(metric['data']['result'][0]['value'][1]),3)
        return metricValue

class AddPost(View):
    def get(self,request):
        memValue = queryInstant('node_memory_MemAvailable_bytes').getMetric()
        upTimeValue = queryInstant('node_time_seconds').getMetric()
        bootTimeValue = queryInstant('node_boot_time_seconds').getMetric()
        totaldiskValue = queryInstant('node_filesystem_size_bytes{mountpoint="/etc/hosts"}').getMetric()
        freeDiskValue = queryInstant('node_filesystem_avail_bytes{mountpoint="/etc/hosts"}').getMetric()
        memList = queryRange('node_memory_MemAvailable_bytes',1,2).getMetric()
        revTrafficValue = queryInstant('node_network_receive_bytes_total{device=%22wlp2s0%22}').getMetric()
        transTrafficValue = queryInstant('node_network_transmit_bytes_total{device="wlp2s0"}').getMetric()
        usedDisk = totaldiskValue - freeDiskValue
        nodeTime = (upTimeValue - bootTimeValue) /60/60
        context = {
        'mem' : memValue,
        'time':nodeTime,
        'inTraffic': revTrafficValue,
        'outTraffic': transTrafficValue,
        'freedisk': freeDiskValue,
        'useddisk': usedDisk,
        'memList0' : memList[0],    
        'memList1' : memList[1],
        'memList2' : memList[2],
        'memList3' : memList[3],
        'memList4' : memList[4],
        'memList5' : memList[5],
        'memList6' : memList[6],
        'memList7' : memList[7],
        'memList8' : memList[8],

        }  

        return render(request,'mychart/chart.html',context)





