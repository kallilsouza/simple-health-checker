import os
from dotenv import load_dotenv

from flask import Flask, render_template

app = Flask(__name__)

load_dotenv()


SITES = [
    {"name": site[0], "url": site[1]}
    for site in [s.split("|") for s in os.environ.get("SITES").split(",")]
]


@app.route("/")
def index():
    return render_template("index.html", sites=SITES)


if __name__ == "__main__":
    app.run(debug=True)
