from flask import Blueprint, request, jsonify
from models.user import User
import re
import sqlite3

user_routes = Blueprint("user_routes", __name__)


# Validate email format
def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


# Validate user data
def validate_user_data(data):
    if not data:
        return "Request body is required"

    name = data.get("name")
    email = data.get("email")
    department = data.get("department")
    role = data.get("role")

    if not name or not email or not department or not role:
        return "All fields are required"

    if len(name.strip()) < 2:
        return "Name must contain at least 2 characters"

    if not is_valid_email(email):
        return "Invalid email format"

    valid_roles = ["Employee", "Technician", "Admin"]

    if role not in valid_roles:
        return "Role must be Employee, Technician, or Admin"

    return None


# =========================
# CREATE USER
# =========================

@user_routes.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    error = validate_user_data(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    name = data.get("name").strip()
    email = data.get("email").strip()
    department = data.get("department").strip()
    role = data.get("role")

    try:
        user_id = User.create(
            name,
            email,
            department,
            role
        )

        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409


# =========================
# GET ALL USERS
# =========================

@user_routes.route("/users", methods=["GET"])
def get_users():

    users = User.get_all()

    user_list = []

    for user in users:
        user_list.append(dict(user))

    return jsonify(user_list), 200


# =========================
# GET ONE USER
# =========================

@user_routes.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = User.get_by_id(user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(dict(user)), 200


# =========================
# UPDATE USER
# =========================

@user_routes.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    error = validate_user_data(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    user = User.get_by_id(user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    name = data.get("name").strip()
    email = data.get("email").strip()
    department = data.get("department").strip()
    role = data.get("role")

    try:
        User.update(
            user_id,
            name,
            email,
            department,
            role
        )

        return jsonify({
            "message": "User updated successfully"
        }), 200

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409


# =========================
# DELETE USER
# =========================

@user_routes.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = User.get_by_id(user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    User.delete(user_id)

    return jsonify({
        "message": "User deleted successfully"
    }), 200