from flask import Blueprint, request, jsonify
from models.ticket import Ticket
import sqlite3

ticket_routes = Blueprint("ticket_routes", __name__)


# =========================
# CREATE TICKET
# =========================

@ticket_routes.route("/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority", "Medium")
    status = data.get("status", "Open")
    user_id = data.get("user_id")
    asset_id = data.get("asset_id")
    technician_id = data.get("technician_id")

    if not title or not description or not user_id:
        return jsonify({
            "error": "Title, description and user_id are required"
        }), 400

    valid_priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    if priority not in valid_priorities:
        return jsonify({
            "error": "Invalid ticket priority"
        }), 400

    valid_statuses = [
        "Open",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if status not in valid_statuses:
        return jsonify({
            "error": "Invalid ticket status"
        }), 400

    try:

        ticket_id = Ticket.create(
            title,
            description,
            priority,
            status,
            user_id,
            asset_id,
            technician_id
        )

        return jsonify({
            "message": "Ticket created successfully",
            "ticket_id": ticket_id
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "Invalid user, asset or technician ID"
        }), 400


# =========================
# GET ALL TICKETS + SEARCH/FILTER
# =========================

@ticket_routes.route("/tickets", methods=["GET"])
def get_tickets():

    status = request.args.get("status")
    priority = request.args.get("priority")
    user_id = request.args.get("user_id")

    # Validate user_id
    if user_id:

        try:
            user_id = int(user_id)

        except ValueError:

            return jsonify({
                "error": "user_id must be a number"
            }), 400

    # Validate status
    valid_statuses = [
        "Open",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if status and status not in valid_statuses:

        return jsonify({
            "error": "Invalid ticket status"
        }), 400

    # Validate priority
    valid_priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    if priority and priority not in valid_priorities:

        return jsonify({
            "error": "Invalid ticket priority"
        }), 400

    tickets = Ticket.get_all(
        status=status,
        priority=priority,
        user_id=user_id
    )

    ticket_list = []

    for ticket in tickets:
        ticket_list.append(dict(ticket))

    return jsonify(ticket_list), 200


# =========================
# GET ONE TICKET
# =========================

@ticket_routes.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):

    ticket = Ticket.get_by_id(ticket_id)

    if ticket is None:

        return jsonify({
            "error": "Ticket not found"
        }), 404

    return jsonify(dict(ticket)), 200


# =========================
# UPDATE TICKET
# =========================

@ticket_routes.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    ticket = Ticket.get_by_id(ticket_id)

    if ticket is None:

        return jsonify({
            "error": "Ticket not found"
        }), 404

    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority")
    status = data.get("status")
    user_id = data.get("user_id")
    asset_id = data.get("asset_id")
    technician_id = data.get("technician_id")

    if not title or not description or not user_id:

        return jsonify({
            "error": "Title, description and user_id are required"
        }), 400

    valid_priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    if priority not in valid_priorities:

        return jsonify({
            "error": "Invalid ticket priority"
        }), 400

    valid_statuses = [
        "Open",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if status not in valid_statuses:

        return jsonify({
            "error": "Invalid ticket status"
        }), 400

    try:

        Ticket.update(
            ticket_id,
            title,
            description,
            priority,
            status,
            user_id,
            asset_id,
            technician_id
        )

        return jsonify({
            "message": "Ticket updated successfully"
        }), 200

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "Invalid user, asset or technician ID"
        }), 400


# =========================
# DELETE TICKET
# =========================

@ticket_routes.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):

    ticket = Ticket.get_by_id(ticket_id)

    if ticket is None:

        return jsonify({
            "error": "Ticket not found"
        }), 404

    Ticket.delete(ticket_id)

    return jsonify({
        "message": "Ticket deleted successfully"
    }), 200