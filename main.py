"""
NAME  : weatherapi.py
AUTHOR: Alexandre Fukaya
DATE  : Wed Dec  4 08:01:25 2019

DESCRIPTION:
    The script connects to Openweathermap weather API and retrieves the weather
    info for a given location - Web.

USAGE:
    Just run it.

DEPENDENCIES:
    Flask
    Requests

TODO:
    - Create a ZIP to City relationship.

INPROGRESS:
    - None.

CHANGES:
    20191204 - Configuração Inicial.

"""

import requests

from flask import Flask, render_template, request

api_call = 'http://api.openweathermap.org/data/2.5/weather?q='
api_key  = 'appid=2f752b9eaccbf9ae2ac08e243b22da1e'
#api_key  = 'appid=b6907d289e10d714a6e88b30761fae22'

app = Flask(__name__)

def Convert2Celcius(temp):
    return temp - 273.15

def Convert2Fahrenheit(temp):
    return (temp - 273.15) * 9/5 + 32

@app.route('/temperature',methods=['POST'])
def temperature():
    try:
        location = request.form['location'] 
        scale    = request.form['degrees']
        city,country = location.split(',')

        url = api_call + location + '&' + api_key
        
        r = requests.get(url)

        print('---> {}'.format(city))
        print('---> {}'.format(country))
        print('---> {}'.format(url))
        print('---> Request Status: {}'.format(r.reason))
        
        if r.ok:
            weather_info = r.json()
            info_temp    = weather_info['main']['temp']
            info_weather = weather_info['weather'][0]['description']
            info_maxtemp = weather_info['main']['temp_max']
            info_mintemp = weather_info['main']['temp_min']

            if scale == 'C' :
                temperature = round(Convert2Celcius(info_temp),1)
                temp_min    = round(Convert2Celcius(info_mintemp),1)
                temp_max    = round(Convert2Celcius(info_maxtemp),1)
            else :
                temperature = round(Convert2Fahrenheit(info_temp),1)
                temp_min    = round(Convert2Fahrenheit(info_mintemp),1)
                temp_max    = round(Convert2Fahrenheit(info_maxtemp),1)

            return render_template('index.html', city = city.capitalize(), country = country.upper(), info_weather = info_weather, temperature = temperature, temp_min = temp_min, temp_max = temp_max, scale = scale)
        else :
            return render_template('error.html',error = r.reason)
    except:
        return render_template('error.html',error = "Oops the country is missing...")

@app.route('/')
def index():
    return render_template('index.html',city = '', info_weather = '', temp = '', temp_min = '', temp_max = '', scale = '')

