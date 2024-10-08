from django.shortcuts import render
import requests

def weather_forecast(request):
    api_key = '810901f3c70f8754158b4bcc606047db'

    location = 'Chennai'
    temperature = None
    weather = None
    humidity = None
    wind_speed = None
    crops = ""

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    try:
        if lat and lon:
            url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
            location = f"{lat}, {lon}"
        else:
            location = request.GET.get('location', 'Chennai')
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

        response = requests.get(url)
        weather_data = response.json()

        if response.status_code == 200:
            temperature = weather_data['main']['temp']
            weather = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            crops = crop_suggestion(temperature)
        else:
            print("Error fetching weather data:", weather_data.get("message", "Unknown error"))

    except Exception as e:
        print("An error occurred:", e)

    context = {
        'location': location,
        'weather': weather if weather else 'Unavailable',
        'temperature': temperature if temperature is not None else 'Unavailable',
        'humidity': humidity if humidity is not None else 'Unavailable',
        'wind_speed': wind_speed if wind_speed is not None else 'Unavailable',
        'crops': crops,
    }

    return render(request, 'farming/weather.html', context)

def crop_suggestion(temperature):
    if temperature < 0:
        return "Too low for crops."
    elif 0 <= temperature < 10:
        return "Not suitable for crops."
    elif 10 <= temperature < 15:
        return "Wheat, Potato, Onion"
    elif 15 <= temperature < 20:
        return "Cauliflower, Carrots, Cabbage"
    elif 20 <= temperature < 25:
        return "Tomato, Brinjal, Radish"
    elif 25 <= temperature < 30:
        return "Sugarcane| Cucumber| Green Beans"
    elif 30 <= temperature < 35:
        return "Rice| Millets| Chilli"
    elif 35 <= temperature < 40:
        return "Maize, Sorghum, Groundnut"
    else:
        return "Pulses, Cotton, Turmeric"
