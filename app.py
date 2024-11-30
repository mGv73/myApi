from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import lxml
import os



app = Flask(__name__)
preUrl = "https://www.kleinskitchen.se/skolor/ies-huddinge/"
prePage = requests.get(preUrl) 
preSoup = BeautifulSoup(prePage.text, 'lxml')
divs = preSoup.find('div', class_ ='embed-container')
iframe = divs.find('iframe')
url = iframe['src']
page = requests.get(url) 
soup = BeautifulSoup(page.text, 'lxml')
days = soup.find_all('div', class_ ='row no-print day-alternative-wrapper')
day = days[12]
span = day.find('span')

print(span.text)








@app.route('/api/food', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({"food": f"{span.text}"})

# Start the server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 

#https://mpi.mashie.com/public/menu/kk+%C3%A4lvsj%C3%B6/8a1fcfe5