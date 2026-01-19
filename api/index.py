from flask import Flask, render_template, make_response, send_from_directory
import requests
import os

app = Flask(__name__)

# --- CONFIGURATION ---
NEWS_API_KEY = "39bbc467ab07459396692bfbc8564151"
AIRLABS_API_KEY = "e6f87644-fdb1-4963-a391-1d66b790ded0"


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


# --- SEO, VERIFICATION & AI DISCOVERY ---


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


@app.route("/apple-touch-icon.png")
def apple_touch():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "apple-touch-icon.png"
    )


# --- OTHER ROUTES ---
@app.route("/aviation")
def aviation():
    # Existing aviation logic remains here
    return render_template("aviation.html", flights=[])


@app.route("/travel-planning")
def travel():
    return render_template("travel_services.html")


@app.route("/support")
def support():
    return render_template("support.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
