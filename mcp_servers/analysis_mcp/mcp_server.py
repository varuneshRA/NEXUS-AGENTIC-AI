import os
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tools.viz_tools import generate_visual, OUTPUT_DIR

mcp = FastMCP(name="nexus-analytics-suite")


@mcp.tool()
def create_chart(data: list, chart_type: str, x: str, y: str = None, title: str = None) -> dict:
    """
    Generates a chart and saves it as a PNG file.
    Supported chart types: 'bar', 'line', 'pie', 'scatter', 'heatmap'.
    Returns the file path of the saved chart.
    """
    return generate_visual(data, chart_type, x, y, title)


app = mcp.streamable_http_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/plots", StaticFiles(directory=OUTPUT_DIR), name="plots")

if __name__ == "__main__":
    import uvicorn
    print(f"Analytics MCP running at http://localhost:8002/mcp")
    print(f"Plots directory: {OUTPUT_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8002)
