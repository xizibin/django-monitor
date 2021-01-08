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

        nodeTime = (upTimeValue-bootTimeValue) /60/60
        return render(request,'mychart/chart.html',{'mem' : memValue,'time':nodeTime})

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



