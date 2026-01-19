from flask import Flask, render_template, make_response, send_from_directory, request
import requests
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace with your flexible 'Payment Page' link
PAYSTACK_LINK = "https://paystack.com/pay/your_flexible_link"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"
WHATSAPP_HUB = "https://wa.me/2349063350998"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"


@app.route("/")
def home():
    stats = {"logs_delivered": 142, "active_queries": 12, "system_uptime": "99.9%"}
    news = []
    try:
        url = f"https://newsapi.org/v2/everything?q=aviation+intelligence&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        news = requests.get(url, timeout=5).json().get("articles", [])
    except:
        pass
    return render_template("index.html", news=news, stats=stats)


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
        sched = (
            requests.get(
                f"https://airlabs.co/api/v9/schedules?api_key={AIRLABS_API_KEY}",
                timeout=8,
            )
            .json()
            .get("response", [])
        )
        combined_data = [{"status_type": "LIVE", **f} for f in live] + [
            {"status_type": "SCHEDULED", **s} for s in sched
        ]
    except:
        pass
    return render_template("aviation.html", flights=combined_data[:150])


@app.route("/support")
def support():
    return render_template(
        "support.html", paystack=PAYSTACK_LINK, wallet=ETH_WALLET, whatsapp=WHATSAPP_HUB
    )


# --- AUTOMATED LOGO ROUTES ---
@app.route("/apple-touch-icon.png")
@app.route("/favicon-32x32.png")
@app.route("/favicon-16x16.png")
@app.route("/favicon.ico")
def serve_logo():
    # Maps all icon requests to your 'logo.png' automatically
    return send_from_directory(os.path.join(app.root_path, "static"), "logo.png")


# --- SEO & DISCOVERY ---
@app.route("/llm.txt")
def llm_txt():
    return send_from_directory(os.path.join(app.root_path, "static"), "llm.txt")


@app.route("/sitemap.xml")
def sitemap():
    response = make_response(render_template("sitemap.xml"))
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route("/googledadc4e071c25e5f7.html")
def google_verify():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "googledadc4e071c25e5f7.html"
    )


# Static Pages
@app.route("/travel-planning")
def travel():
    return render_template("travel_services.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
