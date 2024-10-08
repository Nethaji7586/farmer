from django.urls import path
from .views import weather_forecast

urlpatterns = [
    path('weather/', weather_forecast, name='weather_forecast'),
]
