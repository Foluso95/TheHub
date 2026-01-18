from flask import Flask, render_template
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"
PAYSTACK_LINK = "https://paystack.shop/pay/tskni695ms"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TheHub/1.0"}


@app.route("/")
def home():
    news = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        res = requests.get(url, headers=HEADERS, timeout=5)
        news = res.json().get("articles", [])
    except:
        pass
    return render_template("index.html", wallet=ETH_WALLET, news=news)


@app.route("/aviation")
def aviation():
    flights = []
    try:
        url = f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        flights = res.json().get("response", [])[:20]
    except:
        pass
    return render_template("aviation.html", flights=flights)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html", paystack=PAYSTACK_LINK, wallet=ETH_WALLET)


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/wallet")
def wallet():
    return render_template("wallet.html", wallet=ETH_WALLET)
