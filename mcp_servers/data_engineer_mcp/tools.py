import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

_DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ecommerce_db"),
}


def get_db_connection():
    """Establishes a connection to the ecommerce_db."""
    return mysql.connector.connect(**_DB_CONFIG)


def execute_read_query(sql_query: str, max_rows: int = 100) -> dict:
    """Executes SELECT queries safely."""
    if not sql_query.strip().upper().startswith("SELECT"):
        return {"status": "error", "error": "Only SELECT statements are allowed for read operations."}

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        rows = cursor.fetchmany(max_rows)
        return {
            "status": "success",
            "row_count": len(rows),
            "results": rows,
        }
    except Error as e:
        return {"status": "error", "error": str(e)}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def execute_write_query(sql_query: str, params: tuple = None) -> dict:
    """Handles INSERT, UPDATE, DELETE, and CREATE/ALTER operations."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query, params or ())
        conn.commit()
        return {
            "status": "success",
            "affected_rows": cursor.rowcount,
            "last_id": cursor.lastrowid,
        }
    except Error as e:
        return {"status": "error", "error": str(e)}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_db_schema() -> dict:
    """Fetches table names and their column structures."""
    query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        ORDER BY table_name, ordinal_position;
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (_DB_CONFIG["database"],))
        rows = cursor.fetchall()
        return {"status": "success", "row_count": len(rows), "results": rows}
    except Error as e:
        return {"status": "error", "error": str(e)}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
