import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

# Import the generalized specialized tools
# Note: Ensure your folder is named 'tools' or adjust the import path
from tools.viz_tools import generate_visual, OUTPUT_DIR

mcp = FastMCP(name="nexus-analytics-suite")

# --- TOOL 1: Visualization ---
@mcp.tool()
def create_chart(data: list, chart_type: str, x: str, y: str = None, title: str = None) -> dict:
    """
    Generates professional plots/charts. 
    Supported: 'bar', 'line', 'pie', 'scatter', 'heatmap'.
    """
    return generate_visual(data, chart_type, x, y, title)


# --- App Configuration ---
app = mcp.streamable_http_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the directory exists before mounting
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount the static plots folder
app.mount("/plots", StaticFiles(directory=OUTPUT_DIR), name="plots")

if __name__ == "__main__":
    # Port 8002 to stay separate from the Data Engineer MCP (8001)
    print(f"🚀 Nexus Analytics Suite (Viz + ML + Decision) active on Port 8002")
    print(f"📁 Plots directory: {OUTPUT_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8002)