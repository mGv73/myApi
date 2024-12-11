from flask import Flask, request, Response, json
from bs4 import BeautifulSoup
import requests
import lxml
import os
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from dotenv import load_dotenv

#load_dotenv()
app = Flask(__name__)

def translate_text(text):
    url = "https://mymemory.translated.net/api/get"
    params = {
        "q": text,
        "langpair": f"sv|en"
    }
    response = requests.get(url, params=params)
    return response.json()["responseData"]["translatedText"]

def fetch_food_data(day):
    preUrl = "https://www.kleinskitchen.se/skolor/ies-huddinge/"
    prePage = requests.get(preUrl)

    preSoup = BeautifulSoup(prePage.text, 'lxml')
    divs = preSoup.find('div', class_='embed-container')

    iframe = divs.find('iframe')

    url = iframe['src']
    page = requests.get(url)  

    soup = BeautifulSoup(page.text, 'lxml')
    days = soup.find_all('div', class_='row no-print day-alternative-wrapper')

    

    number = set_day() * 3
    if number > 15:
        number = 15

    if day == "monday":
        number = 0
    elif day == "tuesday":
        number = 3
    elif day == "wednesday":
        number = 6
    elif day == "thursday":
        number = 9
    elif day == "friday":
        number = 12
    elif day == "saturday":
        number = 15
    elif day == "sunday":
        number = 15

    day = days[number]
    span = day.find('span')
    text = span.text

    if number >= 15:
        return f"Food on monday is: {translate_text(text)}"
    else:
        return f"Food today is: {translate_text(text)}"

def fetch_training_data():
    trainings = ['Smolov Jr', 'Team training', 'Smolov Jr and back + biceps', 'Team training', 'Smolov Jr', 'Legs', 'Team technique training']
    number = set_day()
    training = trainings[number]
    return training

def set_day():
    utc = datetime.now(timezone.utc)
    cet_now = utc + timedelta(hours=1)
    weekday = cet_now.weekday()
    return weekday


@app.route('/')
def home():
    return "Welcome to my API!"

@app.route('/api/food', methods=['GET'])
def get_food():
    day = request.args.get('day', 'today')
    food_data_raw = fetch_food_data(day)
    food_data = translate_text(food_data_raw)
    response = json.dumps({"food": food_data}, ensure_ascii=False)
    return Response(response, content_type="application/json; charset=utf-8")

@app.route('/api/training', methods=['GET'])
def get_training():
    training_data = fetch_training_data()
    response = json.dumps({"training": training_data}, ensure_ascii=False)
    return Response(response, content_type="application/json; charset=utf-8")

# Start the server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
