import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Establishes connection to the ecommerce_db."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="varun", 
        database="ecommerce_db"
    )

def execute_read_query(sql_query: str, max_rows: int = 100) -> dict:
    """Executes SELECT queries safely."""
    if not sql_query.strip().upper().startswith("SELECT"):
        return {"status": "error", "error": "Only SELECT allowed for read operations."}

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        rows = cursor.fetchmany(max_rows)
        return {
            "status": "success",
            "row_count": len(rows),
            "results": rows
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
            "last_id": cursor.lastrowid
        }
    except Error as e:
        return {"status": "error", "error": str(e)}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_db_schema() -> dict:
    """Fetches table names and their column structures so the agent knows the schema."""
    query = """
        SELECT table_name, column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'ecommerce_db'
        ORDER BY table_name, ordinal_position;
    """
    return execute_read_query(query)