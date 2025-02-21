from dotenv import load_dotenv
from pprint import pprint
import requests
import os

# Load API key from .env file
load_dotenv(dotenv_path='C:\\Users\\bkt29\\OneDrive\\Desktop\\MLE_AI\\weather_app\\.venv\\.env')
API_KEY = os.getenv('API_KEY')

def get_lat_lon(city):  # function to get lat/lon
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json() 

    #lat = 39.2908816, lon = -76.610759, city_corrected = 'Baltimore'

    if geocode_data:  # Check if any results were returned
        lat = geocode_data[0]['lat']
        lon = geocode_data[0]['lon']
        city_corrected = geocode_data[0]['name']
        country_corrected = geocode_data[0]['country']
        return lat, lon, city_corrected, country_corrected
    else: 
        return None, None, None, None
    
def get_current_weather(lat = 39.2908816, lon = -76.610759):  # function to get current weather
    if lat is None or lon is None:
        return 'No City Found'
    else: 
        requests_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial'
        weather_data = requests.get(requests_url).json()
        return weather_data

if __name__ == '__main__':
    print('\n*** Get Current Weather ***\n')

    city_input = input('Please Enter a city: ')
    
    # Check for empty strings or string with only spaces
    if not bool(city_input.strip()):
        city_input = 'Baltimore' # Default city

    lat_city, lon_city, city_correct, country = get_lat_lon(city_input)
    if lat_city is None or lon_city is None:
        print('No City Found')
    else: 
        weather_data = get_current_weather(lat_city, lon_city)
        print('\n')
        pprint(f'Current weather in {city_correct.capitalize()}')
        pprint(weather_data['current']['weather'][0]['description'].capitalize())
        pprint(weather_data['current']['temp'])
        pprint(weather_data['current']['feels_like'])