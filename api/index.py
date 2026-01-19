from flask import Flask, render_template, make_response, send_from_directory
import requests
import os

app = Flask(__name__)

# --- CENTRAL HUB CONFIGURATION ---
PAYSTACK_DATA_LOGS = "https://paystack.shop/pay/tskni695ms"
PAYSTACK_SUPPORT = "https://paystack.shop/pay/m2091khojf"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"
WHATSAPP_HUB = "https://wa.me/2349063350998"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"


@app.route("/")
def home():
    news = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation+intelligence&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        news_data = requests.get(url, timeout=5).json().get("articles", [])
        news = news_data
    except:
        pass
    return render_template("index.html", news=news)


@app.route("/aviation")
def aviation():
    combined_data = []
    try:
        live = (
            requests.get(
                f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}",
                timeout=8,
            )
            .json()
            .get("response", [])
        )
        combined_data = [{"status_type": "LIVE", **f} for f in live]
    except:
        pass
    return render_template(
        "aviation.html",
        flights=combined_data[:150],
        data_pay=PAYSTACK_DATA_LOGS,
        whatsapp=WHATSAPP_HUB,
    )


# --- STATIC & ASSET ROUTES ---
@app.route("/apple-touch-icon.png")
@app.route("/favicon.ico")
def serve_logo():
    return send_from_directory(os.path.join(app.root_path, "static"), "logo.png")


@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path, "static"), "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    response = make_response(render_template("sitemap.xml"))
    response.headers["Content-Type"] = "application/xml"
    return response


# Standard Routes
@app.route("/travel-planning")
def travel():
    return render_template("travel_services.html", whatsapp=WHATSAPP_HUB)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
