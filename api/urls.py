from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('getWeather/<str:city>', views.getWeatherInCity),
    path('getStoredData', views.getStoredWheatherData),
    path('cities/<str:symbols>', views.getCities)
]