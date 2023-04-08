import requests
from twilio.rest import Client

STOCK_SYMBOL = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "sfsjfksnjfbjksk" #random
NEWS_API_KEY = "shkhfkshfksd" #random
TWILIO_SID = "ksjfhksjfdhjksdjhfd"#random
TWILIO_AUTH_TOKEN = "sohfdiskhufks"#random

STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"


stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol":   STOCK_SYMBOL,
    "apikey":   STOCK_API_KEY,
}

response = requests.get(STOCK_API_ENDPOINT, stock_parameters)
stock_data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_stock_data = stock_data_list[0]
yesterday_stock_closing_price = float(yesterday_stock_data["4. close"])

day_before_yesterday_stock_data = stock_data_list[1]
day_before_yesterday_stock_closing_price = float(day_before_yesterday_stock_data["4. close"])

difference_stock_prices = yesterday_stock_closing_price - day_before_yesterday_stock_closing_price
percentage_difference = round((difference_stock_prices/yesterday_stock_closing_price) * 100)

up_down = None
if difference_stock_prices > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(percentage_difference) > 5:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_API_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"][:3]

    sms_news = [f"{STOCK_SYMBOL}: {up_down}{percentage_difference}%\nHeadline: {news['title']}.n\Brief: {news['description']}" for news in articles]
    client  = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for news in sms_news:
        message = client.messages.create(
            body= news,
            from_= "+132242353465", #random
            to= "+42u828949759782" #random
        )