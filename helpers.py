import os
from dotenv import load_dotenv, find_dotenv
import json
import urllib

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

print('-' * 90, WEATHER_API_KEY)


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query, WEATHER_API_KEY)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
                   "city"       : parsed["name"]
                   }
    return weather
