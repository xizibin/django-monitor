from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpRequest, response, request
from django.shortcuts import render
import requests
from django.views import View
import decimal
# Create your tests here.
class AddPost(View):
    def get(self,request):
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
        context = {
        'mem' : memValue,
        'time':nodeTime,
        'inTraffic': revTrafficValue,
        'outTraffic': transTrafficValue,
        'freedisk': freeDiskValue,
        'useddisk': usedDisk
        
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



