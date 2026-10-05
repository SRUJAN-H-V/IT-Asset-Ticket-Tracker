from database.database import get_db_connection


class User:

    @staticmethod
    def create(name, email, department, role):
        connection = get_db_connection()

        query = """
            INSERT INTO users (name, email, department, role)
            VALUES (?, ?, ?, ?)
        """

        cursor = connection.execute(
            query,
            (name, email, department, role)
        )

        connection.commit()
        user_id = cursor.lastrowid
        connection.close()

        return user_id

    @staticmethod
    def get_all():
        connection = get_db_connection()

        users = connection.execute(
            "SELECT * FROM users ORDER BY user_id DESC"
        ).fetchall()

        connection.close()

        return users

    @staticmethod
    def get_by_id(user_id):
        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        connection.close()

        return user

    @staticmethod
    def update(user_id, name, email, department, role):
        connection = get_db_connection()

        query = """
            UPDATE users
            SET name = ?, email = ?, department = ?, role = ?
            WHERE user_id = ?
        """

        connection.execute(
            query,
            (name, email, department, role, user_id)
        )

        connection.commit()
        connection.close()

    @staticmethod
    def delete(user_id):
        connection = get_db_connection()

        connection.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,)
        )

        connection.commit()
        connection.close()