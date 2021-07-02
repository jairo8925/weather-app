import os
import sys
import requests
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.secret_key = os.urandom(24)
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
    cities_list = [x for x in query]
    cities_info = []
    for c in cities_list:
        r = requests.get(url, params={'q': c.name, 'appid': api_key, 'units': 'metric'})

        if r.status_code == 200:
            data = r.json()
        else:
            flash("The city doesn't exist!")
            app.config.update(SECRET_KEY=os.urandom(24))
            city = City.query.filter_by(name=c.name).first()
            db.session.delete(city)
            db.session.commit()
            return redirect('/')

        city = data.get('name').upper()
        degrees = round(int(data.get('main').get('temp')))
        state = data.get('weather')[0].get('main')

        offset = int(data.get('timezone'))
        dt = int(data.get('dt'))
        local_hour = get_local_hour(dt, offset)

        day_state = get_background_image(local_hour)

        weather_info = {'id': c.id, 'city': city, 'degrees': degrees, 'state': state, 'day_state': day_state}

        if all(weather_info.values()):
            cities_info.append(weather_info)

    return render_template('index.html', cities=cities_info)


@app.route('/add', methods=['POST'])
def add():
    city_name = request.form['city_name']
    exists = db.session.query(City.id).filter_by(name=city_name).first() is not None
    if exists:
        flash("The city has already been added to the list!")
        app.config.update(SECRET_KEY=os.urandom(24))
        return redirect('/')
    else:
        db.session.add(City(name=city_name))
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


def get_background_image(hour):
    if 6 <= int(hour) <= 16:
        return 'day'
    elif 17 <= int(hour) <= 23:
        return 'evening-morning'
    elif 0 <= int(hour) <= 5:
        return 'night'
    else:
        return 'day'


def get_local_hour(dt, offset):
    ts = dt + offset
    return int(datetime.utcfromtimestamp(ts).strftime('%H'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
