from django.shortcuts import render
from datetime import datetime,timedelta

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpRequest, response, request
from django.shortcuts import render
import requests
from django.views import View
import decimal
# Create your tests here.
class AddPost(View):
    def get(self,request):
        def gen():    
            utc_now = (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
            utc_2 = (datetime.utcnow() - timedelta(minutes=2) ).strftime("%Y-%m-%dT%H:%M:%SZ")      
            step = '15s'
            memList = []
            memQuery = requests.get(f'http://localhost:9090/api/v1/query_range?query=node_memory_MemAvailable_bytes&start={utc_2}&end={utc_now}&step={step}').json()
            for x in range(9):
                memList.append(round(int(memQuery['data']['result'][0]['values'][x][1])/1024/1024/1024,3)) 
            return memList
            
        mem = requests.get('http://localhost:9090/api/v1/query?query=node_memory_MemAvailable_bytes')
        memJson = mem.json()
        memValue = int(memJson['data']['result'][0]['value'][1]) /1024/1024/1024

        upTime = requests.get('http://localhost:9090/api/v1/query?query=node_time_seconds')
        upTimeJson = upTime.json()
        upTimeValue = float(upTimeJson['data']['result'][0]['value'][1])
        
        bootTime = requests.get('http://localhost:9090/api/v1/query?query=node_boot_time_seconds')
        bootTimeJson = bootTime.json()
        bootTimeValue = float(bootTimeJson['data']['result'][0]['value'][1])

        revTraffic = requests.get('http://localhost:9090/api/v1/query?query=node_network_receive_bytes_total{device=%22wlp2s0%22}') 
        revTrafficJson = revTraffic.json()
        revTrafficValue = float(revTrafficJson['data']['result'][0]['value'][1]) /1024/1024

        transTraffic = requests.get('http://localhost:9090/api/v1/query?query=node_network_transmit_bytes_total{device="wlp2s0"}') 
        transTrafficJson = transTraffic.json()
        transTrafficValue = float(transTrafficJson['data']['result'][0]['value'][1]) /1024/1024
        
        freeDisk = requests.get('http://localhost:9090/api/v1/query?query=node_filesystem_avail_bytes{mountpoint="/etc/hosts"}') 
        freeDiskJson = freeDisk.json()
        freeDiskValue = float(freeDiskJson['data']['result'][0]['value'][1]) /1024/1024/1024

        totaldisk = requests.get('http://localhost:9090/api/v1/query?query=node_filesystem_size_bytes{mountpoint="/etc/hosts"}') 
        totaldiskJson = totaldisk.json()
        totaldiskValue = float(totaldiskJson['data']['result'][0]['value'][1]) /1024/1024/1024

        usedDisk = totaldiskValue - freeDiskValue
        nodeTime = (upTimeValue - bootTimeValue) /60/60
        memList = gen()
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

def get_data(request):
    data = {
        "sale": 100,
        "customers": 10,
        "name": {
            "nam": "male",
            "duyen": "female",
        }
    }
    printItem = data['name']['duyen']
    # gender = printItem['nam']
    return HttpResponse(printItem)



