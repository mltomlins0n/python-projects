import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
city = input('Enter a city: ')
base_url = 'http://api.openweathermap.org/data/2.5/weather?APPID={}&q={}'.format(os.getenv('API_KEY'), city)
weather_data = requests.get(base_url).json()

print('Request made to: ' + base_url)
pprint(weather_data)