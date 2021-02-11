from django.shortcuts import render
from .utils import get_data, set_up
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
from django.http import HttpResponse
import requests

# Create your views here.

def send_data(request):
    return render(request, 'show_data.html')


def show_data(request):
    return JsonResponse({'data': get_data()})
    # return render(request,'csv_data.html',context={'data':get_data()})




@csrf_exempt
def search_data(request):
    r = set_up()
    stock_list = []
    stock_dict = {}
    response = HttpResponse(content_type='text/csv')
    if request.method == 'POST':
        searched_data = request.POST.get('search')
        try:

            for equity in r.scan_iter(match='*' + str(searched_data).upper() + '*'):
                stock_list.append(r.hgetall(equity))
                stock_dict[searched_data] = r.hgetall(equity)

            # stock_list = []
            # for key in keys:
            #     data = r.hgetall(key)
            #
            #     stock_list.append(data)
            # print(stock_list)
        except Exception as e:
            "Something went wrong"
    return JsonResponse({'data': stock_list})


