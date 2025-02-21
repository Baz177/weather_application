from flask import Flask, render_template, request
from weather import get_current_weather, get_lat_lon
from waitress import serve

app = Flask(__name__)  

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather') 
def weather():
    city = request.args.get('city')
    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = 'Baltimore' # Default city

    lat, lon, city_corrected, country = get_lat_lon(city)
    if lat is None or lon is None:
        return render_template('error.html')
    else: 
        weather_data = get_current_weather(lat, lon)
        if 'current' in weather_data:
            return render_template('weather.html',
                           title = city_corrected.capitalize(),
                           country = country.upper(),
                           status = weather_data['current']['weather'][0]['description'].capitalize(),
                           temp = f'{weather_data["current"]["temp"]}',
                           feels_like = f'{weather_data["current"]["feels_like"]}',
                           humidity = weather_data['current']['humidity'])
        else: 
            return render_template('error.html')

if __name__ == '__main__':
    #app.run(debug = True)
    serve(app, host = "0.0.0.0", port = 8000)