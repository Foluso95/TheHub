from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Replace these with your actual keys
NEWS_API_KEY = "YOUR_ACTUAL_NEWS_API_KEY"
AIRLABS_API_KEY = "YOUR_ACTUAL_AIRLABS_API_KEY"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"

# APIs often block requests that don't look like they come from a browser
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TheHub/1.0"}


@app.route("/")
def home():
    news_articles = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        # NewsAPI Free Tier might block this on Vercel; we add a timeout and check status
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            news_articles = response.json().get("articles", [])
    except Exception as e:
        print(f"News fetch failed: {e}")  # This will show in Vercel Logs

    return render_template("index.html", wallet=ETH_WALLET, news=news_articles)


@app.route("/aviation")
def aviation():
    flights_data = []
    try:
        url = f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            flights_data = response.json().get("response", [])
            # Limit results to 15 flights so the page loads fast
            flights_data = flights_data[:15]
    except Exception as e:
        print(f"AirLabs fetch failed: {e}")

    return render_template("aviation.html", flights=flights_data)
