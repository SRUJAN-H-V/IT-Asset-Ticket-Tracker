from database.database import get_db_connection


class Asset:

    @staticmethod
    def create(asset_tag, asset_type, brand, model, serial_number,
               status, purchase_date, assigned_user_id):

        connection = get_db_connection()

        query = """
            INSERT INTO assets (
                asset_tag,
                asset_type,
                brand,
                model,
                serial_number,
                status,
                purchase_date,
                assigned_user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor = connection.execute(
            query,
            (
                asset_tag,
                asset_type,
                brand,
                model,
                serial_number,
                status,
                purchase_date,
                assigned_user_id
            )
        )

        connection.commit()

        asset_id = cursor.lastrowid

        connection.close()

        return asset_id

    @staticmethod
    def get_all(status=None, asset_type=None, brand=None):

        connection = get_db_connection()

        query = "SELECT * FROM assets WHERE 1=1"
        parameters = []

        if status:
            query += " AND status = ?"
            parameters.append(status)

        if asset_type:
            query += " AND asset_type = ?"
            parameters.append(asset_type)

        if brand:
            query += " AND brand = ?"
            parameters.append(brand)

        query += " ORDER BY asset_id DESC"

        assets = connection.execute(
            query,
            parameters
        ).fetchall()

        connection.close()

        return assets

    @staticmethod
    def get_by_id(asset_id):

        connection = get_db_connection()

        asset = connection.execute(
            "SELECT * FROM assets WHERE asset_id = ?",
            (asset_id,)
        ).fetchone()

        connection.close()

        return asset

    @staticmethod
    def update(
        asset_id,
        asset_tag,
        asset_type,
        brand,
        model,
        serial_number,
        status,
        purchase_date,
        assigned_user_id
    ):

        connection = get_db_connection()

        query = """
            UPDATE assets
            SET
                asset_tag = ?,
                asset_type = ?,
                brand = ?,
                model = ?,
                serial_number = ?,
                status = ?,
                purchase_date = ?,
                assigned_user_id = ?
            WHERE asset_id = ?
        """

        connection.execute(
            query,
            (
                asset_tag,
                asset_type,
                brand,
                model,
                serial_number,
                status,
                purchase_date,
                assigned_user_id,
                asset_id
            )
        )

        connection.commit()

        connection.close()

    @staticmethod
    def delete(asset_id):

        connection = get_db_connection()

        connection.execute(
            "DELETE FROM assets WHERE asset_id = ?",
            (asset_id,)
        )

        connection.commit()

        connection.close()