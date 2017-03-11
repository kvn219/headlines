import feedparser
from flask import Flask, render_template
from flask import request
from helpers import get_weather, get_rate

app = Flask(__name__)

RSS_FEEDS = {'bbc'            : 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn'            : 'http://rss.cnn.com/rss/edition.rss',
             'fox'            : 'http://feeds.foxnews.com/foxnews/latest',
             'iol'            : 'http://www.iol.co.za/cmlink/1.640',
             'fivethirtyeight': 'https://fivethirtyeight.com/all/feed'}

DEFAULTS = {'publication':'bbc',
            'city': 'London,UK',
            'currency_from':'GBP',
            'currency_to':'USD'}


@app.route("/")
@app.route("/<publication>")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customised currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html",
                           articles=feed['entries'],
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies)
                           )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
