from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

FINNHUB_API_KEY = "d2ic8e1r01qgfkrllj40d2ic8e1r01qgfkrllj4g"
BASE_URL = "https://finnhub.io/api/v1/news"

@app.route('/')
def home():
    return "Welcome to the Finance News API using Flask + Finnhub!"

@app.route('/news', methods=['GET'])
def get_news():

    category = request.args.get('category', 'general')

    url = f"{BASE_URL}?category={category}&token={FINNHUB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        # Return only the top 5 articles for demo
        return jsonify(news_data[:5])
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
