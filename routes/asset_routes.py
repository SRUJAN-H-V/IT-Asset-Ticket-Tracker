from flask import Blueprint, request, jsonify
from models.asset import Asset
import sqlite3

asset_routes = Blueprint("asset_routes", __name__)


# =========================
# CREATE ASSET
# =========================

@asset_routes.route("/assets", methods=["POST"])
def create_asset():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    asset_tag = data.get("asset_tag")
    asset_type = data.get("asset_type")
    brand = data.get("brand")
    model = data.get("model")
    serial_number = data.get("serial_number")
    status = data.get("status", "Available")
    purchase_date = data.get("purchase_date")
    assigned_user_id = data.get("assigned_user_id")

    if not asset_tag or not asset_type or not brand or not serial_number:
        return jsonify({
            "error": "Asset tag, asset type, brand and serial number are required"
        }), 400

    valid_statuses = [
        "Available",
        "Assigned",
        "Under Repair",
        "Retired"
    ]

    if status not in valid_statuses:
        return jsonify({
            "error": "Invalid asset status"
        }), 400

    try:

        asset_id = Asset.create(
            asset_tag,
            asset_type,
            brand,
            model,
            serial_number,
            status,
            purchase_date,
            assigned_user_id
        )

        return jsonify({
            "message": "Asset created successfully",
            "asset_id": asset_id
        }), 201

    except sqlite3.IntegrityError as error:

        return jsonify({
            "error": "Asset tag or serial number already exists"
        }), 409


# =========================
# GET ALL ASSETS
# =========================

@asset_routes.route("/assets", methods=["GET"])
def get_assets():

    assets = Asset.get_all()

    asset_list = []

    for asset in assets:
        asset_list.append(dict(asset))

    return jsonify(asset_list), 200


# =========================
# GET ONE ASSET
# =========================

@asset_routes.route("/assets/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):

    asset = Asset.get_by_id(asset_id)

    if asset is None:
        return jsonify({
            "error": "Asset not found"
        }), 404

    return jsonify(dict(asset)), 200


# =========================
# UPDATE ASSET
# =========================

@asset_routes.route("/assets/<int:asset_id>", methods=["PUT"])
def update_asset(asset_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    asset = Asset.get_by_id(asset_id)

    if asset is None:
        return jsonify({
            "error": "Asset not found"
        }), 404

    asset_tag = data.get("asset_tag")
    asset_type = data.get("asset_type")
    brand = data.get("brand")
    model = data.get("model")
    serial_number = data.get("serial_number")
    status = data.get("status")
    purchase_date = data.get("purchase_date")
    assigned_user_id = data.get("assigned_user_id")

    if not asset_tag or not asset_type or not brand or not serial_number:
        return jsonify({
            "error": "Asset tag, asset type, brand and serial number are required"
        }), 400

    valid_statuses = [
        "Available",
        "Assigned",
        "Under Repair",
        "Retired"
    ]

    if status not in valid_statuses:
        return jsonify({
            "error": "Invalid asset status"
        }), 400

    try:

        Asset.update(
            asset_id,
            asset_tag,
            asset_type,
            brand,
            model,
            serial_number,
            status,
            purchase_date,
            assigned_user_id
        )

        return jsonify({
            "message": "Asset updated successfully"
        }), 200

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "Asset tag or serial number already exists"
        }), 409


# =========================
# DELETE ASSET
# =========================

@asset_routes.route("/assets/<int:asset_id>", methods=["DELETE"])
def delete_asset(asset_id):

    asset = Asset.get_by_id(asset_id)

    if asset is None:
        return jsonify({
            "error": "Asset not found"
        }), 404

    Asset.delete(asset_id)

    return jsonify({
        "message": "Asset deleted successfully"
    }), 200