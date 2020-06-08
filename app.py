from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from helpers import getData

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/main', methods=["GET", "POST"])
def main():

    # adding new city to the database
    if request.method == "POST":
        city = request.form.get("name")
        if city:
            city_to_add = Weather(name=city)
            if Weather.query.filter_by(name=city).first() is None:
                db.session.add(city_to_add)
                db.session.commit()

    # getting all cities
    cities = Weather.query.all()
    print("cities : ")
    print(cities)
    # if there are more than cities, delete the first one
    if len(cities) > 5:
        to_delete = Weather.query.first()
        db.session.delete(to_delete)
        db.session.commit()
        cities.pop(0)

    all_weather_data = []
    alert = None
    for city in reversed(cities):
        weather_data = getData(city.name)
        if(weather_data["cod"] == '404'):
            alert = city.name
            to_delete = Weather.query.filter_by(name=city.name).first()
            db.session.delete(to_delete)
            db.session.commit()
        else:
            weather_to_add = {
                "city": weather_data["name"],
                "temp": round((weather_data["main"]["temp"] - 273.15), 1),
                "text": weather_data["weather"][0]["description"],
                "icon": weather_data["weather"][0]["icon"]
            }
            all_weather_data.append(weather_to_add)
        print(weather_data)

    return render_template("main.html", alert=alert, weather_list=all_weather_data)


@app.route('/main/<city>')
def city(city):
    weather_data = getData(city)
    weather = {
        "city": city,
        "temp": round((weather_data["main"]["temp"] - 273.15), 1),
        "temp_feels": round((weather_data["main"]["feels_like"] - 273.15), 1),
        "temp_min": round((weather_data["main"]["temp_min"] - 273.15), 1),
        "temp_max": round((weather_data["main"]["temp_max"] - 273.15), 1),
        "pressure": weather_data["main"]["pressure"],
        "humidity": weather_data["main"]["humidity"],
        "wind": weather_data["wind"]["speed"],
        "cloudiness": weather_data["clouds"]["all"],
        "desc": weather_data["weather"][0]["main"],
        "icon": weather_data["weather"][0]["icon"]
    }
    return render_template("city.html", weather=weather)


if __name__ == '__main__':
    app.run()
