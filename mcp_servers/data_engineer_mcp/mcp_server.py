from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from tools import execute_read_query, execute_write_query, get_db_schema

mcp = FastMCP(name="ecommerce-data-engineer")


@mcp.tool()
def describe_database() -> dict:
    """Get the list of all tables and columns in the ecommerce database.
    Use this first to understand the data structure before writing queries."""
    return get_db_schema()


@mcp.tool()
def fetch_data(sql_query: str) -> dict:
    """Execute a SELECT query to read data.
    Example: 'SELECT * FROM products WHERE price > 500'"""
    return execute_read_query(sql_query)


@mcp.tool()
def modify_data(sql_query: str) -> dict:
    """Execute INSERT, UPDATE, or DELETE statements.
    Example: 'UPDATE products SET price = 899 WHERE product_id = 1'"""
    return execute_write_query(sql_query)


@mcp.tool()
def manage_schema(sql_query: str) -> dict:
    """Execute CREATE TABLE or ALTER TABLE statements to modify database structure."""
    return execute_write_query(sql_query)


app = mcp.streamable_http_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    print("Data Engineer MCP running at http://localhost:8001/mcp")
    uvicorn.run(app, host="0.0.0.0", port=8001)
