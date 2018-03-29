import os
from dotenv import load_dotenv, find_dotenv
import json
import urllib
from flask import request
import feedparser
from defaults import DEFAULTS, RSS_FEEDS

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

WEATHER_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

CURRENCY_KEY = os.environ.get("CURRENCY_API_KEY")
CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id={}'.format(
    CURRENCY_KEY)


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query, WEATHER_KEY)
    print(url)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"],
            'country': parsed['sys']['country']
        }
    return weather


def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]
