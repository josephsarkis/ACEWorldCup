import os
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("ODDS_API_KEY", "a1100a501aa6d3b110b9a340f4254a8f")
SPORT_KEY = "soccer_fifa_world_cup"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/odds")
def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT_KEY}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "uk",
        "markets": "h2h,totals",
        "oddsFormat": "decimal"
    }
    try:
        # Fetching odds using Railway server's cloud network (avoids local ISP/firewall blocks)
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "error": f"API responded with status {response.status_code}",
                "details": response.text
            }), response.status_code
    except Exception as e:
        return jsonify({
            "error": "Failed to connect to The Odds API from cloud server",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
