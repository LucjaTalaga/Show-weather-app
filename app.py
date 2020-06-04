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
    for city in cities:
        weather_data = getData(city.name)
        if(weather_data["cod"] == '404'):
            alert = city.name
        print(weather_data)

    return render_template("main.html", alert=alert)


if __name__ == '__main__':
    app.run()
