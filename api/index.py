from flask import Flask, render_template
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"
PAYSTACK_LINK = "https://paystack.shop/pay/tskni695ms"


@app.route("/")
def home():
    news = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        res = requests.get(url, timeout=5)
        news = res.json().get("articles", [])
    except:
        pass
    return render_template("index.html", news=news)


@app.route("/aviation")
def aviation():
    combined_data = []
    try:
        live_res = (
            requests.get(
                f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}",
                timeout=10,
            )
            .json()
            .get("response", [])
        )
        for f in live_res:
            f["status_type"] = "LIVE"
            combined_data.append(f)
        sched_res = (
            requests.get(
                f"https://airlabs.co/api/v9/schedules?api_key={AIRLABS_API_KEY}",
                timeout=10,
            )
            .json()
            .get("response", [])
        )
        for s in sched_res:
            s["status_type"] = "SCHEDULED"
            combined_data.append(s)
    except:
        pass
    return render_template("aviation.html", flights=combined_data[:250])


@app.route("/travel-planning")
def travel_services():
    return render_template("travel_services.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html", paystack=PAYSTACK_LINK, wallet=ETH_WALLET)
