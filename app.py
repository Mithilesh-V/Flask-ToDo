import pandas as pd
import sqlite3
from flask import Flask,render_template,request

app = Flask(__name__)


def connect_to_db(database):
    conn = sqlite3.connect(database)
    return conn

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
