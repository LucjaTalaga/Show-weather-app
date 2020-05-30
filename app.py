from flask import Flask, render_template, request
from helpers import getData

app = Flask(__name__)

url = 'api.openweathermap.org/data/2.5/weather?q={city name}&appid={your api key}'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def main():
    city = 'Las Vegas'
    weatherData = getData(city)
    print("weatherData: ")
    print(weatherData)
    return render_template("main.html")



if __name__ == '__main__':
    app.run()
