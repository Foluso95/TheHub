from flask import Flask, render_template, make_response, send_from_directory, request
import requests
import os

app = Flask(__name__)

# --- CONFIGURATION ---
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"
ETH_WALLET = "0x5b2ca3bac67d28d254a16fe3341ca6a136913ed3"
PAYSTACK_LINK = "https://paystack.shop/pay/tskni695ms"


@app.route("/")
def home():
    stats = {
        "logs_delivered": 124,
        "active_queries": 8,
        "system_uptime": "99.9%",
        "global_reach": "24 Countries",
    }
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
        # Optimization: Fetching with timeout to prevent terminal hang
        live_req = requests.get(
            f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}", timeout=7
        )
        sched_req = requests.get(
            f"https://airlabs.co/api/v9/schedules?api_key={AIRLABS_API_KEY}", timeout=7
        )

        live = (
            live_req.json().get("response", []) if live_req.status_code == 200 else []
        )
        sched = (
            sched_req.json().get("response", []) if sched_req.status_code == 200 else []
        )

        combined_data = [{"status_type": "LIVE", **f} for f in live] + [
            {"status_type": "SCHEDULED", **s} for s in sched
        ]
    except:
        pass
    return render_template("aviation.html", flights=combined_data[:150])


@app.route("/support")
def support():
    # Variables passed directly to the template
    return render_template("support.html", paystack=PAYSTACK_LINK, wallet=ETH_WALLET)


# --- SEO & DISCOVERY ROUTES ---
@app.route("/llm.txt")
def llm_txt():
    return send_from_directory(os.path.join(app.root_path, "static"), "llm.txt")


@app.route("/googledadc4e071c25e5f7.html")
def google_verify():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "googledadc4e071c25e5f7.html"
    )


@app.route("/robots.txt")
def robots():
    content = (
        "User-agent: *\nAllow: /\nSitemap: https://thehubglobal.vercel.app/sitemap.xml"
    )
    return make_response(content, 200, {"Content-Type": "text/plain"})


@app.route("/sitemap.xml")
def sitemap():
    xml = render_template("sitemap.xml")
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


# Standard templates
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
