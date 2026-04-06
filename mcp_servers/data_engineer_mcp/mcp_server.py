from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from tools import execute_read_query, execute_write_query, get_db_schema

mcp = FastMCP(name="ecommerce-data-engineer")

# --- TOOL 1: Schema Exploration ---
@mcp.tool()
def describe_database() -> dict:
    """Get the list of all tables and columns in the ecommerce database. 
    Use this first to understand the data structure."""
    return get_db_schema()

# --- TOOL 2: Read Data ---
@mcp.tool()
def fetch_data(sql_query: str) -> dict:
    """Execute a SELECT query to analyze data. 
    Example: 'SELECT * FROM products WHERE price > 500'"""
    return execute_read_query(sql_query)

# --- TOOL 3: Modify Data (Write/Update/Delete) ---
@mcp.tool()
def modify_data(sql_query: str) -> dict:
    """Execute INSERT, UPDATE, or DELETE statements.
    Example: 'UPDATE products SET price = 899 WHERE product_id = 1'"""
    return execute_write_query(sql_query)

# --- TOOL 4: Schema Management (DDL) ---
@mcp.tool()
def manage_schema(sql_query: str) -> dict:
    """Execute CREATE TABLE or ALTER TABLE statements to modify database structure."""
    return execute_write_query(sql_query)

# --- Server Setup ---
app = mcp.streamable_http_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Ecommerce Data Engineer MCP running at http://localhost:8001/mcp")
    uvicorn.run(app, host="0.0.0.0", port=8001)