from database.database import get_db_connection


class Dashboard:

    @staticmethod
    def get_statistics():

        connection = get_db_connection()

        # =========================
        # Asset statistics
        # =========================

        total_assets = connection.execute(
            "SELECT COUNT(*) AS count FROM assets"
        ).fetchone()["count"]

        assigned_assets = connection.execute(
            "SELECT COUNT(*) AS count FROM assets WHERE status = 'Assigned'"
        ).fetchone()["count"]

        available_assets = connection.execute(
            "SELECT COUNT(*) AS count FROM assets WHERE status = 'Available'"
        ).fetchone()["count"]

        repair_assets = connection.execute(
            "SELECT COUNT(*) AS count FROM assets WHERE status = 'Under Repair'"
        ).fetchone()["count"]

        retired_assets = connection.execute(
            "SELECT COUNT(*) AS count FROM assets WHERE status = 'Retired'"
        ).fetchone()["count"]

        # =========================
        # Ticket statistics
        # =========================

        total_tickets = connection.execute(
            "SELECT COUNT(*) AS count FROM tickets"
        ).fetchone()["count"]

        open_tickets = connection.execute(
            "SELECT COUNT(*) AS count FROM tickets WHERE status = 'Open'"
        ).fetchone()["count"]

        assigned_tickets = connection.execute(
            "SELECT COUNT(*) AS count FROM tickets WHERE status = 'Assigned'"
        ).fetchone()["count"]

        in_progress_tickets = connection.execute(
            "SELECT COUNT(*) AS count FROM tickets WHERE status = 'In Progress'"
        ).fetchone()["count"]

        resolved_tickets = connection.execute(
            "SELECT COUNT(*) AS count FROM tickets WHERE status = 'Resolved'"
        ).fetchone()["count"]

        closed_tickets = connection.execute(
            "SELECT COUNT(*) AS count FROM tickets WHERE status = 'Closed'"
        ).fetchone()["count"]

        high_priority_tickets = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM tickets
            WHERE priority IN ('High', 'Critical')
            """
        ).fetchone()["count"]

        # =========================
        # Asset type statistics
        # =========================

        asset_types = connection.execute(
            """
            SELECT asset_type, COUNT(*) AS count
            FROM assets
            GROUP BY asset_type
            ORDER BY count DESC
            """
        ).fetchall()

        asset_type_statistics = {}

        for row in asset_types:
            asset_type_statistics[row["asset_type"]] = row["count"]

        # =========================
        # Department-wise tickets
        # =========================

        department_tickets = connection.execute(
            """
            SELECT users.department, COUNT(tickets.ticket_id) AS count
            FROM tickets
            JOIN users ON tickets.user_id = users.user_id
            GROUP BY users.department
            ORDER BY count DESC
            """
        ).fetchall()

        department_statistics = {}

        for row in department_tickets:
            department_statistics[row["department"]] = row["count"]

        # Close database connection
        connection.close()

        # =========================
        # Return dashboard data
        # =========================

        return {
            "assets": {
                "total": total_assets,
                "assigned": assigned_assets,
                "available": available_assets,
                "under_repair": repair_assets,
                "retired": retired_assets,
                "by_type": asset_type_statistics
            },

            "tickets": {
                "total": total_tickets,
                "open": open_tickets,
                "assigned": assigned_tickets,
                "in_progress": in_progress_tickets,
                "resolved": resolved_tickets,
                "closed": closed_tickets,
                "high_priority": high_priority_tickets,
                "by_department": department_statistics
            }
        }