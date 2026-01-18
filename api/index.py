from flask import Flask, render_template
import requests

app = Flask(__name__)

# Primary and Fallback API Keys
API_KEYS = ["e6f87644-fdb1-4963-a391-1d66b790ded0", "39bbc467ab07459396692bfbc8564151"]

ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"


@app.route("/")
def home():
    return render_template("index.html", wallet=ETH_WALLET)


@app.route("/aviation")
def aviation():
    flights_data = []
    for key in API_KEYS:
        try:
            url = f"http://api.aviationstack.com/v1/flights?access_key={key}&limit=50"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                flights_data = response.json().get("data", [])
                if flights_data:
                    break
        except:
            continue
    return render_template("aviation.html", flights=flights_data)


@app.route("/wallet")
def wallet():
    return render_template("wallet.html", wallet=ETH_WALLET)
