import logging
import os
import requests

from dotenv import load_dotenv

from flask import Flask, render_template, jsonify

app = Flask(__name__)

load_dotenv()

logger = logging.getLogger(__name__)


PORT = os.environ.get("PORT", 5000)
SITES = [
    {"name": site[0], "url": site[1]}
    for site in [s.split("|") for s in os.environ.get("SITES").split(",")]
]
TIMEOUT = 5


@app.route("/")
def index():
    return render_template("index.html", sites=SITES)


@app.route("/check-health")
def check_health():
    health = {}

    for site in SITES:
        try:
            logger.info("Checking health for %s", site["name"])
            response = requests.get(site["url"], timeout=TIMEOUT)
            health[site["name"]] = response.status_code == 200
        except Exception as e:
            logger.error("Error checking health for %s: %s", site["name"], e)
            health[site["name"]] = False

    return jsonify(health)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
