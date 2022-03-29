import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY_FOR_STOCK = "HQ4NDISIP2TZYXGB"
API_KEY_FOR_NEWS = "93a9c5b2dd5944c1ba3ec64757235763"

Twilio_Sid = "ACc877ee94b33b5d4236955c56a115c4f4"
Twilio_Auth_Token = "cc5623f4362ee36435bc524aa0e5360e"
client = Client(Twilio_Sid, Twilio_Auth_Token)

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY_FOR_STOCK
}

new_params = {
    "apiKey": API_KEY_FOR_NEWS,
    "qInTitle": COMPANY_NAME,
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterdays_data = data_list[0]
yesterdays_closing_price = yesterdays_data["4. close"]

day_before_yesterdays_data = data_list[1]
day_before_yesterdays_closing_price = day_before_yesterdays_data["4. close"]

diff_in_price = float(day_before_yesterdays_closing_price) - float(yesterdays_closing_price)
up_down = None
if diff_in_price > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percent_diff = round((diff_in_price / float(yesterdays_closing_price)) * 100)

if abs(percent_diff) > 1:
    response = requests.get(NEWS_ENDPOINT, params=new_params)
    articles = response.json()["articles"]
    three_articles = articles[:3]
    formatted_news = [f"{STOCK_NAME} {up_down} {abs(percent_diff)} (%) \n Headline:{item['title']}"
                      f" \n Brief: {item['description']}" for item in three_articles]
    for i in formatted_news:
        message = client.messages \
            .create(
            body=i,
            from_='+15867017861',
            to='+2348130207733'
        )
