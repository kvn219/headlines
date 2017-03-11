import datetime
from flask import Flask, render_template, make_response
from helpers import get_weather, get_rate, get_news, get_value_with_fallback

app = Flask(__name__)


@app.route("/")
@app.route("/<publication>")
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    # get customised currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    # save cookies and return template
    response = make_response(render_template(
            "home.html",
            articles=articles,
            weather=weather,
            currency_from=currency_from,
            currency_to=currency_to,
            rate=rate,
            currencies=sorted(currencies))
    )
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from",
                        currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
