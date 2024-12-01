from flask import Flask, request, Response, json
from bs4 import BeautifulSoup
import requests
import lxml
import os
from datetime import datetime, timedelta

app = Flask(__name__)

def fetch_food_data():
    preUrl = "https://www.kleinskitchen.se/skolor/ies-huddinge/"
    prePage = requests.get(preUrl)

    preSoup = BeautifulSoup(prePage.text, 'lxml')
    divs = preSoup.find('div', class_='embed-container')

    iframe = divs.find('iframe')

    url = iframe['src']
    page = requests.get(url)  

    soup = BeautifulSoup(page.text, 'lxml')
    days = soup.find_all('div', class_='row no-print day-alternative-wrapper')

    number = set_day()
    if number >= 15:
        return "Other food"
    else:
        day = days[number]
        span = day.find('span')

    return span.text

def set_day ():
    utc = datetime.utcnow()
    cet_now = utc + timedelta(hours=1)
    weekday = cet_now.weekday()
    number = (2 - 1) * 3
    return number


@app.route('/')
def home():
    return "Welcome to my API!"

@app.route('/api/food', methods=['GET'])
def get_food():
    food_data = fetch_food_data()
    response = json.dumps({"food": food_data}, ensure_ascii=False)
    return Response(response, content_type="application/json; charset=utf-8")

# Start the server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 