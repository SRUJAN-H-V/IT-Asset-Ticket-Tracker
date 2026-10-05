from database.database import get_db_connection


class Ticket:

    @staticmethod
    def create(
        title,
        description,
        priority,
        status,
        user_id,
        asset_id,
        technician_id
    ):

        connection = get_db_connection()

        query = """
            INSERT INTO tickets (
                title,
                description,
                priority,
                status,
                user_id,
                asset_id,
                technician_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor = connection.execute(
            query,
            (
                title,
                description,
                priority,
                status,
                user_id,
                asset_id,
                technician_id
            )
        )

        connection.commit()

        ticket_id = cursor.lastrowid

        connection.close()

        return ticket_id

    @staticmethod
    def get_all(status=None, priority=None, user_id=None): 

        connection = get_db_connection()

        query = "SELECT * FROM tickets WHERE 1=1"
        parameters = []

        if status:
            query += " AND status = ?"
            parameters.append(status)

        if priority:
            query += " AND priority = ?"
            parameters.append(priority)

        if user_id:
            query += " AND user_id = ?"
            parameters.append(user_id)

        query += " ORDER BY ticket_id DESC"

        tickets = connection.execute(
            query,
            parameters
        ).fetchall()

        connection.close()

        return tickets

    @staticmethod
    def get_by_id(ticket_id):

        connection = get_db_connection()

        ticket = connection.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?",
            (ticket_id,)
        ).fetchone()

        connection.close()

        return ticket

    @staticmethod
    def update(
        ticket_id,
        title,
        description,
        priority,
        status,
        user_id,
        asset_id,
        technician_id
    ):

        connection = get_db_connection()

        query = """
            UPDATE tickets
            SET
                title = ?,
                description = ?,
                priority = ?,
                status = ?,
                user_id = ?,
                asset_id = ?,
                technician_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE ticket_id = ?
        """

        connection.execute(
            query,
            (
                title,
                description,
                priority,
                status,
                user_id,
                asset_id,
                technician_id,
                ticket_id
            )
        )

        connection.commit()

        connection.close()

    @staticmethod
    def delete(ticket_id):

        connection = get_db_connection()

        connection.execute(
            "DELETE FROM tickets WHERE ticket_id = ?",
            (ticket_id,)
        )

        connection.commit()

        connection.close()