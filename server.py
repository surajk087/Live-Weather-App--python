from flask import Flask, render_template, request
from weather import getCurrentWeather
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # check for empty strings or string with only spaces
    if not bool(city.strip()):
        city="kolkata"

    weatherData = getCurrentWeather(city)

    # city is not found by api
    if not weatherData['cod']==200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weatherData["name"],
        status=weatherData["weather"][0]["description"].capitalize(),
        temp=f'{weatherData["main"]["temp"]:.1f}',
        feels_like=f'{weatherData["main"]["feels_like"]:.1f}'
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
