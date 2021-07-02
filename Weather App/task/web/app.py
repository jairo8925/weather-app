import os
import sys
import requests
from datetime import datetime
from flask import Flask, abort, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)
url = 'https://api.openweathermap.org/data/2.5/weather'

try:
    api_key = str(os.environ["API_KEY"])
except KeyError:
    sys.exit("Can't find api_key!")


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<City %r>' % self.name


db.drop_all()
db.create_all()


@app.route('/')
def index():
    query = City.query.all()
    cities_list = [x.name for x in query]
    cities_info = []
    for city_name in cities_list:
        r = requests.get(url, params={'q': city_name, 'appid': api_key, 'units': 'metric'})

        if r.status_code == 200:
            data = r.json()
        else:
            return render_template('index.html')

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

        weather_info = {'city': city, 'degrees': degrees, 'state': state, 'day_state': day_state}

        if all(weather_info.values()):
            cities_info.append(weather_info)

    return render_template('index.html', cities=cities_info)


@app.route('/add', methods=['POST'])
def add_city():
    city_name = request.form['city_name']
    exists = db.session.query(City.id).filter_by(name=city_name).first() is not None
    if exists:
        print("City already exists")
    else:
        db.session.add(City(name=city_name))
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
