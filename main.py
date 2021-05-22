import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(city_name, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}".format(city_name, api_key)
    r = requests.get(api_url)
    return r.json()


@app.route('/results', methods=['post'])
def render_results():
    city_name = request.form['city']
    api_key = get_api_key()
    data = get_weather_results(city_name, api_key)
    temp = float("{0:.2f}".format(data["main"]["temp"]))
    temps = round((temp-32)*5/9, 2)
    feels_like = float("{0:.2f}".format(data["main"]["feels_like"]))
    feel_like = round((feels_like-32)*5/9, 2)
    weather = data["weather"][0]["main"]
    location = data["name"]
    return render_template('return_page.html', location=location, weather=weather, temp=temps, feels_like=feel_like)
print(get_weather_results("Butwal", get_api_key()))


if __name__ == '__main__':
    app.run(debug=True)