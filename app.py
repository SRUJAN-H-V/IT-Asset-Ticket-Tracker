from flask import Flask
from database.database import initialize_database
from routes.user_routes import user_routes
from routes.asset_routes import asset_routes

app = Flask(__name__)

# Register user routes
app.register_blueprint(user_routes)
app.register_blueprint(asset_routes)


@app.route("/")
def home():
    return "IT Asset & Ticket Tracker is running!"


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)