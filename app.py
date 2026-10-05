from flask import Flask
from database.database import initialize_database

app = Flask(__name__)


@app.route("/")
def home():
    return "IT Asset & Ticket Tracker is running!"


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)