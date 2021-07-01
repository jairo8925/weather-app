from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import requests
import sys

app = Flask(__name__)

api_key = 'e07b8023530957662796387e1eca0337'
url = 'https://api.openweathermap.org/data/2.5/weather'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_city():
    city_name = request.form['city_name']

    r = requests.get(url, params={'q': city_name, 'appid': api_key, 'units': 'metric'})
    data = r.json()

    # print("NAME:", weather_info.get('name'))
    # print("TEMP:", weather_info.get('main').get('temp'))
    # print("DESC:", weather_info.get('weather')[0].get('main'))

    city = data.get('name').upper()
    degrees = round(int(data.get('main').get('temp')))
    state = data.get('weather')[0].get('main')

    offset = int(data.get('timezone'))
    ts = int(data.get('dt')) + offset
    local_hour = int(datetime.utcfromtimestamp(ts).strftime('%H'))

    day_state = None
    if 6 <= int(local_hour) <= 16:
        day_state = 'day'
    elif 17 <= int(local_hour) <= 23:
        day_state = 'evening-morning'
    elif 0 <= int(local_hour) <= 5:
        day_state = 'night'

    dict_with_weather_info = {'city': city,
                              'degrees': degrees,
                              'state': state,
                              'day_state': day_state}

    if all(dict_with_weather_info.values()):
        return render_template('add.html', weather=dict_with_weather_info)
    else:
        return render_template('index.html'), 404


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
