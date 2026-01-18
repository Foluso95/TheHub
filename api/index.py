from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# --- CONFIGURATION ---
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"

# Headers to prevent being blocked by API providers
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TheHub/1.0"}


@app.route("/")
def home():
    news_articles = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            news_articles = response.json().get("articles", [])
    except Exception as e:
        print(f"News Error: {e}")
    return render_template("index.html", wallet=ETH_WALLET, news=news_articles)


@app.route("/aviation")
def aviation():
    flights_data = []
    try:
        url = f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            flights_data = response.json().get("response", [])[:15]
    except Exception as e:
        print(f"AirLabs Error: {e}")
    return render_template("aviation.html", flights=flights_data)


@app.route("/wallet")
def wallet():
    return render_template("wallet.html", wallet=ETH_WALLET)
