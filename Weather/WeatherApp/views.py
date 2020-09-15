from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=233f34f7caf9c1bf3e582b239fed25b2'

    error_message = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            #to check if city already exists
            existing_city_count = City.objects.filter(name=new_city).count()

            #if city doesn't exist in database
            if existing_city_count == 0:
                city_weather = requests.get(url.format(new_city)).json()

                if city_weather['cod'] == 200:
                    form.save()
                else:
                    error_message = 'City does not exist in the world!'
            else:
                error_message = 'City already exists in the database!'

        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city' : city.name,
            'temperature' : round(((city_weather['main']['temp']-32)*5)/9,1),
            'feels_like' : round(((city_weather['main']['feels_like']-32)*5)/9,1),
            'temperature_min' : round(((city_weather['main']['temp_min']-32)*5)/9,1),
            'temperature_max' : round(((city_weather['main']['temp_max']-32)*5)/9,1),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data' : weather_data, 'form' : form, 'message' : message, 'message_class' : message_class}

    return render(request,'WeatherApp/index.html',context)

def delete_city(request, city):
    City.objects.get(name=city).delete()
    return redirect('home')
