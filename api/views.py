from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .apps import ApiConfig
from .models import Weather
from .utils import transform_data_to_my_format, CityStorage

import requests
import json
import datetime

cities = CityStorage()

@csrf_exempt
def index(request):
    return HttpResponse('Hello, API V1')


@csrf_exempt
def getWeatherInCity(request, city):
    if request.method == 'GET':
        openweather_url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&appid={ ApiConfig.api_key }'

        respose = requests.get(openweather_url) 
        if respose.status_code == 200:
            data = respose.json()
            transformed_data = transform_data_to_my_format(data)
            Weather.insert(transformed_data)

            return HttpResponse(json.dumps(transformed_data))
        else:
            return HttpResponseBadRequest('City Not Founded')

    else:
        return HttpResponseNotAllowed('Use GET')


@csrf_exempt
def getStoredWheatherData(request):
    if request.method == 'POST':
        args = list()
        try:
            if request.body:
                args = json.loads(request.body)
            else: 
                args = {}
            data = Weather.custom_selector(**args)
            data = json.dumps(data)

        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()
        except Exception as error:
            return HttpResponse(error.__repr__())
        return HttpResponse(data)    

    else:
        return HttpResponseNotAllowed('Use POST')


@csrf_exempt
def getCities(request, symbols):
    print(symbols.lower())
    data = json.dumps(cities.get_cities_on_char(symbols))
    return HttpResponse(data)
    