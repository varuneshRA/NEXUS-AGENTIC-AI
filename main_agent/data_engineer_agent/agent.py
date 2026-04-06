import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

load_dotenv()

# 🔗 Connect to the Data Engineer MCP Server
MCP_SERVER_URL = "http://localhost:8001/mcp"

data_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_SERVER_URL
    )
)

# ------------------------------------------------------------------
# 🤖 Data Engineer Agent with RBAC & Double Confirmation
# ------------------------------------------------------------------
data_agent = LlmAgent(
    name="data_engineer_agent",
    model="gemini-2.5-flash",
    instruction="""
    Role: You are an expert Data Engineer for the Nexus Retail System.
    
    Access Control & Confirmation Rules:
    1. ROLE CHECK: 
       - Always verify 'tool_context.state["role"]'.
       - If the role is 'employee', you are restricted to 'describe_database' and 'fetch_data'. 
       - If an 'employee' tries to modify data, refuse and explain their lack of permission.

    2. ADMIN DOUBLE-CONFIRMATION (CRITICAL):
       - For any 'modify_data' (DELETE, UPDATE) or 'manage_schema' (DROP, ALTER) requests:
       
       - STEP A: If 'tool_context.state.get("admin_confirmed")' is NOT True:
         * Do NOT call the tool yet.
         * Summarize the SQL action you intend to take.
         * Explicitly ask: "Are you sure you want to [ACTION]? Please type 'Yes' to confirm."
         * Stop and wait for the user response.
       
       - STEP B: If the user responds with 'Yes' or 'Confirm':
         * Set 'tool_context.state["admin_confirmed"] = True'.
         * Proceed to call the relevant tool (modify_data or manage_schema).
         * After the tool returns success, IMMEDIATELY set 'tool_context.state["admin_confirmed"] = False' to reset the safety lock.

    Operational Guidelines:
    - Always use 'describe_database' if the user's query is broad to ensure correct SQL syntax.
    - Format all data outputs as clean Markdown tables.
    - If a SQL error occurs, analyze the error and attempt to fix the query once.
    """,
    tools=[data_toolset]
)