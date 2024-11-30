from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import lxml
import os



app = Flask(__name__)

def fetch_food_data():
    # Scrape the external website
    preUrl = "https://www.kleinskitchen.se/skolor/ies-huddinge/"
    prePage = requests.get(preUrl)
    
    # Check if request was successful
    if prePage.status_code != 200:
        return "Error fetching the page"

    preSoup = BeautifulSoup(prePage.text, 'lxml')
    divs = preSoup.find('div', class_='embed-container')
    
    if divs is None:
        return "Unable to find the embedded container"

    iframe = divs.find('iframe')
    if iframe is None or 'src' not in iframe.attrs:
        return "No iframe found with src attribute"

    url = iframe['src']
    page = requests.get(url)
    
    # Check if iframe page request was successful
    if page.status_code != 200:
        return "Error fetching the iframe page"

    soup = BeautifulSoup(page.text, 'lxml')
    days = soup.find_all('div', class_='row no-print day-alternative-wrapper')

    if len(days) < 13:
        return "Insufficient days data"

    day = days[12]  # Fetch the 13th day
    span = day.find('span')
    
    if span is None:
        return "No menu data available"

    return span.text




@app.route('/')
def home():
    return "Welcome to my API!"

@app.route('/api/food', methods=['GET'])
def get_food():
    food_data = fetch_food_data()
    return jsonify({"food": food_data})

# Start the server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 