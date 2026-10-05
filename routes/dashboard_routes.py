from flask import Blueprint, jsonify, render_template
from models.dashboard import Dashboard


dashboard_routes = Blueprint("dashboard_routes", __name__)


# =========================
# DASHBOARD PAGE
# =========================

@dashboard_routes.route("/dashboard", methods=["GET"])
def dashboard_page():

    return render_template("dashboard.html")


# =========================
# DASHBOARD API
# =========================

@dashboard_routes.route("/api/dashboard", methods=["GET"])
def dashboard_api():

    statistics = Dashboard.get_statistics()

    return jsonify(statistics), 200
