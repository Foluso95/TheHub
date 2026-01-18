from flask import Flask, render_template
import requests

app = Flask(__name__)

# --- ENTER YOUR ACTUAL KEYS HERE ---
NEWS_API_KEY = "your_news_api_key_here"
AIRLABS_API_KEY = "your_airlabs_api_key_here"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"


@app.route("/")
def home():
    # Fetch Top Aviation News from NewsAPI
    news_articles = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            news_articles = response.json().get("articles", [])
    except Exception as e:
        print(f"News fetch error: {e}")

    return render_template("index.html", wallet=ETH_WALLET, news=news_articles)


@app.route("/aviation")
def aviation():
    # Fetch Live Airborne Flights from AirLabs
    flights_data = []
    try:
        # AirLabs "flights" endpoint provides high-frequency live data
        url = f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            flights_data = response.json().get("response", [])
    except Exception as e:
        print(f"AirLabs fetch error: {e}")

    return render_template("aviation.html", flights=flights_data)


@app.route("/wallet")
def wallet():
    return render_template("wallet.html", wallet=ETH_WALLET)
